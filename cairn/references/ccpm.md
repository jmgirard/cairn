# ccpm — Claude Code Project Manager (automazeio)

Source: https://github.com/automazeio/ccpm (~8k stars; studied
2026-07-11, full skill source read + local flow executed hands-on).

## What it is

One skill implementing a five-phase delivery pipeline: PRD → epic →
numbered task files → GitHub Issues → parallel agents in a shared epic
worktree. State is frontmatter-schema'd markdown under `.claude/prds/`
and `.claude/epics/<name>/`; GitHub Issues become the shared status
surface after sync (task files renamed to issue numbers).

## Workflow model

- **Script-first rule**: deterministic reads (status, standup, next,
  blocked, validate) are bash scripts over frontmatter, run verbatim —
  LLM reserved for reasoning. 14 shipped scripts.
- **Task metadata for parallelism**: `depends_on`, `parallel`,
  `conflicts_with` arrays; an analysis step decomposes an issue into
  parallel "streams" (file-scoped lanes), each executed by an agent
  committing to one shared worktree with pull-rebase coordination.
- **Traceability doctrine**: "requirements live in files, not heads";
  every code change traces to issue → task → epic → PRD.
- Artifact-heavy: per-issue analysis file, per-stream progress files,
  execution-status trackers, github-mapping.

## Hands-on observations (2026-07-11, scratch repo)

Ran the local flow (PRD → epic → 2 tasks) and the scripts. `next.sh`
correctly derived readiness from `depends_on`; `status.sh`/`standup.sh`
gave instant zero-token status; `validate.sh` checked structure,
references, frontmatter — a mechanized mini consistency-gate — but
printed a ⚠️ (missing optional dir) while summarizing "Warnings: 0"
(minor script bug). GitHub sync/execute phases verified from source
only (per M06 trial-method decision).

## What cairn should steal

- **Deterministic status scripts.** Cairn's `/milestone` snapshot and
  hygiene audit re-derive everything by LLM each session; a shipped
  `status`/`validate` script would be instant, token-free, and
  drift-proof. Biggest single steal in the whole survey.
- `conflicts_with` / `parallel` task metadata — cairn tasks are ordered
  serially; explicit file-scope conflict lanes are a cheap enabler if
  cairn ever wants parallel task execution.

## What cairn does that it doesn't

No user approval gates anywhere — "code reviewed" is a checkbox in a
task template, not a gate; agents commit and epics merge per
instruction. No review evidence, no acceptance-criteria verification
step, no decision log, no weight caps (artifacts proliferate per issue),
no archive compression, no oracle/test doctrine. GitHub is a hard
dependency for the full loop (cairn works offline/local-only). ccpm
optimizes for parallel throughput; cairn optimizes for auditability and
safe merges.
