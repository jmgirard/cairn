# M180: ROADMAP terminal-row retention drops from 5 to 3

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — `cairn_validate` gates adopting repos on the constant
- **Branch/PR:** m180-retention-three

## Goal

The ROADMAP table keeps only the 3 most recent done/dropped rows, so the injected status view shows less finished work.

## Scope

**In:** the `TERMINAL_ROW_RETENTION` constant and its validator tests; the
three live prose statements of the count (tracking-rules bullet, cairn-init
ROADMAP skeleton comment, the M111 lesson line); this repo's own ROADMAP
pruned to 3; a CHANGELOG entry telling adopters what reds and how to fix it.

**Out:** a per-repo configurable count → rejected at the plan gate (work
log); a D-entry → rejected at the plan gate; archive summaries and
DECISIONS.md text that mention 5 → history, never edited (IP4).

## Acceptance criteria

- [ ] AC1: `TERMINAL_ROW_RETENTION` in `scripts/cairn_scripts.py` is 3, and two
      tests in `scripts/tests/test_scripts.py` pin it from both sides: a
      fixture of 4 terminal rows (BASE_ROWS' M01 + 2 done + 1 dropped) fails
      the `terminal-row retention` check, and a fixture of exactly 3 done rows
      (M01 + 2 done) passes it; the fail case reds with the constant at 5 and
      the pass case reds with it at 2.
- [ ] AC2: The three live statements of the count each say 3 —
      `skills/shared/tracking-rules.md` terminal-row retention bullet, the
      `skills/cairn-init/SKILL.md` ROADMAP skeleton comment, and the
      `cairn/LESSONS.md` line dated 2026-07-23 (M111, trimmed M147) — and
      `grep -rnEi "(\b5\b|\bfive\b).*(terminal|retention|done|dropped)|(terminal|retention|done|dropped).*(\b5\b|\bfive\b)" skills scripts hooks README.md cairn/LESSONS.md cairn/DESIGN.md`
      returns no line stating the old count (a match on an unrelated 5 is
      dispositioned in the work log).
- [ ] AC3: This repo's `cairn/ROADMAP.md` holds exactly 3 terminal rows on the
      branch (M175 and M176 pruned; they survive in `archive/` + git) and
      `python3 scripts/cairn_validate.py` reports green.
- [ ] AC4: `CHANGELOG.md` Unreleased carries one entry naming the
      `terminal-row retention` check, the new cap of 3, and the remedy for an
      adopting repo that reds on upgrade (prune the oldest done/dropped rows;
      they survive in `milestones/archive/` + git); both gating suites green.

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5

## Tasks

- [x] T1: Rewrite `test_dropped_rows_count_toward_retention`
      (`scripts/tests/test_scripts.py:3203`) as the fail-at-4 case (M01 + 2
      done + 1 dropped) with a truthful comment, and add a pass-at-3 case
      (M01 + 2 done, asserting no `terminal-row retention` finding); run them
      red first against the constant at 5.
- [x] T2: Set `TERMINAL_ROW_RETENTION = 3` (`scripts/cairn_scripts.py:48`);
      re-run T1's tests green; temporarily set 2 to show the pass case red,
      restore, record both reds in the work log.
- [ ] T3: Edit the three prose sites (`tracking-rules.md:83`,
      `cairn-init/SKILL.md:146`, `LESSONS.md:24`) to 3; run AC2's grep and
      disposition every hit; hand-run `skills/tests` (prose guards).
- [ ] T4: Prune M175 and M176 rows from `cairn/ROADMAP.md`; replace the
      hygiene stamp line; `cairn_validate` green.
- [ ] T5: CHANGELOG Unreleased entry per AC4; both gating suites green.

## Work log

- 2026-09-06: created by /milestone-plan.
- 2026-09-06: criteria audit ran in full mode ([O] reader): 5 findings, all fixed before the gate — pass-at-3 cannot red under 5 (reworded to red under 2); counts include BASE_ROWS' M01; the existing dropped-row test loses discrimination at cap 3 (becomes the fail case); AC2's grep was a proxy (three sites named as the domain, pattern widened); AC4's CHANGELOG entry names the check and remedy.
- 2026-09-06: plan gate chose a fixed constant over a per-repo PROFILE slot because no repo has asked to vary it and a slot adds validate/init surface; falsified by an adopting repo needing a different count.
- 2026-09-06: plan gate chose no D-entry over appending one because the 5 was an M005 gate choice recorded only in its archive and the rulebook bullet is the operative record; falsified by a later dispute over why 3 that the CHANGELOG line cannot settle.
- 2026-09-06: T1 — `test_dropped_rows_count_toward_retention` rewritten as the fail-at-4 case (M01 + M04/M05 done + M06 dropped, asserts `4 terminal rows (retention 3)`), `test_three_terminal_rows_pass_retention` added (M01 + 2 done, asserts `PASS  terminal-row retention`); against the constant at 5 the fail case reds (validate exits 0, 4 rows under cap 5) and the pass case is green; suite 350 with that one red, hooks 126 green.
- 2026-09-06: T2 — `TERMINAL_ROW_RETENTION = 3`; T1's tests green; with the constant at 2 the pass case reds `3 terminal rows (retention 2)` (verified after clearing `__pycache__`: a same-size, same-second edit had served a stale `.pyc` and shown a false green first); restored to 3; scripts 350 + hooks 126 green.

## Decisions

## Review
