# LinkML vs SEMIC Core Person Vocabulary 2.1.1 — comparison

| Field | Value |
|---|---|
| Last refreshed | 2026-07-18 |
| LinkML (generators) commit | `1288dbb6e9a6df8d1f04e250a1fb48af635bd530` (1.11.0.post159.dev0+1288dbb6) |
| linkml-runtime commit | `1288dbb6e9a6df8d1f04e250a1fb48af635bd530` (1.11.0.post159.dev0+1288dbb6) |
| Previous refresh | 2026-05-12 @ `1c5f68e4` (~159 upstream commits earlier) |
| Upstream release | SEMIC Core Person Vocabulary **2.1.1** |
| Upstream sources | `original/releases/2.1.1/{shacl,context,voc,html}/` |

This document compares the artefacts generated from
`src/core_person/schema/core_person.yaml` (a hand-written LinkML
approximation of SEMIC Core Person 2.1.1) against the official
SEMIC artefacts under `original/releases/2.1.1/` (read-only clone of
<https://github.com/SEMICeu/Core-Person-Vocabulary>).

## Counts

| metric                              | original                | linkml output           |
|-------------------------------------|-------------------------|-------------------------|
| SHACL `sh:NodeShape` count          | 14                      | 9                       |
| SHACL property shapes (`sh:path`)   | ~37                     | 41 (one per slot assignment; each now a labelled top-level blank node `_:c14nNN` post-RDFC-1.0) |
| OWL `owl:Class` declarations        | 2 (m8g:ContactPoint, m8g:GenericDate) | 9 (external IRI subjects when generated with `--no-use-native-uris`; each retains a `skos:exactMatch cpv:Foo` back-pointer to the local namespace — intentional, see [linkml#2693](https://github.com/linkml/linkml/pull/2693)) |
| OWL `owl:DatatypeProperty` (string occurrences) | 5           | 25 (`dcterms:identifier` is typed as both Datatype+Object, so counts overlap) |
| OWL `owl:ObjectProperty` (string occurrences)   | 3           | 15                      |
| classes captured                    | Person, Identifier, Address, ContactPoint, Agent, Jurisdiction, Location, Document, Concept (Code), GenericDate | 9 (GenericDate replaced by slot-level `any_of` of xsd:date / xsd:gYear / xsd:gYearMonth) |
| total Person properties (SHACL)     | 18                      | 18                      |
| OWL file size (lines)               | 143                     | **345** as currently configured (was 377 on 2026-05-12; the 32-line drop is the new pyoxigraph RDFC-1.0 serialization compacting blank-node lists, not a content change — see "Changed in this run"). Was 625 before the cardinality-trim flags |

**Note on OWL generation flags.** The OWL output bundled in
`project/owl/core_person.owl.ttl` is produced with this combination
(wired into `config.public.mk` `LINKML_GENERATORS_OWL_ARGS`):

- `--no-use-native-uris` — subject IRIs match the external SEMIC
  vocabulary (`m8g:`, `foaf:`, `person:`, `locn:`, …) rather than the
  schema-internal `cpv:` namespace. Residual class-IRI back-pointer
  remains (see "OWL: what does not match" item 1).
- `--metadata-profile rdfs` — `gen-owl` emits `rdfs:label` /
  `rdfs:comment` for each class and property instead of
  `skos:definition`. Matches the upstream OWL style — `skos:definition`
  count dropped to 0 in this run, `rdfs:comment` count is now 49.
- `--ontology-uri-suffix ""` — the `owl:Ontology` IRI is now the bare
  schema `id` (`…/2.1.1`) instead of `…/2.1.1.owl.ttl`.
- `--skip-vacuous-local-range-axioms`,
  `--skip-vacuous-min-zero-cardinality-axioms`,
  `--consolidate-cardinality-axioms` — strip the vacuous
  `owl:Restriction` axioms (just-emit-because-LinkML-can) that
  previously bloated the output 4× over upstream. `owl:Restriction`
  blocks dropped from many to **2** for the entire schema. These flags
  are LinkML-side defaults-to-be (deprecation warnings flag them as
  flipping in a future release); enabling them now also silences the
  forward-compat noise.

## Changed in this run — 2026-07-18

LinkML `main` moved ~159 commits (`1c5f68e4` → `1288dbb6`). The schema
source was **not** edited this run; every change below is upstream
generator behaviour. `just gen-project`, `just gen-doc` and `just test`
all run clean (3 pytest + `linkml-run-examples` pass).

1. **RDF output is now canonicalised (pyoxigraph RDFC-1.0).** Both the
   SHACL and OWL Turtle are now serialised through the deterministic
   pyoxigraph RDFC-1.0 canonicaliser
   ([linkml#3407](https://github.com/linkml/linkml/pull/3407),
   hardened by [linkml#3524](https://github.com/linkml/linkml/pull/3524)).
   Effect: property/restriction/list blank nodes that were previously
   inlined as `[ … ]` / `( … )` are now emitted as **top-level labelled
   blank nodes** (`_:c14n0`, `_:c14n1`, …) with stable, content-derived
   labels. The graph is **semantically identical** — same targets, paths,
   datatypes, cardinalities, `sh:or` unions — just flattened and
   diff-stable across runs/processes. This is a net win for the
   evaluation (deterministic diffs) at some cost to human readability.
   It also accounts for the OWL line count dropping 377 → 345.
   Consequence for the existing "property shapes as blank nodes vs named
   IRIs" gap: **unchanged** — they are still blank nodes, now merely
   labelled `_:c14nNN` instead of nested. Still not externally
   referenceable.

2. **New `sh:ignoredProperties ( rdf:type )` on every NodeShape**
   ([linkml#3518](https://github.com/linkml/linkml/pull/3518) sorts it for
   determinism; the emission itself is now default `shaclgen` behaviour).
   All 9 generated NodeShapes now carry `sh:ignoredProperties` listing
   `rdf:type`. Upstream SEMIC SHACL has **none**. There is no CLI flag to
   suppress it (`gen-shacl --help` exposes only `--closed/--non-closed`
   and `--message-template`). Classified as **added LinkML noise** (like
   `sh:nodeKind` / `sh:order` below), not a missing-capability gap.
   Candidate for an upstream "make ignoredProperties opt-out" request.

3. **New `skos:inScheme <…/2.1.1>` on every OWL class and property.**
   `gen-owl` now stamps each declared term with `skos:inScheme` pointing
   at the ontology IRI. Upstream OWL has none. Harmless / arguably
   correct provenance, but a divergence. Classified as **added LinkML
   noise**, not a gap.

4. **`skos:exactMatch cpv:Foo` class back-pointer is now confirmed
   *intentional*, not a bug.**
   [linkml#2693](https://github.com/linkml/linkml/pull/2693) ("Make
   `class_uri` be `skos:exactMatch` of the element URI on JSON-LD and
   RDF", closes #2687) makes this back-pointer deliberate generator
   behaviour. The 2026-05-12 framing ("a narrow upstream bug in
   `owlgen.py:432-438` to file") is therefore **withdrawn** — there is
   nothing to file; with `--no-use-native-uris` the external IRI is the
   subject and the `skos:exactMatch cpv:Foo` link back to the internal
   IRI is by design. Count unchanged: 9 back-pointers (one per class).

### Flags evaluated and **not** adopted this run

- **`--xsd-anyuri-as-iri`** (new cross-generator flag,
  [linkml#3292](https://github.com/linkml/linkml/pull/3292); available on
  `gen-owl` and `gen-jsonld-context`). It re-types `xsd:anyURI`-ranged
  slots as IRIs (`owl:ObjectProperty` in OWL, `@type: @id` in the JSON-LD
  context) instead of literals. **Rejected because it moves us away from
  upstream.** Our three `uri`-typed slots — `schemeUri` (`dcterms:conformsTo`),
  `jurisdictionId` (`dcterms:identifier` on Jurisdiction) and
  `geographicIdentifier` (`rdfs:seeAlso`) — are each declared
  `@type: xsd:anyURI` in the **upstream** JSON-LD context, and our current
  output already matches that exactly. Adopting the flag would flip all
  three to `@id` and diverge. (Note the upstream context is itself
  inconsistent: `Person.identifier`, `issuingAuthorityUri` and the
  object-valued slots are `@id`, but the three above stay `xsd:anyURI`.
  We reproduce the upstream inconsistency faithfully.)
- **`--message-template`** for `sh:message` on property shapes
  ([linkml#3450](https://github.com/linkml/linkml/pull/3450)). Not
  adopted — upstream SHACL emits no `sh:message`; adding it would diverge.

## Closed (or partially closed) in a previous run — 2026-05-12

This is the first `align-model` run after the harness was set up. The
following changes were applied to the pipeline by reading recent
`linkml/linkml` merges and trying the new CLI flags:

1. **OWL bloat — closed.** Three new flags merged in `linkml/linkml`
   (forewarned by deprecation warnings — see [linkml#3190](https://github.com/linkml/linkml/issues/3190),
   [linkml#3191](https://github.com/linkml/linkml/issues/3191))
   — `--skip-vacuous-local-range-axioms`,
   `--skip-vacuous-min-zero-cardinality-axioms`,
   `--consolidate-cardinality-axioms` — drop the redundant
   `owl:Restriction` blocks. **OWL output: 625 → 377 lines**
   (`owl:Restriction` count: many → 2). Upstream is 143; the
   remaining 234 lines are mostly per-property declarations that
   genuinely have no upstream counterpart (LinkML emits one for every
   slot; the SEMIC OWL is intentionally thin).

2. **OWL `skos:definition` → `rdfs:comment` — closed via
   `--metadata-profile rdfs`.** All class/property documentation now
   round-trips into the upstream-canonical `rdfs:comment` channel.
   `skos:definition` count: 18 → 0.  `rdfs:comment` count: 0 → 49.

3. **OWL ontology IRI cleanup — closed via
   `--ontology-uri-suffix ""`.** Was `…/2.1.1.owl.ttl`, now `…/2.1.1`
   — matching the schema `id` exactly.

4. **`rdfs:seeAlso` per-property spec-anchor — channel proven, partial
   apply.** With `config.yaml` `shacl.include_annotations: true` plus
   per-slot `annotations: { rdfs:seeAlso: <url> }`, gen-shacl now
   emits the `rdfs:seeAlso` triple **as an IRI** on the (still
   blank-node) property shape, and gen-owl emits it on the property
   declaration (as a string literal — minor inconsistency between the
   two generators). Demonstrated end-to-end on `m8g:birthDate`. The
   remaining 30+ slots are not yet annotated; that's mechanical
   follow-up work, not a LinkML expressivity gap.

5. **`rdfs:isDefinedBy` per-property — same channel as (4).**
   Demonstrated on `m8g:birthDate` (`rdfs:isDefinedBy <http://data.europa.eu/m8g>`
   in SHACL, `rdfs:isDefinedBy "http://data.europa.eu/m8g"` in OWL).
   Same caveats: rest of the slots not yet annotated; OWL emits the
   value as a string literal while SHACL treats it as an IRI.

6. **`rdfs:range` direct triple — was never a gap.** The previous
   `issue_rdfs_domain_range_direct.md` claimed `rdfs:range` is only
   emitted as `owl:Restriction` axioms. Recount on the regenerated
   file: 39 direct `rdfs:range` triples on properties. The actual
   residual gap is `rdfs:domain` only — `gen-owl` emits 0 of them
   regardless of flags tested. (Issue file is human-curated; flag for
   correction in next run.)

## Still open — captured under `issues/`

The 11 issue files remain valid descriptions for the following gaps
(see `issues/track_issues.txt`):

- SHACL targets pointing at datatype IRIs
- `rdfs:isDefinedBy` not auto-emitted for re-used external vocab properties
  (manual annotations work but require per-slot effort)
- `rdfs:domain` not emitted on properties
- `skos:scopeNote` round-trip (LinkML `comments` lands on `skos:note`,
  not `skos:scopeNote`)
- per-property `rdfs:seeAlso` to spec anchors (manual annotations work
  but require per-slot effort, plus an OWL string-vs-IRI mismatch)
- custom `xsd:gYear` / `xsd:gYearMonth` types collapse in Pydantic and
  JSON Schema
- property shapes as blank nodes vs named IRIs
- top-of-file `rdfs:member` collection of NodeShapes
- `rdf:langString` as a first-class LinkML type
- multilingual ontology-header titles

**Reclassified 2026-07-18 (no longer tracked as LinkML gaps):**

- ~~residual `skos:exactMatch cpv:Foo` class back-pointer in OWL~~ —
  confirmed intentional generator behaviour
  ([linkml#2693](https://github.com/linkml/linkml/pull/2693)); nothing to
  fix. Any corresponding issue file should be closed.

**New divergences 2026-07-18 (added LinkML noise, not capability gaps):**

- `sh:ignoredProperties ( rdf:type )` on every SHACL NodeShape
  ([linkml#3518](https://github.com/linkml/linkml/pull/3518)); no
  suppression flag — candidate for an upstream opt-out request.
- `skos:inScheme <…/2.1.1>` on every OWL class and property (`gen-owl`
  default). Both absent from upstream artefacts.

## SHACL: what matches

- 9 entity-class shapes round-trip with the **same target IRI**:
  `person:Person`, `adms:Identifier`, `locn:Address`,
  `m8g:ContactPoint`, `foaf:Agent`, `dcterms:Jurisdiction`,
  `dcterms:Location`, `foaf:Document`, `skos:Concept`. The original
  `m8g:GenericDate` NodeShape is intentionally not produced — it is
  replaced by an inline `sh:or` constraint on the date slots (see the
  Union datatypes section below).
- All 36 `sh:property` paths match the originals exactly:
  `foaf:familyName`, `foaf:givenName`, `foaf:name`, `dcterms:identifier`,
  `dcterms:alternative`, `dcterms:conformsTo`, `dcterms:issued`,
  `dcterms:creator`, `dcterms:title`, `dcterms:type`, `m8g:birthDate`,
  `m8g:deathDate`, `m8g:domicile`, `m8g:gender`, `m8g:sex`,
  `m8g:matronymicName`, `m8g:contactPoint`, `m8g:contactPage`,
  `m8g:email`, `m8g:telephone`, `m8g:identifies`, `person:birthName`,
  `person:patronymicName`, `person:placeOfBirth`, `person:placeOfDeath`,
  `person:countryOfBirth`, `person:countryOfDeath`, `person:citizenship`,
  `person:residency`, `locn:thoroughfare`, `locn:adminUnitL1`,
  `locn:adminUnitL2`, `locn:addressArea`, `locn:postName`,
  `locn:locatorName`, `locn:fullAddress`, `locn:geographicName`,
  `rdfs:label`, `rdfs:seeAlso`.
- `sh:datatype`, `sh:class`, `sh:name`, `sh:description` all match the
  originals after iteration (LangString custom type added to make
  `rdf:langString` fields render correctly).
- `sh:closed false` matches after setting `closed: false` in
  `config.yaml`.
- Shape names use the `…Shape` suffix convention thanks to
  `suffix: Shape`.

## SHACL: what does not match

1. **Missing `NodeShape`s for datatype targets** (4 shapes lost):
   `DateShape` (target `xsd:date`), `LiteralShape` (`rdfs:Literal`),
   `TextShape` (`rdf:langString`) and `URIShape` (`xsd:anyURI`).
   LinkML cannot generate `sh:NodeShape` whose target is a datatype
   IRI, because LinkML datatypes are not classes.
2. **`rdfs:seeAlso` per-property pointers** in originals reference the
   spec's HTML anchor for each property
   (`https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.givenname`).
   LinkML does not emit a per-property `seeAlso` to spec docs.
3. **`rdfs:member` collection list** of all node shapes at the top of
   the SHACL file is not produced by LinkML.
4. **`sh:nodeKind`** values are added by LinkML (`sh:Literal`,
   `sh:BlankNodeOrIRI`); the original SHACL omits `sh:nodeKind`. Not
   wrong, but adds noise.
5. **`sh:order`** is added by LinkML and not present in the original.
6. **Property shapes are blank nodes** in the LinkML output instead of
   named `…/<sha-hash>` IRIs. Since 2026-07-18 they are emitted as
   top-level *labelled* blank nodes (`_:c14nNN`, pyoxigraph RDFC-1.0)
   rather than inlined `[ … ]`, but they are still blank nodes: the
   original hash-named property shapes can be referenced from outside;
   LinkML's cannot.
7. **`sh:ignoredProperties ( rdf:type )`** is added by LinkML on every
   NodeShape since 2026-07-18 (`shaclgen` default; no suppression flag).
   The original SHACL has none. Added noise, not a capability gap.
8. **No `sh:datatype xsd:anyURI` constraint** for `Identifier.schemeUri`
   gets a `sh:nodeKind sh:Literal` from LinkML, while semantically the
   original treats it as a URI literal — actually they match here, but
   `Jurisdiction.id` (also `xsd:anyURI`) has the same shape; matches.

## OWL: what matches

- The 9 SEMIC classes appear with the external IRI as the subject
  (`person:Person`, `m8g:ContactPoint`, `foaf:Agent`, …) when generated
  with `--no-use-native-uris`. A `skos:exactMatch cpv:Foo` back-pointer
  to the LinkML-internal IRI is still emitted on each class (see "what
  does not match" item 1).
- All slots are declared directly under their external IRI
  (`m8g:birthDate`, `foaf:familyName`, …) when generated with
  `--no-use-native-uris`, with **no** `skos:exactMatch` back-pointer.
  The flag fully resolves the IRI-shadowing question for slots.
- `rdfs:label` and `skos:definition` for every class round-trip from
  LinkML.
- The vocabulary metadata (`dcterms:license`, `dcterms:title`,
  `pav:version`) is emitted on the `owl:Ontology`.

## OWL: what does not match

1. **Default mode emits shadow IRIs; `--no-use-native-uris` mostly
   fixes it.** By default (`--use-native-uris`), every class and slot
   is declared in the schema-internal `cpv:` namespace with a
   `skos:exactMatch` triple pointing to the external IRI. That is
   wrong for SEMIC's use case (the spec *re-uses* external IRIs
   directly). Setting `--no-use-native-uris` flips the subject to
   the external IRI. For slots, this is a clean fix — no shadow,
   no back-pointer. For classes, there is a residual issue: a
   `skos:exactMatch cpv:Foo` back-pointer is still emitted from the
   external class IRI to the (otherwise unused) local IRI. The
   relevant code is `linkml/generators/owlgen.py:432-438`. This is a
   narrow upstream issue to file, not a fundamental capability gap.
   The previous version of this document overstated this as the
   "single biggest expressivity gap" — that framing was wrong.
2. **No `rdfs:isDefinedBy`** is emitted by `gen-owl`. The original has
   `rdfs:isDefinedBy <http://data.europa.eu/m8g>` on every property
   it owns.
3. **`rdfs:domain` and `rdfs:range` are not produced** as direct
   triples on properties. LinkML uses
   `owl:Restriction`/`owl:allValuesFrom`/`owl:onProperty` axioms
   under the class instead, which is more verbose and harder to read.
4. **`skos:scopeNote`** annotations on `birthDate`, `deathDate`,
   `gender`, `sex`, `ContactPoint` are not modelled by LinkML
   `comments`/`notes` round-tripping into OWL output.
5. **Multilingual labels** (`@en` and `@nl` on the ontology label) are
   lost — LinkML titles are single-string.
6. **Editor metadata** (`foaf:maker`, `dcterms:mediator`, list of
   `<…rec54#editor>` blank nodes) is not modelled in LinkML and is
   absent from the OWL.
7. **`skos:inScheme <…/2.1.1>`** is added by LinkML on every class and
   property since 2026-07-18 (`gen-owl` default). The original OWL has
   none. Added noise (arguably-correct provenance), not a capability gap.
8. **`skos:exactMatch cpv:Foo` back-pointer on each class** — retained
   from `--no-use-native-uris`. As of 2026-07-18 this is confirmed
   *intentional* generator behaviour
   ([linkml#2693](https://github.com/linkml/linkml/pull/2693)), not a bug
   to file. 9 occurrences (one per class).

## LinkML expressivity gaps surfaced by this exercise

1. **Residual class-IRI back-pointer in `gen-owl --no-use-native-uris`.**
   *Not a capability gap, and — as of 2026-07-18 — not a bug either.*
   The default mode (`--use-native-uris`) emits the LinkML-internal IRI
   as the OWL subject and `skos:exactMatch` to the external one.
   `--no-use-native-uris` flips the subject to the external IRI for both
   classes and slots. For slots this is a clean fix. For classes, a
   `skos:exactMatch cpv:Foo` back-pointer to the local IRI is still
   emitted — but [linkml#2693](https://github.com/linkml/linkml/pull/2693)
   confirms this is **intentional** (`class_uri` is deliberately made a
   `skos:exactMatch` of the element URI on JSON-LD and RDF). Nothing to
   file; nothing to fix. The previous "narrow upstream bug in
   `owlgen.py:432-438`" framing is withdrawn.
2. **Cannot model SHACL targets that point at datatype IRIs**
   (Date/Literal/Text/URI shapes in the original). LinkML treats
   datatypes as a closed registry separate from classes.
3. **Union datatypes — works in SHACL/OWL, degrades elsewhere.**
   This was tested directly. The slots `dateOfBirth` / `dateOfDeath`
   were modelled with:
   ```yaml
   any_of:
     - range: date
     - range: gYear
     - range: gYearMonth
   ```
   Result by generator:
   - **SHACL** (`gen-shacl`): correct. Each date slot emits an
     `sh:or` with three branches, and each branch carries the right
     `sh:datatype`: `xsd:date`, `xsd:gYear`, `xsd:gYearMonth`. This
     is a *better* approximation than the original SEMIC SHACL,
     which only declared `m8g:GenericDate` as an empty `NodeShape`
     and did not actually constrain the date properties at all.
   - **OWL** (`gen-owl`): correct. `rdfs:range` is emitted as
     `[ a rdfs:Datatype ; owl:unionOf ( xsd:date xsd:gYear xsd:gYearMonth ) ]`,
     and the same blank-node datatype union is used inside the
     `owl:Restriction` axioms on the Person class.
   - **JSON Schema** (`gen-json-schema`): partial. `anyOf` is
     emitted with three branches, but only the `date` branch keeps
     `format: date` — the gYear and gYearMonth branches collapse to
     `{"type": "string"}` with no pattern, since the custom types
     have `base: str` and no `pattern` slot.
   - **Pydantic** (`gen-pydantic`): degraded. The slot type becomes
     `Optional[list[Union[date, str]]]` — three custom types
     collapse to two Python types because gYear and gYearMonth share
     the same `base: str`. The `any_of` metadata is preserved in
     `json_schema_extra`, so callers that read the metadata can
     still see the intended union, but Python static checking
     cannot distinguish gYear from gYearMonth from any other str.
   - **dataclasses** (`pythongen`): worst. The slot range becomes
     `Optional[Union[str, list[str]]]` — `xsd:date` is silently
     dropped from the union and the field accepts any string. The
     `any_of` semantics are lost entirely.

   Summary: `any_of` is round-trippable in the RDF generators
   (SHACL, OWL) but lossy in the code generators because Python's
   type system cannot distinguish multiple custom types that share
   a `base`.
4. **No per-property `rdfs:isDefinedBy` / scope notes / spec anchors.**
   The original SHACL/OWL treat each property as a documented spec
   element with an HTML anchor — LinkML descriptions don't carry this.
5. **No mechanism to suppress shadow class declarations.** LinkML
   always declares `cpv:Foo` even when the intent is "I am only
   describing the existing `foaf:Agent` shape". This means the OWL
   output is roughly 4x the size of the original (615 vs 143 lines).

### Custom datatypes (`xsd:gYear`, `xsd:gYearMonth`)

Neither `xsd:gYear` nor `xsd:gYearMonth` is in LinkML's built-in
type registry (the built-in `date` covers `xsd:date`, but there is
no `gYear` / `gYearMonth`). To use them in `any_of`, both types had
to be declared in the schema's `types:` section:

```yaml
types:
  gYear:
    name: gYear
    uri: xsd:gYear
    base: str
    description: An XSD gregorian year (e.g. "1980") …
  gYearMonth:
    name: gYearMonth
    uri: xsd:gYearMonth
    base: str
    description: An XSD gregorian year-month (e.g. "1980-09") …
```

How that played out per generator:

- **SHACL**: the `uri:` is honoured. `sh:datatype xsd:gYear` and
  `sh:datatype xsd:gYearMonth` are emitted with the canonical XSD
  IRIs.
- **OWL**: `xsd:gYear` and `xsd:gYearMonth` are declared as
  `rdfs:Datatype` in the output and used directly in the
  `owl:unionOf` list. Correct.
- **JSON Schema**: only `base: str` survives — the `uri:` field is
  not consulted, so both types render as plain
  `{"type": "string"}`. There is no XSD-style hint left.
- **Pydantic / dataclasses**: same problem. Because there is no
  Python type for `gYear` / `gYearMonth`, both collapse to `str`,
  losing distinctness from each other and from any other `str`.

Note: a richer encoding would be to also add a `pattern:` (e.g.
`^\d{4}$` for gYear, `^\d{4}-\d{2}$` for gYearMonth). That would
be carried through into JSON Schema and Pydantic as a regex
constraint and would partially recover the distinction. We did
not add patterns here because the SEMIC original does not
constrain the literal lexical form either; following the spec's
laxer semantics is the right approximation.

## Files

- `original/releases/2.1.1/context/core-person-ap.jsonld` — official JSON-LD context
- `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl` — official SHACL
- `original/releases/2.1.1/voc/core-person-ap.ttl` — official OWL/RDF vocabulary
- `original/releases/2.1.1/index.html` — official HTML spec
- `src/core_person/schema/core_person.yaml` — LinkML schema
- `project/shacl/core_person.shacl.ttl` — generated SHACL
- `project/owl/core_person.owl.ttl` — generated OWL
- `project/jsonld/core_person.context.jsonld` — generated JSON-LD context
