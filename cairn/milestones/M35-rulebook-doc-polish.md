<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M35: Rulebook & doc-wording polish batch

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m35-rulebook-doc-polish

## Goal

Apply five deferred doc/wording tweaks to `tracking-rules.md`, each locked
by a prose-guard so it can't silently drift.

## Scope

**In:** five self-contained wording additions and their prose-guards —
(1) a mature-backlog migration remedy in the weight-caps section;
(2) a cap of 3 on prioritized clarification markers at question gates;
(3) a reading-list instruction for Explore subagents; (4) stating the *why*
of different-model review in the fan-out; (5) an output-discipline rule that
copy-run commands go in their own fenced code block, not inline backticks.

**Out:** the `/cairn-init` §2 migration protocol wording (owned by
`test_migration_guidance.py`, a *different* migration concern — DESIGN
disposition and reference sweep, not the ROADMAP-cap backlog remedy here) —
unchanged; at most a one-line pointer from there to the new weight-caps
remedy. Any behavioral/script change (this milestone is prose + guards
only). The M06 "minor steals" bundle and the two dropped marginal candidates
(read_when frontmatter, baseline-commit capture) → not in scope.

## Acceptance criteria

- [ ] `tracking-rules.md` weight-caps remedies include the mature-backlog
      remedy: cluster related backlog into grouped candidate rows pointing at
      the entombed legacy ROADMAP (the M21 circumplex-pilot G-C4 case where a
      large parking-lot blows the <60-line ROADMAP cap one-row-per-item).
- [ ] The "Question gates and routing chips" rule caps prioritized
      clarification markers at 3 at a question gate.
- [ ] The "Model and agent strategy" section instructs giving Explore
      subagents a reading list (which files/areas to read) in their spec.
- [ ] The review fan-out text states *why* review uses a different/fresh
      model — independent judgment catches diff-blindness the author shares.
- [ ] "Output & interaction discipline" requires that runnable commands the
      user is meant to copy-run appear in their own fenced code block, not
      inline backticks.
- [ ] Each of the five tweaks is locked by a prose-guard assertion, and the
      skills test suite passes: `python3 -m unittest discover -s skills/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T6
- AC2 → T2, T6
- AC3 → T3, T6
- AC4 → T4, T6
- AC5 → T5, T6
- AC6 → T6

## Tasks

- [x] T1 — Add the mature-backlog clustering remedy to the weight-caps
      "Remedies when a cap is hit" list in `tracking-rules.md` (over-cap
      ROADMAP branch); add at most a one-line pointer from the `/cairn-init`
      §2 migration section without altering its M23-guarded wording.
- [x] T2 — Add the cap-at-3 clause for prioritized clarification markers to
      the "Question gates and routing chips" section.
- [x] T3 — Add the Explore-subagent reading-list instruction to the "Model
      and agent strategy" section (Sonnet-subagents / Explore guidance).
- [x] T4 — Add the *why* of different-model review to the review fan-out
      bullet in "Model and agent strategy".
- [x] T5 — Add the copy-run-commands-in-a-fenced-block rule to "Output &
      interaction discipline".
- [ ] T6 — Lock all five: extend `test_gate_wording.py` (AC2) and
      `test_review_fanout.py` (AC4) where topical; add a new
      `test_rulebook_polish.py` for AC1/AC3/AC5 (filename avoids the taken
      `test_migration_guidance.py`). Anchor every asserted phrase on a single
      source line (M23) and keep sentinels out of `**bold**` splits (M26).
      Run `python3 -m unittest discover -s skills/tests`.

## Work log

- 2026-07-12: created by /milestone-plan (backlog-polish set 2 of 2).
- 2026-07-12: T1 — mature-backlog clustering remedy added to weight-caps; one-line pointer added in cairn-init §2 step 5 (M23-guarded wording untouched).
- 2026-07-12: T2 — cap-at-3 prioritized-clarification-markers clause added to "Question gates and routing chips".
- 2026-07-12: T3 — Explore reading-list instruction added to the Sonnet-subagents bullet in "Model and agent strategy".
- 2026-07-12: T4 — why-fresh-model rationale (diff-blindness) prepended to the review fan-out bullet.
- 2026-07-12: T5 — copy-run-commands-in-own-fenced-block rule added to "Output & interaction discipline".

## Decisions
<!-- owner: implement / review · append-only -->

## Review
<!-- owner: review · exclusive -->
