# M10: Deterministic tracking scripts

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —   <!-- M<xx>, M<yy> or — -->
- **Branch/PR:** m10-deterministic-scripts · https://github.com/jmgirard/cairn/pull/7

## Goal

Ship `status`/`next`/`validate` scripts over the `cairn/` files so status,
routing, and the mechanical consistency checks are instant, token-free, and
drift-proof instead of re-derived by the LLM every session.

## Scope

**In:** three python3-stdlib scripts under `scripts/`, reusing the tested
`cairn_common` parser/root-finder; python `unittest` fixtures for each;
wiring `/milestone` to invoke them for the mechanizable parts of its
Snapshot/Audit/Route; a DESIGN.md bullet for the new layer.

**Out:**
- Wiring `/milestone-review`'s consistency gate to `validate` → candidate.
- Wiring `/milestone-plan`'s readiness derivation to `next` → candidate.
- `--json` output mode → candidate.
- Mechanizing git-reconciliation, CLAUDE.md-section-intact, staleness and
  candidate-triage-by-date judgments → these stay LLM-owned in `/milestone`
  (semantic, not deterministic); a date-format sweep → candidate.

## Acceptance criteria

- [ ] **status**: on a fixture `cairn/` tree, `cairn_status.py` prints status
      counts, the active (`in-progress`/`blocked`/`review`) milestone(s) with
      title, next `planned` by priority, candidate count, and the last
      hygiene-check date; exits 0. Verified by a unittest fixture.
- [ ] **next**: `cairn_next.py` derives workable `planned` milestones by
      resolving each `Depends on:` against the `done` set, and surfaces
      resume/review when an `in-progress`/`review` milestone exists. Verified
      by a fixture with a mix of resolved/unresolved dependencies.
- [ ] **validate**: `cairn_validate.py` runs the mechanical checks — mirror
      agreement (file header Status vs ROADMAP), at-most-one `in-progress`,
      weight caps (line counts: CLAUDE.md <80, ROADMAP <60, active milestone
      <150, archive ≤25), done-row retention (≤5), status-vocabulary
      membership, dependency-target existence, ROADMAP↔disk orphans, and
      M-number uniqueness across ROADMAP+archive — exiting non-zero on any
      failure with an accurate per-check line and summary count (no false
      "0 warnings" while flagging; fixes the ccpm count bug noted in
      references/ccpm.md), and exiting 0 on a clean tree. One unittest per
      failure mode plus a clean-tree pass.
- [ ] **validate** passes on this repo's own live `cairn/` tree.
- [ ] Parsing and cairn-root logic is shared with the hooks layer, not
      copy-pasted; the existing `hooks/tests/test_hooks.py` still passes.
- [ ] `/milestone` SKILL.md invokes the three scripts for the mechanizable
      parts of Snapshot/Audit/Route, while explicitly retaining the LLM-only
      checks (git reconciliation, CLAUDE.md-section intact, staleness and
      candidate triage). DESIGN.md Architecture documents the `scripts/`
      layer, and each script prints a clear message + exits non-zero when run
      outside a cairn repo.

## Tasks

- [x] Scaffold `scripts/` and make `cairn_common` importable from there
      without duplicating it (default: prepend `hooks/` to `sys.path`, leaving
      the enforcement layer untouched); confirm hook tests still green.
- [x] Implement `scripts/cairn_status.py` (snapshot from ROADMAP + milestone
      headers).
- [x] Implement `scripts/cairn_next.py` (Depends-on resolution against the
      `done` set → workable/resume/review).
- [x] Implement `scripts/cairn_validate.py` (all mechanical checks above;
      accurate per-check + summary counts; correct exit codes).
- [x] Write `scripts/tests/test_scripts.py`: fixture `cairn/` trees exercising
      each script, one case per `validate` failure mode + a clean pass;
      confirm `test_hooks.py` still passes.
- [x] Wire `/milestone` SKILL.md to shell out to the three scripts for the
      mechanizable Snapshot/Audit/Route parts; keep the LLM-only checks.
- [x] Add the `scripts/` bullet to DESIGN.md Architecture; ensure each script
      handles being run outside a cairn repo; run `validate` on this repo's
      live tree.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (promoted from the deterministic
  tracking scripts candidate; language=python3-stdlib reusing cairn_common,
  wiring scoped to /milestone per question gate).
- 2026-07-11: shipped status/next/validate + shared cairn_scripts helper;
  extended cairn_common with parse_roadmap_rows_full (hooks untouched, 18
  hook tests green); 15 script tests pass; validate clean on live tree.
- 2026-07-11: wired /milestone SKILL.md to the three scripts (semantic
  checks kept LLM-owned); DESIGN.md architecture bullet added. All tasks
  done → review.
- 2026-07-11: review — 6/6 criteria pass with fresh evidence; PR #7.
  Independent Opus review found 1 med + 2 low, all fixed with regressions
  (archived-dep resolution, dropped-dep flag, numeric ID sort); 18 script
  tests green.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Scripts are python3-stdlib reusing `cairn_common`, not bash: matches the
  existing enforcement layer, reuses the tested ROADMAP parser and
  cairn-root finder, and stays cross-platform. Supersedes the candidate
  row's "bash" wording (ccpm's model).

## Review

**Evidence (2026-07-11, PR #7):**
- C1 status / C2 next / C3 validate-modes / C5 shared-parser: `scripts/tests`
  15/15 pass; `hooks/tests` 18/18 pass (parser reuse didn't regress hooks).
- C3 exit + counts: injected two-in-progress tree → `FAIL at most one
  in-progress (1)`, exit 1; clean tree → exit 0. Count is accurate (no false
  "0 failed").
- C4 live tree: `cairn_validate.py` → "all checks passed", exit 0.
- C5 no duplication: row-splitter appears only at `cairn_common.py:74`;
  `cairn_scripts` imports `cairn_common`.
- C6 wiring: SKILL.md invokes all three scripts (Snapshot/Audit/Route) and
  retains the LLM-only checks (staleness, git reconciliation, CLAUDE.md
  intact, untriaged inboxes); DESIGN.md Architecture documents `scripts/`;
  scripts exit 2 outside a cairn repo.

**Consistency gate:** R-specific steps waived (plugin, not a package). Both
python `unittest` suites green; no generated docs to regenerate.

**Independent review (Opus, fresh context):** 1 medium + 2 low, all fixed:
- (med) `cairn_next` built its done-set from ROADMAP rows only → a dep on a
  done-but-row-pruned (archived) milestone misfired; now folds in archive
  files (agrees with validate). Regression test added.
- (low) folding the dangling-dep bullet into validate dropped the
  `dropped`-target case → `check_dependencies` now flags it (check renamed
  "dependency resolution"). Regression test added.
- (low) string ID sort breaks past M99 → `sort_by_priority` now sorts on
  numeric ID. Regression test added.
- Also hardened `candidate_count` header match (startswith). Refactored
  archive/live-file lookup into shared `cairn_scripts` helpers (validate +
  next now share one source). Script tests 15 → 18.
