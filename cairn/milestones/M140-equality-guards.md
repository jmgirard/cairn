# M140: Whole-slice equality guards for the M139 rules

- **Status:** planned
- **Priority:** high
- **Depends on:** —
- **Driving RR:** RR12
- **Principles touched:** —
- **Branch/PR:** —

## Goal

The four M139 rule slices get whole-slice equality guards against verbatim
in-test fixtures, closing D-103's recorded exposure.

## Scope

**In:** whole-slice equality guards in `skills/tests/test_thrash_rule.py`
replacing the fragment regexes; the implement-side sub-slice; per-slice
harness re-registration; the probes AC-2–AC-4 and AC-10 name; the
guard-doctrine banking (AC-8).

**Out:**
- Corpus-wide anchor remediation → refused at D-090's unsatisfied trigger
  (RR12 Q5, D-103); other guards fail forward.
- Hash, AST-parse and probe-generator instruments → rejected, RR12
  recs 7–9 / D-103; AC-10's probes are one-time measurements.
- The one-surface-pin row (cross-file fork detection) → parked, own
  promotion condition (RR12 B2).
- Ledgers, per-probe records, certification → D-095/D-090; outcomes are
  Review lines only (AC-6).

## Acceptance criteria

- [ ] AC-1 (BC1): Each of the four M139 rule slices (`review_floor`,
      `review_amendment`, `review_widening`, and the implement-side M139
      sub-slice) is guarded by exactly one test method holding exactly one
      assertion of the form `assertEqual(normalize(<slice>), <fixture>)`, where
      the fixture is a verbatim copy of the slice's entire rule text held in
      `skills/tests/`, and no per-fragment substring or regex assert remains as
      any of those slices' pin — checked by AST walk over `TestWideningTest`'s
      successor at the review commit.
- [ ] AC-2 (BC2): AC4's original probe matrix, re-run at the review commit over
      the domain enumerated by `git diff -w main...HEAD -- skills/milestone-review/SKILL.md
      skills/milestone-implement/SKILL.md` split at sentence boundaries, reds on
      every probe run with zero green (tolerance: zero), each run restored with
      `git diff` shown clean.
- [ ] AC-3 (BC3): An insertion probe placing one fixed sentinel sentence at every
      inter-sentence gap inside each guarded slice reds the suite at every gap,
      zero green (tolerance: zero); the gap count is derived at the review
      commit from the slice text by a stated procedure, not free-standing; each
      run restored with `git diff` shown clean.
- [ ] AC-4 (BC4): A relocation probe moving each M139-added sentence (a) into each
      other rule block of `/milestone-review` step 5, (b) into the other skill
      file, and (c) for the implement-side sentences, to at least two other
      positions inside the Substantive bullet but outside their sub-slice, reds
      on every move, zero green (tolerance: zero), the move counts derived at
      the review commit by a stated procedure; each run restored clean.
- [ ] AC-5 (BC5): Every slice fixture has a mutation-harness registration whose
      blanked block reds that slice's own equality method one-to-one, and
      `python3 -m unittest discover -s skills/tests -k mutation_harness`
      reports `OK` at the review commit.
- [ ] AC-6 (BC6): The child branch's `git diff main...HEAD` adds no committed
      artifact outside `skills/tests/` and the tracking files: no ledger file,
      no hash constant, no per-probe record; probe outcomes appear only as
      Review-section evidence lines (D-095).
- [ ] AC-7 (BC7): All six existing boundary markers, plus any new implement-side
      sub-slice markers, are each asserted unique in their host file, and a
      slice helper returning `""` on a missing marker fails the equality assert
      rather than passing vacuously — demonstrated once at the review commit by
      the marker-blanking entries of BC5's harness run.
- [ ] AC-8. `skills/shared/guard-doctrine.md` §1 states the two-invariant
      statement — totality (the pinned extent equals the slice) and granularity
      (the slice equals one rule), with anchors short of totality leaving a
      free complement — and the "What it cannot see" list in §2 names
      **inserting** beside blanking and swapping, together with the
      normalization blind spot the equality instrument declares (mutations
      expressible purely in collapsed whitespace pass). Evidence: the sentences
      read verbatim from the file at the review commit, plus one
      mutation-harness registration per added claim.
- [ ] AC-9. `skills/tests`, `scripts/tests` and `hooks/tests` pass and
      `python3 scripts/cairn_validate.py` is green at the review commit.
      Evidence: one `## Review` line per command naming the command, the
      commit measured at, and its reported counts.
- [ ] AC-10. Two probes run at one named review commit over the four
      equality-guarded slices and their four fixtures this milestone creates.
      (a) *Intra-slice permutation*: for each guarded slice, apply one at a
      time every adjacent-sentence transposition, the pairs enumerated by the
      stated splitter procedure (pairs per slice = sentences − 1, listed per
      slice; a slice yielding 0 pairs is recorded as 0, never counted as a
      pass). (b) *Stale fixture*: for each fixture, apply one deterministic
      substitution that survives normalization — replace the fixture's first
      alphabetic word with `zzqq` — with its target skill file untouched.
      Every enumerated run reds the suite; no enumerated run greens.
      Additionally, the splitter's per-slice sentence list contains no
      duplicate sentence (a duplicate pair is the one permutation whole-slice
      equality cannot see). All figures are derived at the named commit and
      never free-standing: pair counts by the stated splitter procedure, the
      edit count as the number of equality fixtures in the suite at that
      commit. Each run is reverted and `git diff` shown clean over every
      touched file. Both probes are one-time review-gate measurements, not
      committed generators (D-103's rejected standing generator). Evidence:
      one `## Review` line per probe family (two lines), each naming its
      procedure verbatim, its derived counts, the commit measured at, and the
      red tally.

### Deviations from RR12

| BC | Departure | Reason |
|---|---|---|
| BC2, BC4 | The domain/moves command `git diff -w main...HEAD -- <the two skill files>` is executed as `git diff -w 03ab592^..03ab592 -- <same paths>` (M139's squash commit). BC2's matrix, quoted here for want of a live referent (AC4 survives only as a tombstone): relabel, negation, subject transposition, and relocation run twice (once into a different section of the host file, once into the other of the two files), five probe runs per sentence; a sentence carrying no rule is exempt from the negation form alone and is listed by number. | M139's sentences are on `main` since the merge; on this branch `main...HEAD` no longer enumerates them. The rebased command enumerates exactly the sentences the original matrix swept. |
| BC6 | "adds no committed artifact outside `skills/tests/` and the tracking files" is scoped to instrument and probe-output artifacts — the D-095 class BC6's own enumeration names. The doctrine sentences AC-8 adds to `skills/shared/guard-doctrine.md`, and any boundary-marker need in the two skill files, sit outside that scope per RR12 §5/rec 5, which mandate the banking inside this milestone. All else binds unchanged; no new file lands outside `skills/tests/` and `cairn/`. | As literally worded BC6 forbids the guard-doctrine edit RR12 rec 5 mandates — a drafting collision inside the RR, resolved for its intent. |
| BC1, BC5 | Readings recorded, text unchanged: "verbatim copy" means verbatim modulo the guard's read pipeline (lowercase, whitespace collapse); "`TestWideningTest`'s successor" is `TestWideningTest` in `skills/tests/test_thrash_rule.py`; a slice's "pin" is an assert whose read surface is one of the four slice helpers (whole-file M130 anchors are out of domain); BC5's "one-to-one" is targeting — each registration names the method it proves and blanking reds that method — the bijection reading being unsatisfiable where one marker bounds two slices. | The literal readings are unsatisfiable (a byte-verbatim fixture can never equal the normalized slice; a shared boundary marker reds two equality methods by construction). |

## Coverage

- AC1 → T1, T2
- AC2 → T5
- AC3 → T5
- AC4 → T5
- AC5 → T3
- AC6 → T6
- AC7 → T2, T3
- AC8 → T4
- AC9 → T6
- AC10 → T5

## Tasks

- [ ] T1. `normalize()`; four fixtures copied from the target files' actual
      bytes (M95/M118); four one-assertion equality methods replacing the
      twelve fragment-regex methods; keep every marker-uniqueness assert;
      grep adjacent anchors first (M104).
- [ ] T2. Implement-side sub-slice: existing-prose boundary phrases, helper
      returning `""` on a missing marker, uniqueness asserts; the Substantive
      markers, asserts and entries stay even if superseded (AC-7).
- [ ] T3. Harness: one registration per slice fixture; per-slice
      marker-blanking entries naming that slice's equality method (AC-7); the
      twelve regex-method entries replaced in the same commit (a deleted
      method reds `load_case`).
- [ ] T4. Guard-doctrine banking per AC-8; register each added claim.
- [ ] T5. Probes, each procedure stated verbatim in its Review line: the AC-2
      matrix (forms quoted in the BC2 deviation row) over the deviated
      command; AC-3's non-whitespace sentinel at the splitter's interior gaps;
      AC-4's moves; AC-10's two families. The splitter is a runnable command
      over the normalized slice, unhandled forms enumerated; AC-2's file-side
      runs carry the flagged word-edit axis.
- [ ] T6. Suites + `cairn_validate` (AC-9); branch diff adds nothing outside
      `skills/tests/`, guard-doctrine (BC6 deviation) and `cairn/` (AC-6).

## Work log

- 2026-08-14: created by /milestone-plan from RR12's binding criteria (D-103's split; absorbs the "Child of M139" candidate row, lineage RR12/D-103/M139 R4-01).
- 2026-08-14: criteria audit ran twice ([O], fresh context, authored none of the wording). Round 1 over BC1–7 + AC-8/9: three unstated procedures (splitter, gap and move counts), the BC6×AC-8 joint conflict, strict readings unsatisfiable in BC1/BC5, AC4's matrix lacking a live referent — disposed as two further Deviations rows, task obligations (T3's same-commit repointing, T5's quoted matrix and stated splitter), and the auditor's own rewordings of AC-8/AC-9. Round 2 audited the gate-added AC-10 alone: FIX adopted verbatim (deterministic normalization-surviving fixture edit, zero-pair slices recorded as 0, duplicate-sentence check, one-time-measurement clause); its flagged file-side word-edit axis is carried by AC-2's matrix, noted in T5.
- 2026-08-14: plan gate (maintainer): plaintext in-test fixtures cleared the D-095 door — the retired class is opaque update-blind ledgers, and fixtures are longer members of the harness's existing Mutation-block class; falsified by a fixture updated without its diff read shipping a doctrine change unnoticed, D-103's own residual and supersede target.
- 2026-08-14: plan gate chose in-milestone guard-doctrine banking over a candidate row (RR12 rec 5: the child banks it as ordinary work within itself); falsified by the banking crowding the plan-owned body past its cap.
- 2026-08-14: plan gate added AC-10's two probes over relying on the by-construction argument, because the predecessor's geometry failed twice on undemonstrated axes; falsified by the probes finding nothing across two milestones of fixture edits — then they shrink to one exemplar each.
- 2026-08-14: plan chose an implement-side sub-slice over one fixture spanning the whole Substantive bullet, because the bullet holds six rules other milestones edit (RR12 rec 3); falsified by an M139 sentence relocated within the bullet but outside the sub-slice running green.
- 2026-08-14: instrument choice (equality over hash/AST/generator) not re-weighed — decided at D-103, whose falsifiers and owners stand.
- 2026-08-14: sizing tripwire noted (10 ACs > 7): deliberate, not split — seven are RR12's verbatim binding-criteria floor (indivisible per the brief protocol), one surface, six tasks.

## Decisions

## Review
