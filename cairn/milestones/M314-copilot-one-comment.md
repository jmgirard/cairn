# M314: Answer each Copilot review in one PR comment

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the Copilot round and `/copilot-review` post on the user's pull requests
- **Branch/PR:** m314-copilot-one-comment, https://github.com/jmgirard/cairn/pull/328

## Goal

In every mode, the Copilot round and `/copilot-review` answer a Copilot review with one PR comment that gives each note's outcome, in place of a reply on each thread.

## Scope

**In:** `skills/shared/copilot-review.md` §4 to §6: the per-thread reply goes, and the summary reply becomes the one comment, with one line per note, then the resolves. `skills/copilot-review/SKILL.md` (description and steps 6 and 7), the Copilot wording in `/milestone-review` and `/hotfix`, README's Copilot text, `CHANGELOG.md`, the hand-run guards in `skills/tests` that cite the removed reply text, and a D-entry that supersedes the per-thread reply.

**Out:** guest-mode limits on open PRs, threads, bots, and issue closes → M315. When the round runs and who requests the review stay as they are: the opt-in line, and the request by `/milestone-review` and `/hotfix` (the user's answer at this plan's question set).

## Acceptance criteria

- [x] AC1: In `skills/shared/copilot-review.md`, the round answers each Copilot review that has a note with one PR comment, and it posts no reply on a thread. A review has a note when it has an unresolved Copilot thread or a body finding with no thread anchor. The comment goes once every note of that review has a disposition and each fix is pushed. Its first line is the review's URL, and it has one line per note: each such thread, named by its path and its line (its original line when the thread is outdated), and each such body finding. Each line says `fixed in <short-sha>`, gives the reason the note is not a problem, or says the note is left for a later change. No line thanks Copilot, and in guest mode no line carries cairn vocabulary. After the comment, the round resolves each Copilot thread the comment names. A review whose URL an operator comment already carries gets no second comment, and its unresolved Copilot threads are resolved. A note that takes `/milestone-review`'s return floor holds back its review's comment and resolves. `git grep -n -E "/replies|addPullRequestReviewThreadReply|in_reply_to" -- skills ':!skills/tests'` prints nothing.
- [x] AC2: `skills/copilot-review/SKILL.md`'s description and steps state that it posts the one comment of AC1 for each review that has a note and that no operator comment links yet, then resolves the threads that comment names, with no reply on a thread. They also state that it asks the user in chat about a note it cannot settle, before that review's comment goes.
- [x] AC3: Each line that `git grep -n -i -E "repl(y|ies)" -- skills ':!skills/tests' README.md` prints and that is about Copilot's threads or reviews describes the one comment, not a reply on each thread.
- [x] AC4: `CHANGELOG.md`'s Unreleased section says that in every mode the Copilot round and `/copilot-review` answer each Copilot review with one PR comment that gives each note's outcome, in place of a reply on each note, and resolve Copilot's threads after it. No Unreleased entry still says that the round or `/copilot-review` replies on each thread.
- [x] AC5: `wc -l -c skills/shared/copilot-review.md` reads under 165 lines and under 9,600 bytes, the budget the module's header states.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T2, T3
- AC4 → T3
- AC5 → T1

## Tasks

- [x] T1: Rewrite `skills/shared/copilot-review.md` §4 to §6. §4's thread read selects each thread's first comment's review URL (`pullRequestReview{url}`), so threads group by review. §5 drops step 3's reply and its command, and its summary reply becomes AC1's one comment, then the resolves. A note fixed on an earlier pass takes its line from the Review section's `copilot:` line. Drop the "one for each reply" empty-body clause. §6's report lines stay. Diff every removed sentence against main (LESSONS M152/M287), and keep the module within its budget.
- [x] T2: Update `skills/copilot-review/SKILL.md` (description, steps 6 and 7, close), `/milestone-review` (step 7's read, ~line 586) and `/hotfix` (~lines 217 and 361) where they name replies, and README's `/copilot-review` row and Copilot bullet (~lines 777 and 975-1010). Update or retire the hand-run guards in `skills/tests` that cite the removed reply text (`test_copilot_review_round.py`, `test_mutation_harness.py`, `test_resume_routing.py`), and run them.
- [x] T3: Edit the two Unreleased CHANGELOG entries that name the summary reply and `/copilot-review`'s replies (~lines 174-183 and 305-314) to the one-comment form, or add one entry and correct them. Write the D-entry that supersedes the per-thread reply of D-153 and D-187's order (D-187's one-comment-per-review link and skip rule stand). Its trigger is shipped behavior, the replies `copilot-review` posted, so D-108's door does not bar it.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a change to what two skills post on GitHub, with a design decision.
- 2026-10-21: idea vet: none found. The one comment keeps the public record of which notes were real (the user's reason) and sends one notification per review in place of one per note.
- 2026-10-21: collision check: D-153 (the read replies on each thread and resolves it) and D-187 (the summary reply after the threads are resolved, linked by the review's URL) are narrowed by this milestone's D-entry; D-152's opt-in stands. LESSONS M152/M287 (a budgeted module's rewrite dropped earlier rules) shapes T1. Inbox sweep: 0 open issues, 1 open PR (#327, M312's own), no overlap.
- 2026-10-21: request: the user decided the one-comment form, in every mode and with no profile switch, from the second easystats audit (175 inline Copilot replies and about 30 summary replies, 22 from one template, three starting "Thanks"), sent by the easystats session. When it lands, tell that session (`local_95d534cd-aebf-45b4-80c3-073b576fd59f`) so it can cut its rule to "request the Copilot review yourself and run `copilot-review`".
- 2026-10-21: criteria audit (full mode, fresh Opus reader): AC1 gained the crash-safe skip (a linked review's threads are resolved with no second comment), the "has a note" definition, the outdated thread's original line, the guest vocabulary rule, and the GraphQL and REST reply forms in its grep; AC2 cites AC1's qualifiers; AC3's grep leaves out the hand-run `skills/tests` (T2 updates them); AC4 bars a stale Unreleased entry. The thread-to-review grouping and the earlier-pass line moved to T1, and the D-entry to T3. Proportionality: nothing.
- 2026-10-21: plan gate chose to group threads by their first comment's review URL over the body's `#discussion_r` anchors, because the anchors were never shown complete; falsified by a Copilot thread whose first comment names no review.
- 2026-10-21: question set: guest repos keep the Copilot opt-in line (the round runs, and requests Copilot, only with `# Copilot review: on`), so this milestone leaves §1 and §2 as they are.
- 2026-10-21: implement started on `m314-copilot-one-comment`; the untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-21: T1 done: §5's thread reply and its `/replies` command are gone; §4's thread read selects each first comment's `pullRequestReview{url}`; the summary reply became **The comment** (one per review that has a note, after every disposition and push, the review's URL then one line per note, no thanks, guest vocabulary rule, no second comment for a linked review, then the resolves); §1's write list names the comment. Every removed sentence was diffed against main (LESSONS M152/M287). Module 158 lines, 9,535 bytes. The remaining simple-english lint hits in the module predate the branch.
- 2026-10-21: T2 done: `/copilot-review`'s description and steps 4, 6 (Comment), and 7 (Resolve), `/hotfix` (two sites), `/milestone-review` step 7, and README's row and Copilot bullet name the one comment. Hand-run guards: `test_copilot_review_round` (TestOneComment replaces TestSummaryReply, no-thanks tests retargeted), its mutation-harness entries, and `test_resume_routing` updated; `skills/tests` all OK, the harness included. Verify green: scripts/tests, hooks/tests, both validates, `claude plugin test` 2466 pass, 0 fail.
- 2026-10-21: T3 done: the two Unreleased CHANGELOG entries ("The Copilot round answers each review in one comment", retitled, and `/copilot-review`'s New entry) now give the one-comment form; no Unreleased line says the round replies on each thread. D-212 records the decision, superseding D-153's thread reply and D-187's order.
- 2026-10-21: claim audit: 24 claims read, 2 corrected — CHANGELOG.md (the unsettled-thread sentence now says `/copilot-review` asks in chat), skills/copilot-review/SKILL.md (description names defer); also a TestOneComment docstring and a blank line before the module's no-reply paragraph. Verify green: scripts/tests, hooks/tests, both validates, `claude plugin test` 2466 pass, 0 fail; `skills/tests` OK. Status review.

## Review

- AC1: on 8740e094, `skills/shared/copilot-review.md` §5 reads "The read posts no reply on a thread" (:109); "A review has a note when an unresolved Copilot thread names it ... or its body has a finding with no anchor" (:122-124); the comment goes "once every note of the review has a disposition and each fix is pushed" (:132-133); "Its first line is the review's `url`, then one line per note", threads by path and line, `originalLine` when outdated, and each body item (:136-138); each line is `fixed in <short-sha>`, why the note is not a problem, or left for a later change (:138-140); "The comment never thanks Copilot ... in guest mode carries no cairn vocabulary" (:142-143); "Then resolve each Copilot thread the comment names" (:143-144); a review whose `url` an operator comment already carries "gets no second comment" and its open threads are resolved (:129-131); a return-floor item "holds back its own review's comment and resolves" (:109-111). `git grep -n -E "/replies|addPullRequestReviewThreadReply|in_reply_to" -- skills ':!skills/tests'` printed nothing (exit 1). Pass.
- AC2: `skills/copilot-review/SKILL.md` description: "Post one PR comment for each review that has a note, one line per note, then resolve the notes' threads. Never reply on a thread"; step 6 posts the module's one comment "For each Copilot review that has a note and that no comment by the operator links yet", "Post no reply on a thread"; step 7 resolves the threads a posted comment names; step 4: "That note's review gets no comment until the user answers" after asking in chat. Pass.
- AC3: `git grep -n -i -E "repl(y|ies)" -- skills ':!skills/tests' README.md` on 8740e094: the lines about Copilot are README.md:777 and :985, `skills/copilot-review/SKILL.md`:3 and :101, and `skills/shared/copilot-review.md`:8 and :109. Each states the one comment or that no thread reply is posted, and :8 names M287's budget reset. The other hits are about issue replies, host text, or the pane's thread count. Pass.
- AC4: CHANGELOG Unreleased "The Copilot round answers each review in one comment" (:174) says in every mode the round and `/copilot-review` no longer reply on each Copilot thread, post one PR comment per review with an open note in place of a reply on each note, and resolve the named threads after it; the `/copilot-review` New entry matches. No Unreleased line says the round replies on each thread (`awk 'NR<400' CHANGELOG.md | grep -i -E "repl(y|ies)"` prints only the "no longer reply" and "in place of a reply" clauses). Pass.
- AC5: `wc -l -c skills/shared/copilot-review.md` on 8740e094 prints 162 lines and 9,597 bytes, under 165 and 9,600. Pass.
- gate: `cairn_validate` passed, coverage complete. Verify on 8740e094: scripts/tests OK, hooks/tests OK, both validates passed (marketplace with no `plugins[N].version` warning), `claude plugin test` 2466 pass, 0 fail. `skills/tests` (958) and the mutation harness OK. CHANGELOG Unreleased has the entry. No principle changed, so `cairn_impact` was skipped. A planted `/replies` line turned `test_no_reply_command_in_the_module` red, and the restore turned it green.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a linked review's notes could be disposed again after a crash between the comment and the resolves (main's "skips that review's body items too" was dropped) — fix now (a linked review's notes get no disposition), fixed 8740e094
- diff-bug #2: a thread whose first comment names no review is never answered or resolved — fix now (it joins the newest Copilot review), fixed 8740e094
- diff-bug #3: `/milestone-review` step 7's thread query lacked the fields the grouping needs — fix now (it selects §4's fields with the round on), fixed 8740e094
- diff-bug #4: only a note fixed on an earlier pass had a source for its line — fix now (any note settled on an earlier pass), fixed 8740e094
- diff-bug #5: a floor return could stop the other reviews' comments — fix now (a floor item holds back only its own review), fixed 8740e094
- diff-bug #6: a review held by a failed fix push was not reported — fix now (§6's held line), fixed 8740e094
- diff-bug #7: a review URL that prefixes a longer one counted as carried — fix now (no digit after the `url`), fixed 8740e094
- diff-bug #8: `/copilot-review` step 3 read only non-empty-body reviews and not the operator's comments — fix now, fixed 8740e094
- diff-bug #9: the module header names M287's "summary reply" — reject (false): it records why M287 reset the budget, a history note
- diff-bug #10: DESIGN.md:35-36 said `copilot-review` answers its summary — fix now, fixed 8740e094
- diff-bug #11: the old one-sentence cap on a reply was dropped — fix now (each line is one sentence), fixed 8740e094
- diff-bug #12: D-212 did not name D-187's "before that thread gets a reply" — fix now (D-212's heading names it), fixed 8740e094
- diff-bug #13: summaries said one comment for each review, without "that has a note" or the linked review's resolves — fix now in README, CHANGELOG, and the skill description, fixed 8740e094; the `/hotfix` and `/milestone-review` mentions cite §5 — reject (false): they defer to the module's rule
- diff-bug #14: step 7 listed the comment before matching body findings — fix now (reordered), fixed 8740e094
- diff-bug #15: no guard for the floor hold or the linked review's resolves, which README and CHANGELOG state — fix now (two TestOneComment guards and harness entries), fixed 8740e094; the guest vocabulary, `originalLine`, and §4 field clauses — reject (false): no changelog or README claim states them, and the rulebook asks a test for documented claims
- diff-bug #16: no guard checks that the reply commands are absent — fix now (`test_no_reply_command_in_the_module`, shown to fail on a planted `/replies` line), fixed 8740e094
- diff-bug #17: test docstrings name milestones and how tests are split — reject (style): the guard files' docstrings cite their milestone criteria by convention
- diff-bug #18: one operator comment per review can sit after unanswered maintainer comments in `/milestone`'s guest audit — reject (false): the reviewer notes per-thread replies did the same, so the diff adds nothing here
- blame-history #1: the floor hold widened to the whole review, and the sentence read two ways — reject (planned change) for the widening, which AC1 states; the wording was fixed (diff-bug #5), fixed 8740e094
- blame-history #2: a chat-pending note holds its whole review — reject (planned change): AC2 says the ask comes before that review's comment
- blame-history #3: the linked path now resolves threads on any operator comment carrying the URL — reject (planned change): AC1 states it, so a stopped run finishes its resolves
- blame-history #4: the linked review's body-item skip was dropped — fix now (diff-bug #1), fixed 8740e094
- blame-history #5: "has a note" replaced the non-empty-body trigger — reject (planned change): AC1 defines it
- blame-history #6: the operator's-reply source for an earlier-resolved thread was dropped — reject (false): only unresolved threads are notes now, and an earlier pass's line comes from the Review section
- blame-history #7: the order reversal rests on the linked-path resolve — reject (planned change): D-212 records both
- blame-history #8: DESIGN.md:35-36 — fix now (diff-bug #10), fixed 8740e094
- prior-review #1: the linked-path resolve contradicts the floor hold — reject (false): a review's comment goes only after every note has a disposition, so a floor-held note never sits under a linked review
- prior-review #2: the reviews read is called paged with no `hasNextPage` loop — reject (false): the wording is main's, unchanged, and "paged" means read to the last page
- prior-review #3: README and CHANGELOG said a comment goes to every Copilot review — fix now (diff-bug #13), fixed 8740e094
- ripple #1: DESIGN.md:35-36 — fix now (diff-bug #10), fixed 8740e094
- ripple #2: the comment's `fixed in <short-sha>` differs from §6's `, fixed <short-sha>` — reject (style): the two are different texts, a public line and a record line, as on main
