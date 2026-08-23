# M51: Oracle-registry doctrine (shape-free)

- **Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/49
- **Principles touched:** GP4

## Goal

Fold a shape-free oracle-registry requirement into the Validation doctrine so
the ≥2-independent-types bar is auditable at scale, without fixing a shape.

## Outcome

`tracking-rules.md` Validation doctrine now names an "Oracle registry
(auditability)" rule: every oracle is recorded by **ID, type, asserting
`test:line`, source, and provenance** (the test is the single source of truth
the record maps to), and the record's **shape is the repo's choice** — central
file, distributed generator headers, or embedded fixture fields all satisfy it.
Locked by two `test_oracle_doctrine.py` anchors; gates had cleared (M42, M45–M49).

## Key decisions

- **D-029** — registry generalizes as shape-free *content* doctrine, not a
  central `ORACLES.md` file (symmetric to M49/D-028). Rejected a central file
  and a `cairn_validate` CHECK; annotates D-024/D-025; graduated the candidate.
  Review: 4/4 ACs, validate 14/14, three-lens review zero findings.
