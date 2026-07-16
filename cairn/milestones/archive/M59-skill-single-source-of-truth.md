# M59: Skill single-source-of-truth (archived)

- **Status:** done · PR https://github.com/jmgirard/cairn/pull/57 · merged 2026-07-16 · GP1, GP2

## Goal

Skills defer to their single sources of truth (RR01 recs 7+12): cairn-init's
default-branch fallback canonical, check enumerations run-and-read, migration
protocol progressively disclosed.

## Outcome

cairn-init §0 follows the rulebook recipe (ls-remote rung, ask on no-remote;
the old `--show-current` fallback was a latent pre-M25 bug per blame).
`/milestone-review` step 4 + `/milestone` §2 run validate and read it (old
lists were 5 checks stale). §2's ~150-line protocol verbatim-moved
(diff-clean) to `skills/shared/migration-protocol.md`, read only on footprint
detection; cairn-init 304→164 lines. Guards re-anchored in the relocating
commits (M46); 8 mutation entries; new test_run_and_read_checks.py.

## Review

AC1 evidence grep amended via mini-gate (tripped on the guard's own
assertNotIn). Fan-out: F1 (85, fixed) — name the emitted label `coverage
complete`, not the concept phrase; blame + prior-PR clean. 171+83+32 green.
