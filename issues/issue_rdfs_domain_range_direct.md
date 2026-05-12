# `rdfs:domain` and `rdfs:range` not emitted as direct triples on properties

## Context
The upstream Core Person OWL vocabulary uses direct
`rdfs:domain` / `rdfs:range` triples on every property declaration.
LinkML's `gen-owl` instead encodes range information via
`owl:Restriction` / `owl:allValuesFrom` / `owl:onProperty` axioms under
each class. The semantic content is broadly equivalent but the
syntactic form is harder to read, verbose, and diverges from
established OWL vocabulary conventions.

## Example input
```yaml
classes:
  Person:
    class_uri: person:Person
    slots:
      - dateOfBirth

slots:
  dateOfBirth:
    slot_uri: m8g:birthDate
    range: date
```

## Expected output
```turtle
m8g:birthDate a owl:DatatypeProperty ;
  rdfs:domain person:Person ;
  rdfs:range xsd:date .
```

(structure of `original/releases/2.1.1/voc/core-person-ap.ttl`
lines 10–15 for `m8g:birthDate`.)

## Actual output
The range is emitted only as an `owl:Restriction` axiom under the
`Person` class:

```turtle
person:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:allValuesFrom [ a rdfs:Datatype ;
                    owl:unionOf ( xsd:date xsd:gYear xsd:gYearMonth ) ] ;
            owl:onProperty m8g:birthDate ],
        [ a owl:Restriction ;
            owl:onClass m8g:birthDate ;
            owl:onProperty m8g:birthDate ;
            owl:qualifiedCardinality 0 ] ,
        … .
```

The property itself (`m8g:birthDate a owl:DatatypeProperty`) has its
range as an inline blank-node datatype union but **no `rdfs:domain`
triple** anywhere.

## Why this matters
Tools that read OWL property declarations look for `rdfs:domain` and
`rdfs:range` directly on the property; many do not unfold
`owl:Restriction` axioms to reconstruct that information. Without
direct domain/range triples the generated OWL is not idiomatic and
loses interoperability with these tools, even though it remains
logically equivalent.
