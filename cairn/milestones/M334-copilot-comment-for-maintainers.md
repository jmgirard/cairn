# M334: Say only what maintainers need in a Copilot comment

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the skill text decides what adopters' sessions post under their accounts
- **Branch/PR:** m334-copilot-comment-for-maintainers, https://github.com/jmgirard/cairn/pull/349

## Goal

A Copilot comment says only what the maintainers need to know, written to them, and goes out only when they need something.

## Scope

**In:**
- `skills/shared/copilot-review.md` §5: replace the rules on naming notes, shas, and reasons with a reader's test, add the path with no comment, and adapt the draft chip and the post.
- `skills/copilot-review/SKILL.md`, `skills/milestone-review/SKILL.md`, and `skills/hotfix/SKILL.md`: their Copilot comment text follows §5.
- `README.md`, `cairn/DESIGN.md`, and `CHANGELOG.md`: state the new rule.
- The hand-run guards in `skills/tests` that pin the removed wording.
- One decision entry.

**Out:**
- A checker or scored test of prose quality: none, because this is a judgment for the writer and for the user at the chip (D-236).
- The guest limit "Reply to no bot, except the one comment per Copilot review" in `skills/shared/tracking-rules.md`, `hooks/session_context.py`, and `README.md`: it stays as a ceiling, and it reads true when no comment goes out.
- The session's own `copilot:` report lines in §6: they keep the short sha and each disposition, because that is the session's record and not text for the maintainers.
- Pointing cairn at the user's `writing-for-people` skill: adopters do not have it.
- Asking the maintainers a question in the comment: "asks no question" stands, and a question for the user goes to chat.

## Acceptance criteria

- [ ] AC1: In `skills/shared/copilot-review.md`, "The comment" paragraphs tell the session to write to the maintainers who will read the PR, in ordinary sentences, and to say only what they need to know from this review. They state the test for a sentence: would a maintainer reading the PR act differently, or be misled, without it? They say that the comment need not mention each fix or note, cite a commit, or give a reason for a note left alone. They hold no sample comment and no list of cases. With line breaks removed, those paragraphs hold none of "Name each fix", "a person reading the PR", "short sha", "gets its reason", or "one sentence saying". §6's fix-now line still ends `, fixed <short-sha>`.
- [ ] AC2: The same paragraphs state that when no sentence passes that test, under the same conditions as a comment (every note has a disposition, each fix is pushed, and no return-floor item holds the review), the session posts no comment and resolves that review's unresolved Copilot threads. They state that a review with a body finding that has no anchor stays a note with no comment, so each later run decides it again, and that `/milestone-review` reuses its `copilot:` line. §5's draft step states that in a guest-mode round and in `/copilot-review` the session shows this in a chip first, with options to resolve the threads with no comment and to hold, and that a typed comment posts as typed once the session restores a dropped review link. An owner-mode round asks no question. A hold posts nothing and resolves nothing.
- [ ] AC3: §5 still states that a comment that posts carries the review's `url` as a markdown link, is in ordinary sentences, passes the one-read test first, matches the host's tone and length in guest mode after that test, never thanks Copilot, asks no question, and in guest mode carries no cairn vocabulary. It still states that a review whose `url` an operator comment already carries gets no second comment, and that a comment posts with `--body-file` from a temp file. §6 still reports each note's disposition to the user.
- [ ] AC4: Each of these states the new rule, and none says that every review with a note gets a comment: `skills/copilot-review/SKILL.md`'s description and its comment and resolve steps; the Copilot comment text in `skills/milestone-review/SKILL.md` and `skills/hotfix/SKILL.md`; `README.md`'s `/copilot-review` table row and Copilot round section; `cairn/DESIGN.md`'s `copilot-review` line; and a new entry in `CHANGELOG.md`'s Unreleased section. `git grep -nE "one (PR )?comment|has a note" -- skills README.md cairn/DESIGN.md hooks` is the sweep, and the Review section gives each hit's disposition.
- [ ] AC5: `cairn/DECISIONS.md` gains one entry that supersedes D-236's clauses on naming each fix and any other note, D-212's "one public record" and "its outcome lives in the review's comment", and D-187's comment for the review summary where they require a comment. It states that §6 is then the only record of an unmentioned note, and that outside `/milestone-review` that record lasts only in chat. It names what would falsify the rule.
- [ ] AC6: `wc -l -c skills/shared/copilot-review.md` reads under the module's stated 200 lines and 12,000 bytes, with no rule cut except those this scope removes.
- [ ] AC7: The profile's `verify` slot passes on the branch head, and `python3 -m unittest discover -s skills/tests` exits 0.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T1, T2
- AC4 → T3, T4
- AC5 → T5
- AC6 → T1, T2
- AC7 → T6

## Tasks

- [x] T1: In `skills/shared/copilot-review.md`, rewrite the "The comment" paragraphs per AC1 and AC3. Remove the naming, sha, and reason rules and the "one sentence" line. State no sample and no list of cases.
- [x] T2: Add the no-comment path per AC2 to "The comment", "The draft", and "The post". Read `wc -l -c` afterward, and cut wording rather than rules if the budget is close.
- [x] T3: Update the comment text in `skills/copilot-review/SKILL.md`, `skills/milestone-review/SKILL.md`, and `skills/hotfix/SKILL.md`.
- [x] T4: Update `README.md` and `cairn/DESIGN.md`, add the `CHANGELOG.md` entry, and run the AC4 sweep.
- [x] T5: Append the decision entry per AC5.
- [x] T6: In `skills/tests/test_copilot_review_round.py` and `skills/tests/test_mutation_harness.py`, replace the pins on the removed wording, and pin the test sentence and the no-comment path. Run `verify` and `skills/tests`.

## Work log

- 2026-11-05: created by /milestone-plan. Source: the user's objections to Copilot comment drafts on easystats/report#629, with their request to plan the change; they asked to keep the sha only if tracking needs it.
- 2026-11-05: tier check: milestone — changes what running skills post and holds a design decision on when a comment goes out.
- 2026-11-05: sha finding: nothing reads a sha in the comment. A later run reads only the review's `url` (D-236), and §6's report line keeps the sha for the session's record, so the comment's sha rule goes.
- 2026-11-05: idea vet: flaw, none. Gap, "what the maintainers need to know" has no test; reading taken: the audit's test, would a maintainer act differently or be misled without the sentence. Gap, a body finding with no anchor has no thread to clear; reading taken: it stays a note and each later run decides it again, told to the user at the set.
- 2026-11-05: lessons used: 2026-11-02 (M332), an example becomes the template, so AC1 states a reader's test and no sample; 2026-11-02 (M331, used M332), several surfaces owe a check on each, so AC4 names each surface.
- 2026-11-05: collision check: D-212 said "the user wants one public record of which notes were real", and the user chose this change at the set, so the new entry supersedes it. D-236's "It names each fix and any other note a person reading the PR could ask about" is the wording this replaces. D-235's chip stands. M331 and M332 shipped the earlier forms, and this extends them.
- 2026-11-05: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-11-05: question set: post no comment when the maintainers need nothing, or always one comment — the user chose no comment.
- 2026-11-05: plan chose no comment over one always-posted sentence because that sentence is the report voice the user rejected; falsified by a maintainer asking why a resolved Copilot thread went unexplained.
- 2026-11-05: plan chose to leave a body-only finding open to re-decision over forcing a comment for it, because D-153 keeps no record and forcing one weakens the goal; falsified by a user who is shown the same finding across runs and calls it noise.
- 2026-11-05: criteria audit (full): an Opus reader returned 9 findings. Fixed: the body-finding gap (AC2 and the set), a missing decision entry (new AC5), a sweep that missed `milestone-review`, `hotfix`, and the guest limit (AC4 and Out), ordering conditions for the no-comment path (AC2), AC5's instrument clause moved to T6, a reader's test and no sample (AC1), the `one sentence` line and the chip with no draft (AC1, AC2), the one-read and host clauses (AC3), a line-wrap gap in AC1's check, and the unstated budget (new AC6). Answered with no change: a partial stop, since a rerun re-disposes the remaining threads and git history prevents a second fix.
- 2026-11-05: remainder ledger: every part of the request is in this milestone. Nothing is deferred or dropped.
- 2026-11-05: T1-T6 done in one commit because the tasks edit the same paragraphs and the guards pin them together. The module reads 199 lines and 11,966 bytes after rewrapping my own paragraphs, with no rule cut outside this scope. `verify` is green, and skills/tests pass 1014 tests.
- 2026-11-05: lint hits in the touched files are older text that this milestone does not change; I fixed the two long sentences I wrote and left the rest.
- 2026-11-05: claim audit: about 60 claims read, 8 corrected — `skills/shared/copilot-review.md`, `skills/copilot-review/SKILL.md`, `README.md`, `CHANGELOG.md`, `skills/tests/test_copilot_review_round.py`; the same reader re-read the corrected claims and they hold.
- 2026-11-05: left the guest limit "the one comment per Copilot review with a note" unchanged in the rulebook, the session hook, and the README, as the Out section says; it stays true as a ceiling.
- 2026-11-05: to fit the budget, shortened the module's budget line (the reset reasons are in D-188 and D-235) and rewrapped my own paragraphs; no rule was cut outside this scope.

## Decisions

## Review
