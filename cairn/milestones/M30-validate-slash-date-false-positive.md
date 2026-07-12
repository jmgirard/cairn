<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M30: Stop cairn_validate false-flagging R CMD check counts as non-ISO dates

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m30-validate-slash-date   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Tighten `cairn_validate`'s slash-date matcher to require a 4-digit year so R
CMD check count-notation (`0 / 0 / 0`) no longer trips the non-ISO-date check.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Rewrite the `\d{1,4}/\d{1,2}/\d{1,4}` slash branch of `_NON_ISO_DATE`
(`cairn_validate.py:29`) to require a 4-digit year on one end — year-first
(`2026 / 07 / 11`) or year-last (`07 / 11 / 2026`). Update the "conservative by
design" comment to state the requirement and the accepted miss. Add a test
proving count-triples pass while real slash dates still fail. Record a D-entry
for the tightening and the accepted 2-digit-year miss, and append a follow-up
LESSONS line retiring the M21 slash-form workaround. Absorbs candidate G-C2.

**Out:** Month/day range validation of matched triples (e.g. rejecting
`50 / 3 / 2000`) — dropped at the plan gate as over-engineering; the 4-digit-year
rule alone kills every realistic false positive. Catching 2-digit-year slash
dates (`07 / 11 / 26`) — deliberately not caught (structurally indistinguishable
from a count-triple; zero such dates exist in the repo). The G-C4 backlog /
ROADMAP-cap candidate stays a candidate — unrelated.

**Note on examples:** slash tokens in this file are written *spaced*
(`0 / 0 / 0`, `2026 / 07 / 11`) so the still-unfixed scanner doesn't flag the
plan itself (M21 convention). The behavior under test is the **unspaced** form
of each (no spaces around the slashes); `scripts/tests/test_scripts.py` lives
outside `cairn/`, is not date-scanned, and uses the unspaced literals verbatim.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — R CMD check count-notation passes the date scan: `0 / 0 / 0` and
      `0 / 1 / 2` on a line in a tracked milestone/tracking file yield exit 0 on
      the `iso date format` check. (behavior under test)
- [ ] AC2 — Real misformatted slash dates are still caught: both `07 / 11 / 2026`
      (year-last) and `2026 / 07 / 11` (year-first) still fail the `iso date
      format` check. (behavior under test)
- [ ] AC3 — No regression on the other branches: the full
      `scripts/tests/test_scripts.py` suite passes (year-last dashed,
      month-name orders, malformed-ISO, and valid-ISO pass-through unchanged).
- [ ] AC4 — `python3 scripts/cairn_validate.py` run in this repo passes clean
      (consistency gate; this plugin's stand-in for `devtools::check()`).
- [ ] AC5 — A `cairn/DECISIONS.md` D-entry records the 4-digit-year tightening
      and the accepted 2-digit-year-slash miss; the code comment at
      `cairn_validate.py:22-25` reflects the new rule.
- [ ] AC6 — A `cairn/LESSONS.md` line notes the scanner now accepts slash-form
      check results, retiring the M21 workaround.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T2
- AC5 → T2, T3
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1 — Add a failing test to the date-scan group in
      `scripts/tests/test_scripts.py` (~line 313): assert `0 / 0 / 0` and `0 / 1 / 2`
      on a tracked-file line pass the scan, and add a year-first `2026 / 07 / 11`
      case to the fail set. Confirm the count-triple case fails against
      current code.
- [ ] T2 — Replace the slash branch in `_NON_ISO_DATE`
      (`cairn_validate.py:29`) with year-first `\d{4}/\d{1,2}/\d{1,2}` OR
      year-last `\d{1,2}/\d{1,2}/\d{4}`; update the conservative-design comment
      (lines 22-25) to state the 4-digit-year requirement and the accepted
      miss. Run the suite to green and `cairn_validate.py` clean.
- [ ] T3 — Append a D-entry to `cairn/DECISIONS.md` recording the tightening
      and the accepted 2-digit-year-slash miss (supersedes the M13
      conservative-design rationale for this branch only).
- [ ] T4 — Append a follow-up line to `cairn/LESSONS.md` noting the scanner now
      accepts slash-form R CMD check results, retiring the M21 workaround.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (absorbs candidate G-C2).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
