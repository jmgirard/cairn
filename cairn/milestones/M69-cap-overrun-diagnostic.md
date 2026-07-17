<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M69: Cap-overrun diagnostic — per-section breakdown + single-pass compression discipline

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m69-cap-overrun-diagnostic / https://github.com/jmgirard/cairn/pull/67   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

When a milestone plan-body exceeds the 150-line cap, the cap check names which
section is heavy and by how much, and the rulebook mandates one targeted
rewrite — so trimming is a single step, not a nibble-and-recount loop.

## Scope

**In:** A per-section line breakdown of an over-cap milestone's plan-owned body,
emitted by the cap check, and a central rulebook remedy that turns the breakdown
into one compression pass.

- A `cairn_scripts` helper returns each plan-owned `## ` section's line count
  (fence-aware, same plan-owned/`## Review` boundary as
  `milestone_body_line_count`).
- `check_caps` uses it: for each over-cap live milestone it emits the sections
  heaviest-first plus the overage (`+N over`), alongside today's total line.
- tracking-rules "Weight caps" remedies gain the single-pass compression
  discipline: read the breakdown, compress the single heaviest plan-owned
  section in one rewrite (never iterative Edit-then-recount), and
  cross-reference durable records (DECISIONS/DESIGN) instead of restating their
  substance in the milestone.

**Out:**
- Budget-first / up-front per-section budgets (prevention) → ROADMAP candidate,
  reassessed after this ships (user-flagged at the plan gate).
- Any change to *what* is counted or a second budget number → governed by
  D-030; not touched.
- Work-log cap exemption → rejected at this plan gate; the work log stays
  counted (parallels D-030 keeping the milestone-local `## Decisions` counted).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] When a live milestone's plan-owned body ≥ 150 lines, `cairn_validate`
      output includes a per-section breakdown — each plan-owned `## ` section
      with its line count, heaviest-first — plus the overage (`+N over`).
- [x] The breakdown is fence-aware and uses the same plan-owned/`## Review`
      boundary as `milestone_body_line_count`: a fenced `## Review` in the body
      is not the boundary, and the exempt `## Review` section is excluded from
      the breakdown.
- [x] A milestone under cap produces no breakdown; the breakdown appears only
      for over-cap live milestones (archived summaries unaffected).
- [x] tracking-rules "Weight caps" remedies state the single-pass compression
      discipline: use the breakdown, compress the heaviest section in one
      rewrite (not iterative nibbling), and cross-reference durable records
      rather than restate them.
- [x] `verify` slot clean: `python3 -m unittest discover -s scripts/tests` and
      `-s skills/tests` both pass.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T2
- AC2 → T1
- AC3 → T1, T2
- AC4 → T3
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Add `milestone_section_line_counts(path)` to `scripts/cairn_scripts.py`:
      fence-aware, returns ordered `(heading, line_count)` for each plan-owned
      `## ` section up to the `## Review` boundary (reuse the M45 fence logic
      that `milestone_body_line_count` uses). Unit tests in
      `scripts/tests/test_scripts.py`: present, fenced-`## Review`-in-body,
      no-`## Review`, and Review-excluded cases.
- [x] T2 — Wire the breakdown into `check_caps` (`scripts/cairn_validate.py:88`):
      on an over-cap live milestone append a heaviest-first section breakdown +
      `+N over` to the emitted line(s). Tests assert the breakdown appears
      over-cap and is absent under-cap, reusing the existing over-cap fixtures.
- [x] T3 — Add the single-pass compression remedy to the tracking-rules
      "Weight caps" "Remedies when a cap is hit" bullet; add a
      mutation-registered guard (likely
      `skills/tests/test_milestone_cap_exemption.py`, which already reads the
      weight-caps text) and register the block in the mutation harness.
- [x] T4 — Run both suites from repo root; confirm green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-17: created by /milestone-plan (+candidate: budget-first drafting, to reassess).
- 2026-07-17: T1 — milestone_section_line_counts helper + 7 tests; preamble+sections==body invariant holds; both suites green.
- 2026-07-17: T2 — check_caps emits heaviest-first breakdown + `shed ≥N` on over-cap milestones; 2 tests (multi-section ordering, under-cap absence); scripts 96 green.
- 2026-07-17: T3 — single-pass compression remedy in tracking-rules "Weight caps" (breakdown-driven, never nibble, cross-reference not restate); 2 guard asserts + 2 mutation-registry entries; skills 221 green.
- 2026-07-17: T4 — both suites green from repo root (scripts 96, skills 221); all tasks done → status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->

**Evidence per criterion (fresh, PR #67):**
- AC1 ✓ — `test_over_cap_shows_heaviest_first_breakdown` passes: an over-cap
  live milestone emits `heaviest first: …` + `shed ≥N`, sections in
  descending line order (Tasks before Scope before Work log).
- AC2 ✓ — `TestMilestoneSectionLineCounts` (7/7): fence-aware; a fenced
  `## Review` in the body is not the boundary; the exempt `## Review` section
  is excluded; `preamble + Σsections == milestone_body_line_count`.
- AC3 ✓ — `test_under_cap_shows_no_breakdown` passes: a passing repo emits no
  breakdown (exit 0, no `heaviest first:`).
- AC4 ✓ — `test_weight_caps_states_single_pass_compression` and
  `test_weight_caps_states_cross_reference_not_restate` pass; both blocks are
  mutation-registered (harness `TestRegisteredGuardsFailWhenBlanked` green).
- AC5 ✓ — scripts 96 / skills 221, both green from repo root.

**Consistency gate:**
- `cairn_validate.py` exit 0 — all checks pass (incl. weight caps, coverage
  complete). Recorded below.
- No IPn/GPn principle changed (works under GP1, adds none) → `cairn_impact`
  skipped per protocol.
- Profile `generic` names no toolchain consistency-gate checks → clean no-op.

**Independent review:** _pending fan-out._
