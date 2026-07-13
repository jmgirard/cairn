# M45: Toolchain-profile spine — mechanism, r-package + generic profiles, init selection

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** GP1, GP3
- **Branch/PR:** —

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

- [ ] Two reference profiles ship — `skills/shared/profiles/r-package.md` and
      `skills/shared/profiles/generic.md` — each defining all six named slots.
      Evidence: files exist; a guard test asserts the six slot names in each.
- [ ] The `r-package` slot values reproduce today's hardcoded R commands
      (`devtools::test/document/check`, `pkgdown::check_pkgdown`, `.Rbuildignore`,
      NEWS). Evidence: a text-equivalence guard test maps r-package slot values
      to the current skill command strings.
- [ ] `cairn-init` recommends `r-package` when DESCRIPTION is present and
      `generic` otherwise, writes `cairn/PROFILE.md`, and repair-mode backfills a
      missing `PROFILE.md` by inferring from DESCRIPTION. Evidence: skill prose +
      a guard test asserting the detection rule and the backfill.
- [ ] `session_context` injects the active profile name at SessionStart and
      no-ops when `PROFILE.md` is absent. Evidence: hook unit test (present +
      absent).
- [ ] `cairn_validate` no-ops when `PROFILE.md` is absent and FAILs on a
      missing/unknown slot when present; `PROFILE.md` appears in the file-map,
      weight-caps, and `LINE_CAPS`. Evidence: validate unit tests (absent,
      present-valid, present-incomplete) + the three wiring points visible in
      the diff.
- [ ] Operational skills are unchanged — existing R behavior is byte-for-byte
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

- [ ] T1 — Author `skills/shared/profiles/generic.md` and `r-package.md`: the
      six-slot schema, `r-package` capturing current R commands verbatim
      (source of truth: grep the live command strings in the skills),
      `generic` the no-R path (verify = repo-declared test command,
      consistency-gate = cairn-file checks only, release-walk = tag path,
      init-detection = fallback, greenfield-openers = minimal).
- [ ] T2 — `tracking-rules.md`: add the profile concept — a paragraph naming the
      six slots and the "absent `PROFILE.md` → infer from DESCRIPTION" default;
      add the `cairn/PROFILE.md` file-map row and its weight-caps line.
- [ ] T3 — `cairn-init`: §0 detection recommends a profile; §1 instantiates the
      chosen reference into `cairn/PROFILE.md`; repair-mode backfills a missing
      declaration via DESCRIPTION inference.
- [ ] T4 — `session_context` hook: read + inject the active profile name; no-op
      when absent. Extend `hooks/tests/test_hooks.py`.
- [ ] T5 — `cairn_validate`: profile presence / slot-completeness check (no-op
      when absent); register `PROFILE.md` in `cairn_scripts.LINE_CAPS`. Extend
      the shared `Tree.build()` fixture / add a dedicated builder per the
      M24/M34 fixture pattern.
- [ ] T6 — Guard tests: the six slot names per profile, the `r-package`
      text-equivalence map, the init detection + backfill rule, and the
      "operational skills still hardcoded" negative assertion.

## Work log

- 2026-07-12: created by /milestone-plan (toolchain-profiles arc, milestone 1 of 3).

## Decisions

## Review
