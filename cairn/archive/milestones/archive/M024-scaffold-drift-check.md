# M24: Scaffold-drift detection in the audit — done 2026-07-12

**Status:** done · approved 2026-07-12 · PR #22

## Outcome

`cairn_validate.py` gained a deterministic `scaffold present` check
(`check_scaffold` + `_ignore_entries`, in `CHECKS`): FAILs and names any missing
§1 piece — a top-level tracking file, `references/INDEX.md`, a required
`.gitignore` entry (`cairn/references/pdf/`, `cairn/.merge-approved`), or
`^cairn$` in `.Rbuildignore` (package repos). Lists live in `cairn_scripts.py`
(single source). Fires in `/milestone` audit and `/milestone-review` gate; a FAIL
routes to `/cairn-init` repair, never hand-patched. Catches the tidymedia-repair
gaps (missing `LESSONS.md` + `.merge-approved` line), spec additions that
post-dated that adoption.

## Key decisions & review

- Empty scaffold dirs NOT checked — git drops empty dirs, absence ≠ drift.
- Version-stamp / content-drift detection deferred → candidate (Direction 2).
- Adding the check forced extending the shared `Tree.build()` fixture to a full
  scaffold, else existing validate tests fail the new check.
- Two-lens review (Opus diff-bug + Sonnet blame-history): 2 findings, both fixed
  comment-only (dead-but-documented `ROADMAP.md` entry; stale test comment).
  Gate: validate exit 0; 43/43 script + 58/58 skills green; R gates waived; no CI.
