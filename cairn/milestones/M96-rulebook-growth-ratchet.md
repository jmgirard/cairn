<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M96: Growth ratchet — the rulebook is governed by attention, not by a permitted size

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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
- 2026-07-20: amended at M95's re-cut gate (user-selected) to carry RR03 rec 5's two items, which the 2026-07-19 plan named nowhere and would have silently dropped (IP3): the editorial-pass rule states that a pass applies M95's placement procedure rather than RR02 rec 1's falsified "delete the defense back to its D-entry", and the rulebook preamble gains the one-sentence inflow test. New AC6 + T5; the verify criterion/task shift to AC7/T6 and Coverage follows.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
