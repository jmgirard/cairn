# M59: Skill single-source-of-truth — canonical fallback, de-enumerated checks, migration module

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** GP1, GP2
- **Branch/PR:** m59-skill-single-source-of-truth

## Goal

Skills defer to their single sources of truth instead of restating them:
cairn-init's default-branch fallback matches the rulebook's canonical recipe,
the two stale check enumerations become run-and-read, and the migration
protocol is progressively disclosed out of the common scaffold path
(RR01 recs 7 + 12).

## Scope

**In:**

- `skills/cairn-init/SKILL.md` §0: replace the `git branch --show-current`
  fallback (line ~19) with the canonical recipe (origin/HEAD → `git ls-remote
  --symref origin HEAD` → ask the user; never guess the current branch).
- `skills/milestone-review/SKILL.md` step 4: drop the parenthetical
  enumeration of cairn_validate's checks and the manual "Coverage
  completeness" bullet (mechanical since M34) — run-and-read wording.
- `skills/milestone/SKILL.md` §2: same de-enumeration (run-and-read).
- Move cairn-init §2 (migration protocol, ~150 lines) to
  `skills/shared/migration-protocol.md`, read only when §0 detects a
  precursor footprint; relocation, not rewrite.
- Guard re-anchors ship in the same commit as each relocation (M46 lesson).

**Out:**

- Force-push deny hook + merge_guard PostToolUse companion → M60.
- Changelog profile slot → candidate row (gated on the next profile).
- Migration dry-run mode, env check → release-prep candidate row.

## Acceptance criteria

- [ ] cairn-init §0's default-branch detection states the canonical recipe
      (ls-remote rung, then ask); `git grep -n "show-current" skills/` returns
      nothing.
- [ ] Neither `/milestone-review` step 4 nor `/milestone` §2 enumerates
      cairn_validate's individual checks, and review step 4 carries no manual
      "Coverage completeness" bullet — validate is run-and-read in both.
- [ ] The migration protocol lives in `skills/shared/migration-protocol.md`;
      cairn-init §0 directs reading it only on footprint detection; the moved
      text is verbatim-relocated except heading/pointer edits (diff recorded
      in Review).
- [ ] Repo-wide pointer sweep done: no live file still points at "cairn-init
      §2" as the protocol's home (history files excluded per the M58 lesson —
      exclusion list may name only DECISIONS/CHANGELOG/legacy/reviews-archive).
- [ ] All three unittest suites green from the repo root (skills/tests,
      scripts/tests, hooks/tests), including re-anchored guards
      (test_migration_guidance.py, test_default_branch_parameterized.py,
      test_toolchain_profiles.py, test_ac_traceability.py); mutation-harness
      completeness passes with any new/moved guard blocks registered (M53/M54).

## Coverage

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T1, T2, T4, T6

## Tasks

- [x] T1: Align cairn-init §0's default-branch bullet
      (skills/cairn-init/SKILL.md:17-19) to the canonical recipe; re-anchor
      test_default_branch_parameterized.py in the same commit; sweep
      `git grep -n "show-current"` repo-wide (M48).
- [x] T2: De-enumerate `/milestone-review` step 4
      (skills/milestone-review/SKILL.md:63-70): run-and-read; delete the
      manual Coverage-completeness bullet; re-anchor
      test_toolchain_profiles.py:356 and test_ac_traceability.py:86.
- [x] T3: De-enumerate `/milestone` §2 (skills/milestone/SKILL.md:46):
      run-and-read.
- [x] T4: Move cairn-init §2 → `skills/shared/migration-protocol.md`; add the
      read-on-footprint-detection directive to §0; re-anchor
      test_migration_guidance.py in the same commit (M46).
- [x] T5: Repo-wide grep sweep for pointers to the protocol's old home
      (tracking-rules, templates, DESIGN, references — live files only);
      update each.
- [x] T6: Run all three suites from the repo root (M56: no exit-blind pipes);
      register new mutation blocks or record the M47 by-hand check.

## Work log

- 2026-07-16: created by /milestone-plan (promoted from the RR01 rec
  7/12 half of the skill/hook candidate row; recs 8/13 → M60).
- 2026-07-16: T1 done — §0 fallback now canonical (ls-remote rung, never
  guess); guard extended test-first + 2 mutation entries; hooks'
  `--show-current` uses verified legitimate (current-branch checks).
- 2026-07-16: T2 done — review step 4 run-and-read; Coverage completeness
  kept as validate-output disposition (guard tokens survive), manual bullet
  gone; new guard file test_run_and_read_checks.py + 2 mutation entries.
- 2026-07-16: T3 done — /milestone §2 run-and-read (+1 guard test, +1
  mutation entry). Minor amendment: fixed adjacent "docs-only commit to
  main" → "to the default branch" in the same rewritten paragraph.
- 2026-07-16: T4 done — §2 body verbatim-moved (diff-clean) to the module;
  cairn-init 304→164 lines; pointer directive in the retained §2 stub;
  guards split-retargeted (protocol→module, §0/§1→skill) + 3 mutation
  entries retargeted/added, same commit (M46).
- 2026-07-16: T5 done — sweep found 4 note-and-leave hits ("§2" still
  resolves: cairn-init §2 remains the protocol via the pointer stub);
  DESIGN Architecture gained the shared-modules line (also closing M58's
  unlisted validation-doctrine.md gap).
- 2026-07-16: T6 done — 171+83+32 tests green from repo root, validate
  clean; all new asserts mutation-registered. Status → review.

## Decisions

## Review
