# `gen-owl --no-use-native-uris` still emits `skos:exactMatch cpv:Foo` back-pointer on classes

## Context
The Core Person LinkML schema re-uses external class IRIs (`person:Person`,
`foaf:Agent`, `m8g:ContactPoint`, …) via `class_uri`. With the default
`--use-native-uris` flag, `gen-owl` emits the schema-internal `cpv:Foo`
IRI as the subject and `skos:exactMatch` to the external one — wrong for
SEMIC, which simply re-uses the external IRIs. The `--no-use-native-uris`
flag flips the subject to the external IRI. For **slots** this works
cleanly. For **classes** there is a residual: a `skos:exactMatch cpv:Foo`
back-pointer to the otherwise-unused local IRI is still emitted on every
external class subject. The relevant generator code is
`linkml/generators/owlgen.py:432-438`.

## Example input
```yaml
classes:
  Person:
    class_uri: person:Person
    description: An individual human being who may be dead or alive, but not imaginary.
```

Generated with `LINKML_GENERATORS_OWL_ARGS="--no-use-native-uris"` (the
bundled config — see `config.public.mk`).

## Expected output
```turtle
person:Person a owl:Class ;
  rdfs:label "Person" ;
  skos:definition "An individual human being who may be dead or alive, but not imaginary." ;
  skos:inScheme <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> ;
  rdfs:subClassOf [ … cardinality axioms … ] .
```

No `skos:exactMatch cpv:Person` (the `cpv:Person` IRI is otherwise
unused in the OWL output).

## Actual output
```turtle
person:Person a owl:Class ;
    rdfs:label "Person" ;
    rdfs:subClassOf [ … cardinality axioms … ] ;
    skos:definition "An individual human being who may be dead or alive, but not imaginary." ;
    skos:exactMatch cpv:Person ;
    skos:inScheme <https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> .
```

(verbatim from `project/owl/core_person.owl.ttl` line 315 onward, with
the back-pointer at line 440.)

Slot output for the same flag is clean — `m8g:birthDate` is declared
directly under its external IRI with no `cpv:` back-pointer, confirming
that the residual is class-only.

## Why this matters
The whole purpose of `--no-use-native-uris` for SEMIC is to make the
generated OWL look like a single-namespace re-use vocabulary. The
trailing `skos:exactMatch cpv:Person` triple introduces a parallel IRI
that doesn't exist in the upstream Core Person vocabulary and is the
only reason the local `cpv:Person` IRI ever surfaces. It muddies any
diff between the generated and upstream OWL and forces a downstream
consumer to filter the back-pointer out.
