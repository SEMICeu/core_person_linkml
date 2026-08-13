from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import sys
import tempfile
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDFS, XSD
from rdflib.compare import isomorphic, to_canonical_graph


SH = Namespace("http://www.w3.org/ns/shacl#")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST = PROJECT_ROOT / "config" / "baseline-sources.json"
PROFILE_MANIFEST = PROJECT_ROOT / "config" / "validation-profiles.json"
DEFAULT_SOURCE_ROOT = PROJECT_ROOT / "generated" / "baseline" / "sources"
DEFAULT_REPORT_ROOT = PROJECT_ROOT / "generated" / "baseline" / "reports"
DEFAULT_CACHE_ROOT = PROJECT_ROOT / "generated" / ".cache"

CONSTRAINT_PREDICATES = (
    "and", "class", "closed", "datatype", "disjoint", "equals", "flags",
    "hasValue", "in", "languageIn", "lessThan", "lessThanOrEquals",
    "maxCount", "maxExclusive", "maxInclusive", "maxLength", "minCount",
    "minExclusive", "minInclusive", "minLength", "node", "nodeKind", "not",
    "or", "pattern", "qualifiedMaxCount", "qualifiedMinCount",
    "qualifiedValueShape", "uniqueLang", "xone",
)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _artifact_index() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in _read_json(SOURCE_MANIFEST)["artifacts"]}


def _artifact_url(item: dict[str, Any], manifest: dict[str, Any]) -> str:
    repository = manifest["repositories"][item["repository"]]
    return f"{repository['raw_base']}/{repository['commit']}/{item['path']}"


def _artifact_path(item: dict[str, Any], source_root: Path) -> Path:
    destination = (source_root / item["repository"] / item["path"]).resolve()
    root = source_root.resolve()
    if root != destination and root not in destination.parents:
        raise ValueError(f"Artifact path escapes source root: {item['path']}")
    return destination


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def artifact_path_by_id(artifact_id: str, source_root: Path = DEFAULT_SOURCE_ROOT) -> Path:
    artifacts = _artifact_index()
    if artifact_id not in artifacts:
        raise KeyError(f"Unknown artifact: {artifact_id}")
    return _artifact_path(artifacts[artifact_id], source_root)


def verify_sources(source_root: Path = DEFAULT_SOURCE_ROOT) -> list[dict[str, Any]]:
    results = []
    for item in _read_json(SOURCE_MANIFEST)["artifacts"]:
        path = _artifact_path(item, source_root)
        exists = path.is_file()
        actual_size = path.stat().st_size if exists else None
        actual_hash = _sha256(path) if exists else None
        results.append({
            "id": item["id"], "path": _display_path(path), "exists": exists,
            "expected_bytes": item["bytes"], "actual_bytes": actual_size,
            "expected_sha256": item["sha256"], "actual_sha256": actual_hash,
            "verified": exists and actual_size == item["bytes"] and actual_hash == item["sha256"],
        })
    return results


def fetch_sources(source_root: Path = DEFAULT_SOURCE_ROOT) -> list[dict[str, Any]]:
    manifest = _read_json(SOURCE_MANIFEST)
    for item in manifest["artifacts"]:
        destination = _artifact_path(item, source_root)
        if (destination.is_file() and destination.stat().st_size == item["bytes"]
                and _sha256(destination) == item["sha256"]):
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            _artifact_url(item, manifest),
            headers={"User-Agent": "semic-linkml-baseline/0.1"},
        )
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".part", dir=destination.parent
        )
        os.close(fd)
        temporary = Path(temporary_name)
        try:
            with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as stream:
                while block := response.read(1024 * 1024):
                    stream.write(block)
            if temporary.stat().st_size != item["bytes"]:
                raise RuntimeError(f"Size mismatch for {item['id']}")
            if _sha256(temporary) != item["sha256"]:
                raise RuntimeError(f"SHA-256 mismatch for {item['id']}")
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
    return verify_sources(source_root)


def load_profile_graph(profile_id: str, source_root: Path = DEFAULT_SOURCE_ROOT) -> Graph:
    profiles = _read_json(PROFILE_MANIFEST)["profiles"]
    if profile_id not in profiles:
        raise KeyError(f"Unknown validation profile: {profile_id}")
    artifacts = _artifact_index()
    graph = Graph()
    for artifact_id in profiles[profile_id]["artifacts"]:
        item = artifacts[artifact_id]
        path = _artifact_path(item, source_root)
        if not path.is_file():
            raise FileNotFoundError(f"Missing {artifact_id}: {path}. Run 'semic-baseline fetch' first.")
        graph.parse(path, format="turtle")
    return graph


def _path_kind(graph: Graph, path: URIRef | BNode | Literal) -> str:
    if isinstance(path, URIRef):
        return "direct"
    tests = (
        (SH.inversePath, "inverse"), (SH.alternativePath, "alternative"),
        (SH.zeroOrMorePath, "zero-or-more"), (SH.oneOrMorePath, "one-or-more"),
        (SH.zeroOrOnePath, "zero-or-one"), (RDF.first, "sequence"),
    )
    for predicate, label in tests:
        if (path, predicate, None) in graph:
            return label
    return "other-blank-node"


def inventory_graph(graph: Graph) -> dict[str, Any]:
    node_shapes = set(graph.subjects(RDF.type, SH.NodeShape))
    typed_property_shapes = set(graph.subjects(RDF.type, SH.PropertyShape))
    property_shapes = typed_property_shapes | set(graph.objects(None, SH.property))
    paths = [path for shape in property_shapes for path in graph.objects(shape, SH.path)]
    return {
        "triples": len(graph),
        "node_shapes": len(node_shapes),
        "property_shapes": len(property_shapes),
        "typed_property_shapes": len(typed_property_shapes),
        "targets": {name: len(set(graph.subjects(SH[name], None))) for name in (
            "targetClass", "targetNode", "targetObjectsOf", "targetSubjectsOf")},
        "constraints": {name: len(set(graph.subjects(SH[name], None))) for name in CONSTRAINT_PREDICATES},
        "path_kinds": dict(sorted(Counter(_path_kind(graph, path) for path in paths).items())),
        "severities": dict(sorted(Counter(str(value) for value in graph.objects(None, SH.severity)).items())),
        "messages": len(set(graph.subjects(SH.message, None))),
    }


def _canonical_lines(graph: Graph) -> set[str]:
    canonical = to_canonical_graph(graph)
    return {f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in canonical}


def canonical_ntriples(graph: Graph) -> str:
    """Return deterministic N-Triples, a strict subset of Turtle."""
    return "\n".join(sorted(_canonical_lines(graph))) + "\n"


def normalize_generated_shacl(graph: Graph) -> Graph:
    """Remove generator-only ordering noise from semantically unordered lists."""
    for subject, head in list(graph.subject_objects(SH.ignoredProperties)):
        values = list(Collection(graph, head))
        Collection(graph, head).clear()
        graph.remove((subject, SH.ignoredProperties, head))
        new_head = BNode()
        Collection(graph, new_head, sorted(values, key=lambda value: value.n3()))
        graph.add((subject, SH.ignoredProperties, new_head))
    return graph


def apply_semic_shacl_extensions(graph: Graph, generator: Any) -> Graph:
    """Apply explicit SEMIC annotations/types that stock LinkML cannot express."""
    schema_view = generator.schemaview
    rdfs_literal = URIRef(str(RDFS.Literal))
    # sh:ignoredProperties has no effect on open shapes and is absent from the
    # official Core Person distribution.
    for shape in set(graph.subjects(RDF.type, SH.NodeShape)):
        for head in list(graph.objects(shape, SH.ignoredProperties)):
            Collection(graph, head).clear()
            graph.remove((shape, SH.ignoredProperties, head))
    for class_definition in schema_view.all_classes(imports=False).values():
        shape = URIRef(schema_view.get_uri(class_definition, expand=True))
        for slot in schema_view.class_induced_slots(class_definition.name):
            slot_uri = URIRef(schema_view.get_uri(slot, expand=True))
            property_shapes = {
                node
                for node in graph.objects(shape, SH.property)
                if (node, SH.path, slot_uri) in graph
            }
            for property_shape in property_shapes:
                if slot.range == "rdf_literal":
                    graph.remove((property_shape, SH.datatype, rdfs_literal))
                    graph.remove((property_shape, SH.nodeKind, None))
                    graph.add((property_shape, SH.nodeKind, SH.Literal))
                elif slot.range == "any_uri_literal":
                    graph.remove((property_shape, SH.nodeKind, None))
                    graph.add((property_shape, SH.nodeKind, SH.Literal))
                    graph.add((property_shape, SH.datatype, XSD.anyURI))
                annotations = slot.annotations or {}
                annotation = (
                    annotations.get("semic_unique_lang")
                    if isinstance(annotations, dict)
                    else getattr(annotations, "semic_unique_lang", None)
                )
                if annotation is not None and bool(annotation.value):
                    graph.add((property_shape, SH.uniqueLang, Literal(True)))
    if schema_view.schema.name == "core_person_2_1_2":
        # Official compatibility shapes target RDF datatype IRIs. They are
        # publication artifacts, not ordinary LinkML object classes.
        for target in (XSD.date, RDFS.Literal, RDF.langString, XSD.anyURI):
            graph.add((target, RDF.type, SH.NodeShape))
            graph.add((target, SH.targetClass, target))
            graph.add((target, SH.closed, Literal(False)))
    return graph


def compare_graphs(reference: Graph, candidate: Graph) -> dict[str, Any]:
    reference_lines, candidate_lines = _canonical_lines(reference), _canonical_lines(candidate)
    reference_inventory, candidate_inventory = inventory_graph(reference), inventory_graph(candidate)
    return {
        "isomorphic": isomorphic(reference, candidate),
        "reference": reference_inventory,
        "candidate": candidate_inventory,
        "inventory_delta": {
            "triples": candidate_inventory["triples"] - reference_inventory["triples"],
            "node_shapes": candidate_inventory["node_shapes"] - reference_inventory["node_shapes"],
            "property_shapes": candidate_inventory["property_shapes"] - reference_inventory["property_shapes"],
            "constraints": {key: candidate_inventory["constraints"][key] - reference_inventory["constraints"][key]
                            for key in CONSTRAINT_PREDICATES},
        },
        "canonical_triples_only_in_reference": len(reference_lines - candidate_lines),
        "canonical_triples_only_in_candidate": len(candidate_lines - reference_lines),
    }


def validate_data(profile_id: str, data_path: Path,
                  source_root: Path = DEFAULT_SOURCE_ROOT) -> dict[str, Any]:
    from pyshacl import validate
    shapes, data = load_profile_graph(profile_id, source_root), Graph().parse(data_path)
    conforms, result_graph, result_text = validate(
        data, shacl_graph=shapes, inference="none", advanced=False,
        meta_shacl=False, do_owl_imports=False, allow_infos=False, allow_warnings=False,
    )
    return {
        "profile": profile_id, "data": _display_path(data_path), "conforms": bool(conforms),
        "result_count": len(set(result_graph.subjects(RDF.type, SH.ValidationResult))),
        "result_text": result_text.replace("\r\n", "\n").replace("\r", "\n"),
    }


def generate_shacl(
    schema_path: Path,
    output_path: Path,
    *,
    open_shapes: bool = False,
    semic_extensions: bool = False,
) -> Path:
    # LinkML imports prefixmaps/curies, which initializes PyStow. Keep that
    # implicit cache inside the project instead of depending on user-home access.
    os.environ.setdefault("PYSTOW_HOME", str(DEFAULT_CACHE_ROOT / "pystow"))
    from linkml.generators.shaclgen import ShaclGenerator
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generator = ShaclGenerator(str(schema_path), closed=not open_shapes)
    generated = Graph().parse(data=generator.serialize(), format="turtle")
    if semic_extensions:
        generated = apply_semic_shacl_extensions(generated, generator)
    generated = normalize_generated_shacl(generated)
    output_path.write_text(canonical_ntriples(generated), encoding="utf-8", newline="\n")
    Graph().parse(output_path, format="turtle")
    return output_path


def generate_plantuml(schema_path: Path, output_path: Path) -> Path:
    os.environ.setdefault("PYSTOW_HOME", str(DEFAULT_CACHE_ROOT / "pystow"))
    from linkml.generators.plantumlgen import PlantumlGenerator

    output_path.parent.mkdir(parents=True, exist_ok=True)
    diagram = PlantumlGenerator(
        str(schema_path),
        format="puml",
        include_all=True,
        include_enums=True,
        preserve_names=True,
    ).serialize()
    if not diagram.startswith("@startuml") or not diagram.rstrip().endswith("@enduml"):
        raise RuntimeError("PlantUML generator returned an invalid textual diagram")
    output_path.write_text(diagram, encoding="utf-8", newline="\n")
    return output_path


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _inventory_markdown(inventories: dict[str, Any]) -> str:
    lines = [
        "# Official SHACL inventory", "",
        "Generated from checksum-verified, commit-pinned SEMIC release files.", "",
        "| Profile | Triples | Node shapes | Property shapes | Direct paths | Inverse paths |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for profile_id, item in inventories.items():
        lines.append(f"| `{profile_id}` | {item['triples']} | {item['node_shapes']} | "
                     f"{item['property_shapes']} | {item['path_kinds'].get('direct', 0)} | "
                     f"{item['path_kinds'].get('inverse', 0)} |")
    lines.extend(["", "Counts are evidence, not an equivalence verdict. Semantic equivalence also requires",
                  "normalized constraint comparison and validation-result comparison on agreed fixtures.", ""])
    return "\n".join(lines)


def run_baseline(source_root: Path = DEFAULT_SOURCE_ROOT) -> dict[str, Any]:
    verification = fetch_sources(source_root)
    if not all(item["verified"] for item in verification):
        raise RuntimeError("One or more baseline sources failed verification")
    core_person_candidate = generate_shacl(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml",
        PROJECT_ROOT / "project" / "shacl" / "core-person-candidate.ttl",
        open_shapes=True,
        semic_extensions=True,
    )
    core_person_comparison = compare_graphs(
        load_profile_graph("core-person-2.1.2", source_root),
        Graph().parse(core_person_candidate, format="turtle"),
    )
    generate_plantuml(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml",
        PROJECT_ROOT / "project" / "uml" / "core-person.puml",
    )
    report = {
        "tool_versions": {
            "python": sys.version.split()[0],
            "linkml": importlib.metadata.version("linkml"),
            "pyshacl": importlib.metadata.version("pyshacl"),
            "rdflib": importlib.metadata.version("rdflib"),
        },
        "source_verification": verification,
        "official_inventory": inventory_graph(
            load_profile_graph("core-person-2.1.2", source_root)
        ),
        "core_person_current_model_comparison": core_person_comparison,
        "decision_status": {
            "core_person_profile": "fixed",
            "byte_identity_gate": "not-required",
            "rdf_and_shacl_semantic_equivalence_gate": "required-not-yet-passed",
        },
    }
    _write_json(
        PROJECT_ROOT / "project" / "reports" / "shacl-comparison.json",
        core_person_comparison,
    )
    _write_json(DEFAULT_REPORT_ROOT / "baseline.json", report)
    return report


def _print_verification(results: Iterable[dict[str, Any]]) -> int:
    failed = 0
    for item in results:
        marker = "OK" if item["verified"] else "FAIL"
        print(f"[{marker}] {item['id']}: {item['path']}")
        failed += not item["verified"]
    return int(failed > 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reproducible SEMIC LinkML baseline")
    parser.add_argument("--source-root", type=Path, default=DEFAULT_SOURCE_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch", help="Download and verify pinned official artifacts")
    commands.add_parser("verify", help="Verify the local artifact cache")
    inventory = commands.add_parser("inventory", help="Inventory an official SHACL profile")
    inventory.add_argument("profile"); inventory.add_argument("--output", type=Path)
    compare = commands.add_parser("compare", help="Compare a candidate SHACL graph")
    compare.add_argument("profile"); compare.add_argument("candidate", type=Path); compare.add_argument("--output", type=Path)
    validate = commands.add_parser("validate", help="Validate RDF data with a profile")
    validate.add_argument("profile"); validate.add_argument("data", type=Path); validate.add_argument("--output", type=Path)
    generate = commands.add_parser("generate", help="Generate parse-checked SHACL from LinkML")
    generate.add_argument("schema", type=Path); generate.add_argument("output", type=Path)
    generate.add_argument("--open-shapes", action="store_true")
    generate.add_argument("--semic-extensions", action="store_true")
    visualize = commands.add_parser("visualize", help="Generate deterministic PlantUML from LinkML")
    visualize.add_argument("schema", type=Path); visualize.add_argument("output", type=Path)
    commands.add_parser("run", help="Fetch, generate and compare the Core Person pilot baseline")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "fetch":
            return _print_verification(fetch_sources(args.source_root))
        if args.command == "verify":
            return _print_verification(verify_sources(args.source_root))
        if args.command == "inventory":
            result = inventory_graph(load_profile_graph(args.profile, args.source_root))
        elif args.command == "compare":
            result = compare_graphs(
                load_profile_graph(args.profile, args.source_root),
                Graph().parse(args.candidate.resolve()),
            )
        elif args.command == "validate":
            result = validate_data(args.profile, args.data, args.source_root)
        elif args.command == "generate":
            print(generate_shacl(
                args.schema,
                args.output,
                open_shapes=args.open_shapes,
                semic_extensions=args.semic_extensions,
            )); return 0
        elif args.command == "visualize":
            print(generate_plantuml(args.schema, args.output)); return 0
        elif args.command == "run":
            result = run_baseline(args.source_root)
        else:
            raise AssertionError(args.command)
        if getattr(args, "output", None):
            _write_json(args.output, result)
        else:
            print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
