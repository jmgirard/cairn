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
- [x] AC6: The `verify` slot is green (both `python3 -m unittest` suites, `claude plugin validate` on both manifests,
      `claude plugin test`), and the hand-run `skills/tests` suite passes on the branch head.

## Coverage

- AC1 → T1, T2
- AC2 → T3, T8
- AC3 → T4, T8
- AC4 → T5, T8
- AC5 → T6, T8
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
- [x] T8: Review return 1: fix every Review-section finding marked "fix now (floor return 1)" — one stacked sync that
      replaces the plain guest rebase in implement and review step 1, the stack-base lookup after hygiene, step 1's
      chained, cross-repo, and fork-head stops, the closed-base routes, the placeholder names, the stale wording, and
      the PROFILE.md regular-file check; re-run `verify` and `skills/tests`.

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
- 2026-10-16: review opened PR #280 at its start (Copilot round on) and requested Copilot (state `none` before the request).
- 2026-10-16: review return 1: floor return on load-bearing stacked-sync prose defects: a stacked resume can run the plain guest rebase (review step 1 and implement step 2: diff-bug #1, #2), the restack has no stack-base lookup after hygiene and pushes a branch never pushed (#4, #5), and the step-1 checks miss a chained, cross-repo, or fork-headed base PR (#3, #6, #7); fix every finding the Review section marks "fix now (floor return 1)" in one task.
- 2026-10-16: resumed for review return 1; added T8 (minor amendment) and mapped it in Coverage to AC2–AC5.
- 2026-10-16: T8: implement step 1 now stops on a base PR URL outside `<base-repo>`, a base PR whose `baseRefName` is not the default branch (chains), and a fork-headed base PR; the stacked sync replaces the plain guest rebase, fetches first, names `<slug>` in both `--onto` forms, pushes only a branch the check found pushed, keeps the lease on the remote tip, and defines `<N>`; review step 1 takes the stacked sync; review step 8's and §2's closed-base arms stop or report with no status change; tracking-rules says how a stacked milestone finds its stack base after hygiene, that an archived dependency is never a stack base, and fixes the two older guest bullets; stale "all done" wording fixed in `cairn_next.py`, `reader.ts`, `/milestone`; `check_release_window`'s comment states the done-only rule; `_profile_header` skips a non-regular file (new FIFO test, shown to fail with the check removed); prose guard updated; verify green (409, 179, 0, 0, 2018), skills/tests 822 OK, cairn_validate clean.
- 2026-10-16: claim audit not re-run for T8: the step's one-pass rule ran it once above; T8's prose goes to review's fresh lenses.
- 2026-10-16: status review; handed to /milestone-review.

## Decisions

## Review

- AC1: `python3 -m unittest scripts.tests.test_status_fixtures -v` on the review head: 11 OK, `test_python_helpers_match_expected` and `test_stack_base_fixtures_hold_the_cases` pass; expected workable lists read `stack-base` [M302, M304], `stack-owner`, `stack-no-push-line`, `stack-no-pr`, `stack-in-progress` [M304], `stack-two-bases` [M304, M305]; `fixtures.gen.ts` holds the six trees; planted defect: the same suite with main's `scripts/cairn_next.py` fails on `stack-base` and `stack-two-bases` only; the TS reader side is `claude plugin test` in AC6's run.
- AC2: whitespace-normalized read of `skills/milestone-implement/SKILL.md`: step 1 holds "except that in guest mode one of them may be a stack base", the two-or-more stop, and the stop when `git ls-remote <base> <stack-base-branch>` prints no `refs/heads/<stack-base-branch>` line, naming the branch; step 2 holds the cut `git checkout -b <slug> <base>/<stack-base-branch>` with its `stack base: <stack-base-branch> at <sha>` line, the open-base sync `git rebase --onto <base>/<stack-base-branch> <old>` where `<old>` is "the `<sha>` of the newest `stack base:` line", and "Each sync writes a work-log line `stack base: <branch> at <sha>`, naming the new base and its tip".
- AC3: `skills/milestone-review/SKILL.md` step 8's guest arm, normalized read: it reads the base PR with `gh pr view <base-pr> --repo <base-repo> --json state`; on `OPEN` "the create below adds `--base <stack-base-branch>`, and its body names the stack base's PR"; on `MERGED` "push nothing and open no PR" and stop with a close block whose next command is `/milestone-implement M<NNN>`.
- AC4: `skills/milestone/SKILL.md` §2's blocked bullet routes "`OPEN` on a stacked milestone ... whose stack base's PR reads `MERGED`" to `/milestone-implement M<NNN>`; implement step 1 accepts that `blocked` milestone; step 2's stacked sync runs `git rebase --onto <base>/<default-branch> <old> <slug>` (`<old>` the newest `stack base:` line's `<sha>`), "Then push to the PR's head remote" under "the same check and lease push" (`git push --force-with-lease=<slug>:<sha> <remote> <slug>`), reads `gh pr view <N> --repo <base-repo> --json baseRefName`, and runs `gh pr edit <N> --repo <base-repo> --base <default-branch>` only "If that still names the stack-base branch".
- AC5: AC5's grep returns 29 lines; the five that state the rule carry the exception: tracking-rules 158 ("or in guest mode when one of them is a stack base"), its new Collaboration-mode bullet (397), milestone-plan step 7 (525), milestone-implement step 1 (38), DESIGN.md 167–172, README 186–192; the other hits use the word without stating the rule (tracking-rules 431, 494; milestone-plan 37, 201, 529; DESIGN 40, 164, 184, 274, 291, 733; README 217–220, 252–253, 313, 898). README guest bullet "A milestone can build on one that waits for review" (894) and CHANGELOG's top entry describe stacking and the restack.
- AC6: from the repo root, code unchanged since 5bfa8237, each exit code 0: `scripts/tests` 409 OK (21 skipped), `hooks/tests` 178 OK, `claude plugin validate` plugin 0 and marketplace 0 with no version warning, `claude plugin test .` 2018 pass 0 fail (235 passing cases name a `stack-` fixture, including the reader's workable and next-step cases for `stack-base` and `stack-two-bases`), hand-run `skills/tests` 822 OK.
- gate: `cairn_validate.py` exit 0, all checks passed (coverage complete included); no DESIGN.md principle changed, so `cairn_impact` skipped; profile consistency-gate: verify green on the review head (AC6), marketplace validate shows no `plugins[N].version` warning, and CHANGELOG's Unreleased section opens with this milestone's entry, with no milestone number.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: review step 1's guest sync runs the plain `git rebase <base>/<default-branch>` on a stacked branch and replays the stack base's commits — fix now (floor return 1: a load-bearing skill defect)
- diff-bug #2: implement step 2 never says the stacked `--onto` sync replaces the plain guest rebase, so both can run — fix now (floor return 1)
- diff-bug #3: a chained stack (a base that is itself stacked) restacks onto the default branch though its base merged elsewhere — fix now (floor return 1): step 1 stops when the base PR's `baseRefName` is not the default branch
- diff-bug #4: the restack says "push to the PR's head remote" for a branch never pushed, against the check's "push nothing" — fix now (floor return 1)
- diff-bug #5: after the base's hygiene its row is `done`, so the text never says which dependency the stacked milestone built on — fix now (floor return 1): find it by the first `stack base:` line's branch
- diff-bug #6: the header's PR URL can name another repo while `gh pr view <n> --repo <base-repo>` reads a different PR — fix now (floor return 1): step 1 stops on a URL outside `<base-repo>`
- diff-bug #7: step 1 checks the branch by name only, not the PR head's owner — fix now (floor return 1): step 1 stops when `headRepositoryOwner` is not the base repo's owner
- diff-bug #8: `/milestone` §2 has no route for a stacked milestone whose base PR is `CLOSED` — fix now (floor return 1): §2 reports it as the user's decision
- diff-bug #9: review step 8's `CLOSED` arm "stop the same way" is ambiguous about setting `in-progress` and writing a `restack:` line — fix now (floor return 1)
- diff-bug #10: `<sha>` names both the lease tip and the base tip in one step — fix now (floor return 1)
- diff-bug #11: `<N>` is undefined in implement — fix now (floor return 1)
- diff-bug #12: a base branch deleted with no merge closes the stacked PR — follow-up, "Stack-base edges (M268 review)"; a closed base PR is the #8 report
- diff-bug #13: tracking-rules' guest bullets still say the branch is cut from the default branch and list §2's routes with no restack — fix now (floor return 1)
- diff-bug #14: `check_release_window`'s comment claims it mirrors `cairn_next` — fix now (floor return 1): comment states the done-only rule and why
- diff-bug #15: the readers list as workable a milestone whose base PR already merged or closed, until hygiene runs — reject, planned change: AC1 defines a stack base by its header URL, and the readers run no `gh`; implement step 1 stops on it
- diff-bug #16: TS `splitLines` breaks PROFILE.md lines on more characters than Python's file iteration — follow-up, "Stack-base edges (M268 review)"
- diff-bug #17: `cairn_next` now opens PROFILE.md with no regular-file check, so a FIFO hangs it — fix now (floor return 1)
- diff-bug #18: no fixture with a padded id, a duplicate dependency, a BOM PROFILE.md, or a done-and-blocked row — follow-up, "Stack-base edges (M268 review)"
- diff-bug #19: the open-base `--onto` form leaves out `<slug>` — fix now (floor return 1)
- diff-bug #20: a single-branch fetch refspec leaves no `<base>/<stack-base-branch>` after `ls-remote` passed — follow-up, "Stack-base edges (M268 review)"
- blame-history #1: GitHub may close the stacked PR when the merged base branch is deleted — reject, false: GitHub retargets open PRs based on a merged PR's deleted head branch to that PR's base; only a deletion without a merge closes them (diff-bug #12)
- blame-history #2: implement's plain rebase vs stacked sync; garbled sentence; no fetch named; `<slug>` missing — fix now (floor return 1, with diff-bug #2, #19)
- blame-history #3: the `gh pr edit` retarget is an outward write no question granted — reject, planned change: AC4 names it, and the question set took the stacking scope
- blame-history #4: `<base-pr>` has no lookup on a resume — fix now (floor return 1, with diff-bug #5)
- blame-history #5: `check_release_window`'s mirror comment — fix now (floor return 1, with diff-bug #14)
- blame-history #6: "dependencies all done" wording left at `cairn_next.py`'s docstring, `reader.ts`'s `WorkableRow` comment, and `/milestone` line 372 — fix now (floor return 1)
- blame-history #7: a stack base's PR state is never read by the readers — reject, planned change (diff-bug #15)
- blame-history #8: no direct unit tests for `stack_bases`, `_met`, `workableRows` with bases — follow-up, "Stack-base edges (M268 review)" (with diff-bug #18)
- blame-history #9: a stacked PR merged into the base branch reaches `done` though its code is not on the default branch — follow-up, "Stack-base edges (M268 review)"
- blame-history #10: chained stacks are unspecified — fix now (floor return 1, with diff-bug #3)
- prior-review #1: the rulebook's archive clause reads as if an archived base counts as a stack base, which the code excludes — fix now (floor return 1, with diff-bug #5's rewrite)
- prior-review #2: the TS PROFILE read has no guard like Python's catch-all — follow-up, "Stack-base edges (M268 review)" (with diff-bug #16)
- pass 2 (head 9e0e1a40, after return 1): AC1 `scripts.tests.test_status_fixtures` OK; AC2–AC4 normalized reads find each clause, now worded as `git rebase --onto <base>/<stack-base-branch> <old> <slug>` with "`<old>` is the base tip that the newest `stack base:` line names", the restack `git rebase --onto <base>/<default-branch> <old> <slug>`, the lease push to the open PR's head remote, and the conditional `gh pr edit`; AC5 grep returns 27 lines and the rule sites are unchanged; AC6 verify green (scripts 409 OK, hooks 179 OK, validates 0 and 0, plugin test 2018 pass), skills/tests 822 OK, cairn_validate clean.
- pass 2 spawned: diff-bug, blame-history, prior-review
- pass 2 diff-bug #1: the readers still count a chained base (a stacked milestone) as a stack base, so `cairn_next` recommends what implement step 1 then refuses — follow-up, "Stack-base edges (M268 review)"; reading a dependency's work log in both readers is new reader scope
- pass 2 diff-bug #2: review step 10 still states the done-only rule — fix now, fixed fd375d3c
- pass 2 diff-bug #3: a sync that stopped could still write a `stack base:` line and move `<old>` — fix now: the line is written last, and a stopped sync writes none, fixed fd375d3c
- pass 2 diff-bug #4: the stacked sync never re-runs `verify` — fix now, fixed fd375d3c
- pass 2 diff-bug #5: `<sha>` still names both the lease tip and the base tip — reject, planned change: AC2 fixes the line's `<sha>` and M267's guard pins the lease's; the step states which tip each names and that the lease never uses `<old>`
- pass 2 diff-bug #6: the URL-repo check is case-sensitive — fix now, fixed fd375d3c
- pass 2 diff-bug #7: on a resume, a stack base back at `review` after rework no longer qualifies — follow-up, "Stack-base edges (M268 review)"
- pass 2 diff-bug #8: review step 1 can run the restack itself, a second restack path — fix now: review step 1 syncs only while the base PR is `OPEN`, and step 8 routes a merged base, fixed fd375d3c
- pass 2 diff-bug #9: the CHANGELOG says "force-pushes it" unconditionally — fix now, fixed fd375d3c
- pass 2 diff-bug #10: line-wrap nits — reject, style
- pass 2 blame-history #1: an interrupted restack can leave the PR on the merged base branch with no route back — fix now (with diff-bug #3), fixed fd375d3c
- pass 2 blame-history #2: review's handoff close block lists §2's routes without the restack; resume routing has no stacked-merge arm — fix now for the close block, fixed fd375d3c; the merged-into-base case is first-pass blame-history #9's follow-up
- pass 2 blame-history #3: review steps 1 and 8 disagree on who restacks; the `restack:` line has no reader — fix now (with diff-bug #8), fixed fd375d3c; the `restack:` line is a record for the work log's reader, as `blocked:` lines are
- pass 2 blame-history #4: a row `blocked` for another cause, with a stale PR URL, counts as a stack base — reject, planned change (first-pass diff-bug #15)
- pass 2 blame-history #5: D-173 does not name return 1's stops — reject: D-173's decision (one stack base on an open base PR) stands, and the rulebook bullet carries the stops that carry it out
- pass 2 blame-history #6: `_profile_header` adds a stat to each `collaboration_mode` call — noted, no change in behavior
- pass 2 blame-history #7: `cairn_next.render` marks no stacked workable row — follow-up, "Stack-base edges (M268 review)"
- pass 2 blame-history #8: return 1 grew implement step 1 by about 20 lines of edge-case stops — noted; each stop names a case that cuts from the wrong branch
- pass 2 prior-review #1: "never a stack base" sits beside "stays the dependency ... after it turns `done`" — fix now: reworded to "met as `done`, not as a stack base", fixed fd375d3c
- pass 2 prior-review #2: the stack-base lookup has no command — fix now: the bullet gives the `gh pr view <n> --json headRefName` read, fixed fd375d3c
- pass 2 prior-review #3: the mirror comments drop "at most one" — fix now, fixed fd375d3c
- pass 2 prior-review #4: the rulebook-size seed in `/milestone` and the mutation harness is stale — reject: the seed drifted on main before this branch, and the branch follows the existing practice
- pass 2 prior-review #5: README and CHANGELOG name only the two-base stop — fix now, fixed fd375d3c
- pass 2 prior-review #6: the open edges on the two review rows stay open — noted
- copilot: skills/milestone-implement/SKILL.md:46 (outdated) — verify the base PR's head repository — fixed 9e0e1a40 (return 1's `headRepositoryOwner` stop)
- copilot: skills/milestone-implement/SKILL.md:48 (outdated) — a planned milestone whose base merged before the start loops between implement and `/milestone` — reject, false: `/milestone` routes the merged base to hygiene, which marks it `done`, and the milestone then cuts from the default branch
- copilot: skills/milestone-implement/SKILL.md:106 (outdated) — the plain guest rebase runs before the stacked sync — fixed 9e0e1a40
- copilot: skills/milestone-review/SKILL.md:668 — the exact `gh pr create` command omits `--base` — fix now, fixed a777bd5d
- copilot: review body (5bfa8237, COMMENTED) — an index of the four threads above, each anchored — noted
- Copilot level: unknown (the review body has no `Review effort:` line; set by GitHub's settings); its one review covered 5bfa8237, before return 1
- conversation: no human reviews, no conversation comments on PR #280; the reads ran on 2026-10-16 before the merge question
- pass 2 fixes on fd375d3c: verify green (scripts 409 OK, hooks 179 OK, validates 0 and 0, plugin test 2018 pass), skills/tests 822 OK, cairn_validate clean.
