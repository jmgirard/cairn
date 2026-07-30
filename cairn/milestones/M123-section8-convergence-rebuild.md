# M123: Rebuild guard-doctrine §8 so its certification loop converges

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** RR10
- **Principles touched:** IP2, IP4
- **Branch/PR:** `m123-section8-convergence-rebuild` / https://github.com/jmgirard/cairn/pull/123

## Goal

Rebuild `guard-doctrine.md` §8 so its certification loop terminates on its own
stated rules rather than by maintainer override.

## Scope

**In:** `skills/shared/guard-doctrine.md` §8 — the reopening rule stated on the
reopening object, the mandate boundary, the confirmation-obligation
reconciliation, the evidence paragraph, and the replaced falsifier; the asserts
in `skills/tests/test_fresh_context_readers.py` that pin them and their
`skills/tests/test_mutation_harness.py` registry entries; the `cairn/DECISIONS.md`
entry recording every supersession the rebuild requires.

**Out:** RR09 rec 7's one-shot robustness read beside round 1 → stays the
ROADMAP candidate row it is banked on. `/milestone-implement` step 8's routing →
unchanged; §8 owns the rules and step 8 only fires it. Any repair of D-079,
D-080 or D-081's standing text → IP4 forbids it; this milestone supersedes and
never edits. Any `cairn_validate` mechanization of §8 → rejected at D-067 and
not reopened here.

## Acceptance criteria

- [x] AC1 — §8 defines the non-reopening class as description-layer records a
      previous round's fix authored (docstrings, comments, work-log lines,
      record claims); one term, defined at first use, never alternated with an
      unmarked synonym; the same paragraph states that a fix's code, asserts and
      fixtures remain round-opening. A false claim in an original record reopens.
- [x] AC2 — §8 states the two-axis discriminator: subject matter draws what is
      checked and fixed (citing D-069, D-070), provenance draws what reopens.
      Every "certified scope" occurrence in §8 is on the subject-matter axis;
      the provenance rule is nowhere called a certified-scope exclusion.
      Evidence: `grep -n "certified scope"` over §8, each hit's axis named.
- [x] AC3 — §8 states a mandate boundary: a round reopens only on a finding
      within its three named checks, and robustness observations no
      acceptance-criterion clause pins are fixed as ordinary §§1–7 and
      harness work without reopening. It states how this composes with AC1's
      rule — both lines cleared — and, per AC10, that clearing both suffices.
- [x] AC4 — §8 gives each of its three finding classes exactly one confirmation
      obligation: a reopening finding obliges a further fresh-context round; a
      fix-authored record is fixed in place and confirmed by the next round's
      reader, else by `/milestone-review`'s fan-out, with none on the author
      (D-067); an out-of-mandate observation is confirmed by operation. No
      sentence gives a class a second, and the shipped "fixed and re-certified"
      sentence is restated. Evidence: every obligation-stating §8 sentence
      enumerated with its class.
- [x] AC5 — §8's falsifier is yield-based, naming window, counted quantities and
      consequences: (i) over the next three guard-authoring milestones running
      §8, zero shipped-behaviour defects and zero pre-round-1-surface findings
      from rounds after each milestone's first retires those later rounds (exact
      zero on both, totalled; the window counts only if one milestone convened a
      later round); (ii) one in-place record fix later found false returns that
      class to round-opening (one occurrence); (iii) per AC11, a whole-step
      clause. A finding counts where it was found, never where it was fixed.
- [x] AC6 — one appended `cairn/DECISIONS.md` entry supersedes every D-067,
      D-069, D-070 or D-082 claim this rebuild changes — at minimum the
      falsifier as D-082 restored it, and D-067's zero-unresolved bar as AC3 and
      AC4 each narrow it — naming each by id, stating why retirement is not the
      disposition given the fired falsifier's unpaid remedy, and grounding
      itself against D-059 on the checkable fact that the replacement's counted
      quantity is not the round count. No existing D-entry is edited.
- [x] AC7 — §8's evidence paragraph grounds the rule on record churn, states
      that under AC1's rule alone M119's round count is unchanged, and states
      AC3's projection separately. Per AC12 the derivations live in the decision
      record behind pointers; every count carries its deriving revision, and one
      contradicting a standing D-entry claim gets its own superseding entry.
- [ ] AC8 — Every rule AC1–AC5 and AC10–AC11 add to §8 is pinned by an assert
      failing when the rule is inverted in place; a positive block also fails
      when blanked and carries its own `test_mutation_harness.py` entry, while a
      negative or heading-bounded assert registers its positive framing and
      records the by-hand check (guard-doctrine §2). The inversion sweep covers
      §8 whole, recorded in the work log naming the mutation and the test that
      reddened. Asserts whose target text is rewritten or relocated are
      re-anchored or retired with their registry entries.
- [x] AC9 — The profile's `verify` slot passes clean and `cairn_validate`
      reports no new FAIL.
- [x] AC10 (BC1) — by reference to `reviews/archive/RR10-section8-survival.md` §BC1 (D-066 choice 4): §8's sufficiency arm, pinned and registered.
- [ ] AC11 (BC2) — by reference to RR10 §BC2, amended below: falsifier clause (iii), retiring the whole step on round-1 yield decay.
- [x] AC12 (BC3) — by reference to RR10 §BC3, amended below: §8's evidence derivations relocate to the decision record behind pointers; §8 ends at ≤150 lines.
- [ ] AC13 (BC4) — by reference to RR10 §BC4, amended below: remaining rounds run under the rebuilt rules, authorized at a maintainer gate.
- [x] AC14 (BC5) — by reference to RR10 §BC5, amended below: one appended D-entry carrying the iff demonstration, clause (iii), the relocated derivations and the RR09 re-visit.

**Deviations from RR10.** All found by the mandatory pre-ingest criteria audit
(13 findings, 5 set-level) and disposed of at the 2026-07-30 ingestion gate.

| BC | Departure | Reason |
|---|---|---|
| BC1–BC5 | by reference, not verbatim | 60 lines into 7 of headroom, and `binding criteria` string-compares text that therefore cannot be compressed (S1). D-066 choice 4. |
| BC2 | clause (iii) also counts anchor-fidelity findings | as written it omits §8's third check, so a window of only anchor-fidelity findings reads zero and retires the step — the anti-calibration RR10 convicts the old falsifier of (F9); also closes the (i)/(iii) double-fire (F10). |
| BC3 | ceiling 150 not 135; §8 is 164 lines not 162; movable evidence ~23 not ~40 | RR10's arithmetic is self-contradictory: best case after its own permitted removals is 151 (F1, F2, F3). |
| BC3 | protected set widened to every §8 sentence an assert pins | its closed five omits ≥8 pinned rules, one inside a paragraph it relocates (F4). |
| BC3 | amendment list is AC3, AC5, AC7, AC8 | AC5 needs BC2's clause (iii), mandated by no criterion; AC3 goes stale when BC1 ships the iff (F6). |
| BC4 | authorized by the maintainer at this gate, not by RR10's authority | the maintainer had refused this option at the block gate; IP2 and the ingest protocol forbid an RR overriding that silently (F11). Put to them 2026-07-30 and taken. |
| BC5 | (b) reworded to "extends D-083's trigger to a third clause"; (d) records the outcome of re-visiting RR09 recs 8–9 rather than mandating re-affirmation | an appended entry cannot make D-083's "either" cover three, and asserting it would be a false record claim (F12); mandating a conclusion is not a checkable state (F13). |

## Coverage

- AC1 → T2, T7
- AC2 → T2, T7
- AC3 → T3, T7
- AC4 → T4, T7
- AC5 → T5, T7
- AC6 → T6
- AC7 → T1, T5, T6
- AC8 → T7, T8, T11, T13, T14, T15, T16
- AC9 → T8, T12, T16
- AC10 → T9
- AC11 → T9, T13
- AC12 → T10
- AC13 → T12, T16
- AC14 → T10

## Tasks

- [x] T1 — Re-derive AC7's counts per named revision; log each and any RR09/D-081 disagreement.
- [x] T2 — Two-axis discriminator and the provenance-qualified class, with AC2's grep evidence (AC1, AC2).
- [x] T3 — Mandate boundary and its "clears both" composition (AC3).
- [x] T4 — Restate the confirmation-obligation sentences, one per class, and enumerate them (AC4).
- [x] T5 — Yield falsifier and evidence paragraph (AC5, AC7).
- [x] T6 — Append the superseding D-entry (AC6).
- [x] T7 — Author and register the asserts; re-anchor the rewritten two (AC8).
- [x] T8 — Section-wide inversion sweep; suites and `cairn_validate` (AC8, AC9).
- [x] T9 — RR10's sufficiency arm and falsifier clause (iii), per the Deviations table (AC10, AC11).
- [x] T10 — Relocate the evidence derivations to a D-entry; §8 to ≤150 lines (AC12, AC14).
- [x] T11 — Re-anchor or retire every assert T9/T10 moved; re-run the sweep (AC8).
- [x] T12 — Run the next round under the rebuilt rules, classification recorded (AC13, AC9).
- [x] T13 — Pin clause (iii)'s three unpinned quantities, its tolerance and window
      scope, AC3's composition and tie-break decider, and the declarative
      falsifier sentence; register each (AC8, AC11).
- [ ] T14 — Rebuild the three defeated structural tests — the obligations proxy,
      the no-synonym check's prefix-dropping direction, defined-at-first-use —
      and fix the reflow false-red (AC8).
- [ ] T15 — Fix round 3's F10 as §8's boundary prescribes: pin the pre-M123 rules
      that invert green; append the D-entry correcting D-083 part 4 (AC8).
- [ ] T16 — Section-wide inversion sweep, then certification round 4 under the
      rebuilt rules; suites and `cairn_validate` (AC8, AC9, AC13).

## Work log

- 2026-07-30: created by /milestone-plan.
- 2026-07-30: criteria audit ([O], fresh context, authored none of the criteria) returned 12 findings + 4 set-level conflicts; 8 fixed pre-gate, 3 posed at the gate, 1 (F12, Review-section ownership) fixed to work-log recording.
- 2026-07-30: plan gate chose counting a finding where it was FOUND over counting it where it was fixed, because AC3's routing would otherwise zero AC5(i) by construction; falsified by a window closing at zero counts while the rounds demonstrably returned findings.
- 2026-07-30: plan gate chose author-re-reads-the-record over "verified by the diff and the suite" for non-reopening fixes, because a false docstring passes every suite — §8's own founding diagnosis (D-067); falsified by an in-place fix later found false, which AC5(ii) counts.
- 2026-07-30: plan gate chose one milestone over splitting rules from falsifier, because a half-rebuilt §8 leaves a record chain a later reader must reconstruct — the cost D-082 names; falsified by the plan-owned body missing the 150-line cap or the AC set proving jointly unsatisfiable at implement.
- 2026-07-30: plan gate chose the pre-rebuild §8 to govern this milestone's own certification over the rebuilt rules, because RR09 faults D-079 as "authored by the session whose loop it excuses"; falsified by the loop exceeding M119's nine rounds, at which point the maintainer override is the recorded remedy.
- 2026-07-30: chose subordinating AC3's out-of-mandate list to check 1 over a separate tie-break clause, the gate having declined the tie-break option; falsified by a finding that is neither pinned by an AC clause nor classifiable under §§1–7.
- 2026-07-30: CHECKPOINT — committed with the second criteria-audit pass (over the gate-changed AC1/AC3/AC4/AC5/AC6/AC7/AC8) still running; its findings land as a plan-owned amendment before implement starts, and this line is the honest record that the audit had not reported at commit time.
- 2026-07-30: `cairn_validate` sizing advisory WARNs at 9 acceptance criteria (>7 split tripwire); the gate chose one milestone over a split with the tripwire stated, so the advisory stands unactioned by user decision.
- 2026-07-30: criteria audit pass 2 (same [O] reader, gate-changed criteria only) returned 6 findings + 2 coverage gaps; it confirmed AC1/AC3/AC4 now compose and that AC5(i)'s count-at-discovery defeats AC3's routing, and discharged 7 of pass 1's findings by name. 5 fixed here (AC4 gains a third obligation arm for out-of-mandate surface; AC6 widens to D-082 and to D-067's rejected re-derivation step, and must state why retirement is not the disposition; AC8's blanking obligation scopes to positive blocks; T2 gains AC2's grep evidence; T6 gains T1's contradicted-figure entry).
- 2026-07-30: chose a non-vacuity floor on AC5(i) — the window counts only if at least one milestone convened a round after its first — over accepting a vacuous firing, because retiring a mechanism the window never exercised is the same inert-on-its-own-case defect RR09 charges against M121's withdrawn rule; falsified by three consecutive milestones converging at round 1, which would make the floor unreachable and the falsifier unfireable.
- 2026-07-30: CORRECTION, appended not edited (IP4): the 2026-07-30 counting-decision line above states its falsifier as "a window closing at zero counts while the rounds demonstrably returned findings". That is wrong as written — AC5(i) counts only shipped-behaviour defects and pre-round-1-surface findings, so later rounds returning findings on fix-authored surface while the window totals zero is the designed behaviour, not a falsification. The correct falsifier for that choice is a window closing at zero on both counted quantities while a later round returned a shipped-behaviour defect or a pre-round-1-surface finding. Found by criteria audit pass 2.

- 2026-07-30: implement gate — status `in-progress`, branch `m123-section8-convergence-rebuild` cut from pushed `main` at `e80c46c`; baseline suites green (skills 700, scripts 332, hooks 103). No RB tripwire fires: the milestone works UNDER IP2/IP4 and changes neither, and the one hard normative question (retire §8 vs rebuild) was settled at the plan gate on RR09's verdict (d).
- 2026-07-30: AMENDMENT (substantive, gated) — AC4's confirmation mechanism for a non-reopening record moves off the author and onto the next round's reader, or `/milestone-review`'s three-lens fan-out where no further round occurs. Ground: the criteria audit found the author re-read collides with D-067's rejection of "a mandatory re-derivation step" and with the delegation warrant's over-verification clause. The gate chose handing it to review over arguing the two cases differ. Consequence: AC6's minimum supersession list drops the re-derivation clause and gains AC4 as a second narrowing of D-067's zero-unresolved bar, since the gate is now entered with those fixes unconfirmed.
- 2026-07-30: implement gate chose review-side confirmation over an author re-read for non-reopening records; falsified by AC5(ii) firing — a record fixed in place and later found false — at a rate the author re-read would have caught pre-gate.
- 2026-07-30: implement gate chose rules-with-reasoning over compressed rules for §8's new material (~35 added lines over ~20), because this section's failure history is rules whose reasoning was left implicit being read two ways; falsified by a later editorial pass finding the added rationale never load-bearing under the D-071 deletion test.
- 2026-07-30: noted at the gate — AC4 routing confirmation to the three-lens review makes that review the source of AC5(ii)'s data, so the falsifier's second clause is now fed by the mechanism AC4 names rather than by an independent channel. Not a conflict; recorded so a later reader does not read the coupling as circular.

- 2026-07-30: T1 — revisions named for all three sources: M119's work log at `8dace78^` = `016a210`; M114 pass 8 at `a25e6dd^` (a25e6dd is `review M114: done`); M121 at `8763368^` (8763368 is `review M121: done`). All three resolve; the two previously unnamed are recorded here so AC7's counts never age from an archive summary.
- 2026-07-30: T1 — derived from `016a210`, M119 rounds 5-9 record errors / coverage gaps by round: 5 → 2/3, 6 → 4/4, 7 → 0/2, 8 → 3/2, 9 → 2/1. Totals 11 record errors, 12 coverage gaps. The gap sequence 3,4,2,2,1 reproduces RR09 §2 exactly, so AC7(a) holds on the primary source and not merely on RR09's restatement.
- 2026-07-30: T1 — derived from `a25e6dd^`, M114 pass 8 round 4 superseded a round-3 entry on four false claims and found its neighbour re-recording two observations already recorded three entries earlier; every claim's subject was that pass's own certification narrative. This is D-069's motivating case and the record-churn class's first instance.
- 2026-07-30: T1 — derived from `8763368^`, M121 §8 round 2 returned 12 findings of which 5 had round 1's fix text as their only subject; the other 7 were count and citation precision in original text. RR09 B1's figure reproduces exactly.
- 2026-07-30: T1 CONTRADICTION — D-081's Decision clause states "the supported figure is **eleven** record errors, **ten of them** in an earlier round's own fix text". Re-derivation supports the eleven and not the ten-of-eleven: `016a210` locates the authoring round for at least eight of the eleven (round 5's two in rounds 3/4's fix prose, round 6's "a change of kind, never silence" and "six of the ten signatures" in round 5's, round 8's three in round 7's, round 9's in round 8's), identifies NONE as sitting in original pre-round-1 text, and RR09 §2's table classifies all eleven as fix-authored. The "ten" traces to `8763368^`:143, where M121 round 2 asserted it without a shown derivation. D-081's own parenthetical half-concedes this. Superseding entry owed at T6 per AC7.
- 2026-07-30: T1 — AC7(b)'s projection under AC3's boundary is NOT derived here; round 6's four gaps are the ±1 classification judgment RR09 flags, and the derivation belongs beside the prose that states it (T5).

- 2026-07-30: T2 — §8 gains the two-axis discriminator and the defined term `fix-authored record`, placed after the D-069 paragraph so the subject-matter axis is established before the provenance one is drawn against it. D-069 and D-070 named by id; the paragraph states the compatibility rather than claiming a partial supersession. AC2 evidence: `certified scope` occurs exactly twice in §8 (`guard-doctrine.md:288`, `:318`), both on the subject-matter axis; the provenance rule is nowhere called a certified-scope exclusion.
- 2026-07-30: T3 — mandate boundary shipped with the "clears both lines" composition. The check-1 overlap is settled by the definition rather than a tie-break, per the plan gate: a one-directional pin leaving an AC clause unpinned is check 1 and reopens; one hardening an assert no criterion names is out of mandate.
- 2026-07-30: T4 — the universally-quantified "a discrepancy is fixed and re-certified" sentence is restated to carry only the zero-unresolved bar and the never-argued-down rule, with the three per-class obligations stated in their own paragraph. Gate-amended AC4 shipped: no obligation falls on the author, D-067's rejection cited in the prose itself.
- 2026-07-30: T4 — M104's trap hit and fixed as guard-doctrine §1 prescribes: the edit reflowed `this moves certification, not operation` across a line break, reddening a guard on a rule this milestone never touched. Fixed by re-wrapping the TARGET, never the assert.
- 2026-07-30: T4 — `test_section_requires_zero_unresolved_and_forbids_arguing_down` re-anchored to the shipped bytes and its mutation-registry block updated (AC8, brought forward from T7 because T4 is what invalidated it). Verified by inversion, not only by blanking: negating the rule to "or argued down as imprecision where the author judges it immaterial" reds the suite (failures=1, errors=1); restored and diffed byte-identical.
- 2026-07-30: T2-T4 verify — three suites exit 0 each (skills 700), `cairn_validate` exit 0, run from the repo root with exit codes captured per suite.

- 2026-07-30: T5 — the evidence paragraph ships the record-churn ground with each count carrying its revision (`a25e6dd^`, `016a210`, `8763368^`), states the provenance rule changes M119's round count by ZERO with the gap sequence 3,4,2,2,1 as the reason, and states the mandate boundary's projection separately.
- 2026-07-30: T5 — AC7(b) derived rather than restated: M119's rounds 5-9 gaps classified against M119's OWN AC1 clauses (`016a210`) puts round 5 in-mandate (the signature set and fence handling ARE AC1's two clauses, under-pinned) and rounds 7-9 out. Replay stops after round 6, saving three. DISAGREEMENT with RR09 recorded: RR09 places its ±1 tolerance on round 5's classification; the derivation puts round 5 beyond doubt and the genuine coin-flip on round 6's `kind`-label gap, since those two labels are AC1's pasted-output-or-fenced-block distinction. Shipped prose carries the tolerance on round 6.
- 2026-07-30: T5 — `test_section_carries_its_own_falsifier` re-anchored from the retired round-count falsifier to the replacement's operative rule (the quantity it counts), registry block updated (AC8, brought forward for the same reason as T4's).
- 2026-07-30: T6 — D-083 appended (append-only; no existing entry edited). Supersedes D-082 part 2's restoration of the round-count falsifier, narrows D-067's zero-unresolved bar twice with both narrowings named, annotates D-069/D-070 as compatible rather than superseded, and corrects D-081's ten-of-eleven measurement per T1's derivation. `dangling id tokens` stayed OK after the append — M115's lesson predicts a possible batch of newly-unmasked references and none appeared.
- 2026-07-30: T6 — durable-record preview for D-083 was its verbatim rendering in the authoring command immediately before the commit, not a second re-print of the same 70 lines. Recorded as a disclosed reading of D-036 rather than left implicit.
- 2026-07-30: T5-T6 verify — three suites exit 0 each, `cairn_validate` exit 0.

- 2026-07-30: T7 — 18 asserts authored for the rules AC1-AC5 add, every one registered in the mutation harness; anchors extracted programmatically from the shipped bytes rather than transcribed (M95). The file docstring's enumeration of what it pins was stale the moment the asserts landed and is corrected — §8 check 2's own failure mode, caught here rather than at certification.
- 2026-07-30: T7 — no rule needed the negative/bounded carve-out for its ASSERT: AC1's no-synonym rule and AC4's no-second-obligation rule each had a positive framing already in the prose ("That name is the only one this section gives the class"; "and no class carries two"), so both are registrable per guard-doctrine §2. AC2's every-occurrence property is the one bounded claim and takes the by-hand check.
- 2026-07-30: T8 — AC2 by-hand check (the bounded property no assert can carry): `certified scope` occurs exactly twice in §8, at `guard-doctrine.md:290` (D-069's bound) and `:320` (the compatibility clause), both on the subject-matter axis; `certified-scope exclusion` occurs zero times, so the provenance rule is nowhere called one.
- 2026-07-30: T8 — INVERSION SWEEP over §8 whole, not the diff (M117/M121). 20 rules inverted in place one at a time, suite run per mutation, restored and diffed byte-identical after each: 20/20 reddened their OWN test (failures=1 each; the accompanying errors=1 is the harness meta-test reporting the block no longer resolves, a different signal — M122). Mutations were relabel/negate/transpose, never blanking, so this proves the asserts pin the rules and not merely the text's presence.
- 2026-07-30: T8 — coverage sweep over §8 found three paragraphs with zero asserted bytes; two stated rules and gained asserts (the disclosed narrowing of the zero-unresolved bar; the record-churn grounding sentence), the third is the clause-(i)/clause-(ii) gloss, left deliberately unpinned as rationale that fails D-071's deletion test — the clauses themselves carry the rules.
- 2026-07-30: T8 — the sweep instrument was itself wrong first and is recorded as such (M122): a regex extraction of registry blocks matched only double-quoted literals and missed every entry generated with `repr()`, reporting 27 blocks and 8 uncovered paragraphs. Re-run as an AST parse over the real `Mutation(...)` calls: 42 blocks, 28 resolving inside §8, 3 uncovered paragraphs. The regex figure was never acted on.
- 2026-07-30: T7-T8 verify — skills 718 / scripts 332 / hooks 103, each exit 0 from the repo root with exit codes captured per suite; `cairn_validate` exit 0.

- 2026-07-30: §8 CERTIFICATION ROUND 1 (fresh-context [O], authored no part of this; run under the PRE-rebuild §8 per the implement gate, so every finding reopens): 16 discrepancies. All fixed, zero unresolved.
- 2026-07-30: round 1's three shipped-rule defects — AC4's three per-class confirmation obligations, most of AC5's falsifier (window, both counted quantities, clause (i)'s consequence, both tolerances), and AC3's out-of-mandate enumeration were ALL invertible in place with the whole suite green. 15 new asserts + 16 registry entries close them.
- 2026-07-30: round 1's internal contradiction (D6) — §8:290 put a record about a certification round OUTSIDE the certified scope while §8's new :319 said a fix-authored record "never leaves" it; a work-log line round 3's fix wrote about round 2's finding satisfies both. Restated as a non-removal rule ("being a fix-authored record never removes it from the certified scope"), so D-069 still operates on its own axis and the two no longer collide.
- 2026-07-30: round 1's D8 — D-083 part 3(a) claimed the mandate boundary means such a finding "does not hold the gate", which §8 nowhere said; §8 said only "does not reopen". §8 now states the gate clause explicitly, which is what makes D-083's claim true rather than the other way round.
- 2026-07-30: round 1's D15 — §8 sourced a universal ("none of them sitting in text that existed before round 1") to `016a210`, which T1's own line records as locating eight of eleven. Restated to what the revision establishes.
- 2026-07-30: round 1's D4, the finding that matters most — my T8 sweep claimed "§8 whole, not the diff" and inverted 20 rules, which is exactly 18 new + 2 re-anchored, i.e. the diff. §8 carries 30 asserts. The certifier's own 45-inversion sweep found 12 survivors mine could not have reached. M117's lesson as extended by M121 says invert the SECTION, not your diff; I re-committed the error in the milestone that ships the rule.
- 2026-07-30: T8 SWEEP RE-RUN over §8 whole — 47 rules inverted one at a time, suite run per mutation, restored and diffed byte-identical after each. First pass: 41/47 red, 6 green. Four of the six were my own mutation anchors failing to match (ANCHOR-NOT-UNIQUE, so untested rather than verified) and were corrected; two were REAL survivors, both in structural tests I had written that same hour.
- 2026-07-30: the two real survivors, each a defect in its own guard. `test_the_class_is_never_called_by_a_synonym` searched case-sensitively, so a synonym at the start of a sentence ("Fix-authored text is still read") escaped it — fixed with `re.I`. `test_exactly_three_confirmation_obligations_are_assigned` counted known obligation PHRASINGS, so a fourth obligation worded any other way was simply not among the phrasings counted — the enumerate-the-renderings failure guard-doctrine §3 names, reproduced inside the check for it. Rewritten to count the paragraph's own structure (bold class labels, and mentions of the author) instead of a phrase list. Final: 47/47 red.
- 2026-07-30: AC4 evidence (owed by the criterion, absent until round 1 asked for it) — every §8 sentence stating a confirmation obligation, with the class it governs: "obliges a further fresh-context round" → reopening finding; "confirmed by the next round's reader ... otherwise by /milestone-review's three-lens fan-out" → fix-authored record; "no confirmation obligation falls on the author" → negative, scoped to that same class; "confirmed by operation: the harness, the sweeps and the suite" → out-of-mandate robustness observation; "this class's obligation is discharged by operation rather than by a further round" → the same class restated in the boundary paragraph, not a second obligation. Three classes, three obligations, none on the author.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T2 line above records AC2's evidence as `guard-doctrine.md:288` and `:318`. The shipped occurrences are at `:290` and `:320`; the T8 line has the correct pair. Found by round 1 (D12).
- 2026-07-30: D-084 appended, correcting two measurement claims in D-083 rather than editing them (IP4, D-065): §8 grew +116 lines (46 → 162), not the "roughly 60" D-083 states and not the "~35" the implement gate projected; and the "M118 16 of which eleven were blocking" figure is sourced to `c76fa65^`, which D-083 does not name. D-083's decision is untouched. The general cause is the one already in the rulebook — settle numeric records last (guard-doctrine §6); D-083 was appended at T6, three tasks before the content stopped moving.
- 2026-07-30: round 1 verify — skills 736 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0, `dangling id tokens` OK after both D-entry appends.

- 2026-07-30: §8 CERTIFICATION ROUND 2 (second fresh-context [O], did not run round 1; still under the PRE-rebuild rules): 13 discrepancies. All fixed, zero unresolved. It verified round 1's substantive fixes reproduce, confirmed D-084's two corrected measurements are true at HEAD, and independently re-derived every count and revision §8's evidence paragraph cites.
- 2026-07-30: round 2's contradiction (D9), the one that mattered — §8:305 stated provenance as SUFFICIENT for reopening ("a finding is grounds for a further round unless its only subject is a fix-authored record") while the mandate boundary states a second necessary condition; for an out-of-mandate finding on original text the two sentences gave opposite answers. Restated negatively: the shield says which findings cannot reopen and never that anything else must. A shield-not-a-licence sentence is now shipped and pinned.
- 2026-07-30: round 2 found ten §8 rules inverting green, seven now pinned (the shield's cost clause, the forward reference's loose restatement of the exactly-one rule, the D-070 compatibility sentence that D-083 part 4 rests on, and three evidence counts the docstring had claimed were locked). 744 tests.
- 2026-07-30: round 2's D4 and D6 — both structural tests I wrote in round 1 were defeatable. The synonym check keyed on the prefix, so a synonym DROPPING it ("A shielded record is still read") was unreachable; it now checks both directions, including that every paragraph stating a rule about the class names it in full. And AC1's "defined at first use" was a placement property nothing pinned: moving the definition paragraph to the end of the file left every anchor matching and the suite green. A paragraph-index test now pins it.
- 2026-07-30: round 2's D2/D3 disclosed rather than closed — AC4's "no sentence in §8 assigns a second obligation" is section-wide, and the structural test is paragraph-scoped and structure-proxied, so an unbolded sentence adding an obligation and naming no author escapes it. Recorded as a proxy in the test comment and in the module docstring, per guard-doctrine §2's by-hand-check route, rather than papered over with a phrase list — a phrase list is what round 1's version of this same test already failed at.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the two lines above recording AC2's evidence (`:187` "exactly twice ... :288 and :318", and the `:202` correction naming ":290 and :320") are BOTH now false. Round 1's own fix rewrote that paragraph. Re-measured at HEAD: `certified scope` occurs THREE times in §8, at `guard-doctrine.md:290`, `:322` and `:325`, all three on the subject-matter axis; `certified-scope exclusion` occurs zero times. AC2's substance holds at all three. Found by round 2 (D1) — and it is guard-doctrine §6's settle-numeric-records-last failure occurring inside the fix for a numeric-record failure, which is the third instance in this milestone.
- 2026-07-30: CORRECTION, appended not edited (IP4) — round 1's sweep line says four survivors were "ANCHOR-NOT-UNIQUE ... failing to match". Those are opposite conditions and the line names neither the anchors nor the correction. What happened: four mutation SOURCE strings in the sweep script did not occur in the file at all (count 0, not >1), so no mutation was applied and those four rules went untested that pass; the script's label was wrong. They were corrected against the shipped bytes and the re-run gave 47/47. Found by round 2 (D8).
- 2026-07-30: CORRECTION, appended not edited (IP4) — round 1's line "15 new asserts + 16 registry entries close them" attributes all of them to the three shipped-rule defects; 9 of the 15 close those, the other 6 close the evidence counts, the revisions, the gate clause and the re-anchor. And the D6 record cites `:319` for a phrase on `:320` at the revision it describes. Both found by round 2 (D7, D13).
- 2026-07-30: round 2 verify — skills 744 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0.

- 2026-07-30: FIRST MEASUREMENT of the rules M123 ships, taken by classifying round 2's own 13 findings under them. Shielded as fix-authored records: 4 (D1, D7, D8, D13 — all false claims in round 1's fix prose). Out of mandate, routed to §§1-7: 4 (D10, D11, D12 and D5's unpinned counts — §8 rules that no acceptance-criterion clause pins). Still reopening: 5 (D2, D4, D6 are AC1/AC4 clauses left unpinned, which is check 1; D9 is a contradiction in shipped doctrine; D3 is a false docstring claim about original text). So the rebuilt rules would have cut round 2's reopening set from 13 to 5 — a real reduction, and NOT a stop: a round 3 is convened either way. Recorded because it is the honest first data point for the falsifier's clause (i), and because it shows the rules do less than a reader might assume from RR09's projection.
- 2026-07-30: round 2's fixes are themselves uncertified under the pre-rebuild rules ("fixed and re-certified"), so a round 3 is owed. Surfaced to the maintainer rather than decided here: RR09 faults D-079 as "authored by the session whose loop it excuses", and the same objection reaches a session deciding its own loop is finished. Round counts so far: 16, 13.

- 2026-07-30: STATUS -> blocked at the maintainer's call. BLOCKER: an escalated review on whether §8 should survive at all, given that its own rebuild took two certification rounds and thirteen unpinned rules to stabilise. The maintainer chose escalation over running a round 3, over entering review with the deviation recorded, and over switching this milestone to the rules it ships. Routed to `/milestone-brief`; the milestone resumes on RR ingestion.
- 2026-07-30: STATE AT THE BLOCK — all 8 tasks checked; skills 744 / scripts 332 / hooks 103 each exit 0, `cairn_validate` exit 0; §8 rebuilt at 162 lines from 46; D-083 and D-084 appended; two §8 rounds run and both closed at zero unresolved (16 findings, then 13). No acceptance criterion is ticked — AC ticks are review's under AC fencing. Nothing is pushed and no PR exists.

- 2026-07-30: blocked on RB10 — `cairn/reviews/RB10-section8-survival.md`, seven questions on whether §8 should survive, whether D-083's replacement falsifier is legitimate or is the tuning D-059 forbids, and whether the rebuilt rule is free of the two-readings defect RR09 found in M121's version.
- 2026-07-30: DEVIATION from `/milestone-brief` step 2, logged not silent — the brief is committed on the milestone BRANCH rather than on main. Every artifact it cites (the rebuilt §8, D-083, D-084, the milestone file's work log) exists only on `m123-section8-convergence-rebuild`; a brief on main would point at files main does not have, which is M115's lesson exactly. The brief pins `cafbbc1` and instructs the reviewer to read at that ref.

- 2026-07-30 (RR10 ingest): verdict is (e) — keep §8 with four amendments. Retirement, single-pass-by-fiat and folding into `/milestone-review`'s fan-out are each rejected with evidence; the fold rejection rests on a measured fact, that the review scorer down-scored description-layer findings to 78/78/68/60 and they were logged rather than fixed.
- 2026-07-30 (RR10 ingest): RR10's central contribution supersedes M123's own argument for the same conclusion. Under the PRE-rebuild rule "fixed and re-certified", a second round is convened iff round 1 finds anything — so "average multiple returns" fired precisely when the instrument had yield. The old falsifier measured yield and called it failure. D-083 part 2 reached the same verdict only via the new-rules-game-the-old-measure argument, which presupposes the rules it is defending; RR10's ground needs no reference to them.
- 2026-07-30 (RR10 ingest): RR10's one real deficiency finding against M123 — after D-083 no condition anywhere retires the whole step, so round 1 became unfalsifiable. Clause (iii) is owed (AC11).
- 2026-07-30 (RR10 ingest): RR10's live two-readings residue — reopening now carries only NECESSARY conditions, so a loop-fatigued reader can derive "nothing must reopen". The sufficiency arm is owed (AC10). This is the same class of defect RR09 found in M121's version, surviving M123's round 2.
- 2026-07-30 (RR10 ingest): PRE-INGEST CRITERIA AUDIT ([O], fresh context, authored none of the criteria) returned 13 findings + 5 set-level. Every one is disposed of in the shown "Deviations from RR10" table; none was softened silently. The set was NOT ingestible as written — S1 alone (60 lines of string-compared text into 7 of headroom, with the prescribed compression remedy unavailable) blocks it.
- 2026-07-30 (RR10 ingest): the audit's F11 is why BC4 went to the maintainer rather than being applied. RR10 directs the remaining rounds to switch to the rebuilt rules "on this review's authority", but the milestone file already recorded the maintainer refusing exactly that option at the block gate. IP2 and the ingest protocol forbid an RR overriding a recorded decision silently; `tracking-rules.md` adds that the implementing session never authors the durable verdict on the review constraining it.
- 2026-07-30 (RR10 ingest): MAINTAINER GATE — three questions put, three answered. (1) Carry BC1-BC5 by reference (D-066 choice 4) over splitting M123 or taking only the sound criteria. (2) SWITCH the remaining rounds to the rebuilt rules on RR10's grounds, REVERSING the block-gate refusal; recorded as the maintainer's call on an outside review's reasoning, not as the milestone loosening its own bar. (3) Raise §8's ceiling to 150 and move the genuinely movable evidence, over RR10's arithmetically unreachable 135.
- 2026-07-30 (RR10 ingest): plan-owned body went 142 → 157 on ingestion, over the 150 cap. Remedied per tracking-rules by rewriting the heaviest section once (Acceptance criteria, 78 → 74, every clause kept and the verbosity cut), then the Tasks section once (32 → 23, the eight completed tasks compressed to one line each). 144/149, headroom 5. No nibble-and-recount loop.
- 2026-07-30 (RR10 ingest): RR10 recs 7, 8 and 9 are `consider` and are NOT taken here — a disclosing clause beside falsifier clause (i), banking the prune-the-apparatus consequence if clause (i) fires, and extending the criteria audit's two questions to falsifier clauses at authoring time. Rec 9 needs a D-057 door check before adoption, which RR10 itself flags. Each goes to a candidate row at post-merge hygiene rather than into this milestone.

- 2026-07-30 (RR10 ingest): `binding criteria` FAILed on ingestion — "RR10 has a Binding criteria section but no parseable '- BC<n>:' item — enforcement would silently bind nothing", which is M100's fail-loud rule working. RR10 wrote its items as `- **BC1** — ` and the parser requires a `:` or `.` delimiter. Normalized the five headers to `- **BC1:** `, delimiter only, no content changed, before the artifact settled as history — the skill's own robustness rule says never to reject usable review output on formal grounds. Check now PASSes and each BC resolves through the Deviations table.
- 2026-07-30 (RR10 ingest): `sizing` advisory now WARNs at 14 acceptance criteria, up from 9. Both figures stand unactioned by the same maintainer decision recorded at planning — one milestone over a split — and the five new criteria are by-reference one-liners rather than new scope.

- 2026-07-30: T9 — the sufficiency arm ships in the clears-both-lines paragraph (AC10/BC1): a finding clearing both lines IS a reopening finding and carries that class's obligation, with the sentence saying why the rule runs both ways. RR10's residue was that reopening carried only necessary conditions, so a reader deep in a loop could derive "nothing must reopen" with every rule intact.
- 2026-07-30: T9 — falsifier clause (iii) ships (AC11/BC2): round 1 itself retires the whole step on zero yield across the window. Two deviations from RR10 applied as the Deviations table records — it counts FOUR quantities, the fourth being anchor-fidelity findings (§8's third check, which RR10's version omitted, so a window of only those findings would read zero and retire a working instrument); and §8 states that clauses (i) and (iii) cannot both fire, since (i)'s non-vacuity floor requires a round 1 that found something and (iii)'s zeroes forbid one.
- 2026-07-30: T9 — 5 asserts + 5 registry entries; all 5 redden their own test under in-place inversion, restored byte-identical after each. 749 tests.

- 2026-07-30: T10 — D-085 appended first, per the pre-ingest audit's S5 ordering (the pointers cannot point at an entry that does not exist). It carries RR10's independent wrong-quantity ground, clause (iii) as extending D-083's supersede-on-firing trigger to a third clause, the four relocated derivations, and the RR09 recs 8-9 re-visit recorded as an outcome rather than as the conclusion RR10's BC5 mandated.
- 2026-07-30: T10 — §8 compressed 183 → 150 lines, meeting AC12's ceiling exactly. Relocated: the three measured record-churn cases, the M119 gap sequence, the mandate-boundary replay projection and its tolerance, the clause gloss, M114's four-round minute costs, the seven-returns case detail, and four justification passages. Kept: every sentence an assert pins, plus the two grounding sentences the audit's F5 flagged as rules rather than evidence (the record-churn claim and the zero-round-change claim), which now stand as pointers that still state their claim.
- 2026-07-30: T11 — 8 asserts retired with their registry entries (their only anchor was relocated evidence, which BC3 licenses); 1 re-anchored; 7 registry blocks re-synced after the compression reflowed them. `test_the_class_is_defined_and_bounded_in_one_paragraph` was reddening on a reflow of prose it is not about, and is fixed by normalizing the paragraph's whitespace before the containment check — the property it tests is co-location, which is wrap-independent, so pinning the wrap there was the defect.
- 2026-07-30: T11 — SWEEP REBUILT rather than patched. The hand-authored table from round 1 had gone stale against the compressed text and reported 10 survivors, 5 of them asserts that no longer exist; patching its anchors would have left the same drift. The replacement derives its subjects from the shipped mutation registry by AST parse and mutates each by polarity substitution: 49/49 registered §8 rules redden their own test, restored byte-identical after each.
- 2026-07-30: T11 — HONEST BOUND on what that sweep proves. For a regex-anchored prose assert, editing the pinned sentence reds it whether the edit inverts the rule or merely garbles it, so this run proves each assert reacts to its own block and no more. The stronger question — can §8 be made to say the opposite WITHOUT touching any pinned block, by adding a contradicting sentence or renaming a term elsewhere — is not mechanizable, and is exactly what rounds 1 and 2 found (D2, D4, D6, D9-D12). It is left to T12's round rather than claimed here.
- 2026-07-30: T10-T11 verify — skills 740 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0; §8 at 150/150; plan-owned body 144/149.

- 2026-07-30: §8 CERTIFICATION ROUND 3 (third fresh-context [O]; the FIRST run under the rebuilt rules, per the maintainer's RR10 gate and BC4): 10 findings, classified as the rules require — 7 REOPENING, 2 FIX-AUTHORED RECORD, 1 OUT-OF-MANDATE. **The gate does not open.**
- 2026-07-30: FIRST MEASURED YIELD of the shipped rules, from a real round rather than a replay. The shield removed 2 of 10 from round-opening (both false claims in round 2's own fix prose — exactly the churn class D-085 grounds the rule on) and the mandate boundary removed 1 (two surviving mutations negating real §8 rules that no criterion names). 3 of 10, 30%. That is well short of the round-2 replay's 13→5, and it did not stop the loop — which is what this milestone's own line at the round-2 gate predicted.
- 2026-07-30: round 3's F1, a coverage REGRESSION this milestone introduced and then misreported. T10/T11 retired NINE test methods, not eight: the ninth was `test_the_class_is_never_called_by_a_synonym`, whose anchor was not relocated evidence and which had no registry entry — it was the only pin on AC1's no-unmarked-synonym clause. With it gone, "Fix-authored text is neither read nor corrected" shipped green. Restored, with the deletion recorded in its comment; verified it reds on exactly that mutation. The T11 work-log line and D-085's "with no rule removed" are both corrected below rather than edited.
- 2026-07-30: round 3's F2, the finding this milestone deferred to it and the largest one open. §8's asserts pin sentence PRESENCE, not section CONSISTENCY, so eight of ten attempted mutations negated a shipped rule without touching any pinned block, whole suite green — appending "A robustness observation outside them reopens a round on the same terms", or "Records predating round 1 are shielded on the same terms as fix-authored ones", or moving the three-checks list so "the three named checks above" is false. Six distinct AC clauses (AC1, AC2, AC3, AC5) are defeatable this way. Two mutations were caught, both by structural tests rather than by anchors — which is the shape of the remedy.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T11 line says "8 asserts retired with their registry entries ... 1 re-anchored". Nine were retired; the ninth is named above and is restored. D-085's "no rule removed" is likewise wrong as written and is superseded by this line pending its own entry.
- 2026-07-30: CORRECTION, appended not edited (IP4) — D-085 says §8 "falls from 183 lines to under 150"; it is exactly 150 (round 3 F4). The Deviations row claiming movable evidence was "~23 not ~40" is also wrong against the shipped result: 164 + 19 added − 33 removed = 150, so ~33 moved, and 150 beat the row's stated best case of 151 (round 3 F5). The extra ten came from justification passages BC3 does not name, which the row should have said.
- 2026-07-30: AC2 evidence RE-MEASURED at HEAD after the compression, which round 3 F9 found had no post-compression record: `certified scope` occurs three times in §8, at `guard-doctrine.md:287`, `:316` and `:319`, all three on the subject-matter axis; `certified-scope exclusion` occurs zero times. This supersedes all three earlier measurements in this log, each of which is now stale by relocation rather than wrong when written.
- 2026-07-30: round 3 verify — skills 741 (the restored assert) / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0; §8 at 150.

- 2026-07-30: round 3 F6 closed by SATISFYING BC1 rather than deviating from it — the sufficiency sentence was its own paragraph where BC1 says "in the clears-both-lines paragraph", so the two are merged. §8 is now 149 lines. No Deviations row is owed.
- 2026-07-30: round 3 F1, F4, F5 and F7 closed by appending D-086 (no entry edited): the "no rule removed" claim, the "under 150" figure, the movable-evidence arithmetic in the Deviations table, and the replay projection's missing revision (`016a210`). Three of the four were written by an earlier round's own fix — the churn distribution D-085 grounds the provenance rule on, produced once more by the milestone that ships it.
- 2026-07-30: round 3 F3 and F8 are FIX-AUTHORED RECORDS under the shipped rules — fixed in place, not reopening. F3: the module docstring said four structural properties were checked when the deletion left three; the restored ninth assert makes it true again. F8: round 2's grep line is stale by relocation, superseded by the re-measurement above rather than edited.
- 2026-07-30: round 3 F10 is OUT-OF-MANDATE and is left as §§1-7 work: two pre-M123 §8 rules (the zero-unresolved bar, the fresh-reader placement) invert green, but no M123 acceptance-criterion clause names them. Recorded, not fixed, which is exactly what the mandate boundary prescribes.
- 2026-07-30: round 3 F2 BANKED at the maintainer's call rather than fixed here — a new ROADMAP candidate row carrying the ten-mutation evidence, cross-referenced to the parked one-surface-pin row as a distinct class (that one is a rule forking across files; this is contradiction within one). M123 therefore ships a §8 that is correct and pinned against DELETION and is NOT protected against CONTRADICTION, and the record says so rather than implying otherwise.
- 2026-07-30: STATUS -> review with a stated deviation: round 3's gate verdict is REOPENING and a round 4 is owed under §8's own rules. The maintainer chose to bank F2 and enter review instead. Logged as an override, not as convergence — the three-lens fan-out still reads the diff independently before anything merges.
- 2026-07-30: round 3 close verify — skills 741 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0; §8 at 149; plan-owned body under cap.

- 2026-07-30: REVIEW RETURN 1 — status back to `in-progress`. **Exactly what failed:** AC8 (every rule AC1-AC5 and AC10-AC11 add is pinned by an assert failing when the rule is inverted in place) — falsifier clause (iii) has three of four counted quantities, its tolerance and its window scope unpinned; AC3's composition sentence and tie-break decider unpinned; AC1's no-synonym and defined-at-first-use rules both defeatable; the falsifier's declarative sentence unpinned. AC11 (BC2 requires clause (iii) "pinned and registered like the others") fails on the same evidence. AC13 (BC4 requires "the gate is entered only per the amended rules") fails because round 3 returned a reopening verdict and the gate was entered anyway.
- 2026-07-30: the criteria are NOT reinterpreted to fit what shipped. AC8 is right and the work fails it; that is a return, not an amendment. The three unticked boxes go back through implement, and the 12 actioned findings are the work.
- 2026-07-30: the return is the milestone's own instrument working. Every ≥80 finding is in §8's own three checks, and five were confirmed by mutating the suite rather than argued — including one that reproduces, in clause (iii), the exact defect round 1 found in clause (i). The section certifies its author no better than it certified M121's.
- 2026-07-30: thrash rule — this is return 1 of this milestone; neither trigger (a) nor (b) fires. Work-log return count: 1.

- 2026-07-30: AMENDMENT (minor) — four tasks added for the return's work (T13 pinning gaps, T14 structural tests, T15 F10 + the D-083 correction, T16 sweep + round 4), Coverage extended to map AC8/AC9/AC11/AC13 onto them. Paid for by compressing the twelve completed task lines in one pass (25 lines for 16 tasks); plan-owned body 146/149. No criterion or scope text changed, so no gate is owed.
- 2026-07-30: return-1 findings REPRODUCED before fixing, not taken on the review's word — A3 (clause (iii)'s first quantity, its tolerance, its window scope), A7 (AC3's composition sentence and its tie-break decider), A19 (the declarative falsifier sentence), A4 (a prefix-dropping synonym), A5 (an unbolded earlier use) all invert or delete with the suite green; A22 reproduces the other way, a content-preserving reflow of the definition RED-ing a rule still present.
- 2026-07-30: round 3's F10 RE-DERIVED and its two named instances do NOT reproduce — negating the zero-unresolved bar in place and negating the fresh-reader placement in place each red the suite. Two other pre-M123 §8 rules do invert green: "The reader checks three things and reports discrepancies verbatim:" and "The author still runs everything". F10's substance stands, its labels were wrong, and T15 fixes what is actually green.
- 2026-07-30: A9 resolved AGAINST the record, not against the doctrine — §8 says an out-of-mandate observation "is recorded and fixed", AC3 says the same ("are fixed as ordinary §§1–7 and harness work"), so round 3's recorded-not-fixed disposition of F10 is the half that was wrong. Fixing it at T15 needs no criterion amendment; changing §8 to "recorded and routed" would have needed one.

- 2026-07-30: T13 — 5 asserts added and 1 re-anchored, 5 registry entries added and 1 updated. `test_section_carries_its_own_falsifier` now opens on the sentence it is named for; A19 was that test passing while the sentence it names was deleted. Verified by inversion, not blanking: 7 mutations (negate quantity 1, negate quantity 3, transpose the window scope, relabel clause (iii)'s tolerance, negate AC3's composition into the tie-break the plan gate declined, transpose the decider, delete the declarative falsifier) each red their OWN test, restored byte-identical after each.
- 2026-07-30: T13 verify — skills 746 / scripts 332 / hooks 103, each exit 0; `cairn_validate` exit 0.

## Decisions

## Review

Evidence gathered 2026-07-30 by command against branch HEAD, never recall.
Fan-out and merge gate below.

### Acceptance-criteria evidence

- **AC1** — §8 carries all four clauses, each resolving once: the four record
  kinds (`is a docstring, a comment, a work-log line, or a record`), the
  one-term rule, `are not records and stay ordinary round-opening surface`, and
  `reopens a round no matter who wrote it`. The no-synonym property is enforced
  structurally over §8 whole (`test_the_class_is_never_called_by_a_synonym`,
  restored at round 3 after T11 retired it in error), and reds on
  `Fix-authored text is neither read nor corrected`.
- **AC2** — both axes present and cited (`is drawn by *subject matter*` …
  `(D-069, as narrowed by D-070)`; `is drawn by *provenance*`). Grep evidence:
  `certified scope` occurs 3× in §8 (`:287`, `:316`, `:319`), all three on the
  subject-matter axis; `certified-scope exclusion` occurs 0×.
- **AC3** — mandate boundary, the §§1–7 routing, the does-not-hold-the-gate
  clause and the clears-both composition all present. The check-1 overlap is
  settled by definition, so no tie-break rule is owed.
- **AC4** — three classes, one obligation each; `no confirmation obligation
  falls on the author` present. Enumeration recorded in the work log and
  re-verified at round 3.
- **AC5** — all three falsifier clauses present, with `counts where it was
  **found**`, both tolerances, and the non-vacuity floor.
- **AC6** — `git diff main...HEAD -- cairn/DECISIONS.md` is **+267 / −0**:
  append-only, no entry edited (IP4). Four entries added; D-067 named 5×,
  D-070 5×, D-069 4×, D-082 3×, D-059 3× across them.
- **AC7** — §8 carries 5 pointers to D-085 and **zero** raw revisions or count
  sequences; the derivations sit in D-085 with `016a210`, `a25e6dd^`,
  `8763368^`, and D-086 supplies the replay projection's missing revision.
- **AC8** — 49 registry blocks resolve inside §8, 63 resolve exactly once in
  the file, 53 tests in the class. Section-wide inversion sweep: **49/49**
  registered rules redden their own test, restored byte-identical after each.
  Bound on that claim recorded in the work log and not overstated here.
- **AC9** — skills **741** / scripts **332** / hooks **103**, each exit 0 from
  the repo root with exit codes captured per suite. `cairn_validate` exit 0,
  23 checks passing.
- **AC10 (BC1)** — sufficiency arm shipped and, at round 3's F6, merged into
  the clears-both-lines paragraph so BC1 is satisfied as written rather than
  deviated.
- **AC11 (BC2)** — clause (iii) shipped with the two recorded deviations: it
  counts four quantities including anchor fidelity, and states that (i) and
  (iii) cannot both fire.
- **AC12 (BC3)** — §8 is **149** lines, under the 150 ceiling the Deviations
  table sets. Corrected arithmetic in D-086.
- **AC13 (BC4)** — the switch to the rebuilt rules is authorized by the
  maintainer at the ingestion gate, not by RR10's authority; round 3 ran under
  the rebuilt rules and carries the three-way classification.
- **AC14 (BC5)** — D-085 appended carrying all four required contents;
  D-086 corrects four of its claims by appending, not editing.

### Fan-out — three lenses, then a scorer

Three fresh-context reviewers with distinct evidence bases, then an [S] scorer
that generated none of the findings and was given the diff and the plan. 37
findings reported unfiltered; **12 scored ≥80**. The scorer independently
reproduced every MEASURED finding by mutating a scratch copy and running the
real suite.

**Actioned (≥80) — 12:**
- **A1 (93) / B1 (88) / A15 (91)** — §8 as shipped obliges a further round on a
  reopening finding; round 3 returned 7 and no round 4 ran. Disclosed in the
  work log as a maintainer override, but the Review section presented AC9/AC13
  as met with no live caveat, and RR10's BC4 requires "the gate is entered only
  per the amended rules". **AC13 unticked.**
- **A3 (92)** — MEASURED, reproduced: three of falsifier clause (iii)'s four
  counted quantities, its tolerance and its window scope all invert green. The
  identical defect round 1's D3 found in clause (i), reproduced in the clause
  added after it. **AC8 and AC11 unticked.**
- **A17 (88), A4 (85), A5 (85), A7 (84), A19 (83)** — MEASURED, all reproduced:
  the AC4 proxy does not cover its own paragraph; AC1's no-synonym rule is
  defeated by the exact mutation its own comment names as fixed; "defined at
  first use" is defeated by an unbolded earlier use; AC3's composition sentence
  and tie-break decider are unpinned; and deleting "This step carries its own
  falsifier." is green despite a test of that name.
- **A9 (82)** — §8 says out-of-mandate findings are "recorded and fixed", but
  round 3's F10 was recorded and not fixed and called exactly what the boundary
  prescribes. One of the two is wrong.
- **A2 (80)** — D-083 part 4 still carries "a fix-authored record never leaves
  the certified scope", the formulation round 1's D6 convicted, inside the
  paragraph asserting nothing in D-069/D-070 is superseded. IP4 means this is
  corrected by appending, not editing.
- **A22 (80)** — MEASURED: `test_the_class_is_defined_and_bounded_in_one_paragraph`
  matches a literal hard space, so a content-preserving reflow false-reds a rule
  still present — the M105 convention this file's own docstring states.

**Logged, below threshold — 25** (surfaced, never silently dropped, IP3):
A16 (79) AC4's "re-verified at round 3" is unsupported · A28 (74) RR10 recs 7/9
have no ROADMAP row · A26 (74) the Review section's D-069/D-070 counts mix two
counting conventions · A13 (72) D-086's over-reach disclosure omits two
removals · A25 (68) the falsifier counts a quantity the reader is never tasked
to find · A11 (68) the (i)/(iii) non-conflict proof assumes rounds are convened
only by the rule · A20 (65) · A24 (62) · A18 (62) · C1 (60) the BC3 ceiling
override, routed through a maintainer gate · A6 (58) · A21 (58) · A23 (58) ·
B2 (58) · A8 (55) · A12 (55) · B4 (50) · A10 (48) · C2 (45) · B3 (40) · A27
(35, premise false — main did have an over-80 line) · B5 (35) · A29 (30) · B6
(30) · C3/C4 (20, notes not findings).

### Consistency gate

`cairn_validate` exit 0 — every check passes, including `coverage complete`,
`binding criteria`, `dangling id tokens` and `mirror agreement`. Two advisories
stand, both pre-recorded maintainer decisions: `sizing` at 14 acceptance
criteria and 12 tasks (one milestone chosen over a split, at planning and
re-affirmed at ingestion). Profile is `generic`, whose `consistency-gate` slot
names no toolchain checks — that half no-ops. No `DESIGN.md` principle changed,
so `cairn_impact` is skipped. **Returns to `in-progress` from review: 0** — the
thrash rule does not fire; the three §8 rounds were implement-phase.

