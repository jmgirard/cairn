<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M21: Migration stress-test pilot — circumplex (Lineage B)

- **Status:** review
- **Priority:** normal
- **Depends on:** M23
- **Branch/PR:** m21-migration-pilot-circumplex · cairn PR https://github.com/jmgirard/cairn/pull/21 · circumplex PR https://github.com/jmgirard/circumplex/pull/31

## Goal

Extend migration-protocol hardening to a second Lineage B repo (circumplex),
whose many-`active` and validation-skill footprint stresses edges ackwards
does not, folding surfaced gaps back into the skill.

## Scope

**In:**
- Execute `/cairn-init` §2 migration on **circumplex** on a
  `cairn-init-migration` branch → real PR, CI exercised (with the M20-derived
  fixes from **M22/M23** already in the skill, so the second run compounds
  them). circumplex's own
  IDs are qualified "circumplex M<nn>"; this milestone is cairn M21.
- Deliberately exercise circumplex-specific edges: the **6 "active" items vs.
  the at-most-one-`in-progress` rule** (§2 step 3 disposition), the separate
  `MILESTONES-ARCHIVE.md`, and the repo-local **`statistical-validation`**
  skill relocation (validation doctrine).
- Append a **circumplex** section to `cairn/references/migration-pilot-notes.md`
  (ledger summary, per-§2-step friction log, tagged gap list).
- Land small-and-clear `fix-here` gaps in `/cairn-init` / `tracking-rules.md`;
  lock new mechanical invariants with guard tests.

**Out:**
- ackwards migration → **M20** (done first).
- Merging the circumplex PR / actually adopting cairn there → circumplex's own
  review gate, later; not required to close M21.
- Design-heavy protocol redesign a gap implies → ROADMAP `candidate` row.

## Acceptance criteria

- [x] `/cairn-init` §2 executed on circumplex on a `cairn-init-migration`
      branch; PR opened; PR description carries a complete **migration ledger**
      (§2 step 7b). Evidence: PR URL + ledger text.
- [x] The many-`active` disposition is resolved per the no-invention rule:
      **at most one** item becomes `in-progress`; the rest map to
      `planned`/`candidate` with the mapping recorded in the ledger (§2 steps
      3, 5). Evidence: ledger + ROADMAP on the branch.
- [x] The `/milestone` health audit runs **clean** on the circumplex migration
      branch, and the repo-local `statistical-validation` skill is relocated
      out of `.claude/skills/` to `cairn/legacy/` (§2 steps 6, 7a). Evidence:
      audit output + file listing in the pilot notes.
- [x] The circumplex section of `cairn/references/migration-pilot-notes.md` is
      committed here with ledger summary, per-§2-step friction log, and tagged
      gap list. Evidence: file section (+ INDEX row already present from M20).
- [x] Every `fix-here` gap is resolved this milestone (skill/rulebook edit) with
      new mechanical invariants guard-tested; every `candidate` gap has a
      ROADMAP row. Evidence: diffs + passing tests + ROADMAP rows.
- [x] Guard-test suite green over `skills/tests/` and `scripts/tests/`.
      Evidence: test run output.

## Coverage

- AC1 → T1, T2, T3, T4, T5
- AC2 → T2, T4
- AC3 → T5, T6
- AC4 → T7
- AC5 → T8
- AC6 → T9

## Tasks

- [x] **T1** — Preconditions + branch (§2 steps 1–2).
- [x] **T2** — Inventory + disposition of the active items (§2 step 3).
- [x] **T3** — Entomb history verbatim → `cairn/legacy/` (§2 step 4).
- [x] **T4** — Translate live state, no-invention; IDs from legacy max (§2 step 5).
- [x] **T5** — Redistribute CLAUDE + relocate 3 skills + scaffold §1 (§2 step 6).
- [x] **T6** — Open circumplex PR + ledger; health audit; observe CI.
- [x] **T7** — Append the circumplex section to `references/migration-pilot-notes.md`.
- [x] **T8** — Land fix-here gaps + guard tests; file candidate gaps as ROADMAP rows.
- [x] **T9** — Guard suite green; commit cairn-side tracking + code.

## Work log

- 2026-07-11: created by /milestone-plan (second half of the Lineage B
  migration stress-test; depends on M20 so its fixes compound here).
- 2026-07-12: re-pointed Depends on M20 → M23 per the harden-before-pilot
  decision — the M20 pilot landed no fixes; they now ship as M22 (defaults) +
  M23 (§2 guidance), which must precede this pilot.
- 2026-07-12: T1–T6 — ran `/cairn-init` §2 live on circumplex (default branch
  `master`); branch `cairn-init-migration` → PR
  https://github.com/jmgirard/circumplex/pull/31 (docs/tracking only, 100%
  renames, no package code). Entombed MILESTONES/ARCHIVE/ROADMAP + 3 skills;
  kept DESIGN verbatim (Compromise A); authored ROADMAP (M7 blocked, M6+backlog
  candidates), DECISIONS (D-001..D-004), LESSONS, INDEX; redistributed CLAUDE.
  Health audit `cairn_validate` 9/9 clean on the branch; full R-CMD-check matrix
  (7 jobs) exercised.
- 2026-07-12: T7 — appended the circumplex section to
  `references/migration-pilot-notes.md` (ledger + validation table + tagged gaps).
- 2026-07-12: T8 — fix-here G-C1 (§1 scaffold omitted `LESSONS.md`) + G-C3
  (legacy "planned" without criteria → candidate, not `planned`), both
  guard-tested in `test_migration_guidance.py`; candidates G-C2 (date-scan
  false-positive on check notation) + G-C4 (mature backlog vs ROADMAP cap) filed
  as ROADMAP rows.
- 2026-07-12: T9 — guard suite green (58 skill + 33 script); cairn_validate clean.

## Decisions

- 2026-07-12: **Disposition (user gate).** circumplex's at-most-one-`in-progress`
  edge resolved per the no-invention rule: the v2.0.0 release-prep → one
  `blocked` milestone (M7; blocker = CRAN cadence window ~2026-08-02), M4
  entombed as `done` (release narrative + MILESTONES treat M2–M5 complete;
  maintainer confirmed), M6 → `candidate` (scope but no criteria), backlog →
  clustered candidate rows. Zero `in-progress`. Full-run + real PR authorized by
  the user.
- 2026-07-12: **Pilot result.** Running against the M22/M23-hardened protocol,
  circumplex validated 5 of those fixes (default-branch, §0 widening, Compromise
  A, §6 sweep, `.Rbuildignore` prune) and surfaced only small mechanical residue
  (G-C1/G-C3 fix-here; G-C2/G-C4 candidates) — a deliberate contrast with M20's
  all-design-level gaps.

## Review

_2026-07-12, same-session implement→review. cairn PR #21; circumplex PR #31._

**AC evidence (fresh, by command):**
- AC1 (PR + ledger): `gh pr view 31` → OPEN, title "cairn-init: migrate tracking
  to cairn/", body contains the Migration ledger table (every legacy file +
  live item accounted for). PASS.
- AC2 (at-most-one in-progress): circumplex `cairn/ROADMAP.md` on the branch has
  **0** in-progress rows (release-prep → M7 `blocked`; M4 done; M6 + backlog →
  candidates); the mapping is recorded in the PR ledger. `cairn_validate` "at
  most one in-progress" PASS. PASS.
- AC3 (audit clean + skill relocated): `cairn_validate` on the circumplex branch
  → all 9 checks pass; `cairn/legacy/statistical-validation/SKILL.md` exists and
  `.claude/skills/statistical-validation` is gone. PASS.
- AC4 (pilot notes): `references/migration-pilot-notes.md` gains the "Pilot 2 —
  circumplex (M21)" section — ledger summary, M22/M23-validation table, tagged
  gap list (G-C1..G-C4), disposition. PASS.
- AC5 (fix-here resolved + guard-tested; candidates filed): `cairn-init/SKILL.md`
  diff adds LESSONS.md to §1 scaffold (G-C1) and the planned-needs-criteria note
  to §2 step 5 (G-C3); `test_migration_guidance.py` gains 2 locking tests;
  `cairn/ROADMAP.md` gains G-C2 + G-C4 candidate rows. PASS.
- AC6 (suite green): `unittest discover` → skills/tests 58 ok, scripts/tests
  33 ok. PASS.

**Consistency gate:** `cairn_validate.py` (cairn) → 9/9. Coverage complete (all
6 ACs map to existing tasks). No principle touched → impact skipped. R gates
waived (non-package repo).

