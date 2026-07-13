# M53: Prose-guard mutation harness

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP2, GP4
- **Branch/PR:** m53-prose-guard-mutation-harness

## Goal

Build a mutation-test harness that, for every registered prose-guard, blanks
the rule block it protects and proves the guard fails — mechanizing the
"mentally delete the feature" check so false-coverage guards are caught at
authoring time, and requiring every prose-guard to register.

## Scope

Promoted from the RR01 whole-architecture retrospective's single
highest-leverage recommendation (rec 2 / Q8 / Q11,
`cairn/reviews/archive/RR01-architecture-retrospective.md`). The false-coverage
trap — a prose-guard whose asserted phrase also occurs elsewhere, so deleting
the rule's own occurrence doesn't fail the test — has recurred 6+ times
(M23/M26/M39/M40/M47/M48/M50) despite being a known, documented lesson each
time. Lessons don't execute; a harness does.

**In:**
- A harness engine (in `skills/tests/`) that, given a registered
  (guard test, target file, protected-block locator), produces mutated content
  with that block blanked and re-runs *that specific guard* against it,
  asserting it fails. Zero-touch on existing guards: intercept the file read
  (`pathlib.Path.read_text`) for the target during a scoped re-run — verified
  viable because every guard reads via a per-test `read()`/`rules()` helper,
  none at import time.
- A registry mapping each prose-guard test → its target source file + the
  block locator it protects, plus a self-test fixture pair (a deliberately
  false-coverage guard the harness must flag, a sound guard it must clear) as
  the harness's own oracle.
- Register **all** existing prose-guards under `skills/tests/`; re-anchor
  inline any false-coverage guard the harness discovers.
- A completeness meta-test that fails CI when a prose-guard test file is
  neither registered nor explicitly exempted.
- The rulebook rule ("every prose-guard registers in the mutation harness")
  and a LESSONS line graduating the M39/M40 false-coverage class to mechanism.

**Out:**
- Structural/behavioral tests that aren't prose-`assertIn` guards (hook
  behavior in `hooks/tests/`, script logic in `scripts/tests/`) — not
  prose-guards; not retrofitted here.
- A large re-anchor rework a discovered weak guard might need → carded as a
  hotfix/candidate (only small one-line re-anchors land inline).
- The other RR01 clusters (release-prep/positioning, doctrine relocation,
  IP4, hook hardening, changelog slot) → their existing ROADMAP candidate rows.

## Acceptance criteria

- [ ] Harness proven both directions: for a registered guard, blanking its
      protected block makes that guard test fail; and the control (the guard
      against unmutated content) passes — demonstrated by the self-test
      fixture pair (one false-coverage guard the harness flags, one sound
      guard it clears). (RR01 rec 2 / Q8)
- [ ] Every prose-guard test under `skills/tests/` is registered, and the
      harness passes over all registered (guard, block) pairs — i.e. each
      guard demonstrably fails when its protected block is deleted; any guard
      that did not is re-anchored inline (small) or its fix carded (large),
      one work-log line per fix.
- [ ] The completeness meta-test fails when a prose-guard test file is neither
      registered nor exempted — proven by exercising it against an
      unregistered fixture (or asserting discovered-set == registered ∪
      exempt) — so a future unregistered guard breaks the suite.
- [ ] `tracking-rules.md` states the registration requirement (every
      prose-guard registers in the mutation harness) and stays under its cap;
      `LESSONS.md` records the M39/M40 false-coverage class as mechanized.
- [ ] The active profile's `verify` slot is clean: all three `unittest
      discover` suites green (`skills/tests`, `scripts/tests`, `hooks/tests`).

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T1, T2, T3, T4, T5

## Tasks

- [x] T1 — Harness engine (`skills/tests/mutation_engine.py`): blank a block, re-run the guard via a scoped `Path.read_text` patch, assert it fails; ambiguous/missing locator is a hard error. (AC1)
- [x] T2 — Registry format (`Mutation`) + self-test fixture pair proving both oracle directions. (AC1)
- [x] T3 — Register all prose-guards; re-anchor inline any false-coverage guard flagged (one caught: `test_design_interview`); card large rework (none). (AC2)
- [x] T4 — Completeness meta-test: every prose-guard registered or exempted, proven to fail on an unregistered fixture. (AC3)
- [x] T5 — Rule in `tracking-rules.md` "What gets a test" (guard must fail when its rule is deleted) + `LESSONS.md` graduation line; caps held. (AC4)

## Work log

- 2026-07-13: created by /milestone-plan; promoted from the RR01 retrospective
  candidate (rec 2). Zero-touch read-interception mechanism chosen at plan
  after verifying no guard reads its source file at import time.
- 2026-07-13 (T1): engine in `skills/tests/mutation_engine.py` (`blank_block`,
  `_run_single` via scoped `Path.read_text` patch, `guard_fails_when_blanked`);
  both oracle directions proven in `test_mutation_harness.py` — sound guard
  caught failing on deletion, weak guard flagged surviving. Fixture guards
  defined locally so `discover` doesn't collect them. 3 suites green.
- 2026-07-13 (T2): `Mutation` registry record + `EXEMPT` map +
  `TestRegisteredGuardsFailWhenBlanked` driver; seeded with the search-first
  guard and confirmed it fails when its block is blanked (real-guard pipeline
  validated). Target paths are repo-relative (guards read files outside
  `skills/` too, e.g. DESIGN.md).
- 2026-07-13 (T3): registered all 14 prose-guards (one strong per file). The
  harness flagged one genuine false-coverage guard on first run —
  `test_design_interview.test_phase1_banks_never_classifies` asserted a bare
  `banked-candidates ledger` that survives via a whitespace-wrapped second
  mention; re-anchored inline onto the bolded introduction. 13/14 were sound.
  3 suites green (skills 140).
- 2026-07-13 (T4): `TestRegistryCompleteness` — `prose_guard_modules()` globs
  `test_*.py`, `unregistered()` reports any not registered/exempt; proven to
  flag a synthetic unregistered module and to reject stale entries. skills
  suite 143 green.
- 2026-07-13 (T5): universal false-coverage rule in tracking-rules "What gets a
  test" (plugin mechanism named, matching the existing `locked by …` style);
  LESSONS graduation line, pruning the now-mechanized M39/M40/M47 lessons
  (47/50). Compressed the Tasks block to reclaim review headroom vs the 150 cap
  (M22/M50 remedy). 3 suites green.

## Decisions

- 2026-07-13: Registry granularity is **one strong entry per guard file**
  (the completeness bar), not one per assertion — a file may add more entries
  per distinct block over time. The harness is meaningful for positive
  (`assertIn`) assertions; `assertNotIn`/negative guards aren't blanked (their
  oracle is absence, not presence).
- 2026-07-13: First harness run found real false coverage in
  `test_design_interview` (bare `banked-candidates ledger` survives via a
  whitespace-wrapped duplicate); re-anchored onto `**banked-candidates
  ledger**`. This is the milestone's thesis demonstrated on live code.

## Review
