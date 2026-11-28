# RB10: Should `guard-doctrine.md` §8 survive, and is its replacement falsifier legitimate? (M123)

- **Date:** 2026-07-30
- **Output required:** write findings to `cairn/reviews/RR10-section8-survival.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

**Read the materials at a branch ref, not at the default branch.** Every
artifact under review lives on `m123-section8-convergence-rebuild`, whose HEAD
is `cafbbc1` (9 commits ahead of `main`). On `main` these files are still in
their pre-M123 state, and reading them there will silently answer a different
question. Use `git show cafbbc1:<path>` for anything this brief names, or check
the branch out read-only. Where a revision other than `cafbbc1` is named below,
use that one.

## Background

**What cairn is.** cairn is a Claude Code plugin that provides a milestone-based
development-tracking system: skills for planning, implementing and reviewing
units of work, a shared rulebook (`skills/shared/tracking-rules.md`) and doctrine
modules, plus Python guard tests that lock the doctrine prose so a rule cannot
be deleted without a test failing. The repo dogfoods its own system by hand
under `cairn/`. It is not a library; its deliverable is prose and the guards
over that prose.

**What §8 is.** `skills/shared/guard-doctrine.md` §8, "The author never certifies
its own guard's coverage", is a step run before a guard-authoring milestone
enters review. A fresh-context Opus reader that authored none of the work checks
three things: that every acceptance-criterion clause maps to an assert that
actually pins it, that every docstring/comment/work-log/record claim is true of
the file it describes, and that every anchor matches the shipped bytes. The gate
is entered only at zero unresolved. It was adopted by **D-067** after a
milestone (M114) returned from review seven times, its seventh return arriving
with every suite green and still carrying two records that described its own
artifact wrongly. The diagnosed root cause: an author checks a description
against its generative model of the artifact rather than against the artifact.

**§8's own falsifier, and that it fired.** §8 carries a stated exit condition,
in the shape D-059 established for retiring a mechanism measured not to work:
*"if guard-authoring milestones still average multiple description-layer returns
after adoption, the step didn't work — retire it (D-059), don't tune it."* That
condition **fired**. The average over M116–M119 is 4.5 rounds (2, 4, 3, 9), and
M121 added two more. The prescribed remedy — retire the step — is owed and, as
of `cafbbc1`, unpaid.

**The prior attempt and the prior review.** M121 attempted to narrow §8 by
excluding, from the certified scope, text a previous round's own fix authored.
That was escalated as RB09. **RR09** (at
`cafbbc1:cairn/reviews/archive/RR09-section8-scope-exclusion-soundness.md`)
found the exclusion's behavioural content defensible but its formulation
unusable: it was framed on the wrong object ("certified scope"), putting it in
unacknowledged conflict with D-070, and its operative noun alternated between
"text" and "record" undefined, licensing two opposite rules — under one the rule
was provably inert on its own motivating case, under the other it stopped the
loop at a point RR09's own analysis calls unacceptable. RR09 returned verdict
**(d): keep the exclusion, rebuilt**, explicitly rejecting both reverting
unchanged (rec 8) and retiring §8 outright (rec 9). M121 then departed from
RR09's rec 8 and withdrew the exclusion entirely (**D-080**), because RR09's own
eight binding criteria were found to carry ten blocking defects. **D-082**
restored D-067's falsifier in full, "don't tune it" included, and recorded that
its remedy is owed and unpaid.

**What M123 is.** M123 is the rebuild RR09 prescribed, with the criteria re-cut
rather than ingested. As of `cafbbc1` it ships, in §8: a two-axis discriminator
(subject matter draws what is checked and fixed, provenance draws what reopens);
a defined class, the *fix-authored record*, that does not reopen a round; an
explicit statement that a fix's code, asserts and fixtures — and any record
predating round 1 — do reopen; a mandate boundary limiting reopening to §8's
three named checks, with robustness observations routed to §§1–7; three
per-class confirmation obligations, none of them on the author; a record-churn
evidence paragraph; and a **yield-based falsifier replacing the round-count
one**. The supersessions are **D-083**, with two of its measurement claims
corrected by **D-084**.

**The new fact neither RR09 nor D-082 had.** M123 ran its own §8 certification —
under the *pre-rebuild* rules, by a deliberate gate decision, so that the author
would not apply its own newly-loosened rule to itself. It took **two rounds**,
returning **16 and 13 discrepancies**. This matters in three ways:

1. Round 2 found a genuine contradiction in the shipped doctrine that round 1
   missed entirely, and found **ten §8 rules that inverted green** — the rule
   could be negated in place with the whole 736-test suite passing.
2. Round 2 also found **three false records that round 1's own fixes
   introduced**, including an evidence line that round 1's fix invalidated in
   the same commit that wrote it.
3. **Both structural tests written during round 1 were defeatable**, and one of
   them reproduced, inside the check for it, the exact enumerate-the-renderings
   failure that `guard-doctrine.md` §3 exists to name.

**The measurement that motivates this brief.** M123 classified round 2's own 13
findings under the rules M123 ships: 4 would be shielded as fix-authored
records, 4 would be routed out of mandate to §§1–7, and **5 would still
reopen**. So the rebuild cuts the reopening set from 13 to 5 — a real reduction,
and not a stop. A round 3 is convened either way.

The maintainer stopped at that point rather than running a round 3, and
escalated. The question is no longer only whether the rebuild is well-formed. It
is whether an instrument whose own repair costs two certification rounds, 29
discrepancies and a near-quadrupling of the section's length is an instrument
worth keeping.

## Materials

All paths are at `cafbbc1` unless stated otherwise.

- `skills/shared/guard-doctrine.md` — §8 in full (the section begins at the
  heading `## 8. The author never certifies its own guard's coverage` and runs
  to end of file; 162 lines at this ref, 46 lines on `main`). §§1–7 are the
  surrounding doctrine the mandate boundary routes work to; read §2 (what the
  mutation harness does and does not catch) and §3 (absence assertions, and the
  enumerate-the-renderings failure) at minimum.
- `cairn/DECISIONS.md` — entries **D-083** and **D-084** (the last two in the
  file), and for context **D-059**, **D-067**, **D-069**, **D-070**, **D-079**,
  **D-080**, **D-081**, **D-082**. The file is append-only; scan its `### D-`
  headings and read whole only what you need.
- `cairn/milestones/M123-section8-convergence-rebuild.md` — the acceptance
  criteria AC1–AC9, the Coverage map, and the whole work log. The work log is
  the record of both certification rounds, what each returned, and what was done
  about it; it also carries the classification measurement quoted above.
- `cairn/reviews/archive/RR09-section8-scope-exclusion-soundness.md` — the prior
  review, especially §2 (the round-by-round classification of M119's rounds
  5–9), §4 (the falsifier analysis and the yield-based replacement it proposed),
  §5 (why it rejected retirement), and §6 (the defects it found in M121's prose).
- `skills/tests/test_fresh_context_readers.py` — the guards over §8, class
  `TestDescriptionLayerCertification`, including four structural tests near the
  end of the class that check properties of §8 rather than phrases in it.
- `skills/tests/test_mutation_harness.py` — the `Mutation(...)` entries with
  `target=GUARD_DOCTRINE`; the harness blanks each registered block and requires
  its guard to fail.
- Historical round counts, if you want to verify them yourself:
  `016a210` (M119's pre-archive milestone file, its nine rounds),
  `a25e6dd^` (M114 pass 8, four rounds),
  `8763368^` (M121, two rounds),
  `c76fa65^` (M118, three rounds).
- To run the suites from the repo root:
  `python3 -m unittest discover -s skills/tests` (and likewise `scripts/tests`,
  `hooks/tests`). All three are green at `cafbbc1`.

## Questions

1. **Does D-067's falsifier, as D-082 restored it, now read as met, and with
   what consequence?** It fires on guard-authoring milestones "still averaging
   multiple description-layer returns after adoption". M123 is at two rounds.
   The average across every milestone that has run the step (M114 4, M116 2,
   M117 4, M118 3, M119 9, M121 2, M123 2) is well above one. State plainly
   whether the condition is met, and whether "retire it, don't tune it" is
   therefore owed as written — or whether the condition as phrased is itself
   defective, since a step whose bar is zero unresolved will almost always take
   more than one round and the falsifier may have been unmeetable-in-the-good-case
   from the start.

2. **Is D-083's replacement of the falsifier legitimate, or is it the tuning
   D-059 forbids?** M123's argument (D-083 part 2) is that the distinction is a
   checkable fact rather than a claim about intent: the old falsifier counts
   *rounds*, and §8's two new rules both act directly on the round count, so the
   measure is satisfiable by construction by the very rules it polices. The
   replacement counts shipped-behaviour defects and pre-round-1-surface findings
   returned by rounds after the first, plus in-place record fixes later found
   false. Assess whether that distinction is sound, or whether "the measure was
   of the wrong quantity" is a move that would excuse replacing any inconvenient
   falsifier.

3. **Is round 2's yield evidence for the instrument or against it?** Round 2
   found a real contradiction in shipped doctrine, ten rules that inverted green,
   and two defeatable structural tests — all of which round 1 missed. Read one
   way, that is the instrument working exactly as intended on the hardest
   possible subject. Read the other way, a doctrine section that needs 29
   findings across two rounds to stabilise is too complex to be doctrine, and
   the instrument is generating work proportional to the prose it is asked to
   certify rather than to the risk in it. Which reading does the evidence
   support, and what would distinguish them?

4. **What should happen to §8?** Choose among, and argue against the others:
   (a) retire it entirely, paying the fired falsifier as written;
   (b) keep it as M123 rebuilt it;
   (c) reduce it to a single certification pass — round 1 only, with a fix
   confirmed by operation and no re-certification round — which is what D-083's
   own clause (i) would produce if it fired;
   (d) keep the instrument but move it, e.g. fold it into
   `/milestone-review`'s existing three-lens fan-out (note that the fan-out runs
   *after* `status → review` and is diff-anchored, while §8 reads the whole
   description layer before the gate — RR09 §5 treats this as decisive against
   folding, on evidence you should re-examine rather than inherit);
   (e) something else you identify.
   Round 1's measured yield across milestones is real and is RR09's stated
   ground for rejecting retirement: M116 9 findings, M117 8, M118 16 of which
   eleven were blocking, M119 2 code defects, M121 1 shipped-behaviour defect
   plus 10 description-layer, M123 16. Weigh that against the cost.

5. **Is §8's growth part of the disease?** The section went from 46 lines to
   162 in this milestone (D-084 corrects D-083's understatement of this). The
   rebuild's answer to a convergence problem was substantially more prose, and
   more prose is more surface for the next certification to audit — which is
   arguably the regress D-069 identified, relocated from the work log into the
   doctrine itself. Is there a materially smaller form of §8 that keeps round
   1's measured yield? If so, sketch it concretely.

6. **Is the rebuilt rule actually free of the two-readings defect RR09 found?**
   RR09's decisive finding against M121 was an undefined operative noun
   licensing two opposite rules. M123's answers are: a defined term
   (*fix-authored record*, enumerated as docstrings, comments, work-log lines
   and record claims); an explicit statement of what the shield does *not*
   cover; a "shield and never a licence" sentence added in round 2 after the
   provenance rule was found to read as *sufficient* for reopening; and a
   "clears both lines" composition with the mandate boundary. Read §8 as shipped
   and say whether a careful later reader could still derive two incompatible
   rules from it, naming the sentences if so.

7. **Is the mandate boundary sound?** It limits reopening to §8's three named
   checks and routes robustness observations that no acceptance-criterion clause
   pins to §§1–7. RR09 (rec 5) proposed this as "the piece that answers M119's
   round count". Two concerns to test: whether the boundary is decidable in
   practice (M123 resolves the overlap with check 1 by definition rather than by
   a tie-break — see §8's "What decides is whether a criterion clause is at
   stake"), and whether routing a finding out of certification means it actually
   gets fixed, given that §§1–7 carry no gate of their own.

## Constraints

Flag disagreement with any of these explicitly rather than silently working
around it.

- **IP4 / D-065.** `cairn/DECISIONS.md` is append-only and attaches at append
  time, not merge time. No recommendation may require editing an existing
  D-entry, including D-083 and D-084, which are unmerged. Supersession by a new
  entry is the only legal correction route. RB09 supplied the opposite
  constraint in error and thereby produced an unsatisfiable binding criterion;
  do not repeat it.
- **D-067's standing rejections**, which a recommendation may supersede but must
  not ignore: a mandatory re-derivation step by the author ("it instructs the
  same judgment that failed while citing the same instructions"); any rubric or
  threshold change; and any `cairn_validate` mechanization of the instrument,
  on the ground that satisfiability and claim accuracy are judgments about prose
  meaning.
- **D-059's precedent** — a mechanism measured not to work is retired, not
  tuned. This is the constraint question 2 asks you to apply, not one to assume
  the answer to.
- **RR09's recs 8 and 9** (rejecting revert-unchanged and rejecting outright
  retirement) are on the record but are explicitly **open to revision here**:
  they were reached without M123's own two-round cost, which is the new
  evidence. Say so if you revise them, and say why.
- **D-057** closed the stock-side size-governance program; rulebook growth is
  governed at the door and reopened only on measured cost. Question 5 asks about
  §8's length as a *certification* cost, not as a weight-governance matter — do
  not reopen size governance.
- cairn assumes one operator running these skills; do not propose mechanisms
  requiring concurrent operators or CI, as this repo has no CI.

## Output format

In `RR10-section8-survival.md`: answer each question by number with your
reasoning and evidence; list any additional findings separately under "Beyond
the brief"; end with concrete recommendations, each marked apply / consider /
reject-with-reason.

Where findings bind implementation, also emit a `## Binding criteria` section:
numbered `BC1…`, each a measurable assertion checkable against evidence, with
any numeric projection stating its tolerance.

**A specific caution about binding criteria.** These are ingested *verbatim*
into the constrained milestone's acceptance criteria and mechanically
string-compared against this file, so a criterion that is unsatisfiable as
written cannot be quietly softened later. RR09's own eight binding criteria were
found, at the pre-ingest audit, to carry ten blocking defects — two criteria
assigning opposite status to the same objects, two freezing a count that RR09's
own analysis contradicted, one mandating an edit IP4 forbids, and one changing a
standing decision with no criterion requiring the superseding entry. Before you
emit each criterion, ask of it the two questions that audit asks: *what state of
the world satisfies this exactly as written*, and *does any inviolable principle
or D-entry make that state unreachable*. Ask them of the set as a whole as well
as of each member, since criteria that are individually satisfiable can be
jointly unsatisfiable. Prefer few criteria that survive those questions to many
that do not. If your recommendation is to retire §8, say so without binding
criteria rather than manufacturing them.
