# Milestone 15: Sync Impact Report on principle changes

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m15-sync-impact-report   <!-- PR URL once opened -->

## Goal

When a DESIGN.md principle (IPn/GPn) is added, changed, or retired, report
every `cairn/` file that cites it so downstream references reconcile in the
same change.

## Scope

**In:** A deterministic reporter `scripts/cairn_impact.py` that, given one or
more principle ids (or `--changed`, deriving changed principles from the git
diff of `DESIGN.md`), greps the tracked `cairn/` files (milestone files,
`DECISIONS.md`, `ROADMAP.md`, `DESIGN.md`) for `IPn`/`GPn` tokens and prints
referencing `file:line`. Read-only; reuses the `cairn_scripts` parser (no
duplication); exit 2 outside a cairn repo — matching `cairn_validate` /
`cairn_status` / `cairn_next` (M10). A step in the `/milestone-review`
consistency gate names when to run it (a milestone that touches a principle).
A lock test in `scripts/tests/` with a fixture repo.

**Out:** Impact of `tracking-rules.md` *rule* changes on the plugin's own
skills — that keys on plugin-internal structure, meaningful only in this repo
(the dogfood case), not portably in adopting repos → candidate if wanted.
`--json` output → existing "Scripts --json" candidate.

## Acceptance criteria

- [ ] `scripts/cairn_impact.py IP2 GP4` prints the referencing `cairn/`
      `file:line` for each named principle; exit 0.
- [ ] `--changed` derives the changed principle ids from the working/committed
      diff of `cairn/DESIGN.md` and reports on those.
- [ ] Runs read-only, reuses `cairn_scripts`, exits 2 outside a cairn repo
      (parity with the other reporters).
- [ ] `/milestone-review` consistency gate names when to run it (principle
      touched by the milestone).
- [ ] `scripts/tests/test_scripts.py` covers it with a fixture: a principle
      cited in a milestone file + `DECISIONS.md` is reported at the right
      lines; an uncited principle reports none.
- [ ] Full `scripts/tests/` + `skills/tests/` + `cairn_validate` pass.

## Tasks

- [ ] Write `scripts/cairn_impact.py` (principle-id args + `--changed`), on
      the `cairn_scripts` parser and `resolve_root`/`NotCairn` idiom.
- [ ] Add fixture + cases to `scripts/tests/test_scripts.py`.
- [ ] Add the invoke-when step to `skills/milestone-review/SKILL.md`
      consistency gate.
- [ ] Note the reporter in `cairn/DESIGN.md` Architecture (scripts layer).
- [ ] Run all test suites + `cairn_validate`.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
