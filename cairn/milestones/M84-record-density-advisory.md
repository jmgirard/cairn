<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M84: Record-density advisory — the item caps gain a weight axis

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m84-record-density-advisory   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Give `cairn/ROADMAP.md` and `cairn/LESSONS.md` a character-mass advisory
alongside their existing item caps, so prose weight that accumulates inside
single lines stops being invisible to the audit.

## Scope

**In:** A new exit-code-neutral `cairn_validate` advisory measuring total
character mass per item-list file against a per-file threshold; thresholds
derived from a survey of both cairn and intraclass and anchored to a real
incident; the `tracking-rules` weight-caps section rewritten to document two
orthogonal axes (item count and weight) with distinct remedies; and pruning
cairn's own ROADMAP and LESSONS under the resulting thresholds.

**Out:**
- A per-line character warn — rejected at the plan gate: both files are parsed
  one-item-per-line (`cairn_validate` reads ROADMAP rows positionally; D-015
  defines LESSONS as one lesson per line), so pressure on individual line
  length rewards splitting a row across lines and corrodes the format the
  parsers depend on. It would also fire on ~10-12 legitimate candidate rows
  across the two repos today. The measure is therefore total characters per
  file — an orthogonal axis over the same whole file, which distinguishes
  D-030: that rejected splitting *one* budget into two sub-budgets of the same
  kind with a new section boundary, not a second axis.
- Hard-FAIL severity — advisory chosen at the plan gate. D-018 rejected "a soft
  non-failing warn (loses the hard signal on a genuinely bloated cairn
  section)"; distinguished, not superseded — that was the CLAUDE.md section cap,
  where cairn owns the whole content and a hard signal was the point, whereas
  density is a judgment about prose quality, the justification the
  references-staleness advisory already carries. Revisit if it proves ignorable.
- The 150-line milestone-body cap and budget-first drafting → candidate row at
  `cairn/ROADMAP.md` ("Budget-first drafting (cap prevention)"). Investigation
  found it a *distinct* defect: that is a wrapped-prose file where line count
  tracks weight correctly and the problem is drafting overshoot.
- `PROFILE.md` — surveyed, no density problem (max line 80 chars in cairn, 116
  in intraclass); stays on the item cap alone.
- Pruning intraclass's own ROADMAP and LESSONS → the intraclass repo, as its
  own work there once this ships the measure.

## Acceptance criteria

- [x] AC1: `cairn_validate` emits a new advisory reporting total character
      mass for `cairn/ROADMAP.md` and `cairn/LESSONS.md` against a per-file
      threshold, with its emitted label used verbatim in any prose naming it
      (M78).
- [x] AC2: The thresholds are derived from a recorded survey of both repos,
      and regression-anchored: the ROADMAP threshold WARNs on the pre-prune
      state (`git show dbf1068^:cairn/ROADMAP.md`, 9,807 bytes / 9,691 chars)
      and passes on the post-prune state (`dbf1068`, 8,106 / 8,001).
- [x] AC3: cairn's `ROADMAP.md` and `LESSONS.md` both pass the new advisory
      after an in-milestone prune, evidenced by a before/after mass table.
- [x] AC4: The advisory is exit-code neutral — `cairn_validate` exits 0 on a
      repo tripping only it — covered by a test asserting the exit code, not
      just the output.
- [x] AC5: The `tracking-rules` weight-caps section documents both axes and
      their distinct remedies (graduate/prune for count, compress for weight),
      locked by a prose-guard registered in the mutation harness.
- [x] AC6: Verify slot clean — all three unittest suites green
      (`scripts/tests`, `skills/tests`, `hooks/tests`), run from the repo root
      with exit codes checked individually (M56/M65).

## Coverage

- AC1 → T2, T3, T4
- AC2 → T1, T3
- AC3 → T7
- AC4 → T2, T3
- AC5 → T5, T6
- AC6 → T8

## Tasks

- [x] T1: Survey character mass across both repos and the pre-prune ROADMAP
      state; record the table in this file and derive the two thresholds from
      it, stating the headroom rationale.
- [x] T2: Tests first — fixtures in `scripts/tests/` for over-threshold,
      under-threshold, and exit-code neutrality of the new advisory.
- [x] T3: Implement the measure — char thresholds in `scripts/cairn_scripts.py`
      alongside `LINE_CAPS` (`scripts/cairn_scripts.py:44`), and the advisory
      in `scripts/cairn_validate.py` near `check_caps`
      (`scripts/cairn_validate.py:67`), emitting WARN not FAIL.
- [x] T4: Wire the advisory into the validate output ordering and label; confirm
      `/milestone`'s audit surfaces it as a judgment call, not a mechanical fix.
- [x] T5: Rewrite the `tracking-rules` weight-caps section for two axes.
      Author the guarded phrase on one physical line and expect the reflow to
      split already-registered neighbouring phrases (M23/M82).
- [x] T6: Register the new prose-guard in `skills/tests/test_mutation_harness.py`;
      pin the label together with its members on one physical line (M74/M76).
- [x] T7: Prune cairn's `ROADMAP.md` and `LESSONS.md` under threshold —
      compress lessons rather than evict them where possible, since eviction is
      the item-cap remedy, not the weight remedy.
- [x] T8: Full verify — three suites plus `cairn_validate` green; record the
      before/after mass table as AC3 evidence.

## Work log

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: T1 survey done; thresholds 9,000 / 17,000 and the label `record density` settled at the implement question gate (M84-D1).
- 2026-07-18: AC2 amended (gated) — the cited hash `5d0d5b6` does not exist in this repo; the real pre-prune ref is `dbf1068^` at 9,807 chars (plan estimated ~9,600), post-prune `dbf1068` at 8,106.
- 2026-07-18: T2/T3 — `record density` advisory shipped: `CHAR_CAPS` in cairn_scripts, `check_record_density` first in ADVISORIES, 11 fixture tests; fires on cairn's own LESSONS.md (18,607 chars, shed ≥1,608).
- 2026-07-18: AC2 amended again (unit precision) — the survey figures were `wc -c` bytes but the advisory measures characters (~1% apart); both units now stated, no threshold call changes (M84-D1 **Unit.**).

- 2026-07-18: T4 — no `/milestone` edit needed: its audit already treats every `WARN` generically as "a judgment call surfaced for the user, not a mechanical problem to auto-fix", and enumerating advisories there is the M28 stale-count trap the skill explicitly forbids ("never restate or recall its internals"). DESIGN.md's script inventory is likewise generic.
- 2026-07-18: T5/T6 — tracking-rules weight-caps documents both axes and their opposite remedies; new guard `skills/tests/test_record_density.py` (6 asserts) with 5 mutation registrations; the remedies bullet's "over-cap ROADMAP" is now "over-count ROADMAP" since the phrase became ambiguous. 362 skills tests green.

- 2026-07-18: T7 prune — LESSONS.md 18,607 → 16,272 chars (-2,335, 13%) and 49 → 42 lines; compressed, not evicted: 36 lessons folded into 28 by consolidating five explicit continuation pairs (M53+M54, M57+M79+M81, M60+M80, M74+M76, M81+M82) and two topic pairs, with every milestone tag still present (46 → 47). ROADMAP.md needed no prune: 8,386 chars, 614 under threshold. Header now states both caps and both remedies.
- 2026-07-18: T8 verify — three suites green from the repo root, exit codes checked individually (scripts 171, skills 362, hooks 72); `cairn_validate` all checks passed, `OK record density`, exit 0.

- 2026-07-18: all tasks done, verify clean → status `review`. Anchor re-verified live: pre-prune ROADMAP (9,691 chars over 38 lines, 22 UNDER its item cap) WARNs; post-prune (8,001) clean.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

### M84-D1 (2026-07-18): Thresholds 9,000 (ROADMAP) / 17,000 (LESSONS), derived from a two-repo survey

**Survey** (`wc -c`, 2026-07-18): cairn `ROADMAP.md` 8,491 c / 35 L (243 c/L),
`LESSONS.md` 18,729 / 49 (382), `PROFILE.md` 3,094 / 63 (49); intraclass
7,322 / 37 (198), 15,861 / 49 (324), 6,188 / 101 (61). cairn's `LESSONS.md`
held 49 lines — one under the `<50` item cap — across M78–M83 while its mass
grew 16,567 → 18,729 (+13%): the item cap sat saturated and reported nothing,
which is the incident this advisory answers. ROADMAP peaked at 9,807
(`dbf1068^`) and was pruned to 8,106 (`dbf1068`).

**Derivation.** Each threshold is its item cap × a per-file target mean line
length. ROADMAP: 60 × 150 = **9,000**, independently confirmed by the
incident — it sits between post-prune 8,106 (10% headroom) and pre-prune
9,807. LESSONS: a lesson is a paragraph of hard-won detail, not a table row,
so 150 does not transfer and the mean comes from the corpus instead:
50 × 340 = **17,000**, above intraclass's 324 and below cairn's 382. cairn
sheds ~1,750 chars (9%) at T7; intraclass keeps ~1,100 (about three lessons)
of headroom. Both settled at the implement question gate, 2026-07-18.

**Unit.** The survey above is `wc -c` bytes; the advisory measures CHARACTERS
(`cs.char_count`), so a page of em-dashes is not penalised over one of
hyphens. They differ ~1% here and no threshold call changes: cairn 8,386 /
18,607 chars (LESSONS mean 380), intraclass 7,219 / 15,699 (mean 320), anchor
9,691 pre-prune and 8,001 post-prune — still astride 9,000. Corrected
2026-07-18, before the thresholds shipped.

- 2026-07-18: review — 3 lenses (7 findings, all from the diff-bug lens; blame and prior-PR clean) + scorer. F2/90, F4/82, F7/80 actioned and fixed; F5/62, F6/58, F3/50 also fixed (F3/F6 were landmines this diff introduced); F1/78 resolved by recording AC3's table as review evidence. All six criteria verified against fresh evidence.

## Review

Reviewed 2026-07-18. PR: https://github.com/jmgirard/cairn/pull/82

### Acceptance-criteria evidence

- **AC1** — `cairn_validate` emits `OK    record density` in the ADVISORIES
  block; on an over-threshold fixture it emits one finding per file naming
  chars, lines, item cap, threshold and shed. Label used verbatim in prose at
  `tracking-rules.md:94`, and `test_stated_advisory_label_matches_the_emitted_label`
  couples the rulebook string to the ADVISORIES registration.
- **AC2** — survey + derivation recorded as M84-D1. Anchor re-run live against
  both git states: pre-prune `dbf1068^` (9,691 chars) → WARN `shed ≥692`;
  post-prune `dbf1068` (8,001) → clean. Locked by
  `test_anchored_on_the_real_prune` on the character figures.
- **AC3** — both files pass; before/after mass table:

  | File | Before (main) | After | Threshold | Headroom | Lines |
  |---|---|---|---|---|---|
  | `cairn/ROADMAP.md` | 8,382 | 8,381 | < 9,000 | +619 | 35 → 35 |
  | `cairn/LESSONS.md` | 18,607 | 16,272 | < 17,000 | +728 | 49 → 42 |

  ROADMAP needed no prune. LESSONS shed 2,335 chars (13%) by compression:
  36 lessons folded into 28, all 38 unique milestone tags retained
  (verified by the blame lens with `comm`: zero lost, zero new).
- **AC4** — `test_advisory_never_moves_the_exit_code` asserts `returncode == 0`
  plus `all checks passed` on a tree tripping only this advisory; 12 tests in
  `TestRecordDensityAdvisory`, all green.
- **AC5** — `tracking-rules.md:87-105` states both axes, their opposite
  remedies, and (post-review) each axis's label and severity; guarded by
  `skills/tests/test_record_density.py` (7 asserts), 6 blocks registered in the
  mutation harness and proven to fail when blanked.
- **AC6** — three suites run from the repo root, exit codes checked
  individually and unpiped: scripts 171 (exit 0), skills 363 (exit 0), hooks 72
  (exit 0). `cairn_validate` all checks passed, exit 0.

### Consistency gate

`cairn_validate` exit 0 — all 15 checks PASS including `coverage complete` and
`scaffold present`; 6 advisories OK. Profile `generic`: its `consistency-gate`
slot names no toolchain checks, a clean no-op. No `DESIGN.md` principle
changed, so no Sync Impact Report is owed.

### Independent review — three lenses + scorer

[O] diff-bug: 7 findings. [S] blame-history: 0. [S] prior-PR-comments: 0
(no GitHub review comments on the touched files; archive review sections read
instead — this repo records findings there).

Actioned (scored ≥80):

- **F2 (90)** — `test_missing_file_is_not_a_finding` was vacuous: its only
  assertion was an `assertNotIn`, which an empty stdout satisfies, so the test
  could not tell "handled gracefully" from "crashed". Proven live by two
  agents independently (raising inside the `n is None` branch left all 12
  tests green while validate tracebacked). **Fixed** — now asserts the
  positive `OK    record density` plus the expected `FAIL  scaffold present`
  (exit is 1 here for that unrelated reason, so exit 0 would be the wrong
  signal).
- **F4 (82)** — "weight" named both the failing and the non-failing axis: the
  section is `## Weight caps`, the hard CHECK is labelled `weight caps` and
  measures lines, yet the new prose asserted "Weight WARNs and never fails".
  **Fixed** — the false sentence is replaced, and a new sentence maps each
  axis to its label and severity, pinned label-with-severity for both pairs on
  one physical line (M74/M76) and registered.
- **F7 (80)** — the ADVISORIES placement comment claimed the advisory sits
  "directly under the `weight caps` CHECK", but `run()` prints all 15 CHECKS
  before any advisory; the sentence was also garbled. **Fixed.**

Logged, below the 80 threshold — substance read per the M73 lesson, and three
fixed anyway because two were landmines this diff itself introduced:

- **F1 (78)** — AC3's "before/after mass table" existed only as prose.
  **Resolved** by recording the table above as review evidence, which is where
  AC fencing puts acceptance evidence; no criterion text changed.
- **F5 (62)** — the threshold printed as a bare `threshold 9,000` while the
  comparison is `>=`, unlike every neighbouring cap (`cap <60`). **Fixed** —
  emits `threshold <9,000`; rulebook states `< 9,000`; guard regex widened.
- **F6 (58)** — the AC2 anchor test padded to the `wc -c` BYTE figures
  (9,807/8,106) though the advisory measures characters, right after a gated
  AC amendment made to fix exactly that byte/char confusion. **Fixed** — now
  anchors on 9,691/8,001.
- **F3 (50)** — introduced by this diff: `CHAR_CAPS` reuses the key
  `"cairn/LESSONS.md"`, and `test_lessons_loop`'s unanchored regex was correct
  only because `LINE_CAPS` happens to be declared first. **Fixed** — anchored
  to the `LINE_CAPS` block.
- Borderline, not a defect, no action: the LESSONS compression genericized
  M79's F5 example and reduced M47's question to a pointer. The reviewer
  confirmed every dropped token's rule survives, and the `..`-normalization
  gotcha still lives at its enforcement site.

A fix for F4 tripped the M78 exactly-once trap live — adding the severity
sentence gave `` `record density` `` a second occurrence, breaking its
mutation registration; re-anchored on the unique introducing phrase.
