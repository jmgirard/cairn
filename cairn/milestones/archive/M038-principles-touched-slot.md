# M38 — Principles-touched slot in the milestone template

**Status:** done · approved 2026-07-12 · PR #36

## Goal
Give each milestone a declared `Principles touched:` header slot and make
`cairn_validate`/`cairn_impact` treat it as the authoritative source of a
milestone's principle impact.

## Outcome
- Template gained a plan-owned `Principles touched:` header field (default `—`);
  section-ownership table row added; `/milestone-plan` directs filling it.
- `cairn_validate` check `principles slot valid`: FAILs a live milestone whose
  slot names a non-existent DESIGN.md principle; no-ops on absent/`—`
  (validate-if-present, M34 pattern — no `Tree.build` change).
- `cairn_impact` tags slot-sourced references `(declared)`, separating
  authoritative declarations from incidental prose citations (closes M17
  fragility).
- Tests: +4 fixtures (valid / `—` no-op / bogus-id FAIL / declared-vs-prose);
  53 scripts + 85 skills green; `cairn_validate` 11/11.

## Key notes
- Independent review (2 lenses + scorer): zero findings; one docstring nit fixed.
- Out (still candidates): diff-touches-a-principle cross-check; prose linting;
  sharing the duplicated slot/id regex across the two reporter scripts.
