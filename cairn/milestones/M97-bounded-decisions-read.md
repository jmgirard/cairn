<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M97: Bounded DECISIONS read — the sweep scans headings and reads what it hits

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP2, IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m97-bounded-decisions-read`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Stop sweeping all of `cairn/DECISIONS.md` at every plan: scan its `### D-`
headings, read every matched entry whole, and record the resulting IP2 recall
trade as a D-entry rather than slipping it in as an optimization.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A read protocol for session start and the collision / search-first
sweeps — headings first, matched entries read whole before anything is
surfaced; a stated heading-quality rule (a heading names its subject and any
entry it supersedes or annotates) with a guard; a D-entry annotating IP2's
collision-check reading and stating the recall trade openly; the measured
read reduction recorded.

**Out:**
- **Editing, moving, deleting, or renumbering any D-entry.** IP4 is untouched:
  this milestone changes how the file is *read*, never what it holds.
- A generated or external index → rejected. The 52 `### D-` headings are
  already a zero-divergence index (5,378 chars, 5.6% of the file, measured
  2026-07-19); a second record is the divergence vector M56 and D-051 rejected.
- Archival-with-tombstone for superseded entries → candidate row (RR02 rec 6):
  it buys almost nothing once the read is bounded, and needs its own
  IP4-adjacent D-entry.
- Any cap or advisory on `DECISIONS.md` mass — its growth is legitimate.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: A D-entry records the change and its cost — that recall shifts from
      full-text to heading-plus-targeted-read, and a collision whose heading
      fails to name its subject can be missed. It annotates IP2's
      collision-check reading; it does not weaken IP2's rule that prior state
      is surfaced, never silently obeyed or overridden. Shown verbatim in chat
      before its commit (D-036). The trade was gated and accepted by the user
      at the RR02 ingest, 2026-07-19.
- [x] AC2: The skills that sweep — `/milestone-plan` session start and
      collision check, and the search-first candidate rule — state the bounded
      protocol, and state that a **matched entry is read whole** before being
      surfaced. A collision is still quoted verbatim from the full entry,
      never from the heading (IP2's quoting requirement is unchanged).
      **Amended 2026-07-19 (implement gate): a matched entry is also
      back-referenced — its own `D-0NN` id searched across the file — so an
      entry superseding or annotating it surfaces even when that entry's
      heading omits the relationship.** D-012, D-014, and D-019 each hide a
      supersession in their body, and IP4 forbids repairing them, so the read
      protocol closes the gap rather than the headings.
- [x] AC3: The heading-quality rule is stated and guarded: a `### D-` heading
      names its subject, and names any entry it supersedes, annotates, or
      narrows. The guard runs over the **real `DECISIONS.md`**, not a fixture
      copy (M77/M80), and reports which headings fail rather than only a count.
- [x] AC4: The read reduction is measured and recorded — chars scanned under
      the bounded protocol versus the 95,374-char whole-file sweep — from
      command output, never from memory (M28).
- [x] AC5: Guards assert against the classifier rather than a filtered report
      (M93), pair every absence-assert with a positive signal that the path ran
      (M84), and the guard file carries its mutation registration (M53).
- [x] AC6: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T3, T5
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Author the D-entry annotating IP2 — the trade, its bound, and the two
      mitigations (heading-quality rule; the sweep is model-read, not a literal
      grep). Durable-record preview before commit.
- [x] T2: Update the sweeping skills to the bounded protocol, keeping the
      read-matched-entries-whole and quote-from-the-full-entry requirements
      explicit. Pin each label→rule pairing on one physical line (M74/M92).
- [x] T3: State the heading-quality rule and guard it against the real file;
      report failing headings by ID.
- [x] T4: Measure and record the read reduction from command output.
- [x] T5: Register guards in the mutation harness; run all three suites from
      the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan, re-cutting M94 per RR02 rec 3. Absorbs the "Bounded DECISIONS collision sweep" candidate row (graduates at completion, M35). The IP2 trade was put to the user at the RR02 ingest gate and accepted; AC1 records it as a D-entry rather than leaving it implicit.
- 2026-07-19: in-progress; branch `m97-bounded-decisions-read`. Implement gate settled two open choices. (1) The heading-quality check is an ADVISORY (WARN, never FAIL) scoped prospectively from D-054, because exactly three legacy headings hide a supersession — D-012 omits D-010, D-014 omits D-013, D-019 omits D-003 — and IP4 forbids repairing them; an advisory that can never go green trains people to ignore it. Severity follows the D-049/D-052 split: judgments WARN, structural facts FAIL.
- 2026-07-19: AC2 AMENDED at the implement gate (user-selected): a matched entry is also back-referenced by its own id, so a superseding entry surfaces even when its heading omits the relationship. This closes the recall gap the three legacy headings create without touching history — RR03 recommended it as an AC2 refinement (its "supersession-aware read"). Verified false positives, not amended for: D-029, D-032, D-052 already name their relationships in the heading.
- 2026-07-19: T1 done — D-054 authored, annotating IP2. States the recall trade openly (recall shifts from full-text to heading-plus-targeted-read; a collision whose heading fails to name its subject can be missed) and bounds it with three mitigations: prospective heading-quality advisory, back-reference by id, and the fact that the scan is a model read rather than a literal grep. IP2's quote-verbatim-from-the-full-entry requirement is explicitly unchanged; IP4 untouched.
- 2026-07-19: T2 done — the bounded read is stated ONCE in `tracking-rules.md` beside the search-first rule it modifies, and wired at both `/milestone-plan` sweep sites (session start, collision check). Label→rule pairings pinned on one physical line each (M74/M92): read-whole-before-surfacing, back-reference-by-id, quote-from-the-full-entry, and the heading-quality rule. Written per D-053/M95 discipline — state the rule, cite D-054, no restated defense.
- 2026-07-19: T3 done — `decision heading quality` advisory added to `cairn_validate` (WARN tier, scoped from D-054), tests first (10 tests, red before implementation). It runs over the REAL DECISIONS.md (M77/M80) and names both the offending entry and the omitted id rather than a count. Classifier validated by dropping the scope: it finds exactly D-012/D-014/D-019 and none of the three incidental-mention shapes (D-029, D-032, D-052) — that probe is itself a committed test, so the advisory can never go vacuously silent.
- 2026-07-19: T4 done — read reduction measured from command output. Heading scan 5,681 chars (with newlines) of a 100,678-char file = 5.6%; a typical sweep of scan + 2-3 matched entries reads 9,141-10,898 chars, a 89.2-90.9% reduction, confirming RR02's ~90% projection. 54 entries, mean 1,757 chars, median 1,745, max 4,621. Back-referencing adds one id search per match, negligible against an entry read.
- 2026-07-19: AC4's stated baseline was 95,374 chars; the file measured 100,678 at T4 because THIS milestone's D-053 and D-054 grew it (+5,304). Recorded rather than restated to the old figure — the reduction ratio is unchanged (heading mass grows proportionally: 5.6% at both), so the criterion is met on either baseline. Numbers are the measurement, never the plan's estimate (M87/M93).
- 2026-07-19: T5 done — `skills/tests/test_bounded_decisions_read.py` added (13 tests) and FIVE blocks registered in the mutation harness, one per clause rather than one exemplar per file: dropping the back-reference alone leaves a rule that reads correctly and recalls wrongly, so a single exemplar would let three clauses be deleted green (M53's per-file registration is the floor, not the target).
- 2026-07-19: T5 — two anchors were wrapped when first authored and the fix was the WRAP, never the assert (M74/M78): the collision-quoting sentence in `tracking-rules.md` and again in `milestone-plan/SKILL.md` both broke mid-phrase. Caught by the guard failing, which is the mechanics self-reporting as intended.
- 2026-07-19: verify slot clean — skills 460, scripts, hooks all exit 0, run from the repo root with exit codes checked individually and never behind a pipe (M56); `cairn_validate` 15 PASS / 8 OK, exit 0.
- 2026-07-19: all tasks complete, verify clean; status `review`. The candidate row "Bounded DECISIONS collision sweep" graduates at post-merge hygiene, not here (M35).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

**PR:** https://github.com/jmgirard/cairn/pull/94 · reviewed 2026-07-19 · branch level with `main` at review time (7 ahead, 0 behind; no merge-forward needed).

### Evidence per criterion

- **AC1 — met.** D-054 exists; its heading reads "…— annotates IP2's collision-check reading". Its Consequences state the cost in the criterion's own terms: "recall shifts from full-text to heading-plus-targeted-read, so a collision whose heading fails to name its subject *can* be missed where a whole-file read would have caught it." IP2 is preserved, not weakened — "prior state is still surfaced, never silently obeyed or overridden" and "quoted verbatim from the full entry, never from the heading". Shown verbatim in chat before commit `32135a5` (D-036). IP4 verified mechanically: `git diff main..HEAD -- cairn/DECISIONS.md` is +44/−0, zero deletions.
- **AC2 — met.** The rule is stated once in `tracking-rules.md` ("Bounded `DECISIONS.md` read") and wired at both sweep sites in `milestone-plan/SKILL.md` (session start; collision check). `test_bounded_decisions_read.py` — 13 tests, all green — pins read-whole-before-surfacing, back-reference-by-id, quote-from-the-full-entry, heading quality, and the IP2-unchanged clause, each on its own physical line. The back-reference clause is present per the gated AC2 amendment (2026-07-19).
- **AC3 — met.** `decision heading quality` is registered in `cairn_validate.ADVISORIES` (not `CHECKS`). It runs over the real `cairn/DECISIONS.md` (`TestRealFile`), never a fixture copy (M77/M80). Findings name the offending entry AND the omitted id, not a count. Live output: `OK    decision heading quality`. Non-vacuity proven by command — with `HEADING_QUALITY_FROM` dropped to 1 the classifier returns exactly `['D-012', 'D-014', 'D-019']` and none of the three incidental-mention shapes; that probe is a committed test.
- **AC4 — met.** Measured from command output, not memory (M28): heading scan 5,681 chars (with newlines) of a 100,678-char file = 5.6%; scan + 2 matched entries = 9,141 chars (**90.9% reduction**); scan + 3 = 10,898 (89.2%). 54 entries, mean 1,757, median 1,745, max 4,621. Baseline drift from AC4's stated 95,374 is recorded and explained in the work log — this milestone's own D-053/D-054 added 5,304 chars; the ratio is 5.6% on either baseline.
- **AC5 — met.** Tests assert the classifier directly (`TestClassifier` calls `check_decision_heading_quality`), never only the rendered report (M93). Absence-asserts are paired with positive signals (M84): `test_real_decisions_file_is_clean` is paired with `test_real_file_actually_has_in_scope_entries`, which fails if the advisory has nothing in scope to judge; `test_legacy_entries_are_out_of_scope` is paired with `test_heading_omitting_its_supersession_is_reported`. Five mutation registrations (four in `tracking-rules.md`, one in `milestone-plan/SKILL.md`), one per clause rather than one exemplar per file; `TestRegisteredGuardsFailWhenBlanked` green.
- **AC6 — met.** Run from the repo root, exit codes checked individually, never behind a pipe (M56): `skills/tests` Ran 460 exit=0 · `scripts/tests` Ran 246 exit=0 · `hooks/tests` Ran 72 exit=0.

### Consistency gate

`cairn_validate` exit 0 — 15 PASS / 8 OK, including `coverage complete` and `weight caps`. `cairn_impact --changed`: "no changed principles in cairn/DESIGN.md" (GP1's D-053 amendment landed on `main` before this branch was cut, so it is not in this diff). Profile `generic`, `consistency-gate` slot names no toolchain checks — clean no-op. Repo has no CI by declared profile; PR mergeable on local green.
