<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M214: Clear the prose-guard reds

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — the hand-run prose-guard suite gates nothing and no adopter runs it   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m214-prose-guard-reds   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The hand-run `skills/tests` suite passes again, with each stale guard repointed to the current prose or deleted.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the suite's 4 failures and 1 error as of 2026-10-04. Two asserts
in `skills/tests/test_default_branch_parameterized.py` (lines 69, 92) and
the Mutation block at `skills/tests/test_mutation_harness.py:305` pin the
`origin` spelling of the default-branch recipe, which the rulebook and
`skills/cairn-init/SKILL.md:85-91` now write as `<base>` (guest mode).
`test_two_way_check_runs_against_the_baseline`
(`skills/tests/test_resume_routing.py:195`) pins a `/hotfix` step-1
passage that gained a guest-arm clause (`skills/hotfix/SKILL.md:67-69`).
`test_partial_coverage_was_trimmed_not_deleted`
(`skills/tests/test_lesson_graduation.py:87`) pins `cairn/LESSONS.md`
lines that later prunes removed.

**Out:** re-gating `skills/tests`, because D-109 stands and the suite stays hand-run.
New guards or harness entries (D-090/D-108 door). The other
`skills/tests` files, which pass today. The ROADMAP hygiene stamp's
suite note, which `/milestone-review` post-merge hygiene rewrites.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: From the repo root, `python3 -m unittest discover -s skills/tests` exits 0 and reports no failures and no errors.
- [ ] AC2: The branch removes one test method from `skills/tests`, `test_partial_coverage_was_trimmed_not_deleted`, and no other: `git diff <default-branch>...HEAD -- skills/tests` shows no other removed `def test_` line.
- [ ] AC3: The active profile's `verify` slot is clean: both gating suites, `claude plugin validate`, and `claude plugin test` (`cairn/PROFILE.md`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T2, T3, T4
- AC2 → T3, T4
- AC3 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: In `test_default_branch_parameterized.py`, change the asserted
      `git ls-remote --symref origin HEAD` and
      `git symbolic-ref --short refs/remotes/origin/HEAD` to the `<base>`
      spellings, and change the matching Mutation `block` at
      `test_mutation_harness.py:305` the same way.
- [x] T2: Repoint `test_two_way_check_runs_against_the_baseline` to the
      current `/hotfix` step-1 text: assert the passage before the guest-arm
      parenthetical and the passage after it as two `assertIn` calls, so the
      guest-arm wording is not pinned here.
- [ ] T3: Delete `test_partial_coverage_was_trimmed_not_deleted` from
      `test_lesson_graduation.py`. Leave the file's other tests, including
      the absence assert and its positive control.
- [ ] T4: From the repo root, run `skills/tests` and each `verify` command
      on its own, checking each exit code (no pipe, no `;` chain).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to plan (no work named) — clear the prose-guard reds, deleting or repointing stale guards, not hardening them.
- 2026-10-04: question set: a live look in a new desktop Code session if the work changes the band or pane — yes, at review (this scope does not touch them).
- 2026-10-04: collision check: D-090's Untouched clause keeps repairs to existing apparatus as ordinary work, and D-108 puts removal-shaped work outside the door, so no superseding entry is owed.
- 2026-10-04: collision check: each red traces to an intentional rewording (guest-mode `<base>` recipe, the hotfix guest arm, lesson prunes), so none is a firing of D-109's falsifier.
- 2026-10-04: checker-regress shape: the repairs keep each guard's promise and the deletion narrows it, so the shape does not fire. The user chose repair-or-delete at the gate.
- 2026-10-04: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-04: lessons harvested: run each suite from the root with exit codes checked (M56 line). Quote `====` in zsh (M133). A guard pinning prunable LESSONS lines breaks on prunes (M165).
- 2026-10-04: criteria audit (reduced mode, fresh Opus reader): no findings on AC1-AC3.
- 2026-10-04: plan gate chose repointing the default-branch guards over deleting them because their subject, the recipe in the rulebook and `/cairn-init`, still ships; falsified by the guards going red again on the next intentional rewording of the recipe.
- 2026-10-04: plan gate chose deleting the lesson-trim assert over re-anchoring it to a surviving lesson line because LESSONS lines are prunable by rule and any anchor breaks at the next prune; falsified by a graduated family reappearing in LESSONS that only this assert catches.
- 2026-10-04: plan commit merged the M212 and M213 band-button candidate rows into one to keep ROADMAP under its 60-line and 24,000-byte caps.
- 2026-10-04: implement start: branch m214-prose-guard-reds cut from main at 854c2c6. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's work and stay unstaged.
- 2026-10-04: T1 done: the two asserts and the Mutation block now read `<base>`. skills/tests went from 4 failures and 1 error to 2 failures. Verify slot: all four commands exit 0.
- 2026-10-04: T2 done: the guard asserts the text up to `pull ff-only` and the text from `), and in a throwaway worktree` on. The existing Mutation entry covers the second passage. An in-memory edit that drops `ff-only` turns the first passage false. Only test files changed, so the verify slot result from T1 stands.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
