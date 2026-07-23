# M109: Cost-test fixture store

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** —

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

- [ ] AC1: `test_attribution_mode_refuses_the_milestone_filter` drives `cairn_cost.main()` through the `home=` seam against a fixture store (a slugged `*.jsonl` under a temp home) and never opens the real `STORE_HOME` path — both the refusal (`--attribution --milestone` → exit 2) and the unfiltered success (`--attribution` → exit 0) are asserted against the fixture, exit 0 running the real attribution branch over the fixture's records.
- [ ] AC2: `main()` refuses `--attribution --milestone` before any store read — with `home` pointed at an empty temp home (no store dir) the refusal still returns exit 2, proving the refusal precedes both the `isdir` check and `read_records` (today it wrongly returns 0 there).
- [ ] AC3: Exactly one retained test reads the real store as a live-shape guarantee and `skip`s (never fails) when the store dir is absent or empty; when present it asserts records carry `message.usage` and the attribution fields in their real shape.
- [ ] AC4: The generic profile's `verify` is clean — `python3 -m unittest` over all three suites, each exit code checked from the repo root.

## Coverage

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5

## Tasks

- [ ] T1: Add `home=None` to `main(argv, home=None)` and pass it to `store_dir(root, home)` (`scripts/cairn_cost.py:407-425`); note in the docstring/comment that `main` now honors the documented `home` test override.
- [ ] T2: Move the `--attribution --milestone` refusal to the top of `main()`'s post-parse body, before `store_dir`/`isdir`/`read_records` (`:421-438`); keep the stderr usage text and exit 2. Record the no-store 0→2 correction as a milestone-local decision.
- [ ] T3: Rewrite `test_attribution_mode_refuses_the_milestone_filter` (`scripts/tests/test_cairn_cost.py:299`): build `<tmp_home>/<store_slug(root)>/s.jsonl` with a couple of assistant records, drive `main([...], home=tmp)` for exit 2 (filtered) and exit 0 (unfiltered), and assert the real `STORE_HOME` path is not read during the test.
- [ ] T4: Add `test_live_store_shape_if_present`: `skipUnless` the real store dir exists and is non-empty; read it once via `read_records(store_dir(root))` and assert record shape (usage present; `attributionSkill`/`gitBranch` in their real forms). Prove the skip path with `home` redirected at an empty dir.
- [ ] T5: Run the three suites from the repo root, checking each exit code (M56); confirm the cost suite no longer scans the real store twice and full `verify` is clean.

## Work log

- 2026-07-23: created by /milestone-plan.

## Decisions

## Review
