<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M77: Work-log cap exemption — the budget stops counting a section IP4 forbids editing

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m77-worklog-cap-exemption` / https://github.com/jmgirard/cairn/pull/75   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: a fixture milestone whose `## Work log` would push it over cap
      measures under cap, and the heaviest-first breakdown emitted by
      `check_caps` never contains the work-log heading; a fixture with no work
      log counts exactly as before (back-compat), and a fenced `## Work log`
      inside a ``` block is not treated as the section (M45 fence-awareness).
- [x] AC2: `cairn_validate` renders a `WARN` naming each work-log entry that
      spans more than one physical line, renders `OK` when every entry is one
      line, and its exit code is unchanged in both cases.
- [x] AC3: `skills/shared/tracking-rules.md` states the work log is exempt from
      the milestone cap with the D-045/IP4 rationale, its cap-remedy text no
      longer directs the heaviest-section trim at the work log, and the
      milestone template's `## Work log` owner comment states the exemption.
- [x] AC4: every new guard assertion is registered in
      `skills/tests/test_mutation_harness.py` and the harness passes; the
      exemption's label→rule mapping is pinned label-inclusively on one physical
      line of the target (M74/M76), verified by a by-hand swap check.
- [x] AC5: the `generic` profile's verify slot is clean — all three suites
      (`scripts/tests`, `skills/tests`, `hooks/tests`) exit 0 — and
      `cairn_validate.py` exits 0 on this repo.
- [x] AC6: `cairn/DECISIONS.md` carries D-046 annotating D-030, recording the
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

- [x] T1: D-046 — written by `/milestone-plan` at the plan commit; implement
      verifies the committed entry rather than re-authoring it.
- [x] T2: `scripts/cairn_scripts.py` — subtract the `## Work log` section from
      `milestone_body_line_count` (`:232`) and drop it from
      `milestone_section_line_counts` (`:264`); keep both fence-aware and
      back-compatible when the section is absent.
- [x] T3: `scripts/tests/test_scripts.py` — extend the shared `Tree.build()`
      fixture first (M24: a stricter counter reddens every reusing test), then
      add the AC1 fixtures (over-cap-without-exemption, no-work-log, fenced).
- [x] T4: `scripts/cairn_validate.py` — add `check_worklog_format` and register
      it in `ADVISORIES` (`:577`), never `CHECKS`; an entry opens with `- ` and
      a continuation is any following non-blank line that does not.
- [x] T5: fixtures for T4 — wrapped entry warns and names the entry, one-line
      entries render `OK`, exit code neutral in both.
- [x] T6: `skills/shared/tracking-rules.md` weight-caps bullet + cap-remedy
      text, and `skills/shared/templates/milestone.md`'s work-log owner comment.
- [x] T7: guards in `skills/tests/` for the T6 wording + their
      `test_mutation_harness.py` entries (per file, ≥1 exemplar block).
- [x] T8: run all three suites and `cairn_validate` from the repo root; check
      exit codes explicitly, never through a pipe (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; promotes the work-log-vs-cap candidate (M76 review); gate chose exempt-plus-guard, advisory severity, and keeping the milestone-local Decisions section counted.
- 2026-07-18: branch `m77-worklog-cap-exemption` cut from main; status -> in-progress.
- 2026-07-18: T1 ticked as already satisfied — /milestone-plan commits its own D-entries, so D-046 landed in 1a6c808 at plan time and AC6 reads the committed entry.
- 2026-07-18: T2+T3 worked as a pair, tests-first (3 new asserts failed, then passed); the two counters now share one fence-aware `_plan_owned_scan`, replacing duplicated scan logic rather than adding a third copy.
- 2026-07-18: T3 — the shared `Tree.build()` fixture needed no change (M24 risk did not materialize: the exemption loosens the counter, it does not add a required file); the M69 breakdown test DID need updating — it used the work log as its third-ranked section, the exact behavior this milestone removes.
- 2026-07-18: T4 — added `cs.milestone_worklog_lines` rather than a second scanner in validate, so the section the cap exempts and the section the advisory polices are one definition (`WORKLOG_HEADING`); a divergence there would be a silent hole.
- 2026-07-18: T4/T5 — advisory registered in ADVISORIES (never CHECKS); 6 fixtures; scripts suite 102 -> 108, exit 0; `cairn_validate` on this repo reports `OK work-log format`, exit 0.
- 2026-07-18: T6 — hit the M59 reflow trap live: rewriting the weight-caps bullet split `review evidence never scrambles plan-owned content` across two physical lines and broke M55's existing guard; reworded to keep the pinned phrase contiguous rather than re-anchor the guard (M68 discipline).
- 2026-07-18: T6 — template work-log comment now states the exemption in 3 physical lines, inside the `lines[i+1:i+4]` window the owner-tag parser reads (M55).
- 2026-07-18: T7 — 6 new guards + 5 mutation entries (added `TEMPLATE` target); skills 298 -> 304. Set-membership assert pins both members on one physical line per M74/M76.
- 2026-07-18: T7 — by-hand SWAP check (blanking cannot simulate a swap): exchanging `## Review` and `## Work log` in the exempt-set line fails the guard, exit 1; file restored, suite green.
- 2026-07-18: T5 live-fire against real history — M76's plan-commit revision shows 3 wrapped continuation lines the advisory would flag, and its merged revision 1 (a stray non-entry prose line); M76's body measures 100 under the exemption versus the 121 it measured under the old rules. The 58-line peak itself is unreachable (squash-merge erased the branch commits).
- 2026-07-18: review trip 1 — gate FAILED on AC4: six new guard asserts but only five mutation entries; `test_stated_advisory_label_matches_the_emitted_label` was unregistered. Status -> in-progress; draft PR #75 opened.
- 2026-07-18: AC4 fix — registered the sixth entry (block `` `work-log format` ``, unique in the rulebook). Declined the available charitable reading (that computed stated<->enforced couplings are exempt by the `test_stated_cap_matches_enforced_cap` precedent) — the criterion says every new assert, and reinterpreting it at review is what AC fencing forbids. Registry 153 -> 154; skills stays 304, exit 0.
- 2026-07-18: T8 — all eight tasks done; skills 304 / scripts 108 / hooks 72 exit 0, cairn_validate exit 0 with `OK work-log format`; M77's own body measures 102 under the new rules versus 118 under the old, and its breakdown no longer lists the work log; status -> review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->

### Trip 1 (2026-07-18) — FAILED on AC4

AC4 requires every new guard assertion to be mutation-registered. Six new
asserts shipped with five entries; `test_stated_advisory_label_matches_the_emitted_label`
was unregistered. A charitable reading was available — the pre-existing
`test_stated_cap_matches_enforced_cap` is also unregistered, so computed
stated↔enforced couplings look exempt by precedent — and was declined, because
reinterpreting a criterion at review is exactly what AC fencing forbids.
Returned to `in-progress`; fixed by registering the sixth entry (block
`` `work-log format` ``, verified unique in the rulebook); registry 153 → 154.

### Trip 2 (2026-07-18) — evidence per criterion

- **AC1 — PASS.** `TestMilestoneBodyLineCount` + `TestMilestoneSectionLineCounts`
  19 tests OK. Over-cap-with-work-log measures under cap; no-work-log and
  no-Review files count as before; fenced `## Work log` stays content;
  `## Work log notes` stays counted (exact match only). `check_caps`
  breakdown test asserts both `Review` and `Work log` absent, OK.
  Invariant `preamble + sum(sections) == body` re-proven with a work log present.
- **AC2 — PASS.** `TestWorkLogFormatAdvisory` 6 tests OK: wrapped entry emits
  `WARN work-log format` with exit 0 and "all checks passed"; one-line entries
  emit `OK`; blanks/comments are not continuations; finding carries `file:line`;
  archived summaries skipped.
- **AC3 — PASS.** Greps against the shipped surface return the exempt-set
  sentence (1 occurrence), the advisory-warns clause, the
  "both cap-exempt sections are omitted, so the remedy can never aim" remedy
  clause, and the template's "EXEMPT from the 150-line cap (D-046)".
- **AC4 — PASS (after trip 1).** `test_milestone_cap_exemption` 11 tests OK;
  mutation harness OK via `discover` (dotted-name run dies on `import
  mutation_engine` — M54). 10 registered entries for this guard, 6 of them new.
  Swap check by hand: exchanging `## Review` and `## Work log` in the exempt-set
  line fails the guard (exit 1); file restored, suite green.
- **AC5 — PASS.** skills 304 / scripts 108 / hooks 72, all exit 0;
  `cairn_validate.py` exit 0, `OK work-log format`.
- **AC6 — PASS.** `cairn/DECISIONS.md:1100` carries D-046 annotating D-030.

### Consistency gate (2026-07-18)

`cairn_validate` exit 0, all checks passed, 3 advisories OK.
`cairn_impact --changed`: no changed principles — IP4 is worked *under*, not
altered, and `cairn/DESIGN.md` is absent from the branch diff entirely, which
is the strongest form of the IP4-untouched claim.
Toolchain `consistency-gate` slot: `generic` names no checks — clean no-op.
