# Property shapes are emitted as blank nodes, not as named IRIs

## Context
The upstream Core Person SHACL declares every property shape with a
stable, named IRI of the form
`<…/<ParentShape>/<sha-hex>>` (e.g.
`<…/PersonShape/c2c54ded0a433cc00911573f794f1aeab900c624>`). This
allows external profiles to reference an individual property shape and
attach additional constraints to it. LinkML's `gen-shacl` instead
inlines property shapes as blank nodes inside the parent node shape,
which cannot be referenced from outside the file.

## Example input
```yaml
classes:
  Person:
    class_uri: person:Person
    slots:
      - gender

slots:
  gender:
    slot_uri: m8g:gender
    range: Concept
    multivalued: true
```

## Expected output
```turtle
person:PersonShape a sh:NodeShape ;
  sh:targetClass person:Person ;
  sh:property <…/PersonShape/c2c54ded0a433cc00911573f794f1aeab900c624> .

<…/PersonShape/c2c54ded0a433cc00911573f794f1aeab900c624>
  rdfs:seeAlso "https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.gender" ;
  sh:class skos:Concept ;
  sh:description "The identities, expressions and societal roles of the Person."@en ;
  sh:name "gender"@en ;
  sh:path m8g:gender .
```

(structure of `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl`
lines 295–299.)

## Actual output
```turtle
person:PersonShape a sh:NodeShape ;
    rdfs:comment "An individual human being who may be dead or alive, but not imaginary." ;
    sh:closed false ;
    sh:property [ sh:class skos:Concept ;
            sh:description "The identities, expressions and societal roles of the Person." ;
            sh:name "gender" ;
            sh:nodeKind sh:BlankNodeOrIRI ;
            sh:order 12 ;
            sh:path m8g:gender ],
        … other property shapes as blank nodes …
        ;
    sh:targetClass person:Person .
```

(verbatim from `project/shacl/core_person.shacl.ttl` lines 160 and
228–233.) Every property shape is a `[ … ]` blank node nested inside
the parent NodeShape.

## Why this matters
Two consequences. First, external SHACL profiles cannot attach
additional triples (`rdfs:seeAlso`, custom severity, extra
constraints) to an individual property shape, because there is no
stable subject IRI to attach to. Second, the
`issue_seealso_property_anchor.md` gap is downstream of this one:
even if `gen-shacl` learned how to emit `rdfs:seeAlso` per property,
that triple would have nowhere to land while property shapes remain
blank-node-inlined.
