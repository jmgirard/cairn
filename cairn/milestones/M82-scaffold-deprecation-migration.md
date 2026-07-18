<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M82: Scaffold-deprecation migration — repair mode acts on the advisory it inherits

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3, IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m82-scaffold-deprecation-migration` · https://github.com/jmgirard/cairn/pull/80   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give `/cairn-init` repair mode a section of its own and a step that performs
the scaffold rename `cairn_validate`'s `scaffold deprecations` advisory names,
so an adopting repo stops carrying that WARN until a maintainer acts by hand.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a new `## 3. Repair` section in `skills/cairn-init/SKILL.md` carrying
the repair substance §0 currently states inline, plus a deprecation-migration
step driven by the advisory's own output — so a future `DEPRECATED_GITIGNORE`
entry is migrated without editing the skill. The `.gitignore` rewrite is
mechanical; the shelf-directory move is gated on an explicit user ask (the
shelf is gitignored, so its contents are untracked and a move is unrecoverable
by git), and a repo where both directories exist is surfaced, never clobbered.
Prose-guards for the new rules, registered in the mutation harness.

**Out:** closing the deprecation window into a hard FAIL — D-047's severity
reasoning (the rename is cairn's, not the repo's) is unchanged by a migrator
existing; D-047's own "supersede here" hook is the route if it ever changes.
Renumbering the existing `§1`/`§2` sections → not done: Repair lands as `§3`
so the identifiers `migration-protocol.md` and two test docstrings cite stay
stable. A mutating `scripts/` helper → refused outright; `scripts/` report and
never fix, so the actor is skill prose. Migrating a repo's *committed*
`references/` pages → nothing about page content changes here.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] `skills/cairn-init/SKILL.md` carries a `## 3. Repair` section; §0's
      "Already on cairn" bullet is a pointer to it, and the section carries the
      scaffold-piece repair and `PROFILE.md` backfill substance §0 states today.
- [x] The migration step names the emitting script and the advisory's label
      verbatim in backticks (`scaffold deprecations`), so a reader can run the
      check the step consumes.
- [x] The step is written against the advisory's output rather than a
      hardcoded `pdf/`→`sources/` pair; prose states that generality, and a
      guard fails if it is narrowed to the one rename.
- [x] Three actions are pinned to their rules: the `.gitignore` successor
      entry is added without asking, and the superseded one removed only once
      the old directory is gone; the directory move happens only after an
      explicit user ask; both-directories-exist is surfaced and never
      clobbered — and the case that governs is chosen before any move, not
      after. Each guard pins the action label together with its rule on one
      physical line (M74/M76).
- [x] The step closes by re-running the check and states what a quiet advisory
      does and does not prove: `check_gitignore_deprecations` reads
      `.gitignore` alone, so repair reports the directory outcome — moved,
      declined, or awaiting a choice — separately, never inferred from the
      check going quiet.
- [x] A prose-guard file covering the above registers in
      `skills/tests/test_mutation_harness.py` and fails when its registered
      block is blanked.
- [x] Both suites green from the repo root, exit codes checked separately:
      `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s skills/tests` (profile `verify` slot).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T4
- AC2 → T2, T4
- AC3 → T2, T4
- AC4 → T2, T4
- AC5 → T2, T4
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Add `## 3. Repair` to `skills/cairn-init/SKILL.md` after §2; move the
      repair substance out of §0's bullet ([SKILL.md:79-87](skills/cairn-init/SKILL.md:79))
      leaving a one-line pointer in its place, matching how §0 dispatches to
      §1 and §2 today.
- [x] T2: Write the deprecation-migration step inside §3: run
      `cairn_validate.py`, read each `scaffold deprecations` line
      ([cairn_validate.py:651](scripts/cairn_validate.py:651)), rewrite the
      `.gitignore` entry, ask before moving the shelf directory, surface the
      both-exist case, re-run to confirm quiet.
- [x] T3: Sweep the repo for prose asserting cairn-init's section inventory
      that a third section makes stale — whole-repo `git grep`, excluding only
      history (`DECISIONS.md`, `milestones/archive/`, `reviews/archive/`,
      `legacy/`) per M58; fix live hits.
- [x] T4: New prose-guard `skills/tests/test_scaffold_migration.py` locking
      AC1–AC5; register it in the mutation harness (per file, ≥1 exemplar
      block on one unwrapped physical line — M53/M54).
- [x] T5: Run both suites from the repo root, checking each exit code
      explicitly — never piped through `tail` (M56/M65).
- [x] T6 (review send-back, F1/84): keep the shelf covered at every moment —
      *add* the new `.gitignore` entry and remove the old one only once the old
      directory is gone, so a declined move never un-ignores it
      (`test_both_entries_present_is_silent` shows both-present is already
      silent). Scope §3's commit bullet so a repair commit can never sweep an
      un-migrated shelf.
- [x] T7 (review send-back, F3/62 — actioned per M73): re-shape §3's steps 2–4
      from a numbered sequence into explicit mutually-exclusive cases, so the
      both-present clobber check is reached *before* any move, not after.
- [x] T8 (review send-back, F2/92): AC5 needs a gated amendment at implement
      step 6 — `check_gitignore_deprecations` reads only `.gitignore` and can
      never distinguish a verified migration from an attempted one, so either
      the closing check becomes a filesystem check or the criterion drops the
      "verified outcome" claim. Delete the false sentence at `SKILL.md:231-232`
      either way.
- [x] T9 (review send-back, F5/58 + F6/62, cheap while in there): anchor the
      advisory-label assert to the instruction that consumes it, and register
      the AC5 closing block and AC1 pointer line in the mutation harness.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: T1+T2 — `## 3. Repair` added to cairn-init; §0's repair bullet reduced to a pointer; migration step written against the `scaffold deprecations` advisory output (generic over the plugin's superseded-entry map, no rename named in the prose).
- 2026-07-18: T3 — whole-repo sweep (history excluded per M58) found no prose asserting cairn-init's section inventory; nothing to fix. `§1`/`§2` citations in `migration-protocol.md` and two test docstrings stay correct, as the milestone-local decision intended.
- 2026-07-18: T4 — `skills/tests/test_scaffold_migration.py` (10 tests) + 4 mutation entries; two asserts initially hit the M23 wrapped-phrase trap and were re-anchored to single physical lines. Entries proven live: pointing one block at absent text errors the harness, exit 1.
- 2026-07-18: T5 — verify clean from repo root, exit codes checked separately: scripts 147 OK (exit 0), skills 353 OK (exit 0), `cairn_validate` exit 0. Status → review.
- 2026-07-18: review in progress — draft PR #80 opened; AC1–AC7 evidence gathered; consistency gate clean; blame-history lens reported zero findings; diff-bug + prior-PR lenses still running. Checkpoint only, gate not yet reached.
- 2026-07-18: review gate FAILED — AC4 (both-present clobber protection unreachable in the mandated step order, F3) and AC5 (the named check cannot distinguish a verified migration from an attempted one, F2) fail as written; F1 (declined move un-ignores a copyright-sensitive shelf) actioned alongside. Status → in-progress; T6–T9 added; PR #80 stays draft, unmerged. First trip back (thrash rule: 1 of 3).
- 2026-07-18: T6+T7 — §3's migration step restructured: the successor `.gitignore` entry is now ADDED (old one retained), the four numbered steps became three mutually-exclusive on-disk cases chosen before any move (clobber case first in reading order), and `<old>` is removed only once its directory is gone. Verified F1/F3's premise in code: `check_gitignore_deprecations` (`cairn_validate.py:663`) fires only when `old in gitignore and new not in gitignore`, so both-present is genuinely silent and the shelf stays covered throughout. §3's commit bullet now mandates staging by path, never `git add -A`.
- 2026-07-18: T8 — AC4 + AC5 amended via the step-6 gate (fork chosen by the user at the plan-gate: drop the verified-outcome claim, keep `scripts/` report-only per Scope's Out). AC5 now requires the prose to state what a quiet advisory does NOT prove; the false sentence "a still-firing advisory means a step above was declined or failed" is deleted and an `assertNotIn` guards its return.
- 2026-07-18: T9 — advisory-label assert re-anchored to the one instruction consuming it (script + label fused on a single physical line, M80 shape); mutation registry grew 4 → 8 `test_scaffold_migration` entries, adding the removal rule, the case-exclusivity block, the AC5 closing paragraph, the commit-scoping rule, and AC1's §0 pointer.
- 2026-07-18: verify clean from repo root, exit codes checked separately (never piped — M56/M65): skills 356 OK (exit 0), scripts 147 OK (exit 0). Mutation entries proven live: pointing the new removal-rule block at absent text errors the harness `found 0`, exit 1; reverted. One authoring slip caught by the suite — reflowing the move case wrapped the guarded phrase `via AskUserQuestion before moving anything` (M23/M78 trap, third recurrence); fixed in the prose, not by loosening the assert. Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- 2026-07-18 (plan): Repair lands as `§3`, not `§2`. Inserting it before the
  migration protocol would renumber a section identifier cited from
  `skills/shared/migration-protocol.md` (title + body) and two test docstrings;
  §0 is a dispatch table, not a narrative, so forward-pointing costs nothing
  while renumbering buys a sweep M48/M58 say is where things get missed.

## Review

**Outcome: gate FAILED 2026-07-18 — returned to `in-progress`.** AC4 and AC5
fail as written; PR #80 left open as draft, not merged.

**Evidence per criterion** (fresh, by command, on `m82-…` @ 8b8d1c7):

- AC1 ✓ — `## 3. Repair` at `SKILL.md:186`; §0 reduced to the pointer at `:79`;
  moved block at `:192-200` diffs identical to `main`'s `:79-87` except the
  bold lead-in.
- AC2 ✓ — `${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py` at `:210`,
  `` `scaffold deprecations` `` at `:211`; label matches the emitted string at
  `cairn_validate.py:664` verbatim.
- AC3 ✓ — generality sentence at `:213`; `references/pdf` occurs **0 times** in
  the skill (grep -c), so no rename is named in the prose.
- AC4 ✗ — the three labels are pinned (`:216`, `:219`, `:223`) and guarded, but
  the third rule is **unreachable in the mandated execution order** (F3): steps
  2–4 are mutually-exclusive directory states presented under "Per line, in
  order", so the move in step 2 precedes step 3's clobber protection.
- AC5 ✗ — the step re-runs the check (`:229-232`), but
  `check_gitignore_deprecations` reads only `.gitignore` content and never the
  filesystem, so step 1 alone silences the advisory (F2). "Verified outcome
  rather than an attempted one" is not deliverable by the named mechanism, and
  the shipped sentence "a still-firing advisory means a step above was declined
  or failed" is false.
- AC6 ✓ — 4 `test_scaffold_migration` entries registered; harness and
  completeness meta-test both exit 0; pointing a block at absent text errors
  the harness (exit 1), proving the entries live.
- AC7 ✓ — from repo root, exit codes checked separately: scripts 147 OK (0),
  skills 353 OK (0), `cairn_validate` 15 PASS (0).

**Consistency gate:** `cairn_validate` exit 0. Generic profile's
`consistency-gate` slot names no toolchain checks → universal half only.
DESIGN untouched, so `cairn_impact` correctly skipped. No CI on this repo (M16).

**Fan-out:** [O] diff-bug 6 findings · [S] blame-history 0 · [S] prior-PR 0
(this repo records review findings in archives, not GitHub PR comments; the
`gh api` comment endpoints were empty across all 12 relevant PRs).

**Actioned (≥80, plus one sub-threshold by M73):**

- F1 (84) — step 1's unconditional `.gitignore` rewrite un-ignores the old
  shelf while its untracked contents remain; §3's own commit bullet then
  follows with no `git add` scoping, so a declined move can publish files
  `references/llm-wiki.md:113` records as gitignored out of copyright
  necessity. `check_references` skips both shelf names, so no check catches it.
- F2 (92) — the closing re-run cannot distinguish verified from attempted; the
  prose states a falsehood. Drives the AC5 failure.
- F3 (62, actioned anyway) — sub-80 but authorizes an irreversible action
  (`mv` over untracked files git cannot restore), the exact class M73's lesson
  says to fix regardless of score. Drives the AC4 failure.

**Logged, not actioned (<80):**

- F4 (28) — "fix what's missing" → "create what is missing" leaves a damaged
  (present-but-corrupt) piece with no remedy, against `SKILL.md:10-11`'s
  "missing or damaged" promise. Pre-existing: the original §0 wording covered
  only the missing case too, so this diff is lateral, not a regression.
- F5 (58) — the advisory-label assert is satisfiable by any of three
  occurrences in §3 (`:205`, `:211`, `:230`), so it does not pin the label to
  the instruction that consumes it (M80 shape); not mutation-registered.
- F6 (62) — AC5's closing paragraph and AC1's §0 pointer are independently
  load-bearing but unregistered; the registry comment claims one entry per such
  block. AC6 as literally written is still satisfied (registration is per file).
<!-- owner: review · exclusive -->
