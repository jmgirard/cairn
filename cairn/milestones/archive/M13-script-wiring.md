# M13: Wire deterministic scripts into review + plan — done

**Status:** done · approved 2026-07-11 · normal · Depends: — · PR #11 (squash
2b6a42e). Promoted from the deterministic-script-wiring candidate (M10 Out).

## Goal
Wire M10's read-only scripts into `/milestone-review` and `/milestone-plan`, and add a date-format check to `cairn_validate`.

## Outcome
`/milestone-review`'s consistency gate now runs `cairn_validate.py` first
(mechanical cairn-file checks); `/milestone-plan` step 1 runs `cairn_next.py`
to confirm nothing is in-progress. `cairn_validate` gained a 9th check, "iso
date format": flags non-ISO calendar dates (slash, year-last dashed,
month-name, and unpadded year-first ISO) in status/decision files;
conservative patterns skip versions/anchors/IDs; excludes `references/` and
`legacy/`. Scripts suite 21 green, skills 17 green.

## Decisions
- Date check is conservative-by-construction: catches recognizable wrong-format
  dates only; prose relative dates ("yesterday") stay LLM-owned.

## Review
Opus fresh-context: no blocking issues. Fixed — malformed-ISO detection,
review-skill check-list (8→9), test hardening. Rejected — guarding three-part
slash / range tokens and scanning `reviews/` (FP risk). Deferred: `--json` mode.
