# M102: Verify-suite speedup — the dogfood suite runs on its tests, not on process spawns, and greens in any repo state

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Branch/PR:** m102-verify-suite-speedup

## Goal

The verify suite spends its wall time on the tests, not on subprocess spawns, and stays green whether or not a milestone is in flight.

## Scope

**In:**
- `scripts/tests`: route the bulk of `cairn_validate` invocations through the in-process seam `validate.run(root) → (report, failures)` (`cairn_validate.py:1628`) instead of `subprocess.run([python, cairn_validate.py, root])` (`test_scripts.py:107`); retain a named, representative set of end-to-end subprocess tests covering CLI argv parsing, exit codes, and `die_not_cairn`.
- `scripts/tests`: collapse the two M81 combinatorial fixtures — `test_contradiction_is_caught_wherever_it_sits_and_however_wrapped` (`test_scripts.py:1117`) and `test_decoration_layout_and_phrasing_vary_independently` (`test_scripts.py:1213`) — so their axes are covered without a full cross-product of subprocess spawns.
- `hooks/tests`: replace the per-test git-init-commit `setUp` (5 git spawns × 72 tests, `test_hooks.py:69`) with a module-level template repo built once and copied per test; keep the hook invocation itself a real subprocess (print-envelope fidelity, M07).
- Fix the state-coupled red: `test_it_runs_against_this_repos_own_live_milestone_files` (`test_cairn_budget.py:322`) must pass whether or not the live tree holds `milestones/M*.md`.

**Out:**
- Converting hook *invocation* to in-process — refused here (M07: a self-consistent-but-wrong JSON envelope passes in-process while doing nothing live); if ever revisited it is its own milestone.
- The ~1.6s `test_attribution_mode_refuses_the_milestone_filter` (`test_cairn_cost.py:299`) — slow from reading the whole real ~25k-record telemetry store in-process, an I/O concern not a spawn → candidate row.
- `skills/tests` (already ~1.7s, in-process) → untouched.

## Acceptance criteria

- [ ] The bulk of `scripts/tests` `cairn_validate` invocations run in-process via `validate.run(root)`; a named set of ≥3 subprocess tests remains and covers CLI argv, non-cairn exit code, and `die_not_cairn`. Evidence: the retained named tests pass, and a grep shows the former per-`install()` spawn replaced by the in-process call.
- [ ] The two M81 fixtures no longer spawn a full cross-product of subprocesses — each covers its decoration/layout/phrasing axes via in-process calls or a covering set — and the behaviors they pin (contradiction-caught; three axes vary independently) remain asserted and pass. Evidence: the two tests, plus their before/after spawn count.
- [ ] `hooks/tests` `setUp` spawns zero git subprocesses (a module-level template repo is copied per test); hook invocation remains a real subprocess and the printed-JSON-envelope assertions are unchanged. Evidence: `setUp` git-spawn count = 0; a representative subprocess hook test still asserts the `hookSpecificOutput` / top-level-decision shapes.
- [ ] The budget live-shape test passes on a tree with no `milestones/M*.md` present while still parsing a real milestone file's shape. Evidence: the test passes with the live `milestones/` empty; a regression exercises the empty-milestones tree.
- [ ] All three verify suites green (PROFILE `verify` slot). Evidence: the three `unittest discover` runs, with before/after wall time reported.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: In `scripts/tests`, replace the per-`install()` `run("cairn_validate.py", root)` spawns with `validate.run(root)`; extract a named subprocess set (argv, non-cairn exit, `die_not_cairn`) as the retained CLI-contract tests.
- [ ] T2: Collapse the two M81 combinatorial fixtures (`test_scripts.py:1117`, `:1213`) to in-process covering sets, preserving the asserted contradiction and three-axes-independent behaviors.
- [ ] T3: In `hooks/tests`, build a committed template repo once at module/class scope and `shutil.copytree` it per test in `setUp`; drop the 5 git spawns; keep the hook subprocess call and the envelope assertions.
- [ ] T4: Fix `test_it_runs_against_this_repos_own_live_milestone_files` to green with no live milestone files while still parsing a real milestone shape (e.g. include `milestones/archive/M*.md`, or write a fixture from the template); add the empty-milestones regression.
- [ ] T5: Run all three suites green; capture before/after wall time as review evidence.

## Work log

- 2026-07-20: created by /milestone-plan (promoted from the "Verify-suite subprocess cost" candidate row, banked M94 Out; the red-suite fold-in and hooks-lever decisions settled at the plan gate).
- 2026-07-20: T1 — `run()` in `scripts/tests/test_scripts.py` dispatches `cairn_validate.py` in-process (`_run_validate_inproc` capturing report + exit code); `_spawn` retained for the process boundary. `TestOutsideCairn` repointed to `_spawn`; added `TestValidateCliContract` (real-process exit-0 and exit-1). Scripts suite ~20s→6.7s, all green (268 tests).

## Decisions

## Review
