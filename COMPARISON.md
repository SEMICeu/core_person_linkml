# LinkML vs SEMIC Core Person Vocabulary 2.1.1 — comparison

| Field | Value |
|---|---|
| Last refreshed | 2026-05-12 |
| LinkML (generators) commit | `1c5f68e43a6960ec1066521f0d5bb112cebde21a` (1.11.0rc3.post8.dev0+1c5f68e4) |
| linkml-runtime commit | `1c5f68e43a6960ec1066521f0d5bb112cebde21a` (1.11.0rc3.post8.dev0+1c5f68e4) |
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
| SHACL `sh:property` count           | 36                      | 36                      |
| OWL `owl:Class` declarations        | 2 (m8g:ContactPoint, m8g:GenericDate) | 9 (external IRI subjects when generated with `--no-use-native-uris`; each retains a `skos:exactMatch cpv:Foo` back-pointer to the local namespace) |
| OWL `owl:DatatypeProperty`          | 5                       | 24                      |
| OWL `owl:ObjectProperty`            | 3                       | 17                      |
| classes captured                    | Person, Identifier, Address, ContactPoint, Agent, Jurisdiction, Location, Document, Concept (Code), GenericDate | 9 (GenericDate replaced by slot-level `any_of` of xsd:date / xsd:gYear / xsd:gYearMonth) |
| total Person properties (SHACL)     | 18                      | 18                      |
| OWL file size (lines)               | 143                     | 625 with `--no-use-native-uris`, 631 with the default `--use-native-uris` |

**Note on OWL generation flag.** The OWL output bundled in
`project/owl/core_person.owl.ttl` was produced with the non-default
`--no-use-native-uris` flag so that subject IRIs match the external
SEMIC vocabulary (`m8g:`, `foaf:`, `person:`, `locn:`, …) rather than
the schema-internal `cpv:` namespace. See "OWL: what does not match"
below for what this flag does and does not solve.

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
6. **Property shapes are inlined as blank nodes** in the LinkML output
   instead of named `…/<sha-hash>` IRIs. The original hash-named
   property shapes can be referenced from outside; LinkML's blank
   nodes cannot.
7. **No `sh:datatype xsd:anyURI` constraint** for `Identifier.schemeUri`
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

## LinkML expressivity gaps surfaced by this exercise

1. **Residual class-IRI back-pointer in `gen-owl --no-use-native-uris`.**
   *Not a capability gap — a narrow upstream bug.* The default mode
   (`--use-native-uris`) emits the LinkML-internal IRI as the OWL
   subject and `skos:exactMatch` to the external one; that is wrong
   for SEMIC. `--no-use-native-uris` flips the subject for both
   classes and slots. For slots this is a clean fix. For classes,
   a `skos:exactMatch cpv:Foo` back-pointer to the unused local IRI
   is still emitted (see `linkml/generators/owlgen.py:432-438`). The
   right next action is a small upstream patch / issue, not a
   metamodel discussion.
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
