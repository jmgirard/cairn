# M159: The test floor states check discrimination: five distilled principles

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP4
- **Branch/PR:** m159-check-discrimination-floor

## Goal

Add a compact check-discrimination passage to the universal "What gets a
test" floor in `skills/shared/tracking-rules.md`, distilling the five
transferable principles quarto-index paid repeated review returns to learn,
so adopting repos stop rediscovering them. Surface tier: user-facing — the
rulebook is the shipped product every adopting repo reads.

## Scope

**In:** ≤14 added lines in the "What gets a test" section, craft register
(imperative prose, no recorded per-check evidence mandate); the door-walk
D-entry (D-108's retained trigger, hosted per D-098); source citation of
quarto-index `cairn/check-design.md` @ 3fbf848 (2026-08-23).

**Out:** any new module, budget header, validator check, guard test, or
mutation registration (D-109: no prose guard owed) → nowhere, refused;
quarto-index's repo-specific instances (Quarto/makeindex/shell-runner
pitfalls) → stay in that repo's local module; a mandatory per-check
discrimination-proof rule → declined at the plan gate, revisit only on its
falsifier (a vacuous check reaching a default branch past review in an
adopting repo); profile `test-doctrine` slot changes → none needed, the
floor is language-agnostic.

## Acceptance criteria

- [ ] AC1: The "What gets a test" section of `skills/shared/tracking-rules.md`
      states, in shipped prose, all five check-discrimination principles as
      restated here (this list is normative): (1) a new check is proven able
      to fail by planting the defect class it claims to catch; (2) a check
      whose domain, pattern, or input artifact can silently empty is shown to
      run over a non-empty domain; (3) an expectation derived from the
      artifact under test keeps one fact stated independently of that
      artifact; (4) fixtures include shapes the change leaves untouched and
      at least one case where a new report must stay silent; (5) checks
      assert identity or kind, never counts or printed text alone — each
      recognizable by its concept on a read of the section.
- [ ] AC2: Rulebook growth is bounded: `git diff --numstat $(git merge-base
      main HEAD)..HEAD -- skills/shared/tracking-rules.md` reports ≤ 14 in
      its added-lines column.
- [ ] AC3: `cairn/DECISIONS.md` carries a new D-entry that (a) states the
      shipped-behavior defect and its measured downstream cost — the floor's
      silence on check discrimination, paid in quarto-index review returns
      (M01, M08, M23) and in that repo authoring its own doctrine module —
      cited by quarto-index repo-relative path and milestone ids; and (b)
      records that this milestone proceeds on D-108's retained trigger,
      hosted per D-098, superseding nothing in D-090/D-108.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2

## Tasks

- [x] T1: Draft the five-principle passage into "What gets a test"
      (`skills/shared/tracking-rules.md:436`), ≤14 added lines, craft
      register; grep the repo for restating surfaces (README and profiles
      verified clean at plan time — re-verify after drafting).
- [x] T2: Append the door-walk D-entry to `cairn/DECISIONS.md` per AC3.
- [x] T3: Run both gating suites (`python3 -m unittest discover -s
      scripts/tests`, `… -s hooks/tests`) and hand-run `skills/tests`
      (M148 lesson: edits near guarded rulebook regions); repair any red
      traced to the edit.

## Work log

- 2026-08-23: created by /milestone-plan.
- 2026-08-23: criteria audit ran in full mode (fresh [O] reader): three findings — AC1 dual-authority ambiguity, AC2 unpinned merge-base/count procedure, AC3 record-only (no defect/cost stated) — all fixed at the gate; bounded-promise, probe, and proportionality questions returned nothing.
- 2026-08-23: plan gate chose proceeding through D-108's door on the satisfied-trigger reading over parking as a candidate or staying repo-local because the floor ships nothing on check discrimination (guard-doctrine.md, which carried the discrimination test, was deleted whole in M146) and quarto-index's rediscovery cost is measured; falsified by evidence that the addition itself starts a hardening spiral (returns thrashing on the new floor lines).
- 2026-08-23: plan gate chose the universal floor over a new shared module because check-writing is universal (D-031's own boundary test), nearly every milestone writes checks, and M146 deliberately deleted the module home for this content family; falsified by adopter-side evidence that the floor lines burden sessions that never write checks.
- 2026-08-23: plan gate chose craft register over a mandatory per-check discrimination-proof rule because the mandate would re-grow the certification burden RR13/M144-M146 dismantled; falsified by a vacuous check reaching a default branch past review in an adopting repo.
- 2026-08-23: T1 — "Check discrimination" paragraph appended to "What gets a test" (7 added lines, numstat); restating-surface grep found only pre-existing planted-defect criteria wording in milestone-plan/milestone-brief SKILL.md; suites green (scripts 324, hooks 103).
- 2026-08-23: T2 — D-126 appended (door walk: D-108 retained trigger, hosted per D-098, supersedes nothing); append verified by re-read; suites green.
- 2026-08-23: T3 — gating suites green (scripts 324, hooks 103); skills/tests hand-run: 528 tests, zero reds; branch numstat on tracking-rules.md: 7 added / 0 removed. All tasks done; status to review.

## Decisions

## Review
