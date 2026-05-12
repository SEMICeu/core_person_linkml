# No `rdfs:isDefinedBy` emitted on classes or properties

## Context
The upstream Core Person OWL vocabulary attaches
`rdfs:isDefinedBy <http://data.europa.eu/m8g>` to every class and
property that lives in the `m8g:` namespace. This is the canonical RDF
mechanism for saying "the definition of this term lives in vocabulary
X". `gen-owl` and `gen-shacl` do not emit it, regardless of CLI flags
explored so far.

## Example input
```yaml
slots:
  dateOfBirth:
    slot_uri: m8g:birthDate
    title: date of birth
    description: The point in time on which the Person was born.
    range: date
```

## Expected output
```turtle
m8g:birthDate a owl:DatatypeProperty ;
  rdfs:label "date of birth"@en ;
  rdfs:comment "The point in time on which the Person was born."@en ;
  rdfs:domain person:Person ;
  rdfs:isDefinedBy <http://data.europa.eu/m8g> ;
  rdfs:range <http://data.europa.eu/m8g/GenericDate> .
```

(verbatim from `original/releases/2.1.1/voc/core-person-ap.ttl` lines
10–15.)

## Actual output
```turtle
m8g:birthDate a owl:DatatypeProperty ;
    rdfs:label "dateOfBirth" ;
    dcterms:title "date of birth" ;
    rdfs:range [ a rdfs:Datatype ;
            owl:unionOf ( xsd:date xsd:gYear xsd:gYearMonth ) ] ;
    skos:definition "The point in time on which the Person was born." ;
    skos:inScheme <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> ;
    skos:note "The date of birth could be expressed as date, gYearMonth or gYear, e.g. 1980-09-16, 1980-09, 1980." .
```

(verbatim from `project/owl/core_person.owl.ttl` lines 46–53.) No
`rdfs:isDefinedBy` is emitted on this property, and the same is true for
every other property and every class in the file.

## Why this matters
`rdfs:isDefinedBy` is how a reasoner or consumer follows a property
back to its source ontology. For Core Person, where most properties
are owned by the EU m8g vocabulary but re-used here, the absence of
this triple means downstream consumers cannot tell from the generated
OWL alone which terms belong to which authoritative vocabulary.
