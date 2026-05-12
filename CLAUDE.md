# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mission

Translate **SEMICeu/Core-Person-Vocabulary** (currently 2.1.1) into a complete
LinkML-driven pipeline. This is a **scoping/demo schema** built for the SEMIC ×
LinkML evaluation — the deliverable is the *evaluation*, not a production Core
Person profile. The point is to surface gaps in LinkML by trying to reproduce
the SEMIC SHACL / JSON-LD / OWL / HTML artefacts at
<https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/> and to
track those gaps as LinkML's `main` branch evolves.

Iterative workflow: every time we discover something in Core Person that LinkML
cannot represent cleanly,

1. document the gap in `COMPARISON.md`,
2. file it as an issue under `issues/` (see the `track-issues` skill),
3. work around it in the LinkML schema if a reasonable approximation exists,
4. retrofit once LinkML gains the capability (re-run the `align-model` skill
   against the latest `linkml/linkml` `main`).

`COMPARISON.md` is the running ledger of "what matches / what's missing / what
LinkML can't yet express". **Keep it current whenever the schema or the
upstream artefacts change.** Treat it as a deliverable, not a scratch file.

## LinkML version pinning

`pyproject.toml` pins both `linkml` and `linkml-runtime` to git
`linkml/linkml@main` (the linkml repo is now a uv workspace; both packages
live under `packages/` and are pulled via `#subdirectory=...` URLs). This is
**intentional and permanent**: the project's purpose is continuous evaluation
against unreleased LinkML. Do not "fall back" to PyPI versions. To pull newer
commits run `uv sync --group dev --refresh`.

## Repository layout

- `src/core_person/schema/core_person.yaml` — **the only hand-edited schema
  file.** Everything else is generated.
- `src/core_person/datamodel/` — generated Python (dataclasses + Pydantic).
  Do not edit by hand; regenerate via `just gen-python`.
- `project/` — generated artefacts (SHACL, OWL, JSON Schema, ShEx, GraphQL,
  Java, TypeScript, Excel, Protobuf, SQL DDL, JSON-LD context, prefix map).
  Gitignored except `project/README.md`.
- `docs/elements/` — generated per-class/per-slot Markdown. Gitignored.
- `original/` — **read-only clone of
  <https://github.com/SEMICeu/Core-Person-Vocabulary>** (gitignored). The full
  upstream repo, with every released version under `original/releases/`.
  Primary 2.1.1 sources of truth:
  - `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl` — SHACL shapes
    (authoritative for cardinalities/datatypes/nodeKind)
  - `original/releases/2.1.1/voc/core-person-ap.ttl` — OWL/RDF vocabulary
    (authoritative for class/property declarations and ontology metadata)
  - `original/releases/2.1.1/context/core-person-ap.jsonld` — JSON-LD context
    (authoritative for term-to-IRI mappings)
  - `original/releases/2.1.1/index.html` + `original/releases/2.1.1/html/` —
    HTML spec + assets
  - `original/releases/2.1.1/Changelog.md` — release notes
  - Earlier/later releases (`2.1.0`, `2.1.2`, `2.00`, `1.00`, `w3c/`) live
    alongside — useful when checking that 2.1.1 hasn't silently dropped
    class/property declarations.

  To refresh: `rm -rf original && git clone --depth=1
  https://github.com/SEMICeu/Core-Person-Vocabulary original && rm -rf
  original/.git`.
- `tests/data/{valid,invalid}/` — example data tested by
  `linkml-run-examples`. Populating these is part of the gap-closing work.

## Build / generate / test

All recipes go through [`just`](https://github.com/casey/just/). Run `just`
(no args) for the list. Environment variables come from `config.public.mk`
(loaded automatically via `set dotenv-load`); generator-level config lives in
`config.yaml`.

| Recipe | What it does |
|---|---|
| `just install` | `uv sync --group dev` |
| `just gen-project` | Run all configured LinkML generators → `project/`; also writes the Python dataclasses + Pydantic into `src/core_person/datamodel/` |
| `just gen-python` | Just the Python data models |
| `just gen-doc` | Schema markdown + bundled YAML under `docs/` |
| `just site` | `gen-project` + `gen-doc` |
| `just test` | Schema regen smoke test + pytest + `linkml-run-examples` |
| `just lint` | `linkml-lint` over the schema source dir |
| `just clean` | Remove `project/`, `tmp/`, generated docs, and `src/core_person/datamodel/*` (except `__init__.py`) |

Subset recipes used during iteration:

- `just _test-schema` — `gen-project` into `tmp/` only (fast sanity check)
- `just _test-python` — regen Python then `pytest`
- `just _test-examples` — run `linkml-run-examples` against `tests/data/valid`
  and `tests/data/invalid`

Run a single pytest: `uv run pytest tests/path/to/test.py::test_name`.

The SHACL output is generated with `--non-closed` (see `config.yaml`/justfile)
to match SEMIC's open-shape semantics — don't switch to closed shapes without
updating COMPARISON.md.

The OWL output is generated with `--no-use-native-uris` so that subject IRIs
match the external SEMIC vocabulary (`person:`, `foaf:`, `m8g:`, …) rather
than the schema-internal `cpv:` namespace. See `COMPARISON.md` ("OWL: what
does not match") for the residual `skos:exactMatch cpv:Foo` back-pointer
issue this flag does *not* fix.

## Schema architecture

The schema is a single file (`src/core_person/schema/core_person.yaml`) with
three sections worth understanding before editing:

1. **Top-level prefixes** map Core Person's namespaces (`cpv`, `m8g`,
   `person`, `foaf`, `locn`, `adms`, `dcterms`, `skos`, `rdfs`, `rdf`, `xsd`,
   `owl`). These flow into both SHACL output and the JSON-LD context, so they
   round-trip — do not rename casually.
2. **Classes** mirror the 9 entity-class SHACL shapes (`person:Person`,
   `adms:Identifier`, `locn:Address`, `m8g:ContactPoint`, `foaf:Agent`,
   `dcterms:Jurisdiction`, `dcterms:Location`, `foaf:Document`,
   `skos:Concept`). The upstream `m8g:GenericDate` NodeShape is intentionally
   *not* reproduced as a class — it's modelled as a slot-level `any_of` over
   `date | gYear | gYearMonth` on the date slots. LinkML class names match
   the SEMIC English labels (e.g. `Person`, `ContactPoint`, `Jurisdiction`)
   while the underlying `class_uri` points at the external IRI.
3. **Slot URIs** follow the SEMIC SHACL property paths (e.g. `dateOfBirth`
   mapped to `m8g:birthDate`). Keep that convention.

Schema ID: `https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1`.
**Not registered as a w3id** — use `configure-w3id` if/when this is promoted
beyond the demo.

### Class inventory

The 9 entity classes (LinkML name → URI):

| LinkML | URI |
|---|---|
| `Person` | `person:Person` |
| `Identifier` | `adms:Identifier` |
| `Address` | `locn:Address` |
| `ContactPoint` | `m8g:ContactPoint` |
| `Agent` | `foaf:Agent` |
| `Jurisdiction` | `dcterms:Jurisdiction` |
| `Location` | `dcterms:Location` |
| `Document` | `foaf:Document` |
| `Concept` | `skos:Concept` |

### Date-disjunction handling

The date-typed slots (`dateOfBirth`, `dateOfDeath`) use `any_of` over `date |
gYear | gYearMonth`. The two `g*` types are declared as custom types with
explicit `uri: xsd:gYear` / `uri: xsd:gYearMonth` because LinkML doesn't ship
them. This is the only practical way to round-trip the SEMIC date disjunction
through SHACL (it inlines as an `sh:or` with three datatype branches —
*better* than the upstream `m8g:GenericDate` NodeShape, which is empty and
does not actually constrain the property). The cost is that Python/Pydantic
collapse the two `g*` types to `str`. See `COMPARISON.md` "Union datatypes"
for the full picture.

### LangString custom type

`rdf:langString` is declared as a custom `LangString` type (`base: str`,
`uri: rdf:langString`) so that `sh:datatype rdf:langString` is emitted for
multilingual slots like `fullName`, `givenName`, `familyName`. LinkML has no
native first-class language-tagged-string type, and this is the closest
practical approximation.

## Known gaps (do not "fix" silently)

These are deliberate approximations driven by LinkML limitations. Document any
change to them in COMPARISON.md:

- **Datatype-targeted SHACL shapes** (`DateShape`, `LiteralShape`,
  `TextShape`, `URIShape`) — LinkML cannot emit a `sh:NodeShape` whose
  target IRI is a datatype. The four upstream shapes are not reproduced.
- **Residual `skos:exactMatch cpv:Foo` back-pointer** on each class in OWL
  output, even with `--no-use-native-uris`. This is a narrow upstream
  `gen-owl` issue (`linkml/generators/owlgen.py:432-438`), not a metamodel
  gap.
- **Per-property `rdfs:isDefinedBy`** (`<http://data.europa.eu/m8g>`) — not
  emitted.
- **Per-property `rdfs:seeAlso`** pointing at the spec HTML anchor (e.g.
  `https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.givenname`)
  — not emitted; LinkML descriptions don't carry per-property spec anchors.
- **`skos:scopeNote` annotations** on `birthDate`, `deathDate`, `gender`,
  `sex`, `ContactPoint` — not round-tripped from LinkML `comments`/`notes`.
- **Multilingual ontology titles** (`@en` + `@nl` on the ontology label) —
  LinkML titles are single-string.
- **Editor metadata** (`foaf:maker`, `dcterms:mediator`, list of editor blank
  nodes) — not modelled.
- **Property shapes as named IRIs** — the upstream uses
  `<…/<sha-hash>>`-named property shapes; LinkML emits blank-node
  property shapes. Functionally equivalent but not externally referenceable.
- **`rdfs:domain` / `rdfs:range` direct triples** — LinkML emits
  `owl:Restriction` / `owl:onProperty` axioms under the class instead, which
  is verbose and harder to read.

### Deliberate scoping omissions (not LinkML gaps)

Things upstream Core Person has that we intentionally don't model — these are
scoping choices for the demo, not LinkML limitations:

- **SKOS code lists for gender / sex** — upstream *recommends* but doesn't
  *enforce* SKOS concept schemes for these values. Adding them as LinkML
  enums would bloat the schema without changing what the gap-finding
  evaluation tests.
- **Generated UML diagrams** (`original/releases/2.1.1/uml/`) — not
  reproduced from the LinkML side; LinkML's mkdocs output is the diagram
  equivalent.

## Working with this repo

- **Edit `src/core_person/schema/core_person.yaml` only.** Anything under
  `project/`, `src/core_person/datamodel/`, or `docs/elements/` is generated
  and will be overwritten by `just gen-project` / `just gen-doc`.
- After a schema change, the standard cycle is `just gen-project` → eyeball
  the SHACL/OWL/JSON-Schema diff under `project/` → update COMPARISON.md if
  a gap closed or opened → `just test`.
- The `original/` checkout is the upstream artefact for diffing. Compare
  generated SHACL against
  `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl`, OWL against
  `original/releases/2.1.1/voc/core-person-ap.ttl`, JSON-LD context against
  `original/releases/2.1.1/context/core-person-ap.jsonld`. Not against an
  older local snapshot.
- This repo is bootstrapped from the [linkml-project-copier
  template](https://github.com/dalito/linkml-project-copier). `copier update`
  refreshes scaffolding via `just update`.

## Conventions inherited from `~/.claude/CLAUDE.md`

- Never `git commit`, push, or open PRs unless the user explicitly says so.
- Prefer `git mv` over `mv` for tracked files.
- `gh issue view` / `gh pr view` must use `--json` (the plain forms hit
  deprecated GraphQL fields).
