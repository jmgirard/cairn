<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M87: Density-threshold recalibration — the weight axis is derived from what records actually cost

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m87-density-threshold-recalibration` · https://github.com/jmgirard/cairn/pull/86   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Re-derive both `record density` thresholds from the mass the item caps actually
permit at measured item length, so the advisory stops binding before the cap it
was built to backstop.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** replacing M84-D1's `item_cap × target_mean` derivation with one measured
from practice, for both `CHAR_CAPS` files; the new values in
`scripts/cairn_scripts.py:60` and the basis comment above them; the stated
thresholds and basis sentence in `skills/shared/tracking-rules.md:94-97`; the
numeric fixtures in `scripts/tests/test_scripts.py:1500-1519`; a D-entry
superseding M84-D1's basis.

The premise M84-D1 assumed is falsified by this repo's own history. It set
LESSONS at `50 × 340` while the file's measured mean was **581** — 41% higher —
so 29 lessons (81% of the 36 the line cap permits) already consumed the whole
budget. ROADMAP is worse: its `60 × 150` matched the **table-row** mean (154)
while candidate rows run **679**, 4.4× that, and candidates are 10 of 15 items —
9,000 permitted only 16 items, **39%** of the 41 its line cap allows. Item count
has been flat since M41 (36 lessons through M83, 29 since M84) while the mean
climbed 290 → 561: lessons are consolidated, never appended, and consolidation
*raises* the mean by construction, so the prescribed weight remedy moves the
quantity the threshold was derived from.

**GP1 tradeoff** (guiding, so tradeable with justification): raising a cap reads
against "caps keep always-read files small", but a weight threshold set below
what the item cap permits does not keep files small — it fires at normal density,
making the advisory a false positive by construction and taxing each milestone
with compression of unrelated records (M61 records that bulk-editing tracking
files has already damaged content once). The item cap stays the hard
small-keeper; the advisory returns to flagging genuine intra-line bloat.

**Out:**
- Lesson graduation/retirement (retiring a lesson once a guard test mechanises
  its rule) → candidate row; attacks inflow, not the threshold.
- A mechanical mean-drift/coupling test (D-034's move) → rejected at the
  2026-07-18 plan gate in favour of stating the basis in prose; rationale
  recorded in the D-entry, re-openable by superseding it.
- Milestone-file cap drafting overshoot → the existing "Budget-first drafting"
  candidate; that is a wrapped-prose file where line count tracks weight.
- `PROFILE.md` density → surveyed at M84, no problem found; item cap alone.
- Changing either **line** cap, or the WARN-not-FAIL severity → unchanged.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1 Both `CHAR_CAPS` values equal a derivation recorded in this file:
      (line cap − the file's fixed non-item lines) × measured mean item length,
      plus non-item mass; each new value is ≥ the mass its line cap permits, and
      the arithmetic for both files is shown with the command that produced it.
- [x] AC2 `tracking-rules.md` states that basis in place of "each its item cap ×
      a target mean line length", and states that consolidating raises the mean
      so the mean is re-measured rather than assumed.
- [x] AC3 `test_record_density.py::test_stated_thresholds_match_enforced_thresholds`
      passes against the new numbers — its regex still matches the reworded
      sentence, and membership (not just values) is still compared.
- [x] AC4 `cairn_validate` reports `OK record density` on this repo's files, and
      a fixture one char over each new threshold still WARNs carrying the
      `shed ≥N` token; every over-threshold assertion is paired with a positive
      signal that the check ran (`OK record density` / the emitted line), never
      an `assertNotIn` alone (M84 lesson).
- [x] AC5 A `DECISIONS.md` entry supersedes M84-D1's basis, recording the
      falsified premise with both files' numbers and the rejected drift test.
- [x] AC6 The `verify` slot's three suites are green — `discover -s skills/tests`,
      `-s scripts/tests`, `-s hooks/tests`, each run from the repo root with its
      exit code checked and never piped (M56/M65) — and the mutation harness is
      green for the two blocks registered from the edited rulebook paragraph
      (`test_mutation_harness.py:327,339`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it. Review reads to fence evidence. -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T5
- AC4 → T4, T6
- AC5 → T7
- AC6 → T3, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 Measure both files and record the derivation in this file: item count,
      fixed non-item lines, measured mean, capacity at the line cap, derived
      threshold, rounded value. Expect ≈ LESSONS 20,881 → **21,000** and ROADMAP
      21,368 → **21,500**; re-measure at implement rather than trusting these —
      the ROADMAP figure moves when this milestone's own candidate row graduates.
- [x] T2 Update `CHAR_CAPS` (`scripts/cairn_scripts.py:60`) to the T1 values and
      rewrite the basis comment (`:48-59`), which currently states the
      `60 x 150` / `50 x 340` target means, to the measured derivation.
- [x] T3 Update `skills/shared/tracking-rules.md:94-97`: new thresholds and the
      replacement basis sentence. Before editing, `grep` the paragraph against
      the two registered blocks (`test_mutation_harness.py:327,339`) — each must
      stay on one physical line, occur exactly once, with trailing punctuation
      intact (M58/M64); re-run the skills suite after any rewording near them.
- [x] T4 Update the numeric fixtures in `scripts/tests/test_scripts.py:1500-1519`
      (`threshold <9,000` / `<17,000`, the 9,500 mid-band case that relies on one
      file being over and the other under, and the boundary case asserting a
      file exactly at the threshold WARNs) to the new numbers, preserving both
      directions and AC4's positive-signal pairing.
- [x] T5 Run `test_record_density.py` and confirm the stated↔enforced coupling
      still binds; if the reworded sentence no longer matches its regex
      (`:86-101`), fix the regex to the new wording — never loosen it to a
      values-only match, which would drop the membership check.
- [x] T6 Run the three suites from the repo root with explicit exit codes, plus
      `cairn_validate`, and record the `record density` line for both files.
- [x] T7 Author the D-entry: supersedes M84-D1's basis, records both files'
      falsified numbers and the rejected drift test.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan; thresholds derived from measured practice, prose-only safeguard, both files in scope (gate answers).
- 2026-07-18: review — 3 lenses + scorer; F1/90 and F5/80 actioned, F6/75 actioned as an AC1 gate issue, F2/60 recorded, F3/45 rejected, F4/40 reworded. F5 moved the shipped thresholds to 20,500/21,000.
- 2026-07-18: review evidence grew M87-D1 past the 150-line cap; compressed the review-owned Decisions section (never the plan-owned Scope) and cross-referenced D-049 rather than restating it.
- 2026-07-18: D-049 corrected on-branch before merge (capacities/percentages/values). Pre-merge branch content is not yet the published record — not a precedent for editing merged history (IP4).
- 2026-07-18: T7 recorded D-049 (supersedes M84-D1's derivation; records the rejected drift test and the retired prune anchor); all tasks done, status → review.
- 2026-07-18: T2-T6 landed the new thresholds (CHAR_CAPS + rulebook basis + fixtures); all three suites green (174/385/72, exit 0 each) and `cairn_validate` now reports `OK record density`.
- 2026-07-18: T4 retired M84's prune regression anchor at a mini-gate — dbf1068 was a boundary-rule cleanup (graduation breadcrumbs restating archive-owned history), not a density judgment, so M84 calibrated on a misread signal; re-based on the M87-D1 derivation.
- 2026-07-18: T1 measured both files; derivations 20,881 / 21,122 → set 21,000 / 21,500 (M87-D1). Rejected shipping a re-runnable measurement script — the gate chose prose-only, and a new shipped script is machinery.
- 2026-07-18: registering this milestone tripped the advisory live — ROADMAP 9,187 chars at 36 lines against a 60-line item cap (60% of the item budget), remedy "compress entries". Left uncompressed: it is evidence for AC1/AC5, not a defect to absorb.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- M87-D1 (2026-07-18, corrected at review): threshold = `non-item mass +
  capacity × measured mean item length`, rounded **up to the next 500** (never
  down — rounding below capacity is how M84-D1's number became the binding cap).
  Capacity = `(line cap − 1) − fixed non-item lines`; the −1 because `check_caps`
  FAILs at `n >= cap` (`cairn_validate.py:71`), so 49/59 lines are permitted. The
  first pass read the cap inclusively, over-derived by one item each, and moved
  both shipped values down when corrected (F5/80). Reproduce — items match `- 20`
  (LESSONS) / `| M` or `- ` (ROADMAP), item newlines count in non-item mass, mean
  floors (F6/75):

  ```
  python3 -c "import math;t=open('cairn/LESSONS.md').read();L=t.splitlines();i=[l for l in L if l.startswith('- 20')];c=49-(len(L)-len(i));d=len(t)-sum(len(x)+1 for x in i)+c*(sum(len(x) for x in i)//len(i));print(c,d,math.ceil(d/500)*500)"
  ```

  | file | chars | lines | items | hdr | cap | capacity | mean | derived | set |
  |---|---|---|---|---|---|---|---|---|---|
  | LESSONS.md | 16,998 | 43 | 29 | 14 | 50 | 35 | 561 | 20,320 | **20,500** |
  | ROADMAP.md | 9,186 | 36 | 17 | 19 | 60 | 40 | 497 | 20,584 | **21,000** |

  Mean not median (458 both) — mass is built from the mean; ROADMAP's is bimodal, caveat in D-049 (F2/60).

## Review
<!-- owner: review · exclusive -->

**Evidence per criterion** (2026-07-18, all commands run from the repo root,
exit codes checked, never piped):

- **AC1** — the M87-D1 command reproduces live: LESSONS capacity 35, derived
  20,320 → set **20,500**; ROADMAP capacity 40, derived 20,584 → set **21,000**.
  Both enforced values ≥ their derivation. Corrected at review from 21,000/21,500
  after F5 showed the cap is exclusive (`n >= cap`), so capacity is
  `(cap−1) − non-item lines`. Command verified by running it, not by reading it.
- **AC2** — `tracking-rules.md` states "capacity × the measured mean item
  length" (1 occurrence) plus the measure-never-assume mandate; the superseded
  "item cap × a target mean line length" is gone (0 occurrences).
- **AC3** — `test_stated_thresholds_match_enforced_thresholds` passes; the
  reworded sentence still matches its regex and membership is still compared.
  `test_record_density.py` 8 tests OK (was 7 — F1 added a third-encoding guard).
- **AC4** — `cairn_validate` reports `OK record density` on this repo.
  `TestRecordDensityAdvisory` 12 tests OK: both files WARN over threshold with
  the `shed ≥N` token (`shed ≥501`), one mass (20,700) produces opposite
  verdicts per file, boundary WARNs at exactly the threshold and is quiet one
  char under, and the absent-file path asserts `OK record density` positively.
- **AC5** — D-049 recorded (`cairn/DECISIONS.md`), superseding M84-D1's
  derivation and recording the rejected mean-drift test.
- **AC6** — three suites green: scripts 174, skills 386, hooks 72, exit 0 each.
  Mutation harness 9 tests OK via `discover -s skills/tests`; all five blocks
  registered from the edited rulebook paragraph remain unique and unwrapped.
  `cairn_validate` exit 0, all checks passed.

**Consistency gate:** `cairn_validate` exit 0. The `generic` profile's
`consistency-gate` slot names no toolchain checks — clean no-op. `cairn_impact`
skipped: `DESIGN.md` is not in the diff, so no principle text changed (M87
trades against GP1, it does not rewrite it).

**Independent review** — three lenses + scorer. Blame-history: no findings,
verdict "historically sound", and it independently confirmed the prune-anchor
retirement reads `dbf1068` correctly. Prior-PR-comments: no prior-PR evidence
(22 candidate PRs, no review comments on these files). Diff-bug: 6 findings.

Actioned (≥80):
- **F1/90** `cairn/LESSONS.md:10` — the file's own header still taught the
  retired 17,000, a third encoding the coupling test never covered. Fixed, and
  the gap closed: `test_lessons_header_states_its_own_enforced_threshold` now
  pins the header to `CHAR_CAPS`.
- **F5/80** — capacity used the line cap inclusively, but `check_caps` FAILs at
  `n >= cap`. Corrected to `(cap−1) − non-item lines`, which moved both shipped
  thresholds down (21,000/21,500 → 20,500/21,000) and fixed the percentages in
  M87-D1 and D-049.

Sub-threshold (4, logged not silently dropped — actioned on operator judgment
where the substance warranted it, per the M73 lesson that the score gates the
actioned list, not the judgment):
- **F6/75** — half of it was an AC-gating defect: AC1 requires the arithmetic
  "shown with the command that produced it" and no command existed. Criteria are
  never reinterpreted, so this was fixed, not waived; the accounting (item
  newlines in non-item mass, floored mean) is now stated and the command runs.
- **F2/60** — ROADMAP's mean is blended over a bimodal population (rows ~158,
  candidates ~683), the mirror of the error D-049 charges M84 with. Not
  re-engineered (per-population modelling would over-fit), but named in
  `cairn_scripts.py` and D-049 so a re-measurement checks the mix, not just the
  mean. Leaving it unstated in a decision that criticises the same flaw would
  have been a record-integrity defect.
- **F3/45** — rejected as a finding: the retained founding example is accurate
  history about the ITEM axis's blindness, and that state sat one line from
  tripping the item cap. Its substance — the axes divide labour and neither
  backstops the other's saturation — is recorded alongside F2.
- **F4/40** — the anchor's comment overstated what it does. Reworded rather than
  strengthened: an assertion recomputing capacity × measured mean would fire
  whenever the mean drifts, which is precisely the mean-drift test rejected at
  the plan gate.

**Deviations:** the plan anticipated updating numbers; it did not anticipate
retiring M84's semantic regression anchor (gated at implement) or the shipped
values moving at review (F5). Compressing M87-D1 to hold the 150-line cap after
review evidence grew it is recorded in the work log.
