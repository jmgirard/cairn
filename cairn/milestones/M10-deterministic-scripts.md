# M10: Deterministic tracking scripts

- **Status:** planned   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- high | normal | low -->
- **Depends on:** —   <!-- M<xx>, M<yy> or — -->
- **Branch/PR:** —   <!-- m10-deterministic-scripts; PR URL once opened -->

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

- [ ] Scaffold `scripts/` and make `cairn_common` importable from there
      without duplicating it (default: prepend `hooks/` to `sys.path`, leaving
      the enforcement layer untouched); confirm hook tests still green.
- [ ] Implement `scripts/cairn_status.py` (snapshot from ROADMAP + milestone
      headers).
- [ ] Implement `scripts/cairn_next.py` (Depends-on resolution against the
      `done` set → workable/resume/review).
- [ ] Implement `scripts/cairn_validate.py` (all mechanical checks above;
      accurate per-check + summary counts; correct exit codes).
- [ ] Write `scripts/tests/test_scripts.py`: fixture `cairn/` trees exercising
      each script, one case per `validate` failure mode + a clean pass;
      confirm `test_hooks.py` still passes.
- [ ] Wire `/milestone` SKILL.md to shell out to the three scripts for the
      mechanizable Snapshot/Audit/Route parts; keep the LLM-only checks.
- [ ] Add the `scripts/` bullet to DESIGN.md Architecture; ensure each script
      handles being run outside a cairn repo; run `validate` on this repo's
      live tree.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan (promoted from the deterministic
  tracking scripts candidate; language=python3-stdlib reusing cairn_common,
  wiring scoped to /milestone per question gate).

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- Scripts are python3-stdlib reusing `cairn_common`, not bash: matches the
  existing enforcement layer, reuses the tested ROADMAP parser and
  cairn-root finder, and stays cross-platform. Supersedes the candidate
  row's "bash" wording (ccpm's model).

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
