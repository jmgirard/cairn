# cairn (plugin repo)

This repo IS the cairn plugin (skills/, templates, rulebook) and dogfoods
its own tracking format by hand under `cairn/`. It is not an R package:
R-specific gates (devtools, pkgdown, .Rbuildignore) are waived here.

## Project tracking (cairn)

**Before acting on any request, classify it and route** — the tracking
rulebook only loads once a cairn skill fires, so working in plain
conversation silently bypasses the work tiers and the git model. Classify
first:

- **Trivial** (no runtime surface — typo, comment, tracking edit): commit to
  main.
- **User-visible bug**: invoke `/hotfix`.
- **New work, a design decision, or more than one sitting**: invoke
  `/milestone-plan` (then `/milestone-implement` → `/milestone-review`).
- **Status, "what's next", or unsure which tier**: invoke `/milestone`.
- **Never implement code on main** outside a milestone/hotfix branch; nothing
  reaches main without explicit user approval at the review gate.

Anything but trivial → invoke the skill *first* so the full rulebook
(`skills/shared/tracking-rules.md`) and its conduct load; don't reconstruct
the rules from memory. State lives under `cairn/`: **Architecture → DESIGN ·
Status → ROADMAP · Tasks → milestone files · Decisions → DECISIONS · History
→ archive + git**. Never record status or TODOs here; memory never holds
project state — `cairn/` files win any conflict.
