# cairn (plugin repo)

This repo IS the cairn plugin (skills/, templates, rulebook) and dogfoods
its own tracking format by hand under `cairn/`. Its toolchain profile is
`generic` (declared in `cairn/PROFILE.md`): the language-agnostic core with no
R gates; `verify` is this repo's `python3 -m unittest` suites.

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
(the plugin's `skills/shared/tracking-rules.md`) and its conduct load; don't
reconstruct the rules from memory. State lives under `cairn/`: **Architecture → DESIGN ·
Status → ROADMAP · Tasks → milestone files · Decisions → DECISIONS · Lessons
→ LESSONS · History → archive + git**. Never record status or TODOs here; memory never holds
project state — `cairn/` files win any conflict.
