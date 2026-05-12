# Custom XSD datatypes (`xsd:gYear`, `xsd:gYearMonth`) collapse to `str` in non-RDF generators

## Context
SEMIC Core Person 2.1.1 wants `m8g:birthDate` / `m8g:deathDate` to
accept a union of `xsd:date`, `xsd:gYear`, and `xsd:gYearMonth`.
LinkML's built-in type registry only ships `date`, `datetime`,
`date_or_datetime`, and `time` — there is no `gYear` / `gYearMonth`.
The schema declares them as custom types backed by `base: str` with
explicit `uri: xsd:gYear` / `uri: xsd:gYearMonth`. The RDF generators
honour the `uri:` (correct `sh:datatype` / `owl:unionOf` output); the
JSON Schema, Pydantic, and Python-dataclasses generators do not — they
see two `base: str` types and collapse both to `str`.

## Example input
```yaml
types:
  gYear:
    uri: xsd:gYear
    base: str
    description: An XSD gregorian year (e.g. "1980").
  gYearMonth:
    uri: xsd:gYearMonth
    base: str
    description: An XSD gregorian year-month (e.g. "1980-09").

slots:
  dateOfBirth:
    slot_uri: m8g:birthDate
    multivalued: true
    any_of:
      - range: date
      - range: gYear
      - range: gYearMonth
```

## Expected output
SHACL (round-trips correctly, shown for reference):

```turtle
[ sh:or (
    [ sh:datatype xsd:date    ; sh:nodeKind sh:Literal ]
    [ sh:datatype xsd:gYear   ; sh:nodeKind sh:Literal ]
    [ sh:datatype xsd:gYearMonth ; sh:nodeKind sh:Literal ]
  ) ; sh:path m8g:birthDate ]
```

JSON Schema should preserve the three-way distinction (e.g. via
`format` or `pattern`):

```json
"anyOf": [
  {"type": "string", "format": "date"},
  {"type": "string", "pattern": "^\\d{4}$"},          // gYear
  {"type": "string", "pattern": "^\\d{4}-\\d{2}$"}    // gYearMonth
]
```

Pydantic / Python should likewise carry distinct types so static
checks can tell `gYear` from `gYearMonth`.

## Actual output
JSON Schema (`project/jsonschema/core_person.schema.json`) — both
`gYear` and `gYearMonth` branches collapse to bare strings with no
pattern; only the `date` branch keeps its `format`:

```json
"anyOf": [
  {"format": "date", "type": "string"},
  {"type": "string"},
  {"type": "string"}
]
```

Pydantic (`src/core_person/datamodel/core_person_pydantic.py`) — the
field is `Optional[list[Union[date, str]]]`: three distinct LinkML
types collapse to two Python types because `gYear` and `gYearMonth`
share `base: str`. The `any_of` metadata is preserved in
`json_schema_extra`, so callers reading the metadata can still see the
intent, but static checking cannot tell the three datatypes apart.

Python dataclasses (`src/core_person/datamodel/core_person.py`) — the
field becomes `Optional[Union[str, list[str]]]`: `xsd:date` is silently
dropped from the union and the field accepts any string. The `any_of`
semantics are lost entirely.

## Why this matters
The whole point of the date-disjunction custom-types workaround is to
let Core Person record partial dates (year only, year+month, full
date). The SHACL and OWL outputs preserve that distinction faithfully,
so RDF validators reject malformed inputs. But applications that
consume the JSON Schema or Python data model lose the distinction at
the type level, so a string `"foo"` validates the same as a four-digit
year. The asymmetry between the RDF generators and the
JSON-and-Python end of the toolchain is the gap.
