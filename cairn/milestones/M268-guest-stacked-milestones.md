<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M268: Let a guest milestone build on one that waits for the maintainers

- **Status:** planned
- **Priority:** normal
- **Depends on:** M267
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — changes which guest milestones are workable and where their branches and PRs start
- **Branch/PR:** —

## Goal

In a guest repo that pushes to the base repo, a milestone can depend on a handed-off milestone, with its branch and PR
built on that milestone's branch until the first PR merges.

## Scope

**In:** a stack base: in guest mode with `# Push remote: base`, a dependency that is `blocked` and whose milestone
file's `Branch/PR` header names a PR URL. `scripts/cairn_next.py`'s workable rule and its mirror in
`hooks/status/reader.ts`, with fixtures under `hooks/status/fixtures/`; `/milestone-implement` steps 1–2 (accept a
stack base, cut from its branch, record the base tip); `/milestone-review` step 8's guest arm (`--base`); the restack
after the base PR merges (`/milestone` §2's route and the implement sync); tracking-rules, README, CHANGELOG; a
D-entry annotating D-137.

**Out:** where the branches are pushed → M267. Stacking in owner mode → not planned; owner milestones merge in order,
and a dependency there stays `done`-only. A milestone with two or more stack-base dependencies → it stops at implement
step 1 with a close block; building on more than one branch is not planned. Stacking a hotfix on a milestone → not
planned.

## Acceptance criteria

- [ ] AC1: `cairn_next.workable` and the pane reader's workable list count a `planned` milestone as workable when
      each dependency is `done` or a stack base and at most one is a stack base. The fixtures under
      `hooks/status/fixtures/`, held to both readers by `scripts/tests/test_status_fixtures.py` and `claude plugin
      test`, include a guest repo with the line where a milestone on one stack base is workable, and five trees where
      it is not: owner mode, guest mode without the line, a `blocked` dependency whose header names no PR URL, an
      `in-progress` dependency whose header names a PR URL, and a milestone on two stack bases.
- [ ] AC2: `/milestone-implement` step 1 accepts a stack base as a met dependency; it stops with a close block naming
      them when a milestone has two or more, and with one naming the branch when `git ls-remote <base>
      <stack-base-branch>` finds no such branch. Step 2's guest arm cuts the branch from `<base>/<stack-base-branch>`;
      each later sync onto an unmerged stack base runs `git rebase --onto <base>/<stack-base-branch> <sha>` with the
      newest `stack base:` line's `<sha>`; and the cut and each sync write a work-log line `stack base: <branch> at
      <sha>` naming the new base tip.
- [ ] AC3: While the stack base's PR is `OPEN`, `/milestone-review` step 8's guest arm opens a stacked milestone's PR
      with `--base <stack-base-branch>`, and the PR body names the stack base's PR; when that PR is `MERGED`, step 8
      opens no PR and routes to `/milestone-implement M<NNN>` for the restack of AC4.
- [ ] AC4: Once the stack base's PR is `MERGED`, `/milestone` §2 routes a `blocked` stacked milestone to
      `/milestone-implement M<NNN>`, whose sync runs `git rebase --onto <base>/<default-branch> <sha> <slug>` with the
      newest `stack base:` line's `<sha>`, force-pushes with lease to the PR's head remote, and runs `gh pr edit <N>
      --repo <base-repo> --base <default-branch>` when `gh pr view <N> --repo <base-repo> --json baseRefName` still
      names the stack-base branch.
- [ ] AC5: The stack-base exception is stated at each statement of the workable rule that
      `grep -n -i -e workable -e "Depends on" skills/shared/tracking-rules.md skills/milestone-plan/SKILL.md
      skills/milestone-implement/SKILL.md cairn/DESIGN.md README.md` returns (among them tracking-rules line 158,
      milestone-plan step 7's run chaining, DESIGN.md line 167, README.md line 186); the README's guest-mode section and
      a CHANGELOG entry describe stacking and the restack.
- [ ] AC6: The `verify` slot is green (both `python3 -m unittest` suites, `claude plugin validate` on both manifests,
      `claude plugin test`), and the hand-run `skills/tests` suite passes on the branch head.

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T7

## Tasks

- [ ] T1: Fixtures first: add the six trees from AC1 under `hooks/status/fixtures/` with `expected.json`, regenerate
      `hooks/status/fixtures.gen.ts`, and see the stack-base tree fail on both readers.
- [ ] T2: Add the stack-base rule to `scripts/cairn_next.py` (`_deps_done`, line 240) using
      `cairn_common.collaboration_mode` and the `Branch/PR` reader it already has (line 23), and mirror it in
      `hooks/status/reader.ts` (`workableRows`, line 157); the `waiting` list follows the same rule.
- [ ] T3: `/milestone-implement` step 1 (line 36) and step 2's guest arm: accept a stack base, stop on two or more or
      on a branch missing from `<base>`, cut from its branch, sync onto it with `--onto`, and write the `stack base:`
      line at the cut and at each sync.
- [ ] T4: `/milestone-review` step 8's guest arm: read the stack base PR's state; on `OPEN`, `--base
      <stack-base-branch>` and the PR body line naming the base PR; on `MERGED`, route to the restack.
- [ ] T5: The restack: `/milestone` §2's `blocked` bullet (lines 173–185) gains the merged-stack-base route;
      `/milestone-implement`'s guest sync gains the `--onto` rebase, the lease push, and the conditional base edit.
- [ ] T6: Each workable-rule site AC5's grep returns (tracking-rules, milestone-plan step 7, DESIGN.md, README) and
      the Collaboration-mode bullets; README guest section; CHANGELOG; a
      D-entry annotating D-137 for the stack-base exception; prose guards in `skills/tests/` for T3–T5.
- [ ] T7: Run `verify` and the hand-run `skills/tests` suite from the repo root, each exit code checked.

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: scope — the push location plus stacking; M267 holds the push location, this milestone the stacking.
- 2026-10-16: plan gate chose a recorded `stack base:` tip over reading the old base from the local branch or `<base>/<branch>` because `git fetch --prune` or a deleted local branch loses those refs after the merge; falsified by a restack whose recorded tip is missing or wrong.
- 2026-10-16: plan gate chose the existing `/milestone-implement` resume path for the restack over a new §2 action that rebases on its own, because §2 writes nothing and implement already re-runs `verify` and hands back to review; falsified by restacks that need no verify and make the review pass pure overhead.
- 2026-10-16: criteria audit (full mode, fresh Opus reader): 6 findings on M268, all fixed — AC1's negative trees lacked an `in-progress` dependency and a two-stack-base milestone (both added; readers allow at most one stack base); AC2 lacked a check that the base branch exists and a rule for syncing onto a force-pushed base (`ls-remote` stop and `--onto` sync added); AC3 had no condition on the base PR being open (now routes a merged base to the restack); AC4's `gh pr view` lacked `--repo` (added); AC5 missed copies of the workable rule in DESIGN.md, README, and milestone-plan step 7 (now a grep-bounded promise). AC6: no finding.
- 2026-10-16: absorbed candidate row "Guest milestone branches on the base repo" (with M267).

## Decisions

## Review
