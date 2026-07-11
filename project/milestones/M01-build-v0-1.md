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
- 2026-07-11: catch-up — post-review refinements landed on main (GP/IP
  prefixes, rename to cairn, marketplace.json, git-model + context-hygiene
  doctrine, recommended-option rule for chips); review gate still pending.
- 2026-07-11: /milestone-review run — criteria evidence gathered, consistency
  gate passed, independent Opus review triaged (see Review). Fixes committed
  directly to main, matching M01's built-on-main exception; awaiting Jeff's
  approval (AC5).

## Decisions

See project/DECISIONS.md D-001 … D-007 (D-001…D-005 extracted from DRAFT_2
§10; D-006 naming; D-007 marketplace.json timing).

## Review

2026-07-11 evidence, gathered by command:

- AC1 ✓ all 8 skills exist; frontmatter complete; each reads the shared
  rulebook first (grep: 8/8 reference it at line 9).
- AC2 ✓ rulebook headings cover all 11 required topic areas (heading list
  checked against the criterion one-for-one).
- AC3 ✓ four templates present; structure matches DRAFT_2 §6 (elaborations
  only, no omissions; §6.4 skill-list gap found by review, fixed).
- AC4 ✓ README covers all six §12 subsections + an Install section.
- Consistency gate (plugin-adapted; R gates waived per ROADMAP note):
  plugin.json + marketplace.json parse; name matches D-006; CHANGELOG has
  the 0.1.0 entry.
- Independent fresh-context review (Opus): 0 blockers, 3 should-fix,
  7 nits; verdict fit-to-ship. Triage: fixed now — D-007 records the
  marketplace.json timing (finding 1), full skill list added to
  claude-md-section template (3), single-in-progress guard added to
  /milestone-implement (4), stale D-ref updated (9). Already tracked as
  candidates — README install paths (2), repo CLAUDE.md (10, audit flag).
  Bundled into a new candidate row — nits 5–8 (v0.2 polish).
