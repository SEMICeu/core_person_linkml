# `gen-shacl` emits `sh:ignoredProperties ( rdf:type )` on every NodeShape with no opt-out

## Context
The Core Person SHACL shapes are open (`sh:closed false`) and list only the
property paths the vocabulary defines. Since linkml `main` @ `1288dbb6`,
`gen-shacl` adds a `sh:ignoredProperties` list containing `rdf:type` to every
generated `sh:NodeShape` unconditionally — there is no CLI flag to suppress it
(`gen-shacl --help` exposes only `--closed/--non-closed` and
`--message-template`). None of the 14 upstream SEMIC NodeShapes carry
`sh:ignoredProperties`.

## Example input
```yaml
classes:
  Agent:
    class_uri: foaf:Agent
    description: Any entity carrying out actions, typically a person or an organisation.
    slots:
      - agentName
      - agentType
```

Generated with the bundled config (`--non-closed`; `config.yaml`
`closed: false`).

## Expected output
```turtle
foaf:AgentShape a sh:NodeShape ;
	rdfs:comment "Any entity carrying out actions, typically a person or an organisation." ;
	sh:closed false ;
	sh:property _:b0 , _:b1 ;
	sh:targetClass foaf:Agent .
```

No `sh:ignoredProperties` triple (the upstream `AgentShape` has none).

## Actual output
```turtle
foaf:AgentShape a sh:NodeShape ;
	rdfs:comment "Any entity carrying out actions, typically a person or an organisation." ;
	sh:closed false ;
	sh:ignoredProperties _:c14n32 ;
	sh:property _:c14n25 , _:c14n34 ;
	sh:targetClass foaf:Agent .

_:c14n32 rdf:first rdf:type ;
	rdf:rest rdf:nil .
```

(verbatim from `project/shacl/core_person.shacl.ttl`.) The same
`sh:ignoredProperties ( rdf:type )` block is emitted on all 9 generated
NodeShapes.

## Why this matters
`sh:ignoredProperties` only has an effect under closed-shape validation, so on
these open shapes the triple is inert but adds a per-shape blank-node list to
every NodeShape. It appears on every generated shape and on none of the
upstream SEMIC shapes, so it inflates every generated-vs-upstream SHACL diff
with noise that a consumer must filter out, and there is currently no flag to
turn it off.
