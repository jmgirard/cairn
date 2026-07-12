# M11: Shift phase headers up one level (H1 unit / H2 phase)

- **Status:** planned   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** —   <!-- m11-phase-header-levels; PR URL once opened -->

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

- [ ] Rewrite the "Phase header" bullet in `skills/shared/tracking-rules.md`
      (~L218–236): `##`→`#`, `###`→`##` throughout, including all skill
      examples and the "one `# Planning`" note.
- [ ] Update the single `Phase header:` line in each skill: milestone-plan,
      milestone-implement, milestone-review, milestone-brief, hotfix,
      cairn-init, cairn-release, milestone.
- [ ] Add `skills/tests/test_phase_header_levels.py` (mirror
      `test_gate_wording.py`): assert rulebook + skills use `#`/`##` and
      assert absence of `## Milestone <NN>` / `### Plan` forms.
- [ ] Append D-012 to `cairn/DECISIONS.md` superseding D-010.
- [ ] Remove `scannable-h2-phase-headers.md` and its `MEMORY.md` line.
- [ ] Run the full test suite; confirm green.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- D-012 (below) is cross-cutting and lands in cairn/DECISIONS.md, superseding
  D-010.

## Review
<!-- filled by /milestone-review -->
