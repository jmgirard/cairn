# RR10: Should `guard-doctrine.md` §8 survive, and is its replacement falsifier legitimate? (M123)

- **Date:** 2026-07-30
- **Brief:** `cairn/reviews/RB10-section8-survival.md`
- **Materials read:** `cafbbc1:skills/shared/guard-doctrine.md` (§8 whole, §§1–7,
  §2 and §3 closely); `cafbbc1:cairn/DECISIONS.md` D-059, D-067, D-069, D-070,
  D-079–D-084; `cafbbc1:cairn/milestones/M123-section8-convergence-rebuild.md`
  (criteria, coverage, full work log);
  `cafbbc1:cairn/reviews/archive/RR09-section8-scope-exclusion-soundness.md`;
  `cafbbc1:skills/tests/test_fresh_context_readers.py`
  (`TestDescriptionLayerCertification`, including the four structural tests);
  `main:skills/shared/guard-doctrine.md` §8 (the pre-rebuild text); primary
  round-count sources spot-verified at `016a210` (M119's nine rounds and the
  rounds 5–9 detail) — the gap sequence, the round-9 stop line, and the review
  override all reproduce.

**Verdict in one paragraph.** §8 survives, amended, and the replacement
falsifier is legitimate — but on a stronger ground than D-083 records. The old
falsifier was not merely gameable by the new rules; it was defective at
adoption: under the pre-rebuild "fixed and re-certified" rule, a second round
is convened exactly when round 1 finds anything, so "average multiple returns"
fires precisely when the instrument has yield. It measured yield and called it
failure, which means "retire it, don't tune it" was never a remedy the measure
could honestly command. Round 2's evidence cuts both ways and the cut is
clean: it is evidence *for* the instrument's discriminating power (a real
contradiction in shipped doctrine, invisible to 736 green tests) and *against*
the rebuilt section's mass (11 of its 13 findings were scaffolding the rebuild
itself generated). The right disposition is (e): keep the rebuilt semantics,
close the one residual two-readings hazard (reopening now has necessary
conditions but no stated sufficient one), restore a whole-step exit condition
the replacement quietly dropped, move the evidence derivations out of the
doctrine into the decision record, and run M123's remaining rounds under the
rebuilt rules with this review as the independent authorization the plan gate
lacked. Retirement, fold-into-review, and single-pass-by-fiat are each argued
against below; single-pass remains live, but as the outcome the shipped
falsifier's clause (i) decides on evidence, not one this review should decree
against its first data point.

## Answers

### 1. Does D-067's falsifier, as D-082 restored it, read as met, and with what consequence?

**Met, plainly, under the reading D-082 itself used — and defective as a
measure, in a way that determines what "owed" can mean.**

The condition is met. The restored text fires on guard-authoring milestones
"still averag[ing] multiple description-layer returns after adoption". Counting
rounds, as D-082 counted them ("the average over M116–M119 is 4.5 rounds"):
M114 4, M116 2, M117 4, M118 3, M119 9, M121 2, M123 2 — 26/7 ≈ 3.7, and
3.67 excluding M114. Every milestone that ever ran the step took at least two
rounds. On its operative reading the condition is not marginal; it is met by
every data point individually.

The condition is also defective, and the defect is structural, not a matter of
threshold. The pre-rebuild §8 (verified on `main`) reads: "The gate is entered
at zero unresolved: a discrepancy is fixed and **re-certified**, never argued
down as imprecision." Re-certification is a further fresh-context round. So
under the rules the falsifier polices, **rounds ≥ 2 if and only if round 1
returns at least one discrepancy**. "Average multiple returns" is therefore
equivalent to "round 1 usually finds something" — which is the instrument
*succeeding*. The only world in which the falsifier stays silent is one where
the fresh reader typically finds nothing, i.e., where the instrument is
worthless. The brief's suspicion is confirmed and can be stated more strongly:
the falsifier was not merely unmeetable-in-the-good-case, it was
*anti-calibrated* — it fired in proportion to yield.

Two honest caveats. First, there is a second available reading of "returns":
review returns (milestone bounces from `/milestone-review`), which is the
quantity M114's seven returns made salient when D-067 was written. Under that
reading the falsifier has never actually been measured — no one has counted
post-adoption review returns attributable to description-layer defects. But
D-082 is the standing restoration and it fixed the rounds reading; this review
takes the record as it stands and notes the ambiguity as one more defect in
the original clause, not as an escape hatch. Second, the round-count data does
capture one real failure the defect analysis must not launder away: M119's
loop terminated only by maintainer override, and an instrument whose loop ends
by override has failed structurally whatever the falsifier says. That failure
is real; it is just a *convergence* failure of the loop's rules, not a
*yield* failure of the instrument, and the rebuild is addressed to exactly it.

Consequence: the remedy came due as written, and paying it as written —
retirement — would have been obedience to a measure demonstrably measuring
the wrong thing. A falsifier binds only insofar as it measures what it claims.
The honest disposition is the one the repo took: replace the measure and put
the demonstration of its defect on the record. D-083 did that with a partially
miswired argument (see question 2); BC5 below repairs the record's ground
without editing any entry.

### 2. Is D-083's replacement of the falsifier legitimate, or the tuning D-059 forbids?

**Legitimate in substance; argued on its weaker leg; and it quietly narrows
the step's retirement exposure, which needs repair.**

The discriminating test the brief asks for — what separates "the measure was
of the wrong quantity" from a move that would excuse any inconvenient
falsifier — is this: the defect in the old measure must be demonstrable
*without reference to the new mechanism's convenience*, and the replacement
must retain at least comparable power to command retirement. Apply both:

**First test: passes, but not on D-083's stated ground.** D-083 part 2 argues
the old falsifier counts rounds and "§8's two new rules both act directly on
the round count, so the measure is satisfiable by construction by the very
rules it polices." That is true, but as stated it is an argument that the
*new rules* would game the old measure — which is a reason not to ship those
rules under that measure, not a reason the measure was wrong before they
existed. Standing alone it is exactly the move the brief worries about. The
clean leg is the one from question 1, which needs no reference to the new
rules at all: under "fixed and re-certified", the old measure fired iff the
instrument had yield, from the day D-067 wrote it. RR09 §4 saw both horns of
this ("honest-but-already-failed, or unfireable") and D-083 cites RR09 §4,
so the substance is on the record — but the load-bearing demonstration
deserves to be stated in its own right rather than reached through the
new-rules argument. BC5 has the ingestion entry record it.

**Second test: fails as shipped.** The old falsifier's consequence was
"retire **the step**". The replacement's clause (i) retires only "the rounds
after the first"; clause (ii) returns one class to round-opening. RR09's own
proposed clause (ii) ended "or the step is retired" — the shipped version
dropped that alternative, unremarked in D-083. Net: after D-083, there exists
**no stated condition under which §8 as a whole retires**. Round 1 is now
unfalsifiable. That is a real weakening of exposure enacted in the same entry
that declined to pay a fired retirement remedy, and it is the one respect in
which the replacement genuinely resembles tuning-in-the-forbidden-sense. It
is repairable by addition rather than retraction: a third clause under which
the whole step, round 1 included, retires on measured yield decay (BC2). With
that clause restored, the replacement is strictly more honest than what it
replaced: both of its existing clauses count quantities the policed rules
cannot manufacture (a finding counts where found, not where fixed; clause (ii)
counts the cost the new rules themselves create), and both are countable from
work logs as written.

One further observation, disclosed in the work log but visible nowhere in
§8's own text: clause (i) can fire across a window in which later rounds
returned genuine *in-mandate reopening findings* — a coverage gap in a
round-1 fix's assert that leaves an AC clause unpinned reopens under the
rules, yet counts in neither of clause (i)'s quantities (not shipped
behaviour, not pre-round-1 surface). The work log's correction line records
this as designed. It is a defensible design — clause (i) is a meta-judgment
that such rounds are not earning their cost even when the rules convene them
— but a future session reading §8 alone, primed by D-083's gloss ("counts
whether the later rounds still find anything the two rules above have not
already disposed of"), will mispredict when it fires. One disclosing clause
where the falsifier is stated (see recommendation 7) closes the gap.

### 3. Is round 2's yield evidence for the instrument or against it?

**For the instrument's discriminating power; against the rebuilt section's
mass. The two readings are separable, and the evidence separates them.**

The decomposition is the argument. Round 2's 13 findings, classified by the
milestone's own measurement: 4 were false claims in round 1's fix prose
(churn the certification process itself generated), 4 were §8 rules no AC
clause pins (guard-hardening of the guards over the new prose), 3 were AC1/AC4
clauses of the *rebuild's own additions* left unpinned, and exactly 2 were
defects in the artifact-as-doctrine rather than in scaffolding around the
rebuild: D9, a genuine contradiction (provenance stated as sufficient for
reopening while the mandate boundary states a second necessary condition —
opposite answers on a real class), and D3, a false docstring claim about
original text. Add the structural facts: every one of the 29 findings across
both rounds was invisible to operation — 736 tests green throughout — and ten
shipped rules could be negated in place with the suite passing.

Reading A (instrument working) is supported by the *kind* of the top
findings. D9 is precisely the two-readings defect class that sank M121, that
RR09 was convened over, and that this repo's entire failure history turns on
— found by a fresh reader in prose the author and a prior fresh reader had
both accepted. Nothing else in the toolchain catches it: not the suite, not
the harness, and (per the D-082 scoring evidence, question 4d) not the review
fan-out. On its founding purpose — descriptions that read true to their
author and are false of the artifact — the instrument demonstrably works, and
worked hardest on the hardest subject.

Reading B (work proportional to prose, not risk) is supported by the *count*.
Eleven of thirteen findings existed only because the rebuild existed: they
were defects in, or unpinned clauses of, or churn from fixing, the 116 lines
M123 added. The certification audited surface the rebuild created, the
rebuild existed to fix the certification, and each fix added prose and
asserts (700 → 736 → 744 tests) that the next round audited. That is a closed
loop in which cost tracks prose. But note what it indicts: the *section's
size and the AC8-grade guard obligation over it*, not the reader. The reader's
per-finding cost was low; the expensive part was pinning 162 lines of nuanced
prose to inversion-proof standard — an obligation imposed by the milestone's
own acceptance criteria, and one that scales linearly with every line §8
keeps.

What would distinguish the readings going forward: (1) later-round yield on
the next *ordinary* — non-self-referential — guard-authoring milestones,
which is exactly the quantity clause (i) counts; M123 is the degenerate case
where subject and instrument coincide, and generalizing from it alone would
be measuring the fixed point, the error M99's lesson names. (2) The
scaffolding share: on an ordinary milestone the certified surface is not the
instrument's own rules, so the 11-of-13 self-referential share should
collapse; if rounds 2+ on ordinary milestones still return findings mostly
about their own prior fixes, reading B wins and clause (i) will say so. The
shipped falsifier is, in other words, the correct experiment for the question
this brief asks — which is itself a point in the rebuild's favor.

### 4. What should happen to §8?

**(e): keep the instrument and M123's rebuilt semantics, with four amendments
— a sufficiency arm on reopening, a whole-step exit condition, evidence moved
to the decision record, and M123's remaining rounds run under the rebuilt
rules on this review's authority.** That is (b) plus repairs, with (c) left
to clause (i) to decide on evidence. Against the others:

**(a) Retire entirely — rejected.** Three grounds. First, the retirement
command issues from a falsifier shown anti-calibrated (question 1); paying it
as written would be obeying a measure that fired on yield. Second, round 1's
yield is real, blocking, and non-redundant: M116 9, M117 8, M118 16 (eleven
blocking), M119 2 code defects, M121 a shipped-behaviour defect plus ten, M123
16 including three invertible shipped-rule defects — every one invisible to a
green suite, and the measured behavior of the only alternative channel is to
drop the class (the D-082 scoring evidence below). Third, and specific to
this repo: cairn's deliverable *is* prose and the guards over prose. A false
record here is not documentation drift beside the product; it is a defect in
the product. Retiring the one instrument that audits the product's defining
surface, in the repo that exists to demonstrate the tracking discipline,
would be the system declining to dogfood exactly the discipline it ships.
This revises nothing in RR09 rec 9; M123's new cost evidence weighs against
the section's mass (question 5), not against the reader.

**(b) Keep exactly as rebuilt — rejected narrowly.** The rebuilt semantics
survive scrutiny (questions 6 and 7), but three defects should not ship: the
missing sufficiency arm (question 6, a live two-readings residue in the exact
place this section's failures have always lived), the missing whole-step
falsifier (question 2), and 40-odd lines of evidence derivation whose home is
the decision record (question 5). Each is a bounded amendment; none reopens
the design.

**(c) Single pass now — rejected as premature, not as wrong.** The shipped
clause (i) *is* option (c) with an evidence gate: three milestones of later
rounds yielding nothing beyond what the new rules dispose of, and §8 becomes
a single certification pass. Decreeing (c) today would preempt that
experiment against its only data point, which points the other way: M123's
round 2 — the one later round run since the rebuild was written — returned a
shipped-doctrine contradiction (D9) and a pre-round-1-surface finding (D3),
both squarely in clause (i)'s counted quantities. A round 2 that catches a
D9 is a round earning its cost. If the next three ordinary milestones show
otherwise, clause (i) retires the later rounds with a cleaner conscience than
this review could. (One consequence worth banking now: if clause (i) fires,
most of the convergence apparatus — the two-axis discriminator, the
obligations paragraph, the shield — becomes vestigial, since it exists to
govern rounds that no longer run. The retirement edit should prune the prose
with the rounds; recommendation 8.)

**(d) Fold into `/milestone-review`'s fan-out — rejected on re-examined
evidence.** Re-examining rather than inheriting RR09 §5's grounds: the
diff-anchoring leg is *weaker* than RR09 implies — for a guard-authoring
milestone the new guards, the doctrine edits, and the work-log additions are
all in `git diff main..HEAD`, so the [O] diff lens does read most of the
description layer; what it misses is pre-existing records elsewhere whose
truth the new work invalidated, and anchor fidelity in untouched files. But
the leg RR09 under-weighted is decisive and *measured*: the fan-out's scorer
gates findings at an action threshold, and M121's second pass recorded four
description-layer findings scoring 78, 78, 68, 60 — all logged, none fixed,
until the maintainer manually held the merge (D-082's Context). Add M119's
review-entry override, which made description-layer findings log-only at
review by explicit ruling. So the channel (d) would fold §8 into has a
demonstrated systematic behavior: it down-scores exactly this finding class
below the action line, and it runs after the gate, where this repo's own
precedent is to log rather than fix. Folding §8 there is retiring it with
extra steps.

### 5. Is §8's growth part of the disease?

**Partly, and separably — the growth that is disease is evidence and
rationale, not rule.**

The mechanism by which length is cost, made explicit: every line §8 keeps is
(a) read at every guard-authoring milestone, (b) guarded — 30+ asserts whose
anchors any reflow can break (the M104 trap fired during T4 on a rule this
milestone never touched), each needing registry entries and inversion
verification, and (c) certified surface whenever §8 itself is edited, where
each finding's fix adds more of (a) and (b). That last loop is D-069's regress
relocated from the work log into the doctrine, exactly as the brief suggests
— with the difference that it only spins when §8 is its own subject, which is
rare. Costs (a) and (b) recur always.

The decomposition that answers the question: round 1's measured yield depends
on almost none of the growth. The reader's mandate is the three checks and
the fresh-context framing — the original 46 lines. The 116 added lines govern
what happens *after* round 1: reopening, routing, obligations, falsifier.
Within those 116, the rules and their disambiguating sentences are
load-bearing (this section's failure history is precisely under-specified
rules read two ways — the implement gate's choice of rules-with-reasoning was
right in kind, wrong only in what it counted as reasoning). What is not
load-bearing in place is **evidence**: the record-churn grounding paragraph
(~13 lines of per-revision derivations), the M119 replay projection with its
tolerance argument (~13 lines), the clause-(i)/(ii) gloss the T8 sweep
already found fails D-071's deletion test, and scattered history clauses
("the earlier formulation alternated…"). Evidence is what D-entries are for —
D-083/D-084 already carry most of these figures — and evidence in DECISIONS
needs no inversion-proof guards, because history files sit outside the sweep
surface by §7's own rule. Moving it shrinks all three recurring costs at
once, and retires roughly eight evidence-count asserts (gap sequence,
revisions, per-case counts) with their registry entries.

Concrete smaller form (the sketch the brief asks for): keep, in order — the
diagnosis paragraph; the three checks; the zero-unresolved gate sentence; the
D-069 scope paragraph compressed (one line for M114's minutes); the two-axis
paragraph with the fix-authored-record definition, the shield-not-a-licence
sentence, and the non-removal sentence; the fix-code/pre-round-1 reopening
sentence; the mandate boundary with the criterion-clause-at-stake decider and
does-not-hold-the-gate clause; the clears-both-lines composition plus the new
sufficiency arm (BC1); the obligations paragraph and the disclosed narrowing;
the falsifier, all clauses, each with one pointer sentence naming the D-entry
that holds its derivation. Estimated ≤ 135 lines including this review's two
additions — a cut of roughly 30 lines of prose plus its guard surface, with
every disambiguator retained. This is certification-cost repair under the
brief's framing; D-057's door stays shut — nothing here re-opens stock-side
size governance, and the ground throughout is measured certification and
guard-maintenance cost, not felt weight.

### 6. Is the rebuilt rule actually free of the two-readings defect RR09 found?

**Free of RR09's specific defect; not free of a successor, smaller but live:
reopening has necessary conditions only, and no sentence makes any finding
sufficient to reopen.**

First, the checks that pass. The operative noun is fixed: "fix-authored
record" is defined in one paragraph, enumerated (docstring, comment, work-log
line, record claim), bounded in the same paragraph ("A fix's code, its
asserts and its fixtures are not records…; so does every record that existed
before round 1"), and the definition's relative clause cannot be detached
(reading "any docstring whatever" is blocked two sentences later by
pre-round-1 records reopening "no matter who wrote it"). The
sufficient-for-reopening misreading round 2 found (its D9) is closed by the
shield-not-a-licence sentence. The D-069 collision is closed by the
non-removal sentence ("being a fix-authored record never removes it from the
certified scope"). The check-1 overlap is settled by definition ("What
decides is whether a criterion clause is at stake, never how the finding is
phrased"). I attempted the standard adversarial derivations — multi-subject
findings, a false fix-authored claim about shipped behaviour, a finding
failing both lines at once — and each resolves to one rule.

The residue, naming the sentences as the question requires. The D9 fix
removed *all* sufficiency language from the section. What remains is: "**A
finding reopens a round only if it clears both lines**" (only-if — necessary
conditions); "That is a shield and never a licence — it says which findings
cannot reopen a round, **and never that anything else must**" (an explicit
denial that the provenance rule supplies a must); and the obligations
paragraph's "A **reopening finding** obliges a further fresh-context round" —
which assigns the obligation to a class *whose membership no sentence
defines*. The intended iff is carried only by implicature ("Failing either,
it is fixed under the obligation named below and the round **still**
closes"). A careful, motivated later reader — and this repo's record shows
motivated literalism is the live threat: M121's gate entry rested on "a
prospective argument the shipped rule nowhere provides", and D-079 was
"authored by the session whose loop it excuses" — can derive: every sentence
about reopening states what cannot or need not; none states what must;
therefore fixing everything in place and closing at round 1 is compliant.
That is an incompatible rule derivable from the shipped text against its
plain intent, in exactly the load direction (loop fatigue) where it will be
reached for. It is smaller than RR09's defect — one of the two readings
requires effort against context, where M121's two readings were each locally
natural — but this section, of all sections, does not get to rely on readers
declining an available self-serving reading. One sentence closes it (BC1):
clearing both lines is what *makes* a finding a reopening finding, and the
obligation follows. Placed in the composition paragraph, not the shield
paragraph, so the shield-not-a-licence sentence stays exactly true.

### 7. Is the mandate boundary sound?

**Sound, on both concerns, with one disclosed coin-flip and one prose hazard.**

Decidability. The boundary's decider — is an acceptance-criterion clause at
stake — is the same judgment check 1 already performs, exercised by a reader
holding the AC list; it adds no new faculty. The out-of-mandate enumeration
is qualified correctly ("a fixture weak on an axis **no criterion names**"),
so the vacuous-assert case (an AC-pinning assert made hollow by its fixture)
lands in-mandate via check 1's "actually pins it", as it should. M123's own
replay of M119 found exactly one genuine coin-flip in nine rounds (round 6's
`kind`-label gap, carried in the shipped prose with a ±1 tolerance) — and its
disagreement with RR09's tolerance placement (RR09 put the ±1 on round 5) is
recorded with a derivation from M119's own AC clauses, which is the stronger
basis. One coin-flip per nine rounds, disclosed with tolerance, is acceptable
decidability. The boundary's real dependency is upstream: it is only as
decidable as the AC set is precise, which is what the criteria audit (D-067's
first instrument) exists to secure — the two instruments compose rather than
gap. The incentive concern (an author wanting fewer rounds wants narrower
ACs) is blocked by sequencing: ACs are cut and fresh-context-audited at plan
time, before anyone knows what certification will find.

Does routing mean fixed? Yes, and the reason is worth stating because it
looks like a gap and is not. §§1–7 carry no gate of their own, but the routed
finding never leaves §8's gate: "the zero-unresolved bar is met when every
discrepancy has been fixed **under the obligation its own class carries**" —
so an out-of-mandate finding left unfixed is an unresolved discrepancy and
holds the gate like any other. What the routing removes is only the
confirming *round*; confirmation is by operation (harness, sweeps, suite),
which is the channel the founding diagnosis says self-corrects, applied to
the finding class (executable-surface robustness) for which that diagnosis
holds. The residual risks are two, both small: "it does not hold the gate",
quoted alone, invites the misreading that the *fix* is optional pre-gate —
the resolving clause is in the same sentence, but the phrase is the kind that
gets quoted alone (the compression pass should keep them welded); and a
session could try to *bank* a routed finding as a candidate row under the
"ordinary milestone work" phrasing — blocked in substance because a finding
on the milestone's own deliverable is in-scope by construction and unfixed
means unresolved, but "recorded and fixed" is doing quiet load there. Neither
rises to a binding criterion; both belong on the compression pass's checklist.

## Beyond the brief

- **B1 — The falsifier defect was auditable at adoption, by the instrument
  adopted beside it.** D-067 adopted the criteria audit — two questions, "what
  state of the world satisfies this exactly as written" and "is that state
  reachable" — in the same entry that adopted §8's falsifier, and the
  falsifier was never put through them. Asked at adoption, question one
  answers "a world where round 1 finds nothing", and the defect is visible
  before it costs three D-entries and two reviews. Falsifier clauses in
  doctrine and D-entries are binding criteria with a delay; they should get
  the same two-question audit at authoring time (recommendation 9).
- **B2 — Clause (ii)'s dropped retirement alternative.** RR09's proposed
  clause (ii) ended "or the step is retired"; the shipped clause ends at
  returning the class to round-opening. The shipped form is more determinate
  (the "or" left the chooser undefined — a defect RR09's criteria were prone
  to), but the narrowing of exposure went unremarked in D-083. BC2's
  whole-step clause restores the exposure on the correct axis; the ingestion
  entry should note the divergence so it reads as chosen, not slipped.
- **B3 — A disclosed-enumeration gap in the synonym guard.**
  `test_the_class_is_never_called_by_a_synonym` checks its second direction
  via four hard-coded paragraph markers. A *new* §8 paragraph stating a rule
  about the class by synonym, containing none of the four markers, escapes
  both directions. The obligations test's proxy status is disclosed in its
  comment and the module docstring (round 2's D2/D3 route); this test's
  residual enumeration is not. One comment line brings it under the same
  disclosure discipline. Low severity; it is §3's enumeration shape, disclosed
  nowhere, in a test that exists because of that shape.
- **B4 — The self-referential cost is bounded by rarity.** The 29-finding,
  two-round cost is the cost of §8 auditing §8. Milestones that edit §8 have
  happened three times in its life (M114/M115 shipping it, M121, M123); the
  recurring case is guards over other prose, where the certified surface and
  the instrument are distinct and the regress cannot spin. The brief's cost
  framing ("an instrument whose own repair costs…") is real but should be
  priced at its frequency — and the compression in BC3 is what reduces the
  price of the next §8-touching milestone, since certification cost scales
  with the certified surface.

## Recommendations

1. **Apply** — Keep §8; do not retire, do not fold into review, do not decree
   single-pass. Grounds in question 4. (No binding criterion needed for a
   keep.)
2. **Apply** — Add the sufficiency arm: a finding clearing both lines *is* a
   reopening finding and obliges the further round. One sentence in the
   clears-both-lines paragraph, pinned and registered. (BC1.)
3. **Apply** — Restore a whole-step exit condition as falsifier clause (iii):
   the step retires whole on measured round-1 yield decay. (BC2.)
4. **Apply** — Compress §8: evidence derivations move to the decision record,
   each replaced by a pointer naming its home; disambiguating sentences stay;
   the asserts pinning moved evidence retire with their registry entries.
   Amend M123's AC5/AC7/AC8 at the ingestion gate accordingly. (BC3.)
5. **Apply** — Run M123's remaining certification rounds under the rebuilt
   rules as amended, on this review's authority — the independent sanction
   whose absence was the plan gate's reason for pinning the pre-rebuild
   rules. Record the switch in the work log citing RR10. (BC4.)
6. **Apply** — One appended D-entry at ingestion carrying: the sharpened
   wrong-quantity demonstration (question 1's iff), clause (iii) as an
   annotation narrowing D-083's falsifier claim, the evidence relocation, the
   clause-(ii) divergence note (B2), and the re-affirmation of RR09 recs 8–9
   on M123's new evidence. Append-only; no existing entry touched. (BC5.)
7. **Consider** — One disclosing clause beside falsifier clause (i) stating
   that in-mandate reopening findings on fix-authored executable surface do
   not count toward it, so a later reader predicts its firing correctly
   (question 2's last paragraph). Weigh against BC3's compression before
   adding lines; the work-log correction line already holds the substance.
8. **Consider** — Bank now, on the ROADMAP row or in BC5's entry, that if
   clause (i) fires, the retirement edit prunes the convergence apparatus
   (two-axis, shield, obligations) along with the rounds it governs, rather
   than leaving 60 lines of doctrine about rounds that no longer run.
9. **Consider** — Extend the criteria audit's two questions to falsifier
   clauses in doctrine and D-entries at authoring time (B1). Small conduct
   addition to an existing instrument, not a new mechanism; check it clears
   D-057's door before adopting.
10. **Reject** — Retiring §8 (option a): the retirement command issues from an
    anti-calibrated measure; round 1's yield is real, blocking, and
    unreplaced by any channel this repo has measured; and the repo's
    deliverable is the surface the instrument certifies. (Question 4a.)
11. **Reject** — Single pass by fiat (option c): it preempts the shipped
    falsifier's experiment against the only data point taken, which is
    nonzero in both counted quantities. Clause (i) reaches (c) honestly if
    (c) is right. (Question 4c.)
12. **Reject** — Folding into the review fan-out (option d): the scorer
    measurably down-scores description-layer findings below the action
    threshold (78/78/68/60, logged not fixed) and the channel runs post-gate,
    where precedent is log-only. Re-examined, not inherited; RR09's
    diff-anchoring leg is weaker than stated, its conclusion still holds.
    (Question 4d.)

## Binding criteria

Each criterion was asked the two questions — what state of the world
satisfies it exactly as written, and does any IP or D-entry make that state
unreachable — individually and as a set. The set requires editing no existing
D-entry (IP4/D-065 respected: everything lands in §8's prose, the tests, the
milestone file via gated amendment, and one *new* D-entry), adds no author
re-derivation step, no rubric or threshold change, and no `cairn_validate`
mechanization (D-067's standing rejections respected), and needs one operator
and no CI. BC3's line ceiling was checked against BC1/BC2's additions
(arithmetic: 162 − ~40 movable + ~10 added ≈ 132).

- **BC1:** §8 states, in the clears-both-lines paragraph and not in the
  shield paragraph, that a finding which clears both lines is a reopening
  finding and carries that class's obligation (a further fresh-context
  round). The sentence is pinned by an assert that fails when the rule is
  inverted in place and is registered in the mutation harness. Check: the
  sentence supplies the sufficiency direction (only-if becomes iff); the
  shield paragraph is unmodified by this criterion.
- **BC2:** §8's falsifier carries a third clause under which the whole step
  retires: if, totalled across the same three-milestone window, round 1
  itself returns zero shipped-behaviour defects, zero false claims in records
  predating the milestone's round 1, and zero acceptance-criterion clauses
  found unpinned, the step has stopped earning its reader and is retired
  whole (tolerance: exact zero on all three counts, totalled across the
  window). The clause is pinned and registered like the others. Check: after
  this criterion, §8 states a condition under which round 1 itself retires;
  before it, none exists.
- **BC3:** §8 at the review-entry ref is at most 135 lines from its heading
  to end of file (tolerance: 135 is a ceiling; the current count is 162), and
  contains no per-revision evidence derivation: the record-churn cases, the
  M119 replay projection, and the clause gloss each appear only as a pointer
  of at most one sentence naming the D-entry or archived record that carries
  the derivation (D-083, D-084, or BC5's entry — whichever holds it). Every
  disambiguating rule sentence question 6 names as passing (the definition,
  the shield-not-a-licence sentence, the non-removal sentence, the
  criterion-clause-at-stake decider, the clears-both-lines composition)
  survives the compression. Asserts whose only anchor was moved evidence are
  retired with their registry entries; every rule assert is kept or
  re-anchored. M123's AC5, AC7 and AC8 are amended at the ingestion gate to
  match this criterion, with the amendment recorded as gated in the work log.
  Check: section line count at the ref; grep finds no gap-sequence or
  per-revision count in §8; the named sentences present; suites green.
- **BC4:** M123's certification rounds after RR10's ingestion run under the
  rebuilt §8 as amended by BC1–BC3, and the work log records the switch in a
  line citing RR10 as the independent authorization superseding the plan
  gate's pre-rebuild pinning. The next round's report classifies each finding
  under the rebuilt discriminator (reopening / fix-authored record /
  out-of-mandate), and the gate is entered only per the amended rules. Check:
  the work-log line exists and names RR10; the round report carries the
  three-way classification.
- **BC5:** One new `cairn/DECISIONS.md` entry is appended (no existing entry
  edited) recording: (a) the wrong-quantity demonstration in its independent
  form — under the pre-rebuild "fixed and re-certified" rule a further round
  is convened iff round 1 yields at least one finding, so the round-count
  falsifier fired exactly when the instrument had yield — as the load-bearing
  ground D-083 part 2 reaches only via the new-rules argument; (b) clause
  (iii) as an addition annotating D-083's falsifier claim ("this entry is the
  one to supersede if either happens" now covers three clauses); (c) the
  relocation of §8's evidence to the decision record, carrying any derivation
  BC3 removes from §8 that D-083/D-084 do not already hold; and (d) that
  RR09's recommendations 8 and 9 were revisited against M123's two-round cost
  and re-affirmed, with the divergence from RR09's clause (ii) ("or the step
  is retired") noted as chosen. Check: one appended entry naming D-083 by id;
  `dangling id tokens` stays OK; no existing entry's bytes change.
