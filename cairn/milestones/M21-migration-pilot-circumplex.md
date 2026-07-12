<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M21: Migration stress-test pilot — circumplex (Lineage B)

- **Status:** review
- **Priority:** normal
- **Depends on:** M23
- **Branch/PR:** m21-migration-pilot-circumplex · circumplex PR https://github.com/jmgirard/circumplex/pull/31

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

- [ ] `/cairn-init` §2 executed on circumplex on a `cairn-init-migration`
      branch; PR opened; PR description carries a complete **migration ledger**
      (§2 step 7b). Evidence: PR URL + ledger text.
- [ ] The many-`active` disposition is resolved per the no-invention rule:
      **at most one** item becomes `in-progress`; the rest map to
      `planned`/`candidate` with the mapping recorded in the ledger (§2 steps
      3, 5). Evidence: ledger + ROADMAP on the branch.
- [ ] The `/milestone` health audit runs **clean** on the circumplex migration
      branch, and the repo-local `statistical-validation` skill is relocated
      out of `.claude/skills/` to `cairn/legacy/` (§2 steps 6, 7a). Evidence:
      audit output + file listing in the pilot notes.
- [ ] The circumplex section of `cairn/references/migration-pilot-notes.md` is
      committed here with ledger summary, per-§2-step friction log, and tagged
      gap list. Evidence: file section (+ INDEX row already present from M20).
- [ ] Every `fix-here` gap is resolved this milestone (skill/rulebook edit) with
      new mechanical invariants guard-tested; every `candidate` gap has a
      ROADMAP row. Evidence: diffs + passing tests + ROADMAP rows.
- [ ] Guard-test suite green over `skills/tests/` and `scripts/tests/`.
      Evidence: test run output.

## Coverage

- AC1 → T1, T2, T3, T4, T5
- AC2 → T2, T4
- AC3 → T5, T6
- AC4 → T7
- AC5 → T8
- AC6 → T9

## Tasks

- [x] **T1** — Preconditions + branch (§2 steps 1–2): confirm circumplex clean
      tree; cut `cairn-init-migration` from up-to-date circumplex main.
- [x] **T2** — Inventory + disposition (§2 step 3), with explicit focus on the
      6 `active` items: propose which single one (if any) carries over as
      `in-progress` and where the others land; handle `MILESTONES-ARCHIVE.md`.
- [x] **T3** — Entomb history verbatim (§2 step 4): legacy tracking files +
      `MILESTONES-ARCHIVE.md` → circumplex `cairn/legacy/`; ROADMAP header
      points at legacy + git.
- [x] **T4** — Translate live state under the no-invention rule (§2 step 5):
      the carried `in-progress` item + `planned`/`candidate` mappings; IDs
      continue from legacy max; DECISIONS.md fresh with legacy pointer.
- [x] **T5** — Redistribute + deactivate (§2 step 6): CLAUDE.md per ownership
      table; relocate `next-task`, `release-checklist`, `statistical-validation`
      skills to `cairn/legacy/`; scaffold missing §1 pieces + ignore entries.
- [x] **T6** — Open the circumplex PR with ledger; run the `/milestone` health
      audit on the branch; observe CI. Record PR URL, ledger, audit output.
- [x] **T7** — Append the circumplex section to
      `cairn/references/migration-pilot-notes.md`: ledger summary + friction
      log + tagged gap list.
- [x] **T8** — Land `fix-here` gaps in `/cairn-init` / `tracking-rules.md`; add
      guard tests for new invariants; file `candidate` gaps as ROADMAP rows.
- [x] **T9** — Run the guard-test suite green; commit cairn-side tracking +
      code together.

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
