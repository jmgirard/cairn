# M309: Route a handed-off PR with merge conflicts to a sync

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes what `/milestone` reports and routes for open PRs
- **Branch/PR:** m309-guest-conflict-route, https://github.com/jmgirard/cairn/pull/323

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

- [x] AC1: In `skills/milestone/SKILL.md` §2, the read for a guest-mode `blocked` milestone whose header names a PR
      adds `mergeable` to its `--json` fields. An `OPEN` PR that no earlier arm routes takes two new arms:
      `CONFLICTING` routes to `/milestone-implement M<NNN>`, and `UNKNOWN` is reported with no route.
- [x] AC2: The "Open hotfix PRs" bullet adds `mergeable` to its read and reports a `CONFLICTING` PR as having merge
      conflicts.
- [x] AC3: `skills/milestone-implement/SKILL.md` step 1 names a `CONFLICTING` route from `/milestone` as a reason that a
      `blocked` guest milestone resumes for step 2's guest sync.
- [x] AC4: `skills/milestone-implement/SKILL.md` step 2's guest sync says what happens when the rebase stops on
      conflicts. The session resolves them and runs the `verify` slot before the re-push. If it cannot resolve them,
      it stops with a close block that names the conflicted files.
- [x] AC5: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3

## Tasks

- [x] T1: Edit `skills/milestone/SKILL.md` §2: the guest `blocked` bullet (near line 176) and the "Open hotfix PRs"
      bullet (near line 199), for AC1 and AC2.
- [x] T2: Edit `skills/milestone-implement/SKILL.md` step 1 (near line 35) and step 2's guest sync (near line 94),
      for AC3 and AC4.
- [x] T3: Check whether README.md, the cairn pane, or the rulebook restates the §2 guest routes, and update any stale
      text. Add the CHANGELOG entry. Run the five `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a new route in the status audit and implement's resume gate.
- 2026-10-21: idea vet: no concern.
- 2026-10-21: question set: merge conflicts — route conflicts, no warning on PR volume.
- 2026-10-21: criteria audit (full, fresh Opus reader): for M309, ordered the new arms after the existing ones (AC1); moved the resume rule to step 1 and dropped a false premise (AC3); added the conflicted-rebase criterion (AC4); dropped the prose-guard criterion per D-109; cited the verify slot in full.
- 2026-10-21: collision check: no D-entry or archived milestone covers merge state; D-137 and D-173 stand.
- 2026-10-21: implement start: branch m309-guest-conflict-route cut from origin/main at b3573dc0; untracked cairn-probe.log and tsconfig.json are unrelated and stay unstaged.
- 2026-10-21: T1 done: §2's guest `blocked` read adds `mergeable`, with a `CONFLICTING` arm (route to implement) and an `UNKNOWN` arm (report, no route) before `OPEN` otherwise; the hotfix-PR list reads `mergeable` and reports conflicts. Enum values read from GitHub's `MergeableState` schema; modelbased #698 read `CONFLICTING` live. The simple-english hook's file-wide hits are pre-existing house style, left as is. Verify 5/5 green.
- 2026-10-21: T2 done: step 1 names the `CONFLICTING` route as a resume reason; step 2's guest sync resolves a conflicted rebase (here or in the stacked sync), runs verify before the push, and otherwise lists the files with `git diff --name-only --diff-filter=U`, aborts the rebase, and stops. Decided: abort before the stop so the stop leaves no half-done rebase behind. Verify 5/5 green.
- 2026-10-21: minor amendment: T3 adds the rulebook and the CHANGELOG entry (the consistency gate wants one), found while checking restatements.
- 2026-10-21: T3 done: README restates no §2 guest route (its pane table and merge mark already cover `CONFLICTING`, and the pane's lack of a conflict Button is new behavior, not stale text); tracking-rules "Collaboration mode" route list gains the conflict route; CHANGELOG guest entry extended. Verify 5/5 green; cairn_validate all checks passed.
- 2026-10-21: claim audit: 15 claims read, 4 corrected — CHANGELOG.md, skills/milestone/SKILL.md, skills/milestone-implement/SKILL.md, skills/shared/tracking-rules.md; the reader also flagged the stale §2 route list in skills/milestone-review/SKILL.md's guest close label, fixed; all 5 re-read once and hold. Verify 5/5 green.
- 2026-10-21: status → review; handing off to /milestone-review.

## Decisions

## Review

- AC1 evidence (2026-10-21, grep at 6bfd1a2b): skills/milestone/SKILL.md:178-179 reads `--json state,reviewDecision,mergeable`; the `CONFLICTING` arm (195-200) routes to `/milestone-implement M<NNN>` and the `UNKNOWN` arm (200-203) reports with no route. Both sit after the stack-base `CLOSED` arm and before `OPEN` otherwise, and open with "that no arm above takes". PASS.
- AC2 evidence (2026-10-21, grep at 6bfd1a2b): the "Open hotfix PRs" read at skills/milestone/SKILL.md:225 ends its `--json` list with `mergeable`, and 228-229 say "Report a PR whose `mergeable` reads `CONFLICTING` as having merge conflicts." PASS.
- AC3 evidence (2026-10-21, grep at 6bfd1a2b): skills/milestone-implement/SKILL.md:38-40, in step 1, say a `blocked` guest milestone that `/milestone` routed because its PR's `mergeable` reads `CONFLICTING` "resumes for step 2's guest sync". PASS.
- AC4 evidence (2026-10-21, grep at 6bfd1a2b): skills/milestone-implement/SKILL.md:112-120, in step 2's guest sync: a rebase there or in the stacked sync "can stop on conflicts"; the session resolves each file, stages it, runs `git rebase --continue`, and runs `verify` green "before any push"; if it cannot resolve them it lists them with `git diff --name-only --diff-filter=U`, runs `git rebase --abort`, pushes nothing, and stops with a close block naming those files. PASS.
- AC5 evidence (2026-10-21, at 6bfd1a2b): `scripts/tests` 445 OK (21 skipped) exit 0; `hooks/tests` 193 OK exit 0; plugin validate exit 0; marketplace validate exit 0, no version warning; `claude plugin test .` 2444 tests, 0 fail, exit 0. Re-run after the fix-now edits, same counts, all five exit 0. PASS.
- Gate (2026-10-21): cairn_validate all checks passed, exit 0; no principle changed, so no cairn_impact; profile gate: verify green (AC5), no marketplace version warning, CHANGELOG Unreleased carries the entry. PASS.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the step 1 resume rests on a remembered route, not a fresh read — fix now (step 1 reads `mergeable` fresh)
- diff-bug #2: a red verify, or a session end, between the resolved rebase and the push — fix now for red verify (fixed before the push); the session-end window went to the candidate row "Close the guest conflict sync edges"
- diff-bug #3: the unanswered-maintainer-comment read belongs only to `OPEN` otherwise — fix now (the `CONFLICTING` and `UNKNOWN` arms read it too)
- diff-bug #4: a sync-only resume runs a full second review pass — follow-up ("Close the guest conflict sync edges")
- diff-bug #5: the stacked sync pushes before its verify — fix now (verify before any push, the stacked lease push included)
- diff-bug #6: a dirty tree makes the rebase refuse with no conflicted files — follow-up, pre-existing ("Close the guest conflict sync edges")
- diff-bug #7: `UNKNOWN` gets no retry — reject, planned change (AC1 reports `UNKNOWN` with no route)
- diff-bug #8: the abort stop leaves the milestone `in-progress` while its PR waits — follow-up ("Close the guest conflict sync edges")
- diff-bug #9: `--diff-filter=U` leaves out files already resolved — reject, false: the stop names the files the user must still act on, and resolved files need nothing
- diff-bug #10: nothing in `/hotfix` rebases a conflicted hotfix PR — follow-up ("Close the guest conflict sync edges")
- diff-bug #11: the pane's `PR_BUTTON` comment reads as the full route list — fix now (pane.ts comment and DESIGN.md say "three of the routes")
- diff-bug #12: the §2 arm leaves out the cannot-resolve stop, and the rulebook and review close overstate the route for a closed stack base — fix now
- diff-bug #13: a conflict resolved in review's step 1 sync gets no claim re-check — reject, false: review step 1 runs before step 3's evidence and step 5's lenses, which read the resolved tree
- diff-bug #14: lines past the wrap width — reject, style
- blame-history #1: resolved conflicts are pushed with no user chip (tension with D-171) — reject, planned change (AC4 names the re-push after resolution; D-171 binds the `/hotfix` requested-changes route)
- blame-history #2: the new arms skip the unanswered-comment quotes — fix now (same fix as diff-bug #3)
- blame-history #3: verify placement is ambiguous, and the generic guest sync lets the requested-changes route resolve conflicts too — reject, false for the order (the text runs verify after the rebase ends) and planned change for the placement (AC4 puts it in the guest sync)
- blame-history #4: the review close overstates §2 for a closed stack base — fix now (same fix as diff-bug #12)
- blame-history #5: the CHANGELOG adds the conflict route to the M308 bullet, and lines run long — reject, style
- prior-review #1: the review close label routes a closed-stack-base PR — fix now (same fix as diff-bug #12)
- prior-review #2: step 1's "guest sync" reads as the plain rebase for a stacked milestone — fix now (step 1 names the stacked sync)
- prior-review #3: long lines — reject, style
- ripple #1: skills/tests/test_guest_stacked_milestones.py:42 pins "and an open stacked one …" that the diff rewrote — fix now (wording restored; the guard passes by hand)
- ripple #2: cairn/DESIGN.md:462-463 reads the three Buttons as all the routes — fix now (same fix as diff-bug #11)
