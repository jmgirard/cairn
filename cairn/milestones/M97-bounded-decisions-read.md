<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M97: Bounded DECISIONS read — the sweep scans headings and reads what it hits

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [ ] AC1: A D-entry records the change and its cost — that recall shifts from
      full-text to heading-plus-targeted-read, and a collision whose heading
      fails to name its subject can be missed. It annotates IP2's
      collision-check reading; it does not weaken IP2's rule that prior state
      is surfaced, never silently obeyed or overridden. Shown verbatim in chat
      before its commit (D-036). The trade was gated and accepted by the user
      at the RR02 ingest, 2026-07-19.
- [ ] AC2: The skills that sweep — `/milestone-plan` session start and
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
- [ ] AC3: The heading-quality rule is stated and guarded: a `### D-` heading
      names its subject, and names any entry it supersedes, annotates, or
      narrows. The guard runs over the **real `DECISIONS.md`**, not a fixture
      copy (M77/M80), and reports which headings fail rather than only a count.
- [ ] AC4: The read reduction is measured and recorded — chars scanned under
      the bounded protocol versus the 95,374-char whole-file sweep — from
      command output, never from memory (M28).
- [ ] AC5: Guards assert against the classifier rather than a filtered report
      (M93), pair every absence-assert with a positive signal that the path ran
      (M84), and the guard file carries its mutation registration (M53).
- [ ] AC6: The active profile's `verify` slot is clean — all three suites
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
- [ ] T2: Update the sweeping skills to the bounded protocol, keeping the
      read-matched-entries-whole and quote-from-the-full-entry requirements
      explicit. Pin each label→rule pairing on one physical line (M74/M92).
- [ ] T3: State the heading-quality rule and guard it against the real file;
      report failing headings by ID.
- [ ] T4: Measure and record the read reduction from command output.
- [ ] T5: Register guards in the mutation harness; run all three suites from
      the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan, re-cutting M94 per RR02 rec 3. Absorbs the "Bounded DECISIONS collision sweep" candidate row (graduates at completion, M35). The IP2 trade was put to the user at the RR02 ingest gate and accepted; AC1 records it as a D-entry rather than leaving it implicit.
- 2026-07-19: in-progress; branch `m97-bounded-decisions-read`. Implement gate settled two open choices. (1) The heading-quality check is an ADVISORY (WARN, never FAIL) scoped prospectively from D-054, because exactly three legacy headings hide a supersession — D-012 omits D-010, D-014 omits D-013, D-019 omits D-003 — and IP4 forbids repairing them; an advisory that can never go green trains people to ignore it. Severity follows the D-049/D-052 split: judgments WARN, structural facts FAIL.
- 2026-07-19: AC2 AMENDED at the implement gate (user-selected): a matched entry is also back-referenced by its own id, so a superseding entry surfaces even when its heading omits the relationship. This closes the recall gap the three legacy headings create without touching history — RR03 recommended it as an AC2 refinement (its "supersession-aware read"). Verified false positives, not amended for: D-029, D-032, D-052 already name their relationships in the heading.
- 2026-07-19: T1 done — D-054 authored, annotating IP2. States the recall trade openly (recall shifts from full-text to heading-plus-targeted-read; a collision whose heading fails to name its subject can be missed) and bounds it with three mitigations: prospective heading-quality advisory, back-reference by id, and the fact that the scan is a model read rather than a literal grep. IP2's quote-verbatim-from-the-full-entry requirement is explicitly unchanged; IP4 untouched.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
