# M13: Wire deterministic scripts into review + plan

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —
- **Branch/PR:** m13-script-wiring   <!-- PR URL once opened -->

## Goal

Wire M10's read-only scripts into `/milestone-review` and `/milestone-plan`
so those skills stop re-deriving mechanical facts by LLM, and add a
date-format check to `cairn_validate`.

## Scope

**In:**
- `/milestone-review` step 4 (consistency gate) runs `cairn_validate.py` as
  its first, mechanical cairn-file check — before the R-package gates —
  with a failure routing status back to `in-progress` like any gate failure.
- `/milestone-plan` step 1 (confirm nothing `in-progress`) / collision-check
  readiness runs `cairn_next.py` for the mechanical active/workable picture
  instead of eyeballing the ROADMAP.
- A new `cairn_validate` check that flags non-ISO calendar dates in tracked
  cairn/ files (enforces the tracking-rules absolute-dates rule), with tests.

**Out:**
- `--json` output mode → candidate row (deferred; no consumer today — the
  scripts' only readers are the skills, which parse text).
- Review-pipeline upgrades (reviewer fan-out, Haiku-triage decision) → stays
  the existing candidate row; the never-Haiku relaxation needs its own gate.
- Milestone-file mechanics (allow-lists, lessons harvest, Sync Impact Report)
  → stays the existing candidate row.
- Catching prose relative dates ("yesterday", "last week") — undecidable by
  regex; stays LLM-owned in the semantic audit. This check only catches
  *misformatted* calendar dates.

## Acceptance criteria

- [ ] `skills/milestone-review/SKILL.md` step 4 names
      `${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py` as a mechanical check
      whose failure routes status back to `in-progress`. (evidence: grep the
      skill file)
- [ ] `skills/milestone-plan/SKILL.md` step 1 names
      `${CLAUDE_PLUGIN_ROOT}/scripts/cairn_next.py` for the in-progress /
      readiness check. (evidence: grep the skill file)
- [ ] `cairn_validate` gains a date-format check: it FAILs (non-zero exit,
      named FAIL line) on a tracked cairn/ file containing a non-ISO date and
      PASSes on a clean ISO-only tree. Behavior under test: non-ISO date
      detection. (evidence: new `unittest` cases, one injected defect + clean
      pass, per the suite's inject-one-defect convention)
- [ ] Full script suite green:
      `python3 -m unittest discover -s scripts/tests`. (evidence: run output)
- [ ] Existing `skills/tests` suite still green after the skill edits.
      (evidence: run output)

## Tasks

- [x] Add `check_dates` to `scripts/cairn_validate.py` (new entry in `CHECKS`)
      that scans tracked cairn/ markdown for date-like tokens and flags any
      not in `YYYY-MM-DD` form; keep the pattern conservative to avoid
      false-positiving on prose/citations (see Decisions). Add `unittest`
      cases to `scripts/tests/test_scripts.py`: clean-tree pass + one injected
      non-ISO date. Run the suite.
- [x] Wire `cairn_validate.py` into `skills/milestone-review/SKILL.md` step 4
      as the first mechanical check; state that a FAIL returns status to
      `in-progress` (consistent with the existing gate-failure rule at :52).
- [x] Wire `cairn_next.py` into `skills/milestone-plan/SKILL.md` step 1 /
      collision-check readiness.
- [x] Run `python3 -m unittest discover -s scripts/tests` and the
      `skills/tests` suite; update work-log.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Promoted from the
  "Deterministic-script wiring beyond /milestone" candidate (M10 Out).
- 2026-07-11: T1 — added `check_dates` (9th validate check, conservative
  non-ISO patterns) + test; suite 19 green; real-repo validate all-PASS.
- 2026-07-11: T2-T4 — wired cairn_validate into review step 4, cairn_next
  into plan step 1; scripts 19 + skills 17 tests green. → review.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Date check is conservative-by-construction: it targets recognizable
  *wrong-format* calendar dates (e.g. `MM/DD/YYYY`, `DD-MM-YYYY`,
  `Mon DD`/`DD Mon YYYY`), not every 3-digit-ish token, to avoid flagging
  reference citations, version numbers, or line/page anchors. A false
  negative (a missed weird format) is preferred over a false positive that
  makes the gate cry wolf.

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
