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
- **Branch/PR:** m267-guest-push-remote

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

- [ ] AC1: `skills/shared/tracking-rules.md` defines the push remote `<push>`: in guest mode it is `<base>` when
      `cairn/PROFILE.md` carries the header line `# Push remote: base`, and `<fork>` otherwise; `<push-owner>` is the
      owner of the repo `<push>` names. It also states that a push to a branch that already has an open PR goes to the
      remote that holds that PR's head. The file-map row for `PROFILE.md` names the line and says no validator reads
      it, and the Collaboration-mode bullets name `<push>` where they now name `<fork>` as the push target.
- [ ] AC2: No line that `git grep -n -i -e fork -e 'gh pr create' -e 'git push' -- skills ':!skills/tests'` returns
      on the branch head names, in a guest arm, the fork as where a branch is pushed or where a new PR's head lives,
      except through `<push>`/`<push-owner>` or the open-PR head rule of AC1.
- [ ] AC3: When `<push>` is `<base>`, `/milestone-review` step 8's guest arm and `/hotfix`'s guest handoff run
      `gh api repos/<base-repo> --jq .permissions.push` before the push; on any output but `true`, or a failed read,
      the step pushes nothing, opens no PR, and stops with a close block that names the read and its result.
- [ ] AC4: The rulebook's fork-remote stop (no matching remote, or more than one) applies whenever a guest push target
      resolves to the fork, by `<push>` or by an open PR's head, and does not apply when it resolves to `<base>`.
- [ ] AC5: `/milestone-implement`'s guest sync of a branch that is already pushed, before it rebases, fetches the
      remote that holds the branch and reads `git rev-list <slug>..<remote>/<slug>`; when that is non-empty it does not
      rebase, pushes nothing, and stops with a close block naming those commits. Otherwise it rebases and pushes with
      `--force-with-lease=<slug>:<sha>`, `<sha>` being the remote branch tip read at that check.
- [ ] AC6: The README's guest-mode section and a CHANGELOG entry state the line, the push-access check, and that a repo
      without the line still pushes to the fork; `grep -n -i fork README.md` shows no line left saying that guest mode
      always pushes to the fork.
- [ ] AC7: The `verify` slot is green, and the hand-run prose guards (`python3 -m unittest discover -s skills/tests`
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
- [ ] T6: Update `skills/tests/test_guest_fork_remote.py` for the new targets, and add guards that fail when the
      `<push>` definition, the access read, or the implement remote-only-commits stop is removed; plant each removal
      once and see the guard go red.
- [ ] T7: README guest section (lines 848–891, and line 797's "pushes to your fork") and a CHANGELOG entry.
- [ ] T8: Run `verify` and the hand-run `skills/tests` suite from the repo root, each exit code checked.

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
- 2026-10-16: decided the change route's push target is the upstream `gh pr checkout` sets, named `<head-remote>`, since that is the remote holding the PR's head whichever repo it is.

## Decisions

## Review
