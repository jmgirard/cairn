# Task Master (claude-task-master, eyaltoledano)

**Provenance.** Citekey `task-master` · ingested 2026-07-11 by M06 from https://github.com/eyaltoledano/claude-task-master.
Pagination: —.
Extraction: unverified — [S] subagent study of the clone and docs, with no claim checked against the source at ingestion.

Source: https://github.com/eyaltoledano/claude-task-master (studied
2026-07-11; [S] subagent study of clone + docs).

## What it is

An npm package exposing the same task-management engine as a CLI and an
MCP server (~40 tools, tiered core/standard/all to manage context
budget). Three configurable model roles (main / research / fallback)
across ~10 providers; inside Claude Code it can run key-free by sampling
the host session.

## Workflow model

- **State is JSON, not markdown**: `.taskmaster/tasks/tasks.json` is
  authoritative (committed); per-task text files are regenerated
  exports. Tasks carry id, status, dependencies (cycle-validated),
  priority, testStrategy, nested subtasks.
- **Tags = parallel task contexts** with independent ID sequences; a
  `branchTagMapping` in `state.json` can auto-switch context on git
  branch checkout.
- **PRD → tasks by LLM under a strict Zod schema** (`.strict()`, fields
  fixed, metadata added by code not the model); `--append` re-parses
  without clobbering.
- **Complexity pipeline**: an AI pass scores each task 1–10 and writes a
  regenerable per-tag complexity report (recommended subtask count +
  tailored expansion prompt); `expand` consumes it highest-first.
- `set-status --status=done` is a free write — no verification gate.

## What cairn should steal

- **Explicit branch↔context mapping** — cairn ties branch to milestone
  by naming convention only; a recorded mapping (milestone header
  already holds Branch/PR) could drive automatic "which milestone am I
  in" detection.
- **Complexity-scored right-sizing as a plan-time advisory** — a cheap
  formalization of cairn's split tripwires (score tasks, recommend
  splits before implement starts).
- **Tiered tool exposure** if cairn ever ships an MCP surface.
- Strict-schema validation for any machine-written tracking fragment.

## What cairn does that it doesn't

Human-first artifacts (Task Master's source of truth is
agent-optimized JSON; markdown is derived), a skimmable single status
index, gated transitions (its statuses are freely settable), review
evidence and merge approval, append-only decision/work-log ledgers,
weight caps (its own dogfood tasks.json holds 93+ tasks across 9 tags,
unbounded), and any enforced test doctrine (testStrategy is free-text
LLM output).
