# core-person (LinkML)

A LinkML approximation of
[SEMICeu Core Person Vocabulary](https://github.com/SEMICeu/Core-Person-Vocabulary)
2.1.1, built as a **continuous evaluation harness** for LinkML itself.

## What this is (and isn't)

This is a **scoping / demo schema**, not a production Core Person profile.
The deliverable is the evaluation: by trying to reproduce the upstream SEMIC
SHACL, OWL, JSON-LD context, and HTML spec from a single LinkML source schema,
we surface exactly where LinkML can and can't express what Core Person needs.

The findings live in [`COMPARISON.md`](COMPARISON.md) — a running ledger of
"what matches / what's missing / what LinkML can't yet express". Individual
gaps get filed as issues under [`issues/`](issues/) and (manually)
cross-linked to upstream
[`linkml/linkml`](https://github.com/linkml/linkml) tickets.

## How it works

```
src/core_person/schema/core_person.yaml      ← the only hand-edited file
            │
            │  just gen-project / just gen-doc
            ▼
project/{shacl,owl,jsonschema,...}           ← generated artefacts
docs/elements/*.md                            ← generated documentation
src/core_person/datamodel/*.py                ← generated Python / Pydantic
            │
            │  diff against
            ▼
original/releases/2.1.1/{shacl,voc,context,html,...}   ← upstream truth
            │
            ▼
COMPARISON.md  + issues/issue_*.md            ← what's still off, and why
```

`original/` is a gitignored clone of
<https://github.com/SEMICeu/Core-Person-Vocabulary>; refresh it with
`git clone --depth=1 https://github.com/SEMICeu/Core-Person-Vocabulary
original`. The clone is read-only — never edit it.

## LinkML version

The project intentionally pins both `linkml` and `linkml-runtime` to git
`linkml/linkml@main` (the linkml repo is now a uv workspace with both
packages under `packages/`). This is permanent: the whole point is to
evaluate against unreleased LinkML so we can see what *will* be possible,
not just what is. Pull the latest commits with:

```bash
uv sync --group dev --refresh
```

## Quick start

```bash
just install      # uv sync --group dev (LinkML from git@main)
just gen-project  # SHACL, OWL, JSON Schema, ShEx, Pydantic, dataclasses, ...
just gen-doc      # mkdocs sources under docs/
just test         # schema regen + pytest + linkml-run-examples
```

Run `just` with no arguments for the full recipe list.

## Iterative workflow

When something in Core Person doesn't translate cleanly:

1. Document the gap in `COMPARISON.md`.
2. File it as `issues/issue_<topic>.md` (see the `track-issues` skill in
   `.claude/skills/`).
3. Work around it in the LinkML schema if a reasonable approximation
   exists.
4. Re-run the `align-model` skill against the latest LinkML `main` to
   check whether a recent merge has closed the gap.

Both skills (`align-model`, `track-issues`) are stored as Claude Code
project skills under `.claude/skills/` and are invoked automatically when
their triggering conditions match.

## Repository layout

| Path | Purpose |
|---|---|
| `src/core_person/schema/core_person.yaml` | The LinkML schema — only hand-edited file |
| `src/core_person/datamodel/` | Generated Python dataclasses + Pydantic |
| `project/` | Generated SHACL, OWL, JSON Schema, ShEx, GraphQL, Java, TypeScript, Protobuf, SQL DDL, JSON-LD context, prefix map (gitignored) |
| `docs/elements/` | Generated per-class/per-slot Markdown (gitignored) |
| `original/` | Read-only clone of SEMICeu/Core-Person-Vocabulary (gitignored) |
| `tests/data/{valid,invalid}/` | Example data tested by `linkml-run-examples` |
| `issues/` | Local issue files describing LinkML gaps |
| `COMPARISON.md` | Running gap analysis between generated and upstream artefacts |
| `CLAUDE.md` | Operating manual for Claude Code working on the repo |
| `.claude/skills/` | Project-local Claude Code skills (`align-model`, `track-issues`) |

## Credits

Bootstrapped from the
[linkml-project-copier](https://github.com/dalito/linkml-project-copier)
template
([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).
