# SEMIC Core Person 2.1.2 LinkML candidate

## Status

`src/core_person/schema/core_person.yaml` is now the local canonical candidate representation of
Core Person 2.1.2. It is based on the checksum-verified official SHACL,
vocabulary and JSON-LD context. No upstream file has been changed.

The model covers 11 semantic classes and 49 distinct class/property rules. Four
official datatype-target shapes (`xsd:date`, `rdfs:Literal`, `rdf:langString` and
`xsd:anyURI`) are added by the deterministic SEMIC SHACL adapter because they
are publication compatibility shapes, not ordinary object classes.

## Deliberate modelling rules

- Every property is optional and multivalued: official SHACL contains no
  minimum or maximum cardinalities.
- Shapes are open (`sh:closed false`). Unknown RDF properties remain valid.
- Canonical classes have no artificial LinkML identifiers, preserving official
  `sh:BlankNodeOrIRI` object semantics.
- The 18 `rdf:langString` properties retain `sh:uniqueLang true` through the
  `semic_unique_lang` extension.
- Unrestricted literals are not narrowed to `xsd:string`.
- Jurisdiction identifiers and geographic identifiers remain typed
  `xsd:anyURI` literals, not RDF IRI nodes.
- Birth and death dates follow authoritative SHACL and accept any RDF literal.
  The documented GenericDate union remains a Working Group decision.

## Editing versus publication

`src/core_person/schema/core_person_dataset.yaml` is a non-semantic editing wrapper with one
`CorePersonDataset` tree root. This satisfies editors and Table Schema tools
that require exactly one root. It must be excluded from SHACL, RDF and OWL
publication, otherwise it would introduce a non-official class and shape.

## Current equivalence result

The generated candidate and official SHACL are not RDF-isomorphic: the official
file uses 106 separately named, hash-IRI property shapes, while LinkML combines
them into 49 property shapes. However, the generated candidate matches the
official counts for all normative constraint components:

| Component | Official | Candidate |
|---|---:|---:|
| Node shapes | 15 | 15 |
| `sh:class` | 18 | 18 |
| `sh:datatype` | 21 | 21 |
| `sh:nodeKind` | 49 | 49 |
| `sh:uniqueLang` | 18 | 18 |
| `sh:closed` | 15 | 15 |
| `sh:minCount` | 0 | 0 |
| `sh:maxCount` | 0 | 0 |

Representative behavioural tests cover open/multivalued data, language
uniqueness, object class, URI-literal and issued-date constraints. Official and
candidate validation results agree for these fixtures. Full acceptance still
requires focused fixtures for all 49 rules and Working Group resolution of
GenericDate and official constraint-IRI requirements.

## Reproduce

```powershell
$env:PYSTOW_HOME = Join-Path $PWD 'generated\.cache\pystow'
$env:UV_CACHE_DIR = Join-Path $PWD 'generated\.uv-cache'

uv run core-person-baseline generate src\core_person\schema\core_person.yaml `
  generated\core-person\2.1.2\shacl\core-person-candidate.ttl `
  --open-shapes --semic-extensions

uv run core-person-baseline compare core-person-2.1.2 `
  generated\core-person\2.1.2\shacl\core-person-candidate.ttl `
  --output generated\core-person\2.1.2\reports\shacl-comparison.json

uv run core-person-baseline visualize src\core_person\schema\core_person.yaml `
  generated\core-person\2.1.2\uml\core-person.puml

uv run pytest -q
```
