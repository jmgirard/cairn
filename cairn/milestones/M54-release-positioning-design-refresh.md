<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M54: Release positioning + DESIGN refresh

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Principles touched:** IP1
- **Branch/PR:** m54-release-positioning-design-refresh

## Goal

Bring cairn's outward positioning and DESIGN.md into line with the
language-agnostic architecture M45–M48 shipped, so the first files an external
adopter reads no longer say R-only and DESIGN audits clean (RR01 recs 1 + 5).

## Scope

**In:**
- Reframe the two externally-first-read surfaces — `.claude-plugin/plugin.json`
  description and `README.md` ¶1 — from R-exclusive to the profile-based
  framing already stated in DESIGN Purpose & Scope.
- Remove `cairn-init` §0's redundant "not an R package — adapt or abort"
  bullet; genericize `/hotfix` step 5's hardcoded `NEWS.md` (prose only).
- Refresh `cairn/DESIGN.md`: all 5 hooks listed, IP1 "main" → "the default
  branch", Known-issues rewritten to the honest single-author/single-OS list
  including the honor-system limitation.
- Fold in the same-family template drift: `claude-md-section.md` boundary rule
  gains `Lessons → LESSONS`.
- Lock the positioning framing + DESIGN 5-hook fact with a mutation-harness-
  registered guard test.

**Out:**
- LICENSE (MIT), README worked example, human-facing "what cairn does without
  asking" section, external de-risking (env check, migration dry-run mode),
  DRAFT file removal, v1.0 tag → stay in the "Public release prep" candidate
  (RR01 rec 14 / §10).
- `cairn-init` §0 default-branch fallback recipe alignment → RR01 rec 7
  candidate ("Skill/hook single-source-of-truth").
- Adding a changelog declaration to the profile schema → RR01 rec 11 candidate
  ("Changelog profile slot"); this milestone genericizes `/hotfix` wording
  only, no slot.

## Acceptance criteria

- [ ] AC1 — `plugin.json` description and README ¶1 both reframed from
      R-exclusive to the language-agnostic-core + toolchain-profile framing
      (naming r-package / python / generic), consistent with DESIGN Purpose &
      Scope; a whole-repo `git grep` for other R-exclusive positioning mentions
      (M48 lesson) turns up none unaddressed.
- [ ] AC2 — `cairn-init` §0's "No DESCRIPTION file → not an R package" bullet
      is gone and the adjacent "Toolchain profile" bullet still handles the
      DESCRIPTION-absent case (profile-selection behavior unchanged).
- [ ] AC3 — `/hotfix` step 5 no longer hardcodes `NEWS.md`; it names the
      profile's changelog generically, with no profile-schema slot added.
- [ ] AC4 — `cairn/DESIGN.md` hooks bullet lists all 5 hooks (adds
      `commit_guard.py`, `memory_guard.py`) and IP1 reads "the default branch",
      not "main". (RB tripwire: ip-touching — IP1 wording; M25 already decided
      the semantics, so review confirms no new D-entry is owed, only alignment.)
- [ ] AC5 — DESIGN Known-issues no longer says "Unpiloted (M02/M03)"; it states
      the honest list — single-author, single-OS, hooks unverified on Windows,
      and conduct enforced as prose/guard-tests (only spot-verified at runtime).
- [ ] AC6 — `skills/shared/templates/claude-md-section.md` boundary rule
      includes `Lessons → LESSONS`.
- [ ] AC7 — a guard test positively asserts the profile framing (plugin.json +
      README) and DESIGN's 5-hook list, registered in the mutation harness
      (blanking a protected block fails the guard; the completeness meta-test
      passes); the `verify` slot — `python3 -m unittest discover` over the
      script + skill suites — is clean.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T4
- AC6 → T5
- AC7 → T6

## Tasks

- [x] T1 — Reframe outward positioning: `.claude-plugin/plugin.json:4`
      description and `README.md:6` ¶1 to the profile framing (derive wording
      from `DESIGN.md` Purpose & Scope). Then `git grep` the whole repo for
      other R-exclusive positioning strings and fix any found (M48
      "sweep all mentions" lesson).
- [x] T2 — Delete `cairn-init` §0's "No DESCRIPTION file → not an R package"
      bullet (`skills/cairn-init/SKILL.md:24`); confirm the "Toolchain profile"
      bullet below still covers the DESCRIPTION-absent path.
- [ ] T3 — Genericize `/hotfix` step 5 (`skills/hotfix/SKILL.md:39`): replace
      hardcoded `NEWS.md` with a reference to the profile's changelog (no slot;
      keep it honest that R-package uses `NEWS.md`).
- [ ] T4 — Refresh `cairn/DESIGN.md`: hooks bullet → all 5 hooks; IP1 "main" →
      "the default branch" (RB tripwire: ip-touching); rewrite Known-issues to
      the honest env list + the honor-system line.
- [ ] T5 — Add `Lessons → LESSONS` to the boundary rule in
      `skills/shared/templates/claude-md-section.md:23`.
- [ ] T6 — Add the positioning/DESIGN-hooks guard test (positive `assertIn`s,
      each phrase on a single line and outside `**bold**` per M23/M26), add its
      `Mutation` entries to `skills/tests/test_mutation_harness.py` REGISTRY,
      and run `python3 -m unittest discover` green including the completeness
      meta-test.

## Work log

- 2026-07-13: created by /milestone-plan (RR01 recs 1 + 5; carved from the
  "Public release prep" candidate).
- 2026-07-13: IP1 disposition gate → wording alignment, no D-entry (M25 owns
  the semantics).
- 2026-07-13: T1 — plugin.json + README ¶1 reframed to profile framing; M48
  sweep caught `marketplace.json` (2 more R-only strings), both fixed.
- 2026-07-13: T2 — removed cairn-init §0's R-centric bullet; the Toolchain
  profile bullet (confirm-before-write) owns the DESCRIPTION-absent case. No
  guard referenced the removed wording.

## Decisions

## Review
