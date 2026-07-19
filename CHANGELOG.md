# Changelog

## Unreleased

- Fixed: a references page with no provenance block could be reported as
  having an incomplete one — or pass the check outright — when ordinary
  prose happened to wrap so that a line began with the word "provenance".
  The block heading is now recognized as a label rather than as any line
  starting with that word.

## 1.0.0 (2026-07-16)

First stable release. cairn is a milestone-driven development workflow and
tracking system for Claude Code: a language-agnostic core with per-repo
toolchain profiles, human-gated skills for planning, implementing, and
reviewing work, and a self-auditing `cairn/` file system that keeps all
project state in plain markdown. Everything below has been piloted on real
repositories since 0.1.0.

- **Nine skills** (was eight): `/design-interview` joins the set — a
  standalone two-phase interview (facts → principles) that fills or deepens
  a repo's `DESIGN.md`; `/cairn-init` hands off to it, and it can be re-run
  to deepen a thin design doc.
- **Toolchain profiles**: the R-only assumptions of 0.1.0 are gone. Each
  repo declares its toolchain in `cairn/PROFILE.md` with seven slots
  (verify, consistency-gate, test-doctrine, release-walk, init-detection,
  greenfield-openers, changelog); three reference profiles ship — r-package
  (CRAN walk), python (pyproject/pytest/PyPI), and generic. A repo without
  a profile is inferred from its markers, so pre-profile adopters keep
  working unchanged.
- **Validation doctrine** for statistical/numeric work, in its own module:
  five named oracle types (frozen, live, invariant, closed-form,
  simulation-coverage), a two-independent-types bar per numeric result,
  reproducibility and primary-sources hard stops, and an auditable oracle
  registry whose shape is the repo's choice.
- **Guardrail hooks** (seven): session-start tracking injection, an
  uncommitted-tracking stop guard, marker-based merge-approval enforcement
  (approval survives failed merge retries, never a successful merge), a
  default-branch force-push guard, a commit guard, and a memory-boundary
  nudge. Fail-safe by construction; best-effort Windows fallback.
- **Self-audit scripts**: `cairn_validate` (hard checks plus non-failing
  advisories), `cairn_next` (what's workable, mechanically), `cairn_status`,
  and `cairn_impact` (principle-impact tracing).
- **Interaction discipline**: decisions happen at explicit gates with
  selectable chips (including merge approval — no free-text yes/no);
  produced conclusions and durable-record text appear verbatim in chat
  before being accepted or committed; phase transitions are navigable
  chapters.
- **Migration**: `/cairn-init` migrates precursor tracking systems via an
  interactive, PR-based protocol with a read-only dry-run mode and an
  opening environment check; history is entombed verbatim, never rewritten.
- **Docs**: MIT license; README with a worked example, install paths
  (symlink dev install or marketplace), and an explicit no-lock-in bail-out.

## 0.1.0 (2026-07-11)

## 0.1.0 (2026-07-11)

Initial build from the DRAFT_2.md spec.

- Eight skills: `/milestone` (status + health audit + routing),
  `/milestone-plan`, `/milestone-implement`, `/milestone-review`,
  `/milestone-brief` (Fable RB/RR protocol), `/hotfix`, `/cairn-release`,
  `/cairn-init` (scaffold / repair / migration).
- Shared rulebook (`skills/shared/tracking-rules.md`) read by every skill:
  ownership boundaries, weight caps, status vocabulary, work tiers, git and
  approval model, CI waiting rules, model strategy, oracle doctrine, source
  ingestion, test-scope guidance, R guardrails.
- Templates: milestone, review brief, decision entry, CLAUDE.md section.
- Unpiloted — see DRAFT_2.md §11 for the pilot plan.
