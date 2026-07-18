<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M77: Work-log cap exemption — the budget stops counting a section IP4 forbids editing

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Exempt the work log from the 150-line plan-owned milestone cap and add an
advisory that catches wrapped entries, so the cap can never demand a trim to a
section D-045 classifies as history.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `milestone_body_line_count` stops counting the `## Work log` section and
`milestone_section_line_counts` stops reporting it, so the heaviest-first
diagnostic never names an untrimmable section; a new exit-code-neutral advisory
WARNs on a work-log entry spanning more than one physical line; the rulebook's
weight-caps and cap-remedy text plus the milestone template state the exemption
and its rationale; guards, mutation registration, D-046.

**Out:** the milestone-local `## Decisions` section stays counted → D-030's
rejection stands, re-openable only by superseding it (plan gate 2026-07-18).
A hard-FAIL severity for the wrapped-entry check → declined at the same gate;
once the work log costs no budget the issue is tidiness, so it warns.
The ≤25-line archive cap → unchanged, out of scope. Budget-first per-section
drafting → stays its own candidate row (first drafts landing under cap, not
monotonic growth of an un-editable section).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: a fixture milestone whose `## Work log` would push it over cap
      measures under cap, and the heaviest-first breakdown emitted by
      `check_caps` never contains the work-log heading; a fixture with no work
      log counts exactly as before (back-compat), and a fenced `## Work log`
      inside a ``` block is not treated as the section (M45 fence-awareness).
- [ ] AC2: `cairn_validate` renders a `WARN` naming each work-log entry that
      spans more than one physical line, renders `OK` when every entry is one
      line, and its exit code is unchanged in both cases.
- [ ] AC3: `skills/shared/tracking-rules.md` states the work log is exempt from
      the milestone cap with the D-045/IP4 rationale, its cap-remedy text no
      longer directs the heaviest-section trim at the work log, and the
      milestone template's `## Work log` owner comment states the exemption.
- [ ] AC4: every new guard assertion is registered in
      `skills/tests/test_mutation_harness.py` and the harness passes; the
      exemption's label→rule mapping is pinned label-inclusively on one physical
      line of the target (M74/M76), verified by a by-hand swap check.
- [ ] AC5: the `generic` profile's verify slot is clean — all three suites
      (`scripts/tests`, `skills/tests`, `hooks/tests`) exit 0 — and
      `cairn_validate.py` exits 0 on this repo.
- [ ] AC6: `cairn/DECISIONS.md` carries D-046 annotating D-030, recording the
      exemption, the warn-not-fail severity, and the Decisions-section rejection.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2, T3
- AC2 → T4, T5
- AC3 → T6
- AC4 → T7
- AC5 → T8
- AC6 → T1

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1: D-046 — written by `/milestone-plan` at the plan commit; implement
      verifies the committed entry rather than re-authoring it.
- [ ] T2: `scripts/cairn_scripts.py` — subtract the `## Work log` section from
      `milestone_body_line_count` (`:232`) and drop it from
      `milestone_section_line_counts` (`:264`); keep both fence-aware and
      back-compatible when the section is absent.
- [ ] T3: `scripts/tests/test_scripts.py` — extend the shared `Tree.build()`
      fixture first (M24: a stricter counter reddens every reusing test), then
      add the AC1 fixtures (over-cap-without-exemption, no-work-log, fenced).
- [ ] T4: `scripts/cairn_validate.py` — add `check_worklog_format` and register
      it in `ADVISORIES` (`:577`), never `CHECKS`; an entry opens with `- ` and
      a continuation is any following non-blank line that does not.
- [ ] T5: fixtures for T4 — wrapped entry warns and names the entry, one-line
      entries render `OK`, exit code neutral in both.
- [ ] T6: `skills/shared/tracking-rules.md` weight-caps bullet + cap-remedy
      text, and `skills/shared/templates/milestone.md`'s work-log owner comment.
- [ ] T7: guards in `skills/tests/` for the T6 wording + their
      `test_mutation_harness.py` entries (per file, ≥1 exemplar block).
- [ ] T8: run all three suites and `cairn_validate` from the repo root; check
      exit codes explicitly, never through a pipe (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; promotes the work-log-vs-cap candidate (M76 review); gate chose exempt-plus-guard, advisory severity, and keeping the milestone-local Decisions section counted.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->
