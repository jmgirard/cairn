# BMAD-METHOD (bmad-code-org)

**Provenance.** Citekey `bmad-method` · ingested 2026-07-11 by M06 from https://github.com/bmad-code-org/BMAD-METHOD (V6 clone).
Pagination: —.
Extraction: verified 2026-07-19 against a fresh shallow clone at BMAD-METHOD v6.10.0 (commit `c23f234`, 2026-07-18) — every claim below re-read against source; two were wrong and are corrected in place and marked, and a third mark records where the second of those corrections propagated into the steal list rather than a third wrong claim. The M06 first pass checked one claim and git holds that prior status — observed 2026-07-19.

Source: https://github.com/bmad-code-org/BMAD-METHOD (studied 2026-07-11,
re-read 2026-07-19 at v6.10.0 — still the V6 line; sprint-status claim
cited at `src/bmm-skills/4-implementation/bmad-sprint-planning/SKILL.md:8`,
still exact).

## What it is

An installable agent framework (`npx bmad-method install` →
`_bmad/` config + `_bmad-output/` artifacts) organized around persona
agents bound to skills: Analyst, PM, Architect, Developer, UX, Writer,
plus module agents (Test Architect etc.). Four phases: analysis →
planning (PRD) → solutioning
(architecture, epics/stories, readiness gate) → implementation;
`bmad-quick-dev` routes small, zero-blast-radius changes straight to
implementation and sends everything else through planning
(*the named "Quick Flow" this page reported was removed — `removals.txt`
lists `bmad-quick-flow` and its solo-dev agents, consolidated into the
Developer agent per CHANGELOG #2177/#2179/#2186; M06, corrected M91*).
A `bmad-help` meta-skill inspects project state and routes the user; it
is invocable at any point and every persona agent's greeting advertises
it (*not "run automatically at the end of every workflow" as this page
reported — exactly 1 of 26 non-agent skills, `bmad-product-brief`,
invokes it at its close; M06, corrected M91*).

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
  routing chips already do this. *BMAD no longer validates the pattern:
  the corrected fact above shows `bmad-help` is user-invoked, not
  auto-run, so cairn's chips are ahead here rather than confirmed by a
  peer. Kept as a note on cairn's own design, not as borrowed evidence
  (M06, corrected M91).*
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
