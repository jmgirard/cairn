# Milestone 14: Section write allow-lists per skill

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —
- **Branch/PR:** m14-section-allow-lists · https://github.com/jmgirard/cairn/pull/12

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

- [x] Draft the section → owner → write-mode table; add it to the ownership
      section of `skills/shared/tracking-rules.md`.
- [x] Update `skills/shared/templates/milestone.md` comments to name each
      section's owner.
- [x] Add allow-list cross-references to plan/implement/review SKILL.md.
- [x] Write `skills/tests/test_section_allow_lists.py` (table ↔ template
      section parity).
- [x] Run `skills/tests/` + `scripts/tests/` + `cairn_validate`; fix any
      drift.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: section-ownership table added to tracking-rules.md; template comments tag each section's owner.
- 2026-07-11: plan/implement/review SKILL.md cross-reference their writable sections (no rule restated).
- 2026-07-11: test_section_allow_lists.py locks table↔template parity; skills/tests (20) + scripts/tests (21) + cairn_validate all green.
- 2026-07-11: review fixes — owner-parity test (F1), pointer-trim plan/implement (F2), write-mode vocab (F3); F4 rejected. skills/tests 21 green.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

Evidence (2026-07-11, PR #12):

- **C1 table covers every template section:** `test_section_allow_lists.py::test_table_matches_template_sections` passes; parity confirmed non-vacuous — 11 sections each side, dropping any row breaks parity.
- **C2 template tags each owner:** milestone.md comments carry `owner:` tags on all 4 header fields + 7 H2 sections.
- **C3 skills cross-reference the allow-list:** `test_phase_skills_reference_the_allow_list` passes (plan/implement/review each contain "section-ownership table"); pointers, no rule restated.
- **C4 drift lock:** the parity test fails on any table↔template mismatch (verified by removing a row).
- **C5 suites + validate:** skills/tests 20 passed · scripts/tests 21 passed · `cairn_validate` all checks passed.

Consistency gate: `cairn_validate` exit 0. R gates (devtools/README.Rmd/pkgdown/NEWS/.Rbuildignore) waived — plugin repo, no R surface (CLAUDE.md).

Independent fresh-context review (Opus subagent): SHIP WITH NITS, all criteria met. Triage:
- F1 (major) name-only lock missed owner drift → **fixed**: added `test_owner_parity` cross-checking the table's Writing-skill column against the template `owner:` tags (verified it flags a flipped tag).
- F2 (minor) plan/implement restated owned sections vs AC3 → **fixed**: trimmed both to pure pointers.
- F3 (minor) `create-once` used but undefined → **fixed**: Branch/PR uses `create`; added `check-off` to the legend + verb-check.
- F4 (nit) parenthetical-stripping can mask a cosmetic-only rename → **rejected** (reviewer agrees cosmetic-only; known limitation of the substring approach).
