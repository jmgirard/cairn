<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M267: Let a guest repo push its branches to the maintainers' repo

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — changes where guest-mode skills push branches and open PRs in other people's repos
- **Branch/PR:** m267-guest-push-remote — https://github.com/jmgirard/cairn/pull/279

## Goal

In guest mode, a repo whose `cairn/PROFILE.md` asks for it pushes its milestone and hotfix branches to the base repo
instead of the fork, after the skill checks that the operator's account can push there.

## Scope

**In:** a `# Push remote: base` header line in `cairn/PROFILE.md`, read only in guest mode; the push remote `<push>`
and `<push-owner>` defined in `skills/shared/tracking-rules.md`; the guest push and PR-create commands in
`skills/milestone-review/SKILL.md`, `skills/hotfix/SKILL.md`, `skills/milestone-implement/SKILL.md`,
`skills/milestone/SKILL.md`, and `skills/shared/copilot-review.md`; a push-access read before the handoff push; a stop
before a force-push over commits that others pushed to the branch; the prose guards in `skills/tests/`; README and
CHANGELOG; a D-entry annotating D-137.

**Out:** a guest milestone that depends on a handed-off one, with its branch and PR built on that branch → M268 (planned
now, depends on M267). Asking about the line at `/cairn-init` → not planned; the README tells the operator to add it by
hand, and a candidate row is added if that proves insufficient. A validator check of the line → none; like the
`# Copilot review:` line, no validator reads it. Owner mode → unchanged; it never reads the line.

## Acceptance criteria

- [x] AC1: `skills/shared/tracking-rules.md` defines the push remote `<push>`: in guest mode it is `<base>` when
      `cairn/PROFILE.md` carries the header line `# Push remote: base`, and `<fork>` otherwise; `<push-owner>` is the
      owner of the repo `<push>` names. It also states that a push to a branch that already has an open PR goes to the
      remote that holds that PR's head. The file-map row for `PROFILE.md` names the line and says no validator reads
      it, and the Collaboration-mode bullets name `<push>` where they now name `<fork>` as the push target.
- [x] AC2: No line that `git grep -n -i -e fork -e 'gh pr create' -e 'git push' -- skills ':!skills/tests'` returns
      on the branch head names, in a guest arm, the fork as where a branch is pushed or where a new PR's head lives,
      except through `<push>`/`<push-owner>` or the open-PR head rule of AC1.
- [x] AC3: When `<push>` is `<base>`, `/milestone-review` step 8's guest arm and `/hotfix`'s guest handoff run
      `gh api repos/<base-repo> --jq .permissions.push` before the push; on any output but `true`, or a failed read,
      the step pushes nothing, opens no PR, and stops with a close block that names the read and its result.
- [x] AC4: The rulebook's fork-remote stop (no matching remote, or more than one) applies whenever a guest push target
      resolves to the fork, by `<push>` or by an open PR's head, and does not apply when it resolves to `<base>`.
- [x] AC5: `/milestone-implement`'s guest sync of a branch that is already pushed, before it rebases, fetches the
      remote that holds the branch and reads `git rev-list <slug>..<remote>/<slug>`; when that is non-empty it does not
      rebase, pushes nothing, and stops with a close block naming those commits. Otherwise it rebases and pushes with
      `--force-with-lease=<slug>:<sha>`, `<sha>` being the remote branch tip read at that check.
- [x] AC6: The README's guest-mode section and a CHANGELOG entry state the line, the push-access check, and that a repo
      without the line still pushes to the fork; `grep -n -i fork README.md` shows no line left saying that guest mode
      always pushes to the fork.
- [x] AC7: The `verify` slot is green, and the hand-run prose guards (`python3 -m unittest discover -s skills/tests`
      from the repo root) pass on the branch head.

## Coverage

- AC1 → T1
- AC2 → T2, T3, T4, T5
- AC3 → T2, T3
- AC4 → T1
- AC5 → T4
- AC6 → T7
- AC7 → T6, T8

## Tasks

- [x] T1: In `skills/shared/tracking-rules.md`, define `<push>` and `<push-owner>` beside the fork-remote recipe
      (lines 253–264), add the open-PR head rule, scope the fork-remote stop to `<push>` = `<fork>`, name the line in
      the `PROFILE.md` file-map row (line 15), and change the Collaboration-mode push targets (lines 369–376) to
      `<push>`. Append a D-entry annotating D-137: guest branches may live on the base repo by the repo's opt-in.
- [x] T2: `/milestone-review`: step 7's guest chip names where the branch goes; step 8's guest arm (lines 637–656) runs
      the access read when `<push>` is `<base>`, pushes to `<push>`, and opens the PR with `--head
      <push-owner>:<slug>`; fix pushes in `skills/shared/copilot-review.md` (line 99) go to the PR's head remote.
- [x] T3: `/hotfix`: the guest handoff (lines 429–437) takes the access read, the push to `<push>`, and `--head
      <push-owner>:hotfix-<slug>`; the guest change route's push (line 208) goes to the open PR's head remote.
- [x] T4: `/milestone-implement` step 2's guest sync (lines 69–74): before the rebase, fetch the branch's remote and
      stop on remote-only commits, then rebase and push with the explicit-sha lease; replace the "operator's own on the
      fork" reason. `/milestone` §2's
      `CHANGES_REQUESTED` route (line 182) re-pushes to the PR's head remote.
- [x] T5: Run AC2's grep over the branch (it also finds prose such as review line 640's "from the fork's branch"),
      fix any guest-arm line still naming the fork as a push target, and log the match count in one work-log line.
- [x] T6: Update `skills/tests/test_guest_fork_remote.py` for the new targets, and add guards that fail when the
      `<push>` definition, the access read, or the implement remote-only-commits stop is removed; plant each removal
      once and see the guard go red.
- [x] T7: README guest section (lines 848–891, and line 797's "pushes to your fork") and a CHANGELOG entry.
- [x] T8: Run `verify` and the hand-run `skills/tests` suite from the repo root, each exit code checked.

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: what to plan — guest stacked PRs (the "Guest milestone branches on the base repo" row).
- 2026-10-16: question set: how cairn decides to push to the maintainers' repo — a per-repo setting in PROFILE.md, with a push-access check at handoff that stops when access is missing.
- 2026-10-16: question set: scope — the push location plus stacking; stacking is M268.
- 2026-10-16: plan gate chose a PROFILE.md header over an automatic push-permission check because a repo whose norm is fork PRs would get branches upstream without asking; falsified by an operator who sets the line in every repo they can push to.
- 2026-10-16: plan gate chose a stop on remote-only commits over pulling them in with a rebase because a shared base-repo branch can carry a maintainer's commits that the operator has not seen; falsified by such stops proving routine and always resolved by a plain rebase.
- 2026-10-16: absorbed candidate row "Guest milestone branches on the base repo" (split across M267 and M268).
- 2026-10-16: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-16: criteria audit (full mode, fresh Opus reader): 3 findings on M267, all fixed — AC5 checked after the rebase and so always fired, now checked before it with an explicit-sha lease; AC4 conflicted with AC1's open-PR rule, now the fork stop follows wherever the push resolves; AC2 bound a ledger and its grep missed fork prose, now a grep-bounded promise with `-i fork`. AC1, AC3, AC6, AC7: no finding.
- 2026-10-16: lessons applied: M185 (sweep every command that resolves against a remote, not the remote's name: AC2's grep covers `git push` and `gh pr create`); M112 (doctrine wording reaches README: AC6's grep).

- 2026-10-16: implement started on m267-guest-push-remote, cut from origin/main at 78992470.
- 2026-10-16: the simple-english style hook flags tracking-rules.md and the skills as a whole (about 500 pre-existing hits); only the sentences this milestone adds are written to it, since rewriting the rulebook is outside M267's scope.
- 2026-10-16: T1 done: tracking-rules defines `<push>`/`<push-owner>`, the open-PR head rule, and the fork stop scoped to fork-bound pushes; the PROFILE.md file-map row names the line; Collaboration-mode bullets push to `<push>`; D-172 annotates D-137. verify green (5/5).
- 2026-10-16: T2–T5 done in one checkpoint (the same files carry all four): review step 7 chip and step 8 handoff push to `<push>` with the access read; `/hotfix` guest handoff likewise, and its change route pushes to the head remote `gh pr checkout` set; implement's guest sync checks `rev-list <slug>..<remote>/<slug>` before the rebase and leases on that sha; `/milestone` §2 and copilot-review fix pushes go to the PR's head remote. verify green (5/5).
- 2026-10-16: T5 sweep: AC2's grep returns 35 lines on the branch; none in a guest arm names the fork as a push target or new-PR head outside `<push>` or the open-PR head rule.
- 2026-10-16: T6 done: `test_guest_fork_remote.py` now pins the push-remote definition, 15 push sites, both access reads, and implement's remote-only-commits stop; each clause and each site is planted out (removed, or reverted to `<fork>`) in memory and the guard goes red. `test_resume_routing.py`'s change-route pin and its mutation-harness block locator follow the new hotfix wording.
- 2026-10-16: T7 done: README guest section gains the push-remote bullet and line 797 says "pushes to the PR's branch"; `grep -n -i fork README.md` returns only the new bullet's default-to-fork lines. CHANGELOG Unreleased entry added.
- 2026-10-16: T8 done: verify green (scripts 0, hooks 0, plugin validate 0, marketplace validate 0, plugin test 0); hand-run skills/tests 818 tests OK; cairn_validate all checks passed.
- 2026-10-16: decided the change route's push target is the upstream `gh pr checkout` sets, named `<head-remote>`, since that is the remote holding the PR's head whichever repo it is.
- 2026-10-16: claim audit: 40 claims read, 3 corrected — skills/milestone-review/SKILL.md, skills/hotfix/SKILL.md, README.md
- 2026-10-16: claim-audit fixes: review step 8's guest arm skips `gh pr create` when the header names an open PR; the hotfix change route resolves `<head-remote>` from `headRepositoryOwner` (base remote, else the fork recipe with its stop), replacing the `gh pr checkout` upstream decision above, which can point at a URL or `refs/pull/N/head`; README says the access read runs before each handoff push with the line set, and that the stop fires on any remote commit the local copy lacks. skills/tests 818 OK; verify green (5/5).
- 2026-10-16: known edge kept: with the line set after a PR opened from the fork, review step 8 still runs the base-repo access read before pushing to the fork head; a non-`true` answer stops with nothing pushed. AC3 gates the read on `<push>`, and the stop fails safe.
- 2026-10-16: implement complete; status review.
- 2026-10-16: review started; PR #279 opened and Copilot requested at review start (state was `none`); AC1–AC7 evidenced at eae9b417.
- 2026-10-16: review return 1: diff-bug #1 — review step 1 rebases and step 8 then runs implement's remote-only-commits check after the rebase, so a guest re-handoff after the default branch moved always stops. Fix it with the review's fix-now items: run the check before any rebase and lease on that tip (review step 1/8, copilot-review), handle a never-pushed branch and use the branch's tracked remote in implement, move the head-owner lookup into the rulebook's open-PR head rule (`.login`, case-insensitive, stop on another owner), reword D-172's trigger and annotate D-171, fix README/CHANGELOG stacking wording, `/milestone` §2's re-push wording, review's step-7 chip text, and put the mutation block back on "Post no comment or reply".

## Decisions

## Review

Evidence gathered 2026-10-16 on branch head eae9b417 (current with origin/main 78992470). PR #279 opened at review start (Copilot round on).

- AC1: normalized read of `skills/shared/tracking-rules.md` finds the `<push>` definition (`<base>` under `# Push remote: base`, else `<fork>`), "Owner mode never reads the line.", the `<push-owner>` definition, the open-PR head rule, the PROFILE.md file-map clause naming the line and "no validator reads"; the Collaboration-mode bullets read "pushed to `<push>`", `--head <push-owner>:<slug>`, "(the push to `<push>` plus"; a regex for `<fork>` as a push target there returns nothing. `grep 'Push remote' scripts/*.py hooks/*.py` returns nothing (no validator reads it).
- AC2: `git grep -n -i -e fork -e 'gh pr create' -e 'git push' HEAD -- skills ':!skills/tests'` returns 35 lines. Owner-mode only: hotfix 313, 373–374, 411; milestone-review 112, 137, 559, 621; milestone-plan 135 (pushes `<base>`); tracking-rules 285 (both modes, names no remote). Guest push or PR head through `<push>`/`<push-owner>` or the open-PR head rule: hotfix 211, 213, 438, 444; milestone-implement 71, 78; milestone-review 549, 640, 649; milestone 182's route (not matched, reads "the remote that holds the PR's head"); copilot-review 100; tracking-rules 376, 383. Lines defining `<fork>`/`<push>`: tracking-rules 260, 263, 265, 268, 269. Fork mentions that are not push targets: cairn-init 99, hotfix 29, 97, 159, 230, 291, 333, 390, milestone 202. No guest-arm line names the fork as a push target or new-PR head outside `<push>` or the head rule.
- AC3: `skills/milestone-review/SKILL.md` step 8 guest arm and `skills/hotfix/SKILL.md` guest handoff both carry, before the push, "When `<push>` is `<base>`, first run `gh api repos/<base-repo> --jq .permissions.push`." and "On any output but `true`, or a failed read, push nothing, open no PR, and stop with a close block that names the read and its result."; `TestAccessRead` (2 tests) passes and goes red on each clause removed in each file.
- AC4: tracking-rules: "When a guest push target resolves to the fork, by `<push>` or by an open PR's head, and no remote matches, or more than one, the push stops before it is made. A target that resolves to `<base>` needs no fork."; the unscoped "With no match, or more than one, a guest push stops before the push." is gone. Pinned in `RECIPE` of `test_guest_fork_remote.py` (passes).
- AC5: `skills/milestone-implement/SKILL.md` step 2 guest arm (lines 69–80): "Fetch the remote that holds the branch (the open PR's head remote, else `<push>` …) and read `git rev-list <slug>..<remote>/<slug>`. If that lists commits, do not rebase, push nothing, and stop with a close block that names those commits. Otherwise note the remote tip's sha, rebase, and push with `git push --force-with-lease=<slug>:<sha> <remote> <slug>`". The check precedes the rebase; `TestRemoteOnlyCommitsStop` passes and goes red on each clause removed.
- AC6: README guest section bullet "Branches go to your fork unless you ask for the upstream repo." states the line, the push-permission read before each handoff push, and the fork default; CHANGELOG Unreleased entry "Guest branches can go to the upstream repo." states the line, the access check, and "A repo without the line still pushes to the fork." `grep -n -i fork README.md` returns lines 879–880 only, both saying the fork is the default unless the line is set; no line says guest mode always pushes to the fork.
- AC7: at eae9b417 from the repo root, each exit code read: `scripts/tests` 0 (408 tests), `hooks/tests` 0 (175 tests), `claude plugin validate` plugin.json 0 and marketplace.json 0, `claude plugin test .` 0 (0 fail); hand-run `skills/tests` 0 (818 tests OK).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: review step 1's guest rebase plus step 8's "after a rebase the check and lease of implement step 2" runs the remote-only-commits check after the rebase, so every re-handoff after the default branch moved stops — fix now (load-bearing: floor return 1).
- diff-bug #2: copilot-review's fix push "after a rebase with the check and lease" has the same after-the-rebase problem — fix now.
- diff-bug #3: implement's sync gives no path for a never-pushed branch; `rev-list` on a missing `<remote>/<slug>` errors — fix now.
- diff-bug #4: "open PR's head remote, else `<push>`" fetches the wrong remote for a branch on the fork with no PR once the line is added — fix now (use the branch's tracked remote).
- diff-bug #5: the open-PR head rule names no lookup outside `/hotfix` — fix now (lookup moves into the rulebook rule).
- diff-bug #6: with the line set and the PR head on the fork, review's access read still gates the push to the fork — follow-up (row "Guest push remote edges"); fails safe, and AC3 keys the read on `<push>`.
- diff-bug #7: D-172's supersede trigger is met by designed paths (change route, Copilot fixes, sync to a base head) — fix now (reword the trigger to the handoff's first push).
- diff-bug #8: `--json headRepositoryOwner` returns an object; the comparison names no `.login` — fix now (with #5).
- diff-bug #9: `--head <push-owner>:<slug>` for a same-repo PR may not be accepted — reject (false): GitHub's create-PR API documents `head` as `username:branch` and accepts it for a same-repo head; the plan's criteria audit read it the same way.
- diff-bug #10: the removal tests only show `missing()` notices a removed clause — reject (style of the repo's guards): each test removes the clause from the real text and sees the guard go red, the same plant M234's revert test uses.
- diff-bug #11: the guards check phrase presence, not order (access read before push, check before rebase) — reject (false as a regression path): the prose carries order in its own words ("first run", "before it rebases"), and the pinned clauses include those words.
- diff-bug #12: SITES does not catch a new guest site naming `<fork>` — reject (planned change): AC2 is a review-time grep sweep by plan, and widening the guard is checker hardening the plan did not call for.
- diff-bug #13: README/CHANGELOG "a PR can then build on another open PR's branch" reads as a cairn feature before M268 — fix now (reword as what the operator can set).
- diff-bug #14: copilot-review ties the head remote to `<push>` instead of the open-PR head rule — fix now (with #2).
- diff-bug #15: `/milestone` §2 says implement's sync re-pushes the change commits; review's re-handoff pushes them — fix now.
- diff-bug #16: review's step-7 chip text names `<push>` for a re-handoff whose PR head is elsewhere — fix now.
- diff-bug #17: the first push to the base repo does not check for a maintainers' branch named `<slug>` — follow-up (row "Guest push remote edges"); a non-fast-forward push is refused.
- blame-history #1: D-171 still says the guest change route pushes to the fork — fix now (D-172 annotates D-171 too).
- blame-history #2: the head-owner rule has no case, null-owner, or third-owner handling — fix now (with diff-bug #5: case-insensitive, stop on any other owner).
- blame-history #3: review/implement/copilot head-remote lookup left to the model — fix now (same as diff-bug #5).
- blame-history #4: never-pushed branch in implement's check — fix now (same as diff-bug #3).
- blame-history #5: the mutation block for `test_approval_pushes_and_posts_nothing` moved off the no-post clause — fix now (block back on "Post no comment or reply").
- blame-history #6: review's new skip of `gh pr create` when the header names an open PR may not match §2's reconciliation — reject (false): step 8's guest arm writes the PR URL to the header on disk, as owner step 8 reads it.
- blame-history #7: a misspelled `# Push remote:` line falls back to the fork silently — reject (planned change): D-172 and the plan keep the line unvalidated, like the Copilot line.
- prior-review #1: mutation coverage of M266's no-post clause thinned — fix now (same as blame-history #5).
- prior-review #2: the change route pushes to a base-repo head with no access read — reject (false as a gap): an open PR whose head is on the base repo already proves the push; the read guards the handoff's first push, which is what README and CHANGELOG say.
- prior-review #3: open comments on PR #279 (never-pushed check; access read keyed to `<push>`) — fix now for the first (diff-bug #3), follow-up for the second (diff-bug #6).
- Consistency gate: `cairn_validate.py` exit 0, all checks passed. No DESIGN.md principle changed, so `cairn_impact --changed` is skipped. Profile consistency-gate: the verify run above.
