# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system for R packages. Logic lives here
(skills, rules, templates); state lives in each adopting repo under
`cairn/`. Full design rationale: DRAFT_2.md (this file summarizes; the
draft is removed at 1.0, at which point its still-relevant content moves
here).

Positioning (M06, references/competitive-landscape.md): cairn is change
control + longitudinal project memory for agent-driven work — a niche no
surveyed system occupies. Markdown state is commodity; the differentiators
are governed state (sole authority, caps, archives), skill-gated
transitions, human-gated merges, and a domain verification doctrine.

## Architecture

- `.claude-plugin/plugin.json` — manifest.
- `skills/<name>/SKILL.md` × 9 — workflow logic; each reads the shared
  rulebook first and never restates it. Includes `design-interview`, a
  standalone two-phase (facts → principles) DESIGN.md elicitation interview
  (D-013), offered from `/cairn-init`'s routing chip; it recommends running
  the session on Fable (D-014).
- `skills/shared/tracking-rules.md` — the single rulebook.
- `skills/shared/templates/` — milestone, brief, decision, CLAUDE.md section.
- `hooks/hooks.json` + python3 (stdlib) scripts (M07) — the enforcement
  layer: SessionStart context injection, Stop-guard on uncommitted `cairn/`
  tracking, PreToolUse merge-guard (single-use `cairn/.merge-approved`
  marker) technically backing IP1. No-op outside cairn repos.
- `scripts/` + python3 (stdlib) reporters (M10) — the deterministic read
  layer: `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate). Read-only; reuse the
  hooks' `cairn_common` parser (no duplication); exit 2 outside a cairn
  repo. `/milestone` invokes them instead of re-deriving status by LLM;
  semantic checks stay LLM-owned.

## Conventions

- Skills state workflows; the rulebook states rules; nothing is said twice.
- Skill descriptions are written for trigger accuracy: `/hotfix`
  auto-triggers on bug reports; phase skills trigger on explicit
  intent/chips.

## Design Principles

IP<n> = Inviolable Principle (hard constraint; changing one requires an
explicit user decision + D-entry). GP<n> = Guiding Principle (default
stance; tradeable with stated justification). IP block first; numbers run
within each type and are never reused.

- IP1: Nothing reaches main without explicit user approval at a gate.
- IP2: Prior state is surfaced, never silently obeyed or silently
  overridden.
- IP3: Nothing the user asked for is silently dropped (conservation:
  remainder ledger, migration ledger).
- GP1: Efficient — store decisions and outcomes, not minutiae; caps +
  archiving keep always-read files small.
- GP2: Reliable — one status authority; tracking travels with code;
  self-auditing; stateless resume.
- GP3: Portable — identical across repos; one-command adoption; repo
  specifics layer on top without forking the core.
- GP4: Generalizable fixes live in the shared artifact, not per-user memory.
  A defect or lesson that would recur for other users is encoded in the
  skills, rulebook, or a guard test; memory holds only per-user meta-context
  and never substitutes for shared plugin logic (corollary of D-001, GP3;
  see D-011).

## Known issues

- Unpiloted (see M02/M03). Expect trigger-description tuning and cap
  adjustments after real use.
