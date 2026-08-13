from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, RDF
from linkml_runtime.utils.schemaview import SchemaView

from core_person.baseline import (
    PROJECT_ROOT,
    generate_plantuml,
    generate_shacl,
    inventory_graph,
    load_profile_graph,
)


SH = Namespace("http://www.w3.org/ns/shacl#")
FIXTURES = PROJECT_ROOT / "tests" / "fixtures" / "core_person"


def _result_signature(shapes: Graph, data_path: Path):
    conforms, results, _ = validate(
        Graph().parse(data_path),
        shacl_graph=shapes,
        inference="none",
        advanced=False,
        meta_shacl=False,
        do_owl_imports=False,
    )
    signatures = set()
    for result in results.subjects(RDF.type, SH.ValidationResult):
        signatures.add(
            tuple(
                sorted(
                    (str(predicate), str(value))
                    for predicate in (
                        SH.focusNode,
                        SH.resultPath,
                        SH.value,
                        SH.sourceConstraintComponent,
                        SH.resultSeverity,
                    )
                    for value in results.objects(result, predicate)
                )
            )
        )
    return bool(conforms), signatures


def test_core_person_schema_has_no_artificial_identifier_or_tree_root():
    schema = SchemaView(PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml")
    assert len(schema.all_classes(imports=False)) == 11
    assert all(schema.get_identifier_slot(name) is None for name in schema.all_classes(imports=False))
    assert not any(item.tree_root for item in schema.all_classes(imports=False).values())
    assert all(
        slot.multivalued and not slot.required
        for class_name in schema.all_classes(imports=False)
        for slot in schema.class_induced_slots(class_name)
    )


def test_editing_wrapper_has_exactly_one_tree_root():
    schema = SchemaView(PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person_dataset.yaml")
    roots = [item.name for item in schema.all_classes(imports=False).values() if item.tree_root]
    assert roots == ["CorePersonDataset"]


def test_core_person_generated_constraint_inventory_matches_official(tmp_path):
    candidate_path = generate_shacl(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml",
        tmp_path / "core-person.ttl",
        open_shapes=True,
        semic_extensions=True,
    )
    official = inventory_graph(load_profile_graph("core-person-2.1.2"))
    candidate = inventory_graph(Graph().parse(candidate_path, format="turtle"))
    assert candidate["node_shapes"] == official["node_shapes"] == 15
    assert candidate["property_shapes"] == 49
    for component in ("class", "datatype", "nodeKind", "uniqueLang", "closed"):
        assert candidate["constraints"][component] == official["constraints"][component]
    assert candidate["constraints"]["minCount"] == 0
    assert candidate["constraints"]["maxCount"] == 0


def test_representative_shacl_behaviour_matches_official(tmp_path):
    official = load_profile_graph("core-person-2.1.2")
    candidate_path = generate_shacl(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml",
        tmp_path / "core-person.ttl",
        open_shapes=True,
        semic_extensions=True,
    )
    candidate = Graph().parse(candidate_path, format="turtle")
    expected = {
        "valid-open-and-multivalued.ttl": True,
        "invalid-unique-language.ttl": False,
        "invalid-object-class.ttl": False,
        "invalid-uri-literal.ttl": False,
        "invalid-issued-date.ttl": False,
    }
    for filename, conforms in expected.items():
        official_result = _result_signature(official, FIXTURES / filename)
        candidate_result = _result_signature(candidate, FIXTURES / filename)
        assert official_result[0] is conforms, filename
        assert candidate_result == official_result, filename


def test_plantuml_generation_is_deterministic(tmp_path):
    first = generate_plantuml(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml", tmp_path / "first.puml"
    )
    second = generate_plantuml(
        PROJECT_ROOT / "src" / "core_person" / "schema" / "core_person.yaml", tmp_path / "second.puml"
    )
    assert first.read_bytes() == second.read_bytes()
    diagram = first.read_text(encoding="utf-8")
    for class_name in ("Person", "Address", "ContactPoint", "Identifier"):
        assert f'class "{class_name}"' in diagram
