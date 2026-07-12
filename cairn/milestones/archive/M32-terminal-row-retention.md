# M32 — Fold dropped rows into the ROADMAP retention cap (done-row → terminal-row)

**Status:** done · PR #30 · merged 2026-07-12

## Outcome

The ROADMAP retention cap now counts **terminal** rows — `done` OR `dropped` —
against one shared limit of 5, instead of `done` only, so dropped milestones
are pruned and counted like done ones. Renamed to "terminal-row retention"
across: `tracking-rules.md` rule + remedy line; the `TERMINAL_ROW_RETENTION`
constant; the `check_terminal_retention` validator (counts done+dropped) +
its message + `CHECKS` gate label; the `cairn_next.py` comment; the cairn-init
scaffold comment; and the `/milestone` + `/milestone-review` check-name refs.
Extended `test_scripts.py` (renamed retention test + new
`test_dropped_rows_count_toward_retention`). Pruned M26, M27 to land this repo
at the 5-terminal cap once M32 was done.

## Key points

- Cap number stays 5; single shared budget for done+dropped (plan gate, user
  option 1). No D-entry — the `5`/done-only scope was never a recorded decision.
- Pruned **two** rows (M26, M27), not one: M32 itself consumes a terminal slot
  (M28 stale-count trap, flagged at plan).
- Evidence: 45 unittest tests pass; `cairn_validate` 10/10; both review lenses
  clean. `archive_files` dropped-dep quirk predates this branch (Out scope).
