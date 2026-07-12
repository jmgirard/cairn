<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M22: Generalize cairn beyond `main`; recalibrate the mature-repo CLAUDE.md cap

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m22-mature-repo-defaults

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

- [ ] cairn no longer hardcodes `main`: `/cairn-init` detects the repo's
      default branch, and the git model (`tracking-rules.md`), the CLAUDE.md
      template, and `/cairn-init` §2 read correctly for a `master` repo (no bare
      `main`-only instruction that would contradict such a repo). Evidence: the
      ~18 refs updated; a guard test asserting the git-model + init branch
      language is not bare-`main`; a walk-through of §2 step 2 on a `master`
      repo producing correct branch text.
- [ ] The `<80` CLAUDE.md hard cap is replaced by a model that does **not**
      FAIL a legitimate mature repo (a ≥150-line real-doctrine CLAUDE.md fixture
      passes the audit) while still flagging genuine bloat. The chosen model is
      recorded as a D-entry in `cairn/DECISIONS.md`. Evidence: `cairn_validate`
      run against a mature-repo fixture (pass) and a bloated fixture (flag);
      the D-entry.
- [ ] The cap model is consistent across all three wiring points —
      `tracking-rules.md` weight-caps text, `cairn_scripts.LINE_CAPS`, and
      `cairn_validate.check_caps` all agree (the M16 four-wiring-points lesson).
      Evidence: a `scripts/tests/` unit test on `check_caps` with both fixtures,
      plus the tracking-rules text matching the code.
- [ ] Guard-test suite green over `skills/tests/` and `scripts/tests/`.
      Evidence: test run output.

## Coverage

- AC1 → T3, T4
- AC2 → T1, T2
- AC3 → T2, T5
- AC4 → T5

## Tasks

- [ ] **T1** — Settle the cap model: pick higher-flat vs size-tiered vs
      soft-warn-not-fail vs profile-slot (recommended default: soft-warn the
      cairn-owned budget, don't hard-FAIL total lines, so legit doctrine passes
      but drift is still surfaced). Record the choice + rejected options as a
      D-entry in `cairn/DECISIONS.md`.
- [ ] **T2** — Implement the cap change in `scripts/cairn_scripts.py`
      `LINE_CAPS` (line 41) + `scripts/cairn_validate.py` `check_caps` +
      `tracking-rules.md` weight-caps text (line ~82); add a `scripts/tests/`
      unit test with a mature-repo fixture (passes) and a bloated fixture
      (flagged).
- [ ] **T3** — Parameterize the default branch in the `tracking-rules.md` git
      model (~15 `main` refs) — detected branch / "default branch (main/master)".
- [ ] **T4** — Parameterize the default branch in `/cairn-init`
      (`skills/cairn-init/SKILL.md`: §2 step 2 + scaffold/commit lines) and the
      CLAUDE.md template; add default-branch detection at init (§0/§1).
- [ ] **T5** — Guard test locking the new invariants (git model + init carry no
      bare-`main` assumption; cap model shape); run the full suite green; commit
      tracking + code together.

## Work log

- 2026-07-12: created by /milestone-plan. Absorbs ROADMAP candidates
  "Recalibrate the CLAUDE.md weight cap" (G8) and "Parameterize the default
  branch" (G1/G9), both from `references/migration-pilot-notes.md` (M20).
  Sequenced before M21 per the harden-before-pilot decision.

## Decisions

## Review
