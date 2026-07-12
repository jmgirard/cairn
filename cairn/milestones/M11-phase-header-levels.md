# M11: Shift phase headers up one level (H1 unit / H2 phase)

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m11-phase-header-levels · https://github.com/jmgirard/cairn/pull/9

## Goal

Shift the phase-header convention up one level — unit-of-work `##`→`#`,
phase `###`→`##` — so both levels appear in Claude Desktop's TOC (H1/H2 only).

## Scope

**In:** rewrite the "Phase header" rule in `skills/shared/tracking-rules.md`
to use `#` (unit of work) and `##` (phase); update the one `Phase header:`
line in each of the 8 skills to match; append superseding D-012; add a
regression guard test locking the new levels; delete the now-redundant user
memory `scannable-h2-phase-headers`.

**Out:** any change to *when* headers are emitted (once-per-unit / at-each-
phase cadence is unchanged); flattening to a single header level (rejected —
the two-level nesting is preserved); reformatting the M09 archive summary
(append-only history stays verbatim).

## Acceptance criteria

- [ ] The "Phase header" bullet in `tracking-rules.md` states `#` for the
      unit of work and `##` for the phase, with every mapped example
      (`# Milestone <NN>` → `## Plan`, `# Hotfix`, `# cairn-init`,
      `# Release`, `# Status`, `# Review brief`, `# Planning`) shifted.
- [ ] All 8 skills' `Phase header:` lines use `#`/`##` — no skill still
      emits `## Milestone <NN>` or `### Plan`/`### Implement`/`### Review`.
- [ ] `cairn/DECISIONS.md` has D-012 superseding D-010, stating the Desktop-TOC
      rationale.
- [ ] `skills/tests/test_phase_header_levels.py` passes and fails if any
      skill or the rulebook reintroduces the old H2/H3 phase-header form
      (behavior: guard the convention against drift).
- [ ] `python3 -m unittest discover -s skills/tests` is green (existing
      `test_gate_wording.py` still passes).
- [ ] Memory file `scannable-h2-phase-headers.md` and its `MEMORY.md` index
      line are removed.

## Tasks

- [x] Rewrite the "Phase header" bullet in `skills/shared/tracking-rules.md`
      (~L218–236): `##`→`#`, `###`→`##` throughout, including all skill
      examples and the "one `# Planning`" note.
- [x] Update the single `Phase header:` line in each skill: milestone-plan,
      milestone-implement, milestone-review, milestone-brief, hotfix,
      cairn-init, cairn-release, milestone.
- [x] Add `skills/tests/test_phase_header_levels.py` (mirror
      `test_gate_wording.py`): assert rulebook + skills use `#`/`##` and
      assert absence of `## Milestone <NN>` / `### Plan` forms.
- [x] Append D-012 to `cairn/DECISIONS.md` superseding D-010.
- [x] Remove `scannable-h2-phase-headers.md` and its `MEMORY.md` line.
- [x] Run the full test suite; confirm green.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: shifted rulebook + 8 skills to `#`/`##`; added guard test
  test_phase_header_levels.py; full suite green (6 tests).
- 2026-07-11: appended D-012 (supersedes D-010); removed redundant memory
  scannable-h2-phase-headers + index line; suite green; status → review.
- 2026-07-11: review — all ACs verified fresh; PR #9; independent Opus
  review SHIP; hardened guard for over-shift + Migration token per its
  two low-severity flags; suite green (6 tests).

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- D-012 (below) is cross-cutting and lands in cairn/DECISIONS.md, superseding
  D-010.

## Review

2026-07-11 · PR #9 · docs-only, no CI configured.

**Acceptance criteria — all met (fresh evidence):**
- Rulebook states `#` unit / `##` phase; `# Milestone <NN>: <title>` →
  `## Plan` present, old `## Milestone <NN>: <title>` absent (grep: 0).
- All 8 skills' `Phase header:` lines use `#`/`##`; no `###`, no unit-at-H2.
- D-012 present in DECISIONS.md, "Supersedes D-010's level choice"; D-010
  left verbatim (append-only respected).
- Guard `test_phase_header_levels.py` passes; demonstrated to FAIL on both
  an old-form revert (H3 phase) and an over-shift (phase at H1), pass when
  restored.
- Full suite green: 6 tests (3 existing + 3 new).
- Memory `scannable-h2-phase-headers` file + `MEMORY.md` index line removed.

**Independent Opus review (fresh context):** verdict SHIP, no correctness
defects; convention shifted completely and consistently, no leaks in
DESIGN/README/templates, decision hygiene correct. Flagged two low-severity
guard gaps (over-shift not caught; `### Migration` token wouldn't
substring-match alone) → **fixed now**: per-skill assertion split on `→`
(unit must be H1, phase must be H2, not over-shifted), and forbidden-token
match dropped the trailing backtick.
