# spec-kit (GitHub)

**Provenance.** Citekey `spec-kit` · ingested 2026-07-11 by M06 from https://github.com/github/spec-kit.
Pagination: —.
Extraction: verified 2026-07-19 against a fresh shallow clone at spec-kit 0.13.1.dev0 (commit `57cc518`, 2026-07-18; latest release 0.13.0, 2026-07-17) — every claim below re-read against source and all held; the three citations gained their full paths and the command inventory was completed, neither being a correction to a claim. The M06 first pass checked three claims and git holds that prior status — observed 2026-07-19.

Source: https://github.com/github/spec-kit (studied 2026-07-11, re-read
2026-07-19; citations `templates/commands/specify.md:124-128`,
`templates/commands/constitution.md:87`,
`templates/plan-template.md:39,106` — all three still exact).

## What it is

GitHub's spec-driven development toolkit: a `specify` CLI bootstraps
`.specify/` (constitution, templates, scripts) and renders 10 slash
commands per agent (30+ agents supported), namespaced `/speckit.*`. The
pipeline is constitution → specify → clarify → plan → tasks → analyze →
implement → converge; two further commands sit outside it (`checklist`,
a custom per-feature checklist generator, and `taskstoissues`, which
converts tasks into dependency-ordered GitHub issues). Specs are meant
to *generate* code, not merely guide it.

## Workflow model

- **One long-lived artifact**: `memory/constitution.md` — SemVer'd
  governing principles; every amendment must prepend a "Sync Impact
  Report" naming which dependent templates still need updating.
- **Everything else is per-feature**: each feature gets a siloed
  `specs/<NNN>-<slug>/` (spec, plan, research, data-model, contracts,
  tasks, checklists). **No cross-feature index or roadmap exists by
  design**; post-merge spec fate ("flow-back" vs "flow-forward" vs
  "living spec") is explicitly left to team convention.
- **Structural enforcement**: `[NEEDS CLARIFICATION]` markers capped at
  3, forcing prioritized questions over guessing; the plan template
  embeds a Constitution Check gate with a Complexity Tracking table that
  must justify any violation; `/analyze` is a read-only severity-graded
  (CRITICAL→LOW) cross-artifact drift check with a requirement→task
  coverage table; `/converge` appends gap tasks only, never rewrites.

## What cairn should steal

- **Sync Impact Report** — when tracking-rules or an IP/GP changes, a
  structured "what else must now change" comment is a better protocol
  than hoping the consistency gate catches drift.
- **Coverage-table analyze pass**: criterion→task→evidence mapping with
  severity grades would sharpen `/milestone-review`'s consistency gate.
- **Cap-at-3 prioritized clarification markers** — a tighter form of
  cairn's 2–5-question gate discipline, worth citing in the rulebook.
- Constitution-gate-in-the-template pattern: cairn's IP/GP principles
  are checked at review; embedding a "which principles does this plan
  touch" slot in the milestone template would move that check earlier.

## What cairn does that it doesn't

Project-level continuity: no roadmap/status index, no decision log, no
archive, no weight caps, no append-only discipline — a spec-kit project
is a pile of independent feature dirs. No merge-approval gate (a git
extension can even auto-commit). Test doctrine is a constitution
*example*, not tooling. Spec-kit is strongest exactly where cairn is
thinnest (pre-implementation artifact rigor) and absent where cairn is
strongest (longitudinal project memory and gates).
