# M123: Rebuild guard-doctrine §8 so its certification loop converges

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP4
- **Branch/PR:** `m123-section8-convergence-rebuild`

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

- [ ] AC1 — §8 defines the class of finding that does **not** reopen a round as
      description-layer records that a previous round's own fix authored,
      naming at minimum docstrings, comments, work-log lines and record claims;
      the paragraph uses one term for that class, defined at first use, never
      alternating it with an unmarked synonym; and the same paragraph states
      that a fix's code, asserts and fixtures remain ordinary round-opening
      surface. A false claim in an original record still reopens.
- [ ] AC2 — §8 states the two-axis discriminator: subject matter draws what the
      reader checks and the author fixes, citing D-069 and D-070 by id;
      provenance draws what reopens a round. Every occurrence of "certified
      scope" in §8 refers to the subject-matter axis, and the provenance rule is
      nowhere called a certified-scope exclusion. Evidence:
      `grep -n "certified scope"` over §8, each hit's axis named.
- [ ] AC3 — §8 states a mandate boundary: a round reopens only on a finding
      within §8's three named checks, and robustness observations that no
      acceptance-criterion clause pins — mutation survivors, one-directional
      pins, near-miss coverage, fixture weakness — are fixed as ordinary
      milestone work under §§1–7 and the mutation harness without reopening
      certification. §8 states that a finding reopens only if it clears both
      this boundary and AC1's rule.
- [ ] AC4 — §8 assigns each of its three finding classes exactly one
      confirmation obligation: a reopening finding obliges a further
      fresh-context round; a non-reopening **record** is fixed in place and
      confirmed by the next round's reader where a further round occurs and
      otherwise by `/milestone-review`'s three-lens fan-out at the merge gate,
      with no confirmation obligation falling on the author (D-067 rejects
      instructing the author's own re-check); an out-of-mandate robustness
      observation under AC3 is confirmed by operation — the harness, the sweeps
      and the suite. No sentence in §8 assigns a second obligation to a class
      already carrying one, and the shipped sentence "The gate is entered at
      zero unresolved: a discrepancy is fixed and re-certified, never argued
      down as imprecision" is restated accordingly. Evidence: every §8 sentence
      stating a confirmation obligation enumerated with the class it governs.
- [ ] AC5 — §8's falsifier is replaced by a yield-based pair naming its window,
      both counted quantities and both consequences: (i) over the next three
      guard-authoring milestones that run §8, window closing when the third
      completes, zero shipped-behaviour defects and zero pre-round-1-surface
      findings **returned by** the rounds after each milestone's first — counted
      where a finding was found, never where it was fixed, so AC3's routing
      cannot zero it — retires those later rounds and runs §8 as a single
      certification pass (tolerance: exact zero on both counts, totalled across
      the window, and the window counts only if at least one of its milestones
      convened a round after its first); (ii) one record fixed in place under
      AC1's rule and later found false by the three-lens review or a subsequent
      milestone returns that class to round-opening (tolerance: one occurrence).
- [ ] AC6 — one appended `cairn/DECISIONS.md` entry supersedes every D-067,
      D-069, D-070 or D-082 claim this rebuild changes — at minimum the
      falsifier as D-082 restored it, and D-067's zero-unresolved bar as AC3
      and AC4 each narrow it — naming each by id. It states why
      retirement is not the disposition, given that D-067's falsifier has fired
      with its remedy owed and unpaid (D-082); and its ground against D-059 is
      the checkable fact that the replacement's counted quantity is not the
      round count, never an assertion that the change is principled. No
      existing D-entry is edited.
- [ ] AC7 — §8's evidence paragraph grounds the rule on the record-churn class
      and states separately (a) that under AC1's rule alone M119's round count is
      unchanged, each of rounds 5–9 having returned at least one reopening
      finding, and (b) what AC3's boundary projects for that same record. Every
      count carries the revision it was derived from, and a derived figure
      contradicting a standing D-entry claim gets its own superseding entry.
- [ ] AC8 — Every rule AC1–AC5 adds to §8 is pinned by an assert that fails when
      the rule is inverted in place; where the rule is carried by a positive
      block, that assert also fails when the block is blanked and carries its
      own `test_mutation_harness.py` registry entry. A negative or
      heading-bounded assert registers its positive framing phrase instead and
      records the by-hand check, never the bound (guard-doctrine §2). The inversion
      sweep covers §8 whole rather than this milestone's diff, recorded in the
      work log naming the mutation applied and the test that reddened. The two
      asserts whose target text is rewritten —
      `test_section_requires_zero_unresolved_and_forbids_arguing_down` and
      `test_section_carries_its_own_falsifier` — are re-anchored to the shipped
      bytes with their registry entries updated.
- [ ] AC9 — The active profile's `verify` slot passes clean (all three suites)
      and `cairn_validate` reports no new FAIL.

## Coverage

- AC1 → T2, T7
- AC2 → T2, T7
- AC3 → T3, T7
- AC4 → T4, T7
- AC5 → T5, T7
- AC6 → T6
- AC7 → T1, T5, T6
- AC8 → T7, T8
- AC9 → T8

## Tasks

- [x] T1 — Re-derive each count AC7 cites from a revision named per source
      (M119's work log at `8dace78^` = `016a210`; M114 pass 8 and M121 round 2
      have no named revision yet and T1 identifies theirs). Record each
      derivation and any disagreement with RR09 §2 or D-081 in the work log.
- [x] T2 — Write §8's two-axis discriminator and the provenance-qualified
      non-reopening class (AC1, AC2), engaging D-069 and D-070 by id, and
      produce AC2's `grep -n "certified scope"` listing with each hit's axis.
- [x] T3 — Write the mandate boundary and its "clears both" composition (AC3).
- [x] T4 — Restate §8's confirmation-obligation sentences so each class carries
      exactly one, and enumerate them as evidence (AC4).
- [x] T5 — Write the yield-based falsifier and the evidence paragraph from T1's
      figures (AC5, AC7).
- [x] T6 — Append the superseding `cairn/DECISIONS.md` entry covering every
      D-067/D-069/D-070/D-082 claim T2–T5 changed, plus any standing D-entry
      figure T1's re-derivation contradicts (AC6, AC7).
- [x] T7 — Author the asserts for AC1–AC5's rules, register positive blocks in
      the mutation harness, record the by-hand check for negative and bounded
      ones, and re-anchor the two rewritten asserts (AC8).
- [x] T8 — Run the inversion sweep over §8 whole and record it; run the three
      suites and `cairn_validate` (AC8, AC9).

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

## Decisions

## Review
