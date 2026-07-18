# `gen-owl` emits `skos:inScheme <ontology-iri>` on every class and property

## Context
The Core Person LinkML schema re-uses external class and property IRIs
(`person:Person`, `foaf:Agent`, `m8g:birthDate`, …). Since linkml `main` @
`1288dbb6`, `gen-owl` stamps every declared class and property with a
`skos:inScheme` triple pointing at the ontology IRI (the schema `id`). The
upstream SEMIC OWL vocabulary (`original/releases/2.1.1/voc/core-person-ap.ttl`)
carries no `skos:inScheme` on any term.

## Example input
```yaml
classes:
  ContactPoint:
    class_uri: m8g:ContactPoint
    description: Information (e.g. e-mail address, telephone number) of a person or department through which the user can get in touch with.
```

Generated with the bundled config
(`--no-use-native-uris --metadata-profile rdfs --ontology-uri-suffix ''`, see
`config.public.mk`).

## Expected output
```turtle
m8g:ContactPoint a owl:Class ;
	rdfs:comment "Information (e.g. e-mail address, telephone number) of a person or department through which the user can get in touch with." ;
	rdfs:label "ContactPoint" .
```

No `skos:inScheme` triple (the upstream `m8g:ContactPoint` declaration has
none).

## Actual output
```turtle
m8g:ContactPoint a owl:Class ;
	rdfs:comment "Information (e.g. e-mail address, telephone number) of a person or department through which the user can get in touch with." ;
	rdfs:label "ContactPoint" ;
	skos:exactMatch cpv:ContactPoint ;
	skos:inScheme <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> .
```

(verbatim from `project/owl/core_person.owl.ttl`.) The same
`skos:inScheme <…/2.1.1>` triple is emitted on every declared class and every
declared property.

## Why this matters
The upstream Core Person OWL is a thin re-use vocabulary that declares no
`skos:inScheme` provenance on its terms. Adding it to all 9 classes and all
~40 properties introduces a triple per term that has no upstream counterpart,
inflating every generated-vs-upstream OWL diff, and there is currently no flag
to turn it off.
