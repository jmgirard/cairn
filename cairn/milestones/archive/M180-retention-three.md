# M180: ROADMAP terminal-row retention drops from 5 to 3

**Status:** done (2026-09-06, PR #187 https://github.com/jmgirard/cairn/pull/187)

**Goal:** The ROADMAP table keeps only the 3 most recent done/dropped rows, so the injected status view shows less finished work.

**Outcome:** `TERMINAL_ROW_RETENTION = 3` in `scripts/cairn_scripts.py`, the one definition `cairn_validate`'s `terminal-row retention` check reads for both its comparison and its message (`N terminal rows (retention 3): …`). `scripts/tests/test_scripts.py` pins the constant from both sides: `test_dropped_rows_count_toward_retention` rewritten as the fail-at-4 case (M01 + 2 done + 1 dropped), `test_three_terminal_rows_pass_retention` added as the pass-at-3 case; the fail case reds with the constant at 5, the pass case at 2. The three live statements of the count say 3: the tracking-rules terminal-row retention bullet, the cairn-init ROADMAP skeleton comment, the M111 LESSONS line. This repo's ROADMAP pruned M175 and M176 (archive + git). CHANGELOG Unreleased entry names the check, the cap, the red text an adopter sees on upgrade, and the prune remedy. A per-repo PROFILE slot and a D-entry were rejected at the plan gate (the 5 was an M005 gate choice with no D-entry).

**Decisions:** none.

**Review:** user-facing tier, three-lens fan-out. Blame-history: no findings. Prior-review: no inline PR comments (probe empty), no archived finding contradicted; two items noted. Diff-bug: four findings, none actioned as code — the T4 hygiene stamp naming a stale status (rejected, overwritten at hygiene), archiving M180 overflowing the new cap (handled here: M177 pruned in the archive commit per the M111 lesson), the pre-existing 7-row retention test no longer discriminating the boundary (rejected, unmodified; the two new cases pin it), RB04's archived "5 most recent" (rejected, history). A stale-`.pyc` false green when flipping the constant, hit at T2 and again at review, extended the M56 "green is only as wide as what you ran" lesson. Nothing graduated or retired.
