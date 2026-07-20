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

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
