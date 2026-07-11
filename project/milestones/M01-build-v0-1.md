# M01: Build plugin v0.1 from DRAFT_2 spec

- **Status:** review   <!-- mirror; project/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** —
- **Branch/PR:** — (built directly; repo had no prior git history)

## Goal

Translate DRAFT_2.md into a working v0.1 plugin: manifest, shared rulebook,
templates, and all eight skills, plus public-facing README and changelog.

## Scope

**In:** plugin.json; tracking-rules.md; 4 templates; 8 SKILL.md files;
README.md (from DRAFT_2 §12); CHANGELOG.md; dogfooded `project/` for this
repo.

**Out:** piloting in real repos → M02/M03. Marketplace publishing → candidate
(post-1.0). LICENSE + public release prep → candidate.

## Acceptance criteria

- [x] Every DRAFT_2 §5 skill exists with frontmatter (name, description,
      argument-hint) and reads the shared rulebook first.
- [x] tracking-rules.md covers: ownership table, weight caps, universal
      rules, status vocabulary + gatekeepers, sizing/tiers, git + CI rules,
      gates + chips, model strategy, oracle doctrine + source ingestion,
      test scope, R guardrails.
- [x] All four templates exist and match DRAFT_2 §6.
- [x] README contains the §12 user guide + install instructions.
- [ ] Human review by Jeff (this is the `review` state's approval gate).

## Tasks

- [x] .claude-plugin/plugin.json
- [x] skills/shared/tracking-rules.md
- [x] skills/shared/templates/ (milestone, brief, decision, claude-md-section)
- [x] skills/milestone/SKILL.md (entry point + audit)
- [x] skills/milestone-plan/SKILL.md
- [x] skills/milestone-implement/SKILL.md
- [x] skills/milestone-review/SKILL.md
- [x] skills/milestone-brief/SKILL.md
- [x] skills/hotfix/SKILL.md
- [x] skills/cairn-release/SKILL.md
- [x] skills/cairn-init/SKILL.md
- [x] README.md, CHANGELOG.md
- [x] Dogfood project/ (ROADMAP, DECISIONS, this file)

## Work log

- 2026-07-11: built all v0.1 files from DRAFT_2.md in one session; set to
  review pending Jeff's read-through.

## Decisions

See project/DECISIONS.md D-001 … D-005 (extracted from DRAFT_2 §10).

## Review

Pending: Jeff's read-through of skills + rulebook, then pilot via M02/M03.
