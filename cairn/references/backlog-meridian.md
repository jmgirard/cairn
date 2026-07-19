# Backlog.md + Meridian (enforced task scaffolding)

**Provenance.** Citekey `backlog-meridian` · ingested 2026-07-11 by M06 from https://github.com/MrLesk/Backlog.md and https://github.com/markmdev/meridian.
Pagination: —.
Extraction: verified 2026-07-19 against fresh shallow clones of both sources — Backlog.md v1.48.0 (commit `babd1d2`, 2026-07-19) and Meridian (commit `d9b8775`, last commit 2026-03-10) — every claim below re-read against source. Meridian's claims all held, its cited line still exact; three Backlog.md claims about lifecycle discipline were wrong and are corrected in place and marked. The M06 first pass checked one claim and git holds that prior status — observed 2026-07-19.

Sources: https://github.com/MrLesk/Backlog.md and
https://github.com/markmdev/meridian (studied 2026-07-11, re-read
2026-07-19; Meridian blocking-hook claim still exact at
`scripts/stop-checklist.py:69`, which returns `"decision": "block"`).

## Backlog.md

Markdown-native task manager: one file per task under `backlog/`
(frontmatter: id, status, dependencies, priority; body: description,
acceptance criteria fenced in `<!-- AC:BEGIN/END -->` markers,
implementation plan/notes, final summary), with terminal kanban, web
UI, and an MCP server over the same data. Closest cousin to cairn's
file model — even has `decisions/` and `milestones/` dirs. Lifecycle
discipline is one consolidated `src/guidelines/agent-guidelines.md`
whose "Phase discipline: What goes where" section names three phases —
Creation (title, description, AC, labels/priority/assignee),
Implementation (plan + appended progress notes), and Wrap-up (final
summary, verify AC and Definition of Done). Closing a task is a
completeness gate rather than a prohibition: the agent is told to check
its own criteria (`--check-ac`), check DoD items (`--check-dod`), add a
final summary and set `-s Done`, under "NEVER mark a task as Done
without completing ALL items above". Work exceeding the criteria has two
sanctioned routes — widen the AC, or open a follow-up task.

*(M06, corrected M91: this page previously reported "three staged
instruction guides" whose execution stage "forbade" the agent from
checking ACs or setting terminal status, and a finalization rule of "no
follow-up tasks without user approval". The guides are now one file, the
agent performs both closing actions itself, and creating a follow-up
task is explicitly offered rather than gated on approval.)*

Enforcement is purely instructional — no hooks; per-file statuses with
no aggregating index.

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
- **Machine-checkable AC fencing** (Backlog.md): the
  `<!-- AC:BEGIN/END -->` markers are real and still parsed, so a script
  could refuse to check a criterion lacking a cited evidence line —
  mechanizes cairn's fresh-evidence review rule. *The
  evidence-before-checkbox half rested on the finalization rule
  corrected above; Backlog.md requires the criterion be checked, not
  that evidence be cited for it, so this is cairn's own extension of
  their fencing rather than a practice to copy (M06, corrected M91).*
- Search-first creation and explicit scope-change escalation prose.

## What cairn does that they lack

A sole status authority (Backlog.md scatters status across files;
Meridian has no task concept), In/Out scope per milestone, append-only
decision + work-log ledgers, weight caps and compressed archives, and
gated transitions ending in a mandatory human merge approval
(Meridian's plan gate covers planning only; Backlog.md's gates are
prose).
