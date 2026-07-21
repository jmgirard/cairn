<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M101: Decommissioning — machinery measured not to work is removed or repointed

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m101-decommission-measured-noops   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Remove or repoint the four instruments the record shows not working — the
prior-PR lens's dead input surface, the whole-file `CHAR_CAPS` axis, the
`decision heading quality` advisory, and cancelled M96's remainder — on
measured grounds, never on "the file is too big" (D-057).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Prior-PR lens: primary evidence becomes `milestones/archive/`
`## Review` sections; the GitHub PR-thread read survives as a conditional
probe for repos that review on GitHub (gate-chosen 2026-07-20) —
milestone-review SKILL.md:109-121, tracking-rules.md:581-583,
`test_review_fanout.py`. `CHAR_CAPS` whole-file axis removed
(cairn_scripts.py:83; the loop at cairn_validate.py:140-158;
cairn_budget.py:111-113), with the per-line `NON_ITEM_LINE_CAP` axis given
its own file roster (today it iterates `CHAR_CAPS` — cairn_validate.py:163)
and the item `LINE_CAPS` untouched; rulebook two-axes block and LESSONS.md
header rewritten; a D-entry supersedes D-049's whole-file clause. The
`decision heading quality` advisory retired (cairn_validate.py:1392-1462,
its ADVISORIES entry, `test_decision_heading_quality.py`), the rulebook's
heading-authoring rule kept with its enforcement sentence rewritten; a
D-entry annotates D-054 (mitigation 1 withdrawn; the back-reference step
carries recall). D-057's M96 fold: `/milestone` §2 gains a reporting line
beside the cost line (SKILL.md:71-78) — `tracking-rules.md` current mass +
growth since the M95 stamp (779 lines / 53,751 chars, M95 archive) —
reporting only: no threshold, no verdict, no pass machinery. The milestone
counts its own always-read delta (expected net negative).

**Out:** any further stock-side size governance → closed (D-057); nothing
here targets the rulebook's size. The heading-quality classifier redesign →
superseded by retirement at this plan's gate; its candidate row graduates at
completion (M35). The soft-offset-norm and always-read-audit-frame rows →
stay parked candidates, triggers unchanged. Anti-softening mechanisms →
M100.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The prior-PR lens names archived `## Review` sections as its
      primary evidence and runs the PR-thread read only when a cheap
      existence probe finds real review threads; the always-spawned / no-op
      contract is restated for the new surfaces; tracking-rules' lens line
      matches; `test_review_fanout.py` pins the new recipe and fails on the
      old one.
- [ ] AC2: The whole-file character axis is gone from code, tests, and
      prose — `record density` reports only the per-line axis, whose file
      roster no longer depends on `CHAR_CAPS`; item caps unchanged;
      `cairn_budget` prints item + per-line axes only; a repo-wide grep
      finds 21,000/20,500 stated nowhere outside history (DECISIONS.md,
      archives, git) and the milestone's own artifacts (this file's
      tracking lines and the guard's absence-asserts — guard-doctrine §7).
- [ ] AC3: The `decision heading quality` advisory is retired — check,
      registration, and test file gone; the heading-authoring rule survives
      with its enforcement sentence rewritten; affected guards and harness
      entries re-anchored; no orphaned references remain.
- [ ] AC4: `/milestone` §2 prints the rulebook reporting line — current
      mass and growth since the recorded M95 stamp — reporting only (no
      threshold, no verdict), guard-pinned in the same genre as the
      cost-audit line (`test_cost_audit_line.py`).
- [ ] AC5: Two D-entries land, preview-shown (D-036): one superseding
      D-049's whole-file-threshold clause, recording the measured grounds
      and the weighed counter-evidence (the axis fired correctly on the
      NEXT UP row); one annotating D-054's mitigation 1.
- [ ] AC6: The milestone's always-read delta is recorded in the work log,
      counted by diff (expected net negative).
- [ ] AC7: The active profile's `verify` slot is clean — all three suites
      green from the repo root, exit codes checked individually, never
      behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T6
- AC6 → T7
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Repoint the lens — SKILL.md:109-121 rewrite, tracking-rules.md:
      581-583, `test_review_fanout.py` (keep the lens title string: the
      block-isolation split anchors on it).
- [x] T2: Remove the `CHAR_CAPS` loop and dict; give the per-line axis its
      own roster; update `cairn_budget.py`; re-base `test_scripts.py`,
      `test_cairn_budget.py`, `test_record_density.py`.
- [x] T3: Rewrite the rulebook two-axes block (tracking-rules.md:87-110)
      and the LESSONS.md header line; re-anchor the affected mutation-
      harness entries (anchors from the target files' actual bytes — M95).
- [x] T4: Retire the heading-quality advisory — code, ADVISORIES entry,
      test file; rewrite the rulebook enforcement sentence and
      `test_bounded_decisions_read.py:82-85`; re-anchor its harness entry.
- [x] T5: Add the `/milestone` §2 reporting line + guard beside
      `test_cost_audit_line.py`'s pins; seed the stamp from the M95 archive
      figures.
- [x] T6: Author both D-entries (supersede D-049 in part; annotate D-054);
      preview per D-036.
- [ ] T7: Count the always-read delta by diff; run the three suites from
      the repo root, exit codes individually; record both in the work log.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-20: created by /milestone-plan from the NEXT UP candidate row (part b) + the two absorbed IN SCOPE rows; gate chose: remove the CHAR_CAPS axis, retire (not repair) the heading-quality advisory, drop M96 and fold its reporting line here, keep the PR-thread read as a conditional surface.
- 2026-07-20: T1 done — lens repointed to archived `## Review` sections as primary evidence, PR-thread walk gated behind a `pulls/comments?per_page=1` existence probe, no-op contract restated ("no prior-review evidence"); tracking-rules lens line matched; test_review_fanout pins the new recipe (3 new asserts + 3 harness entries) and fails on the old text.
- 2026-07-20: discovered sub-task — pinned rulebook-classification-ledger.md as `partial` in test_scripts.py's shipped-page state ledger; the page was committed at RR04 ingest (526aba6) without its pin, failing the suite on main before this branch.
- 2026-07-20: AC2 amended at a mini gate (user approved): the grep exemption now names the milestone's own artifacts — its tracking lines and the guard's absence-asserts (guard-doctrine §7's known hits) — beside history; substance of the criterion unchanged.
- 2026-07-20: T6 done — D-058 (supersedes D-049's threshold clause + measure-the-mean rule; records the NEXT UP-row counter-evidence and why removal won) and D-059 (annotates D-054, mitigation 1 withdrawn; retire-over-repair with the interaction argument and re-open trigger) appended, both preview-shown per D-036; validate + suites green.
- 2026-07-20: T5 done — /milestone §2 gains the rulebook-mass reporting line beside the cost line (wc -l -m, baseline seeded 779 lines / 53,751 chars from the M95 archive; no threshold, no verdict, no pass machinery); the cost paragraph's stale "M96's to define" deferral rewritten to D-057's closure; 3 new guard tests + 3 harness entries, 1 test and its entry rewritten.
- 2026-07-20: T4 done — check_decision_heading_quality, its regexes/constant, ADVISORIES entry, and test_decision_heading_quality.py removed; the heading-authoring rule survives with its enforcement sentence rewritten to conduct + back-reference; test_bounded_decisions_read's advisory test replaced with a retirement guard (+ its harness entry — the plan expected one to re-anchor, but the old sentence had never been registered); suites green, advisory absent from validate output.
- 2026-07-20: T2+T3 done in one checkpoint (coupled by the stated↔enforced guards) — CHAR_CAPS dict, whole-file loop, and char_count removed; DENSITY_FILES is the per-line roster; budget prints item + per-line only; TestRecordDensityAdvisory + pad_to deleted, TestNonItemLineAxis re-based; rulebook two-axes block rewritten (per-line is the second axis, retirement sentence added), LESSONS.md header now teaches the item cap only; test_record_density rewritten (thresholds coupling → per-line cap + roster couplings + no-threshold negative), 2 harness entries re-anchored, 1 deleted with its test, 1 added; all three suites green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
