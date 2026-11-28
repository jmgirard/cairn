# RB05: Thrash-rule trigger precedence and the post-re-cut case (M114)

- **Date:** 2026-07-26
- **Output required:** write findings to `cairn/reviews/RR05-thrash-trigger-precedence.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**cairn** is a Claude Code plugin that governs project tracking: a repo adopts
it, and a set of skills (`/milestone-plan`, `/milestone-implement`,
`/milestone-review`, `/hotfix`, `/milestone`) drive work through a milestone
lifecycle backed by markdown files under `cairn/`. It dogfoods its own format:
this repo IS the plugin, and its own tracking lives in `cairn/`.

`/milestone-review` verifies a finished milestone. When a criterion or gate
check fails it sends the milestone back to `in-progress` — a **return**. The
**thrash rule** governs what happens when returns accumulate. Milestone M114
rewrote that rule, and the rewrite is what this brief asks about.

**Why the rule was rewritten.** A `/milestone` audit post-mortemed two
milestones in a different cairn-tracked repo (`intraclass`): its M93 took eight
review passes and three plan re-cuts; its M92 took seven passes. The old thrash
rule read: *"if this is the milestone's third trip back from review (count the
work-log), do not queue another retry — that's a mis-planned milestone;
recommend re-plan or split via `/milestone-plan`."* It fired once across
intraclass M93's seven returns, because a `/milestone-plan` re-cut unticks every
acceptance criterion and supersedes the tasks, so the next pass reads as a first
pass. M114 fixed that by counting **per milestone, never per cut**.

**The problem now under review.** M114 has itself been returned four times. Its
own review found, at pass 1, that the two triggers could fire together with
contradictory remedies and no stated precedence (finding F4, confidence-scored
60, logged but not actioned). That collision then actually occurred at pass 3.
M114 therefore added a precedence clause. At pass 4, an independent reviewer
found that clause is a trap (finding J2, scored 82), and the milestone author
escalated rather than fixing it in-session — because the author designed the
clause, the clause was itself the fix for F4, and the milestone has now failed
twice on doctrine edits that same author wrote.

## Materials

**The rule as it currently ships.** `skills/milestone-review/SKILL.md`, the
block beginning `**Thrash rule.**` (around line 104) through to the numbered
step 5 heading. Read the whole of step 4 above it for context — the rule is the
tail of the gate-failure instruction.

**The guard over it.** `skills/tests/test_thrash_rule.py`, and its registered
entries in `skills/tests/test_mutation_harness.py` (search
`guard="test_thrash_rule"`). Registration means: blanking the quoted block in
the target file must make the named test fail.

**The decision record.** `cairn/DECISIONS.md`, entry `### D-064`, which records
the six choices behind the rewrite. Note its Consequences paragraph contains a
claim that is now false (a guard it describes was later deleted); that is a
separate, already-identified defect and is NOT your question.

**The full review history.** `cairn/milestones/M114-review-loop-escape-hatches.md`
— sections `## Review`, `## Review pass 2`, `## Review pass 3`,
`## Review pass 4`, carrying findings F1–F7, G1–G7, H1–H5, J1–J5 and K1, each
with a confidence score. The `## Work log` records every gate decision. Read
the Scope section for what the milestone ships and what it re-cut out.

**Running things.** From the repo root, three stdlib suites, all of which must
be green: `python3 -m unittest discover -s skills/tests`,
`python3 -m unittest discover -s scripts/tests`,
`python3 -m unittest discover -s hooks/tests`. Check each exit code separately;
do not pipe them. Also `python3 scripts/cairn_validate.py`. To experiment
without touching the working tree, export a scratch copy:
`git archive HEAD | tar -x -C /tmp/<dir>` — a partial copy produces a red
baseline and misleads. **Do not modify any tracked file**; a previous reviewer
did and contaminated a commit.

## Questions

1. **Trigger (a)'s condition.** It reads "A third return". Because returns are
   counted per milestone and a re-cut increments rather than resets, this
   predicate is true on the third return and on every return after it. Should it
   stay a threshold, become "exactly the third return", become "the third return
   since the last re-cut", or something else? Any answer must not reintroduce
   per-cut resetting, which is the original defect the rewrite exists to fix and
   which cost intraclass M93 four of its seven returns.

2. **Should a precedence rule exist at all?** The current clause makes (a) win
   unconditionally where both fire. An alternative is that the triggers are
   composable — (a) governs the *disposition* (re-plan or split) while (b)'s
   escalation offer remains available alongside it, since they answer different
   questions ("is this milestone mis-sized?" versus "is this approach wrong?").
   Is unconditional precedence, scoped precedence, or composition correct? If
   precedence is right, is (a) the right winner?

3. **The undefined post-re-cut case.** No rule anywhere in cairn — not
   `skills/milestone-plan/SKILL.md`, `skills/milestone-brief/SKILL.md`, nor
   `skills/shared/tracking-rules.md` — says what happens when a milestone
   returns *again* after a re-plan or split. Today the count keeps rising and
   trigger (a) keeps prescribing the remedy already spent. Should there be a
   terminal disposition (drop, park as `blocked`, mandatory escalation), should
   the count drive escalating remedies, or is the absence correct because a
   maintainer approves every routing chip anyway and no rule should pre-empt
   them? Note cairn's IP3: nothing the user asked for is silently dropped.

4. **Is reverting the honest answer?** Removing the precedence clause returns
   the rule to a documented *ambiguity* (F4, which review scored 60) instead of
   a documented *trap* (J2, scored 82), with F4 recorded as a known gap plus a
   ROADMAP candidate row. Weigh that against shipping a scoped fix. Precedent:
   D-059 retired an advisory measured not to work rather than repairing it.

5. **Is the rule's own guard adequate to whatever you recommend?** If your
   answer changes the rule text, say which assertions in
   `skills/tests/test_thrash_rule.py` must change and what new property needs
   pinning, bearing in mind `skills/shared/guard-doctrine.md` §3 (a detector's
   matcher must be exercised at every rendering its target can take) and §7 (a
   sweep whose cells may legitimately be silent passes for free on silence).
   Both were added by this same milestone, and this milestone violated both.

## Constraints

Fixed; flag disagreement explicitly rather than working around it.

- **Counting is per milestone, never per cut** (D-064). A re-cut increments the
  count. Any recommendation reintroducing per-cut resetting must argue against
  D-064 directly, quoting it.
- **Fable escalation stays gated per instance through the RB/RR protocol**
  (D-004, as re-framed by D-062). Do not recommend making `/milestone-brief`
  automatic or a standing menu item.
- **No `cairn_validate` check for the thrash rule** (D-064 choice 6): the
  counting half is mechanical but inert and the shape-recurrence half is a
  judgment. D-059 is the precedent — an advisory measured not to work was
  retired, not repaired. Recommending a mechanical check requires arguing
  against both.
- **History is never rewritten** (IP4, D-045). `DECISIONS.md`, work logs and
  archived reviews are append-only; corrections are superseding entries.
- **The rulebook is governed at the door** (D-057). `skills/shared/tracking-rules.md`
  is an always-read file; additions to it must earn their lines. The thrash rule
  deliberately lives in `/milestone-review`, not the rulebook, for this reason.
- **Prior state is surfaced, never silently obeyed or silently overridden**
  (IP2). If you recommend against a recorded decision, say so and quote it.

## Output format

In `RR05-thrash-trigger-precedence.md`: answer each question by number with your
reasoning and evidence; list any additional findings separately under "Beyond
the brief"; end with concrete recommendations, each marked apply / consider /
reject-with-reason. Where findings bind implementation, also emit a
`## Binding criteria` section: numbered `BC1…`, each a measurable assertion
checkable against evidence, with any numeric projection stating its tolerance.
These are ingested VERBATIM into M114's acceptance criteria and mechanically
diffed against this file; departures are legal only through that milestone's
shown "Deviations from RR05" table.
