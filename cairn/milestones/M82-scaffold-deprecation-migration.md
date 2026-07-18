<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M82: Scaffold-deprecation migration — repair mode acts on the advisory it inherits

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3, IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m82-scaffold-deprecation-migration`   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] `skills/cairn-init/SKILL.md` carries a `## 3. Repair` section; §0's
      "Already on cairn" bullet is a pointer to it, and the section carries the
      scaffold-piece repair and `PROFILE.md` backfill substance §0 states today.
- [ ] The migration step names the emitting script and the advisory's label
      verbatim in backticks (`scaffold deprecations`), so a reader can run the
      check the step consumes.
- [ ] The step is written against the advisory's output rather than a
      hardcoded `pdf/`→`sources/` pair; prose states that generality, and a
      guard fails if it is narrowed to the one rename.
- [ ] Three actions are pinned to their rules: the `.gitignore` entry is
      rewritten without asking; the directory move happens only after an
      explicit user ask; both-directories-exist is surfaced and never
      clobbered. Each guard pins the action label together with its rule on
      one physical line (M74/M76).
- [ ] The step closes by re-running the check and confirming the advisory is
      quiet, so repair reports a verified outcome rather than an attempted one.
- [ ] A prose-guard file covering the above registers in
      `skills/tests/test_mutation_harness.py` and fails when its registered
      block is blanked.
- [ ] Both suites green from the repo root, exit codes checked separately:
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
- [ ] T5: Run both suites from the repo root, checking each exit code
      explicitly — never piped through `tail` (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: T1+T2 — `## 3. Repair` added to cairn-init; §0's repair bullet reduced to a pointer; migration step written against the `scaffold deprecations` advisory output (generic over the plugin's superseded-entry map, no rename named in the prose).
- 2026-07-18: T3 — whole-repo sweep (history excluded per M58) found no prose asserting cairn-init's section inventory; nothing to fix. `§1`/`§2` citations in `migration-protocol.md` and two test docstrings stay correct, as the milestone-local decision intended.
- 2026-07-18: T4 — `skills/tests/test_scaffold_migration.py` (10 tests) + 4 mutation entries; two asserts initially hit the M23 wrapped-phrase trap and were re-anchored to single physical lines. Entries proven live: pointing one block at absent text errors the harness, exit 1.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- 2026-07-18 (plan): Repair lands as `§3`, not `§2`. Inserting it before the
  migration protocol would renumber a section identifier cited from
  `skills/shared/migration-protocol.md` (title + body) and two test docstrings;
  §0 is a dispatch table, not a narrative, so forward-pointing costs nothing
  while renumbering buys a sweep M48/M58 say is where things get missed.

## Review
<!-- owner: review · exclusive -->
