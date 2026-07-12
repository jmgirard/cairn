<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M34: Mechanical coverage-map lint in cairn_validate

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m34-coverage-map-lint · https://github.com/jmgirard/cairn/pull/32

## Goal

Add a `cairn_validate` check that fails when a live milestone file has an
acceptance criterion not referenced in its Coverage section, giving M18's
skill-text traceability a runtime enforcement arm.

## Scope

**In:** a new deterministic check in `cairn_validate.py` that, for every
*live* milestone file (those under `cairn/milestones/`, not `archive/`),
parses the `## Acceptance criteria` and `## Coverage` sections and flags
(a) any criterion ACk not referenced in Coverage, and (b) any Coverage
reference to an ACk that exceeds the criterion count (dangling ref). Naming
the file and AC number in each finding. Registered in `CHECKS`, with tests.

**Out:** verifying that Coverage-referenced *tasks* actually exist (task
existence is harder to parse reliably — stays skill-text/review-fenced per
M18/`test_ac_traceability.py`) → remains a candidate if wanted. Archived
(compressed ≤25-line) milestone summaries → exempt, they carry no Coverage
section by design. A `--json` output mode → stays the separate deferred
candidate.

## Acceptance criteria

- [x] `cairn_validate` gains a check (e.g. "coverage complete") that FAILs
      when a live milestone file has an acceptance criterion absent from its
      Coverage section, and the finding names the file and the AC number.
- [x] The same check FAILs on a Coverage line referencing an AC number
      greater than the file's criterion count (dangling reference), naming
      the file and the bad reference.
- [x] The check scans only live milestone files; an archived file with no
      Coverage section (compressed summary) produces no finding.
- [x] A live milestone file whose every criterion is referenced in Coverage
      produces no finding (no false positive), including this repo's own
      live milestone files.
- [x] The script test suite passes: `python3 -m unittest discover -s scripts/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2, T3
- AC5 → T3

## Tasks

- [x] T1 — Add `check_coverage_complete(root)` to `cairn_validate.py`:
      for each live milestone file (reuse `cs.live_files(root)`), read the
      `## Acceptance criteria` section (count `- [ ]`/`- [x]` items → ACn)
      and the `## Coverage` section (collect `AC(\d+)` refs); emit a finding
      per unmapped ACk and per dangling ref (k > n). Register in `CHECKS`.
- [x] T2 — Extend `scripts/tests/test_scripts.py`: fixtures for a milestone
      with an unmapped criterion (fails), one with a dangling Coverage ref
      (fails), a fully-mapped one (passes), and an archived file without
      Coverage (exempt). The base `Tree.build()` fixture needed no change —
      its `live()` bodies carry no criteria (0 ACs → exempt), so they stay
      valid under the new check (M24 lesson: verified, not assumed).
- [x] T3 — Ran `python3 -m unittest discover -s scripts/tests` (no pytest
      here — M32 lesson): 49 pass. This repo's own live files (M34, M35)
      pass the new check.

## Work log

- 2026-07-12: created by /milestone-plan (backlog-polish set 1 of 2;
  runtime arm of M18's deferred mechanical coverage lint —
  `test_ac_traceability.py` guards the skill-text side).
- 2026-07-12: T1–T3 done — `check_coverage_complete` added + registered in
  `CHECKS`; 4 fixtures added (2 fail, 2 pass); suite 49/49; real repo 11/11.
  All tasks done → status review.

## Decisions
<!-- owner: implement / review · append-only -->

## Review
<!-- owner: review · exclusive -->

**Fresh evidence (2026-07-12, PR #32):**

- AC1 — `test_unmapped_criterion` passes: a live file with AC2 unmapped
  yields FAIL `coverage complete` + exit 1, message `M03: AC2 not referenced
  in Coverage`.
- AC2 — `test_dangling_coverage_reference` passes: Coverage citing AC3 with
  only 2 criteria yields FAIL + `Coverage references AC3 but file has 2
  criteria`.
- AC3 — `test_archived_file_with_criteria_is_exempt` passes: an archive/
  file with criteria and no Coverage produces no finding (PASS).
- AC4 — `test_fully_mapped_coverage_passes` passes; and the live repo's own
  `python3 scripts/cairn_validate.py` shows `PASS coverage complete` /
  `all checks passed` (M34 + M35 both mapped).
- AC5 — `python3 -m unittest discover -s scripts/tests`: 49/49 OK.

**Consistency gate:** `cairn_validate` exit 0 (11/11). Coverage completeness:
AC1–AC5 all map to existing tasks T1–T3. No DESIGN principle changed (impact
report skipped). R gates waived (plugin repo); no README.Rmd / NEWS surface.

**Independent review (two lenses, fresh context):**

- [O] diff-bug (Opus): no findings. Verified `_section_body` H2 delimiting
  (a `### sub-header` does not break the section — `"### ".startswith("## ")`
  is False), AC-item regex counts only checkbox bullets, `\bAC(\d+)\b` has no
  over/under-match (`AC10`→10, not 1), `range(1, n+1)` off-by-one correct,
  archive exempt via non-recursive `live_files` glob. Two hypotheticals
  (range-notation / lowercase Coverage lines) dropped — forbidden by the
  template, not defects.
- [S] blame-history (Sonnet): no findings. No M24 fixture-coupling regression
  (base `live()` = 0 ACs → skipped by construction, not luck), no D-023
  date-scanner interaction (`live_cov` emits no dates), append-to-`CHECKS`
  matches the M22/M24/M30 pattern; nothing depends on `CHECKS` order.

Zero surviving findings → scorer step moot (no findings to score).
