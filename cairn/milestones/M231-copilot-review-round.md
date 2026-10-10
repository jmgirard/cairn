# M231: Hotfix and milestone PRs get a Copilot review round

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — `/hotfix` and `/milestone-review` ship in the plugin to every operator
- **Branch/PR:** m231-copilot-review-round

## Goal

In a repo whose `cairn/PROFILE.md` opts in, `/hotfix` and `/milestone-review` request a Copilot review on the pull request. They then fix, reply to, and resolve each Copilot thread before the merge question, or before the close block in guest mode.

## Scope

**In:** one shared module, `skills/shared/copilot-review.md`, states the round once. It covers the opt-in line, the request, the wait, the disposition of each thread, the reply, and the resolve. If GitHub takes a level per request, `/hotfix` asks for Lite and `/milestone-review` asks for Balanced. In owner mode with the round on, the PR opens before the merge question (D-152 narrows D-138). In guest mode the round runs after the handoff opens the PR. A run stopped at the round's wait resumes from the PR's state. This absorbs the "`/hotfix` has no resume route for an open PR" candidate row, because the round's wait makes that stop real. cairn's own `PROFILE.md` turns the round on. README, CHANGELOG, DESIGN, and the rulebook's "A branch push starts CI" bullet follow.

**Out:** a `/milestone` audit that reads every bot thread on the operator's open PRs goes to a new candidate row. A `/cairn-init` question that offers the opt-in line is not planned, because the README documents the line. A second Copilot round after the fix pushes is not planned. Copilot's own re-review on push is a repository setting.

## Acceptance criteria

- [ ] AC1: `skills/shared/copilot-review.md` states the round. The opt-in line is `# Copilot review: on` in `cairn/PROFILE.md`, and an absent line or any other value means off. The module states the request command and the wait for the review with its timeout stop. It states that a refused or unavailable request is reported in chat and the round is skipped. A Copilot thread is an unresolved thread whose first comment's author is Copilot. Each Copilot thread gets a disposition: fix now, reject with a reason, or follow-up as a candidate row. Each Copilot thread also gets a reply (`Fixed in <sha>`, or the reason, with no thanks) and a `resolveReviewThread` call. `git grep -n copilot-review.md -- skills` lists both `skills/hotfix/SKILL.md` and `skills/milestone-review/SKILL.md`.
- [ ] AC2: The module asks for Lite from `/hotfix` and Balanced from `/milestone-review` through the per-request level field that T1 found. If T1 found none, the module requests with no level, and the round's chat report says that GitHub's settings chose the level.
- [ ] AC3: In owner mode with the round on, `/milestone-review` pushes the branch and opens the PR after step 6 and before step 7's merge question. It then runs the round, and the merge question lists each Copilot thread with its disposition. `/hotfix` does the same before its step-6 approval chip. With the round off, the post-approval push-and-open text of `/hotfix` step 6 and `/milestone-review` step 8 stays in place as the off arm.
- [ ] AC4: In guest mode with the round on, the round runs after the handoff opens the PR and before the close block. Every `gh pr` command in the module carries `--repo <base-repo>`. Every `gh api` call names the base repo's owner and name in its path or GraphQL variables. Replies carry no cairn vocabulary.
- [ ] AC5: A run stopped at the round's wait timeout resumes from its fenced command: `/milestone-review M<NNN>`, or `/hotfix` with the PR reference. The resume reads from the PR whether Copilot was requested, whether its review arrived, and which Copilot threads are unresolved. A `/hotfix` PR-reference argument whose PR is open, with a `hotfix-*` head branch that the operator authored, enters step 6, not step 1's adopt-a-PR walk.
- [ ] AC6: `cairn/PROFILE.md` carries `# Copilot review: on`. On M231's own PR, Copilot's review is requested and arrives, and each Copilot thread on it gets a reply and is resolved. A GraphQL `reviewThreads` read before the merge question shows zero unresolved threads whose first comment's author is Copilot.
- [ ] AC7: The profile's `verify` slot is green: both unittest suites, `claude plugin validate` on both manifests, and `claude plugin test`. A new prose guard in `skills/tests/` pins AC1's two module citations and AC3's two arms, and the hand-run `skills/tests` suite is green. README and CHANGELOG describe the opt-in line.

## Coverage

- AC1 → T2, T3, T4
- AC2 → T1, T2
- AC3 → T3, T4, T5
- AC4 → T2, T3, T4
- AC5 → T3, T4
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Probe for a per-request Copilot level field: the REST docs for `POST /pulls/{n}/requested_reviewers`, the GraphQL `RequestReviewsByLoginInput` and `CopilotCodeReviewParametersInput` types, and `gh pr edit --help`. Log the field or its absence with the date and the sources read. Also find which request form works: `gh pr edit <N> --add-reviewer @copilot`, or GraphQL `requestReviewsByLogin` with `botLogins`. The insight sessions show that the first form works, and that one empty check right after it can mislead.
- [ ] T2: Write `skills/shared/copilot-review.md`: the opt-in line, the request with its level, the refused-request skip, and the wait. The wait is one foreground loop under the rulebook's wait rule. Its timeout stop has a close block that names the resume command. The module states the thread read: GraphQL `reviewThreads` with `isResolved`, `path`, `line`, and each comment's `databaseId`, author, and body. It states the disposition rule from `/milestone-review` step 5 and the fix pushes. It states the reply through REST `pulls/<N>/comments/<id>/replies`, the resolve, and the guest-mode `--repo` and owner/name forms.
- [ ] T3: `/milestone-review`: with the round on, owner mode pushes and opens the PR after step 6 and runs the round. Step 7's merge question lists the Copilot dispositions, and the PR-conversation read then runs on the PR that already exists. Step 8 skips the create. The guest handoff runs the round after the create. Add the resume route for a stop at the round's wait.
- [ ] T4: `/hotfix`: the same two arms around step 6. Step 1 gains the open-PR route: an open PR whose head is `hotfix-*` and whose author is the operator enters step 6.
- [ ] T5: Append D-152 to `cairn/DECISIONS.md`, done at plan. Point the rulebook's "A branch push starts CI" bullet at the opt-in arm. Update `cairn/DESIGN.md`'s architecture paragraphs on the review and hotfix PR timing.
- [ ] T6: Add `# Copilot review: on` to `cairn/PROFILE.md`, under the collaboration-mode header position. The live round on M231's PR runs at review.
- [ ] T7: README, CHANGELOG, and a prose guard in `skills/tests/`. Run the verify slot and the hand-run `skills/tests` suite.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: collision check: no planned or in-progress milestone, and no open GitHub issue or PR (inbox count 0). D-138 (the PR opens after approval) collides in owner mode, and the question set settled it, so D-152 narrows it. D-145 and D-146 were superseded by D-147, so the merge question is the only gate. M177's PR-conversation read is reused, not changed. The candidate row "`/hotfix` has no resume route for an open PR" is absorbed into AC5 and T4, and its prune is left for post-merge hygiene.
- 2026-10-10: evidence from the insight, parameters, and correlation sessions (Explore subagent): `gh pr edit <N> --add-reviewer @copilot` requests the review, replies go through REST `pulls/<N>/comments/<id>/replies`, and resolves go through GraphQL `resolveReviewThread`. Lite and Balanced are GitHub settings. The insight memory says replies to bots carry no thanks.
- 2026-10-10: GitHub's 2026-10-02 changelog says the API takes a level per request, but the REST docs and the GraphQL schema read on 2026-10-10 show no such field. T1 re-probes.
- 2026-10-10: question set: when the round runs in an owner repo — before the merge question, with the PR opened early.
- 2026-10-10: question set: the level when GitHub takes none per request — request anyway, and the report says GitHub's settings chose it.
- 2026-10-10: question set: turn the round on for cairn's own repo — yes, and each cairn PR then uses Copilot credits.
- 2026-10-10: the user's request ("babysit it to address, respond to, and resolve its comments") is the permission for unattended fix pushes, replies, and resolves in the round. That question was dropped from the set at its four-question limit.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned findings on AC1, AC2, AC3, AC4, and AC6. AC1 now names a thread by its first comment's author. AC2 lost its work-log clause, which moved to T1. AC4 splits `gh pr` from `gh api` forms and adds the refused-request skip (moved to AC1) and the no-cairn-vocabulary rule. AC6 gained the PROFILE line and lost its Review-section clause. The AC3 finding cited the up-front approval of D-145, which D-147 removed, so it was rejected.
- 2026-10-10: plan gate chose a `PROFILE.md` header line over a new profile slot, because `cairn_validate` FAILs a missing slot in every adopting repo. Falsified by an adopter whose skills cannot find the header line. No validate check reads the line, so the checker is not extended.
- 2026-10-10: plan gate chose one shared module over prose in each skill, because the round is the same in both skills. Falsified by the two skills needing different round steps beyond the level.
- 2026-10-10: plan gate chose one Copilot round per PR over re-requesting after fix pushes, because each review uses credits and a repo can turn on Copilot's own re-review on push. Falsified by a merged PR whose fix push drew a Copilot finding that named a real defect.
- 2026-10-10: M231 is planned before M232 (the issue look-in), so that M232's own PR gets the second live round.
- 2026-10-10: implement started on branch `m231-copilot-review-round`. The untracked `cairn-probe.log` on main is not this milestone's and stays unstaged.
- 2026-10-10: T1: no per-request Copilot level field found on 2026-10-10. Sources read: the REST docs for `POST /pulls/{n}/requested_reviewers` (`reviewers` and `team_reviewers` only), the GraphQL `RequestReviewsByLoginInput` (`userLogins`, `botLogins`, `teamSlugs`, `union`) and `CopilotCodeReviewParametersInput` (`reviewDraftPullRequests`, `reviewOnPush`) types, `gh pr edit --help` in gh 2.102.0, and the Copilot code review how-to page. The round uses `gh pr edit <N> --add-reviewer @copilot`, which the help names and the insight sessions used. Copilot's GraphQL login is `copilot-pull-request-reviewer`, and its REST login is `copilot-pull-request-reviewer[bot]` (read on easystats/insight PR 1253).

## Decisions

## Review
