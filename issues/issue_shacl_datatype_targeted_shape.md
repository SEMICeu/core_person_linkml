# Cannot emit `sh:NodeShape` whose `sh:targetClass` is a datatype IRI

## Context
SEMIC Core Person 2.1.1 declares four SHACL node shapes whose target is a
datatype, not a class: `DateShape` (target `xsd:date`), `LiteralShape`
(target `rdfs:Literal`), `TextShape` (target `rdf:langString`), and
`URIShape` (target `xsd:anyURI`). LinkML treats datatypes as a closed
registry separate from classes, so there is no way to generate a node
shape with a datatype IRI as its target.

## Example input
The upstream SHACL declares these shapes directly. The closest LinkML
equivalent would be to declare a class whose `class_uri` is a datatype
IRI:

```yaml
classes:
  DateShape:
    class_uri: xsd:date          # not allowed — datatypes aren't classes
    description: SHACL shape targeting xsd:date literals
```

## Expected output
```turtle
<…/core-person-ap-SHACL.ttl#DateShape> a sh:NodeShape ;
  sh:closed false ;
  sh:targetClass xsd:date .

<…/core-person-ap-SHACL.ttl#LiteralShape> a sh:NodeShape ;
  sh:closed false ;
  sh:targetClass rdfs:Literal .

<…/core-person-ap-SHACL.ttl#TextShape> a sh:NodeShape ;
  sh:closed false ;
  sh:targetClass rdf:langString .

<…/core-person-ap-SHACL.ttl#URIShape> a sh:NodeShape ;
  sh:closed false ;
  sh:targetClass xsd:anyURI .
```

(verbatim from `original/releases/2.1.1/shacl/core-person-ap-SHACL.ttl`
lines 110–112, 179–181, 331–333, 335–337.)

## Actual output
None — `project/shacl/core_person.shacl.ttl` emits the 9 entity-class
node shapes (`person:PersonShape`, `m8g:ContactPointShape`, …) but no
shape targeted at a datatype.

## Why this matters
The upstream SEMIC SHACL uses these datatype-targeted shapes to allow
external profiles to attach constraints to specific XSD types (e.g.
patterns on `xsd:date`, language-tag requirements on `rdf:langString`).
A LinkML profile cannot reproduce that fan-out point, so any downstream
profile that extends Core Person via the `DateShape` / `LiteralShape` /
`TextShape` / `URIShape` extension points loses its hook.
