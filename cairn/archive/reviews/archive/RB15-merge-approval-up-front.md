# RB15: Merge approval given in the plan question set (M203)

- **Date:** 2026-10-03
- **Output required:** write findings to `cairn/reviews/RR15-merge-approval-up-front.md`
- **Binding criteria:** not requested

You are performing an independent expert review. This brief is fully
self-contained. Do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

cairn is a Claude Code plugin. It tracks a repo's work as milestones in
markdown files under `cairn/`, and it runs each milestone through three
skills: `/milestone-plan`, `/milestone-implement`, and `/milestone-review`.
Its first inviolable principle, IP1, reads today: "Nothing reaches the
default branch without explicit user approval at a gate."

Milestone M202 (merged 2026-10-03 as PR #209, decision D-144) made the loop
one "run". The user answers one batched plan question set. The agent then
implements, reviews, and settles every reviewer finding itself (reject with
a reason, fix on the branch, or send to a candidate row). It asks the user
again only at the merge question, or at a closed list of stops. After a
merge, review starts the next workable milestone of the same plan with no
new question set. The plan evidence in M202 counted, across the user's
sessions from 2026-09-22 to 2026-10-03, 323 merge questions answered and 1
changed from the recommended option.

Milestone M203, the subject of this brief, lets the user approve the merge
in the plan question set, before any diff exists. A run whose review passes
then merges without the merge question. The user chose this at the plan
gate, as one approval for each plan (not a standing approval for the repo).
M203 rewrites IP1 so that explicit approval may be given either in the plan
question set or at the merge question. The plan tagged that change as
touching an inviolable principle, and the user chose this escalation before
any of it is written.

The review is wanted because the change moves the only human check on what
reaches the default branch to a point where the user has not seen the code,
the review findings, or the agent's own dispositions of those findings.

## Materials

- `cairn/milestones/M203-merge-approval-up-front.md`: the whole file. AC3
  lists the conditions under which review would skip the merge question.
- `cairn/DESIGN.md` lines 190-215: the IP and GP principles.
- `cairn/milestones/archive/M202-one-question-set-run.md`: what M202 shipped.
- `cairn/DECISIONS.md`: read only these entries, found by their `### D-`
  headings: D-138 (PR opens after approval), D-144 (the run), D-127
  (freshness spawns), D-043 (one operator per repo).
- `skills/shared/tracking-rules.md`: the sections "Git and approval model"
  and "Question gates and phase closes".
- `skills/milestone-review/SKILL.md`: step 5 (how the agent settles
  findings, the return floor), step 7 (the merge question), step 8 (push,
  PR, marker, CI wait, merge), and step 10 (the next milestone of the plan).
- `skills/milestone-plan/SKILL.md`: step 3 (the question set).
- `hooks/merge_guard.py` (231 lines): the PreToolUse hook that denies a
  merge to the default branch unless `cairn/.merge-approved` names the PR.

Rough size: about 1,500 lines of reading. No code needs to run.

## Questions

1. Is an approval given before the diff exists "explicit user approval" in
   the sense IP1 protects? State what the user can and cannot know at that
   moment, and what the merge question gives that the up-front answer does
   not. Weigh this against the 323-to-1 evidence above.
2. AC3 of M203 lists the conditions under which review merges with no
   merge question. Which failure modes pass all of them? Consider at least:
   findings the implementing session itself rejected as false or as planned
   changes; criteria amended during the run; a run that chains several
   milestones of one plan; a scope narrowed by the agent; and a defect
   return that the run fixed on its own. For each one that passes, say
   whether it needs a new condition, or whether the residual risk is
   acceptable, and why.
3. One approval for each plan covers every milestone that the plan created,
   because review chains into them. Should the approval instead bind one
   milestone at a time, or a set the user names? Say which and why.
4. Under M203 the agent writes the merge marker
   (`M<NNN> approved up front YYYY-MM-DD for PR #<N>`) with no user act in
   that turn. Does this weaken what `merge_guard` enforces? What on-disk
   evidence should tie the marker to the user's plan-time answer (for
   example, a `Merge approval:` header slot committed to the default branch
   in the plan commit, before the branch existed), and should the guard
   check that evidence mechanically?
5. Give your recommended wording for IP1. Compare: (a) rewriting IP1 to
   name both points of approval; (b) keeping IP1 and narrowing it through a
   D-entry; (c) keeping IP1 as it is and dropping the up-front path.
6. Name any signal that should send a run back to the merge question even
   under an up-front approval, beyond AC3's list. Name the evidence that
   would show the up-front path to be a mistake after it ships.

## Constraints

- The user decided at the plan gate on 2026-10-03 to allow up-front
  approval, one approval for each plan. A standing approval for every run
  of a repo is out of scope. If you disagree with the decision itself, say
  so explicitly under question 5 option (c). Do not work around it.
- D-144: the run model (one question set, the agent settles findings, one
  merge question) is fixed. This brief does not reopen it.
- D-138: the PR opens only after the approval, at review step 8.
- D-043: one operator per repo. Hooks guard only that operator's own
  session.
- IP4: history is append-only. Decisions are superseded, never edited.
- A dependency change or an outward action outside the question set's
  grants stays a stop, as the rulebook states.

## Output format

In `RR15-merge-approval-up-front.md`: answer each question by number with
your reasoning and evidence (cite file and line). List any additional
findings separately under "Beyond the brief". End with concrete
recommendations, each marked apply / consider / reject-with-reason. Your
report is advisory: emit a `## Binding criteria` section ONLY if this
brief's header slot says `requested`, and it says `not requested`.
