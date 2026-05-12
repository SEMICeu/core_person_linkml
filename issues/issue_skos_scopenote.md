# `skos:scopeNote` annotations not round-tripped from LinkML

## Context
The upstream Core Person OWL vocabulary attaches `skos:scopeNote`
annotations to `m8g:birthDate`, `m8g:deathDate`, `m8g:gender`,
`m8g:sex`, and `m8g:ContactPoint` — these are human-authored guidance
strings (often containing recommended controlled vocabularies or
worked examples). LinkML's schema-level `comments`/`notes` slots
don't round-trip into `skos:scopeNote` on the OWL or SHACL output.

## Example input
```yaml
slots:
  dateOfBirth:
    slot_uri: m8g:birthDate
    description: The point in time on which the Person was born.
    comments:
      - >-
        The date of birth could be expressed as date, gYearMonth or
        gYear, e.g. 1980-09-16, 1980-09, 1980.
```

## Expected output
```turtle
m8g:birthDate a owl:DatatypeProperty ;
  rdfs:label "date of birth"@en ;
  rdfs:comment "The point in time on which the Person was born."@en ;
  skos:scopeNote """The date of birth could be expressed as date, gYearMonth or gYear, example:
<ul><li>- 1980-09-16^^xs:date</li>…</ul>""" .
```

(structure of `original/releases/2.1.1/voc/core-person-ap.ttl`
lines 10–22.)

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

The LinkML `comments` value lands on `skos:note`, not `skos:scopeNote`.
`skos:note` is the SKOS generic note property; `skos:scopeNote` is the
specific subproperty that the upstream vocabulary uses to mark
"guidance about scope of intended meaning".

## Why this matters
`skos:scopeNote` is a stronger semantic signal than `skos:note`: it
specifically tells consumers "this annotation is guidance on how to
choose values for this property". The mapping from LinkML `comments`
to `skos:note` is a downgrade — a downstream consumer reading the
generated OWL cannot distinguish a curated scope note from any other
informal annotation. Same gap applies to `m8g:deathDate`, `m8g:gender`,
`m8g:sex`, and `m8g:ContactPoint`.
