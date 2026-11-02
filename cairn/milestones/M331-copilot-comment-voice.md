# M331: Write Copilot comments like a colleague

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the skills post this comment on PRs that other people read
- **Branch/PR:** m331-copilot-comment-voice

## Goal

Each Copilot review's PR comment reads as a colleague wrote it, with a draft shown first in guest rounds and in `/copilot-review`.

## Scope

**In:** The comment rule in `skills/shared/copilot-review.md` §5, posting it from a file, the resolve rule, the draft chip and the hold, `skills/copilot-review/SKILL.md`, the guest arms of `/hotfix` and `/milestone-review`, README, the Unreleased CHANGELOG entries, the hand-run guards, and a D-entry for the changed decisions and the module budget.

**Out:** Thread replies stay barred (D-212). The `copilot:` report lines keep their shape. An owner-mode round shows no draft, at the user's answer. `skills/shared/tracking-rules.md` does not change, since its stop list already covers an outward action the question set did not cover.

## Acceptance criteria

- [ ] AC1: `skills/shared/copilot-review.md` §5 tells the session to write the comment as ordinary sentences, as the PR's author would write to a reviewer, opening with the review's `url` as a markdown link. It says that in guest mode host matching still governs tone and length. A search of the "**The comment.**" paragraph, with its line breaks removed, for `first line`, `one line per note`, and `Each line` returns no match.
- [ ] AC2: §5 still requires the comment to give the outcome of every note of the review, thread or body item: the fix's short sha, why the note is not a problem, or that it is left for a later change. It still says that the comment never thanks Copilot, asks no question, and in guest mode carries no cairn vocabulary.
- [ ] AC3: §5 decides whether a review already has a comment by the operator comments that carry its `url`, in any position. A fresh reader given §5 and the five cases in T6 gives the expected answer for each and quotes the deciding sentence: the `url` in a markdown link, alone on a line, or mid-sentence in an operator comment means no second comment; the `url` followed by a digit, or the `url` in another author's comment, means the comment posts.
- [ ] AC4: A fresh reader given only §5 and the three note sets in T6 drafts one comment for each. Each draft holds the review's `url` in a markdown link, has no line that holds only a URL, has no line that opens with a path and line number, and gives every note's outcome in a sentence with a subject and a verb.
- [ ] AC5: §5 posts the comment with `gh pr comment --body-file`, so an apostrophe in a sentence cannot break the command. §5 and `skills/copilot-review/SKILL.md` step 7 resolve each unresolved Copilot thread tied to that review by §5's review tie, once its comment posts. A search of `skills/shared/copilot-review.md`, `skills/copilot-review/SKILL.md`, and `README.md`, with line breaks removed, for `--body '` and `comment names` returns no match.
- [ ] AC6: In a guest-mode round and in `/copilot-review`, the session shows each draft comment in a chip before it posts, with one question per draft and four per chip. A draft of at most 800 characters sits in the question text, and a longer one is cited by the path of its temp file. The options are to post it and to hold it, and the user can type an edit, which posts as typed once the session restores a dropped review link. A hold posts no comment and resolves no thread of that review, §6 reports `copilot: <url> — held`, and the close block fences `/copilot-review <N>`. In `/milestone-review` step 8 and `/hotfix`'s guest close, the status and close stay the same on a hold. An owner-mode round posts with no question, and §1's opt-in sentence states both arms.
- [ ] AC7: The `/copilot-review` description and step 6, the README's two passages on the comment, and the Unreleased section of `CHANGELOG.md` describe the new comment, the draft chip, and the hold. The sentences "The user's request gives this skill permission for its pushes, its comments, and its resolves" and "The line is your permission for these pushes, comments, and resolves" no longer claim that a comment needs no question. A search of `README.md`, the Unreleased section of `CHANGELOG.md`, and each file under `skills` outside `skills/tests`, with line breaks removed, for `one line per note`, `one line for each note`, `A fix's line`, `A line names`, and `The lines cover` returns no match.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2, T6
- AC4 → T2, T6
- AC5 → T1, T2, T3
- AC6 → T1, T2, T3, T4
- AC7 → T3, T5

## Tasks

- [x] T1: Update the guards first. In `skills/tests/test_copilot_review_round.py`, change the `TestOneComment` pins for the old first-line and "comment names" sentences, and add tests for `--body-file`, the markdown link, the guest and `/copilot-review` draft chip, and the hold. Change the matching `Mutation` entries in `skills/tests/test_mutation_harness.py` (lines 4281 and 4287) and add entries for the new tests. See them red.
- [x] T2: Rewrite §5's comment paragraph with one short example of the new form. Allow prose up to three notes and a short list of full sentences for four or more. Give a note settled on an earlier pass the outcome its `copilot:` line records. Post from a temp file under the system temp directory with `--body-file`. State the resolve by the review tie. Add the draft chip, the edit rule, and the hold to §5, narrow §1's opt-in sentence, and add a hold to §6's held parenthetical and the `/copilot-review <N>` fence to its report.
- [x] T3: Update `skills/copilot-review/SKILL.md`: the description, the permission sentence, step 6 with the chip and the hold, step 7's resolve, and step 8's close for a held review, including that a rerun disposes of the open threads again and finds pushed fixes from the branch.
- [x] T4: Update the guest round text in `skills/milestone-review/SKILL.md` step 8 and `skills/hotfix/SKILL.md`'s guest close to name the chip and the hold, and to say that a hold changes neither the `blocked` status nor the rest of the close. Check that step 7's owner read still reads true.
- [x] T5: Update the two README passages (the command table row and the Copilot bullet) and edit the two Unreleased CHANGELOG entries in place, since neither has shipped in a release.
- [ ] T6: Append the D-entry, superseding D-212's "the review's URL, then one line per note", D-187's "first line" clause, and the opt-in's "with no question" in D-152's guest and module terms. Reset the module's header budget in that entry at the new size plus stated headroom, as D-188 did, with no rule dropped. Run the reader passes from fresh subagents with these cases, and rerun a case after any later edit to a sentence it relies on.
  Dedupe cases (AC3), for review `R` = `https://github.com/o/r/pull/9#pullrequestreview-100`: (a) operator comment `On [Copilot's review](R): fixed in abc1234.`; (b) operator comment with `R` alone on its first line; (c) operator comment `See R for the notes.`; (d) operator comment that holds `R` followed by `7`; (e) another author's comment that holds `R`.
  Note set 1 (PR 735): one thread at `R/utils_standardize_center.R:319`, fixed in 09b1c08e, a single `TRUE` or `FALSE` now applies to every column.
  Note set 2 (PR 729): zero-length results from a function in `center`, kept as designed, the help now says so, fixed in e6dae14b; all-missing groups, the same on main, left for a later change.
  Note set 3 (made up): six notes on one review: three threads fixed in abc1234, one rejected because the caller already checks the type, one outdated thread left for a later change, and one body note with no anchor rejected because the file is generated.

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

## Decisions

## Review
