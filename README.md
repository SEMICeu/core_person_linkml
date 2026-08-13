# Core Person (LinkML)

A LinkML candidate for [SEMIC Core Person Vocabulary](https://github.com/SEMICeu/Core-Person-Vocabulary)
2.1.2, built as a continuous evaluation harness for LinkML and the SEMIC
toolchain.

## What this is (and is not)

This is a **pilot**, not a production specification. The official Core Person
2.1.2 SHACL distribution remains authoritative.

The objective is to test whether one LinkML source can support semantic
modelling, SHACL generation and automatically generated UML visualisation while
preserving the meaning of the official SEMIC constraints.

Current evidence is encouraging but incomplete:

- the candidate covers 11 semantic classes and 49 class/property rules;
- generated and official SHACL have matching counts for every normative
  constraint component used by Core Person;
- representative positive and negative RDF fixtures produce equivalent SHACL
  validation results; and
- the graphs are not RDF-isomorphic because 106 separately named official
  property shapes are consolidated into 49 generated property shapes.

See [`COMPARISON.md`](COMPARISON.md) for the evidence and remaining decisions.

## How it works

```text
src/core_person/schema/core_person.yaml <- canonical LinkML candidate
            |
            +--> project/shacl/         <- generated SHACL
            +--> project/uml/           <- generated UML visualisation
            +--> project/reports/       <- comparison evidence
            |
            +--> compare with checksum-pinned official Core Person 2.1.2 SHACL
```

`src/core_person/schema/core_person_dataset.yaml` is a non-semantic editing wrapper with one
tree root. It is excluded from SHACL, RDF and OWL publication.

## Reproduce

Prerequisites: Python 3.12 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --frozen
uv run core-person-baseline fetch
uv run core-person-baseline run
uv run pytest -q -p no:cacheprovider --basetemp generated/.pytest-tmp
```

The run downloads only checksum-pinned official release files into the ignored
`generated/` directory. Upstream files are never edited or committed here.

## Repository layout

| Path | Purpose |
|---|---|
| `src/core_person/schema/core_person.yaml` | Canonical LinkML candidate |
| `src/core_person/schema/core_person_dataset.yaml` | Editing-only tree-root wrapper |
| `config/traceability/` | SEMIC modelling decisions and extension mapping |
| `project/` | Locally generated outputs, ignored by Git |
| `tests/fixtures/core_person/` | Focused RDF behavioural fixtures |
| `COMPARISON.md` | Human-readable equivalence assessment |

## Governance

No result in this repository becomes an official SEMIC specification without a
SEMIC Working Group decision. Generated artefacts must not be edited manually;
change the LinkML source or generator configuration, regenerate, and review the
resulting diff.

## Relation to the DCAT-AP pilot

This repository follows the evaluation-harness model established by
[`SEMICeu/dcat_ap_linkml`](https://github.com/SEMICeu/dcat_ap_linkml). Unlike
the fixed 1.11.1 baseline used to establish the first 2.1.2 results, the main
project continues to evaluate the commit-pinned `linkml/main` versions recorded
in `uv.lock`. Every comparison report must record the exact LinkML version used.
