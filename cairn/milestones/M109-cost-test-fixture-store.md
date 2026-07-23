# M109: Cost-test fixture store

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m109-cost-test-fixture-store · https://github.com/jmgirard/cairn/pull/107

## Goal

The `cairn_cost` attribution tests run against a small fixture store instead of scanning the real ~26k-record session store, so the suite pays at most one skip-if-absent real-store read per run.

## Scope

**In:**
- Thread an optional `home=None` through `cairn_cost.main()` into the already-documented `store_dir(root, home=…)` override (`scripts/cairn_cost.py:96,407-425`), giving tests a store seam — no CLI flag (the store location stays non-user-facing per the module note at `:45-46`).
- Move the `--attribution --milestone` refusal ahead of the store read in `main()` (`:432` → before `:421-425`), so the refusal path reads zero records in production and in tests.
- Rewrite `test_attribution_mode_refuses_the_milestone_filter` (`scripts/tests/test_cairn_cost.py:299`) to drive `main()` against a fixture store built under a temp home, asserting both exit codes without touching the real store.
- Add one skip-if-absent live-shape test that reads the real store once and asserts its record shape, guarding against Claude Code's transcript format drifting.

**Out:**
- No change to `cairn_cost.py` production behavior — CLI flags, report/audit-line output — beyond the refusal reordering (regression-guarded by the existing suite). → covered by the retained tests, this milestone.
- No env-var or CLI store override (the env-var seam was rejected at the gate).
- Real-store read cost of `--audit-line` in production, or store growth generally → not test I/O; stays a `cairn_cost` concern, out of scope.

## Acceptance criteria

- [x] AC1: `test_attribution_mode_refuses_the_milestone_filter` drives `cairn_cost.main()` through the `home=` seam against a fixture store (a slugged `*.jsonl` under a temp home) and never opens the real `STORE_HOME` path — both the refusal (`--attribution --milestone` → exit 2) and the unfiltered success (`--attribution` → exit 0) are asserted against the fixture, exit 0 running the real attribution branch over the fixture's records.
- [x] AC2: `main()` refuses `--attribution --milestone` before any store read — with `home` pointed at an empty temp home (no store dir) the refusal still returns exit 2, proving the refusal precedes both the `isdir` check and `read_records` (today it wrongly returns 0 there).
- [x] AC3: Exactly one retained test reads the real store as a live-shape guarantee and `skip`s (never fails) when the store dir is absent or empty; when present it asserts records carry `message.usage` and the attribution fields in their real shape.
- [x] AC4: The generic profile's `verify` is clean — `python3 -m unittest` over all three suites, each exit code checked from the repo root.

## Coverage

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5

## Tasks

- [x] T1: Add `home=None` to `main(argv, home=None)` and pass it to `store_dir(root, home)` (`scripts/cairn_cost.py:407-425`); note in the docstring/comment that `main` now honors the documented `home` test override.
- [x] T2: Move the `--attribution --milestone` refusal to the top of `main()`'s post-parse body, before `store_dir`/`isdir`/`read_records` (`:421-438`); keep the stderr usage text and exit 2. Record the no-store 0→2 correction as a milestone-local decision.
- [x] T3: Rewrite `test_attribution_mode_refuses_the_milestone_filter` (`scripts/tests/test_cairn_cost.py:299`): build `<tmp_home>/<store_slug(root)>/s.jsonl` with a couple of assistant records, drive `main([...], home=tmp)` for exit 2 (filtered) and exit 0 (unfiltered), and assert the real `STORE_HOME` path is not read during the test. (AC2's no-store refusal split into its own `test_attribution_refusal_reads_no_store_even_with_none_present`.)
- [x] T4: Add the live-shape test (`TestLiveStoreShape`): reads the real store once, asserting record shape (usage present; a known `attributionSkill` and a milestone `gitBranch`), skipping when the store is absent/empty. Skip path proven deterministically via a `_live_records_or_skip` helper + a temp-dir test asserting `SkipTest` (not failure).
- [x] T5: Run the three suites from the repo root, checking each exit code (M56); confirm the cost suite no longer scans the real store twice and full `verify` is clean.

## Work log

- 2026-07-23: created by /milestone-plan.
- 2026-07-23: set in-progress; branch m109-cost-test-fixture-store cut from main.
- 2026-07-23: T1 — threaded `home=None` through `main()` into `store_dir(root, home)`.
- 2026-07-23: T2 — moved the `--attribution --milestone` refusal ahead of the store read; no-store case corrected 0→2.
- 2026-07-23: T3 — dispatch test now runs on a fixture store via `home=` with a `read_records` spy proving the real store is untouched; cost suite wall 3.5s→0.03s. Added `test_attribution_refusal_reads_no_store_even_with_none_present` for AC2.
- 2026-07-23: T4 — added `TestLiveStoreShape` (one real-store read, skip-if-absent) + `_live_records_or_skip` helper, and a temp-dir test proving the skip path raises `SkipTest` not a failure.
- 2026-07-23: T5 — all three suites green from repo root (scripts 277, skills 576, hooks 72; each exit 0); `cairn_validate` passes (1 pre-existing references-staleness advisory, unrelated). Instrumented count confirms exactly 1 real-store read across the cost suite (was 2). Status → review.

## Decisions

- M109 (T2): `--attribution --milestone` is now refused ahead of store
  resolution in `main()`, not after `read_records`. Besides removing the
  real-store scan from the refusal path, this corrects a latent escape — on a
  machine with no store the old post-read placement hit the no-store branch
  and returned `0` instead of the intended `2`. Local to `cairn_cost.py`; not
  cross-cutting, so no D-entry.

## Review

**Evidence (fresh, on branch @ 6 commits ahead of main):**
- AC1: `test_attribution_mode_refuses_the_milestone_filter` passes on a fixture store; a `read_records` spy records only the fixture path (`home`-rooted), never `real_store`; refusal→2, unfiltered→0. Suite-wide instrumented count: **1** real-store `read_records` call total (was 2), and it is not this test's.
- AC2: `test_attribution_refusal_reads_no_store_even_with_none_present` — empty temp `home` (no store dir) → `--attribution --milestone M94` returns **2**, proving the refusal precedes the `isdir`/`read_records` path.
- AC3: `TestLiveStoreShape` — `test_the_real_store_still_carries_the_fields_cost_reads` runs (store present, 26,805 records; asserts `message.usage`, a known `cairn:*` skill, and a milestone branch); `test_the_live_shape_check_skips_rather_than_fails_when_the_store_is_empty` proves an empty dir raises `SkipTest` not a failure. Exactly one retained real read.
- AC4: three suites from repo root, each exit 0 — scripts 277, skills 576, hooks 72.

**Consistency gate:** `cairn_validate` exit 0, all checks passed (1 advisory: pre-existing `rulebook-classification-ledger.md` references-staleness, not a file this milestone touched). No `IPn/GPn` changed → `cairn_impact` skipped. Generic profile → no toolchain checks.
