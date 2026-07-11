<!-- Appended to the repo's CLAUDE.md by /cairn-init. Keep under ~20 lines. -->

## Project tracking (cairn)

This repo uses the cairn plugin. All project state lives in markdown
under `project/`. Boundary rule: **Architecture → DESIGN · Status → ROADMAP ·
Tasks → milestone files · Decisions → DECISIONS · History → archive + git.**

- Start with `/milestone` — status snapshot, health audit, suggested next
  action. Never record status or TODOs in this file; anything time-varying
  rots here.
- All eight skills: `/milestone`, `/milestone-plan`, `/milestone-implement`,
  `/milestone-review`, `/milestone-brief` (Fable escalation), `/hotfix`,
  `/cairn-release`, `/cairn-init`.
- Work tiers: trivial edits (no runtime surface) commit directly to main;
  user-visible bugs go through `/hotfix`; everything else is a milestone
  (`/milestone-plan` → `/milestone-implement` → `/milestone-review`).
- Ideas: "add X to the candidates" appends a ROADMAP row — no ceremony.
- Nothing merges to main without the user's explicit approval at review.
- Claude's persistent memory never holds project state; `project/` files win
  any conflict.
- All skills read the plugin's `skills/shared/tracking-rules.md` first and
  obey it.
