# M45: Toolchain-profile spine — mechanism, r-package + generic profiles, init selection

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** GP1, GP3
- **Branch/PR:** m45-toolchain-profile-spine · https://github.com/jmgirard/cairn/pull/43

## Goal

Establish the toolchain-profile mechanism — a `cairn/PROFILE.md` declaring a
repo's language profile and its six slots — and ship the `r-package` and
`generic` reference profiles selected at init, without yet rewiring any
operational skill.

## Scope

**In:**
- Define the six-slot profile format (verify, consistency-gate, test-doctrine,
  release-walk, init-detection, greenfield-openers) and ship two reference
  profiles under `skills/shared/profiles/` — `r-package` (captures today's R
  commands verbatim) and `generic` (no-R).
- `cairn-init`: DESCRIPTION present → recommend `r-package`, else `generic`;
  instantiate the chosen reference into `cairn/PROFILE.md`; repair-mode
  backfills a missing declaration by inferring from DESCRIPTION.
- `session_context` hook surfaces the active profile name at SessionStart;
  no-op when `cairn/PROFILE.md` is absent.
- `cairn_validate`: no-op when `PROFILE.md` is absent (back-compat for the five
  existing R adopters); when present, FAIL on a missing/unknown slot. Wire
  `PROFILE.md` into the tracking-rules file-map + weight-caps and
  `cairn_scripts.LINE_CAPS` (no dates → no date-scan point; 3 of the 4 M16
  wiring points).

**Out:**
- Operational skills still hardcode R commands — they keep working, profiles
  aren't read yet → M46.
- Release-walk generalization (cairn-release) → M47.
- Greenfield opener-question *content* → greenfield-init candidate (the slot
  exists here; its content is that candidate's job).
- Oracle / Validation doctrine stays universal and untouched — it is the
  orthogonal domain axis, not part of the language profile (D-024/D-025).

## Acceptance criteria

- [x] Two reference profiles ship — `skills/shared/profiles/r-package.md` and
      `skills/shared/profiles/generic.md` — each defining all six named slots.
      Evidence: files exist; a guard test asserts the six slot names in each.
- [x] The `r-package` slot values reproduce today's hardcoded R commands
      (`devtools::test/document/check`, `pkgdown::check_pkgdown`, `.Rbuildignore`,
      NEWS). Evidence: a text-equivalence guard test maps r-package slot values
      to the current skill command strings.
- [x] `cairn-init` recommends `r-package` when DESCRIPTION is present and
      `generic` otherwise, writes `cairn/PROFILE.md`, and repair-mode backfills a
      missing `PROFILE.md` by inferring from DESCRIPTION. Evidence: skill prose +
      a guard test asserting the detection rule and the backfill.
- [x] `session_context` injects the active profile name at SessionStart and
      no-ops when `PROFILE.md` is absent. Evidence: hook unit test (present +
      absent).
- [x] `cairn_validate` no-ops when `PROFILE.md` is absent and FAILs on a
      missing/unknown slot when present; `PROFILE.md` appears in the file-map,
      weight-caps, and `LINE_CAPS`. Evidence: validate unit tests (absent,
      present-valid, present-incomplete) + the three wiring points visible in
      the diff.
- [x] Operational skills are unchanged — existing R behavior is byte-for-byte
      intact. Evidence: `git diff` shows no change to the command lines in
      implement/review/hotfix/release; a guard test asserts those skills still
      carry their hardcoded commands (no profile read yet); existing suites green.

## Coverage

- AC1 → T1, T6
- AC2 → T1, T6
- AC3 → T3, T6
- AC4 → T4
- AC5 → T5, T2
- AC6 → T6

## Tasks

- [x] T1 — Author `skills/shared/profiles/generic.md` and `r-package.md`: the
      six-slot schema, `r-package` capturing current R commands verbatim
      (source of truth: grep the live command strings in the skills),
      `generic` the no-R path (verify = repo-declared test command,
      consistency-gate = cairn-file checks only, release-walk = tag path,
      init-detection = fallback, greenfield-openers = minimal).
- [x] T2 — `tracking-rules.md`: add the profile concept — a paragraph naming the
      six slots and the "absent `PROFILE.md` → infer from DESCRIPTION" default;
      add the `cairn/PROFILE.md` file-map row and its weight-caps line
      (+ `cairn_scripts.LINE_CAPS` entry — the M16 weight-cap second wiring point).
- [x] T3 — `cairn-init`: §0 detection recommends a profile; §1 instantiates the
      chosen reference into `cairn/PROFILE.md`; repair-mode backfills a missing
      declaration via DESCRIPTION inference.
- [x] T4 — `session_context` hook: read + inject the active profile name; no-op
      when absent. Extend `hooks/tests/test_hooks.py`.
- [x] T5 — `cairn_validate`: profile presence / slot-completeness check (no-op
      when absent); register `PROFILE.md` in `cairn_scripts.LINE_CAPS` (done in
      T2). Base `Tree.build()` untouched (M34/M38 no-op-when-absent pattern);
      dedicated `TestValidateProfile` + a shipped-reference validity guard.
- [x] T6 — Guard tests: the six slot names per profile, the `r-package`
      text-equivalence map, the init detection + backfill rule, and the
      "operational skills still hardcoded" negative assertion
      (`skills/tests/test_toolchain_profiles.py`, +6).

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 1 of 3).
- 2026-07-12: T1 — shipped `skills/shared/profiles/{generic,r-package}.md` (6 slots each; r-package captures current commands verbatim).
- 2026-07-12: T2 — tracking-rules "Toolchain profiles" section + PROFILE.md file-map row + weight-cap (<90) in rulebook and `cairn_scripts.LINE_CAPS`.
- 2026-07-12: T3 — cairn-init selects profile (§0), instantiates cairn/PROFILE.md (§1 tree + step), repair-mode backfills by DESCRIPTION inference.
- 2026-07-12: T4 — session_context injects the active profile name (no-op when PROFILE.md absent); +2 hook tests (present/absent).
- 2026-07-12: T5 — cairn_validate `check_profile` (no-op absent; FAIL on missing/empty/unrecognized slot) + `TestValidateProfile` (+6) incl. shipped-reference validity.
- 2026-07-12: T6 — `test_toolchain_profiles.py` (+6): six slots, r-package text-equivalence, generic-has-no-R, init select+backfill, AC6 operational-skills-unchanged.
- 2026-07-12: review — all 6 ACs verified with fresh evidence; consistency gate clean. Fan-out diff-bug finding (scored 91) fixed: `_profile_slots` fence-aware + regression test.

## Decisions

- 2026-07-12 (T1): PROFILE.md schema = markdown `# Toolchain profile: <name>`
  header + one `## <slot>` H2 per slot (freeform body: command block or prose),
  matching every other cairn tracking file. Chosen over YAML frontmatter
  (awkward for the prose slots test-doctrine/release-walk; breaks the
  all-markdown convention) and freeform-no-structure (loses mechanical
  slot-completeness checking). `cairn_validate` parses the H2s. The six slots:
  verify, consistency-gate, test-doctrine, release-walk, init-detection,
  greenfield-openers. The oracle/Validation doctrine is NOT a slot (universal,
  orthogonal — D-024/D-025).

## Review

**PR:** https://github.com/jmgirard/cairn/pull/43 · reviewed 2026-07-12 · no CI in this repo (M16).

**Acceptance-criteria evidence** (fresh, by command):
- AC1 — both profiles ship with all six slots: `test_both_profiles_define_all_six_slots` + `test_shipped_reference_profiles_are_valid` (the plugin's own references satisfy `check_profile`) green.
- AC2 — r-package reproduces live R commands: `test_r_package_reproduces_live_commands` green (10 command tokens present in both the profile and the current skills — token drift on either side would trip it).
- AC3 — cairn-init select + backfill: `test_init_selects_and_backfills_profile` green (DESCRIPTION→r-package/else generic, `cairn/PROFILE.md`, repair backfill).
- AC4 — hook present/absent: `TestSessionContext.test_injects_profile_name_when_present` + `test_no_profile_section_when_absent` green.
- AC5 — validate-if-present + wiring: `TestValidateProfile` (absent no-op, valid pass, missing/empty/unrecognized slot FAIL) green; `LINE_CAPS` entry + file-map row + weight-cap line present in the diff.
- AC6 — operational skills intact: `git diff --name-only main..HEAD` touches none of milestone-implement/review/hotfix/cairn-release; `TestOperationalSkillsUnchanged` green.

**Consistency gate:** `cairn_validate` exit 0 (13 CHECKS PASS + sizing OK). Coverage-complete PASS. No DESIGN.md principle changed (M45 works under GP1/GP3, does not edit them) → `cairn_impact` skipped. R-package consistency-gate items (devtools/pkgdown/NEWS/.Rbuildignore) waived — cairn is a non-package repo. Full suites: skills 105 / scripts 64 / hooks 32, all green. M45 file 126/150 lines.

**Independent fresh-context review:** three lenses + scorer.
- [O] diff-bug: 1 finding — `_profile_slots` treated any `## ` line as a slot heading, so a fenced command-block slot body containing a column-0 `## comment` (schema sanctions command blocks) would be misparsed → false gate failure. Scorer **91** (execution-confirmed). **Fixed now**: `_profile_slots` is fence-aware; regression test `test_fenced_command_block_body_not_a_slot`.
- [S] blame-history: no findings (change is additive; M16 3-of-4 wiring intentional, D-018/D-024/D-025/M34-38 patterns respected).
- [S] prior-PR-comments: no prior-PR evidence (cairn PRs carry ~no inline review comments — M40) — clean no-op.
- No sub-threshold (<80) findings.
