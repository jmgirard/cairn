# M53: Prose-guard mutation harness (done)

- **Status:** done · **PR:** #51 · **Principles:** GP2, GP4
- **Archived:** 2026-07-13 · from RR01 rec 2 (highest-leverage change)

## Goal
Mechanize the recurring false-coverage guard trap (M39/M40/M47): prove each
prose-guard *fails* when the rule block it protects is blanked.

## Outcome
`skills/tests/mutation_engine.py` blanks a guard's registered block (exactly-once
locator) and re-runs it under a scoped `Path.read_text` patch — zero touch on
existing guards. `test_mutation_harness.py` holds the registry (15 entries / 14
files), a both-direction oracle, the driver, and a completeness meta-test that
fails CI on any unregistered prose-guard *file*. First run caught a real
false-coverage guard (`test_design_interview`) → re-anchored. Universal rule in
`tracking-rules.md` "What gets a test"; LESSONS graduated M39/M40/M47.

## Key decisions
- Registration is per guard *file* (≥1 exemplar block), not per assertion — a
  new `assertIn` in a registered file needs its own entry or the M47 by-hand
  check. Harness covers positive (`assertIn`) guards; `assertNotIn` isn't blanked.

## Review
5/5 ACs; `cairn_validate` 14/14. Fan-out: diff-bug clean, prior-PR no-op, blame-history 1 finding (82, overclaimed coverage) fixed in-review.
