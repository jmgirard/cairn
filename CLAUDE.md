# cairn (plugin repo)

This repo IS the cairn plugin (skills/, templates, rulebook) and dogfoods
its own tracking format by hand under `project/`. It is not an R package:
R-specific gates (devtools, pkgdown, .Rbuildignore) are waived here.

## Project tracking (cairn)

All project state lives in markdown under `project/`. Boundary rule:
**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone files ·
Decisions → DECISIONS · History → archive + git.**

- Start with `/milestone`. Never record status or TODOs in this file.
- Work tiers: trivial edits commit to main; user-visible bugs → `/hotfix`;
  everything else is a milestone (plan → implement → review).
- Nothing merges to main without explicit user approval at review.
- All skills read `skills/shared/tracking-rules.md` first and obey it.
