# `gen-owl` emits annotation values as string literals; `gen-shacl` emits them as IRIs

## Context
LinkML supports per-slot `annotations:` blocks. With `gen-shacl
--include-annotations` (or the config-yaml equivalent) the same
annotation round-trips into both the SHACL output and the OWL output.
But the two generators disagree on how to type the annotation **value**:
`gen-shacl` parses an IRI-looking value as an IRI (`<…>` form), while
`gen-owl` keeps it as a plain string literal. For upstream Core Person
properties like `rdfs:isDefinedBy <http://data.europa.eu/m8g>` (canonically
an IRI), only the SHACL side is semantically correct.

## Example input
```yaml
slots:
  dateOfBirth:
    slot_uri: m8g:birthDate
    annotations:
      rdfs:seeAlso: https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.birthdate
      rdfs:isDefinedBy: http://data.europa.eu/m8g
```

(verbatim from `src/core_person/schema/core_person.yaml`.)

## Expected output
Both `gen-shacl` and `gen-owl` should treat the annotation value as
the same RDF node kind. Upstream Core Person uses these as IRIs, so
the IRI form (matching SHACL) is what consumers expect:

```turtle
# OWL
m8g:birthDate a owl:DatatypeProperty ;
  rdfs:isDefinedBy <http://data.europa.eu/m8g> ;
  rdfs:seeAlso <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.birthdate> .
```

## Actual output
**SHACL (correct — IRI form):**

```turtle
[ rdfs:isDefinedBy <http://data.europa.eu/m8g> ;
    rdfs:seeAlso <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.birthdate> ;
    sh:description "The point in time on which the Person was born." ;
    sh:path m8g:birthDate ]
```

(verbatim from `project/shacl/core_person.shacl.ttl`.)

**OWL (wrong — string literal form):**

```turtle
m8g:birthDate a owl:DatatypeProperty ;
    rdfs:isDefinedBy "http://data.europa.eu/m8g" ;
    rdfs:seeAlso "https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.birthdate" .
```

(verbatim from `project/owl/core_person.owl.ttl`.) Note the double
quotes around the value — RDF parsers will read this as a plain
`xsd:string`, not as an IRI.

## Why this matters
For `rdfs:isDefinedBy` and `rdfs:seeAlso` specifically — both of which
are formally `rdf:Property` instances expecting `rdfs:Resource` (IRI)
objects in the upstream Core Person OWL — the string-literal form
breaks the RDF semantics. A reasoner or vocabulary browser following
`?prop rdfs:isDefinedBy ?ontology` won't match across the two
serialisations of the same schema, and the OWL output diverges from
upstream even though we are passing the right input. The LinkML
`annotations:` mechanism is the cleanest extension point for per-slot
RDF triples; the gap is that `gen-owl` doesn't auto-detect IRI-looking
values the way `gen-shacl` does.
