# CLAUDE.md

## Mission

Evaluate whether LinkML can represent SEMIC Core Person Vocabulary 2.1.2 and
serve as a future source of truth for generated SHACL, RDF and UML outputs.
This repository is a pilot, not an official production specification. The
official Core Person 2.1.2 SHACL remains authoritative.

## Authority rules

1. `src/core_person/schema/core_person.yaml` is the canonical candidate schema.
2. `src/core_person/schema/core_person_dataset.yaml` is an editing-only wrapper
   with one tree root; exclude it from semantic publication.
3. Never edit generated datamodels or files under `project/` by hand.
4. Regenerate after changing the schema or generator configuration.
5. Keep every custom SEMIC extension traceable in
   `config/traceability/core-person-2.1.2.yaml` and `COMPARISON.md`.
6. No pilot result becomes official without a SEMIC Working Group decision.

## Authoritative comparison inputs

The checksum-pinned source manifest is `config/baseline-sources.json`. It fixes
the official repository commit and the SHA-256 of the Core Person 2.1.2 SHACL,
vocabulary, JSON-LD context, example and legacy EAP file. Downloaded upstream
files belong under ignored `generated/baseline/sources/` and remain read-only.

## Core model facts

- 11 LinkML classes represent the semantic and compatibility targets used by
  the 2.1.2 profile.
- 49 distinct class/path rules are modelled.
- All properties are optional and multivalued because the official SHACL has no
  `sh:minCount` or `sh:maxCount` constraints.
- Shapes are open.
- Canonical classes have no artificial identifiers because official object
  values may be blank nodes or IRIs.
- The adapter preserves 18 `sh:uniqueLang` constraints, unrestricted RDF
  literals and literal `xsd:anyURI` values.
- GenericDate remains a Working Group decision; the candidate follows the
  authoritative SHACL behaviour.

## Commands

```bash
uv sync --frozen
uv run core-person-baseline fetch
uv run core-person-baseline run
uv run pytest -q -p no:cacheprovider --basetemp generated/.pytest-tmp
```

The main project intentionally evaluates the commit-pinned `linkml/main`
versions in `uv.lock`. Record the exact LinkML version in every comparison run.

## Acceptance evidence

Do not claim equivalence from counts alone. Review all three layers:

1. RDF graph comparison, ignoring serialization-only differences;
2. structural SHACL comparison, including targets, paths and constraints; and
3. behavioural equivalence on approved positive and focused-negative fixtures.

Current representative behavioural fixtures pass, but complete positive and
negative coverage for all 49 rules is still required.
