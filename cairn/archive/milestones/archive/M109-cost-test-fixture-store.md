# M109: Cost-test fixture store

**Status:** done (2026-07-23, PR #107 https://github.com/jmgirard/cairn/pull/107)

**Goal:** The `cairn_cost` attribution tests run against a small fixture store instead of scanning the real ~26k-record session store, so the suite pays at most one skip-if-absent real-store read per run.

**Outcome:** `cairn_cost.main()` gained a test-only `home=None` seam threaded into `store_dir(root, home)` (no CLI flag; the store location stays non-user-facing). The `--attribution --milestone` refusal moved ahead of the store read in `main()`, which also corrected a latent no-store escape (it returned 0; now refuses with 2). `test_attribution_mode_refuses_the_milestone_filter` was rewritten onto a fixture store with a `read_records` spy proving the real store is untouched, and `TestLiveStoreShape` (one real read, skip-if-absent) plus a `_live_records_or_skip` helper retains the live-shape guarantee. Suite-wide real-store reads 2→1.

**Decisions:** M109-local — the `--attribution --milestone` refusal is checked ahead of store resolution, correcting the no-store 0→2 escape; not cross-cutting, no D-entry.

**Review:** three fresh-context lenses (Opus diff-bug, Sonnet blame-history, Sonnet prior-review) — zero actioned findings, scorer no-op. Three sub-threshold observations logged (AC1 assertion strength, `import os` nit, cosmetic `report()` header path). Graduated the "Cost-store test I/O" candidate (M102 Out). No lessons captured or retired.
