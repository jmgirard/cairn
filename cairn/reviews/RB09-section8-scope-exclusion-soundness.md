# RB09: Is §8's new scope exclusion sound? (M121)

- **Date:** 2026-07-27
- **Output required:** write findings to `cairn/reviews/RR09-section8-scope-exclusion-soundness.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

**The repo.** `cairn` is a Claude Code plugin that ships a project-tracking
system as prose: skills (`skills/*/SKILL.md`), a shared rulebook
(`skills/shared/tracking-rules.md`), and conditionally-read doctrine modules
(`skills/shared/guard-doctrine.md`, `validation-doctrine.md`,
`records-hygiene.md`). The repo dogfoods its own format by hand under `cairn/`.
Its prose rules are locked by Python `unittest` "prose-guards" that assert
substrings of the shipped markdown, plus a mutation harness
(`skills/tests/test_mutation_harness.py`) that blanks each registered block and
requires the guard to fail.

**The instrument under review.** `guard-doctrine.md` §8 ("The author never
certifies its own guard's coverage") requires that, before a guard-authoring
milestone moves to review, it hand its **description layer** — docstrings,
comments, work-log lines, record claims — to a fresh-context reviewer that
authored none of it. That reviewer checks three things: AC-clause-to-assert
coverage, claim-vs-file accuracy, anchor-vs-shipped-bytes fidelity. The gate is
entered at zero unresolved. §8 was adopted by D-067 and amended by D-069/D-070.

**The problem it developed.** Milestone M119 ran **nine** §8 rounds. Each
round's fix wrote new prose; the next round then found defects in that prose.
Rounds 5–9 found no new code defects (one live detector false positive
excepted) yet kept returning findings, and round 9's two findings sat in round
8's own text. The loop was stopped by maintainer override, not by converging.

**What M121 did about it.** Milestone M121 re-decided §8 on that evidence and
shipped a **scope exclusion** (`cairn/DECISIONS.md` D-079 clause 1): a finding
whose only subject is text a previous round's own fix authored is fixed in
place but opens no further round. An earlier attempt in the same milestone — a
rule bounding the *number of rounds* — was drafted and withdrawn when M121's
own §8 certification showed it would have stopped M119's loop before a real
defect was found.

**Why this needs independent review.** M121's §8 certification and its
three-lens code review have now challenged the shipped disposition twice, on
three distinct grounds (below). The implementing session authored the rule
being challenged, and cairn's own rule (tracking-rules, "Model and agent
strategy") is that the implementing session never authors the durable verdict
on the review constraining it. M121 is currently `blocked` on this brief.

## Materials

Read these, in this order. Line numbers are as of commit `2dbda48` on branch
`m121-verification-triage`.

1. **`skills/shared/guard-doctrine.md`, §8 in full** — from the line
   `## 8. The author never certifies its own guard's coverage` to the end of the
   section (roughly lines 256–320). Four paragraphs matter: the diagnosis, the
   three checks, **D-069's scope bound**, and **M121's new exclusion** (the
   paragraph beginning `**The exclusion extends to text a previous round's own
   fix authored`).

2. **`cairn/DECISIONS.md`** — read these four entries whole, by searching for
   their `### D-` headings:
   - **D-067** — adopts §8 and the plan-gate criteria audit. Carries §8's own
     falsifier: *"if guard-authoring milestones still average multiple
     description-layer returns after adoption, the step didn't work — retire it
     (D-059), don't tune it"*.
   - **D-069** — puts a certification round's own **report** outside the
     certified scope, on the ground that §8 obliges every round to record a
     verdict, that record is append-only under IP4, and so each round
     manufactures uncertified surface for the next one.
   - **D-070** — **narrows D-069's premise.** This is the entry the first
     objection turns on. Its corrected premise reads: *"rounds 1–3 found real
     defects in records about the work, each fixed and confirmed; round 4's
     discrepancies were in certification narrative alone."* D-069's Context had
     claimed rounds 3–4 found defects only in certification narrative; D-070
     establishes that **defects in records about the work are INSIDE the
     certified scope**, and only narrative about the certifying process is
     outside it.
   - **D-079** — M121's disposition. Clause (1) is the exclusion under review.
     Read its Context, Decision and Consequences whole, including the paragraph
     recording the withdrawn round-bounding rule.

3. **M119's nine §8 rounds, in its own words.** The milestone file is archived
   and compressed; the full work log lives only in git history. Retrieve it:

   ```
   git show 8dace78^:cairn/milestones/M119-decisions-advisory-and-consistency-guards.md
   ```

   Read work-log lines ~99–125. Each `§8 round N` line records what that round
   returned. The round-by-round split matters to question 2; the line beginning
   `**§8 loop stopped at round 9, not converged.**` is M119's own diagnosis.

4. **`cairn/milestones/M121-verification-triage.md`** — its `## Review` section
   carries the findings below with their confidence scores, and its `## Work
   log` records the withdrawn round bound and the reasoning at each gate.

5. **`cairn/references/prompting-opus-5.md`** — the source that started this.
   The § Task scope and over-verification finding is the one M121 triaged.

## The three objections

Stated here so you review the argument, not a paraphrase of it.

**Objection A (scored 80, blame-history lens) — the exclusion contradicts
D-070.** D-070 drew the certified-scope line on **subject matter**: records
*about the work* are inside, narrative about the *certifying process* is
outside. M121's exclusion draws it on a different axis — **who authored the
text and when** ("was this written as a previous round's fix"). M119's rounds
5–9 corrections were substantive claims about the shipped code's behaviour and
coverage — "records about the work" in D-070's own terms, which D-070 put
squarely inside the scope. The shipped text frames the exclusion as extending
D-069 and never engages D-070's carve-back.

**Objection B (scored 74, diff-bug lens) — the exclusion is either inert on its
own motivating case, or does the harm it was chosen to avoid.** D-079 rejects
the round bound because *"every one of M119's rounds 5–9 also returned a real
guard-coverage gap"*. But those gaps sat in previous rounds' fix text too:
round 5's six-of-ten-signatures gap is in the round-3/4 removal's own fixtures;
round 8's two boundary arms are in round 6/7's fixes; round 9's
`NEAR_MISS_LINES` gap — the `--- a/|+++ b/` widening that would WARN forever —
is in round 7/8's fix. So either (a) guard-coverage gaps are **not** "such a
record", in which case the exclusion would have changed M119's round count by
**zero** — the very case that produced it — and the re-armed falsifier fires
again identically; or (b) they **are**, in which case the exclusion stops the
loop around round 6 and discards the forever-WARN finding, which is exactly the
outcome D-079 declares unacceptable when rejecting the round bound. D-079 never
chooses, and its evidence supports neither disposition over the other.

**Objection C (scored 62, diff-bug lens) — composed with D-069 it is a round
bound by another route, and it suppresses its own falsifier.** D-069 already
puts a round's own report outside scope; M121 adds the fixes those rounds
write. After round 1, nearly every byte a milestone newly produces is
uncertified surface that cannot reopen a round, so rounds ≥2 can only find
pre-round-1 text that round 1 missed. D-079 asserts *"the scope of what reopens
a round is a different object"* from a round count, never measures the effect on
round counts, and then re-arms §8's falsifier against *"average multiple
returns with this scope in force"* — a measurement the change itself
mechanically suppresses. D-059's precedent ("retire it, don't tune it") is
arguably the thing being worked around.

## Questions

1. **Does M121's exclusion contradict D-070, or is it compatible with it?** If
   it contradicts D-070, say so plainly: cairn's rule is supersede-don't-ignore,
   so a contradiction means D-079 must name D-070 as superseded and carry the
   argument, not merely cite D-069. If it is compatible, state the principle
   that reconciles the subject-matter axis with the authorship axis, in a form
   that could be written into §8 as a discriminator a later reader can apply.

2. **Run objection B to ground against M119's actual rounds.** For each of
   rounds 5–9, classify what that round returned into (i) defects in the
   shipped deliverable's code or guard coverage, and (ii) inaccurate records.
   For (i), determine whether the finding's subject was text an earlier round's
   fix authored. Then answer: **with M121's exclusion in force, at which round
   would M119's loop have stopped, and which of its real findings would have
   been lost?** If the answer is "none would have been lost and it would have
   stopped at round 9 anyway", say so — that is the inert case and it is a
   finding.

3. **Is objection C's regress real?** Does the exclusion, composed with D-069,
   leave rounds ≥2 able to find anything substantive? Give the class of finding
   a round ≥2 can still return under the shipped rule.

4. **Is §8's falsifier still measurable under the shipped rule?** D-067 re-arms
   it as "average multiple returns with this scope in force". If the exclusion
   mechanically reduces returns without changing description-layer quality, the
   falsifier can never fire. If so, propose a falsifier that survives the
   change — something measurable that would tell a future maintainer the
   instrument has stopped earning its cost.

5. **What should M121 actually ship?** Choose among, or improve upon:
   (a) the shipped scope exclusion, amended to answer questions 1–4;
   (b) reverting to §8 unchanged, recording that the sharper reading of M119's
       evidence does not support narrowing;
   (c) retiring §8 outright per its own falsifier, folding description-layer
       accuracy into the three-lens review fan-out that already runs at
       `/milestone-review`;
   (d) something else you judge better.
   State which, with the argument. If your answer is (c), address what replaces
   the round-1 yield: §8's round 1 returned real defects in every milestone that
   ran it (M116 nine, M117 eight, M118 sixteen with eleven blocking, M119 two
   code defects).

6. **Is there a defect in the *shipped §8 prose* independent of the above?**
   One reviewer flagged that the exclusion's operative noun switches from
   "text" to "record" within a single sentence with no definition — "text"
   reaches asserts and fixtures a fix authored, "record" reaches only the
   description layer — and that a milestone could read an unpinned acceptance
   criterion as excluded because the assert was written by a previous round's
   fix. Judge that, and any other wording defect you find in the paragraph.

## Constraints

Fixed; flag disagreement explicitly rather than silently working around it.

- **IP4 — history is never edited.** `cairn/DECISIONS.md` entries, work logs
  and archived milestones are append-only. A wrong entry is superseded by a new
  entry, never rewritten. D-079 has not merged, so the authoring milestone may
  still amend it in place (M115's precedent); anything already on `main`
  cannot be.
- **D-059's precedent** — a mechanism measured to fail is retired, not tuned.
  This is what makes "is this a round-count tuning in disguise?" a real
  question rather than a semantic one.
- **D-031** — new domain doctrine lands in a module (`guard-doctrine.md`), not
  in `tracking-rules.md`. Do not propose moving §8 into the core rulebook.
- **D-057** — the stock-side size-governance program is closed; do not propose
  caps or budgets on rulebook or record mass as the remedy.
- **Out of scope:** the plan-gate criteria audit (D-079 clause 2), the
  self-checking-class rule in `tracking-rules.md` (clause 3), and
  `cairn/references/self-verification-ledger.md`'s classification. Those are
  settled or handled separately by M121.
- The three-lens review fan-out at `/milestone-review` and its scorer are
  fixed except where your answer to question 5 option (c) proposes folding §8
  into them; that proposal is in scope.

## Output format

In `RR09-section8-scope-exclusion-soundness.md`: answer each question by number
with your reasoning and evidence; list any additional findings separately under
"Beyond the brief"; end with concrete recommendations, each marked apply /
consider / reject-with-reason. Where findings bind implementation, also emit a
`## Binding criteria` section: numbered `BC1…`, each a measurable assertion
checkable against evidence, with any numeric projection stating its tolerance.
These are ingested VERBATIM into M121's acceptance criteria and mechanically
diffed against this file; departures are legal only through M121's shown
"Deviations from RR09" table.
