# `rdf:langString` is not a first-class LinkML type

## Context
SEMIC Core Person uses `rdf:langString` heavily for human-readable
multilingual fields: `foaf:familyName`, `foaf:givenName`, `foaf:name`,
`person:birthName`, `person:patronymicName`, `locn:thoroughfare`,
`locn:fullAddress`, `dcterms:title`, `dcterms:alternative`,
`rdfs:label`, and similar. LinkML's type registry has no first-class
language-tagged-string type. The workaround in this project is to
declare a custom `LangString` type backed by `base: str` with
`uri: rdf:langString`, but that only fixes the RDF generators —
JSON Schema, Pydantic, and Python lose the language-tag semantics.

## Example input
```yaml
types:
  LangString:
    typeof: string
    uri: rdf:langString
    base: str
    description: A natural-language string with an optional language tag.

slots:
  familyName:
    slot_uri: foaf:familyName
    range: LangString
    multivalued: true
```

## Expected output
A first-class language-tagged-string type would model the `@language`
tag at every layer:

```turtle
# SHACL — already works via the custom-type workaround
[ sh:datatype rdf:langString ; sh:path foaf:familyName ]
```

```json
// JSON Schema — should encode the language tag, e.g.
{
  "type": "object",
  "properties": {
    "@value":    {"type": "string"},
    "@language": {"type": "string", "pattern": "^[a-z]{2,3}(-[A-Z]{2,4})?$"}
  },
  "required": ["@value"]
}
```

```python
# Pydantic — a LangString model with `value: str` and `language: Optional[str]`
class LangString(BaseModel):
    value: str
    language: Optional[str] = None
```

## Actual output
SHACL works (the custom-type `uri:` lands as `sh:datatype rdf:langString`).
JSON Schema, Pydantic, and dataclasses all see `base: str` and emit
plain strings with no language-tag channel — the `@language` annotation
cannot be carried by data conforming to the generated schemas.

## Why this matters
Core Person is a multilingual EU vocabulary. The upstream SHACL and
context expect `dct:title`, `foaf:name`, address components, etc. to
carry `@language` tags. Without first-class langString support, data
that round-trips through the LinkML-generated JSON Schema or Python
data model loses its language tags — a German address becomes
indistinguishable from a French one at the type level.
