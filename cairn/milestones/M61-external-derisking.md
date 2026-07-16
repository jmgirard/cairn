<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M61: External de-risking — env check, migration dry-run, Windows story, python CI parity

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Close RR01 rec 14's pre-1.0 external-adopter risks: environment
assumptions, first-contact migration safety, and cross-profile symmetry.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- Environment check in `/cairn-init` §0: verify `python3`, `git`, `gh`, and
  a remote; each missing piece gets a documented degradation path (RR01
  §10.2) — runs on scaffold, repair, and migration entry alike.
- An explicit Windows launcher story for `hooks.json`'s `python3`
  invocations (stock Windows has no `python3` on PATH — RR01 §10.2): an
  implemented fallback or a documented limitation; the choice is recorded as
  a milestone Decision. Windows-unverified honesty in DESIGN Known issues
  stays accurate either way.
- Migration **dry-run mode** in `skills/shared/migration-protocol.md`: a
  read-only pass producing the inventory + proposed translation ledger with
  nothing written, offered at migration entry (RR01 §10.3).
- Python profile CI-pair parity: mirror M52's r-package Codecov guidance in
  `skills/shared/profiles/python.md` `test-doctrine` (pytest-cov + GitHub
  Action analog beside the `coverage.py` diagnostic line), diagnostic-only.

**Out:** release docs, LICENSE, DRAFT removal → M62; v1.0 tag →
`/cairn-release` run after M62 merges; model-tier fallback doctrine (RR01
§10.2's Fable-less adopter) → stays inside the existing D-004 gating (no
change needed — escalation is already optional per instance); UI-merge
workflow docs (RR01 §10.4) → not in the candidate row; add later as a
candidate if wanted.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `/cairn-init` §0 contains an environment-check step covering
      `python3`, `git`, `gh`, and remote presence, each with a named
      degradation path; a prose-guard test in `skills/tests/` locks it.
- [ ] The Windows `python3`-launcher gap is closed by an implemented
      fallback in `hooks.json` **or** an explicitly documented degradation
      path; the chosen artifact exists and a milestone Decision line records
      the choice with rationale.
- [ ] `migration-protocol.md` defines a read-only dry-run mode (inventory +
      proposed ledger, nothing written) offered before a real migration; a
      prose-guard test locks it.
- [ ] `python.md` `test-doctrine` carries the CI-pair Codecov analog
      (diagnostic-only, never gates the merge), mirroring
      `r-package.md`; the profile guard suite covers it.
- [ ] All new prose-guards are mutation-registered
      (`skills/tests/test_mutation_harness.py` green, completeness meta-test
      passes).
- [ ] Verify clean: `python3 -m unittest discover -s skills/tests` and
      `discover -s scripts/tests` both green from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate; AC/Task counted top-to-bottom -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [ ] T1: Author the env-check step in `skills/cairn-init/SKILL.md` §0
      (python3/git/gh/remote; degradation path per piece; all three entry
      modes) + guard test.
- [ ] T2: Decide and land the Windows launcher story (fallback command in
      `hooks/hooks.json` vs documented limitation; update DESIGN Known
      issues if wording changes) + milestone Decision line. Note: a
      hooks.json *registration* change only live-fires in a fresh
      conversation (M60 lesson) — fixture-test what the hook prints.
- [ ] T3: Add the dry-run mode to `skills/shared/migration-protocol.md`
      (read-only inventory + ledger; offer chip at migration entry) + guard
      test.
- [ ] T4: Mirror the CI-pair guidance into `python.md` `test-doctrine`
      (pytest-cov + Codecov action line beside `coverage.py` diagnostic) +
      extend the profile guards.
- [ ] T5: Mutation-register every new prose-guard block (one physical line
      each — M59 lesson); run both suites from the repo root (M56 lesson).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan (carved from the "Public release
  prep" candidate row with M62; absorbs the "Python profile Codecov/CI
  parallel" candidate row).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55) -->
