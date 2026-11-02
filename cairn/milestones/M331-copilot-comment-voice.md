# M331: Write Copilot comments like a colleague

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the skills post this comment on PRs that other people read
- **Branch/PR:** m331-copilot-comment-voice https://github.com/jmgirard/cairn/pull/346

## Goal

Each Copilot review's PR comment reads as a colleague wrote it, with a draft shown first in guest rounds and in `/copilot-review`.

## Scope

**In:** The comment rule in `skills/shared/copilot-review.md` §5, posting it from a file, the resolve rule, the draft chip and the hold, `skills/copilot-review/SKILL.md`, the guest arms of `/hotfix` and `/milestone-review`, README, the Unreleased CHANGELOG entries, the hand-run guards, and a D-entry for the changed decisions and the module budget.

**Out:** Thread replies stay barred (D-212). The `copilot:` report lines keep their shape. An owner-mode round shows no draft, at the user's answer. `skills/shared/tracking-rules.md` does not change, since its stop list already covers an outward action the question set did not cover.

## Acceptance criteria

- [x] AC1: `skills/shared/copilot-review.md` §5 tells the session to write the comment as ordinary sentences, as the PR's author would write to a reviewer, opening with the review's `url` as a markdown link. It says that in guest mode host matching still governs tone and length. A search of the "**The comment.**" paragraph, with its line breaks removed, for `first line`, `one line per note`, and `Each line` returns no match.
- [x] AC2: §5 still requires the comment to give the outcome of every note of the review, thread or body item: the fix's short sha, why the note is not a problem, or that it is left for a later change. It still says that the comment never thanks Copilot, asks no question, and in guest mode carries no cairn vocabulary.
- [x] AC3: §5 decides whether a review already has a comment by the operator comments that carry its `url`, in any position. A fresh reader given §5 and the five cases in T6 gives the expected answer for each and quotes the deciding sentence: the `url` in a markdown link, alone on a line, or mid-sentence in an operator comment means no second comment; the `url` followed by a digit, or the `url` in another author's comment, means the comment posts.
- [x] AC4: A fresh reader given only §5 and the three note sets in T6 drafts one comment for each. Each draft holds the review's `url` in a markdown link, has no line that holds only a URL, has no line that opens with a path and line number, and gives every note's outcome in a sentence with a subject and a verb.
- [x] AC5: §5 posts the comment with `gh pr comment --body-file`, so an apostrophe in a sentence cannot break the command. §5 and `skills/copilot-review/SKILL.md` step 7 resolve each unresolved Copilot thread tied to that review by §5's review tie, once its comment posts. A search of `skills/shared/copilot-review.md`, `skills/copilot-review/SKILL.md`, and `README.md`, with line breaks removed, for `--body '` and `comment names` returns no match.
- [x] AC6: In a guest-mode round and in `/copilot-review`, the session shows each draft comment in a chip before it posts, with one question per draft and four per chip. A draft of at most 800 characters sits in the question text, and a longer one is cited by the path of its temp file. The options are to post it and to hold it, and the user can type an edit, which posts as typed once the session restores a dropped review link. A hold posts no comment and resolves no thread of that review, §6 reports `copilot: <url> — held`, and the close block fences `/copilot-review <N>`. In `/milestone-review` step 8 and `/hotfix`'s guest close, the status and close stay the same on a hold. An owner-mode round posts with no question, and §1's opt-in sentence states both arms.
- [x] AC7: The `/copilot-review` description and step 6, the README's two passages on the comment, and the Unreleased section of `CHANGELOG.md` describe the new comment, the draft chip, and the hold. The sentences "The user's request gives this skill permission for its pushes, its comments, and its resolves" and "The line is your permission for these pushes, comments, and resolves" no longer claim that a comment needs no question. A search of `README.md`, the Unreleased section of `CHANGELOG.md`, and each file under `skills` outside `skills/tests`, with line breaks removed, for `one line per note`, `one line for each note`, `A fix's line`, `A line names`, and `The lines cover` returns no match.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2, T6
- AC4 → T2, T6
- AC5 → T1, T2, T3
- AC6 → T1, T2, T3, T4
- AC7 → T3, T5, T7

## Tasks

- [x] T1: Update the guards first. In `skills/tests/test_copilot_review_round.py`, change the `TestOneComment` pins for the old first-line and "comment names" sentences, and add tests for `--body-file`, the markdown link, the guest and `/copilot-review` draft chip, and the hold. Change the matching `Mutation` entries in `skills/tests/test_mutation_harness.py` (lines 4281 and 4287) and add entries for the new tests. See them red.
- [x] T2: Rewrite §5's comment paragraph with one short example of the new form. Allow prose up to three notes and a short list of full sentences for four or more. Give a note settled on an earlier pass the outcome its `copilot:` line records. Post from a temp file under the system temp directory with `--body-file`. State the resolve by the review tie. Add the draft chip, the edit rule, and the hold to §5, narrow §1's opt-in sentence, and add a hold to §6's held parenthetical and the `/copilot-review <N>` fence to its report.
- [x] T3: Update `skills/copilot-review/SKILL.md`: the description, the permission sentence, step 6 with the chip and the hold, step 7's resolve, and step 8's close for a held review, including that a rerun disposes of the open threads again and finds pushed fixes from the branch.
- [x] T4: Update the guest round text in `skills/milestone-review/SKILL.md` step 8 and `skills/hotfix/SKILL.md`'s guest close to name the chip and the hold, and to say that a hold changes neither the `blocked` status nor the rest of the close. Check that step 7's owner read still reads true.
- [x] T5: Update the two README passages (the command table row and the Copilot bullet) and edit the two Unreleased CHANGELOG entries in place, since neither has shipped in a release.
- [x] T6: Append the D-entry, superseding D-212's "the review's URL, then one line per note", D-187's "first line" clause, and the opt-in's "with no question" in D-152's guest and module terms. Reset the module's header budget in that entry at the new size plus stated headroom, as D-188 did, with no rule dropped. Run the reader passes from fresh subagents with these cases, and rerun a case after any later edit to a sentence it relies on.
  Dedupe cases (AC3), for review `R` = `https://github.com/o/r/pull/9#pullrequestreview-100`: (a) operator comment `On [Copilot's review](R): fixed in abc1234.`; (b) operator comment with `R` alone on its first line; (c) operator comment `See R for the notes.`; (d) operator comment that holds `R` followed by `7`; (e) another author's comment that holds `R`.
  Note set 1 (PR 735): one thread at `R/utils_standardize_center.R:319`, fixed in 09b1c08e, a single `TRUE` or `FALSE` now applies to every column.
  Note set 2 (PR 729): zero-length results from a function in `center`, kept as designed, the help now says so, fixed in e6dae14b; all-missing groups, the same on main, left for a later change.
  Note set 3 (made up): six notes on one review: three threads fixed in abc1234, one rejected because the caller already checks the type, one outdated thread left for a later change, and one body note with no anchor rejected because the file is generated.

- [x] T7: Fix review return 1: describe the hold in the `/copilot-review` description and step 6, then fix each other fix-now finding of the Review section's pass 1, with guards.

## Work log

- 2026-11-02: created by /milestone-plan.
- 2026-11-02: tier check: milestone — it changes what the skills post on PRs and holds a design choice, and the row asks the user how a draft step fits.
- 2026-11-02: idea vet: no flaw; gap: a comment in sentences may not name a path, so "resolve each thread the comment names" fails, reading taken: resolve by the review tie; gap: first person or impersonal, reading taken: first person, as in datawizard#738, shown at the question set; gap: many notes, reading taken: prose up to three, a list of sentences from four.
- 2026-11-02: lessons used: 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-22 (M152), 2026-11-02 (M329), 2026-11-02 (M330).
- 2026-11-02: question set: show a draft in a Copilot round — guest repos only; show a draft in `/copilot-review` — show and wait.
- 2026-11-02: collision: absorbed the candidate row "Write Copilot comments like a colleague"; D-212 and D-187 are superseded in T6, not ignored; no overlap in the open issues (0) or the open PRs (0); no checker-regress shape, since the guards only follow the changed sentences; no release shape.
- 2026-11-02: criteria audit (full): 13 findings, all taken: host matching over "the operator's voice", flattened searches and the extra old-form phrases, wider dedupe and draft cases, the review tie for resolves, the chip's length rule, the edit rule, the two false permission sentences, guard updates moved to T1 as instrument work, the zero-match wording, the held rerun's close, `--body-file` for apostrophes, the budget reset, and the guest text in `/hotfix` and `/milestone-review`.
- 2026-11-02: plan gate chose a chip in guest rounds and `/copilot-review` over a chip in every round because owner-mode runs would gain a stop before the merge question for a comment only the user reads; falsified by a user reporting a badly worded owner-mode comment that a person other than the user had to read.
- 2026-11-02: plan gate chose resetting the module budget over compressing it because M282 and M287 lost rules that way (D-188); falsified by a compression that fits with no rule lost.
- 2026-11-02: plan gate chose a temp file with `--body-file` over `--body` with escaping because ordinary sentences hold apostrophes and a failed quote posts a wrong comment; falsified by no such failure when `--body` is tried on sentences with apostrophes, double quotes, and backticks.
- 2026-11-02: T1 to T5 done and D-235 appended: guards red with 24 failures, then green after the module, skill, guest-close, README, and CHANGELOG edits; the module is 185 lines and 11,029 bytes, under the new budget; T6's reader passes are next. The unrelated `cairn-probe.log` and `tsconfig.json` stay unstaged. The simple-english lint hook flags hundreds of older sentences in README, CHANGELOG, and the skills; only new sentences were fixed, because rewriting the rest is outside this scope.
- 2026-11-02: an edit typed at the chip posts as typed, with only a dropped review link restored, because the user may drop a note on purpose and the link keeps a rerun from posting twice; `/copilot-review` still reports each note's `copilot:` line.
- 2026-11-02: T6 reader passes on 7d282f6d (fresh Opus, §5 only): dedupe, 5 of 5 answered as expected with the deciding sentence quoted and none unsettled; drafting, 3 of 3 note sets hold the markdown link, no URL-only line, no line opening with a path, and each outcome in a full sentence, with the six-note set as a list of sentences. Claim audit and `claude plugin test` are running at this checkpoint.
- 2026-11-02: claim audit: 31 claims read, 6 corrected — skills/shared/copilot-review.md, skills/copilot-review/SKILL.md, skills/hotfix/SKILL.md, skills/milestone-review/SKILL.md (a hold's close adds a fence, the temp file comes before the chip, the review id is defined, and a held review's command comes first); all six re-read ok. The reader cases were not rerun, because the corrections left the dedupe sentence and the drafting rule unchanged.
- 2026-11-02: verify: the two Python suites and both manifest validates ran after the corrections; `claude plugin test` passed 2466 tests on the commit before them, which changed no file under `hooks/`.
- 2026-11-02: review return 1: AC7 fails because the `/copilot-review` description and step 6 do not describe the hold (diff-bug #12); the return also fixes each other fix-now finding in the Review section's pass 1.
- 2026-11-02: T7 done: the description and step 6 name the hold; a typed instruction changes the draft; the post re-reads operator comments and a failed post resolves nothing; a rerun reads the temp file and `git log` and makes no second fix; the temp path names `tempfile.gettempdir()`; README says the rerun works while the PR is open; guards and mutation entries added. The fixes passed D-235's figures, so the header budget is under 200 lines and 12,000 bytes, a figure D-235 does not state.

## Decisions

## Review

### Pass 1 (head 744a948f)

- AC1 evidence: flattened search of §5's comment paragraph finds none of `first line`, `one line per note`, `Each line`, and finds the ordinary-sentences, host-matching, and markdown-link sentences.
- AC2 evidence: the same search finds the every-note outcome sentence and the no-thanks, no-question, no-cairn-vocabulary sentence.
- AC3 evidence: a fresh Opus reader given §5 and the five cases answered no second comment for (a), (b), (c) and comment posts for (d), (e), quoting the deciding sentence, with none unsettled.
- AC4 evidence: a fresh Opus reader drafted three comments from §5 alone. Each holds the markdown link, has no URL-only line and no line opening with a path and line number, and gives each outcome in a sentence with a subject and verb.
- AC5 evidence: flattened search of the module, the skill, and README finds no `comment names` and no `--body '`; §5 holds `gh pr comment <N> --body-file "<path>"` and the review-tie resolve, and step 7 holds the same tie.
- AC6 evidence: flattened search finds each draft-chip sentence in §5, the hold in §6 with the `/copilot-review <N>` fence, both arms in §1, the chip in step 6, and the hold sentence in `/milestone-review` step 8 and `/hotfix`'s guest close.
- AC7: not met. The search passes, with 32 files scanned and no old-form hit, but the `/copilot-review` description and step 6 do not describe the hold (diff-bug #12).
- Gate: `cairn_validate` green on 486fb134; rerun at the next pass.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: "a typed edit posts as typed" cannot tell a replacement from an instruction such as "shorten it" — fix now.
- diff-bug #2: nothing re-reads operator comments at the post, so a comment posted by hand during the chip's wait gets a second comment — fix now.
- diff-bug #3: "Then resolve" has no arm for a failed `gh pr comment`, and §6's held list omits it — fix now.
- diff-bug #4: §5's earlier-pass sentence and the rerun's "new dispositions" disagree after a guest hold — fix now, with #5.
- diff-bug #5: "finds the pushed fixes" sits only in step 8, while steps 4 to 6 run first and tell a rerun to make each fix — fix now.
- diff-bug #6: a typed edit that drops a note still resolves its thread — reject, planned change: the work log records this choice, and the user's text is the user's act.
- diff-bug #7: README's "finishes the review later" overclaims once the PR merged while held — fix now.
- diff-bug #8: a dirty tree on another branch stops a rerun that only needs to post — follow-up, "Tighten the Copilot draft step edges", parked: pre-existing step 2 behavior that stops with its cause named.
- diff-bug #9: a hand-edited long draft gets no link check, and a rerun overwrites it — follow-up, same row, parked: no documented use edits the file by hand.
- diff-bug #10: two new positive tests have no `Mutation` entry, though T1 asks for entries — fix now.
- diff-bug #11: the `TestOneComment` docstring is stale — fix now.
- diff-bug #12: step 6 and the description never mention the hold, and AC7 requires it — fix now, floor return.
- diff-bug #13: D-235's heading does not name D-152 — reject, false: D-152 holds no "with no question" text, and the heading names the sentence it narrows.
- diff-bug #14: the temp path omits `tempfile.gettempdir()` and the absolute path that `/milestone` §4 states — fix now.
- diff-bug #15: four 800-character drafts in one chip strain "never the dump" — reject, planned change: AC6 sets the limit.
- diff-bug #16: uneven line wraps — reject, style.
- blame-history #1: the rerun has no way to find pushed fixes — fix now, the same defect as diff-bug #5.
- blame-history #2: chip order against the guest close — reject, false: step 8 runs the round before the close block.
- blame-history #3: a typed edit skips the comment rules with no clause naming that — reject, planned change: D-235 records it.
- blame-history #4: second budget reset — reject, planned change: D-235 records it with the reason.
- blame-history #5: predictable temp file name — follow-up, "Tighten the Copilot draft step edges", parked: per-user temp directories on macOS, and D-155 allows the same shape for `/milestone`.
- blame-history #6: the comment shape supersedes D-212 and M314 — reject, planned change: D-235 names both.
- prior-review #1: "resolves on hold" reads as resolving — reject, false: the same sentence says the next pass finds those threads open, and the diff did not change it.
- prior-review #2: the module grows about 15 percent — reject, planned change: D-235.
- prior-review #3: a guest round now stops at a chip — reject, planned change: the user's answer, D-235.
- prior-review #4: markdown link and paragraphs replace D-212's form — reject, planned change: AC1 and D-235.
- prior-review #5: mutation entries reverse a PR #297 rejection — reject, planned change: T1 asks for them, and the registry already carries this guard.
- ripple #1: `/milestone-review` step 7 names no chip — reject, false: it cites §5, which holds the chip.
- ripple #2: the candidate row states the old form — reject, planned change: step 9 graduates it at the merge.
- ripple #3: DESIGN's "answers each review in one PR comment" — reject, false: the summary holds, and one comment posts for each review that is not held.
- ripple #4: "the first" has no clear referent in step 8 — fix now.
- Pass 1's fix-now findings: fixed c6eb86b1, except diff-bug #4 and #5 and blame-history #1, which pass 2 reworked in c90f79f2.

### Pass 2 (fixes c6eb86b1 and c90f79f2)

- AC1 evidence: on c90f79f2, flattened search of §5's comment paragraph finds none of `first line`, `one line per note`, `Each line`, and finds the ordinary-sentences, host-matching, and markdown-link sentences.
- AC2 evidence: on c90f79f2, the same search finds the every-note outcome sentence and the no-thanks, no-question, no-cairn-vocabulary sentence.
- AC3 evidence: on c6eb86b1, a fresh Opus reader given §5 and the five cases answered no second comment for (a), (b), (c) and comment posts for (d), (e), quoting the deciding sentence, with none unsettled. Later commits did not change §5.
- AC4 evidence: on c6eb86b1, a fresh Opus reader drafted three comments from §5 alone. Each holds the markdown link, has no URL-only line and no line opening with a path and line number, and gives each outcome in a sentence with a subject and verb. Later commits did not change §5.
- AC5 evidence: on c90f79f2, flattened search of the module, the skill, and README finds no `comment names` and no `--body '`; §5 holds `gh pr comment <N> --body-file "<path>"` and the review-tie resolve, and step 7 holds the same tie.
- AC6 evidence: on c90f79f2, flattened search finds each draft-chip sentence in §5, the hold in §6 with the `/copilot-review <N>` fence, both arms in §1, the chip in step 6, and the hold sentence in `/milestone-review` step 8 and `/hotfix`'s guest close.
- AC7 evidence: on c90f79f2, the description and step 6 each describe the new comment, the draft chip, and the hold; both README passages and the Unreleased CHANGELOG section do too; both old permission sentences are gone; the search over 32 files and the Unreleased section finds no old-form phrase.
- Gate: on c90f79f2, `cairn_validate` green, both Python suites exit 0, both manifest validates exit 0 with no `plugins[N].version` warning, and the CHANGELOG has the Unreleased entries. `claude plugin test` passed 2466 tests on c6eb86b1, and no later commit changes `hooks/`. Guard file and mutation harness exit 0 on the review head. Module size 193 lines and 11,513 bytes, under its header budget. No changed snapshot file.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a PR closed or a thread answered during the chip's wait is not re-read — follow-up, "Tighten the Copilot draft step edges", parked: the wait is short in documented use, and the result is an extra comment.
- diff-bug #2: "a rerun after a hold" is unobservable, so a failed post or an abandoned chip can make a second fix — fix now, fixed c90f79f2: every run reads `git log` first.
- diff-bug #3: D-235 says a rerun gives "new dispositions" — reject, false: a note kept with its pushed commit still takes a disposition.
- diff-bug #4: the temp-file read has no arm for a missing file and acts as a record — fix now, fixed c90f79f2: the read is gone.
- diff-bug #5: the guest closes put the fence after the next command, while the skill puts it first — fix now, fixed c90f79f2: first in all three.
- diff-bug #6: a Write outside the checkout can prompt, and a denied Write leaves an older file — follow-up, same row, parked: unobserved, and `/milestone` §4 has the same shape.
- diff-bug #7: a failed post reports `held` with no next command — follow-up, same row, parked: the failure is named in the report.
- diff-bug #8: a failed re-read has no arm — follow-up, same row, parked: the read is the same one §5 already ran.
- diff-bug #9: CHANGELOG's "finishes it" keeps the overclaim — fix now, fixed c90f79f2.
- diff-bug #10: D-235 states no budget figure — reject, false: the rulebook keeps derived measurements out of D-entries, and the module's header states the figure.
- diff-bug #11: the `/copilot-review` CHANGELOG entry never names the hold — reject, false: AC7 binds the section, and the Copilot round's entry names it.
- diff-bug #12: no guard pins `tempfile.gettempdir()`, the paragraph-or-list rule, or README's "while the PR is open" — follow-up, same row, parked: AC4's reader covers the rule.
- diff-bug #13: the `TestDraftChip` docstring's "one test per clause" is false — fix now, fixed c90f79f2.
- diff-bug #14: a fork head's local branch name can differ from "the head branch" — fix now, fixed c90f79f2: "the checked-out head".
- blame-history #1: the temp-file read is a stored record that D-153 rejects — fix now, fixed c90f79f2.
- blame-history #2: the temp directory can be cleared with no fallback — fix now, fixed c90f79f2: the read is gone.
- prior-review #1: the `/copilot-review <N>` fence has no `--repo` — reject, false: the skill reads `<base-repo>` itself, and other slash-command fences do the same.
- prior-review #2: "The post" names the resolve only in general terms for a review already carried — reject, false: the dedupe paragraph resolves those threads.
- ripple #1: the fence order conflict — fix now, fixed c90f79f2, the same defect as diff-bug #5.
- ripple #2: `/milestone-review` step 7 and `/hotfix`'s round name no chip — reject, false: pass 1's ripple #1 reason, since both cite §5.
- ripple #3: the candidate row states the old form — reject, planned change: step 9 graduates it at the merge.

### Copilot

- copilot: skills/tests/test_mutation_harness.py:4383 — fix now, fixed c6eb86b1
- copilot: review body — fix now, fixed c90f79f2: the `/copilot-review` command comes first after a hold
- copilot: review body — reject: §5 already limits the duplicate check to an operator comment
- Copilot level: Lite (set by GitHub's settings)
- conversation: PR comment 6584884419 by the operator answers that review in the new form; thread resolved.
