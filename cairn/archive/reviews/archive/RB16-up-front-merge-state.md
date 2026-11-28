# RB16: When may review skip the merge question under an up-front approval? (M203)

- **Date:** 2026-10-03
- **Output required:** write findings to `cairn/reviews/RR16-up-front-merge-state.md`
- **Binding criteria:** not requested

You are performing an independent expert review. This brief is fully
self-contained. Do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

cairn is a Claude Code plugin. It tracks a repo's work as milestones in
markdown files under `cairn/`, and it runs each milestone through three
skills: `/milestone-plan`, `/milestone-implement`, and `/milestone-review`.
The skills are prose instructions an AI agent follows. A "run" is one plan
question set, then implement and review, ending at the merge question, an
`AskUserQuestion` chip where the user approves the merge (D-144).

Milestone M203 lets the user approve a milestone's merge up front, in the
plan question set. Review then merges with no merge question, but only
while the plan's promise ships unchanged and no "route-back case" applies.
Each route-back case sends the run to the merge question. An earlier Fable
review, RR15, shaped this design. It recommended the route-back cases and a
merge-guard hook that reads the milestone's `Merge approval:` slot from the
default branch. The user accepted that, and IP1 and D-145 now record it.

Review then returned M203 three times, and each pass found new defects in
when the skip may happen. Pass 1 found that a run ending at a later stop
dropped the list of findings an up-front merge must show the user. Pass 2
found 25 findings. Among them, a red-CI fix could re-enter the up-front
check and merge with no question, and the guard's slot read could time out
open. Pass 3 found 20 more. Step 8 keys on any up-front line rather than the
newest approval line, so a run can loop. A default branch that moves before
a resume can lead to an unattended merge of an unverified tree. A `spawned:`
line has no pass id, so "this pass" cannot be read on resume. Most defects
sit in resume and re-entry paths, and in work-log line shapes that one part
of the skill writes and another reads. The milestone hit cairn's thrash rule
(third defect return), and the user chose this escalation over the agent's
recommendation, a "one-pass" narrowing (see question 3).

This is the second escalation of the up-front approval mechanism (RB15 was
the first), so removal of the mechanism is among the options (question 4).

## Materials

Read in this order. Line numbers are as of commit `1ce9749` on branch
`m203-merge-approval-up-front`; use `git show 1ce9749:<path>` if your
working tree differs.

1. `cairn/milestones/M203-merge-approval-up-front.md`: Goal, Scope,
   Acceptance criteria (AC3 is the skip), Tasks, the whole Work log, the
   Decisions section (RR15's answers), and the whole Review section (passes
   1 to 3, every finding with its lens, rank, and disposition).
2. `skills/milestone-review/SKILL.md`: "Resume routing" route (c) (about
   lines 79-92), step 5's finding-line and `spawned:` shapes (about lines
   318-335), step 7 "Up-front approval first" (about lines 386-428), the
   PR-conversation read (about lines 460-500), step 8 and its "Up-front arm"
   (about lines 520-605), and step 10's end-of-run list (about lines
   740-760).
3. `skills/shared/tracking-rules.md`: the approval bullets of "Git and
   approval model" (about lines 240-270) and the close-block paragraph of
   "Question gates and phase closes" (about lines 410-425).
4. `hooks/merge_guard.py` (whole file, about 260 lines) and
   `hooks/cairn_common.py` functions `marker_up_front_milestone`,
   `slot_is_up_front`, and `default_branch_merge_slot` (about lines
   305-400). Tests: `hooks/tests/test_hooks.py` class
   `TestMergeGuardUpFront`. Run them with
   `python3 -m unittest discover -s hooks/tests -k UpFront`.
5. `cairn/DECISIONS.md`: D-043, D-138, D-144, D-145 (find each with
   `grep -n '^### D-' cairn/DECISIONS.md`; read each whole).
6. `cairn/reviews/archive/RR15-merge-approval-up-front.md` (questions 2, 4,
   5, 6 and Recommendations).
7. `skills/milestone-plan/SKILL.md` step 3's merge-approval question (search
   for "merge approval, with one answer").

Rough size: about 1,300 lines.

## Questions

1. **Root cause.** Why does each review pass find new defects in the skip?
   Name the state the skip depends on (for example: which approval line is
   newest, whether a push happened after the PR opened, which review pass
   wrote which line, whether the default branch moved), where each piece of
   state lives today (work-log line, Review line, git, GitHub), and which
   readers and writers of it disagree. Say whether the design as written is
   a closed set of states and transitions that a reviewer could check, or
   an open one.

2. **A verifiable full design.** Is there a design for the skip, covering
   resumes, red CI, PR comments, and re-entry after a decline, that is small
   enough to verify by reading? If yes, state it as a short list of state
   variables, where each is recorded, and the rule that decides "may skip".
   Say whether that rule could be computed by a script from the files and
   `gh` output (so the agent runs one command rather than following prose),
   and what that script would read. If no, say why.

3. **The one-pass narrowing.** The agent recommended narrowing AC3 so the
   merge question is skipped only when review runs from its start to the
   merge in one uninterrupted pass. Any stop, resume, return, red CI, late
   push, or PR conversation item asks the question. Does this remove the
   pass-3 defects (Review section, pass 3, diff-bug #1 to #3 and blame
   #4)? What defects would remain? Is "one uninterrupted pass" itself
   checkable from the files, and how?

4. **Removal.** Weigh dropping the up-front path: every run keeps ending at
   the merge question, and IP1 returns to its prior text. What of M203's
   branch work is worth keeping without the skip: the `Merge approval:`
   slot, the guard's slot read, the end-of-run list, the review line shapes
   (`spawned:`, `step-7 decline:`, lens and rank on finding lines), or the
   stale-prose fixes? What would removal cost, given D-138's serial CI wait
   (the CI wait starts only after the user answers the merge question)?

5. **Recommendation.** Choose among 2, 3, and 4, with the evidence that
   decides it. State what happens to M203's acceptance criteria under your
   choice (which hold, which narrow, which drop), and what happens to the
   pass-3 findings marked "fix now".

6. **PR conversation items.** The branch routes an up-front run back on any
   PR conversation item, bots included. Blame-history pass 3 #2 says this
   widens D-138 and M177's grading, and a repo with a bot that always
   comments would never merge unattended. Should only non-bot items route
   back, or all of them? Does reading the conversation after CI on a fresh
   PR need a D-entry against D-138?

7. **Default-branch resolution in the guard.** The guard reads
   `refs/remotes/<base>/HEAD`, else `<base>/main`, else `<base>/master`, and
   never calls the network (the hook times out at 15 seconds). Blame-history
   pass 3 #3 says the main/master fallback guesses, against the rulebook's
   rule never to hardcode `main`. Should the guard deny when `<base>/HEAD`
   is unset (telling the user to run `git remote set-head origin -a`), keep
   the fallback, or something else?

## Constraints

- IP1 changes only by explicit user decision plus a D-entry
  (`cairn/DESIGN.md`, "Design Principles"). D-145 states that removing or
  narrowing a route-back case changes IP1. A narrowing of when the skip
  happens (more cases ask the user) is not a narrowing of a route-back case.
- The guards are drift defense in one operator's session, not an
  adversarial boundary (D-043). RR15 rejected stronger marker binding on
  that ground. Do not recommend signed tokens or similar.
- The maintainer's stated preference: rigor proportional to the stakes, and
  descoping over hardening when a checker spirals. Weigh the cost of each
  option in plain terms.
- History records (`DECISIONS.md`, work logs, archives) are append-only
  (IP4). Recommend superseding entries, never edits.
- Flag any disagreement with a constraint explicitly.

## Output format

In `RR16-up-front-merge-state.md`: answer each question by number with your
reasoning and evidence; list any additional findings separately under
"Beyond the brief"; end with concrete recommendations, each marked apply /
consider / reject-with-reason. Your report is advisory: emit a
`## Binding criteria` section ONLY if this brief's header slot says
`requested`. It says `not requested`.
