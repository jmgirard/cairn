# M22: Generalize cairn beyond `main`; recalibrate the mature-repo CLAUDE.md cap

- **Status:** done · approved 2026-07-12 · PR #19
- **Depends on:** —

## Goal

Fix the two cairn defaults the M20 ackwards pilot proved don't survive a mature
repo — the `main`-hardcoded git model and the `<80` CLAUDE.md cap.

## Outcome

- **Weight cap (D-018):** dropped the whole-file `<80` CLAUDE.md cap; cairn now
  hard-caps only the appended `## Project tracking (cairn)` section (30 lines,
  `claude_section_line_count` + `check_caps`). Repo doctrine uncapped; a bloated
  cairn section still fails.
- **Default branch (G1/G9):** git model, CLAUDE template, and cairn-init §2 say
  "the default branch" (glossed `main`/`master`); cairn-init detects it via
  `git symbolic-ref --short refs/remotes/origin/HEAD` (current-branch fallback).
- Locked by `test_default_branch_parameterized.py` (5) + 2 cap fixtures. Review:
  2 findings, both <80 (the 65 fallback-wording one fixed anyway). 51 skills +
  33 scripts green; audit 9/9. Out: operational `main` commands in other skills
  → ROADMAP candidate.
- **Decision:** D-018 — CLAUDE.md cap measures the cairn section, not the file.
