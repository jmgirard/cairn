# M55: Milestone-file cap exempts the Review section

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** —
- **Branch/PR:** m55-milestone-file-cap

## Goal

Cap a live milestone file on its plan-owned body only, exempting the
review-exclusive `## Review` section, so review evidence never scrambles
plan-owned content.

## Scope

**In:** Change the milestone weight-cap so `check_caps` measures only the
plan-owned body (every line before the `## Review` heading) against
`MILESTONE_CAP` (150) for live files; add a fence-aware body-measuring helper
in `cairn_scripts.py`; state the exemption in the tracking-rules weight-caps
text; guard the wording (mutation-registered) and the stated↔enforced
agreement.

**Out:**
- Splitting the budget (120/40) or adding a separate Review sub-cap — decided
  against at the plan gate (keeps plan discipline at 150 unchanged, one
  number); re-openable by superseding the milestone's D-entry, not replanned.
- Exempting the milestone-local `## Decisions` section — stays counted; if it
  ever blows the cap on its own, that becomes a candidate row, not this scope.
- The archive ≤25-line cap — unchanged; archived summaries carry no `## Review`
  section by construction.

## Acceptance criteria

- [ ] A live milestone file whose plan-owned body (lines before `## Review`) is
      under 150 but whose *total* exceeds 150 because of Review evidence PASSES
      the weight-caps check — the recurring evidence-vs-cap scramble
      (M19/M22/M33/M50) is gone. Evidence: a scripts/tests fixture.
- [ ] Plan discipline is unchanged: a live milestone whose plan-owned body is
      itself ≥150 lines still FAILS weight-caps. Evidence: a scripts/tests
      fixture (the existing `test_over_cap_milestone` no-Review case plus a
      with-Review case whose body alone is over).
- [ ] Measurement is correct at the edges: a file with no `## Review` section
      measures the whole file exactly as today (back-compat), and a literal
      `## Review` line inside a fenced code block in the plan-owned body does
      not false-terminate the body scan (M45 fence-state trap). Evidence: two
      scripts/tests fixtures.
- [ ] The tracking-rules weight-caps text states the `## Review` exemption, the
      stated cap (150) equals the enforced `MILESTONE_CAP`, and a prose-guard
      locks the wording and is registered in the mutation harness (blanking it
      fails the guard). Evidence: skills/tests guard + a `Mutation(...)` entry.
- [ ] `verify` slot clean: `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s skills/tests` both pass.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T3, T4, T5

## Tasks

- [ ] T1 — Add `milestone_body_line_count(path)` to `cairn_scripts.py`
      (mirroring `claude_section_line_count`, cairn_scripts.py:205): count lines
      up to — not including — the first `## Review` heading, tracking ```/~~~
      fence state so a fenced `## Review` in the body is not the boundary (M45);
      whole-file count when no `## Review`; None if unreadable.
- [ ] T2 — In `check_caps` (cairn_validate.py:78-86), use
      `milestone_body_line_count` for the live-milestone branch instead of
      `line_count`; leave the archive branch and other caps untouched.
- [ ] T3 — scripts/tests: add a `live()`-with-`## Review` fixture helper and
      cases for AC1 (body<150 + Review over → PASS), AC2 (body≥150 → FAIL),
      AC3 back-compat (no Review → whole file) and AC3 fence-safety (fenced
      `## Review` in body not treated as boundary).
- [ ] T4 — Update the tracking-rules weight-caps line
      (tracking-rules.md:86) to state the `## Review` exemption; add a
      skills/tests prose-guard locking the wording + a stated↔enforced check
      (150 == `MILESTONE_CAP`), modeled on `test_lessons_loop.py`; register the
      guard block in `test_mutation_harness.py`. Note the exemption in the
      milestone template's `## Review` comment.
- [ ] T5 — Sweep `/milestone-review` (+ any skill/template wording) for
      instructions to trim the Review section to fit the cap; reconcile them
      with the exemption. Record the milestone-local D-entry (exemption +
      rejected split/sub-cap alternatives) and promote it to DECISIONS.md. Run
      both suites clean.

## Work log

- 2026-07-13: created by /milestone-plan. Promotes the "Milestone-file cap"
  candidate (RR01 rec 3/Q8). Gate: exempt Review + keep 150 (not split/sub-cap);
  exempt only `## Review` (Decisions stays counted). A D-entry (parallel to
  D-018's CLAUDE.md-section cap) is expected at implement/review.

## Decisions

## Review
