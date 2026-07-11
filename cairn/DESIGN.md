# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system for R packages. Logic lives here
(skills, rules, templates); state lives in each adopting repo under
`cairn/`. Full design rationale: DRAFT_2.md (this file summarizes; the
draft is removed at 1.0, at which point its still-relevant content moves
here).

## Architecture

- `.claude-plugin/plugin.json` — manifest.
- `skills/<name>/SKILL.md` × 8 — workflow logic; each reads the shared
  rulebook first and never restates it.
- `skills/shared/tracking-rules.md` — the single rulebook.
- `skills/shared/templates/` — milestone, brief, decision, CLAUDE.md section.

## Conventions

- Skills state workflows; the rulebook states rules; nothing is said twice.
- Skill descriptions are written for trigger accuracy: `/hotfix`
  auto-triggers on bug reports; phase skills trigger on explicit
  intent/chips.

## Design Principles

GP<n> = Guiding Principle (default stance; tradeable with stated
justification). IP<n> = Inviolable Principle (hard constraint; changing one
requires an explicit user decision + D-entry).

- GP1: Efficient — store decisions and outcomes, not minutiae; caps +
  archiving keep always-read files small.
- GP2: Reliable — one status authority; tracking travels with code;
  self-auditing; stateless resume.
- GP3: Portable — identical across repos; one-command adoption; repo
  specifics layer on top without forking the core.
- IP1: Nothing reaches main without explicit user approval at a gate.
- IP2: Prior state is surfaced, never silently obeyed or silently
  overridden.
- IP3: Nothing the user asked for is silently dropped (conservation:
  remainder ledger, migration ledger).

## Known issues

- Unpiloted (see M02/M03). Expect trigger-description tuning and cap
  adjustments after real use.
