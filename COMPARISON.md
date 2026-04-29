# LinkML vs SEMIC Core Person Vocabulary 2.1.1 — comparison

This document compares the artefacts generated from
`src/core_person/schema/core_person.yaml` (a hand-written LinkML
approximation of SEMIC Core Person 2.1.1) against the official
SEMIC artefacts in `originals/`.

## Counts

| metric                              | original                | linkml output           |
|-------------------------------------|-------------------------|-------------------------|
| SHACL `sh:NodeShape` count          | 14                      | 10                      |
| SHACL `sh:property` count           | 36                      | 36                      |
| OWL `owl:Class` declarations        | 2 (m8g:ContactPoint, m8g:GenericDate) | 10 (one per LinkML class, with `skos:exactMatch` to original) |
| OWL `owl:DatatypeProperty`          | 5                       | 24                      |
| OWL `owl:ObjectProperty`            | 3                       | 17                      |
| classes captured                    | Person, Identifier, Address, ContactPoint, Agent, Jurisdiction, Location, Document, Concept (Code), GenericDate | all 10 |
| total Person properties (SHACL)     | 18                      | 18                      |

## SHACL: what matches

- All 10 entity-class shapes round-trip with the **same target IRI**:
  `person:Person`, `adms:Identifier`, `locn:Address`,
  `m8g:ContactPoint`, `foaf:Agent`, `dcterms:Jurisdiction`,
  `dcterms:Location`, `foaf:Document`, `skos:Concept`,
  `m8g:GenericDate`.
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

- The 10 SEMIC classes all appear with `skos:exactMatch` linking the
  LinkML-internal IRI (`cpv:Person`) to the canonical IRI
  (`person:Person`). This is LinkML's standard "shadow class" pattern.
- `rdfs:label` and `skos:definition` for every class round-trip from
  LinkML.
- The vocabulary metadata (`dcterms:license`, `dcterms:title`,
  `pav:version`) is emitted on the `owl:Ontology`.

## OWL: what does not match

1. **Class IRIs differ.** Original declares `m8g:ContactPoint` and
   `m8g:GenericDate` directly as `owl:Class`. LinkML declares
   `cpv:ContactPoint` etc. with `skos:exactMatch m8g:ContactPoint`.
   This is the **single biggest expressivity gap**: a LinkML schema
   models classes in its own namespace and links out via
   `class_uri`, but `gen-owl` does not let you flip the class IRI to
   the external vocabulary.
2. **Property IRIs differ.** Same problem for slots: LinkML emits
   `cpv:familyName` (with `skos:exactMatch foaf:familyName`) instead
   of declaring `foaf:familyName` directly. The original re-uses
   external property IRIs and only declares the m8g-namespaced ones
   it owns.
3. **No `rdfs:isDefinedBy`** is emitted by `gen-owl`. The original has
   `rdfs:isDefinedBy <http://data.europa.eu/m8g>` on every property
   it owns.
4. **`rdfs:domain` and `rdfs:range` are not produced** as direct
   triples on properties. LinkML uses
   `owl:Restriction`/`owl:allValuesFrom`/`owl:onProperty` axioms
   under the class instead, which is more verbose and harder to read.
5. **`skos:scopeNote`** annotations on `birthDate`, `deathDate`,
   `gender`, `sex`, `ContactPoint` are not modelled by LinkML
   `comments`/`notes` round-tripping into OWL output.
6. **Multilingual labels** (`@en` and `@nl` on the ontology label) are
   lost — LinkML titles are single-string.
7. **Editor metadata** (`foaf:maker`, `dcterms:mediator`, list of
   `<…rec54#editor>` blank nodes) is not modelled in LinkML and is
   absent from the OWL.

## LinkML expressivity gaps surfaced by this exercise

1. **Cannot redeclare external IRIs as the OWL class/property IRI.**
   This is the main blocker for SEMIC use: SEMIC vocabularies *re-use*
   `foaf:`, `person:`, `dcterms:` IRIs directly; LinkML always emits
   shadow IRIs in its own namespace. The `class_uri` /`slot_uri`
   slots are only used as `skos:exactMatch` targets in `gen-owl`.
2. **Cannot model SHACL targets that point at datatype IRIs**
   (Date/Literal/Text/URI shapes in the original). LinkML treats
   datatypes as a closed registry separate from classes.
3. **No first-class union datatypes.** `m8g:GenericDate` is the union
   of `xsd:date`, `xsd:gYearMonth`, `xsd:gYear`. LinkML needs a
   user-defined type that erases the union; the union semantics are
   lost.
4. **No per-property `rdfs:isDefinedBy` / scope notes / spec anchors.**
   The original SHACL/OWL treat each property as a documented spec
   element with an HTML anchor — LinkML descriptions don't carry this.
5. **No mechanism to suppress shadow class declarations.** LinkML
   always declares `cpv:Foo` even when the intent is "I am only
   describing the existing `foaf:Agent` shape". This means the OWL
   output is roughly 4x the size of the original (615 vs 143 lines).

## Files

- `originals/core-person-ap.jsonld` — official JSON-LD context
- `originals/core-person-ap-SHACL.ttl` — official SHACL
- `originals/core-person-ap.ttl` — official OWL/RDF vocabulary
- `src/core_person/schema/core_person.yaml` — LinkML schema
- `project/shacl/core_person.shacl.ttl` — generated SHACL
- `project/owl/core_person.owl.ttl` — generated OWL
- `project/jsonld/core_person.context.jsonld` — generated JSON-LD context
