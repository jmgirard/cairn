# M34 — Mechanical coverage-map lint in cairn_validate

**Status:** done · approved 2026-07-12 · PR #32

## Goal

Give M18's skill-text AC→Coverage traceability a runtime enforcement arm.

## Outcome

Added `check_coverage_complete` to `scripts/cairn_validate.py` (11th check in
`CHECKS`): for every *live* milestone file it counts `## Acceptance criteria`
checkbox items and fails if any ACk is unreferenced in `## Coverage`, or if a
Coverage line cites an AC beyond the criterion count (dangling ref). Archived
summaries are exempt (scanned via `cs.live_files`, a non-recursive glob). Helper
`_section_body` delimits the H2 sections. Four fixtures via a new `live_cov`
builder; shared `Tree.build()` needed no change (its `live()` bodies have 0
criteria → skipped by construction). Suite 49/49; real repo validate 11/11
(M34+M35 dogfood it). Two fresh-context reviewers: zero findings.

## Decisions

None cross-cutting. Task-existence checking of Coverage refs left out of scope
(stays skill-text/review-fenced per M18) — candidate if wanted.
