<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M96: Growth ratchet — the rulebook is governed by attention, not by a permitted size

- **Status:** blocked   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M94, M95   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Govern `tracking-rules.md` with a growth-since-last-editorial-pass ratchet
modelled on the `references staleness` advisory — it reports that enough has
accumulated to warrant a deliberate look, and never asserts what size is right.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A dated editorial-pass stamp recording the file's reviewed mass; an
advisory that fires when current mass exceeds the stamped mass by a stated
ratio; the escape being a performed and recorded pass, never a silent
re-stamp. First stamp is M95's pass. Plus RR03 rec 5's two items: the
editorial-pass rule the stamp references states that a pass applies M95's
placement procedure — never RR02 rec 1's "delete the defense back to its
D-entry", which M95's ledger falsified — and the rulebook preamble gains the
one-sentence inflow test, the ratchet's editorial criterion stated at the door.

**Out:**
- A level threshold on `tracking-rules.md` — the instrument RR02 Q3 rejected
  for an n=1 file with no oracle. Superseded, not deferred.
- Any change to `cairn_scripts.LINE_CAPS` / `CHAR_CAPS` or the `record density`
  advisory. **D-049 stands untouched** — it governs the item-capped files,
  where deriving mass from an item cap remains sound (RR02 Q2).
- `DECISIONS.md` weight → M97 bounds its read instead; its mass is legitimate.
- The soft offset norm ("a milestone adding rulebook lines names what it
  removes") → candidate row; RR02 rec 5 says drop it if the ratchet suffices,
  so it waits on evidence from this milestone.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The stamp records a date and the reviewed mass, in one place, and is
      current knowledge corrected in place rather than an appended chain
      (D-045; the M93 accretion failure applies to this stamp by construction).
      Its per-line size is bounded by the existing `NON_ITEM_LINE_CAP` axis or
      an equivalent stated here.
- [ ] AC2: The advisory fires when current mass ≥ stamped mass × (1 + ratio)
      and is quiet below it, proven in **both** directions against the real
      file (M74), and **cannot fail the gate** — it WARNs, matching the
      `references staleness` class it is modelled on. A run on the current tree
      is recorded as evidence of which way it fires.
- [ ] AC3: The ratio is derived **through the advisory's own comparison
      operator**, and what that operator permits is stated where the ratio
      lives (`>=` permits one increment less — M87). The ratio is a tripwire
      for human attention, not a claim about correct size, and the source
      comment says so; both operands are measurements.
- [ ] AC4: The stated↔enforced coupling is pinned at **every** site the ratio
      or the stamp format appears; the site count is established by grepping
      the repo and recorded (M87: the number lived in three places while the
      guard paired two; M93: an amendment fixing a stale number is itself a
      restatement).
- [ ] AC5: Re-stamping without a recorded pass is refused or flagged — the
      escape is performing the pass, and a stamp that can be silently bumped
      governs nothing. Evidenced by a guard, not by prose alone.
- [ ] AC6: The editorial-pass rule the stamp references states that a pass
      applies the placement procedure M95's D-entry records, and the rulebook
      preamble carries the one-sentence inflow test naming what belongs in the
      file. Both guard-pinned; RR02 rec 1's superseded framing appears nowhere.
- [ ] AC7: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T4
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Choose and implement the stamp's home and format; seed it from M95's
      recorded post-pass mass.
- [ ] T2: Implement the advisory and derive the ratio through its own
      operator, with the derivation and its "attention, not size" rationale in
      the source comment.
- [ ] T3: Grep every site of the ratio and the stamp format; pair each with the
      coupling guard; record the site count in the work log.
- [ ] T4: Guards — fires above, quiet below, never fails the gate, and refuses
      an unrecorded re-stamp. Register in the mutation harness.
- [ ] T5: Amend the editorial-pass rule to cite M95's placement procedure and
      add the inflow-test sentence to the rulebook preamble; guard both.
- [ ] T6: Run the advisory on the current tree, record the direction it fires,
      and run all three suites from the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan, re-cutting M94 per RR02 rec 2. Depends on M95 (its pass is the first stamp) and M94 (RR02 rec 4: instrument before further weight machinery ships, since this is an M84-class mechanism).
- 2026-07-20: MAINTAINER DECISION at the RR04 ingest gate, recorded as D-057: the stock-side weight-governance program is closed and M96 folds to a reporting line in `/milestone`'s audit (mass + growth since stamp), with no pass machinery built. The ratchet, the derived ratio, the coupling guard and the re-stamp refusal all go — AC1-AC5 and T1-T5 no longer describe the work. Stays `blocked` pending a `/milestone-plan` re-cut to the reporting line, which is a fraction of the current plan; alternatively it is dropped and the line folded into whatever next touches `/milestone`. Decided against RR04's own preferred Q7 outcome (delta-scoped audit) on cost-data grounds — see D-057's rejections.
- 2026-07-20: RR04 ingested; RB04/RR04 archived. Stays `blocked` (not `in-progress`): rec 10 says do not build as written, and the re-cut needs `/milestone-plan`. Two decisions are the maintainer's and are surfaced at the ingest gate rather than taken here — Q9/rec 11 (close the stock-side program) and rec 6 (whether to set a mechanical budget at all, and at what number). Sweep ledger committed to `cairn/references/` as rec 9's precondition. Triage: 5 apply, 2 consider, 4 reject.
- 2026-07-20: blocked on RB04 — a redteam of the tiering + mechanization + inviolable-budget proposal, which would displace or reshape this milestone. Trigger: an independent full-file sweep found 65 line-equivalents (8.4%) of removable mass where M95 delivered −9 net, so the ratchet's escape ("perform a pass") has a remedy today but a one-time one; RB04 Q7 asks whether any stock-side mechanism is worth building. Tripwire: ip-touching (the proposal makes the always-read budget an IP and supersedes RR01 rec 15).
- 2026-07-20: amended at M95's re-cut gate (user-selected) to carry RR03 rec 5's two items, which the 2026-07-19 plan named nowhere and would have silently dropped (IP3): the editorial-pass rule states that a pass applies M95's placement procedure rather than RR02 rec 1's falsified "delete the defense back to its D-entry", and the rulebook preamble gains the one-sentence inflow test. New AC6 + T5; the verify criterion/task shift to AC7/T6 and Coverage follows.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-20 (RR04 ingest): the three-part proposal RB04 was written to test is REJECTED in its load-bearing parts. Part A (phase-tiering the cross-skill contract) — rejected; RR01 rec 15 stands on its original grounds, genuinely single-phase mass is only ~15-30 lines, and relocation costs more in coupling guards, re-anchoring (111 of 278 mutation blocks anchor in the rulebook) and drift than it saves. Part B's "strictly better" claim — false: guards enforce that prose EXISTS, not behavior; checks fire after authoring; 8 of 23 checks are unbindable WARNs; remedies are class-2 doctrine no check carries; and the prose relocates into the 1,605-line `cairn_validate.py`, off the measured surface. Part C as an IP — rejected: every prior softening was procedurally clean, so the gate is the leak, not the label, and a parameterized IP corrodes the IP class.
- 2026-07-20 (RR04 ingest): Q9's null option is rated **~80% right** and is the review's second-most-useful finding. The stock-side governance program is the dominant CAUSE of the growth it governs — the four anti-growth milestones (M92, M93, M97, M98) added +53 lines combined — the disputed mass is ~3% of per-read tokens, and the causal case for harm was never made (M94 built `cairn_cost` to measure it and nobody has let the data speak). Rec 11 would declare the program closed absent a measured `cairn_cost` regression. NOT actioned here: this is a maintainer decision, surfaced at the ingest gate.
- 2026-07-20 (RR04 ingest): Q8 answers the maintainer's central question — what mechanically stops a correct finding being softened by the session implementing it. Four mechanisms, three applied: RR "Binding criteria" ingested VERBATIM into the milestone's AC block and string-compared by a check, deviations legal only through a shown "Deviations from RR<NN>" table; mandatory projection-vs-outcome juxtaposition at review and above the merge chip (M95's −9 against RR03's 60-100 sailed through because no surface ever showed both numbers); script-measurable ACs preferred, with committed classification ledgers where judgment is unavoidable. Mechanism 3 (adjudication asymmetry — the implementer never authors the durable verdict on the review constraining it) applies as one sentence, RR04 stating honestly that it is the weakest of the four because it is prose-enforced.
- 2026-07-20 (RR04 ingest): what the record shows does NOT work, per RR04 — prose ACs interpreted by their implementer (M95, twice); the review fan-out as an independence mechanism (same lineage, orchestrator-spawned reviewers, self-composed gates — called theatre in Q5); recording a constraint at higher principle strength (Q4); and commissioning another Fable review, this being the fourth.
- 2026-07-20 (RR04 ingest): RR04 lands a finding against this session's own conduct, recorded rather than softened — the 2026-07-20 classification sweep was a fourth unaudited agent classification with no committed artifact, produced by the same session that authored the proposal, and RB04 then embedded its verdict as fact ("D-056's inference is therefore wrong"), structurally the move the brief indicts. It also corrects the overstatement: D-056's headline claim is CONFIRMED by the sweep (90.6% operative); only the yield clause is contradicted. The ledger is now committed at `cairn/references/rulebook-classification-ledger.md`, satisfying rec 9's precondition.
- 2026-07-20 (RR04 ingest): D-056 is to be superseded NARROWLY, not wholesale — its part 1 (rulebook is current knowledge) and part 3 (guard-pinning as deletion screen) stand; what changes is the yield clause and the test's structure (add step 0 for single home, split deletion/placement from inversion/guard-verification). Not actioned here: it needs a milestone, and the maintainer's Q9 call decides whether that milestone happens.
- 2026-07-20 (RR04 ingest): M96 as written is NOT to be built (rec 10). Re-cut to a delta-scoped audit — stamp + advisory stand, but the mandated pass reviews only lines added since the stamp; fallback if the maintainer takes Q9 fully is to fold it to a `/milestone` audit reporting line with no pass machinery. Status stays `blocked` rather than returning to `in-progress`, since the brief protocol's default assumes a milestone that survives its review unchanged and this one does not.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
