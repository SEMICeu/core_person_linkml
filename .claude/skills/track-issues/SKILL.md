---
name: track-issues
description: Use when asked to file, track, log, curate or refresh LinkML-gap issues for this project, or after COMPARISON.md changes and gaps need to be turned into issue files. Triggers on phrases like "track issues", "file a new gap", "update the issues list", "curate issues from COMPARISON". Each gap becomes one local issue file under issues/; the upstream linkml issue URL is added manually by the human, never by the agent.
---

# track-issues

## Purpose

Maintain `issues/` as a flat, human-readable inventory of the gaps recorded in
`COMPARISON.md`. The job is **curation, not problem-solving**: each issue file
describes a single concrete gap precisely enough that the human (or an upstream
LinkML maintainer) can read it once and understand what's broken. No fix
proposals, no implementation options, no PR suggestions — just example input,
expected output, actual output, context.

The directory looks like this:

```
issues/
  track_issues.txt           # one line per issue, with optional upstream URL
  issue_shacl_no_definedby.md
  issue_class_disjunction_range.md
  ...
```

`track_issues.txt` is the manifest. Each line is the issue filename, optionally
followed by `|` and an upstream URL the human adds when an issue is filed
against `linkml/linkml`:

```
issue_shacl_datatype_targeted_shape.md | https://github.com/linkml/linkml/issues/1234
issue_owl_class_backpointer.md
issue_rdfs_isdefinedby.md | https://github.com/linkml/linkml/issues/0987
```

**The agent never writes the `| URL` part.** That column is reserved for the
human after they've actually filed (or located) the upstream issue.

## When to use

- The user says "track issues", "file a new gap", "update issues", "log this
  as an issue", "curate issues".
- `COMPARISON.md` has been updated (e.g. after the `align-model` skill ran)
  and the issue inventory is out of sync.
- The user describes a specific gap that should be captured as a permanent
  reference, independent of COMPARISON.md.

## Workflow

### 1. Read the source of truth

`COMPARISON.md` is the only source for *new* issues unless the human points
at a specific gap. Read it end-to-end. Identify each currently-open gap:

- "SHACL: what does not match" → individual gap entries
- "OWL: what does not match" → individual gap entries
- "LinkML expressivity gaps surfaced by this exercise" → individual gap
  entries
- Each numbered item under those sections is a candidate issue

Do **not** create issues for items marked resolved (e.g. crossed out, marked
*resolved*, moved to a "Closed in this run" section).

### 2. Reconcile with the existing manifest

```bash
ls issues/ 2>/dev/null
cat issues/track_issues.txt 2>/dev/null
```

For every candidate gap from step 1:

- **Already filed** (a matching `issue_*.md` exists): leave it. Do not edit
  unless the human explicitly asks. Don't overwrite to "freshen" the wording.
- **Not filed**: create a new file (see step 3) and append its name to
  `track_issues.txt`.

If `track_issues.txt` doesn't exist yet, create it (no header line, one issue
file per line).

### 3. Write one issue file per gap

Filename convention: `issue_<topic>.md` where `<topic>` is short, lowercase,
underscore-separated, and recognisable. Examples:

- `issue_shacl_datatype_targeted_shape.md` (datatype-IRI as `sh:targetClass`)
- `issue_owl_class_backpointer.md` (residual `skos:exactMatch cpv:Foo`
  with `--no-use-native-uris`)
- `issue_rdfs_isdefinedby.md` (no per-property `rdfs:isDefinedBy`)
- `issue_skos_scopenote.md` (no `comments`→`skos:scopeNote` round-trip)
- `issue_langstring_first_class.md` (multilingual literals)
- `issue_custom_xsd_datatype.md` (`gYear`/`gYearMonth` collapse to `str` in
  Python and JSON Schema)
- `issue_shape_iri_suffix.md` (named property-shape IRIs vs blank nodes)

Use the template below verbatim — every section is mandatory. If you can't
fill a section concisely with concrete content, the issue isn't ready to
file yet; flag that to the human instead of inventing filler.

```markdown
# <Short, declarative title — what's wrong>

## Context
<1–3 sentences. Why does this matter for the Core Person → LinkML translation?
Reference the upstream Core Person construct (SHACL shape, OWL axiom, JSON-LD
property) that depends on this.>

## Example input
<Minimal LinkML schema snippet (or the equivalent fragment of upstream
Core Person SHACL/OWL/JSON-LD) that triggers the gap. Keep it under
~15 lines.>

```yaml
# or ```turtle / ```json — pick the format that makes the case clearest
```

## Expected output
<What the relevant LinkML generator should emit for the input above,
showing the construct the upstream artefact uses. Keep it concrete —
actual SHACL / OWL / JSON Schema text, not prose.>

```turtle
# or other format
```

## Actual output
<What the generator currently emits, verbatim from `project/...` or a
quick repro. Showing the difference is the whole point.>

```turtle
```

## Why this matters
<1–3 sentences. What can't be expressed / validated / round-tripped
because of this gap? Reference the specific Core Person construct or
class that suffers.>
```

**Hard rules for issue files:**

- No "Proposed fix", "Implementation idea", "Workaround", or "Should we…"
  sections. The agent's job is to describe the gap, not solve it. The human
  will read and decide.
- No links to LinkML PRs / issues / commits — the human curates that
  manually in `track_issues.txt`.
- No speculation about which LinkML internal module is responsible (unless
  it's already pinpointed in `COMPARISON.md` — e.g. the
  `linkml/generators/owlgen.py:432-438` site for the class back-pointer —
  in which case a one-line reference is fine).
- Prefer real generator output over hand-written examples. If you're not
  sure what the actual output is, regenerate (`just gen-project`) and copy
  it.

### 4. Append to the manifest

For each new file written in step 3, append a line to
`issues/track_issues.txt`:

```
issue_<topic>.md
```

Just the filename. **Do not add `| URL`** — that's the human's column.

If a manifest entry already exists for a filename you just (re-)wrote, don't
duplicate it.

### 5. Report

Tell the human:

- Which new issues were filed (filenames)
- Which existing issues were left untouched
- Any gaps in COMPARISON.md you chose **not** to file as issues, with the
  one-sentence reason (e.g. "already resolved", "too vague — needs concrete
  repro first")

Then stop. Do not commit, push, or attempt to open upstream issues.

## What this skill never does

- Never edits `track_issues.txt` to add `| <url>`.
- Never opens or comments on `linkml/linkml` issues on GitHub.
- Never proposes fixes inside the issue files.
- Never invents an issue that isn't traceable to a gap in `COMPARISON.md` or
  an explicit human prompt.
- Never overwrites an existing issue file unless the human asks.
- Never deletes issues files when a gap looks resolved — the human decides
  (the manifest is the audit trail).

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing a "Proposed solution" section | Delete it. This skill is curation only. |
| Adding `\| https://github.com/linkml/linkml/issues/...` to `track_issues.txt` | Stop. That column is human-only. |
| Reusing one issue file for multiple gaps because they "feel related" | One file per gap. Cross-referencing in the **Context** section is fine; conflation isn't. |
| Filing an issue for a gap that's already crossed out / marked resolved in COMPARISON.md | Skip it. Report it in step 5 instead. |
| Writing hypothetical example output | Run `just gen-project` and copy the real output. |
| Treating issues as ephemeral and "refreshing" wording on every run | Existing files are immutable from the agent's perspective. Only the human edits past wording. |
| Putting issues under `.claude/` or `docs/` instead of `issues/` | The directory is `issues/` at repo root. |
