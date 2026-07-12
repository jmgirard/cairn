<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M38: Principles-touched slot in the milestone template

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m38-principles-touched-slot

## Goal

Give each milestone a declared `Principles touched:` header slot, and make
`cairn_validate`/`cairn_impact` treat it as the authoritative source of a
milestone's principle impact.

## Scope

**In:** a plan-owned `Principles touched:` header field in the milestone
template; a `/milestone-plan` directive to author it; a `cairn_validate`
check that a live milestone's slot names only current DESIGN.md principles;
`cairn_impact` marking a slot-declared reference as authoritative in its
report. Slot value is a comma-separated list of `IPn`/`GPn` ids, or `—`.

**Out:** requiring the slot on already-archived milestones (validate is
validate-if-present, mirroring M34's coverage check — no back-fill); a
mechanical "did the diff touch a principle the slot omits" cross-check
(candidate → toolchain-profiles-adjacent, needs semantic diff reading);
fuzzy prose-citation linting (the slot is the fix, not prose rewriting).

## Acceptance criteria

- [ ] The milestone template (`skills/shared/templates/milestone.md`) carries
      a `Principles touched:` header field, plan-owned (create/amend-via-gate),
      defaulting to `—`; the tracking-rules section-ownership table has a row
      for it.
- [ ] `/milestone-plan` SKILL directs the planner to fill the slot with the
      DESIGN principles the milestone touches (or `—`) — a `Principles touched:`
      directive line, parallel to the existing `Phase header:` directive.
- [ ] `cairn_validate` FAILs when a live milestone's `Principles touched:` slot
      names an id that is not a current DESIGN.md principle, and passes when the
      slot is absent or every named id is a real principle — proven by a unit
      test with both a valid-slot and a bogus-id fixture.
- [ ] `cairn_impact`'s report distinguishes a reference that comes from a
      `Principles touched:` slot (tagged authoritative/declared) from an
      incidental prose citation — proven by a unit test.
- [ ] Both suites pass: `python3 -m unittest discover -s scripts/tests` and the
      skills guard tests (`skills/tests/`).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T3, T4, T5

## Tasks

- [x] T1 — Add the `Principles touched:` field to the milestone template (after
      `Depends on:`, plan-owner comment) and a row to the section-ownership
      table in `shared/tracking-rules.md`.
- [x] T2 — Add a `Principles touched:` authoring directive to
      `skills/milestone-plan/SKILL.md` (parallel to `Phase header:`).
- [x] T3 — Add a `cairn_validate` check parsing the slot on live milestone
      files; every named id must be a current DESIGN.md principle. No-ops when
      the slot is absent (so no `Tree.build` change per the M34 lesson); add
      targeted valid/bogus fixtures with a dedicated builder in
      `scripts/tests/test_scripts.py`.
- [ ] T4 — Wire `cairn_impact` to tag slot-sourced references as declared in
      its output; add a unit test covering a slot line vs a prose citation of
      the same principle.
- [ ] T5 — Run both suites green; fix any fallout.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: started implementing; branch m38-principles-touched-slot.
- 2026-07-12: T1 — added Principles touched slot to template + section-ownership row.
- 2026-07-12: T2 — added Principles touched authoring directive to /milestone-plan step 4.
- 2026-07-12: T3 — cairn_validate 'principles slot valid' check (validate-if-present) + 3 fixtures; suite 52 green.

## Decisions

## Review
