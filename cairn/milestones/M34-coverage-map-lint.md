<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M34: Mechanical coverage-map lint in cairn_validate

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** —

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

- [ ] `cairn_validate` gains a check (e.g. "coverage complete") that FAILs
      when a live milestone file has an acceptance criterion absent from its
      Coverage section, and the finding names the file and the AC number.
- [ ] The same check FAILs on a Coverage line referencing an AC number
      greater than the file's criterion count (dangling reference), naming
      the file and the bad reference.
- [ ] The check scans only live milestone files; an archived file with no
      Coverage section (compressed summary) produces no finding.
- [ ] A live milestone file whose every criterion is referenced in Coverage
      produces no finding (no false positive), including this repo's own
      live milestone files.
- [ ] The script test suite passes: `python3 -m unittest discover -s scripts/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T2, T3
- AC5 → T3

## Tasks

- [ ] T1 — Add `check_coverage_complete(root, rows)` to `cairn_validate.py`:
      for each live milestone file (reuse `cs.live_files(root)`), read the
      `## Acceptance criteria` section (count `- [ ]`/`- [x]` items → ACn)
      and the `## Coverage` section (collect `AC(\d+)` refs); emit a finding
      per unmapped ACk and per dangling ref (k > n). Register in `CHECKS`.
- [ ] T2 — Extend `scripts/tests/test_scripts.py`: fixtures for a milestone
      with an unmapped criterion (fails), one with a dangling Coverage ref
      (fails), a fully-mapped one (passes), and an archived file without
      Coverage (exempt). Extend the shared `Tree.build()` fixture so every
      existing validate test still represents a valid repo under the new
      check (M24 lesson).
- [ ] T3 — Run `python3 -m unittest discover -s scripts/tests` (no pytest
      here — M32 lesson) and confirm this repo's own live files pass.

## Work log

- 2026-07-12: created by /milestone-plan (backlog-polish set 1 of 2;
  runtime arm of M18's deferred mechanical coverage lint —
  `test_ac_traceability.py` guards the skill-text side).

## Decisions
<!-- owner: implement / review · append-only -->

## Review
<!-- owner: review · exclusive -->
