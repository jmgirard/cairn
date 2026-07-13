# M55: Milestone-file cap exempts the Review section

- **Status:** review
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

- [x] T1 — Add `milestone_body_line_count(path)` to `cairn_scripts.py`
      (mirroring `claude_section_line_count`, cairn_scripts.py:205): count lines
      up to — not including — the first `## Review` heading, tracking ```/~~~
      fence state so a fenced `## Review` in the body is not the boundary (M45);
      whole-file count when no `## Review`; None if unreadable.
- [x] T2 — In `check_caps` (cairn_validate.py:78-86), use
      `milestone_body_line_count` for the live-milestone branch instead of
      `line_count`; leave the archive branch and other caps untouched.
- [x] T3 — scripts/tests: `TestMilestoneBodyLineCount` unit class (exemption,
      back-compat, two fence-safety cases, unreadable→None) + integration cases
      in `TestValidateFailures` for AC1 (body<150 + Review over → PASS) and AC2
      (body≥150 → FAIL, asserts the "plan-owned lines" message).
- [x] T4 — Updated the tracking-rules weight-caps text to state the plan-owned
      body cap + `## Review` exemption; added `test_milestone_cap_exemption.py`
      (exemption wording, plan-body-cap wording, stated↔enforced 150 ==
      `MILESTONE_CAP`); registered both prose blocks in `test_mutation_harness.py`;
      noted the exemption in the template's `## Review` comment.
- [x] T5 — Swept skills: no standing instruction trims the Review section to
      fit the cap (those were LESSONS, append-only history — left intact);
      review step 9's "verify weight caps" stays correct. Recorded D-030 (+
      promoted to DECISIONS.md). Both suites clean.

## Work log

- 2026-07-13: created by /milestone-plan. Promotes the "Milestone-file cap"
  candidate (RR01 rec 3/Q8). Gate: exempt Review + keep 150 (not split/sub-cap);
  exempt only `## Review` (Decisions stays counted). A D-entry (parallel to
  D-018's CLAUDE.md-section cap) is expected at implement/review.
- 2026-07-13 (T1/T2): added fence-aware `milestone_body_line_count` and rewired
  `check_caps` to measure the plan-owned body for live milestones. Existing
  scripts suite (65) green.
- 2026-07-13 (T3): added 7 tests (5 unit + 2 integration); scripts suite 72 green.
- 2026-07-13 (T4): rulebook exemption wording + guard + mutation registration +
  template note; skills suite 153 green. (Template comment kept to 3 lines — the
  owner-tag check reads only 3 lines after an H2.)
- 2026-07-13 (T5): swept skills (no Review-trim instruction to reconcile);
  recorded D-030. All tasks done → status review. scripts 72 + skills 153 green;
  `cairn_validate .` all-pass (weight caps included).

## Decisions

- D-030 (promoted to cairn/DECISIONS.md): cap measures the plan-owned body only,
  `## Review` exempt; rejected split-budget / Review sub-cap / exempting
  `## Decisions`. Parallels D-018.

## Review
