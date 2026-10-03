# RR15: Merge approval given in the plan question set (M203)

- **Date:** 2026-10-03
- **Brief:** `cairn/reviews/RB15-merge-approval-up-front.md`
- **Binding criteria:** not requested (advisory report)
- **Read:** M203 (whole file), `cairn/DESIGN.md` 190-215, the M202
  archive summary, D-138, D-144, D-127, D-043, the rulebook sections "Git
  and approval model" (219-295) and "Question gates and phase closes"
  (355-420), `skills/milestone-review/SKILL.md` Session start (29-91) and
  steps 4, 5, 7, 8, 10, `skills/milestone-plan/SKILL.md` steps 3-6,
  `skills/milestone-implement/SKILL.md` step 6, `hooks/merge_guard.py`,
  `hooks/cairn_common.py` 180-360, `hooks/tests/test_hooks.py` 1045-1110,
  `hooks/commit_guard.py` docstring, `skills/shared/templates/milestone.md`
  header.

## 1. Is a pre-diff approval "explicit user approval" in IP1's sense?

IP1 as written says "explicit user approval at a gate"
(`cairn/DESIGN.md:197-198`). It does not name the merge gate. The narrowing
to the merge question lives one layer down. The rulebook bullet reads
"Nothing reaches the default branch without the user's explicit approval at
the merge question" (`skills/shared/tracking-rules.md:240`). The guard's
docstring says "at the review gate" (`hooks/merge_guard.py:4-5`), and so
does its deny text (`hooks/merge_guard.py:140-141`). The rulebook calls
the plan question set a gate (`tracking-rules.md:359-367`). So the text of
IP1 already admits it. The question is whether the thing approved is the
thing IP1 protects.

What the user knows at the plan gate: the goal, scope, acceptance criteria
and tasks as the plan commit will carry them, previewed verbatim
(`skills/milestone-plan/SKILL.md:358-360`). Also the surface tier, the
principles touched, and the foreseen outward actions and dependency
changes (`milestone-plan/SKILL.md:142-147`).

What the user cannot know at that moment: the diff. Which findings the
reviewers raised, and how the agent disposed of each with no question to
the user (`skills/milestone-review/SKILL.md:297-314`). Any substantive
criterion or scope amendment the agent made without a stop. That is every
amendment the agent judges "wording alone, the deliverable unchanged"
(`skills/milestone-implement/SKILL.md:137-142`). How many defect returns
the run took. The CI result. The conversation of a pre-existing PR.

What the merge question gives that the up-front answer does not
(`milestone-review/SKILL.md:376-404`): the outcome stated in plain words
after the fact. Each actioned finding verbatim with its disposition and a
count per disposition. Each amendment verbatim with a count, "so no
promise changed in the run reaches the merge unseen". A diffstat and an
eyeball prompt. And the one moment of user presence that D-127(b) and the
changes-requested override rely on. It is the only place a human reads the
agent's own settlement of findings before anything ships. That settlement
is new. D-144 moved finding triage from the maintainer (D-110) to the
agent on 2026-10-03. The only run under it is M202's own review, and the
user was still at the merge question for it (24 findings, 4 rejected, 1
amendment, per the M202 archive). The up-front path removes the reader
from a mechanism that has not yet run once unread.

On the 323-to-1 figure. It measures how often the user departed from the
recommended option. Under the regime that produced it, the recommended
option was "merge" whenever review passed. So it shows that the user
agrees with a passing review almost always. It does not show that the read
is idle, for three reasons. The number was produced with the read in
place, so the agent wrote dispositions it knew the user reads. D-110's
maintainer triage was in force for most of the window. And the agent did
not yet settle findings itself. It also counts only merge questions that
were posed, so declines caught earlier by a stop are not in the
denominator. The one departure matters more than its rate. If it caught a
defect, the question's value is one catch per 323 presences, and the user
has judged that trade.

The stronger argument for M203 is not the chip but D-138. The CI wait is
serial with the approval (`tracking-rules.md:245-248`). Under the merge
question, the user must be present to answer, and then again to see the
merge land. Up-front approval is what makes an unattended run possible.

Answer: an up-front answer is explicit approval of a merge of described
work, conditional on the run's own checks. It is not approval of the code.
It is approval only of the promise as the plan commit carries it. It
satisfies IP1's letter today. It satisfies IP1's spirit on two conditions.
First, the promise the user approved must be the promise that merges
(question 2, amendments). Second, the cases where the merge question has
added information must route back to it (questions 2 and 6). Without
those, the rewrite replaces a human check with the agent's report that its
own checks passed.

## 2. Which failure modes pass all of AC3's conditions?

AC3's conditions (`cairn/milestones/M203-merge-approval-up-front.md:44-55`):
slot `up front`. CI green or the no-CI rule. Each criterion evidenced. No
finding "that the reviewers rank as real and in scope" left unfixed. No
M202 stop fired. No step-7 adder.

One wording defect first. Reviewers rank severity and filter nothing
(`milestone-review/SKILL.md:291-295`, D-078). The agent, not the
reviewers, judges real and in scope (`SKILL.md:297-299`). Read literally,
every reported finding is one the reviewers consider real. Then any reject
fails the condition, and the up-front path almost never fires. Read as the
agent's disposition, every reject passes silently. The condition must say
which it means. The analysis below reads it as the agent's disposition,
because that is the only reading under which AC3 ever applies.

**(a) Findings the implementing session rejected as false or as planned
changes.** Passes. A reject is by definition not "left unfixed". The
"planned change" ground is sound under up-front approval. The plan is the
thing the user approved, so a complaint about a planned change is a
complaint about the approval. The "false" ground is the exposed one. The
session that wrote the code refutes a fresh reader's finding. The rule's
own safeguard, refutation verified against the implementation
(`SKILL.md:300-304`), is applied by the same session. M202's data point is
0 false-rejects in 24 findings, so a condition here costs almost nothing.
New condition: a finding rejected as false that its lens ranked first
returns the run to the merge question. So does any false-reject on a
user-facing tier milestone. Every reject, with its reason, must also appear
verbatim in the close block. AC3 lists only candidate-row findings. D-144's
falsifier is "merged runs whose finding dispositions the user reverses".
Without the full list the user never sees the disposition, and the
falsifier has no detector.

**(b) Criteria amended during the run.** Passes, and must not. Implement
step 6 lets the agent change acceptance-criterion wording without a stop
when it judges the deliverable unchanged
(`milestone-implement/SKILL.md:132-142`). An amendment return from review
takes the same route (`milestone-review/SKILL.md:342-359`). The merge
question's purpose clause for amendments is explicit: "so no promise
changed in the run reaches the merge unseen" (`SKILL.md:393-396`). Under
up-front approval the user approved specific promise text. Any change to
that text is a change to what was approved, whoever judges its import. New
condition: any substantive amendment to Goal, Scope, or Acceptance criteria
after the plan commit returns the run to the merge question. It is
mechanical two ways. One: `git diff <plan-commit>..HEAD --
cairn/milestones/M<NNN>-*.md` is non-empty over the plan-owned sections.
Two: any `amendment return:` or dated amendment work-log line exists.
Minor amendments (task order, a sub-task) pass. Cost: M202 asks once, for
the AC5 amendment at implement. That is the right once.

**(c) A run that chains several milestones of one plan.** Passes per
milestone. Review step 10 chains with no new question set
(`milestone-review/SKILL.md:663-675`), and each slot was filled from the
same answer. The second milestone is built on a merged result the user has
not seen. Under the merge-question regime the second chip at least cites
the first milestone's archive summary (`SKILL.md:396-399`). Under up-front
approval both are invisible until the close block. The residual risk is
acceptable on two conditions. The slot is answered per milestone
(question 3), so the user can set a user-facing or IP-touching later
milestone to `at the end` while an internal one runs through. And the
close block that ends the chain names every PR merged and every
disposition of each. No further condition.

**(d) A scope narrowed by the agent.** Partly covered already. The thrash
rule's descope is a chip (`SKILL.md:196-206`). A narrowing that drops
something the user asked for is implement step 6's stop. The gap is the
narrowing the agent judges not to drop anything the user asked for. The
return-adjacent direction rule steers toward exactly that
(`milestone-implement/SKILL.md:145-151`: the agent "narrows or holds the
criteria set"). AC3's "each criterion has passing evidence" is then
satisfied by the narrowed set. This collapses into (b). A Scope or
criteria change after the plan commit is an amendment, and the amendment
condition catches it. No separate condition.

**(e) A defect return the run fixed on its own.** Passes. The fix goes back
through implement and then steps 3-5 again, with fresh evidence and fresh
reviewers (`milestone-review/SKILL.md:178-182`). The third return is a
stop (`SKILL.md:196-199`). The merge question did not list returns anyway.
Its added value here was the diff, which the user rarely read. The
residual risk is acceptable for one return. Consider asking at the second
return under up-front approval, one earlier than the thrash stop. Two
failures of the same promise with no human look is where the unattended
premise is thinnest, and the count is already in the work log.

Two modes the brief did not list also pass.

**(f) A degraded review.** D-127(b) sends a session that cannot spawn
fresh readers to "the pending gate — for review, the merge-approval chip".
D-127(c) permits an author-inline run only as a user-accepted logged
deviation. The stop list carries this case only as "the user's request in
so many words for a freshness-mandated reader"
(`tracking-rules.md:377-378`). That depends on the session stopping rather
than degrading silently, the very failure D-127 records as observed. New
condition, mechanical: the Review section must record the spawned reviewer
lenses. A Review section with no spawn record returns the run to the merge
question.

**(g) A diff that changes the gates themselves.** In this repo a branch can
rewrite `hooks/merge_guard.py`, `hooks/hooks.json`, review steps 7-8, or
the rulebook's approval model, and merge with no human look. The same
holds for a milestone whose `Principles touched:` names an IP. The
plan-gate decision is the explicit user decision DESIGN.md requires
(`DESIGN.md:192-193`), but the final IP text and D-entry are what ship.
New condition: `Principles touched:` naming any IP returns the run to the
merge question. For the plugin repo, a diff touching `hooks/` or the
approval text of the review skill or rulebook does the same. Both are rare
and cheap.

## 3. Bind the approval to one plan, one milestone, or a named set?

Bind it per milestone. Let the question answer for several at once.

Reasons. The slot already lives in each milestone's header (AC2), so
per-milestone is where the record is anyway. Milestones of one plan differ
in surface tier, because plan step 2 classifies each. They differ in
whether they touch a principle. The user's willingness to merge unseen
must track that. M202 and M203 were planned in one question set. A
per-plan answer given for M202 then carries an IP rewrite through with no
look. Later milestones of a chain rest on merges the user has not seen
(question 2c). So the user needs a way to let the first run through and
hold the last. A "named set" is this same thing posed as a multi-select.
There is no third model.

Concretely: when the plan creates one milestone, the question is one
option pair. When it creates several, the recommended option names the ids
it covers, and the alternatives let the user hold any of them `at the
end`. The user's 2026-10-03 decision, "one approval for each plan", is kept
in the sense that matters. The approval is given once, at that plan's gate,
and never stands for a later plan. A re-cut via `/milestone-plan` creates a
new id and a new plan commit, so it asks again. The slot is never inherited
across a re-cut.

One further binding: the approval binds the run the plan started. A
milestone that is stopped and resumed by a typed command keeps its slot,
because the user is present and typed it. A milestone that went `blocked`
and comes back weeks later must ask again. The slot's date makes that
checkable. Consider.

## 4. Does an agent-written marker weaken what `merge_guard` enforces?

Mechanically, no. The marker has always been agent-written. Step 8 has the
agent write `cairn/.merge-approved` after the chip is answered
(`milestone-review/SKILL.md:489-498`). The guard checks presence and the
PR number only (`hooks/merge_guard.py:137-198`,
`cairn_common.py:184,294-307`). It has never checked that a chip was
answered. The regex `for\s+PR\s*#(\d+)` already accepts `M203 approved up
front 2026-10-03 for PR #12`. So AC4's allow test passes against today's
code. It is a regression guard, not a behavior change. What M203 weakens is
the conduct link, not the hook. Today the marker is written in the turn
after a user act. Under M203 it is written in a turn with none, on the
agent's reading of a slot the agent also wrote.

The on-disk evidence that ties the marker to the user's answer is the
`Merge approval:` slot as committed in the plan commit on the default
branch (`milestone-plan/SKILL.md:358-365`). It is good evidence for three
reasons. It was previewed verbatim before the commit. It predates the
branch, which is cut from the default branch afterward. And it sits on a
branch the agent cannot rewrite (`force_push_guard`). The `question set:`
work-log line (`milestone-plan/SKILL.md:161-164`) is the second copy. I
recommend that the marker and the `step-7 approval:` line both cite the
plan commit: `M<NNN> approved up front YYYY-MM-DD per plan <sha> for PR
#<N>`.

Must the guard check it? Yes, the cheap half. When the marker body carries
`up front`, the guard reads the milestone file from the base remote's
default branch: `git show <base>/<default>:cairn/milestones/M<NNN>-*.md`,
the file found with `git ls-tree`. `cairn_common` already has `git()`,
`base_remote()`, and the default-branch recipe. The guard denies unless
that copy's `Merge approval:` slot reads `up front`. A legacy marker
without the token is untouched. This catches the two drift failures worth
catching. One: a slot written on the branch but never on the default
branch. Two: a marker claiming up-front approval for a milestone whose
slot says `at the end`.

It does not catch an agent that commits a slot change to the default
branch as a docs-only tracking commit. `commit_guard` lets such a commit
through silently (`hooks/commit_guard.py:15-16`). Closing that needs the
guard to find the commit that introduced the `up front` text (`git log
-S`) and require a `plan M<NNN>` subject. An agent can still forge a
matching subject. Consider that second check. Reject anything stronger.
The guards are defense-in-depth against drift in the operator's own
session (D-043 choice 1, `merge_guard.py:21-22`). They are not a defense
against an adversarial agent. The record of this project is that
checker-hardening past its stakes costs more than it returns.

Deny text (AC4): name both points. For an `up front` marker, also name the
slot the guard read and where it read it.

## 5. Recommended wording for IP1

The current text, "explicit user approval at a gate", is already
gate-neutral. The real change is what the approval is *of*. The rewrite
must say that, rather than list two places.

Recommended (option a, amended):

> IP1: Nothing reaches the default branch without the user's explicit
> approval at a gate of the run: at the merge question, or in the plan
> question set for a milestone whose promise, as that plan committed it,
> then merges unchanged and with every check of the run passed (D-1xx).

The clause "promise ... merges unchanged" is what makes an up-front
approval an approval of what ships. The route-back conditions of questions
2 and 6 are its mechanism. They live in the rulebook and the review skill,
not in the IP.

(a) Naming both points without the "unchanged" clause: the IP then
licenses merging work whose promise the agent rewrote mid-run. Apply only
with the clause.

(b) Keeping IP1 and narrowing through a D-entry: textually possible, since
"at a gate" admits the plan gate. But the meaning everyone read into it
was the merge gate: the rulebook bullet, the guard docstring and deny text,
D-043's "never weakened". Changing the meaning while leaving the sentence
violates IP2's stance that prior state is surfaced, not silently
overridden. And `DESIGN.md:192-193` requires the decision plus D-entry
anyway. Reject as the sole vehicle. The D-entry is needed under (a) too.

(c) Keeping IP1 and dropping the up-front path: I do not recommend it, and
I do not disagree with the user's decision. The gain is unattended
completion of a run, which D-138's serial CI wait otherwise denies. The
323-to-1 record shows the chip rarely changes the outcome. The cases where
the merge question has shown value (amendments, rejects, principle changes,
degraded review) can each be routed back without a user present in the
ordinary case. The decision is sound on one condition: those routes ship in
M203, not later. Without them, (c) is the better state.

## 6. Signals beyond AC3 that return a run to the merge question

Apply:

- Any substantive amendment to Goal, Scope, or Acceptance criteria after
  the plan commit (question 2b, 2d).
- A finding rejected as false that its lens ranked first, or any
  false-reject on a user-facing tier milestone (question 2a).
- `Principles touched:` naming an IP, or a D-entry written in the run.
- A Review section with no recorded reviewer spawns (question 2f).
- A red CI run fixed after the PR opened. Step 8 already says "re-request
  approval if the fix was nontrivial" (`milestone-review/SKILL.md:516-517`).
  Under up-front approval, "re-request" can only mean the merge question.

Consider:

- The second defect return (question 2e).
- A merge of the default branch into the branch that needed conflict
  resolution (`tracking-rules.md:238-239`).
- In the plugin repo, a diff touching `hooks/` or the approval text of the
  review skill or rulebook (question 2g).

Note on AC3's stop condition. Every stop in the list already returns the
run to the merge question. That includes "a CI wait that times out" and
"a guard hook's denial" (`tracking-rules.md:385-386`). M203 T3 says the
resume routes must find the `up front` line "so a resume after a CI
timeout finds it". Read with AC3, the line tells route (c) that the push
and PR already happened. The chip is still re-posed, because a stop fired.
State that in T3 so the two do not conflict.

Evidence that the up-front path was a mistake after it ships, in rough
order of strength:

- An up-front merge the user reverts or hotfixes for a defect that a
  rejected or follow-up finding had named (M203's own falsifier, work log
  2026-10-03). One is a signal. Two reopen the path.
- A user reversing a disposition after reading the close block (D-144's
  falsifier). Count these per run. The close block must list every
  disposition for the count to exist.
- The reject share or follow-up share per run rising against the M202
  baseline (4/24 and 4/24) once the agent knows nothing is read before the
  merge.
- Hotfixes per merged milestone rising against the pre-M203 rate.
- Revealed preference: the user picking `at the end` on most plans. Then
  the question is a cost with no benefit.
- Wall-clock time from plan commit to merge not falling. Then the
  unattended-run gain did not materialize.

## Beyond the brief

- AC3's phrase "the reviewers rank as real and in scope" conflates two
  roles (question 2). Reword to "no finding the agent disposed fix-now is
  left unfixed", and add the false-reject route-back separately.
- AC3's close block lists only candidate-row findings. It must list every
  disposition verbatim, rejects with reasons included, as step 7 did
  (`milestone-review/SKILL.md:390-392`). Otherwise the D-144 falsifier has
  no detector under up-front approval.
- AC2 must state the default. A plan whose question set did not pose the
  merge question (the five-question cap) writes `at the end`. Review and
  the guard read a slot of `—` or a missing slot as `at the end`.
- `cairn_validate` can check the slot's value set (`up front YYYY-MM-DD` |
  `at the end` | `—`) in one line. That is cheaper than a skill-conduct
  rule.
- The guard docstring (`hooks/merge_guard.py:2-5`) says "at the review
  gate". AC4 changes the deny text only. Add the docstring to T4.
- The question set must say in plain words what the user gives up: the
  code, the findings and their dispositions, and any amendment are seen
  only in the close block after the merge. Recommended option: `at the
  end` for a user-facing tier or IP-touching milestone, `up front` for an
  internal tier one. The pros and cons the rulebook requires of each
  question (`tracking-rules.md:362-364`) carry this.
- The `step-7 approval:` line written with no user act must be
  distinguishable on sight from one written after a chip: `step-7
  approval: <branch> approved up front per plan <sha>`.

## Recommendations

1. **Apply.** Route back to the merge question on any substantive
   amendment to Goal, Scope, or Acceptance criteria after the plan commit.
   Mechanical: diff of the plan-owned sections against the plan commit, or
   any amendment work-log line.
2. **Apply.** Route back on a finding rejected as false that its lens
   ranked first, or any false-reject on a user-facing milestone. List every
   disposition, rejects with reasons, verbatim in the close block.
3. **Apply.** Route back when `Principles touched:` names an IP or a
   D-entry is written in the run.
4. **Apply.** Route back when the Review section records no spawned
   reviewers (degraded review, D-127).
5. **Apply.** Route back on a CI fix made after the PR opened.
6. **Apply.** Bind the slot per milestone. The question answers for several
   ids at once and lets the user hold any of them `at the end`. A re-cut
   asks again.
7. **Apply.** IP1 wording as in question 5, with the "promise ... merges
   unchanged" clause. The D-entry records that the approval precedes the
   diff and names the route-back conditions as its mechanism.
8. **Apply.** On an `up front` marker, the guard reads the milestone file's
   slot from the base remote's default branch and denies unless it reads
   `up front`. The marker and work-log line cite the plan commit SHA. The
   deny text names both points and the slot read.
9. **Apply.** Fix AC3's "reviewers rank as real" wording. State AC2's
   default of `at the end`. Add the guard docstring to T4. Resolve T3
   against AC3's stop condition as in question 6.
10. **Consider.** Ask at the second defect return under up-front approval.
11. **Consider.** Expire an up-front slot for a milestone that went
    `blocked` and resumes later. Conflict-resolved default-branch merges
    return to the question. In the plugin repo, diffs to `hooks/` or the
    approval text return to the question.
12. **Consider.** A `cairn_validate` check on the slot's value set.
13. **Consider.** The guard's second check, that the `up front` text was
    introduced by a `plan M<NNN>` commit.
14. **Reject with reason.** Any stronger binding of the marker to the user
    (signed tokens, hashing the chip answer). The guards are drift defense
    in one operator's session (D-043), not an adversarial boundary, and the
    cost exceeds the stakes.
15. **Reject with reason.** Option 5(b), a D-entry alone with IP1
    unchanged. It changes IP1's read meaning without changing its text,
    against IP2 and `DESIGN.md:192-193`.
16. **Reject with reason.** Option 5(c), dropping the up-front path. The
    unattended-run gain is real, and the merge question's demonstrated
    value can be routed back case by case. This holds only if
    recommendations 1-5 ship with M203.
