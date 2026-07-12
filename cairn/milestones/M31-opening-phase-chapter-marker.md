<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M31: Mark the opening phase — drop the "session start implicit" carve-out

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m31-opening-phase-chapter-marker   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Drop the "session start implicit" carve-out from the chapter-marker mandate so
a session's opening phase marks a chapter and is navigable in the Claude Code TOC.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Reword the Chapter-markers rule in `skills/shared/tracking-rules.md`
(lines ~343-348) to remove `(session start is implicit)` and state that the
opening phase of a session marks a chapter too — there is no auto
session-start chapter node (M27/D-020), so an unmarked opening phase is absent
from the TOC; keep the no-mechanism fallback. Update the one-line
`Chapter markers:` directive in all 9 phase skills to
`...mark a chapter at each phase transition, including the session's opening
phase.` Extend `skills/tests/test_chapter_marker_mandate.py` to lock the new
wording (directive present, carve-out phrase absent, opening-phase inclusion
asserted). Append **D-024** annotating D-021.

**Out:** Live TOC re-verification in Claude Desktop — declined at the plan
gate (prose-guard only; M27 already established markers drive the TOC and
client UI isn't observable agent-side). No change to the H1/H2 phase-header
convention (D-012/D-020 stand). No change to the `NON_REVIEW_CHIP_SKILLS` list
or the routing-chip mandate — untouched.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — All 9 phase skills carry the chapter-marker directive worded to
      include the opening phase, with no "session start implicit" carve-out.
      (guard-tested)
- [ ] AC2 — `tracking-rules.md`'s Chapter-markers rule states the opening phase
      marks a chapter (no auto session-start node, citing M27/D-020) and
      retains the "no chapter mechanism" fallback and "per-phase mandate"
      framing. (guard-tested)
- [ ] AC3 — A `cairn/DECISIONS.md` D-entry (D-024) annotates D-021, records
      removal of the carve-out, and cites M27/D-020 as the basis.
- [ ] AC4 — `skills/tests/test_chapter_marker_mandate.py` passes and asserts the
      carve-out phrase is absent from all 9 skills and tracking-rules; the full
      `skills/tests` suite is green.
- [ ] AC5 — `python3 scripts/cairn_validate.py` passes clean (consistency gate).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T1, T2
- AC3 → T4
- AC4 → T1, T3
- AC5 → T2, T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Extend `skills/tests/test_chapter_marker_mandate.py`: assert neither
      `"session start implicit"` nor `"session start is implicit"` appears in
      any of the 9 skills or in `tracking-rules.md`, and that tracking-rules
      asserts opening-phase inclusion (e.g. contains `"opening phase"`). Run to
      confirm it fails against current files (test-first). Keep asserted tokens
      on one physical line (M23/M26 lesson).
- [ ] T2 — Reword the Chapter-markers rule in `tracking-rules.md` (~343-348):
      drop `(session start is implicit)`, add the opening-phase inclusion +
      the "no auto session-start node (M27/D-020)" rationale, keep
      `per-phase mandate`, `mark a chapter at each phase transition`, and the
      no-mechanism fallback lines intact (guard-asserted).
- [ ] T3 — Update the `Chapter markers:` directive line in all 9 skills
      (milestone-plan, -implement, -review, -brief, hotfix, cairn-init,
      cairn-release, milestone, design-interview) to the new wording. Run the
      guard + full `skills/tests` suite to green.
- [ ] T4 — Append **D-024** to `cairn/DECISIONS.md` annotating D-021: the
      carve-out is removed because M27/D-020 proved there is no auto
      session-start chapter, so the opening phase must mark explicitly.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (from Jeff's observation that this
  session's own opening plan phase produced no TOC node).
- 2026-07-12: T1 — extended test_chapter_marker_mandate.py with
  test_carve_out_phrase_absent_everywhere (9 skills + tracking-rules) and
  test_rulebook_includes_the_opening_phase; confirmed red against current files.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
