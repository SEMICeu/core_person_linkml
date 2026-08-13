# Structural and behavioural comparison

This document compares LinkML-generated SHACL for Core Person 2.1.2 with the
official SEMIC Core Person 2.1.2 SHACL distribution.

## Run metadata

| Field | Value |
|---|---|
| Baseline date | 2026-08-13 |
| Python | 3.12 |
| LinkML | 1.11.1 |
| pySHACL | 0.40.1 |
| RDFLib | 7.6.0 |
| Official source commit | `a1b13f2bed9fd97b28420b0cef7f0032da08d148` |

## Headline result

The candidate is not byte-identical or RDF-isomorphic to the official graph.
That difference is expected: the official graph contains 106 separately named,
hash-IRI property shapes, while LinkML consolidates the same class/path rules
into 49 property shapes.

The following normative constraint counts match:

| Component | Official | Candidate |
|---|---:|---:|
| Node shapes | 15 | 15 |
| `sh:class` | 18 | 18 |
| `sh:datatype` | 21 | 21 |
| `sh:nodeKind` | 49 | 49 |
| `sh:uniqueLang` | 18 | 18 |
| `sh:closed` | 15 | 15 |
| `sh:minCount` | 0 | 0 |
| `sh:maxCount` | 0 | 0 |

Matching counts are evidence, not proof. The behavioural test corpus currently
covers open and multivalued data, language uniqueness, object class, URI
literal and issued-date constraints. Official and candidate validation results
agree on these fixtures.

## SEMIC adapter requirements

Stock LinkML 1.11.1 does not reproduce every Core Person constraint directly.
The deterministic adapter in `src/core_person/baseline.py` implements explicitly
traceable support for:

- `sh:uniqueLang`;
- unrestricted RDF literals;
- `xsd:anyURI` values represented as literals; and
- four datatype-target compatibility shapes used by the official publication.

These are project-owned extensions, not claims about stock LinkML behaviour.

## Decisions still required

1. Complete focused positive and negative fixtures for all 49 rules.
2. Decide the LinkML representation of the documented GenericDate union.
3. Decide whether official hash-IRI property-shape identifiers must be retained.
4. Ask the SEMIC Working Group to approve the traceability mapping and the
   semantic acceptance gate.

The detailed machine-readable result is
`project/reports/shacl-comparison.json`.
