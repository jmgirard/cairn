# Milestone 16: Lessons loop (capture → harvest)

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m16-lessons-loop   <!-- PR URL once opened -->

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

- [ ] (implement gate) Decide the lessons home; create it / define the
      section; update `tracking-rules.md` file-map + weight-caps.
- [ ] Add the capture step to `skills/milestone-review/SKILL.md` (and/or
      implement completion).
- [ ] Add the harvest step to `skills/milestone-plan/SKILL.md`.
- [ ] If a new file: extend `cairn_scripts.LINE_CAPS` + confirm
      `cairn_validate` caps it; add a fixture case to `scripts/tests/`.
- [ ] Add the lock test; run all suites + `cairn_validate`.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: /milestone-implement start; branch m16-lessons-loop cut from main; status → in-progress.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
