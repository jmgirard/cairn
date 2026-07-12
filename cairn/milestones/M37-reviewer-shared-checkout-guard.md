<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M37: Fence cairn subagents off the shared checkout (ref-based git only)

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m37-shared-checkout-guard   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Stop any cairn-spawned subagent from moving the shared primary checkout's HEAD
by mandating ref-based git, closing the M36-review disruption.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A general subagent-conduct rule in `tracking-rules.md` — subagents cairn
spawns share the primary checkout, so they use ref-based git only
(`git diff`/`show`/`log`/`blame` against refs) and never a HEAD-moving command
(`git checkout`/`switch`/`worktree add`/`reset`) in that tree. A pointed
one-line reminder at the `/milestone-review` fan-out step (step 5), where the
disruption bit in the M36 review. A guard in `test_review_fanout.py` locking
both wordings.

**Out:** Worktree-isolation spawn flags (rejected at the plan gate as
non-portable and unlockable by a prose guard → not pursued; the prose rule is
the fix). Any runtime enforcement — these are skill-text mechanics, locked only
by the prose guard, like the rest of the fan-out.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/shared/tracking-rules.md` states a general rule that
      cairn-spawned subagents sharing the primary checkout use ref-based git
      only and names the prohibited HEAD-moving commands (at least
      `git checkout` and `git worktree add`). Evidence: the rule text present +
      the AC3 guard asserts it.
- [ ] AC2 — `skills/milestone-review/SKILL.md` step 5 (the reviewer fan-out)
      carries a pointed reminder that reviewers use ref-based git only, no
      checkout/worktree in the shared tree. Evidence: the text present + the
      AC3 guard asserts it.
- [ ] AC3 — `skills/tests/test_review_fanout.py` gains a guard (or guards)
      locking the AC1 and AC2 wording — single-line-anchored and
      case-insensitive per the M23/M26 prose-guard lessons — and
      `python3 -m unittest discover -s skills/tests` plus
      `python3 scripts/cairn_validate.py` both pass. Evidence: command output.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1 — Add the general subagent-conduct rule to
      `skills/shared/tracking-rules.md`, adjacent to the subagent-orchestration
      bullets (~L375–391): a subagent sharing the primary checkout uses
      ref-based git (`diff`/`show`/`log`/`blame`) and never a HEAD-moving
      command (`checkout`/`switch`/`worktree add`/`reset`). Keep the wording on
      single lines the guard can anchor to.
- [ ] T2 — Add a pointed one-line reminder to the step-5 reviewer spawn in
      `skills/milestone-review/SKILL.md`: reviewers use ref-based git only, no
      `git checkout`/`worktree add` in the shared tree. Anchor the sentinel
      inside any bold, not split across `**` (M26).
- [ ] T3 — Add the guard(s) to `skills/tests/test_review_fanout.py` locking the
      T1 and T2 wording (single-line `assertIn`/`assertRegex`, case-insensitive;
      heed M23 newline + M26 bold-split lessons); run
      `python3 -m unittest discover -s skills/tests` and
      `python3 scripts/cairn_validate.py` to green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan. Absorbs the ROADMAP candidate added
  2026-07-12 from the M36 review; scope generalized from the review fan-out to
  all shared-tree subagents at the plan gate.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
