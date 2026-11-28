# M30: Stop cairn_validate false-flagging R CMD check counts as non-ISO dates

- **Status:** done
- **PR:** https://github.com/jmgirard/cairn/pull/28 (squash-merged 2026-07-12)

## Goal

Tighten `cairn_validate`'s slash-date matcher to require a 4-digit year so R
CMD check count-notation (`0 / 0 / 0`) no longer trips the non-ISO-date check.

## Outcome

The `_NON_ISO_DATE` slash branch was narrowed from `\d{1,4}/\d{1,2}/\d{1,4}` to
year-first (`\d{4}/\d{1,2}/\d{1,2}`) OR year-last (`\d{1,2}/\d{1,2}/\d{4}`):
count-triples now pass, real slash dates in both orders still caught. Test-first
`test_check_result_notation_passes` + format cases; suite 34/34, validate clean.
Absorbed G-C2; retired the M21 spaced-form workaround. Two-lens review: zero
findings.

## Key decisions

- **D-023** — slash branch requires a 4-digit year, superseding M13's
  "conservative by design" rationale for that branch only. Accepted miss:
  2-digit-year slash dates (`07 / 11 / 26`) go uncaught (none exist in-repo).
  Rejected range validation and context-exclusion.
