# M266: Give /hotfix reruns a route for closed PRs, own open PRs, and guest change requests

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's `/hotfix` rerun on a PR takes these routes
- **Branch/PR:** m266-hotfix-rerun-gaps

## Goal

A `/hotfix` rerun on a closed PR, on the operator's own open hotfix PR that no approval marker resumes, or on a guest hotfix PR whose maintainers requested changes reaches a route that can finish, in place of the adopt-a-PR walk or a bare stop.

## Scope

**In:** `skills/hotfix/SKILL.md` step 1 gains a closed-PR stop, an owner route for the operator's own open `hotfix-` PR, and a guest change route; step 6's Copilot round arm and step 7's off-but-present sentence name the owner route. README.md, CHANGELOG.md, and the DESIGN.md Known issues entry follow. Prose guards in `skills/tests/test_resume_routing.py` with mutation entries.

**Out:**
- Reopening a closed PR for the operator. The close block leaves it to the operator on GitHub.
- Re-requesting a maintainer review or replying on the PR in guest mode. The operator does this by hand.
- A third party's open `hotfix-` PR in guest mode. It keeps the report-and-stop, and the DESIGN.md Known issues entry holds it.
- The M262 review's other rerun edges (a masked change request in `latestReviews`, red CI, unread comments on resume). They stay in DESIGN.md Known issues.
- The "Open hotfix PRs" bullet of `/milestone`. It names no next command and stays as it is.

## Acceptance criteria

- [ ] AC1: `/hotfix` step 1 states a closed-PR stop. It covers a PR-reference argument whose `gh pr view <N> --json state,headRefName` reports `CLOSED` and a head branch that does not match `m<nnn>-*`, in owner or guest mode. The run makes the candidate-row match and skips the tier check and steps 2 to 7. In owner mode it removes `cairn/.merge-approved` when the marker's line starts with `hotfix ` and names that PR (`for PR #<N>`), and otherwise leaves the marker. The stop edits no candidate row. Its close block says that the PR closed without a merge and that reopening it on GitHub is the operator's choice. The close block names each matched row that ends with ` — started #<N>`. Its fenced next command is `/hotfix` with a description of the bug, which starts over on a new branch.
- [ ] AC2: `/hotfix` step 1 states an owner route for the operator's own open hotfix PR. It covers an `OPEN` PR in owner mode whose `headRefName` starts with `hotfix-` and whose `author.login` equals `gh api user --jq .login`, when the open-PR re-entry's owner arm does not resume it. The run takes the tier-check walk with the PR as an authored fix whose PR exists, not as an adopted PR. Steps 2, 3, and 5 take their adopting variants, except step 5's contributor fallback. Step 6's Copilot round arm runs for it, with a push to the PR's head branch and no `gh pr create`. Step 7's off-but-present rule applies to it as to an authored fix this run merged. Step 6's sentence "An adopted PR skips the round" and step 7's sentence that exempts an adopted PR each say that this route is outside the exemption.
- [ ] AC3: `/hotfix` step 1's guest arm states a change route. It covers an `OPEN` PR whose head branch starts with `hotfix-` and whose `author.login` equals the operator's login. The PR also has a `latestReviews` entry with state `CHANGES_REQUESTED` whose `submittedAt` is later than the head commit's `committedDate`. The run reads the PR's conversation as step 6's PR-conversation read states, with `--repo <base-repo>`. It checks out the PR's branch, and it makes a change for each requested item or names the reason it makes none. It tier-checks the new diff against `<base>/<default-branch>`, and a diff over the hotfix bar takes step 1's over-the-bar disposition with nothing pushed. It re-runs step 3's two-way check against `<base>/<default-branch>` and step 4's `verify` slot on the new head. It edits step 5's changelog entry when a change makes the entry wrong.
- [ ] AC4: After AC3's checks, the change route poses one chip whose question text lists each requested item with its change or reason, with a decline option. On approval it pushes to `<fork>`, posts no comment or reply on the PR, and stops with the guest arm's close block. That close block also says that the reply to the maintainers is the operator's. On decline it pushes nothing, and its close block names the unpushed commits. Every other open `hotfix-` PR in guest mode keeps the guest arm's report-and-stop.
- [ ] AC5: README.md and a CHANGELOG.md `## Unreleased` entry state the routes of AC1 to AC4. In the DESIGN.md Known issues entry on `/hotfix` reruns, the sentence that cites the candidate row is rewritten, and the sentence "A marker whose PR merged or closed outside the session stays on disk" is narrowed to the merged case. After that, `git grep -n "has no resume route for an open PR" -- README.md skills cairn/DESIGN.md` returns no match.
- [ ] AC6: At the branch head, the five `verify` slot commands of `cairn/PROFILE.md` pass as written there, each exit code read on its own.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks

- [x] T1: Write AC1's closed-PR stop into step 1, ahead of the merged-PR re-entry (`skills/hotfix/SKILL.md:59`). Add a test class for it to `skills/tests/test_resume_routing.py`, pinning its trigger and its outcome on their own, with mutation entries in `skills/tests/test_mutation_harness.py`.
- [x] T2: Write AC2's owner route into the open-PR re-entry (`SKILL.md:125-156`), adding `author` to its `gh pr view` read. Edit step 6's "An adopted PR skips the round" (`SKILL.md:261`) and step 7's adopted-PR sentence (`SKILL.md:437-438`). Update the pinned field list at `test_resume_routing.py:346` in the same commit. Add tests with mutation entries.
- [x] T3: Write AC3's trigger and checks into the guest arm (`SKILL.md:157-166`), adding `author` and `latestReviews` and the head commit date to its read. Keep the pins at `test_resume_routing.py:418` and the mutation block at `test_mutation_harness.py:4141` green, or update them in the same commit. Add tests with mutation entries.
- [x] T4: Write AC4's chip, push, and close into the guest arm. Add tests with mutation entries.
- [x] T5: Edit the README rerun paragraph (`README.md:784-792`), add the CHANGELOG `## Unreleased` entry, and edit the DESIGN.md Known issues sentences (`cairn/DESIGN.md:791-795`).
- [x] T6: Run the five `verify` slot commands, each exit code read on its own. Hand-run `python3 -m unittest discover -s skills/tests` as evidence for T1 to T4 (it gates nothing).

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: what to work on — the user chose the candidate row "`/hotfix` has no resume route for an open PR", over its promotion condition (a real-session occurrence, not yet seen); logged as a user override. Run through to the merge question.
- 2026-10-16: collision check: absorbs that candidate row in full; M262 (done) shipped the marker resume this extends, under D-168, whose resume conditions stay unchanged; D-130 and D-131 annotated by route, not superseded; D-108's door passed on its retained trigger, since `/hotfix` sends a closed PR into a walk that cannot merge and a guest closed PR into the adopt walk guest mode forbids; DESIGN.md Known issues entry on `/hotfix` reruns edited by T5. Not the checker-regress shape.
- 2026-10-16: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-16: lessons harvested: M112 (sweep README, templates, and docs for the old phrasing; owe a CHANGELOG task) shaped T5; M148/M182 (prose-guard locators; hand-run `skills/tests` after edits near guarded regions) and M172 (check each re-entry route against the preconditions of the steps it lands on) shaped T2 to T4 and the audit's design questions.
- 2026-10-16: criteria audit (full mode, fresh Opus reader): 12 findings, all accepted. Closed stop scoped past `m<nnn>-*` heads and to `hotfix ` markers (1); `gh pr reopen` dropped from the close block, since a deleted head, a re-landed PR, or a maintainer's close can make it wrong (2); the stop names a matched row's dead started token and edits no row (3); AC2 names the adopting variants of steps 2, 3, and 5 (4) and quotes the two exemption sentences (5); T2 and T3 name the pins the read changes break (6); AC3 triggers on a `latestReviews` change request, since `reviewDecision` is empty where the base requires no reviews (7), and only one submitted after the head commit, so a rerun after the push does not loop (8); AC3 re-runs the tier check and the two-way check (9); AC5 narrows the closed-marker Known issues sentence (10); AC6 cites the verify slot as written (11) and drops `skills/tests`, which gates nothing (12). AC3 was split into AC3 and AC4.
- 2026-10-16: plan gate chose a dated `latestReviews` change request (`submittedAt` after the head commit's `committedDate`) over `reviewDecision` because `gh` returns an empty `commit.oid` on `latestReviews` (read on PR #277) and `reviewDecision` is empty without required reviews; falsified by a real guest PR whose change request the route misses or re-handles.
- 2026-10-16: plan gate chose one chip after the changes are made over a triage chip before them, because the maintainers' requests are the scope and the user still sees each change or reason before any push; falsified by a run where the user wants to reject a request before work is spent on it.
- 2026-10-16: plan gate chose the adopt walk with an authored-fix label for the owner's own PR over a separate step 1 arm, because the adopting variants of steps 2, 3, and 5 already fit a PR whose fix is committed; falsified by a real run where an adopting step misbehaves on the operator's own branch.
- 2026-10-16: implement started on `m266-hotfix-rerun-gaps`; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-16: T1 done: closed-PR stop in step 1 ahead of the merged-PR re-entry; `TestHotfixClosedPrStop` (5 tests) and 5 mutation entries, each shown to turn its guard red; verify slot green (5 of 5). The simple-english hook flags pre-existing whole-file hits in `SKILL.md`; rewriting the skill is out of scope.
- 2026-10-16: correction to the T1 line: T1 ran only the `-k Hotfix` slice of `skills/tests`; the full hand-run suite was red at 813b861d on `test_external_pr_intake.TestIntakeRouting.test_no_second_approval_mechanism` (a second `cairn/.merge-approved` literal). Fixed in T2: the closed-PR stop names "step 6's merge-guard marker", the file step 6 defines, which keeps AC1's removal; full `skills/tests` green (798).
- 2026-10-16: T2 done: "Own open PR (M266)" paragraph after the guest arm; `author` added to the open-PR read and its pin and mutation block; step 6's round-arm and step 7's off-but-present sentences name the route; `TestHotfixOwnOpenPr` (5 tests) and 5 mutation entries, each red when blanked; verify slot green (5 of 5).
- 2026-10-16: T3 and T4 done in one commit (one inserted block): the guest arm's read gains `author,latestReviews,commits`; "Change route (M266)" triggers on a change request whose `submittedAt` is after the last commit's `committedDate`, runs step 6's three reads with one chip in place of their per-item options, uses `gh pr checkout <N> --repo <base-repo>`, and pushes with `git push <fork> <headRefName>`. M262's guest pins unchanged and green. `TestHotfixGuestChangeRoute` (8 tests) and 8 mutation entries, each red when blanked; full `skills/tests` green (806); verify slot green (5 of 5).
- 2026-10-16: T5 done: README rerun paragraph (`README.md:790-797`) and a CHANGELOG `### Fixes` entry under Unreleased name the three routes; DESIGN.md Known issues sentences rewritten and narrowed (marked `narrowed M266`); AC5's `git grep` returns no match (exit 1). Old-phrasing sweep over README, `/milestone`, `/milestone-plan`, tracking-rules, and `hooks/status/*.ts` found nothing else to change.
- 2026-10-16: claim audit: 20 claims read, 1 corrected — skills/hotfix/SKILL.md, README.md, CHANGELOG.md, skills/tests/test_resume_routing.py, skills/tests/test_mutation_harness.py
- 2026-10-16: claim audit fixes: the "one entry per pinned clause" comments made true with 2 more mutation entries; the reader also found the round arm's decline would `gh pr close` the operator's own pre-existing PR, fixed with a sentence that leaves it open and names `/hotfix` with the PR reference (new test and entry). Same reader's one re-read: both hold. 24 M266 mutation entries, none survive blanking.
- 2026-10-16: open concerns for review: `committedDate` is commit time, not push time, so a commit made before a change request and pushed after it still triggers the change route; `latestReviews` masking (already in Known issues) also applies to the change route's trigger.
- 2026-10-16: T6 done: verify slot green (5 of 5) at the final tree; hand-run `skills/tests` green (807). Status → review.

## Decisions

## Review
