# M266: Give /hotfix reruns a route for closed PRs, own open PRs, and guest change requests

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's `/hotfix` rerun on a PR takes these routes
- **Branch/PR:** m266-hotfix-rerun-gaps, https://github.com/jmgirard/cairn/pull/278

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

- [x] AC1: `/hotfix` step 1 states a closed-PR stop. It covers a PR-reference argument whose `gh pr view <N> --json state,headRefName` reports `CLOSED` and a head branch that does not match `m<nnn>-*`, in owner or guest mode. The run makes the candidate-row match and skips the tier check and steps 2 to 7. In owner mode it removes `cairn/.merge-approved` when the marker's line starts with `hotfix ` and names that PR (`for PR #<N>`), and otherwise leaves the marker. The stop edits no candidate row. Its close block says that the PR closed without a merge and that reopening it on GitHub is the operator's choice. The close block names each matched row that ends with ` — started #<N>`. Its fenced next command is `/hotfix` with a description of the bug, which starts over on a new branch.
- [x] AC2: `/hotfix` step 1 states an owner route for the operator's own open hotfix PR. It covers an `OPEN` PR in owner mode whose `headRefName` starts with `hotfix-` and whose `author.login` equals `gh api user --jq .login`, when the open-PR re-entry's owner arm does not resume it. The run takes the tier-check walk with the PR as an authored fix whose PR exists, not as an adopted PR. Steps 2, 3, and 5 take their adopting variants, except step 5's contributor fallback. Step 6's Copilot round arm runs for it, with a push to the PR's head branch and no `gh pr create`. Step 7's off-but-present rule applies to it as to an authored fix this run merged. Step 6's sentence "An adopted PR skips the round" and step 7's sentence that exempts an adopted PR each say that this route is outside the exemption.
- [x] AC3: `/hotfix` step 1's guest arm states a change route. It covers an `OPEN` PR whose head branch starts with `hotfix-` and whose `author.login` equals the operator's login. The PR also has a `latestReviews` entry with state `CHANGES_REQUESTED` whose `submittedAt` is later than the head commit's `committedDate`. The run reads the PR's conversation as step 6's PR-conversation read states, with `--repo <base-repo>`. It checks out the PR's branch, and it makes a change for each requested item or names the reason it makes none. It tier-checks the new diff against `<base>/<default-branch>`, and a diff over the hotfix bar takes step 1's over-the-bar disposition with nothing pushed. It re-runs step 3's two-way check against `<base>/<default-branch>` and step 4's `verify` slot on the new head. It edits step 5's changelog entry when a change makes the entry wrong.
- [x] AC4: After AC3's checks, the change route poses one chip whose question text lists each requested item with its change or reason, with a decline option. On approval it pushes to `<fork>`, posts no comment or reply on the PR, and stops with the guest arm's close block. That close block also says that the reply to the maintainers is the operator's. On decline it pushes nothing, and its close block names the unpushed commits. Every other open `hotfix-` PR in guest mode keeps the guest arm's report-and-stop.
- [x] AC5: README.md and a CHANGELOG.md `## Unreleased` entry state the routes of AC1 to AC4. In the DESIGN.md Known issues entry on `/hotfix` reruns, the sentence that cites the candidate row is rewritten, and the sentence "A marker whose PR merged or closed outside the session stays on disk" is narrowed to the merged case. After that, `git grep -n "has no resume route for an open PR" -- README.md skills cairn/DESIGN.md` returns no match.
- [x] AC6: At the branch head, the five `verify` slot commands of `cairn/PROFILE.md` pass as written there, each exit code read on its own.

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

Pass 1, 2026-10-16, at 0f68faa1 (PR #278; Copilot requested at review start).

- AC1 evidence: `skills/hotfix/SKILL.md:59-71` reads `gh pr view <N> --json state,headRefName`, covers `CLOSED` with a head not matching `m<nnn>-*` in both modes, makes the candidate-row match, skips the tier check and steps 2 to 7, removes in owner mode "step 6's merge-guard marker" (named `cairn/.merge-approved` at `SKILL.md:402`) only when its line starts with `hotfix ` and names the PR, edits no row, and ends with a close block saying the PR closed without a merge and reopening is the operator's, naming each matched row ending ` — started #<N>`, fenced next command `/hotfix` with a bug description. `TestHotfixClosedPrStop` 5/5 ok.
- AC2 evidence: `SKILL.md:205-216` covers an owner-mode `OPEN` PR with `headRefName` starting `hotfix-` and `author.login` equal to `gh api user --jq .login` (the open-PR read adds `author`, `SKILL.md:139`), when the owner arm does not resume it; walks it as an authored fix whose PR exists, not an adopted PR; steps 2, 3, and 5 take their adopting variants except step 5's contributor fallback; step 6's round arm runs with a push and no `gh pr create`; step 7's off-but-present rule applies. Step 6's "An adopted PR skips the round" is followed by "Step 1's own open PR is outside that exemption" (`SKILL.md:313-316`), and step 7's adopted-PR sentence by "Step 1's own open PR is outside that adopted-PR exemption" (`SKILL.md:493-494`). `TestHotfixOwnOpenPr` 6/6 ok.
- AC3 evidence: the guest arm (`SKILL.md:170-181`, an `OPEN` PR whose head starts `hotfix-`) reads `author,latestReviews,commits` and sends a PR the change route covers to it. `SKILL.md:182-197` covers `author.login` equal to the operator's login and a `latestReviews` entry with state `CHANGES_REQUESTED` and `submittedAt` later than the last commit's `committedDate`; runs step 6's three PR-conversation reads with `--repo <base-repo>`; `gh pr checkout <N> --repo <base-repo>`; a change per item or its reason; tier-check against `<base>/<default-branch>`, over the bar to the over-the-bar disposition with nothing pushed; step 3's two-way check against `<base>/<default-branch>` and step 4's `verify`; changelog edited when a change makes it wrong. `TestHotfixGuestChangeRoute` tests 1-5 ok.
- AC4 evidence: `SKILL.md:198-204`: one `AskUserQuestion` chip listing each item with its change or reason, a decline option; on approval `git push <fork> <headRefName>`, no comment or reply on the PR, the report-and-stop's close block plus a line that the reply to the maintainers is the operator's; on decline nothing pushed and a close block naming the unpushed commits. Any other guest `hotfix-` PR goes on to the report-and-stop (`SKILL.md:174-181`, M262 guards still green). `TestHotfixGuestChangeRoute` tests 6-8 ok.
- AC5 evidence: `README.md:790-797` and a `CHANGELOG.md` `### Fixes` entry under `## Unreleased` state the closed-PR stop, the own-PR walk, and the guest change route (diffstat README +6/-1, CHANGELOG +22). `cairn/DESIGN.md:791-797`: the row-citing sentence rewritten and the marker sentence narrowed to "A marker whose PR merged outside the session stays on disk". `git grep -n "has no resume route for an open PR" -- README.md skills cairn/DESIGN.md` printed nothing, exit 1.
- AC6 evidence: at 0f68faa1 the five `verify` slot commands of `cairn/PROFILE.md` each exited 0, read one at a time (`scripts/tests`, `hooks/tests`, `plugin validate` on plugin.json and marketplace.json, `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`).
- Consistency gate: `cairn_validate` all checks passed (exit 0); no principle text changed, so `cairn_impact` skipped; profile slot: verify green (AC6), marketplace validate shows no `version` warning, CHANGELOG has the entry with no milestone ids. Hand-run `skills/tests` 807 ok.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the change route states no stop for a red `verify` or a failed two-way check before the chip and push — fix now (stop with nothing pushed, close names the failure; new pin)
- diff-bug #2: a decline leaves local commits, and a rerun redoes the route on a branch already ahead — fix now (route goes on from local commits past `headRefOid`; every close names `/hotfix` with the PR)
- diff-bug #3: the change route narrows D-168's guest sentence with no D-entry — fix now (D-171)
- diff-bug #4: the own-PR walk never refreshes the body's `Candidate row:` lines, so a later resume can fail its row condition — follow-up ("Hotfix rerun edges (M266 review)")
- diff-bug #5: `gh pr checkout` in the change route skips step 2's dirty-tree check — fix now
- diff-bug #6: a contributor PR closed by the re-land fallback gets "start over" though the re-landed PR is open — follow-up (same row)
- diff-bug #7: the open-PR re-entry's opening sentence does not name the own-PR paragraph — reject (false: the own-PR paragraph is the tier-check walk that sentence names)
- diff-bug #8: the chip's place in step 6's read leaves the blocking rule unclear — fix now (the rule does not apply, the chip never merges)
- diff-bug #9: the over-the-bar close does not name the local commits — fix now
- diff-bug #10: "last entry of `commits`" assumes no cap, and "the new diff" is ambiguous — fix now for the wording ("the PR's whole diff"); the cap goes to follow-up (same row)
- diff-bug #11: DESIGN Known issues says "no fix planned" beside M266's routes and overstates the closed-marker removal; lines unwrapped — fix now
- diff-bug #12: the CHANGELOG heading says a closed PR's route "can finish" — fix now ("a route forward")
- diff-bug #13: no pins for the closed stop's order, the other-guest-PR fallthrough, or the base-repo checkout — fix now (3 pins, 3 mutation entries)
- diff-bug #14: a closed guest milestone PR takes the hotfix closed stop; a closed owner `m<nnn>-*` PR falls to the adopt walk — follow-up (same row)
- diff-bug #15: unclear referent in the round-decline sentence, unwrapped lines — fix now
- blame-history #1: D-168's guest sentence contradicted with no D-entry — fix now (D-171; same as diff-bug #3)
- blame-history #2: DESIGN.md "The guest arm stops any open `hotfix-` PR, whoever opened it" is now false — fix now (narrowed to PRs outside the change route)
- blame-history #3: a round decline leaving the own PR open departs from M231's close — reject (planned change: the PR predates the run, so the decline closes nothing this run opened; the user can close it by hand)
- blame-history #4: the adopting variants push before the chip, against D-138 — reject (false: D-138 governs when a PR opens, this PR already exists, and adopted PRs push the same way)
- blame-history #5: commit time against push time, `latestReviews` masking, and the decline loop — decline loop fixed now (diff-bug #2); masking added to DESIGN Known issues; commit time to follow-up (same row)
- blame-history #6: `git push <fork> <headRefName>` fails if `gh` names the local branch differently — fix now (`HEAD:<headRefName>`)
- blame-history #7: the route's commits do not cite the no-cairn-vocabulary rule and D-161 — reject (false: both bind every guest write by the rulebook's Collaboration mode section)
- blame-history #8: the re-land edge of the closed stop — follow-up (same row; diff-bug #6)
- blame-history #9: `copilot-review.md` §1 not updated for the own PR — reject (false: its "an authored hotfix PR this run merged" already covers it)
- blame-history #10: the row promoted over its trigger — reject (planned: a logged user override at the question set)
- prior-review #1: lines past 80 columns, as in M244, M249, M265 — fix now (rewrapped)
- prior-review #2: the change route's decline close and the round-decline close carry no CI line (M183) — fix now
- prior-review #3: `latestReviews` masking applies to the change route's trigger — fix now in DESIGN Known issues (Scope Out keeps the fix there)
