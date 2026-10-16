<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M268: Let a guest milestone build on one that waits for the maintainers

- **Status:** review
- **Priority:** normal
- **Depends on:** M267
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — changes which guest milestones are workable and where their branches and PRs start
- **Branch/PR:** m268-guest-stacked-milestones, https://github.com/jmgirard/cairn/pull/280

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

- [x] AC1: `cairn_next.workable` and the pane reader's workable list count a `planned` milestone as workable when
      each dependency is `done` or a stack base and at most one is a stack base. The fixtures under
      `hooks/status/fixtures/`, held to both readers by `scripts/tests/test_status_fixtures.py` and `claude plugin
      test`, include a guest repo with the line where a milestone on one stack base is workable, and five trees where
      it is not: owner mode, guest mode without the line, a `blocked` dependency whose header names no PR URL, an
      `in-progress` dependency whose header names a PR URL, and a milestone on two stack bases.
- [x] AC2: `/milestone-implement` step 1 accepts a stack base as a met dependency; it stops with a close block naming
      them when a milestone has two or more, and with one naming the branch when `git ls-remote <base>
      <stack-base-branch>` finds no such branch. Step 2's guest arm cuts the branch from `<base>/<stack-base-branch>`;
      each later sync onto an unmerged stack base runs `git rebase --onto <base>/<stack-base-branch> <sha>` with the
      newest `stack base:` line's `<sha>`; and the cut and each sync write a work-log line `stack base: <branch> at
      <sha>` naming the new base tip.
- [x] AC3: While the stack base's PR is `OPEN`, `/milestone-review` step 8's guest arm opens a stacked milestone's PR
      with `--base <stack-base-branch>`, and the PR body names the stack base's PR; when that PR is `MERGED`, step 8
      opens no PR and routes to `/milestone-implement M<NNN>` for the restack of AC4.
- [x] AC4: Once the stack base's PR is `MERGED`, `/milestone` §2 routes a `blocked` stacked milestone to
      `/milestone-implement M<NNN>`, whose sync runs `git rebase --onto <base>/<default-branch> <sha> <slug>` with the
      newest `stack base:` line's `<sha>`, force-pushes with lease to the PR's head remote, and runs `gh pr edit <N>
      --repo <base-repo> --base <default-branch>` when `gh pr view <N> --repo <base-repo> --json baseRefName` still
      names the stack-base branch.
- [x] AC5: The stack-base exception is stated at each statement of the workable rule that
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

- [x] T1: Fixtures first: add the six trees from AC1 under `hooks/status/fixtures/` with `expected.json`, regenerate
      `hooks/status/fixtures.gen.ts`, and see the stack-base tree fail on both readers.
- [x] T2: Add the stack-base rule to `scripts/cairn_next.py` (`_deps_done`, line 240) using
      `cairn_common.collaboration_mode` and the `Branch/PR` reader it already has (line 23), and mirror it in
      `hooks/status/reader.ts` (`workableRows`, line 157); the `waiting` list follows the same rule.
- [x] T3: `/milestone-implement` step 1 (line 36) and step 2's guest arm: accept a stack base, stop on two or more or
      on a branch missing from `<base>`, cut from its branch, sync onto it with `--onto`, and write the `stack base:`
      line at the cut and at each sync.
- [x] T4: `/milestone-review` step 8's guest arm: read the stack base PR's state; on `OPEN`, `--base
      <stack-base-branch>` and the PR body line naming the base PR; on `MERGED`, route to the restack.
- [x] T5: The restack: `/milestone` §2's `blocked` bullet (lines 173–185) gains the merged-stack-base route;
      `/milestone-implement`'s guest sync gains the `--onto` rebase, the lease push, and the conditional base edit.
- [x] T6: Each workable-rule site AC5's grep returns (tracking-rules, milestone-plan step 7, DESIGN.md, README) and
      the Collaboration-mode bullets; README guest section; CHANGELOG; a
      D-entry annotating D-137 for the stack-base exception; prose guards in `skills/tests/` for T3–T5.
- [x] T7: Run `verify` and the hand-run `skills/tests` suite from the repo root, each exit code checked.

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: scope — the push location plus stacking; M267 holds the push location, this milestone the stacking.
- 2026-10-16: plan gate chose a recorded `stack base:` tip over reading the old base from the local branch or `<base>/<branch>` because `git fetch --prune` or a deleted local branch loses those refs after the merge; falsified by a restack whose recorded tip is missing or wrong.
- 2026-10-16: plan gate chose the existing `/milestone-implement` resume path for the restack over a new §2 action that rebases on its own, because §2 writes nothing and implement already re-runs `verify` and hands back to review; falsified by restacks that need no verify and make the review pass pure overhead.
- 2026-10-16: criteria audit (full mode, fresh Opus reader): 6 findings on M268, all fixed — AC1's negative trees lacked an `in-progress` dependency and a two-stack-base milestone (both added; readers allow at most one stack base); AC2 lacked a check that the base branch exists and a rule for syncing onto a force-pushed base (`ls-remote` stop and `--onto` sync added); AC3 had no condition on the base PR being open (now routes a merged base to the restack); AC4's `gh pr view` lacked `--repo` (added); AC5 missed copies of the workable rule in DESIGN.md, README, and milestone-plan step 7 (now a grep-bounded promise). AC6: no finding.
- 2026-10-16: absorbed candidate row "Guest milestone branches on the base repo" (with M267).
- 2026-10-16: implement started on branch m268-guest-stacked-milestones; untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-16: T1: six fixtures `stack-base`, `stack-owner` (push line, no mode line), `stack-no-push-line`, `stack-no-pr` (an issue URL), `stack-in-progress`, `stack-two-bases` (M305 on one of the two bases stays workable); before T2 both readers failed on `stack-base` and `stack-two-bases` only; band tests' IDLE_DRAWN and FLOWS tables gained the new fixtures.
- 2026-10-16: T2: chose a `push_remote(root)` reader in `hooks/cairn_common.py` sharing one header reader with `collaboration_mode`, a `stack_bases` set built from `blocked()` (non-archived rows with a PR URL), and one `_met` set for both `workable` and `waiting`, so a row on two stack bases lists both as unmet; TS mirrors as `pushRemote`, `unmetDeps`; verify green (scripts 409 OK, hooks 178 OK, both validates 0, plugin test 2018 pass).
- 2026-10-16: T3: implement step 1 takes the stack base's PR from its milestone header (`<base-pr>`) and the branch from that PR's `headRefName`; a fresh start also stops when the base PR is not `OPEN` (close block → `/milestone`), a case the plan did not name; step 2 gains the cut line and one "Stacked sync" paragraph that holds both the `--onto` sync (T3) and the restack (T5's implement half); verify green (409, 178, 0, 0, 2018).
- 2026-10-16: T4: review step 8's guest arm reads the base PR before the push; `MERGED` sets `in-progress`, writes `restack: PR #<base-pr> merged`, and stops with a close block naming `/milestone-implement M<NNN>` (a close block, not a Skill call, since the user already chose the handoff); `CLOSED` stops the same way; `OPEN` adds `--base` and a body line naming the base PR; verify green (409, 178, 0, 0, 2018).
- 2026-10-16: T5: `/milestone` §2's blocked bullet routes an `OPEN` stacked milestone whose base PR reads `MERGED` to `/milestone-implement M<NNN>`; implement step 1 names that `blocked` milestone as a legal resume; the sync itself landed in T3's paragraph; verify green (409, 178, 0, 0, 2018).
- 2026-10-16: T6: stack-base exception stated at tracking-rules line 158, milestone-plan step 7, implement step 1, DESIGN.md's workable-list paragraph, README's idle-row paragraph; new tracking-rules Collaboration-mode bullet defines stack base, stacked milestone, and the restack, and the PROFILE.md file-map row names the two new readers; README guest bullet and CHANGELOG entry; D-173 annotates D-137 and D-172; prose guard `skills/tests/test_guest_stacked_milestones.py` (EXEMPT entry in the mutation harness, as M234's guards); the three verify figures above were rewritten from slash form to commas because `cairn_validate` read them as dates; verify green, skills/tests 822 OK, cairn_validate clean.
- 2026-10-16: T7: on 17985ff7 from the repo root, each exit code 0: scripts 409 OK (21 skipped), hooks 178 OK, plugin validate 0, marketplace validate 0 with no version warning, plugin test 2018 pass 0 fail, skills/tests 822 OK.
- 2026-10-16: claim audit: 82 claims read, 3 corrected — CHANGELOG.md, skills/milestone/SKILL.md, skills/tests/test_guest_stacked_milestones.py (the CHANGELOG said "open PR" where the readers take any PR URL; §2 left out the restack's conditional retarget; the guard's docstring overstated it, and the guard now pins the restack sentence); the same reader re-read all three and found that they hold.
- 2026-10-16: status review; handed to /milestone-review.

## Decisions

## Review

- AC1: `python3 -m unittest scripts.tests.test_status_fixtures -v` on the review head: 11 OK, `test_python_helpers_match_expected` and `test_stack_base_fixtures_hold_the_cases` pass; expected workable lists read `stack-base` [M302, M304], `stack-owner`, `stack-no-push-line`, `stack-no-pr`, `stack-in-progress` [M304], `stack-two-bases` [M304, M305]; `fixtures.gen.ts` holds the six trees; planted defect: the same suite with main's `scripts/cairn_next.py` fails on `stack-base` and `stack-two-bases` only; the TS reader side is `claude plugin test` in AC6's run.
- AC2: whitespace-normalized read of `skills/milestone-implement/SKILL.md`: step 1 holds "except that in guest mode one of them may be a stack base", the two-or-more stop, and the stop when `git ls-remote <base> <stack-base-branch>` prints no `refs/heads/<stack-base-branch>` line, naming the branch; step 2 holds the cut `git checkout -b <slug> <base>/<stack-base-branch>` with its `stack base: <stack-base-branch> at <sha>` line, the open-base sync `git rebase --onto <base>/<stack-base-branch> <old>` where `<old>` is "the `<sha>` of the newest `stack base:` line", and "Each sync writes a work-log line `stack base: <branch> at <sha>`, naming the new base and its tip".
- AC3: `skills/milestone-review/SKILL.md` step 8's guest arm, normalized read: it reads the base PR with `gh pr view <base-pr> --repo <base-repo> --json state`; on `OPEN` "the create below adds `--base <stack-base-branch>`, and its body names the stack base's PR"; on `MERGED` "push nothing and open no PR" and stop with a close block whose next command is `/milestone-implement M<NNN>`.
- AC4: `skills/milestone/SKILL.md` §2's blocked bullet routes "`OPEN` on a stacked milestone ... whose stack base's PR reads `MERGED`" to `/milestone-implement M<NNN>`; implement step 1 accepts that `blocked` milestone; step 2's stacked sync runs `git rebase --onto <base>/<default-branch> <old> <slug>` (`<old>` the newest `stack base:` line's `<sha>`), "Then push to the PR's head remote" under "the same check and lease push" (`git push --force-with-lease=<slug>:<sha> <remote> <slug>`), reads `gh pr view <N> --repo <base-repo> --json baseRefName`, and runs `gh pr edit <N> --repo <base-repo> --base <default-branch>` only "If that still names the stack-base branch".
- AC5: AC5's grep returns 29 lines; the five that state the rule carry the exception: tracking-rules 158 ("or in guest mode when one of them is a stack base"), its new Collaboration-mode bullet (397), milestone-plan step 7 (525), milestone-implement step 1 (38), DESIGN.md 167–172, README 186–192; the other hits use the word without stating the rule (tracking-rules 431, 494; milestone-plan 37, 201, 529; DESIGN 40, 164, 184, 274, 291, 733; README 217–220, 252–253, 313, 898). README guest bullet "A milestone can build on one that waits for review" (894) and CHANGELOG's top entry describe stacking and the restack.
