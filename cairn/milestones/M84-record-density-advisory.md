<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M84: Record-density advisory — the item caps gain a weight axis

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Give `cairn/ROADMAP.md` and `cairn/LESSONS.md` a character-mass advisory
alongside their existing item caps, so prose weight that accumulates inside
single lines stops being invisible to the audit.

## Scope

**In:** A new exit-code-neutral `cairn_validate` advisory measuring total
character mass per item-list file against a per-file threshold; thresholds
derived from a survey of both cairn and intraclass and anchored to a real
incident; the `tracking-rules` weight-caps section rewritten to document two
orthogonal axes (item count and weight) with distinct remedies; and pruning
cairn's own ROADMAP and LESSONS under the resulting thresholds.

**Out:**
- A per-line character warn — rejected at the plan gate: both files are parsed
  one-item-per-line (`cairn_validate` reads ROADMAP rows positionally; D-015
  defines LESSONS as one lesson per line), so pressure on individual line
  length rewards splitting a row across lines and corrodes the format the
  parsers depend on. It would also fire on ~10-12 legitimate candidate rows
  across the two repos today. The measure is therefore total characters per
  file — an orthogonal axis over the same whole file, which distinguishes
  D-030: that rejected splitting *one* budget into two sub-budgets of the same
  kind with a new section boundary, not a second axis.
- Hard-FAIL severity — advisory chosen at the plan gate. D-018 rejected "a soft
  non-failing warn (loses the hard signal on a genuinely bloated cairn
  section)"; distinguished, not superseded — that was the CLAUDE.md section cap,
  where cairn owns the whole content and a hard signal was the point, whereas
  density is a judgment about prose quality, the justification the
  references-staleness advisory already carries. Revisit if it proves ignorable.
- The 150-line milestone-body cap and budget-first drafting → candidate row at
  `cairn/ROADMAP.md` ("Budget-first drafting (cap prevention)"). Investigation
  found it a *distinct* defect: that is a wrapped-prose file where line count
  tracks weight correctly and the problem is drafting overshoot.
- `PROFILE.md` — surveyed, no density problem (max line 80 chars in cairn, 116
  in intraclass); stays on the item cap alone.
- Pruning intraclass's own ROADMAP and LESSONS → the intraclass repo, as its
  own work there once this ships the measure.

## Acceptance criteria

- [ ] AC1: `cairn_validate` emits a new advisory reporting total character
      mass for `cairn/ROADMAP.md` and `cairn/LESSONS.md` against a per-file
      threshold, with its emitted label used verbatim in any prose naming it
      (M78).
- [ ] AC2: The thresholds are derived from a recorded survey of both repos,
      and regression-anchored: the ROADMAP threshold WARNs on the pre-prune
      state (`git show 5d0d5b6^:cairn/ROADMAP.md`, ~9,600 chars) and passes on
      the post-prune state.
- [ ] AC3: cairn's `ROADMAP.md` and `LESSONS.md` both pass the new advisory
      after an in-milestone prune, evidenced by a before/after mass table.
- [ ] AC4: The advisory is exit-code neutral — `cairn_validate` exits 0 on a
      repo tripping only it — covered by a test asserting the exit code, not
      just the output.
- [ ] AC5: The `tracking-rules` weight-caps section documents both axes and
      their distinct remedies (graduate/prune for count, compress for weight),
      locked by a prose-guard registered in the mutation harness.
- [ ] AC6: Verify slot clean — all three unittest suites green
      (`scripts/tests`, `skills/tests`, `hooks/tests`), run from the repo root
      with exit codes checked individually (M56/M65).

## Coverage

- AC1 → T2, T3, T4
- AC2 → T1, T3
- AC3 → T7
- AC4 → T2, T3
- AC5 → T5, T6
- AC6 → T8

## Tasks

- [ ] T1: Survey character mass across both repos and the pre-prune ROADMAP
      state; record the table in this file and derive the two thresholds from
      it, stating the headroom rationale.
- [ ] T2: Tests first — fixtures in `scripts/tests/` for over-threshold,
      under-threshold, and exit-code neutrality of the new advisory.
- [ ] T3: Implement the measure — char thresholds in `scripts/cairn_scripts.py`
      alongside `LINE_CAPS` (`scripts/cairn_scripts.py:44`), and the advisory
      in `scripts/cairn_validate.py` near `check_caps`
      (`scripts/cairn_validate.py:67`), emitting WARN not FAIL.
- [ ] T4: Wire the advisory into the validate output ordering and label; confirm
      `/milestone`'s audit surfaces it as a judgment call, not a mechanical fix.
- [ ] T5: Rewrite the `tracking-rules` weight-caps section for two axes.
      Author the guarded phrase on one physical line and expect the reflow to
      split already-registered neighbouring phrases (M23/M82).
- [ ] T6: Register the new prose-guard in `skills/tests/test_mutation_harness.py`;
      pin the label together with its members on one physical line (M74/M76).
- [ ] T7: Prune cairn's `ROADMAP.md` and `LESSONS.md` under threshold —
      compress lessons rather than evict them where possible, since eviction is
      the item-cap remedy, not the weight remedy.
- [ ] T8: Full verify — three suites plus `cairn_validate` green; record the
      before/after mass table as AC3 evidence.

## Work log

- 2026-07-18: created by /milestone-plan.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
