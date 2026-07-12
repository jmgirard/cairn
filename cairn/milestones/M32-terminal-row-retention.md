<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M32: Fold dropped rows into the ROADMAP retention cap (done-row → terminal-row)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m32-terminal-row-retention · https://github.com/jmgirard/cairn/pull/30

## Goal

Generalize the ROADMAP done-row retention cap to count terminal (`done` OR
`dropped`) rows against one shared limit of 5, renaming the rule, constant,
check, and gate label to "terminal-row retention," so dropped milestones are
pruned and counted like done ones.

## Scope

**In:**
- Reword the tracking-rules retention rule and the remedy line that names it
  so the cap counts terminal (`done` OR `dropped`) rows, limit unchanged at 5.
- Rename the enforcement identifiers to terminal-row semantics: the constant
  `DONE_ROW_RETENTION` → `TERMINAL_ROW_RETENTION`, the validator function
  `check_done_retention` → `check_terminal_retention` (count done+dropped),
  its output message, and the `CHECKS` gate label.
- Update the cross-references: the `cairn_next.py` explanatory comment, the
  cairn-init ROADMAP scaffold comment, and the consistency-gate check-name
  mentions in `/milestone` and `/milestone-review`.
- Update and extend the retention test in `test_scripts.py` — including a case
  proving a `dropped` row pushes a ROADMAP with ≤5 `done` rows over the cap.
- Prune this repo's ROADMAP to sit at the cap once M32 is `done`: drop the two
  oldest terminal rows (M26, M27) — archive files + git keep them.

**Out:**
- Changing the cap number — stays 5 (decided at plan gate).
- A separate budget for `dropped` rows — single shared terminal cap (plan
  gate, user option 1).
- Editing archived milestone summaries (M05, M10) that mention the old name —
  archive is verbatim history, append-only.
- Dependency-satisfaction semantics for a pruned terminal row — `archive_files`
  already unions done+dropped archive files into the satisfied set; if that
  ever mis-satisfies a dependency on a dropped milestone it becomes a candidate,
  not this milestone.

## Acceptance criteria

- [x] AC1 — `tracking-rules.md`'s retention rule and the weight-cap remedy line
      that names it state the cap counts terminal (`done` OR `dropped`) rows at
      a limit of 5; no "done-row retention" wording remains in the live
      rulebook.
- [x] AC2 — `cairn_validate` flags a ROADMAP with more than 5 terminal rows
      even when 5 or fewer are `done`, proven by a `test_scripts.py` case where
      done+dropped exceeds 5 with done ≤ 5.
- [x] AC3 — the constant, validator function/check, and gate label are named
      for terminal rows; a grep of the live scripts and skills (excluding
      `milestones/archive/`) finds no `DONE_ROW_RETENTION` /
      `check_done_retention` / "done-row retention" identifiers.
- [x] AC4 — `python3 -m unittest discover -s scripts/tests` passes (renamed +
      extended retention test plus the existing suite).
- [x] AC5 — `cairn_validate` passes on this repo with the terminal-row count at
      the cap after M32 is `done` (M26, M27 pruned). (This repo is not an R
      package — the template's `devtools::check()` line is waived per CLAUDE.md;
      the unittest suite + `cairn_validate` are the clean-checks bar.)

## Coverage

- AC1 → T1
- AC2 → T3, T6
- AC3 → T2, T3, T4, T5
- AC4 → T6, T8
- AC5 → T7, T8

## Tasks

- [x] T1 — Reword `skills/shared/tracking-rules.md` retention rule (L94–96) and
      the remedy phrase "enforce done-row retention" (L89) to terminal-row
      semantics + name.
- [x] T2 — Rename `DONE_ROW_RETENTION` → `TERMINAL_ROW_RETENTION` (value 5) in
      `scripts/cairn_scripts.py:47`.
- [x] T3 — Rewrite `check_done_retention` → `check_terminal_retention` in
      `scripts/cairn_validate.py` (count `done` + `dropped`; update the message
      and the `CHECKS` tuple label at L233 to "terminal-row retention").
- [x] T4 — Update the `scripts/cairn_next.py` comment (L20–22) to name
      terminal-row retention.
- [x] T5 — Update the cairn-init ROADMAP scaffold comment
      (`skills/cairn-init/SKILL.md:72`) and the consistency-gate check-name
      references in `skills/milestone/SKILL.md:48` and
      `skills/milestone-review/SKILL.md:59`.
- [x] T6 — In `scripts/tests/test_scripts.py`, rename `test_done_row_retention`
      → `test_terminal_row_retention`, assert on the terminal count, add the
      done≤5 + dropped-over-cap case (AC2), and update the `assert_fails` label.
- [x] T7 — Prune `cairn/ROADMAP.md`: remove the two oldest terminal rows (M26,
      M27) so the terminal count is 5 once M32 is `done`; refresh the hygiene
      date line.
- [x] T8 — Run `python3 -m unittest discover -s scripts/tests` and
      `cairn_validate` on this repo; confirm both clean.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: in-progress on m32-terminal-row-retention.
- 2026-07-12: T2–T4, T6 — renamed constant/check to terminal-row retention (count done+dropped), updated cairn_next comment, renamed+extended retention test with a dropped-over-cap case; 45 unittest tests pass.
- 2026-07-12: AC4/T8 wording fixed pytest→unittest (repo has no pytest; suite is unittest-based) — minor correction, verification intent unchanged.
- 2026-07-12: T1, T5 — reworded the tracking-rules retention rule + remedy line and the cairn-init scaffold + /milestone + /milestone-review check-name refs to terminal-row retention; live-file grep for "done-row retention" is clean.
- 2026-07-12: T7, T8 — pruned M26, M27 from ROADMAP (terminal count now 4, → 5 when M32 done); 45 unittest tests pass and cairn_validate is 10/10 green. All tasks done → status review.

## Decisions

## Review

PR #30 (draft). Consistency gate: `cairn_validate` 10/10 incl. `terminal-row
retention`; Coverage complete (AC1→T1, AC2→T3/T6, AC3→T2/T3/T4/T5, AC4→T6/T8,
AC5→T7/T8 — all tasks exist); no DESIGN principle changed (impact report
skipped); R gates waived (plugin repo).

Evidence per criterion:
- AC1 — `tracking-rules.md:94-95` reads "Terminal-row retention … terminal
  (`done` or `dropped`) rows combined"; remedy line (L89) says "terminal-row
  retention"; live-rulebook grep for "done-row retention" is empty.
- AC2 — `test_dropped_rows_count_toward_retention` (5 done at cap + 2 dropped →
  fails "terminal-row retention") passes; the done-only rule would have passed
  that ROADMAP.
- AC3 — grep of `scripts/` + `skills/` (excl. archive) for
  `DONE_ROW_RETENTION` / `check_done_retention` / "done-row retention" → empty.
- AC4 — `python3 -m unittest discover -s scripts/tests` → 45 tests OK.
- AC5 — `cairn_validate` PASS (terminal now 4 with M32=review); projected count
  at M32=done is `[M31,M30,M29,M28,M32]` = 5 = cap.

Independent fresh-context review (two distinct-evidence lenses, parallel):
- [O] diff-bug (Opus): no findings. Confirmed all identifiers renamed + wired
  (no `NameError` surface), AC2 test arithmetic genuinely fences the
  generalization, and the M26/M27 prune trips no orphan/dependency check.
- [S] blame-history (Sonnet): no findings. No D-entry ever recorded the `5` cap
  or done-only scope as a deliberate choice (plain M10 constant), so no standing
  decision is overridden; M26/M27 aren't cited as any live dependency. Noted the
  `archive_files` dropped-dep quirk predates this branch (M31 exhibits it on
  main) and is already in M32's Out scope — not introduced here.
No findings to score; scorer step a no-op.
