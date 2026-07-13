# M44: Validator-hardening — sizing advisory + Priority-field schema — done

**Status:** done · merged 2026-07-13 · PR #42

## Goal
Give `cairn_validate` the two judgment-call checks it lacked: a non-failing
sizing advisory and a hard Priority-field vocabulary check.

## Outcome
- Non-failing **advisory (WARN/OK) tier** (`ADVISORIES`) in
  `cairn_validate.run()` — exit-code neutral, separate from PASS/FAIL.
- `check_sizing_advisory`: WARNs when a live milestone exceeds the split
  tripwires (>7 criteria, >10 tasks); archived files skipped.
- `check_priority_vocab`: hard FAIL when a ROADMAP Priority ∉
  {high, normal, low}, parallel to `check_vocab`.
- `/milestone` Audit documents advisories (report-but-don't-fix). Folded two
  M06 steals; dropped two low-fit steals via D-026.

## Key decisions
- D-026: dropped the parallel-task-metadata and tiered-tool-exposure M06
  steals — they don't fit cairn's single-milestone, human-gated model.

## Evidence
5/5 acceptance criteria verified; 58/58 script tests; live validate exit 0
(13 PASS + OK sizing). Independent review: 3 lenses, zero findings.
