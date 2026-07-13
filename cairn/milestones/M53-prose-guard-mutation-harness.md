# M53: Prose-guard mutation harness

- **Status:** in-progress
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

- [ ] T1 — Build the harness engine (e.g. `skills/tests/mutation_harness.py`):
      given (target file path, block locator, guard test id), produce mutated
      content with the block blanked, patch `pathlib.Path.read_text` to return
      it for the target during a scoped re-run, execute the guard via
      `unittest.TestLoader`/`TestResult`, and assert failures+errors > 0.
      A locator that resolves to zero or >1 sites is a hard error (catches
      drift), not a silent pass.
- [ ] T2 — Define the registry format (entries: guard module+test, target
      file, block locator) and ship the self-test fixture pair — a
      false-coverage guard the harness must flag and a sound guard it must
      clear — proving both oracle directions. (AC1)
- [ ] T3 — Register all existing prose-guards under `skills/tests/`; run the
      harness; re-anchor inline any false-coverage guard it flags (typically a
      one-line anchor fix per the M39/M40 discipline), card any needing real
      rework (see Out); log one work-log line per fix. (AC2)
- [ ] T4 — Completeness meta-test: discover every prose-guard test file under
      `skills/tests/` and assert each is registered or in an explicit EXEMPT
      set (with a reason string); prove it fails against a temporary
      unregistered fixture. (AC3)
- [ ] T5 — Add the "every prose-guard registers in the mutation harness" rule
      to `tracking-rules.md` (near the guard/testing discipline / "What gets a
      test"), keeping the file under its cap; append a `LESSONS.md` line
      graduating the M39/M40 false-coverage class to mechanism. (AC4)

## Work log

- 2026-07-13: created by /milestone-plan; promoted from the RR01 retrospective
  candidate (rec 2). Zero-touch read-interception mechanism chosen at plan
  after verifying no guard reads its source file at import time.

## Decisions

## Review
