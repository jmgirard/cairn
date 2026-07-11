<!-- Appended to the repo's CLAUDE.md by /cairn-init. Keep the section body under ~25 lines. -->

## Project tracking (cairn)

This repo uses the cairn plugin. **Before acting on any request, classify it
and route** — the tracking rulebook only loads once a cairn skill fires, so
starting work in plain conversation silently bypasses the work tiers and the
git model. Classify first:

- **Trivial** (no runtime surface — typo, comment, tracking edit): commit
  directly to main.
- **User-visible bug**: invoke `/hotfix`.
- **New work, a design decision, or more than one sitting**: invoke
  `/milestone-plan` (then `/milestone-implement` → `/milestone-review`).
- **Status, "what's next", or unsure which tier**: invoke `/milestone`.
- **Never implement code on main** outside a milestone/hotfix branch; nothing
  reaches main without the user's explicit approval at the review gate.

Whenever the request is anything but trivial, invoke the skill *first* so the
full rulebook (`skills/shared/tracking-rules.md`) and its conduct load — do
not reconstruct the rules here from memory. All project state lives under
`cairn/` (**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone
files · Decisions → DECISIONS · History → archive + git**); never record
status or TODOs in this file. Claude's persistent memory never holds project
state; `cairn/` files win any conflict.
