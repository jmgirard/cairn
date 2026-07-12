<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M38: Principles-touched slot in the milestone template

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m38-principles-touched-slot · https://github.com/jmgirard/cairn/pull/36

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

- [x] The milestone template (`skills/shared/templates/milestone.md`) carries
      a `Principles touched:` header field, plan-owned (create/amend-via-gate),
      defaulting to `—`; the tracking-rules section-ownership table has a row
      for it.
- [x] `/milestone-plan` SKILL directs the planner to fill the slot with the
      DESIGN principles the milestone touches (or `—`) — a `Principles touched:`
      directive line, parallel to the existing `Phase header:` directive.
- [x] `cairn_validate` FAILs when a live milestone's `Principles touched:` slot
      names an id that is not a current DESIGN.md principle, and passes when the
      slot is absent or every named id is a real principle — proven by a unit
      test with both a valid-slot and a bogus-id fixture.
- [x] `cairn_impact`'s report distinguishes a reference that comes from a
      `Principles touched:` slot (tagged authoritative/declared) from an
      incidental prose citation — proven by a unit test.
- [x] Both suites pass: `python3 -m unittest discover -s scripts/tests` and the
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
- [x] T4 — Wire `cairn_impact` to tag slot-sourced references as declared in
      its output; add a unit test covering a slot line vs a prose citation of
      the same principle.
- [x] T5 — Run both suites green; fix any fallout.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: started implementing; branch m38-principles-touched-slot.
- 2026-07-12: T1 — added Principles touched slot to template + section-ownership row.
- 2026-07-12: T2 — added Principles touched authoring directive to /milestone-plan step 4.
- 2026-07-12: T3 — cairn_validate 'principles slot valid' check (validate-if-present) + 3 fixtures; suite 52 green.
- 2026-07-12: T4 — cairn_impact tags slot-sourced refs '(declared)' + test; T5 — both suites green (53 scripts, 85 skills). Status → review.

## Decisions

## Review

**Evidence (fresh, 2026-07-12, PR #36):**
- AC1 — `milestone.md:9` carries `- **Principles touched:** —` (plan-owner comment); `tracking-rules.md:50` ownership row extended to "Priority, Depends on, Principles touched (header)".
- AC2 — `milestone-plan/SKILL.md:86` authoring directive under step 4.
- AC3 — `TestPrinciplesSlot`: valid-slot passes, `—` no-ops, bogus id (`GP9`) FAILs → all ok.
- AC4 — `TestImpact.test_slot_reference_tagged_declared`: slot line tagged `(declared)`, prose line untagged → ok.
- AC5 — scripts 53/53 ok; skills 85/85 ok; `cairn_validate` 11/11 (incl. `principles slot valid`) green.

**Consistency gate:** `cairn_validate` exit 0; coverage-complete PASS (AC1–5 → T1–5 mapped). No DESIGN principle changed (diff does not touch `DESIGN.md`) → `cairn_impact --changed` N/A. R gates (document/README/pkgdown/NEWS/Rbuildignore) waived — plugin repo, not an R package.

Diffstat: 8 files, +130/−10.

**Independent review (2 lenses + scorer):** [O] diff-bug and [S] blame-history reviewers both returned **no findings** — verified clean against ACs, DESIGN conventions, DECISIONS, and the M17/M24/M34 lessons (validate no-op-when-absent honored; `(declared)` suffix doesn't disturb existing impact ref-format assertions; ownership-table row passes M18 owner-parity). Scorer step N/A (empty actioned list). Three sub-threshold observations logged, not actioned: (1) `cairn_impact.references()` docstring didn't mention the new `(declared)` suffix — **fixed** here; (2) `_SLOT_LINE`/id regex duplicated across the two standalone reporter scripts — left (pre-existing `_PRINCIPLE` duplication; not worth a shared-module change now); (3) M38's own file carries no slot — left, it predates the field (validate-if-present tolerates it, same as M39).
