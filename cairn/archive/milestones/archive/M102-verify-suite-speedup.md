# M102: Verify-suite speedup — the dogfood suite runs on its tests, not on process spawns, and greens in any repo state

**Status:** done (2026-07-20, PR #100 https://github.com/jmgirard/cairn/pull/100)

**Goal:** The verify suite spends its wall time on the tests, not on subprocess spawns, and stays green whether or not a milestone is in flight.

**Outcome:** Verify ~40s → ~15.6s, test-harness + tracking only. `scripts/tests` `run()` dispatches `cairn_validate` in-process (`_run_validate_inproc`), keeping `_spawn` + `TestValidateCliContract`/`TestOutsideCairn` for the real process boundary (~20s→6.2s); the two M81 combinatorial fixtures inherit the seam (4.86s→0.80s), cross-products kept. `hooks/tests` `RepoFixture.setUp` `shutil.copytree`s a once-built committed template repo instead of git init/config/add/commit per test (360 git spawns gone); hook invocation stays a real subprocess (M07 envelope fidelity, ~15s→9.0s). `test_it_runs_against_this_repos_own_live_milestone_files` now parses the canonical template + any live files, with an empty-milestones regression, so it no longer reds between milestones.

**Decisions:** none.

**Review:** three fresh-context lenses (Opus diff-bug, Sonnet blame-history, Sonnet prior-review) — zero findings, scorer no-op, nothing sent back. Graduated the "Verify-suite subprocess cost" candidate (M94 Out). One lesson captured; none retired.
