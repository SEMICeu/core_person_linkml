# No per-property `rdfs:seeAlso` pointer to spec HTML anchor

## Context
The upstream Core Person SHACL attaches a per-property
`rdfs:seeAlso "<spec-anchor>"` to every property shape, pointing at
the HTML anchor for that property in the published spec (e.g.
`https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.gender`).
LinkML's `gen-shacl` does not emit anything equivalent: descriptions
are landed via `sh:description`, but there is no mechanism to attach
a documentation URL.

## Example input
```yaml
slots:
  gender:
    slot_uri: m8g:gender
    title: gender
    description: The identities, expressions and societal roles of the Person.
    range: Concept
    multivalued: true
```

## Expected output
```turtle
<…/PersonShape/c2c54ded…> rdfs:seeAlso "https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.gender" ;
  sh:class skos:Concept ;
  sh:description "The identities, expressions and societal roles of the Person."@en ;
  sh:name "gender"@en ;
  sh:path m8g:gender .
```

(verbatim from `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl`
lines 295–299.)

## Actual output
```turtle
[ sh:class skos:Concept ;
    sh:description "The identities, expressions and societal roles of the Person." ;
    sh:name "gender" ;
    sh:nodeKind sh:BlankNodeOrIRI ;
    sh:order 12 ;
    sh:path m8g:gender ]
```

(verbatim from `project/shacl/core_person.shacl.ttl` lines 228–233.)
No `rdfs:seeAlso` triple, and the property shape itself is a blank
node so even an external `seeAlso` could not target it.

## Why this matters
The `rdfs:seeAlso` pointer is the round-trip channel between the
machine-readable SHACL and the human-readable spec HTML — it is how
tools open the right section of the spec when they hit a particular
property. Without it, generated SHACL is severed from its
documentation source. (Note: this gap also requires named property
shape IRIs — see `issue_shacl_property_shape_named_iri.md` — because
`rdfs:seeAlso` needs a stable subject IRI to attach to.)
