# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system. The core is language-agnostic; each
adopting repo declares a **toolchain profile** (`cairn/PROFILE.md`, six slots:
verify, consistency-gate, test-doctrine, release-walk, init-detection,
greenfield-openers) that supplies the language/toolchain-specific commands the
operational skills read, instead of the core hardcoding one language (M45
spine, M46 rewire, M47 release; D-024/D-025 keep the oracle doctrine universal,
orthogonal to the profile). Three profiles ship — `r-package` (devtools/CRAN),
`python` (pytest/PyPI), and `generic`; this repo runs `generic`. Logic lives here (skills, rules,
templates); state lives in each adopting repo under `cairn/`. Full design
rationale: DRAFT_2.md (this file summarizes; the draft is removed at 1.0, at
which point its still-relevant content moves here).

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
- `skills/shared/profiles/` — the shipped reference toolchain profiles
  (`r-package`, `python`, `generic`); `cairn-init` instantiates one into a repo's
  `cairn/PROFILE.md`, and the operational skills read its slots.
- `hooks/hooks.json` + python3 (stdlib) scripts (M07) — the enforcement
  layer, all no-op outside cairn repos. Five hooks: `session_context`
  (SessionStart context injection); `stop_guard` (Stop-guard on uncommitted
  `cairn/` tracking); and three PreToolUse guards — `merge_guard` (single-use
  `cairn/.merge-approved` marker, technically backing IP1), `commit_guard`
  (nudge against committing on the default branch), and `memory_guard` (GP4
  memory-boundary nudge, D-017). The two nudges are advisory, never blocking.
- `scripts/` + python3 (stdlib) reporters (M10) — the deterministic read
  layer: `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate), `cairn_impact` (principle
  → citing `cairn/` file:line, for the Sync Impact Report on IPn/GPn changes;
  M15). Read-only; reuse the hooks' `cairn_common` parser (no duplication);
  exit 2 outside a cairn repo. `/milestone` invokes them instead of
  re-deriving status by LLM; `/milestone-review` runs `cairn_impact --changed`
  when a milestone touches a principle; semantic checks stay LLM-owned.

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

- IP1: Nothing reaches the default branch without explicit user approval at a
  gate.
- IP2: Prior state is surfaced, never silently obeyed or silently
  overridden.
- IP3: Nothing the user asked for is silently dropped (conservation:
  remainder ledger, migration ledger).
- IP4: History is never fabricated, rewritten, or renumbered — append-only
  work-logs and DECISIONS (supersede, never edit), no-invention migration,
  entomb-verbatim, IDs never reused (D-032).
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

- Single-author, single-environment: every workflow has been exercised only by
  the author, on macOS + Claude Code with the full model roster, and only on
  repos the author shaped. No external adopter, and no external-repo migration,
  has run yet.
- Hooks are unverified on Windows: `hooks.json` invokes `python3`, which stock
  Windows lacks on PATH (it is `py`/`python`) — the guardrail hooks may fail
  silently there until a launcher fallback lands.
- Conduct rules (question gates, routing chips, chapter markers, AC fencing)
  are enforced as prose: guard tests lock the skill/rulebook wording, not the
  runtime behavior, and live honoring is only spot-verified (hooks snapshot at
  process start, so a rule's runtime effect needs a fresh session to observe).
  A deliberate architectural bet, noted plainly rather than papered over.
