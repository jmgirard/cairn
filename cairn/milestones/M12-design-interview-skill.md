# M12: Design-interview skill (facts → principles)

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —
- **Branch/PR:** m12-design-interview-skill   <!-- PR URL once opened -->

## Goal

Ship a standalone `/design-interview` skill that runs the two-phase
(facts → principles) DESIGN-elicitation interview, gated by a live openac
pilot.

## Scope

**In:** A new `skills/design-interview/SKILL.md` encoding the gold-standard
interview from `references/design-interview-notes.md` (items 1–11):

- **Phase 1 (Facts):** elicit what can't be inferred from the repo;
  chain each round on prior answers; ground every option in repo evidence
  (files, Imports, git history); ask the wart question; **bank**
  proto-principles in a running ledger — never classify in phase 1.
- **Seam:** summarize what was heard, write the DESIGN draft +
  banked-candidates ledger to disk, checkpoint-commit, and offer a routing
  chip (continue into principles / pause). Continuous by default, pausable
  without loss.
- **Phase 2 (Principles):** propose banked + domain-derived + git-mined
  candidates, each pre-classified (IP/GP/skip) with a marked recommendation;
  stress-test the full set for collisions with phase-1 decisions; write
  principles to DESIGN.md respecting IP-block-first ordering and
  never-reuse numbering.
- Runs entirely on Opus in the main session (the cheap lever).
- Wiring: cairn-init's DESIGN-fill step keeps its quick honest lines and
  adds a routing chip into `/design-interview`; skill registered in
  `SKILLS_WITH_PHASE_HEADER`; DESIGN.md skill count `× 8` → `× 9`;
  DECISIONS.md D-entry for the standalone-skill choice.

Model tier (amended 2026-07-11, D-014): the openac pilot found Opus's
questions too technical; Fable was markedly better. The skill now recommends
running the session on Fable (soft steer, user's per-instance choice). This
absorbs the former "phase-2-to-Fable elevation" candidate (dropped).

**Out:**
- Greenfield init opener-questions + toolchain-profile selection → stays
  the separate `Greenfield init flow` candidate (cross-referenced).
- A hard model gate, or any cairn-spawned Fable subagent (D-004 stands) —
  the steer is a soft recommendation only.
- Any change to how the milestone skills write DESIGN.md, or auto-triggered
  DESIGN edits without the interview.

## Acceptance criteria

- [ ] `skills/design-interview/SKILL.md` exists, reads the shared rulebook
      first, and carries the phase-header directive
      `# Design interview` → `## Facts` / `## Principles`; the two phases
      and the checkpoint seam (write-to-disk + commit + routing chip) are
      all specified in the prose. (evidence: file + guard test)
- [ ] Phase 1 prose instructs all of: elicit-don't-classify,
      chain-on-prior-answers, repo-evidence-grounded options, the wart
      question, and banking proto-principles into a running ledger
      (notes items 1–5). (evidence: guard test)
- [ ] Phase 2 prose instructs: candidates arrive pre-classified
      (IP/GP/skip) each with a marked recommendation, drawn from banked +
      domain-derived + git-mined sources, stress-tested against phase-1
      decisions, and written to DESIGN.md with IP-block-first + never-reuse
      numbering (notes items 6–11). (evidence: guard test)
- [ ] Registration complete: `SKILLS_WITH_PHASE_HEADER` in
      `test_phase_header_levels.py` includes `design-interview` and that
      test passes; DESIGN.md architecture line reads `× 9`; cairn-init's
      DESIGN-fill step routes to `/design-interview`. (evidence: unittest
      suite green + grep)
- [ ] New guard test `skills/tests/test_design_interview.py` locks the
      invariants in the three criteria above and passes.
      (evidence: `python3 -m unittest discover -s skills/tests` green)
- [ ] **Merge gate:** `/design-interview` run end-to-end on openac; Jeff
      judges the produced DESIGN draft + principle set acceptable and
      records a one-line verdict. (evidence: pilot verdict in Review)
      → **Met on Fable** 2026-07-11: Opus rejected (questions too technical);
      Fable rerun "a much better experience" → skill now Fable-recommended
      (D-014).
- [ ] Skill recommends running on Fable at the top (soft steer, D-014).
      (evidence: `test_recommends_running_on_fable` green)

## Tasks

- [x] Draft `skills/design-interview/SKILL.md`: front-matter (trigger-tuned
      description), phase-header directive, Phase 1 (Facts) with items 1–5 +
      banking ledger, the seam (checkpoint-commit + routing chip), Phase 2
      (Principles) with items 6–11 + DESIGN-write rules.
- [x] Wire cairn-init: DESIGN-fill step keeps quick lines, adds a routing
      chip to `/design-interview` (SKILL.md §1 + its routing chip).
- [x] Bump DESIGN.md skill count `× 8` → `× 9` + one architecture line;
      add D-013 (standalone `/design-interview`) to DECISIONS.md.
- [x] Add `design-interview` to `SKILLS_WITH_PHASE_HEADER`
      (`test_phase_header_levels.py:26`); write
      `skills/tests/test_design_interview.py`; run the suite green.
- [x] Live pilot on openac (Jeff-run); record the verdict. Done 2026-07-11:
      Opus poor, Fable much better → skill defaults to Fable (D-014).
- [x] Amendment (D-014): add the Fable recommendation to the skill top +
      guard test; supersede D-013's Opus-only v1; drop the elevation candidate.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (promoted from the design-interview
  candidate; lineage references/design-interview-notes.md).
- 2026-07-11: set in-progress; branch m12-design-interview-skill cut.
- 2026-07-11: drafted skills/design-interview/SKILL.md (two phases + seam,
  notes items 1–11) [task 1].
- 2026-07-11: wired cairn-init DESIGN-fill + routing chip to /design-interview;
  added phase-header mapping to tracking-rules [task 2].
- 2026-07-11: DESIGN skill count ×8→×9; DECISIONS D-013 (standalone skill)
  [task 3].
- 2026-07-11: registered skill in phase-header guard; added
  test_design_interview.py (10 assertions); suite green 16/16 [task 4].
- 2026-07-11: build complete (tasks 1–4), local checks green → status
  review. Criterion 6 (openac pilot) is the outstanding Jeff-run merge gate,
  verified at /milestone-review.
- 2026-07-11: openac pilot — Opus questions too technical/hard to parse;
  Fable rerun much better. Reopened in-progress; amended to Fable-recommended
  (D-014, supersedes D-013's Opus-only); elevation candidate dropped. Suite
  re-run green → back to review.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Ship as a standalone `/design-interview` skill (not folded into
  cairn-init): reusable to deepen an existing DESIGN, keeps cairn-init lean.
  Promote to D-013 in the implementation commit that adds the skill.
- Opus-only for v1 — **superseded 2026-07-11 by D-014** after the openac
  pilot: the skill now recommends running on Fable (soft steer). The former
  phase-2-elevation candidate is absorbed and dropped.

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
