<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M22: Generalize cairn beyond `main`; recalibrate the mature-repo CLAUDE.md cap

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m22-mature-repo-defaults · https://github.com/jmgirard/cairn/pull/19

## Goal

Fix the two cairn defaults the M20 ackwards pilot proved don't survive a real
mature repo — the `main`-hardcoded git model and the `<80` CLAUDE.md cap — so
migration and the health audit work on a `master` repo with legitimate dev
doctrine.

## Scope

**In:**
- **Default-branch parameterization (G1/G9).** cairn stops assuming `main`.
  The git model in `tracking-rules.md` (~15 refs), the CLAUDE.md template, and
  `/cairn-init` §2 (`skills/cairn-init/SKILL.md`, ~3 refs incl. step 2 "cut
  from up-to-date main") read against the repo's actual default branch —
  detected at init, spoken as "default branch (main/master)" or the detected
  name in prose. `master` repos get correct branch language, not verbatim
  `main` that contradicts the repo.
- **Weight-cap recalibration (G8).** Replace the `<80` CLAUDE.md cap — which
  FAILs a mature repo (ackwards' CLAUDE.md is 187 lines of legit dev doctrine +
  the ~26-line appended cairn section) — with a model that passes a legitimate
  mature repo without waving through genuinely bloated files. Touches the cap
  model in three wired places: `tracking-rules.md` weight-caps text (line ~82),
  `scripts/cairn_scripts.py` `LINE_CAPS` (line 41), and
  `scripts/cairn_validate.py` `check_caps`. Chosen model recorded as a D-entry.

**Out:**
- Migration §2 guidance for a rich pre-existing DESIGN.md, in-code reference
  sweeps, and `.Rbuildignore`/Lineage-B-detection hygiene → **M23** (depends on
  this).
- Toolchain-profile-based cap (per-language cap slot) → stays the "Toolchain
  profiles" candidate; this milestone picks a repo-agnostic model, and if that
  model is "profile-based" it defines the slot but does not build the full
  profile system.
- Runtime-guard hardening (on-main commit guard, memory-guard content-gating)
  → stays as candidate rows; deferred this run.

## Acceptance criteria

- [x] cairn no longer hardcodes `main`: `/cairn-init` detects the repo's
      default branch, and the git model (`tracking-rules.md`), the CLAUDE.md
      template, and `/cairn-init` §2 read correctly for a `master` repo (no bare
      `main`-only instruction that would contradict such a repo). Evidence: the
      ~18 refs updated; a guard test asserting the git-model + init branch
      language is not bare-`main`; a walk-through of §2 step 2 on a `master`
      repo producing correct branch text.
- [x] The `<80` CLAUDE.md hard cap is replaced by a model that does **not**
      FAIL a legitimate mature repo (a ≥150-line real-doctrine CLAUDE.md fixture
      passes the audit) while still flagging genuine bloat. The chosen model is
      recorded as a D-entry in `cairn/DECISIONS.md`. Evidence: `cairn_validate`
      run against a mature-repo fixture (pass) and a bloated fixture (flag);
      the D-entry.
- [x] The cap model is consistent across all three wiring points —
      `tracking-rules.md` weight-caps text, `cairn_scripts.LINE_CAPS`, and
      `cairn_validate.check_caps` all agree (the M16 four-wiring-points lesson).
      Evidence: a `scripts/tests/` unit test on `check_caps` with both fixtures,
      plus the tracking-rules text matching the code.
- [x] Guard-test suite green over `skills/tests/` and `scripts/tests/`.
      Evidence: test run output.

## Coverage

- AC1 → T3, T4
- AC2 → T1, T2
- AC3 → T2, T5
- AC4 → T5

## Tasks

- [x] **T1** — Cap model chosen: cap-only-cairn-section (D-018).
- [x] **T2** — Cap change in `cairn_scripts.py` (`CLAUDE_SECTION_CAP=30`,
      `claude_section_line_count`; `LINE_CAPS` drops CLAUDE.md) +
      `cairn_validate.check_caps` + tracking-rules text/remedy; +2 fixtures.
- [x] **T3** — Default branch parameterized in the tracking-rules git model +
      adjacent doctrine (12 refs → "the default branch"; `main`/`master` gloss).
- [x] **T4** — Default branch in `/cairn-init` (§0 detection, §1/§2 refs) and
      the `claude-md-section.md` template (section = 24 lines).
- [x] **T5** — `test_default_branch_parameterized.py` (5 cases) locks the
      parameterization + section-scoped cap doctrine.

## Work log

- 2026-07-12: created by /milestone-plan. Absorbs ROADMAP candidates
  "Recalibrate the CLAUDE.md weight cap" (G8) and "Parameterize the default
  branch" (G1/G9), both from `references/migration-pilot-notes.md` (M20).
  Sequenced before M21 per the harden-before-pilot decision.
- 2026-07-12: gate — cap model = cap-only-cairn-section (D-018); branch =
  detect + generic rulebook. T1 done: D-018 recorded.
- 2026-07-12: T2–T5 done. Cap now measures the cairn CLAUDE.md section (30),
  whole file uncapped; default branch parameterized across git model + template
  + cairn-init (detected via `symbolic-ref`). 51 skills + 33 scripts tests
  green. Discovered follow-up: operational `main` git commands in the other
  skills are out of scope → new ROADMAP candidate (M22 Out).

## Decisions

## Review

Reviewed 2026-07-12 on branch `m22-mature-repo-defaults` (PR #19). R gates
waived (plugin repo). No IP/GP changed → `cairn_impact` skipped.

**Evidence per criterion**

- **AC1 (default branch):** `git symbolic-ref --short refs/remotes/origin/HEAD`
  → `origin/main` → detected `main`; on a `master` repo it resolves `master`,
  with a current-branch fallback when no remote HEAD. The git model, CLAUDE
  template, and cairn-init §2 all read "the default branch"; the only residual
  bare `main` in tracking-rules is the intentional ``(`main`/`master`)`` gloss
  (line 185) and the unrelated "main session" (orchestrator). Locked by
  `test_default_branch_parameterized.py` (5 cases, green).
- **AC2 (cap):** `test_mature_claude_md_whole_file_not_capped` — a 210-line
  CLAUDE.md (would fail the old `<80`) passes; `test_over_cap_claude_section` —
  a 36-line cairn section fails with `cap <30`. Model recorded as D-018.
- **AC3 (three wiring points):** `cairn_scripts` (`CLAUDE_SECTION_CAP=30`,
  `LINE_CAPS` drops `CLAUDE.md`), `cairn_validate.check_caps` (section
  measurement), and tracking-rules text ("`## Project tracking` section … < 30")
  all agree; both fixtures exercise `check_caps`.
- **AC4 (suites):** 51 skills + 33 scripts tests green.

**Consistency gate:** `cairn_validate` exit 0 (9/9). Coverage complete —
AC1→T3,T4 · AC2→T1,T2 · AC3→T2,T5 · AC4→T5, all mapping to existing tasks.

**Independent review** (two lenses + Sonnet scorer). 2 findings, both scored
below the 80 actioned threshold — logged per IP3:
- [65] cairn-init §0 detection fallback said "when there is no remote" but
  `symbolic-ref` also fails on an unset `origin/HEAD` (shallow clone, fresh
  `remote add`, CI checkout). Sub-threshold, but a trivial correct fix to
  in-milestone text → **fixed**: fallback broadened to "whenever that fails".
- [8] this repo's own root `CLAUDE.md` still says "main" — factually correct
  (this repo's branch *is* `main`) and deliberately out of AC1's
  template-scoped remit; no action. Reviewer also noted stale `<80` mentions
  in `references/` study notes (historical record, not live enforcement) — no
  action.
No finding scored ≥80; nothing required triage-to-fix.
