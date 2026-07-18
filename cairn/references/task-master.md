# Task Master (claude-task-master, eyaltoledano)

**Provenance.** Citekey `task-master` · ingested 2026-07-11 by M06 from https://github.com/eyaltoledano/claude-task-master.
Pagination: —.
Extraction: verified 2026-07-18 against a fresh shallow clone at
`task-master-ai` v0.43.1 — every claim below re-read against source; three
were wrong and are corrected in place and marked — observed 2026-07-18.
The M06 first pass was an [S] subagent study of the clone and docs with no
claim checked against the source; git holds that prior status.

Source: https://github.com/eyaltoledano/claude-task-master (studied
2026-07-11; [S] subagent study of clone + docs; re-verified 2026-07-18 at
v0.43.1).

## What it is

An npm package exposing the same task-management engine as a CLI and an
MCP server (43 registry tools, tiered core=7 / standard=14 / all to manage
context budget — `mcp-server/src/tools/tool-registry.js`). Three configurable
model roles (main / research / fallback) across 19 providers (M06 said "~10";
corrected 2026-07-18 — `src/ai-providers/` holds 19 provider modules). It can
run key-free two ways: a `claude-code` provider that shells the local Claude
Code CLI (`isRequiredApiKey()` returns false), and an `mcp` provider that
samples the host session in an MCP environment — M06 described these as one
mechanism (corrected 2026-07-18).

## Workflow model

- **State is JSON, not markdown**: `.taskmaster/tasks/tasks.json` is
  authoritative (committed); per-task text files are regenerated
  exports. Tasks carry id, status, dependencies (cycle-validated),
  priority, testStrategy, nested subtasks.
- **Tags = parallel task contexts** with independent ID sequences. The
  `branchTagMapping` field exists in `state.json` and `tag-management.js`
  still writes it, but **auto-switch on branch checkout is disabled
  upstream** — both `checkAndAutoSwitchGitTag` and its `…Sync` variant
  early-return behind the comment "DISABLED: Automatic git workflow is too
  rigid and opinionated. Users should explicitly use git-tag commands"
  (`scripts/modules/utils/git-utils.js:283,300`). M06 recorded the feature as
  live; corrected 2026-07-18. Upstream's own task notes show the automatic
  scope was cancelled 2025-06-14, so this was already dead at ingestion — a
  wrong extraction, not drift.
- **PRD → tasks by LLM under a strict Zod schema** (`.strict()`, fields
  fixed, metadata added by code not the model); `--append` re-parses
  without clobbering.
- **Complexity pipeline**: an AI pass scores each task 1–10 and writes a
  regenerable per-tag complexity report (recommended subtask count +
  tailored expansion prompt) — schema-enforced at
  `src/schemas/analyze-complexity.js` (`complexityScore: min(1).max(10)`,
  `recommendedSubtasks`, `expansionPrompt`). `expand-all` consumes the report
  per task but **does not order by complexity**: it filters on status and
  iterates in `tasks.json` array order
  (`scripts/modules/task-manager/expand-all-tasks.js:92,121`). M06 said
  "highest-first"; corrected 2026-07-18.
- `set-status --status=done` is a free write — the status string is checked
  against a fixed vocabulary (`isValidTaskStatus`,
  `src/constants/task-status.js`) but nothing gates *whether the work was
  done*; no evidence, no checks, no approval.

## What cairn should steal

- **Explicit branch↔context mapping** — cairn ties branch to milestone
  by naming convention only; a recorded mapping (milestone header
  already holds Branch/PR) could drive automatic "which milestone am I
  in" detection. **Weigh against upstream's verdict:** they built exactly
  this, then disabled it as "too rigid and opinionated" in favour of
  explicit commands (see the tags bullet above). The negative result is the
  more useful import here — added 2026-07-18 on re-verification.
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
