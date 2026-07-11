# Backlog.md + Meridian (enforced task scaffolding)

Sources: https://github.com/MrLesk/Backlog.md and
https://github.com/markmdev/meridian (studied 2026-07-11; [S] subagent
study of clones; Meridian blocking-hook claim verified:
scripts/stop-checklist.py:69 returns `"decision": "block"`).

## Backlog.md

Markdown-native task manager: one file per task under `backlog/`
(frontmatter: id, status, dependencies, priority; body: description,
acceptance criteria fenced in `<!-- AC:BEGIN/END -->` markers,
implementation plan/notes, final summary), with terminal kanban, web
UI, and an MCP server over the same data. Closest cousin to cairn's
file model — even has `decisions/` and `milestones/` dirs. Lifecycle
discipline is three staged instruction guides (creation: search-first
+ AC quality bar; execution: forbidden from checking ACs or setting
terminal status; finalization: objective verification evidence required
per AC, "no follow-up tasks without user approval"). Enforcement is
purely instructional — no hooks; per-file statuses with no aggregating
index.

## Meridian

A Claude Code plugin whose enforcement is **hook-based and genuinely
blocking**: SessionStart/PreCompact hooks re-inject `WORKSPACE.md`,
routed docs, and git state as additionalContext (compaction survival);
a Stop hook returns `{"decision":"block"}` until a
tests/lint/docs/review checklist passes; PreToolUse guards deny
mis-scoped reviewer spawns; a PreCompact/SessionEnd session-learner
spawns a headless session to fold learnings back into docs. Long-term
docs carry `summary`/`read_when` frontmatter so a router surfaces the
right file without grepping. No native task schema (delegates to an
optional external tracker); planning skill gates plan-mode exit on a
reviewer score ≥9.

## What cairn should steal

- **Blocking hooks** (Meridian): cairn's gates are convention; a
  PreToolUse/Stop hook could *technically* stop a merge without
  approval or a session ending with uncommitted work. Direct upgrade
  path for the existing "plugin hooks for guardrail feedback" candidate.
- **SessionStart re-injection** of ROADMAP + active milestone —
  insurance for cairn's stateless-resume doctrine instead of relying on
  the skill remembering to read files.
- **`read_when` doc-routing frontmatter** for `references/` notes.
- **Machine-checkable AC fencing + evidence-before-checkbox rule**
  (Backlog.md): a script could refuse to check a criterion lacking a
  cited evidence line — mechanizes cairn's fresh-evidence review rule.
- Search-first creation and explicit scope-change escalation prose.

## What cairn does that they lack

A sole status authority (Backlog.md scatters status across files;
Meridian has no task concept), In/Out scope per milestone, append-only
decision + work-log ledgers, weight caps and compressed archives, and
gated transitions ending in a mandatory human merge approval
(Meridian's plan gate covers planning only; Backlog.md's gates are
prose).
