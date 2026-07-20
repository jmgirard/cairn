<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M94: Always-read weight — the two files cairn re-reads most gain a signal

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give `tracking-rules.md` and `DECISIONS.md` — the two heaviest files cairn
re-reads every phase, both currently ungoverned — a measured weight signal, so
GP1's "caps keep always-read files small" stops being false of the largest
always-read files in the system.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A dated baseline survey of always-read mass; a measured char threshold
for `skills/shared/tracking-rules.md` enforced by a guard in `skills/tests`
(plugin self-discipline — `cairn_validate` is `cairn/`-only and cannot see
plugin files); a `cairn_validate` advisory for `cairn/DECISIONS.md` whose
prescribed remedy respects IP4.

**Out:**
- Actually slimming `tracking-rules.md` (extracting modules per D-031) →
  candidate row, promotes on this milestone's signal.
- Bounding the plan-time `DECISIONS.md` collision sweep → candidate row.
- Test-suite subprocess cost (`hooks/tests` 16.5s / 72 tests) → candidate row;
  independent of this signal and promotable immediately.
- Restructuring the ROADMAP candidates block → left to D-035, unsuperseded
  (user call at the M94 plan gate); row count is not what grew.
- Any cap on `DECISIONS.md`. IP4 makes an append-only file's only compression
  remedy illegal; this milestone measures it and names a legal remedy.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: A dated page under `cairn/references/` records always-read mass by
      the method it states: `tracking-rules.md` sampled across this repo's
      history, and `DECISIONS.md` across all 9 cairn-tracked repos under
      `~/GitHub` (measured 2026-07-19: 854 → 95,976 chars). Figures carry an
      extraction status per the M85 template shape.
- [ ] AC2: `tracking-rules.md`'s threshold is **derived from AC1's measured
      population through the guard's own comparison operator** — the derivation
      is shown in the source comment, naming what the operator permits (`>=`
      permits threshold−1), never a round number assumed ahead of the
      measurement (M87).
- [ ] AC3: A guard in `skills/tests` reddens when `tracking-rules.md` meets its
      threshold and passes below it — proven by inversion (edit the threshold,
      run the suite, require red, restore and diff), not by the success case
      alone (M74) — and the threshold's stated↔enforced coupling is pinned at
      **every** site the number appears, the site count established by grepping
      the repo for the value and recorded (M87: the number lived in three
      places while the guard paired two).
- [ ] AC4: `cairn_validate` emits a WARN naming `cairn/DECISIONS.md`'s
      always-read mass, prescribing a bounded read or archival and explicitly
      **not** compression (IP4), and prints a positive `OK` signal proving the
      path ran when under threshold — an absence-assert alone is vacuous
      against a crash (M84). Validated by running it against all 9 surveyed
      repos: every repo it fires on is named with its measured value and the
      fire/quiet split recorded, a threshold firing on all 9 or none of them
      being a failed derivation that returns to AC2.
- [ ] AC5: The new guard file carries a mutation-harness `Mutation(...)`
      registration whose `block` is a positive assertion's phrase; the harness
      cannot see an unregistered guard file (M53).
- [ ] AC6: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3, T4
- AC4 → T5, T6
- AC5 → T3
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: Measure. Sample `tracking-rules.md` mass across this repo's history
      and `DECISIONS.md` across the 9 cairn repos; write the dated survey page
      under `cairn/references/` with method, figures, and extraction status.
      Add its INDEX entry (`check_references_index` pairs them).
- [ ] T2: Derive `tracking-rules.md`'s threshold from T1's population, in a
      source comment stating the operator and what it permits. No number is
      chosen before T1 lands.
- [ ] T3: Write the guard in `skills/tests` (word-bounded `assertRegex`, target
      read per-test not cached in `setUpClass` — M61), pin the stated↔enforced
      coupling, and add the `Mutation(...)` registration.
- [ ] T4: Grep for every site of the derived number; pair each. Record the site
      count in the work log.
- [ ] T5: Add the `DECISIONS.md` advisory to `cairn_validate` — WARN + positive
      `OK` line, IP4-respecting remedy text; assert against the classifier, not
      the report (M93).
- [ ] T6: Run the advisory across all 9 repos, record the fire/quiet split, and
      run the three suites from the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan. Scope from a measured slowdown investigation — plan→review wall clock rose from a ~23 min median (M63–M68) to ~39 min (M88–M93); the three verify suites contribute ~10% (37s × ~6 runs) while `tracking-rules.md` grew +56% and `DECISIONS.md` +103% over the same 30 milestones, both ungoverned by any cap.
- 2026-07-19: start — branch cut (`m94-always-read-weight`), status in-progress.
- 2026-07-19: implement gate — user rejected the ratchet basis as incoherent with the milestone's own premise (a threshold above current size blesses the state the investigation flagged). Hard-fail at a firing threshold deadlocks verify (AC6 unreachable until the deferred slimming lands), so an AC3 amendment to advisory-at-the-M63-baseline was drafted and is HELD, not applied.
- 2026-07-19: escalating to /milestone-brief on a no-oracle tripwire at user request. Evidence: 9 weight-management milestones (M32, M55, M69, M77, M84, M87, M92, M93, M94), 5 of them 2026-07-18/19, with M87 existing only to re-derive M84's thresholds — wrong on both files 3 days after shipping. Two gate rounds here produced no defensible threshold basis. Question is architectural, not the number.
- 2026-07-19: blocked on RB02. Collision found while drafting: RR01 §5 already ruled on rulebook size at 545 lines — rejected per-skill splitting (rec 15), prescribed ONE extraction (rec 9, executed by M58/D-031) plus a norm. Net effect 545→532 lines, erased within 3 days; today 765 (+44% over the state that triggered RR01, vs its projected ~460 core). RB02 therefore asks why the prescription failed to govern, not whether to split.
- 2026-07-19: deviation logged — RB02 and this status change committed on the milestone branch, not main as /milestone-brief step 2 prescribes. Reason: M94's ROADMAP row and header mirror live on the branch at in-progress, so a docs-only main commit would diverge the mirror it is meant to sync. Tracking-travels-with-code kept them in one commit.
- 2026-07-19: RR02 ingested. Load-bearing claims re-verified against the implementation before ingestion (M75): Weight-caps section 21→80 lines (+59, vs the rec 9 extraction's −53); LESSONS.md 20,494 chars vs the 20,500 threshold; 52 `### D-` headings totalling 5,378 chars (5.6% of the file); D-049 present as cited. RR02's section table counts one line higher per section (heading-boundary convention); every delta matches.
- 2026-07-19: CORRECTION to this log's 2026-07-19 creation entry — that entry books the ~23→~39 min slowdown against re-read growth. RR02 Q6 finds the causal claim unsupported: the slow window is dominated by weight-management meta-milestones carrying extra gate rounds (M94 itself burned two), and the only causally isolated figure is the suites' ~10%, which exonerates them. The growth is a real GP1 defect on its own merits; the latency attribution is withdrawn pending token instrumentation.
- 2026-07-19: returned to planned for a re-cut (user gate). Branch `m94-always-read-weight` carried docs only and landed on main under the docs-only carve-out; branch deleted. Criteria below are superseded per the Decisions section and are the re-cut's input, not a live plan.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->


Full reasoning and evidence: `cairn/reviews/archive/RR02-weight-management-architecture.md`
(answers by question number). Recorded here as findings, not restatements.

- 2026-07-19 (Q1/Q5): RR01 rec 9 failed **structurally** — a one-time extraction
  is a stock remedy for a flow problem (+7.6 lines/milestone, no outflow), and
  D-031's norm governs the wrong margin. Dominant inflow is **rationale, not
  rules**, against the rulebook's own `tracking-rules.md:11-13` boundary.
- 2026-07-19 (Q2): the family splits — outflow (M32, M92) and cap-boundary
  (M55, M69, M77) work is settled and right; the character-mass family
  (M84→M87→M93→M94) is the wrong mechanism class for prose files, because
  D-049's doctrine makes its thresholds nonstationary by design.
- 2026-07-19 (Q3): "threshold" is the wrong instrument at n=1. Replacement is a
  growth-since-last-editorial-pass ratchet. Supersedes AC2/AC3 and the held
  AC3 amendment.
- 2026-07-19 (Q4): `DECISIONS.md` mass is legitimate; the read is the defect.
  The 52 `### D-` headings are already a zero-divergence index. Carries an IP2
  recall trade requiring a user gate. Supersedes AC4.
- 2026-07-19 (Q5): RR01 rec 15 **upheld**; the size fix is evicting
  non-contract content, never reading the contract partially.
- 2026-07-19 (Q6): this milestone's own latency premise is **unsupported**
  (composition + sample confounds). Growth stays a GP1 defect on
  context-pressure and instruction-dilution grounds. Instrument before
  shipping further weight machinery.
- 2026-07-19 (triage): apply rec 1 (slimming), rec 2 (ratchet, replaces
  AC2/AC3), rec 3 (bounded read — user gate, annotates IP2), rec 4
  (instrument, sequenced FIRST); consider recs 5-6; recs 7-9 rejected by RR02
  with reasons.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
