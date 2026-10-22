# M314: Answer each Copilot review in one PR comment

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the Copilot round and `/copilot-review` post on the user's pull requests
- **Branch/PR:** —

## Goal

In every mode, the Copilot round and `/copilot-review` answer a Copilot review with one PR comment that gives each note's outcome, in place of a reply on each thread.

## Scope

**In:** `skills/shared/copilot-review.md` §4 to §6: the per-thread reply goes, and the summary reply becomes the one comment, with one line per note, then the resolves. `skills/copilot-review/SKILL.md` (description and steps 6 and 7), the Copilot wording in `/milestone-review` and `/hotfix`, README's Copilot text, `CHANGELOG.md`, the hand-run guards in `skills/tests` that cite the removed reply text, and a D-entry that supersedes the per-thread reply.

**Out:** guest-mode limits on open PRs, threads, bots, and issue closes → M315. When the round runs and who requests the review stay as they are: the opt-in line, and the request by `/milestone-review` and `/hotfix` (the user's answer at this plan's question set).

## Acceptance criteria

- [ ] AC1: In `skills/shared/copilot-review.md`, the round answers each Copilot review that has a note with one PR comment, and it posts no reply on a thread. A review has a note when it has an unresolved Copilot thread or a body finding with no thread anchor. The comment goes once every note of that review has a disposition and each fix is pushed. Its first line is the review's URL, and it has one line per note: each such thread, named by its path and its line (its original line when the thread is outdated), and each such body finding. Each line says `fixed in <short-sha>`, gives the reason the note is not a problem, or says the note is left for a later change. No line thanks Copilot, and in guest mode no line carries cairn vocabulary. After the comment, the round resolves each Copilot thread the comment names. A review whose URL an operator comment already carries gets no second comment, and its unresolved Copilot threads are resolved. A note that takes `/milestone-review`'s return floor holds back its review's comment and resolves. `git grep -n -E "/replies|addPullRequestReviewThreadReply|in_reply_to" -- skills ':!skills/tests'` prints nothing.
- [ ] AC2: `skills/copilot-review/SKILL.md`'s description and steps state that it posts the one comment of AC1 for each review that has a note and that no operator comment links yet, then resolves the threads that comment names, with no reply on a thread. They also state that it asks the user in chat about a note it cannot settle, before that review's comment goes.
- [ ] AC3: Each line that `git grep -n -i -E "repl(y|ies)" -- skills ':!skills/tests' README.md` prints and that is about Copilot's threads or reviews describes the one comment, not a reply on each thread.
- [ ] AC4: `CHANGELOG.md`'s Unreleased section says that in every mode the Copilot round and `/copilot-review` answer each Copilot review with one PR comment that gives each note's outcome, in place of a reply on each note, and resolve Copilot's threads after it. No Unreleased entry still says that the round or `/copilot-review` replies on each thread.
- [ ] AC5: `wc -l -c skills/shared/copilot-review.md` reads under 165 lines and under 9,600 bytes, the budget the module's header states.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T2, T3
- AC4 → T3
- AC5 → T1

## Tasks

- [ ] T1: Rewrite `skills/shared/copilot-review.md` §4 to §6. §4's thread read selects each thread's first comment's review URL (`pullRequestReview{url}`), so threads group by review. §5 drops step 3's reply and its command, and its summary reply becomes AC1's one comment, then the resolves. A note fixed on an earlier pass takes its line from the Review section's `copilot:` line. Drop the "one for each reply" empty-body clause. §6's report lines stay. Diff every removed sentence against main (LESSONS M152/M287), and keep the module within its budget.
- [ ] T2: Update `skills/copilot-review/SKILL.md` (description, steps 6 and 7, close), `/milestone-review` (step 7's read, ~line 586) and `/hotfix` (~lines 217 and 361) where they name replies, and README's `/copilot-review` row and Copilot bullet (~lines 777 and 975-1010). Update or retire the hand-run guards in `skills/tests` that cite the removed reply text (`test_copilot_review_round.py`, `test_mutation_harness.py`, `test_resume_routing.py`), and run them.
- [ ] T3: Edit the two Unreleased CHANGELOG entries that name the summary reply and `/copilot-review`'s replies (~lines 174-183 and 305-314) to the one-comment form, or add one entry and correct them. Write the D-entry that supersedes the per-thread reply of D-153 and D-187's order (D-187's one-comment-per-review link and skip rule stand). Its trigger is shipped behavior, the replies `copilot-review` posted, so D-108's door does not bar it.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a change to what two skills post on GitHub, with a design decision.
- 2026-10-21: idea vet: none found. The one comment keeps the public record of which notes were real (the user's reason) and sends one notification per review in place of one per note.
- 2026-10-21: collision check: D-153 (the read replies on each thread and resolves it) and D-187 (the summary reply after the threads are resolved, linked by the review's URL) are narrowed by this milestone's D-entry; D-152's opt-in stands. LESSONS M152/M287 (a budgeted module's rewrite dropped earlier rules) shapes T1. Inbox sweep: 0 open issues, 1 open PR (#327, M312's own), no overlap.
- 2026-10-21: request: the user decided the one-comment form, in every mode and with no profile switch, from the second easystats audit (175 inline Copilot replies and about 30 summary replies, 22 from one template, three starting "Thanks"), sent by the easystats session. When it lands, tell that session (`local_95d534cd-aebf-45b4-80c3-073b576fd59f`) so it can cut its rule to "request the Copilot review yourself and run `copilot-review`".
- 2026-10-21: criteria audit (full mode, fresh Opus reader): AC1 gained the crash-safe skip (a linked review's threads are resolved with no second comment), the "has a note" definition, the outdated thread's original line, the guest vocabulary rule, and the GraphQL and REST reply forms in its grep; AC2 cites AC1's qualifiers; AC3's grep leaves out the hand-run `skills/tests` (T2 updates them); AC4 bars a stale Unreleased entry. The thread-to-review grouping and the earlier-pass line moved to T1, and the D-entry to T3. Proportionality: nothing.
- 2026-10-21: plan gate chose to group threads by their first comment's review URL over the body's `#discussion_r` anchors, because the anchors were never shown complete; falsified by a Copilot thread whose first comment names no review.
- 2026-10-21: question set: guest repos keep the Copilot opt-in line (the round runs, and requests Copilot, only with `# Copilot review: on`), so this milestone leaves §1 and §2 as they are.
