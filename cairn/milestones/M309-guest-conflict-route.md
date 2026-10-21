# M309: Route a handed-off PR with merge conflicts to a sync

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/milestone` reports and routes for open PRs
- **Branch/PR:** —

## Goal

`/milestone` finds a handed-off PR that no longer merges cleanly and routes it to a sync.

## Scope

**In:** `/milestone` §2 reads `mergeable` for a guest-mode `blocked` milestone's PR and for open hotfix PRs. A
`CONFLICTING` handoff routes to `/milestone-implement`, whose resume gate accepts it and whose guest sync resolves the
rebase conflicts. The trigger is modelbased #696 and #697: four parallel PRs edited `NEWS.md` and
`tests/testthat/test-ordinal.R`, and a maintainer asked twice for the conflicts to be resolved.

**Out:** A warning on the number of open PRs, which the user declined at the question set. A route for a conflicted
hotfix PR, which is reported only; `/hotfix` with the PR reference already resumes it.

## Acceptance criteria

- [ ] AC1: In `skills/milestone/SKILL.md` §2, the read for a guest-mode `blocked` milestone whose header names a PR
      adds `mergeable` to its `--json` fields. An `OPEN` PR that no earlier arm routes takes two new arms:
      `CONFLICTING` routes to `/milestone-implement M<NNN>`, and `UNKNOWN` is reported with no route.
- [ ] AC2: The "Open hotfix PRs" bullet adds `mergeable` to its read and reports a `CONFLICTING` PR as having merge
      conflicts.
- [ ] AC3: `skills/milestone-implement/SKILL.md` step 1 names a `CONFLICTING` route from `/milestone` as a reason that a
      `blocked` guest milestone resumes for step 2's guest sync.
- [ ] AC4: `skills/milestone-implement/SKILL.md` step 2's guest sync says what happens when the rebase stops on
      conflicts. The session resolves them and runs the `verify` slot before the re-push. If it cannot resolve them,
      it stops with a close block that names the conflicted files.
- [ ] AC5: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3

## Tasks

- [ ] T1: Edit `skills/milestone/SKILL.md` §2: the guest `blocked` bullet (near line 176) and the "Open hotfix PRs"
      bullet (near line 199), for AC1 and AC2.
- [ ] T2: Edit `skills/milestone-implement/SKILL.md` step 1 (near line 35) and step 2's guest sync (near line 94),
      for AC3 and AC4.
- [ ] T3: Check whether README.md or the cairn pane restates the §2 guest routes, and update any stale text. Run the
      five `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a new route in the status audit and implement's resume gate.
- 2026-10-21: idea vet: no concern.
- 2026-10-21: question set: merge conflicts — route conflicts, no warning on PR volume.
- 2026-10-21: criteria audit (full, fresh Opus reader): for M309, ordered the new arms after the existing ones (AC1); moved the resume rule to step 1 and dropped a false premise (AC3); added the conflicted-rebase criterion (AC4); dropped the prose-guard criterion per D-109; cited the verify slot in full.
- 2026-10-21: collision check: no D-entry or archived milestone covers merge state; D-137 and D-173 stand.

## Decisions

## Review
