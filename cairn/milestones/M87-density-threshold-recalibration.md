<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M87: Density-threshold recalibration — the weight axis is derived from what records actually cost

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m87-density-threshold-recalibration`   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] AC1 Both `CHAR_CAPS` values equal a derivation recorded in this file:
      (line cap − the file's fixed non-item lines) × measured mean item length,
      plus non-item mass; each new value is ≥ the mass its line cap permits, and
      the arithmetic for both files is shown with the command that produced it.
- [ ] AC2 `tracking-rules.md` states that basis in place of "each its item cap ×
      a target mean line length", and states that consolidating raises the mean
      so the mean is re-measured rather than assumed.
- [ ] AC3 `test_record_density.py::test_stated_thresholds_match_enforced_thresholds`
      passes against the new numbers — its regex still matches the reworded
      sentence, and membership (not just values) is still compared.
- [ ] AC4 `cairn_validate` reports `OK record density` on this repo's files, and
      a fixture one char over each new threshold still WARNs carrying the
      `shed ≥N` token; every over-threshold assertion is paired with a positive
      signal that the check ran (`OK record density` / the emitted line), never
      an `assertNotIn` alone (M84 lesson).
- [ ] AC5 A `DECISIONS.md` entry supersedes M84-D1's basis, recording the
      falsified premise with both files' numbers and the rejected drift test.
- [ ] AC6 The `verify` slot's three suites are green — `discover -s skills/tests`,
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
- [ ] T2 Update `CHAR_CAPS` (`scripts/cairn_scripts.py:60`) to the T1 values and
      rewrite the basis comment (`:48-59`), which currently states the
      `60 x 150` / `50 x 340` target means, to the measured derivation.
- [ ] T3 Update `skills/shared/tracking-rules.md:94-97`: new thresholds and the
      replacement basis sentence. Before editing, `grep` the paragraph against
      the two registered blocks (`test_mutation_harness.py:327,339`) — each must
      stay on one physical line, occur exactly once, with trailing punctuation
      intact (M58/M64); re-run the skills suite after any rewording near them.
- [ ] T4 Update the numeric fixtures in `scripts/tests/test_scripts.py:1500-1519`
      (`threshold <9,000` / `<17,000`, the 9,500 mid-band case that relies on one
      file being over and the other under, and the boundary case asserting a
      file exactly at the threshold WARNs) to the new numbers, preserving both
      directions and AC4's positive-signal pairing.
- [ ] T5 Run `test_record_density.py` and confirm the stated↔enforced coupling
      still binds; if the reworded sentence no longer matches its regex
      (`:86-101`), fix the regex to the new wording — never loosen it to a
      values-only match, which would drop the membership check.
- [ ] T6 Run the three suites from the repo root with explicit exit codes, plus
      `cairn_validate`, and record the `record density` line for both files.
- [ ] T7 Author the D-entry: supersedes M84-D1's basis, records both files'
      falsified numbers and the rejected drift test.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan; thresholds derived from measured practice, prose-only safeguard, both files in scope (gate answers).
- 2026-07-18: T1 measured both files; derivations 20,881 / 21,122 → set 21,000 / 21,500 (M87-D1). Rejected shipping a re-runnable measurement script — the gate chose prose-only, and a new shipped script is machinery.
- 2026-07-18: registering this milestone tripped the advisory live — ROADMAP 9,187 chars at 36 lines against a 60-line item cap (60% of the item budget), remedy "compress entries". Left uncompressed: it is evidence for AC1/AC5, not a defect to absorb.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- M87-D1 (2026-07-18): thresholds derived as `non-item mass + (line cap − fixed
  non-item lines) × measured mean item length`, rounded **up to the next 500** so
  the value is never below the mass its line cap permits (rounding down is how
  M84-D1's number silently became the binding cap). Measured 2026-07-18; items
  are lines matching `- 20` (LESSONS) / `| M` or `- ` (ROADMAP), capacity is the
  line cap less the file's fixed non-item lines:

  | file | chars | lines | items | hdr lines | line cap | capacity | mean | derived | set |
  |---|---|---|---|---|---|---|---|---|---|
  | LESSONS.md | 16,998 | 43 | 29 | 14 | 50 | 36 | 561 | 20,881 | **21,000** |
  | ROADMAP.md | 9,191 | 36 | 17 | 19 | 60 | 41 | 498 | 21,122 | **21,500** |

  Mean, not median (458 for both): the mean is what total mass is built from, and
  a median would under-count the long-tail items that drive the overrun.

## Review
<!-- owner: review · exclusive -->
