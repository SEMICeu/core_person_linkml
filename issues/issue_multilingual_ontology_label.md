# Ontology-header labels can only be single-string, not multilingual

## Context
The upstream Core Person OWL vocabulary declares its ontology with
multiple language-tagged titles on the `owl:Ontology` resource — the
upstream uses both `@en` and `@nl` strings on the same label/title
property. LinkML's schema header (`title:` / `description:`) accepts a
single string per field, so the multilingual title information is lost
when the schema is round-tripped through `gen-owl`.

## Example input
```yaml
id: https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1
name: core_person
title: Core Person Vocabulary
description: >-
  LinkML approximation of the SEMIC Core Person Vocabulary 2.1.1.
```

## Expected output
```turtle
<https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> a owl:Ontology ;
  dcterms:title "Core Person Vocabulary"@en ,
                "Kernwoordenschat Persoon"@nl ;
  rdfs:label    "Core Person Vocabulary"@en ,
                "Kernwoordenschat Persoon"@nl .
```

(structure of `original/releases/2.1.1/voc/core-person-ap.ttl`
ontology-header block.)

## Actual output
```turtle
<https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1> a owl:Ontology ;
    rdfs:label "core_person" ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:title "Core Person Vocabulary" ;
    pav:version "2.1.1" .
```

(from `project/owl/core_person.owl.ttl` header.) The title is a single
plain string with no `@en` tag and no `@nl` companion.

## Why this matters
Core Person is multilingual by design (the EU SEMIC suite is published
in multiple official languages). The ontology header is the canonical
place where multilingual titles live; if LinkML can't represent
multiple language-tagged titles, the generated OWL loses parity with
the upstream vocabulary's metadata. (This is the ontology-header
analogue of `issue_langstring_first_class.md`, which covers the same
gap at the slot/range level.)
