# M53: Prose-guard mutation harness

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP2, GP4
- **Branch/PR:** m53-prose-guard-mutation-harness · https://github.com/jmgirard/cairn/pull/51

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

- [x] Harness proven both directions: for a registered guard, blanking its
      protected block makes that guard test fail; and the control (the guard
      against unmutated content) passes — demonstrated by the self-test
      fixture pair (one false-coverage guard the harness flags, one sound
      guard it clears). (RR01 rec 2 / Q8)
- [x] Every prose-guard test under `skills/tests/` is registered, and the
      harness passes over all registered (guard, block) pairs — i.e. each
      guard demonstrably fails when its protected block is deleted; any guard
      that did not is re-anchored inline (small) or its fix carded (large),
      one work-log line per fix.
- [x] The completeness meta-test fails when a prose-guard test file is neither
      registered nor exempted — proven by exercising it against an
      unregistered fixture (or asserting discovered-set == registered ∪
      exempt) — so a future unregistered guard breaks the suite.
- [x] `tracking-rules.md` states the registration requirement (every
      prose-guard registers in the mutation harness) and stays under its cap;
      `LESSONS.md` records the M39/M40 false-coverage class as mechanized.
- [x] The active profile's `verify` slot is clean: all three `unittest
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

- 2026-07-13: created by /milestone-plan; promoted from RR01 rec 2; zero-touch mechanism chosen after verifying no guard reads its source at import time.
- 2026-07-13 (T1): engine `skills/tests/mutation_engine.py` (blank_block, scoped `Path.read_text` patch, `guard_fails_when_blanked`); both oracle directions proven with locally-defined fixture guards.
- 2026-07-13 (T2): `Mutation` registry + `EXEMPT` + driver; seeded search-first guard (real-guard pipeline validated); target paths repo-relative.
- 2026-07-13 (T3): registered all 14 guards (one/file); harness flagged one real false-coverage guard (`test_design_interview` bare `banked-candidates ledger` via a wrapped duplicate) → re-anchored on the bolded form; 13/14 sound.
- 2026-07-13 (T4): `TestRegistryCompleteness` (globs `test_*.py`, reports unregistered/stale); proven to flag a synthetic unregistered module.
- 2026-07-13 (T5): universal false-coverage rule in tracking-rules "What gets a test" + LESSONS graduation (pruned M39/M40/M47); Tasks block compressed for cap headroom.
- 2026-07-13 (review): blame-history lens (82) found the LESSONS/rulebook wording overclaimed per-guard coverage — tightened both to per-file granularity + retained the M47 by-hand check, and registered the named M47-scenario guard (generic release-walk `commit`). Work-log compressed to hold the 150 cap.

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

PR #51. Reviewed 2026-07-13 (same-session; evidence by command, fan-out in
fresh-context subagents).

**Acceptance-criteria evidence** (fresh runs):
- AC1 — `TestEngineOracle` green both directions (sound guard fails on deletion, weak guard flagged surviving); `TestBlankBlock` 0/1/many hard-error cases pass.
- AC2 — `TestRegisteredGuardsFailWhenBlanked` green over 15 entries / 14 prose-guard files; harness flagged `test_design_interview` false coverage → re-anchored.
- AC3 — `TestRegistryCompleteness` green: all registered/exempt, no stale, and `test_completeness_flags_an_unregistered_guard` proves the failure path.
- AC4 — rule in `tracking-rules.md` "What gets a test" + harness mechanism; `LESSONS.md` graduation line; LESSONS 47/50.
- AC5 — verify slot clean: skills 143 / scripts 65 / hooks 32, all OK.

**Consistency gate:** `cairn_validate` exit 0 (14/14 incl. mirror, coverage-complete, caps); generic `consistency-gate` → no-op; no DESIGN principle changed → `cairn_impact` skipped.

**Independent fan-out** (3 fresh-context lenses + scorer):
- [O] diff-bug (Opus): no findings — verified the `read_text` patch scoping,
  `blank_block` exactly-once contract, `wasSuccessful()` interpretation, and all
  registry blocks unique/asserted.
- [S] prior-PR (Sonnet): no prior-PR evidence (0 inline comments across 49
  merged PRs) — clean no-op.
- [S] blame-history (Sonnet): **1 finding, scored 82 → fixed now.** The LESSONS
  line + rulebook paragraph overclaimed "mechanized per prose-guard" while the
  registry is per-*file*, leaving a new assertion in a registered file
  unchecked — concretely the M47-scenario guard
  (`test_generic_release_walk_defines_a_tag_path`, `generic.md` release-walk
  `commit` step) was unregistered. Fix: tightened both docs to state per-file
  granularity + retained the M47 by-hand check, and added a registry entry for
  that guard (now 15 entries / 14 files). Re-verified green.

Sub-80 findings: none.
