# RR09: Is §8's new scope exclusion sound? (M121)

- **Date:** 2026-07-27
- **Brief:** `cairn/reviews/RB09-section8-scope-exclusion-soundness.md`
- **Materials read:** `skills/shared/guard-doctrine.md` §8 (working tree,
  branch `m121-verification-triage`); `cairn/DECISIONS.md` D-067, D-069,
  D-070, D-079; M119's full work log at `8dace78^:cairn/milestones/M119-…md`
  lines ~99–125; `cairn/milestones/M121-verification-triage.md` (Work log and
  Review); `cairn/references/prompting-opus-5.md` § extracts;
  `skills/tests/test_fresh_context_readers.py` §8 asserts.

**Verdict in one paragraph.** The exclusion's behavioral content — a finding
whose only subject is description-layer prose a previous round's fix authored
is fixed but reopens nothing — is defensible and worth keeping. The shipped
formulation of it is not: it is framed on the wrong object ("certified
scope"), which puts it in unacknowledged contradiction with D-070; its
operative noun is undefined between two readings whose consequences are
exactly objection B's two horns (one reading is provably inert on M119, the
other reproduces the withdrawn round-bound's round-5 stop and would also
shield fix-introduced code bugs); its measurement paragraph presents M119's
nine rounds as its supporting evidence when the exclusion changes that case's
round count by zero; and its re-armed falsifier is wrong under either
reading. All of this is repairable by restatement, and D-079 is unmerged so
the D-entry may still be amended in place. The repair is specified in the
binding criteria.

## Answers

### 1. Does the exclusion contradict D-070?

**As shipped, yes — but in its framing, not in its substance, and the framing
is what a later reader applies.**

The contradiction. D-070 drew the certified-scope line on subject matter:
"rounds 1–3 found real defects in records about the work, each fixed and
confirmed; round 4's discrepancies were in certification narrative alone" —
records *about the work* are inside the certified scope, and only narrative
about the certifying process is outside it. M119's rounds 5–9 record errors
("six of the ten signatures" is seven; "a change of kind, never silence" is
false for a signatureless quoted fence; "git's actual path prefix"
overstated) are substantive claims about the shipped detector's behavior and
coverage — records about the work in D-070's own terms. D-079 clause 1's
heading sentence reads "**§8's certified scope excludes** text a previous
round's own fix authored", and §8's paragraph opens "The exclusion extends
to…", where "the exclusion" is the previous paragraph's D-069
certified-scope exclusion. So the shipped text removes from the certified
scope a category D-070 explicitly placed inside it, on a new axis (who wrote
it, when) that D-070's axis (what it is about) does not recognize — and it
never names D-070. Under cairn's supersede-don't-ignore rule that is illegal
as shipped: objection A is confirmed.

The reconciliation. The contradiction dissolves once the rule is stated on
the object it actually governs. The excluded findings are *still checked and
still fixed* — §8's own words: "It is still fixed … leaving one unexamined
would ship it." Text that must be examined and repaired has not left the
certified scope in D-069/D-070's sense; what it has lost is only the power
to force another round. Those are two different objects, and D-079's own
sentence "the scope of what reopens a round is a different object" contains
the insight without applying it. The discriminator, in a form writable into
§8:

> Two lines govern a round, drawn on different axes. **What the reader
> checks and the author fixes** is drawn by subject matter: the work and
> every record about the work are inside; narrative about the certifying
> process is outside (D-069, as narrowed by D-070). **What a finding
> reopens** is drawn by provenance: an in-scope finding is grounds for a
> further round unless its only subject is description-layer prose that a
> previous round's own fix authored — such a finding is fixed and confirmed
> in place. A fix's code, asserts, and fixtures carry no such shield.

With that restatement the exclusion is compatible with D-070 — D-070's
carve-back governs the first axis and is untouched; the exclusion governs
the second axis, which D-070 never ruled on. The obligation this creates:
either restate on the reopening object and *engage* D-070 by name as
compatible, or, if the "certified scope excludes" framing is kept, name
D-070 as partially superseded and carry the argument. D-079 has not merged,
so amendment in place is available (M115's precedent, per the brief's
constraints).

### 2. Objection B run to ground against M119's rounds 5–9

Classification per round, from M119's work log (`8dace78^`, lines ~113–125).
"Fix-authored" means the finding's subject text was written by an earlier
round's fix (including the round-3 mini-gate removal, which was round 3's
fix).

| Round | (ii) Record errors | (i) Code / guard-coverage findings | Was (i)'s subject fix-authored? |
|---|---|---|---|
| 5 | 2 (in round-3/4 fix prose: the removal-note inversion; the `>`-quoted-shape claim from round 4's correction) | 3 observations: six-of-ten signatures delete green (`len == 1` shape asserts); `~~~`/column-0/prefix-closing delete green; fence closing unpinned on its endpoint | Yes — the shape tests were rounds 1–3 fix work (four shapes pinned in round 2, `PASTE_SHAPES` in the round-3 removal), and fence handling was rebuilt by the round-3 removal. Co-subject: AC1's unfenced-signatures clause, which is original. |
| 6 | 4 (all in round 5's fix prose) | 4 gaps: `_span` single-line arm, preview truncation, section name, both `kind` labels — all delete/mutate green | Yes — all in code the round-3 removal authored (`_span`, the rebuilt emission path). |
| 7 | 0 | 2 gaps: one-directional line-order pin; unterminated-fence third emission site. Fix work then built `NEAR_MISS_LINES`, which found the **live `^diff --git ` false positive** | Gaps: yes (round-4 fix test; round-4/6 fix tests). The live FP: **no** — `SIGNATURE_LINES` is original T1 code. Note the FP was found by round 7's *fix work*, not returned by the round's reader. |
| 8 | 3 (all in round 7's fix prose) | 2 boundary-arm gaps: preview `>` vs `>=`; blank-line fence opener unfixtured | Yes — the preview assert and its fixtures are round 6's fix. |
| 9 | 2 (both in round 8's fix prose) | 1 gap: `NEAR_MISS_LINES` covers 5 of 10 signatures; five widenings survive, sharpest `--- a/\|+++ b/` → `---\|+++`, the forever-WARN | Yes — `NEAR_MISS_LINES` is round 7's fix, extended by round 8. |

Objection B's factual premise is confirmed: every one of rounds 5–9's
coverage-gap findings sat in text an earlier round's fix authored. Now the
two readings of the shipped rule:

**Reading 1 — "record" governs (exclusion reaches the description layer
only).** Coverage gaps are findings about executable surface — asserts,
fixtures, code — not records, so they reopen regardless of who authored the
surface. Every round 5–9 returned at least one such finding (3, 4, 2, 2, 1).
**The loop replays identically: no round is saved, the loop still fails to
converge at round 9 (round 9's gap would open a round 10), and it still
ends only by maintainer override. No finding is lost.** This is the inert
case the brief names, and it is a finding: on its own motivating
measurement, the exclusion changes nothing. The re-armed falsifier fires
again on the next M119-shaped milestone exactly as it fired on M119.

**Reading 2 — "text" governs (exclusion reaches anything a fix wrote,
fixtures and asserts included).** Round 5's findings then all have
fix-authored subjects: the loop stops at round 5 — **the exact stopping
point of the withdrawn round-bound's first reading, which D-079 records as
unacceptable** ("if guard-coverage gaps are not shipped-behaviour defects
it fires at M119's round 5, discarding nine later gaps"). Lost: round 6's
four gaps, round 7's two gaps *and* the near-miss control whose
construction found the stretch's only live shipped-behaviour defect, round
8's two boundary arms, and round 9's forever-WARN widening set. (It
arguably stops even earlier: round 2's principal defect — round 1's fix
fitted to the easy shape — also had a fix-authored subject.)

So the shipped rule's two readings are objection B's two horns exactly, and
the horn selection is performed by the undefined noun question 6 flags. The
one caveat to the objection: under reading 1 the rule is inert on *round
count* but not on *obligation* — the eleven record errors are fixed in
place instead of fixed-and-re-certified, which is a small real change to
what each round must confirm. It saved M119 zero rounds because no round
5–9 was opened by record errors alone.

### 3. Is objection C's regress real?

**Only under reading 2 — where it is worse than the objection states.
Under reading 1 it fails.**

Under reading 2, after round 1 nearly all newly produced bytes are
fix-authored, so rounds ≥2 are confined to pre-round-1 leftovers — and,
worse than objection C notes, a *code regression introduced by a fix* could
not reopen a round either, since its subject is fix-authored text. That is
a certification instrument that cannot re-examine the repairs it forces:
structurally broken.

Under reading 1, rounds ≥2 retain a substantive class, and it is the class
M119 actually exercised:

- anything in the pre-round-1 work or records that round 1 missed;
- shipped-behaviour defects, coverage gaps, and weak fixtures *introduced
  by any round's fix* — executable surface is never a "record". This is
  M119 rounds 2–4's yield (round 1's fix fitted to the easy shape; the
  fixtures the removal dropped) and rounds 5–9's gap findings;
- claim-vs-file and anchor-fidelity errors in original records.

What reading 1 removes is exactly one class: record errors in prior fix
prose. Composed with D-069 the exclusions are additive and bounded — D-069
removes round *reports*, this removes fix *prose* — and the deliverable,
its original records, and all fix code remain round-opening surface. That
is not a round bound by another route. But the conclusion is conditional on
BC1: the shipped prose does not choose reading 1, and under reading 2
objection C is essentially proven.

### 4. Is the falsifier still measurable?

Under reading 1 the falsifier stays measurable and is *not* mechanically
suppressed — the exclusion is inert on round counts, so an M119-shaped
milestone still averages multiple returns and the falsifier fires. But that
is its own indictment: the re-armed clause ("if guard-authoring milestones
still average multiple returns with this scope in force, retire the step")
then commits §8 to retirement on the next M119-shaped milestone, because
the scope change bought nothing against the measurement that fired it.
Under reading 2 the falsifier is suppressed exactly as objection C says:
rounds collapse whatever the description layer's quality, and "average
multiple returns" becomes unreachable by construction. Either way the
re-armed falsifier is wrong — honest-but-already-failed, or unfireable.

**Proposed replacement** (yield-based, not round-based, so the exclusion
cannot satisfy it mechanically):

> Measured over the next three guard-authoring milestones that run §8,
> window closing when the third completes: (i) if the rounds after each
> milestone's first return, in total across the window, zero
> shipped-behaviour defects and zero in-scope findings whose subject is
> pre-round-1 surface, the rounds after the first have stopped earning
> their cost — retire them and run §8 as a single certification pass
> (tolerance: exact zero on both counts). (ii) If any record fixed in
> place under the exclusion is later found false by the three-lens review
> or a subsequent milestone, the fix-in-place clause has failed — that
> finding class returns to round-opening, or the step is retired
> (tolerance: one occurrence suffices).

Clause (i) measures whether continued rounds find anything the exclusion
did not already dispose of; clause (ii) measures the cost the exclusion
newly created — uncertified in-place fixes — which the old falsifier never
saw. Both are countable from work logs as milestones already write them.

### 5. What should M121 actually ship?

**(d): keep the exclusion, rebuilt — option (a)'s shape with four
amendments and one addition.** Specifically:

1. **Restate on the reopening object, description-layer only, engaging
   D-070** (BC1–BC3). This resolves objections A and C and picks reading
   1 explicitly, which also resolves question 6's misreading.
2. **Correct the measurement claim** (BC4): §8 currently offers M119's
   nine rounds as "the measurement" for a rule that would have changed
   that case's round count by zero. Its honest evidence base is the
   record-churn class: M114 pass-8 round 4 (via D-069), M119's ten
   fix-text record errors now fixed in place rather than
   fixed-and-re-certified, and M121's own round 2, where five of twelve
   findings had round 1's fix prose as their only subject. The rule is a
   convergence guarantee against prose churn, not a remedy for M119's
   round count, and the prose must say so.
3. **Reconcile "fixed and re-certified" with "fixed in place"** (BC5).
   The section currently carries both obligations with no rule for which
   finding gets which; see also Beyond the brief, B2.
4. **Replace the falsifier** per question 4 (BC6).
5. **Add the mandate boundary** (BC7): a round reopens only on findings
   within §8's three named checks; robustness observations outside them —
   mutation survivors, one-directional pins, near-miss coverage, fixture
   weakness beyond what an AC clause pins — are recorded and fixed as
   milestone work under §§1–7 and the mutation harness, and do not reopen
   certification. This, not the exclusion, is the piece that answers
   M119's round count: rounds 6–9 were §8 doing the mutation harness's
   job by hand. M119's own round 5 called these findings "out-of-scope
   observations" before taking them; the stretch's one live defect (the
   `^diff --git ` false positive) was found by a *mutation-style control
   built during fix work*, not by description-layer reading — evidence
   that this yield class belongs to §§1–7, where the doctrine already
   obliges by-hand mutation of new guards (M119's own T1 ran three).
   Projection: M119 replayed under BC1+BC7 stops after round 6 — round
   5's six-of-ten finding is in-mandate, since AC1's unfenced-signatures
   clause was pinned only by asserts any one line satisfies (check 1,
   AC-clause-to-assert coverage); round 6's findings are then four
   excluded record errors plus four out-of-mandate robustness gaps —
   saving three rounds (tolerance ±1 round: round 5's classification is
   the judgment call). What §8 then forgoes: rounds 7–9's hardening and
   the live FP. I judge that acceptable, against D-079's contrary
   declaration, on three grounds: the forgone yield is almost entirely
   hardening against hypothetical future edits, which is §§1–7 work a
   milestone owes anyway; the one live defect was of a *noisy* class — a
   false-positive WARN on ordinary prose is user-visible and routes to
   `/hotfix`, unlike a silent miss; and an instrument whose loop
   terminates only by maintainer override has already failed
   structurally, which is D-059's test, and preserving its accidental
   yield does not repair that. D-079's declaration was authored by the
   session whose loop it excuses, which is why this brief exists. If the
   maintainer declines BC7 at the gate, the Deviations table must record
   that M119's round count remains unaddressed and that BC6's falsifier
   is then expected to fire.

Against the alternatives. **(b) revert** leaves a fired falsifier
(4.5-round average) with its prescribed remedy owed and no answer; the
exclusion's convergence guarantee against pure prose churn is real (M114
round 4 beyond D-069's report-only carve-out; M121 round 2's five) and
worth keeping once correctly stated. **(c) retire outright** discards
round 1's measured yield — 9, 8, 16 (eleven blocking), 2 code defects
across M116–M119, plus M121's own round 1, which found a real
invertibility defect in the milestone's shipped rule *and* refuted the
round bound, the instrument working on its author. Folding the check into
the three-lens review does not replace it: the fan-out runs after
`status → review` and is diff-anchored, while §8 reads the whole
description layer before the gate; and M119's own override shows what
review does with description-layer findings — logs them rather than
fixing them pre-gate. Round 1 is the instrument; the unbounded loop was
the failure; retire the loop's unboundedness, keep the instrument.

### 6. Defects in the shipped §8 prose

The flagged defect is real and blocking, and it is the root of the whole
review: **the operative noun switches from "text" to "such a record"
within one sentence, undefined** ("The exclusion extends to *text* a
previous round's own fix authored: a finding whose only subject is *such a
record*…"). As question 2 shows, the two readings this licenses are
objection B's two horns — inert, or the withdrawn round bound plus a
shield for fix-introduced regressions. The flagged misreading is live
under reading 2: an AC-coverage gap whose weak assert was fix-authored
reads as excluded, so an acceptance criterion ships unpinned and §8's own
first check is self-defeating. D-079 clause 1 carries the identical
sentence and defect.

Further defects in the same paragraph:

1. **It contradicts the unamended re-certification clause.** Line ~284:
   "a discrepancy is fixed and re-certified, never argued down"; the
   exclusion: "fixed in place and opens no further round". Both are
   universally quantified over discrepancies; nothing says which governs
   an excluded finding, or who verifies an in-place fix. (M121's own gate
   entry is the first casualty — Beyond the brief, B2.)
2. **"The measurement is M119's nine rounds" misattributes the
   evidence.** The paragraph presents the nine rounds as the exclusion's
   supporting measurement, then itself concedes "Every round in that
   stretch also returned a real guard-coverage gap" — which, under the
   only sound reading, reopens every one of those rounds. The paragraph
   refutes its own efficacy claim without noticing.
3. **The anti-round-bound sentence indicts the shipped rule too.** "a
   bound on *rounds* would have discarded work that was still finding
   defects" — true, and under reading 2 the exclusion discards the same
   work from round 5, since those gaps sat in fix-authored fixtures. The
   argument does not close.
4. **"this narrows the certified scope, the object D-069 already
   narrows" is the D-070 collision** (question 1): what is narrowed is
   what reopens, not what is certified — excluded findings are still
   examined and fixed. Same defect in D-079's clause-1 heading sentence.
5. Minor: "eleven were record errors, ten of them in an earlier round's
   own fix text and round 9's two in round 8's" — the two are among the
   ten, but the sentence reads as three disjoint counts; and the
   companion assert's comment in `test_fresh_context_readers.py`
   (`test_scope_excludes_text_a_previous_rounds_fix_authored`) still says
   "eleven findings were record errors in an earlier round's fix text" —
   the eleven-vs-ten error F-A1 (88) corrected elsewhere survives in that
   comment.

## Beyond the brief

- **B1 — the exclusion's real precedent is M121's round 2, and it should
  be cited.** Five of round 2's twelve findings had round 1's fix prose
  as their only subject. That is the one measured case where the
  exclusion, correctly read, changes anything — unlike M119, where it
  changes nothing. The honest evidence paragraph writes itself from
  M114-R4 + M119's ten + M121-R2's five.
- **B2 — M121's own gate entry is not licensed by the rule it applies.**
  Round 2 returned seven in-scope findings (count and citation precision
  in *original* text). Under the unamended re-certification clause those
  seven fixes require re-certification; the exclusion governs findings,
  not confirmation obligations, and the gate entry's ground ("a round 3's
  only new surface would be round 2's own fixes") is a prospective
  argument the shipped rule nowhere provides. BC5's reconciliation makes
  the practice legal going forward (in-place and in-scope fixes confirmed
  by operation — diff and suite — with a fresh round owed only for new
  in-scope findings); until it ships, M121 either owes a confirmation
  pass on those seven fixes or must record the deviation at its gate.
- **B3 — D-079's Consequences re-arm the falsifier against a measurement
  its clause 2 does not touch but its clause 1 distorts.** Worth one
  sentence in the amended entry: the falsifier's unit is "returns", and
  the exclusion changes what counts as grounds for a return, so the old
  and new averages are not commensurable. BC6's yield-based falsifier
  sidesteps this.

## Recommendations

1. **Apply** — Restate the exclusion on the reopening object,
   description-layer only, with the two-axis discriminator engaging
   D-069/D-070 by name; amend D-079 in place (unmerged; M115 precedent)
   so clause 1 and its heading sentence no longer say "certified scope
   excludes", and so the entry names D-070 and carries the
   reconciliation. (BC1, BC2, BC3.)
2. **Apply** — Correct §8's measurement paragraph: state that on M119's
   record the exclusion changes the round count by zero, and ground it on
   the record-churn class (M114-R4, M119's ten, M121-R2's five). (BC4.)
3. **Apply** — Reconcile the re-certification clause with fixed-in-place;
   state how in-place fixes are verified (operation: diff and suite) and
   which findings oblige a further fresh-context round. (BC5.)
4. **Apply** — Replace the re-armed falsifier with the yield-based pair
   in question 4. (BC6.)
5. **Apply, gate-eligible** — Add the mandate boundary routing
   out-of-mandate robustness findings to §§1–7/harness work without
   reopening certification; if the maintainer declines it, the Deviations
   table records that M119's round count is unaddressed and BC6 governs.
   (BC7.)
6. **Apply** — Fix the surviving "eleven … in an earlier round's fix
   text" comment in
   `skills/tests/test_fresh_context_readers.py` (the F-A1 class, third
   site). (BC8.)
7. **Consider** — A one-shot robustness read of a milestone's *new*
   guards (near-miss controls, both-orders fixtures, boundary arms) run
   once beside §8 round 1, replacing the yield rounds 6–9 produced ad
   hoc. Bounded because its subject is fixed. Weigh against the Opus 5
   guide's over-verification finding before adopting; do not adopt inside
   M121.
8. **Reject** — Reverting to §8 unchanged (option b): leaves a fired
   falsifier with its remedy owed, and discards a real convergence
   guarantee that M114-R4 and M121-R2 measure. Reason in question 5.
9. **Reject** — Retiring §8 outright (option c): discards round 1's
   measured yield (M116 9, M117 8, M118 16 with eleven blocking, M119 2,
   M121 1 shipped-behaviour + 10), which the diff-anchored, post-gate
   three-lens fan-out does not replace. Reason in question 5.

## Binding criteria

- **BC1** — `skills/shared/guard-doctrine.md` §8's exclusion paragraph
  defines the excluded class as description-layer records only, naming at
  minimum docstrings, comments, work-log lines, and record claims, and
  states in the same paragraph that a fix's code, asserts, and fixtures
  remain ordinary round-opening surface. Check: both statements present;
  the paragraph uses one defined term for the excluded class ("record",
  defined at first use) rather than alternating "text"/"record" as
  unmarked synonyms.
- **BC2** — §8 states the two-axis discriminator: subject matter draws
  what is checked and fixed (citing D-069 and D-070); provenance draws
  what reopens. Check: every occurrence of "certified scope" in §8
  refers to the subject-matter object; the provenance exclusion is never
  called a certified-scope exclusion.
- **BC3** — D-079, amended in place before merge, names D-070 in its
  body and carries either the two-object reconciliation or an explicit
  partial supersession of D-070; clause 1 no longer reads "§8's
  certified scope excludes text a previous round's own fix authored".
  Check: grep D-079 for "D-070" returns at least one hit inside the
  entry; the clause-1 sentence is restated on the reopening object.
- **BC4** — §8's measurement claim states that on M119's record the
  exclusion changes the round count by zero, because each of rounds 5–9
  returned at least one finding outside the excluded class (counts 3, 4,
  2, 2, 1; tolerance: exact), and grounds the exclusion on the
  record-churn class: M114 pass-8 round 4, M119's ten fix-text record
  errors, M121 round 2's five fix-text findings (tolerance on the three
  cited counts: exact).
- **BC5** — §8 assigns each finding class exactly one confirmation
  obligation: in-scope findings on pre-fix surface oblige a further
  fresh-context round; excluded findings are fixed in place and the fix
  verified by operation (diff and suite), not by a further round. Check:
  no two sentences in §8 assign both obligations to the same class; the
  "fixed and re-certified" sentence is qualified or restated
  accordingly.
- **BC6** — §8's falsifier is replaced by the yield-based pair: (i) over
  the next three guard-authoring milestones running §8, zero
  shipped-behaviour defects and zero in-scope pre-round-1-surface
  findings from rounds after the first retires those rounds (tolerance:
  exact zero, totals across the window); (ii) one later-found-false
  in-place fix returns the excluded class to round-opening or retires
  the step (tolerance: one occurrence). Check: the shipped falsifier
  names the window, both counted quantities, and both consequences.
- **BC7** — §8 states that a round reopens only on findings within its
  three named checks, and that robustness observations outside them are
  recorded and fixed as milestone work under §§1–7 and the mutation
  harness without reopening certification. Numeric projection: M119
  replayed under BC1+BC7 stops after round 6, saving three rounds
  (tolerance ±1 round, on round 5's in-mandate classification). If
  declined at M121's gate, the "Deviations from RR09" table records the
  decline and that BC6's falsifier then governs the unaddressed round
  count.
- **BC8** — The comment block of
  `test_scope_excludes_text_a_previous_rounds_fix_authored` in
  `skills/tests/test_fresh_context_readers.py` no longer states that
  eleven findings were record errors in an earlier round's fix text; it
  carries the ten-of-eleven split (tolerance: exact wording split, ten
  of eleven). Check: grep the test file for "eleven" returns no hit
  asserting all eleven sat in fix text.
