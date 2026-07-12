# Milestone 14: Section write allow-lists per skill

- **Status:** planned   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —
- **Branch/PR:** —   <!-- m14-section-allow-lists; PR URL once opened -->

## Goal

Formalize which skill may write which milestone-file section, so plan,
implement, and review can't silently clobber each other's sections.

## Scope

**In:** A section-ownership table in `tracking-rules.md` mapping every
milestone-file section (header fields, Goal, Scope, Acceptance criteria,
Tasks, Work log, Decisions, Review) to its writing skill(s) and write-mode
(create / amend-via-gate / append); `templates/milestone.md` comments naming
each section's owner; plan/implement/review SKILL.md cross-referencing the
sections they may write; a structural lock test that fails if the table and
the template drift apart.

**Out:** *Authorship* enforcement by `cairn_validate` — git records no
which-skill-wrote-what signal, so it can't be mechanized; enforcement stays
conventional (like the existing ownership boundaries) + the structural test.
Deterministic required-section conformance checks → candidate. "Strict
schemas for machine-written fragments" stays its M06-steal candidate row.

## Acceptance criteria

- [ ] `tracking-rules.md` contains a section-ownership table covering every
      section present in `templates/milestone.md`, each mapped to writing
      skill(s) + write-mode. (test: section-parity)
- [ ] `templates/milestone.md` comments name the owning skill for each
      section.
- [ ] plan/implement/review SKILL.md each reference the allow-list (which
      sections they may write); no rule restated (DESIGN convention: nothing
      said twice).
- [ ] `skills/tests/test_section_allow_lists.py` asserts the table's sections
      exactly match the template's sections (no unmapped section, no phantom
      row) and fails on drift.
- [ ] Full test suite + `python3 scripts/cairn_validate.py` still pass.

## Tasks

- [ ] Draft the section → owner → write-mode table; add it to the ownership
      section of `skills/shared/tracking-rules.md`.
- [ ] Update `skills/shared/templates/milestone.md` comments to name each
      section's owner.
- [ ] Add allow-list cross-references to plan/implement/review SKILL.md.
- [ ] Write `skills/tests/test_section_allow_lists.py` (table ↔ template
      section parity).
- [ ] Run `skills/tests/` + `scripts/tests/` + `cairn_validate`; fix any
      drift.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
