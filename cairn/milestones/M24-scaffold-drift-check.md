<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M24: Scaffold-drift detection in the audit

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** `m24-scaffold-drift-check` · https://github.com/jmgirard/cairn/pull/22

## Goal

Make `cairn_validate.py` mechanically detect when a repo's §1 scaffold has
fallen behind the current spec — missing tracking files or ignore-file
entries — and route the user to `/cairn-init` repair, so drift stops being
invisible between manual re-runs.

## Scope

**In:** a new deterministic `check_scaffold` in `cairn_validate.py`,
registered in `CHECKS` so it runs in both `/milestone`'s audit and
`/milestone-review`'s consistency gate; a single machine-readable
required-scaffold list in `cairn_scripts.py`; package-awareness for the
`^cairn$` `.Rbuildignore` entry; skill-text wiring so a scaffold FAIL routes
to `/cairn-init` repair; a guard test.

**Out:**
- Scaffold-spec **version stamp / content drift** (a template body changed
  while the file still exists) → `candidate` row (Direction 2), planned later
  if content drift ever bites.
- **Empty scaffold-dir** presence checks (`milestones/archive/`,
  `reviews/archive/`, `references/pdf/`) — git does not preserve empty dirs,
  so their absence is not drift; excluded by design, not deferred.
- **CLAUDE.md-section** presence/intactness — already LLM-owned in
  `/milestone`'s audit; not duplicated in the script.
- **Auto-backfill** of missing pieces in the audit (rejected at the plan
  gate — `/cairn-init` stays the sole scaffolder).
- Teaching `/cairn-init` repair mode to consume the new list → `candidate`.

## Acceptance criteria

- [x] `check_scaffold` FAILs and names each missing piece when any of these is
      absent: a top-level tracking file (`DESIGN.md`/`ROADMAP.md`/
      `DECISIONS.md`/`LESSONS.md`), `cairn/references/INDEX.md`, the
      `cairn/references/pdf/` or `cairn/.merge-approved` `.gitignore` entry,
      or (package repos only, DESCRIPTION present) the `^cairn$`
      `.Rbuildignore` entry.
- [x] The check PASSes on a fully-scaffolded repo (this repo included) and
      does **not** FAIL when the empty scaffold dirs are absent — proving the
      empty-dir carve-out.
- [x] The check runs from `CHECKS`, so it appears as a PASS/FAIL line in both
      `/milestone`'s audit run and `/milestone-review`'s consistency-gate run
      of `cairn_validate.py`.
- [x] `/milestone`'s audit section (and the `/milestone-review`
      consistency-gate reference) state that a scaffold FAIL is fixed by
      routing to `/cairn-init` repair — never auto-created in the audit.
- [x] The required-scaffold list lives in exactly one place
      (`cairn_scripts.py`) and is consumed by `check_scaffold`; a guard test
      (`scripts/tests/test_scaffold_check.py`) locks the behavior and passes.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T3
- AC4 → T4
- AC5 → T1, T2, T3

## Tasks

- [x] T1: Add a `REQUIRED_SCAFFOLD` spec to `cairn_scripts.py` (beside
      `LINE_CAPS`, ~line 44): required files, required `.gitignore` entries,
      and the package-only `.Rbuildignore` entry; add a package-detection
      helper (DESCRIPTION present) if none exists.
- [x] T2: Write `scripts/tests/test_scaffold_check.py` first (red): fixtures
      that drop each required piece → FAIL naming it; fully-scaffolded → PASS;
      empty scaffold dirs removed but files present → PASS; package vs
      non-package `.Rbuildignore` behavior.
- [x] T3: Implement `check_scaffold(root, rows)` in `cairn_validate.py` and
      register it in `CHECKS` (`scripts/cairn_validate.py:184`); make T2 green.
- [x] T4: Update the `/milestone` SKILL audit section (`skills/milestone/SKILL.md`,
      near the CLAUDE.md-section line ~64) and the `/milestone-review`
      consistency-gate reference: a scaffold FAIL routes to `/cairn-init`
      repair, not auto-fix.
- [x] T5: ROADMAP rows — remove the absorbed "scaffold-drift detection"
      candidate (now M24), add the Direction-2 candidate (spec-version stamp /
      content drift), and add the M24 `planned` row.
- [x] T6: Run `cairn_validate.py` + the script test suite on this repo; confirm
      green; refresh the ROADMAP hygiene date.

## Work log

- 2026-07-12: created by /milestone-plan (promotes the tidymedia-repair
  candidate; Direction 2 deferred as a candidate).
- 2026-07-12: begin — status in-progress, branch m24-scaffold-drift-check.
- 2026-07-12: T1–T3 — REQUIRED_SCAFFOLD lists in cairn_scripts; check_scaffold
  in cairn_validate registered in CHECKS ("scaffold present"); 10 fixture tests
  in test_scaffold_check.py (extended shared Tree to a full scaffold). 43/43
  script tests green; check PASSes on this repo.
- 2026-07-12: T4 — /milestone audit + /milestone-review consistency-gate text
  now list 'scaffold present' and route a scaffold FAIL to /cairn-init repair
  (not hand-fixed). 58/58 skills guard tests green.

- 2026-07-12: T5–T6 — ROADMAP rows already set at plan time (M24 row; absorbed
  candidate removed; Direction-2 candidate added); validate green (exit 0),
  43/43 script + 58/58 skills tests green; hygiene date already 2026-07-12. All
  tasks done → status review.

## Decisions

## Review

**PR:** https://github.com/jmgirard/cairn/pull/22 (no CI configured in this repo — M16 lesson).

Evidence per criterion (fresh, 2026-07-12):

- **AC1** — `test_scaffold_check.py` drops each required piece → `FAIL scaffold
  present` naming it (missing DESIGN/LESSONS/references INDEX, absent
  .gitignore, each missing ignore entry, package-missing `^cairn$`). Live demo
  on a throwaway repo copy with `LESSONS.md` + the `.merge-approved` line
  removed → `FAIL scaffold present (2)` naming both (the exact tidymedia gap),
  exit 1.
- **AC2** — `cairn_validate.py` on this repo → `PASS scaffold present`, all
  checks passed. `test_full_scaffold_passes` asserts `cairn/reviews/` and
  `cairn/references/pdf/` do not exist yet still PASS — the empty-dir carve-out.
- **AC3** — registered at `cairn_validate.py:233` (`"scaffold present"` in
  `CHECKS`); appears as a PASS/FAIL line in the same `cairn_validate` run that
  `/milestone`'s audit and `/milestone-review`'s consistency gate both invoke.
- **AC4** — `skills/milestone/SKILL.md:49,53` and
  `skills/milestone-review/SKILL.md:58` list the check and route a scaffold
  FAIL to `/cairn-init` repair (never hand-created).
- **AC5** — lists live only in `cairn_scripts.py:62,70,76`, consumed by
  `check_scaffold` (`cairn_validate.py:207,211,217`); the 10-test guard file
  passes.

**Consistency gate:** `cairn_validate.py` exit 0 (incl. the new check).
Coverage completeness — AC1→T2,T3 · AC2→T2,T3 · AC3→T3 · AC4→T4 · AC5→T1,T2,T3;
all mapped tasks exist. No `DESIGN.md` principle touched → `cairn_impact`
skipped. R gates (check/document/README/pkgdown/NEWS) waived — plugin repo, not
a package (CLAUDE.md). Full suites: 43/43 script + 58/58 skills green.

**Independent review (two lenses + inline scoring).** [O] diff-bug (Opus) and
[S] blame-history (Sonnet), distinct evidence bases. Two findings, both
confirmed, both actioned (comment-only, no behavior/criteria change):

- **[82] Dead ROADMAP.md branch** (`cairn_scripts.py`) — `resolve_root` raises
  NotCairn (exit 2) on a missing `cairn/ROADMAP.md` before `check_scaffold`
  runs, so that list entry's branch is unreachable via the CLI. **Fixed:** kept
  the entry (the tuple stays the complete §1 file set for the deferred
  cairn-init-repair-consumes-list candidate) with a comment explaining it is
  belt-and-suspenders. AC1 stays valid — ROADMAP.md is in the checked set.
- **[84] Stale test comment** (`test_scripts.py` `test_over_cap_lessons`) — the
  extended `Tree.build()` now always writes `LESSONS.md`, falsifying the
  comment's claim that `test_clean_tree_passes` has none. **Fixed:** comment
  rewritten to state a missing `LESSONS.md` is now caught by `check_scaffold`,
  not weight-caps.

No findings scored below 80 (none dropped). Re-ran after fixes: 43/43 + 58/58
green, `cairn_validate` exit 0.
