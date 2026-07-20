<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M93: Hygiene-line accretion — the ROADMAP stamp is replaced, not appended

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4, GP1, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m93-hygiene-line-replace · https://github.com/jmgirard/cairn/pull/92   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make `Last hygiene check` a replaced one-line stamp rather than a growing
`Prior:`/`Earlier:` chain, and give the density advisory a per-line axis that
catches the accretion wherever it recurs.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the doctrine (the stamp is current knowledge under D-045, so it is
corrected in place, never appended to); a D-entry narrowing the standing
per-line rejection at `tracking-rules.md:109-111` to item lines; the
instruction at all three write sites plus the `/cairn-init` skeleton; a
`record density` per-line axis over non-item lines; guards; and pruning this
repo's own stamp.

**Out:**
- Editing intraclass's and circumplex's ROADMAP files → their own next
  `/milestone` audit, which the new advisory will flag (user decision,
  this session). This milestone reads them as live-fire evidence only.
- Preserving the existing `Prior:`/`Earlier:` chains anywhere → dropped;
  `git log` and `milestones/archive/` already own that detail (user
  decision, this session).
- A per-line axis over *item* lines (rows, candidate bullets, lessons) →
  stays rejected; D-052 narrows the rejection, it does not remove it.
- Raising or lowering the whole-file `CHAR_CAPS` thresholds → D-049 owns
  those; this milestone adds an axis beside them, it does not retune them.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1 `tracking-rules.md` states that the hygiene stamp records the
      *current* check only — replaced each pass, never appended to — and
      grounds that in D-045's current-knowledge class, so the rule is
      visibly not an IP4 history edit. A guard pins the label to its rule on
      one physical line (M74/M92).
- [x] AC2 The per-line rejection at `tracking-rules.md:109-111` is narrowed
      in place to item lines only, and `D-052` records the narrowing with
      the original rationale quoted. No standing rejection is left
      contradicted-but-unsuperseded.
- [x] AC3 All four authoring surfaces carry the replace instruction:
      `skills/milestone/SKILL.md:104`, `skills/milestone-review/SKILL.md:185`,
      `skills/cairn-init/SKILL.md:109` (skeleton), and the tracking-rules
      rule from AC1. Evidence is a grep naming each file:line, scoped to
      the prose surface and exempting this milestone's own tracking lines
      (M58/M59/M62).
- [x] AC4 `record density` gains a non-item-line axis at
      `NON_ITEM_LINE_CAP = 400` (derived below), reported as a WARN under
      the existing advisory label — never a FAIL, per the severity split at
      `tracking-rules.md:106`. It fires at 400 and is silent at 399, both
      directions proven.
- [x] AC5 The new guard is non-vacuous on both known failure shapes: every
      absence-assert is paired with a positive signal that the path actually
      ran (`OK record density` in stdout), so a crash cannot read as a pass
      (M84's own F2/90 defect); and the advisory is run against the
      `/cairn-init` ROADMAP skeleton *instantiated* from
      `skills/cairn-init/SKILL.md:109`, not a fixture copy, which the
      skeleton passes (M77/M80). Registered in the mutation harness per
      file (M53).
- [x] AC6 Live-fire, read-only, every figure dated (amended 2026-07-19 — see
      the work log; circumplex's stamp changed mid-milestone, so an undated
      number is stale by construction — M91/M78). The new axis WARNs on the
      two over-cap stamps — circumplex 2,568 chars and intraclass 1,870, both
      measured 2026-07-19 — and stays silent on ackwards (101), openac (66),
      hitop (48), and this repo (230) after its own hygiene pass, the rule run
      over the artifact the milestone itself authors (M78). Evidence is
      command output with the counts written from it, never from memory (M28).
- [x] AC7 `verify` clean: all three suites green, each exit code checked
      explicitly from the repo root, no piping (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence -->

- AC1 → T1, T5
- AC2 → T1, T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T1, T2, T3, T4, T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 In `skills/shared/tracking-rules.md`: add the replace rule to the
      hygiene-stamp doctrine and narrow the per-line rejection at lines
      109-111 to item lines. Author the label→rule clause on ONE physical
      line — a wrapped sentence is how these anchors go unpinned (M74).
- [x] T2 Append `D-052` to `cairn/DECISIONS.md`: quote the original
      rejection verbatim, narrow it to item lines, and classify the stamp as
      D-045 current knowledge (which is what makes replacement lawful under
      IP4). Append-only; never edit a prior entry.
- [x] T3 Wire the three write sites + the `/cairn-init` skeleton
      (`skills/milestone/SKILL.md:104`,
      `skills/milestone-review/SKILL.md:185`,
      `skills/cairn-init/SKILL.md:109`). Each currently says only "update",
      which is what reads as "append".
- [x] T4 `scripts/cairn_scripts.py`: add `NON_ITEM_LINE_CAP = 400` beside
      `CHAR_CAPS` with the derivation in a comment. `scripts/cairn_validate.py`:
      extend `check_record_density` with the non-item-line axis. Item lines
      (table rows `|…`, bullets `- `) are exempt by construction, not by
      threshold. Warn at `n >= cap` — read the operator, do not assume the
      cap value is attainable (M87).
- [x] T5 Guards in `scripts/tests` + `skills/tests`: the 400/399 boundary
      both directions, the positive `OK` signal, the instantiated-skeleton
      pairing, and the tracking-rules label→rule anchor. Register the new
      guard file in the mutation harness; verify by inversion — negate the
      rule in place, require red, restore and diff (M74).
- [x] T6 Live-fire the advisory across the six surveyed repos (read-only —
      no commits outside cairn), record the counts from output, then prune
      this repo's own stamp and re-run `verify`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Cap 400 derived from a six-repo non-item-line survey — healthy max 245, then 230/194/141/105/101/100, against defects at 1,870 and 3,152; warns at `>=` so it permits 399, leaving 154 chars (63%) of headroom over the observed healthy max and sitting 4.7×/7.9× under both live defects.
- 2026-07-19: implement gate — two open choices settled by the user. (1) `ROADMAP.md` was in NEITHER the history nor the current-knowledge list at `tracking-rules.md:159-162`, so AC1's D-045 grounding did not yet reach it; D-052 adds it to current knowledge rather than classifying the stamp alone. Found by reading the rule out of its source (M75/M85/M91), not assumed from the plan. (2) The `_Released …_` line (105 chars, +~33/release) gets NO exemption from the new cap — it crosses 400 in ~9 releases and the remedy is the milestone's own thesis.
- 2026-07-19: T4 — `NON_ITEM_LINE_CAP = 400` (`cairn_scripts.py:88`) + `non_item_lines()` classifying by line SHAPE (`|…`, `- …` are items and are never measured, so no length can make a row warn — M84's rejection holds by construction, not by threshold); `check_record_density` gained the second report. `cairn_validate.py`'s docstring still taught M84's blanket rejection — a THIRD encoding of the rule D-052 just narrowed — and was corrected with it (M87 F1/90: count every site).
- 2026-07-19: review — one trip. Gate green (validate 0, 15 PASS / 7 OK; `generic` profile names no toolchain checks). 3 lenses + scorer: blame-history clean, prior-PR a clean no-op (0 comments across every merged PR #1–#91), diff-bug 3 findings, all ≥80, all fixed — F1/85 and F2/92 were vacuous guards each proven by live mutation, F3/88 a self-contradicting ratio inside D-052 that my own amendment claimed to have fixed everywhere. Both test fixes re-verified by inversion: each now reddens on the mutation that previously left it green. 441/209/72 green.
- 2026-07-19: T6 — live-fire, read-only, all figures from command output (M28). WARNs: intraclass `cairn/ROADMAP.md:4` 1,870 chars (shed ≥1,471), circumplex `:4` 2,568 (shed ≥2,169). Silent: ackwards, openac, hitop, cairn. Exit-code neutrality proven in the FIELD, not just in fixtures — intraclass carries the WARN and still exits 0; circumplex (1) and openac (1) exit non-zero only on pre-existing unrelated FAILs (`references index<->disk`, `roadmap<->disk orphans`, `scaffold present`), never on `record density`. This repo needed no prune: its stamp is 230 chars and its worst non-item line is the same 230, against cap <400. Writing the stamp is review-owned (`/milestone-review` step 9), so implement left it for the post-merge hygiene pass, which will be the rule's first live exercise. 441/209/72 green, validate 0.
- 2026-07-19: T5 — `TestNonItemLineAxis` (13 tests, `scripts/tests/test_scripts.py`) + `skills/tests/test_hygiene_stamp.py` (9 tests, newly mutation-registered with 5 exemplar blocks across 3 target files). Suites 432→441 and 196→209. VERIFIED BY INVERSION (M74), not just green: deleting the item-line shape exclusion reddened exactly the 3 tests that assert item lines are never measured, and flipping the boundary `<` → `<=` reddened only `test_at_cap_warns`; both restored and diffed clean. The fixture helper's own length assertion caught an off-by-one in the stamp padding before any test asserted on it. Also corrected `test_record_density.py`'s docstring, which still taught the un-narrowed rejection (M91 — a docstring is a restatement site too).
- 2026-07-19: AMENDMENT (substantive, gated) — AC6's `circumplex 3,152 chars` went stale MID-MILESTONE. circumplex's `review M42: done` pass (`d396e94a`, 2026-07-19 19:27) rewrote that stamp to 2,568 chars — still 6.4× over cap — because the instruction it followed said "update", so it compressed the chain rather than replacing it. The defect demonstrated itself in the field, unprompted, while this milestone was being built. AC6 now cites dated figures and the four clean repos; the stale 3,152 was corrected at all four restatement sites (`DECISIONS.md:1365`, `cairn_validate.py:126`, `cairn_scripts.py:93,98`, `tracking-rules.md:115`), each keeping the peak AND the post-pass value since both are load-bearing. D-052 was dated in place rather than superseded: it is committed on this branch but unmerged, so it is a draft under review, not published history — flagged here for review to overrule if it disagrees.
- 2026-07-19: T3 — all four surfaces now say REPLACE, not "update": `skills/milestone/SKILL.md:104`, `skills/milestone-review/SKILL.md:185`, `skills/cairn-init/SKILL.md:109` (skeleton), `skills/shared/tracking-rules.md:153`. AC3 evidence is `grep -rn "Last hygiene check" skills/ | grep -v "/tests/"` — four hits, all prose surfaces, no milestone tracking lines in the result. 432/196/72 green, validate 0.
- 2026-07-19: T2 — `D-052` appended (`cairn/DECISIONS.md:1358`), previewed verbatim before commit. It narrows M84 rather than overturning it (the original rationale is quoted and kept, scoped to item lines), annotates D-045 by naming the file it omitted, and records the rejected `_Released …_` exemption. validate 0, 432/196/72 green.
- 2026-07-19: T1 — tracking-rules gained the replace rule, the current-knowledge enumeration gained `ROADMAP.md`, and M84's blanket per-line rejection is narrowed to item lines in place. The mutation harness reddened two registered anchors I had disturbed (`test_current_knowledge_set_is_enumerated_under_its_own_label`, `test_rule_records_why_a_per_line_warn_was_rejected`); M84's original rationale was restored VERBATIM on one physical line so its assert passes unchanged, while the enumeration assert + its `Mutation(...)` block were re-authored deliberately because that rule genuinely changed. 432/196/72 green, exit codes checked unpiped (M56).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55) -->

**Reviewed 2026-07-19 · PR #92 · one trip.**

### Evidence per criterion

- **AC1** — `tracking-rules.md:154` carries the stamp rule with label and rule
  on one physical line; `:155-156` grounds it in D-045 ("current knowledge
  (D-045), not history"). Guard: `test_hygiene_stamp.TestHygieneStampRule`
  (4 tests), mutation-registered.
- **AC2** — `tracking-rules.md:110` states the narrowing; `:111` keeps M84's
  original rationale verbatim on one line, so its pre-existing assert passes
  unchanged. `D-052` at `DECISIONS.md:1358` quotes the rejection and narrows
  it. No rejection left contradicted-but-unsuperseded.
- **AC3** — `grep -rn "Last hygiene check" skills/ | grep -v "/tests/"` returns
  exactly four hits: `cairn-init/SKILL.md:109`, `milestone/SKILL.md:104`,
  `shared/tracking-rules.md:154`, `milestone-review/SKILL.md:185`. All prose
  surfaces; no milestone tracking lines in the result (M58/M59/M62).
- **AC4** — `TestNonItemLineAxis` 13/13. Boundary both directions
  (`test_at_cap_warns` at 400, `test_one_char_under_cap_is_quiet` at 399).
  Severity: registered in `cairn_validate.ADVISORIES:1463`, which increments
  `warnings` only; `test_advisory_never_moves_the_exit_code` confirms exit 0.
- **AC5** — after two review fixes (F1, F2 below). Mutation registry carries 5
  exemplar blocks for `test_hygiene_stamp` across 3 target files; harness 9/9.
  `test_cairn_init_skeleton_passes_its_own_advisory` instantiates the real
  `skills/cairn-init/SKILL.md` block and now asserts a positive measurement
  signal before its absence-assert.
- **AC6** — live-fire re-run fresh at review: WARN `intraclass ROADMAP.md:4`
  1,870 chars (shed ≥1,471) and `circumplex ROADMAP.md:4` 2,568 (shed ≥2,169);
  silent on ackwards, openac, hitop, cairn (230). Exit-code neutrality holds in
  the field — intraclass carries the WARN at exit 0. (circumplex exited 1 during
  implement on an unrelated `references index<->disk` FAIL that has since
  cleared; `record density` never moved an exit code in any repo.)
  Note on units, since F3 was a units-drift finding: AC6's parentheticals are
  **stamp** lengths (line 4), while `D-052`'s survey list is the corpus-wide
  **maximum** non-item line per file — so ackwards reads 101 as a stamp and 141
  as a maximum, and both are correct. cairn is 230 on both.
- **AC7** — 441/209/72, each exit code checked unpiped from the repo root;
  `cairn_validate` exit 0 (15 PASS, 7 OK).

### Consistency gate

`cairn_validate` exit 0, all 15 CHECKs PASS and all 7 advisories OK. Profile is
`generic`, whose `consistency-gate` slot names no toolchain checks — clean
no-op. No `DESIGN.md` principle changed, so `cairn_impact` was skipped.

### Independent review — 3 lenses + scorer

blame-history [S]: clean, no findings. prior-PR-comments [S]: **no prior-PR
evidence** — every merged PR sampled across #1–#91 returned zero comments and
zero reviews, further quantifying the standing candidate row about that lens
being a structural no-op here. diff-bug [O]: 3 findings, each proven by live
mutation rather than argued. All 3 scored ≥80 and were fixed.

- **F1 (85) — `test_blank_lines_are_not_findings` is vacuous; it cannot fail.**
  Deleting the `if not stripped: continue` skip from `non_item_lines()` left it
  green, because a blank line is 0 chars and `check_record_density` filters
  under-cap lines before printing regardless. Reproduced independently.
  **Fixed:** retargeted at `non_item_lines()` directly and renamed
  `test_blank_lines_are_dropped_by_the_classifier`; it now reddens on that
  mutation.
- **F2 (92) — the instantiated-skeleton test greened on the exact crash shape
  AC5 claims to have eliminated.** `non_item_lines()` swallows every exception
  and returns `[]`, so its lone `assertEqual(over, [])` passed whether or not
  anything was measured. Forcing the `except` path failed 6 of 13 tests in the
  class and left this one green — M84's own F2/90 defect, reproduced in the
  milestone that fixes it, in the only test reading the real shipped artifact.
  **Fixed:** positive signal first (`assertTrue(measured)` plus an assert that
  the stamp line is among the measured lines); it now reddens on that mutation.
- **F3 (88) — `D-052` stated the same defect at two different multiples.** The
  Decision paragraph said "4.7× and 7.9× below the two live defects" (7.9× being
  the stale 3,152 peak) while the same entry and `cairn_scripts.py` said 6.4×
  (the corrected 2,568). The mid-milestone amendment claimed all four
  restatement sites were fixed and missed this one — the exact drift this
  milestone exists to stop. **Fixed:** ratios now stated against the current
  measurement, the peak explicitly labelled as history. Re-measuring to correct
  it also caught two survey miscounts: "seven cairn repos" (there are six) and a
  healthy-values list omitting hitop's 119 and ackwards' 102. Corrected in
  `D-052` and `cairn_scripts.py` from a fresh corpus-wide measurement.

No findings scored below 80.
