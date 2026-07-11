# feature-dev (Anthropic official plugin)

Source: https://github.com/anthropics/claude-plugins-official
`plugins/feature-dev/` @ dc72937 (studied 2026-07-11, full source read).

## What it is

A single `/feature-dev` command implementing a 7-phase guided workflow
(discovery → codebase exploration → clarifying questions → architecture
design → implementation → quality review → summary), plus three Sonnet
agents: code-explorer, code-architect, code-reviewer. ~340 lines of
markdown total; no hooks, no state files.

## Workflow model

- **Fan-out with focus lenses.** Each phase launches 2–3 agents of the
  same type with *different lenses*: explorers target "similar features"
  vs "architecture" vs "UX"; architects target "minimal changes" vs
  "clean architecture" vs "pragmatic balance"; three reviewers split
  simplicity / correctness / conventions.
- **Agents return reading lists, not conclusions alone** — the
  orchestrator must then read the 5–10 files each agent names, building
  its own context rather than trusting summaries.
- **Hard user gates**: clarifying questions ("DO NOT SKIP", wait for
  answers), approach choice, pre-implementation approval, review triage.
- **Reviewer confidence scoring**: issues rated 0–100 against a written
  rubric; only ≥80 reported.

## What cairn should steal

- Focus-lens fan-out for `/milestone-review`'s independent review (one
  fresh Opus agent today) and `/milestone-plan` investigation.
- "Return a reading list" instruction for Explore subagents — cairn asks
  for file:line citations but not a ranked must-read list.
- Confidence rubric for review findings (shared with code-review plugin).

## What cairn does that it doesn't

Everything durable: no tracking files, no status model, no branch/PR/merge
doctrine, no test doctrine, no memory beyond the session (TodoWrite only).
A feature-dev session that dies mid-phase leaves nothing resumable. It is
a *session choreography*, orthogonal to project tracking — closest to
cairn's plan→implement→review arc but evaporates on session end.

## Hands-on observations

(from source-execution trial, 2026-07-11 — see work log)
