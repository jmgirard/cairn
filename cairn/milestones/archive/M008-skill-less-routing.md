# M08: Skill-less routing guardrails — done

**Status:** done · approved 2026-07-11 · high · Depends: — · PR #5 (squash
11d84b9). Lineage: "Skill-less routing guardrails" candidate / M02 openac pilot.

## Goal
Turn the always-loaded CLAUDE.md cairn section into an imperative
classify-first router so plain conversation routes to the right tier/skill
instead of bypassing the rulebook (which loads only once a skill fires).

## Outcome
All 5 criteria passed with fresh grep evidence. Rewrote
`skills/shared/templates/claude-md-section.md` from a passive description into
a classify-first router (20 body lines, under cap): classify every request,
apply tiers (trivial→main, bug→/hotfix, new work→/milestone-plan,
status/unsure→/milestone), never implement on main outside a branch, invoke
the skill first so the full rulebook loads. Dogfooded this repo's CLAUDE.md.
Rubric-to-text mapping + 5 dry-run scenarios recorded. Independent Opus review
clean; F1 fixed (say "the plugin's" `tracking-rules.md` so foreign repos
don't hunt for a missing `skills/` dir).

## Key decisions
- D-009: router carries routing only, not conduct (conduct stays in
  `tracking-rules.md`, loaded when a skill fires).
- Deferred to candidates: on-main commit-guard hook; live-openac router test.
