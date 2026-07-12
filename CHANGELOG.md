# Changelog

## Unreleased

### Fixed
- The final merge-approval step in `/milestone-review` and `/hotfix` now
  requests authorization through a selectable chip rather than a free-text
  yes/no, matching the documented gate model. A regression guard locks the
  wording so it can't drift back.

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
