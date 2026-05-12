# No top-of-file `rdfs:member` collection of all NodeShapes

## Context
The upstream Core Person SHACL declares the SHACL file itself as a
resource and uses `rdfs:member` to enumerate every NodeShape it
contains. This is a directory-style index that lets a consumer load
the file and iterate over its shapes without having to query for
`?s a sh:NodeShape`. LinkML's `gen-shacl` does not emit anything
equivalent.

## Example input
```yaml
# Any LinkML schema with classes that produce NodeShapes
classes:
  Person:
    class_uri: person:Person
  ContactPoint:
    class_uri: m8g:ContactPoint
  # … etc.
```

## Expected output
```turtle
<…/core-person-ap-SHACL.ttl> rdfs:member
  <…/core-person-ap-SHACL.ttl#ContactPointShape>,
  <…/core-person-ap-SHACL.ttl#GenericDateShape>,
  <…/core-person-ap-SHACL.ttl#JurisdictionShape>,
  <…/core-person-ap-SHACL.ttl#LocationShape>,
  <…/core-person-ap-SHACL.ttl#TextShape>,
  <…/core-person-ap-SHACL.ttl#LiteralShape>,
  <…/core-person-ap-SHACL.ttl#URIShape>,
  <…/core-person-ap-SHACL.ttl#DateShape>,
  <…/core-person-ap-SHACL.ttl#CodeShape>,
  <…/core-person-ap-SHACL.ttl#IdentifierShape>,
  <…/core-person-ap-SHACL.ttl#AddressShape>,
  … .
```

(verbatim from `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl`
lines 9–24.)

## Actual output
None — `project/shacl/core_person.shacl.ttl` declares each NodeShape
individually but contains no `rdfs:member` enumeration and no
top-level subject for the SHACL file as a whole.

## Why this matters
A `rdfs:member` block is a cheap-to-emit index that makes it possible
to ask "which shapes live in this file?" without a full RDF parse and
type-filter. The upstream SEMIC file uses it; profiles built on top of
Core Person inherit the same convention. Without it, the generated
LinkML SHACL is harder to consume in tools that expect the
upstream-style directory.
