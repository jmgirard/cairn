# BMAD-METHOD (bmad-code-org)

**Provenance.** Citekey `bmad-method` · ingested 2026-07-11 by M06 from https://github.com/bmad-code-org/BMAD-METHOD (V6 clone).
Pagination: —.
Extraction: partly verified at ingestion — the sprint-status claim was checked against `bmad-sprint-planning/SKILL.md:8`; the rest is an [S] subagent study, not re-read since.

Source: https://github.com/bmad-code-org/BMAD-METHOD (studied
2026-07-11; [S] subagent study of V6 clone; sprint-status claim
verified: bmad-sprint-planning/SKILL.md:8).

## What it is

An installable agent framework (`npx bmad-method install` →
`_bmad/` config + `_bmad-output/` artifacts) organized around persona
agents bound to skills: Analyst, PM, Architect, Developer, UX, Writer,
plus module agents (Test Architect etc.). Four phases: analysis →
planning (PRD) → solutioning (architecture, epics/stories, readiness
gate) → implementation; a "Quick Flow" skips ceremony for small work.
A `bmad-help` meta-skill inspects project state and routes the user —
run automatically at the end of every workflow.

## Workflow model

- **Story files are context packages**: `bmad-create-story` pre-loads
  each story with architecture excerpts, previous-story learnings, and
  git-commit intelligence so the dev agent starts warm — explicitly to
  stop agents "reinventing wheels" and "lying about completion".
- **`sprint-status.yaml`** is a single state-machine ledger (epic and
  story status enums with legal transitions documented inline, both as
  comments and parseable YAML).
- **Section-level write permissions**: the dev agent may touch only
  named story-file sections (checkboxes, Dev Agent Record, File List,
  Change Log, Status). Definition-of-Done is a literal checklist
  artifact with a PASS/FAIL block filled before status flips to review.
- Review agent (`bmad-code-review`) is adversarial, recommended to run
  on a *different LLM* than the implementer.
- Context passes between agents only via committed markdown/YAML;
  sessions are meant to be fresh chats per workflow.

## What cairn should steal

- **Section-level write allow-lists** for milestone files during
  implement (append-only work log generalized: name exactly which
  sections each skill may touch — mechanically checkable).
- **Previous-milestone intelligence harvest** at plan time: mine the
  prior work log + recent commits for "what worked/what bit us" before
  writing the next plan (cairn reads DECISIONS but not lessons).
- **Baseline-commit capture** in the milestone header at implement
  start — makes "what changed for this milestone" a diff, not a guess.
- Auto-running the status/routing skill at every workflow end — cairn's
  routing chips already do this; BMAD validates the pattern.
- Different-model review as stated doctrine (cairn does this via fresh
  Opus subagents; worth stating the *why* in the rulebook).

## What cairn does that it doesn't

A sole status authority with weight caps and compressed archives
(sprint-status.yaml can drift from epic files and needs repair
workflows); an append-only cross-project decision ledger; a hard human
merge gate (BMAD hands off agent-to-agent by default); skills whose
entire job is gating a transition; a codified oracle test doctrine.
BMAD also assumes an agile-product shape (epics/sprints/personas) and
installs a heavy ecosystem; cairn stays a thin tracking layer.
