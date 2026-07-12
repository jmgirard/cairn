# Milestone 16: Lessons loop (capture → harvest)

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m16-lessons-loop · https://github.com/jmgirard/cairn/pull/14

## Goal

Record what was *learned*, not just what happened: capture durable repo
lessons (build quirks, testing tricks) at milestone end and surface recent
lessons at plan time.

## Scope

**In:** A durable, append-only, capped lessons home in `cairn/`; a capture
step at milestone end (`/milestone-review` post-merge hygiene, or
`/milestone-implement` completion) that appends durable lessons; a harvest
step in `/milestone-plan` that surfaces recent lessons before scoping;
`tracking-rules.md` file-map + weight-caps updated for the home; if a new
file, `cairn_scripts` `LINE_CAPS` + `cairn_validate` cap coverage extended.

**Open (implement gate, not an RB tripwire):** the lessons home —
*recommended* a dedicated `cairn/LESSONS.md` (append-only + capped, like
`DECISIONS.md`) over a per-milestone Lessons section promoted at archive;
decide at implement's question gate.

**Out:** Session-end capture for non-milestone / plain-conversation sessions
(would need a Stop-hook, separate design) → candidate. `read_when`
doc-routing frontmatter for `references/` → candidate row.

## Acceptance criteria

- [ ] A durable lessons home exists with an append-only, capped format
      documented in the `tracking-rules.md` file-map + weight-caps section.
- [ ] `/milestone-review` (or `/milestone-implement` completion) has a step
      that appends durable lessons at milestone end.
- [ ] `/milestone-plan` has a step that surfaces recent lessons at plan time
      (before the question gate).
- [ ] If a new `cairn/` file: `cairn_scripts.LINE_CAPS` includes it and
      `cairn_validate` enforces its cap (fixture proves an over-cap file
      fails).
- [ ] A test locks the lessons-home format/cap; full `skills/tests/` +
      `scripts/tests/` + `cairn_validate` pass.

## Tasks

- [x] (implement gate) Decide the lessons home; create it / define the
      section; update `tracking-rules.md` file-map + weight-caps.
- [x] Add the capture step to `skills/milestone-review/SKILL.md` (and/or
      implement completion).
- [x] Add the harvest step to `skills/milestone-plan/SKILL.md`.
- [x] If a new file: extend `cairn_scripts.LINE_CAPS` + confirm
      `cairn_validate` caps it; add a fixture case to `scripts/tests/`.
- [x] Add the lock test; run all suites + `cairn_validate`.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: /milestone-implement start; branch m16-lessons-loop cut from main; status → in-progress.
- 2026-07-11: gate → dedicated cairn/LESSONS.md, cap 50, capture at /milestone-review post-merge; created LESSONS.md + rulebook file-map/boundary/weight-caps + CLAUDE.md boundary.
- 2026-07-11: added lessons-capture to /milestone-review post-merge hygiene (step 9).
- 2026-07-11: added lessons harvest to /milestone-plan (session-start read + surface-before-gate step 2).
- 2026-07-11: LINE_CAPS += cairn/LESSONS.md:50; date-scan covers LESSONS.md; over-cap fixture in scripts/tests (30 pass).
- 2026-07-11: added skills/tests/test_lessons_loop.py (wiring + stated↔enforced cap lock); skills 27 + scripts 30 pass, cairn_validate exit 0; recorded D-015.
- 2026-07-11: all tasks done; status → review.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Lessons home + capture/harvest loop promoted to **D-015** (cross-cutting:
  new top-level tracking file inherited by every adopting repo).

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

2026-07-11 — PR #14 (draft). Evidence per criterion:

- **AC1 (lessons home + documented):** `cairn/LESSONS.md` exists (12 lines),
  append-only one-line format documented in-file; tracking-rules file-map row
  (L22), weight-caps `< 50 lines` (L70), boundary rule (L28). ✓
- **AC2 (capture step):** `/milestone-review` step 9 post-merge hygiene has
  the "Capture durable lessons" instruction (SKILL.md L114). ✓
- **AC3 (harvest step):** `/milestone-plan` reads LESSONS.md at session start
  (L17) and "Harvest recent lessons (before the gate)" in step 2 (L52). ✓
- **AC4 (cap enforced):** `LINE_CAPS` includes `cairn/LESSONS.md: 50`;
  `test_over_cap_lessons` proves a 55-line file fails weight-caps. ✓
- **AC5 (lock + suites):** `test_lessons_loop.py` (6 tests, incl.
  stated↔enforced cap lock) passes; skills/tests 27, scripts/tests 30,
  `cairn_validate` exit 0. ✓

Consistency gate: `cairn_validate` all checks passed. No DESIGN principle
changed → `cairn_impact` skipped. R gates (devtools/README/pkgdown/NEWS/
.Rbuildignore) waived — plugin repo, not an R package (CLAUDE.md).

Independent Opus review (fresh context): no must-fix defects; all 5 ACs met,
cap semantics correct, lessons↔decisions boundary consistent. Triage of 4
nice-to-haves:
- Wiring locks were substring-only → **fixed**: anchor on step text
  ("Capture durable lessons" / "Harvest recent lessons").
- Date-scan of LESSONS.md was unlocked → **fixed**: added
  `test_non_iso_date_in_lessons` (scripts/tests, now 31).
- Misleading comment in `test_over_cap_lessons` → **fixed** (reworded).
- "50 lines" reads as fail threshold not last-allowed → **rejected**:
  consistent with every other cap's `< N` phrasing (CLAUDE.md `< 80`, etc.).
Post-fix: skills/tests 27, scripts/tests 31, `cairn_validate` exit 0.
