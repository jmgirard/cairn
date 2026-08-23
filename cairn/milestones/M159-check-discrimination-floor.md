# M159: The test floor states check discrimination: five distilled principles

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP4
- **Branch/PR:** m159-check-discrimination-floor · https://github.com/jmgirard/cairn/pull/160

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

- [x] AC1: The "What gets a test" section of `skills/shared/tracking-rules.md`
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
- [x] AC2: Rulebook growth is bounded: `git diff --numstat $(git merge-base
      main HEAD)..HEAD -- skills/shared/tracking-rules.md` reports ≤ 14 in
      its added-lines column.
- [x] AC3: `cairn/DECISIONS.md` carries a new D-entry that (a) states the
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
- 2026-08-23: review — AC1-AC3 pass on fresh evidence; gate green; three-lens fan-out: one fix-now (rulebook-mass baseline re-seeded in three sites, M149 lesson), rest rejected at triage with reasons in Review; suites re-run green.

## Decisions

## Review

- 2026-08-23 AC1: fresh read of `skills/shared/tracking-rules.md` "What gets
  a test" — the shipped "Check discrimination" paragraph states all five
  principles recognizably: planted-defect proof, non-empty domain, one
  independent fact, untouched-shape/silent-case fixtures, identity-or-kind
  assertions. PASS.
- 2026-08-23 AC2: `git diff --numstat $(git merge-base main HEAD)..HEAD --
  skills/shared/tracking-rules.md` → 7 added / 0 removed; 7 ≤ 14. PASS.
- 2026-08-23 AC3: D-126 read fresh — states the shipped-behavior defect
  (floor silent on check discrimination after M146 deleted guard-doctrine.md)
  and its measured cost (quarto-index returns M01/M08/M23; own module
  `cairn/check-design.md` @ 3fbf848), and records the door walk (D-108
  retained trigger, hosted per D-098, supersedes nothing). PASS.
- 2026-08-23 gate: cairn_validate exit 0, all checks pass; suites green
  (scripts 324, hooks 103); no DESIGN.md principle changed → impact skip;
  generic profile → toolchain half no-op. No Driving RR → projection
  juxtaposition no-ops.
- 2026-08-23 fan-out (user-facing tier, three lenses). Findings and triage:
  - [S-prior] F1 (top-ranked): deliberate tracking-rules.md change without
    re-seeding the rulebook-mass baseline pinned in three places
    (`skills/milestone/SKILL.md:94`, `skills/tests/test_cost_audit_line.py:67`,
    `skills/tests/test_mutation_harness.py:117`, all still "443 lines /
    40,949 chars") — regresses the M149 LESSONS line. Verified: file now
    453 / 41,941. **Fixed at the gate**: all three sites re-seeded to
    "453 lines / 41,941 chars (M159, 2026-08-23)"; suites re-run green
    (skills 528, scripts 324, hooks 103).
  - [S-blame]: no findings; observation that the D-108 trigger is a softer
    instance than D-098's precedent, judged a reasoned application (plan-gate
    work-log line with falsifier). Logged, no action.
  - [O] 1 (restates shipped rules; principles 1/5 overlap the
    failure-identity rule and fails-before-fix): **rejected** — overlap is
    partial (planting defects to prove a new check ≠ regression test for a
    bug fix; identity-or-kind generalizes failure identity to checks), and
    the five-principle list is AC1's plan-owned normative content.
  - [O] 2 (D-126 "shipped nothing" overstated): **rejected** — the claim
    names the "What gets a test" section; the failure-identity rule lives in
    Universal tracking rules, and no passage addressed check discrimination
    as such. D-entry stands (IP4; a nuance, not a proven-false claim).
  - [O] 3 ("never printed text alone" vs the meaningful-snapshots
    allowance): **rejected** — the snapshot line governs what gets a test,
    the new line how a check asserts; a pinned meaningful snapshot is an
    identity assertion, not "printed text alone".
  - [O] 4 (door walk: doctrine-prose omission is D-090's ordinary-work case,
    not the retained trigger): **rejected** — the plan gate weighed exactly
    this and recorded the satisfied-trigger reading with a falsifier
    (work log 2026-08-23); an intentional, gated decision. Blame lens
    concurred it is a reasoned application.
  - [O] 5 (paragraph lands after the section's boundary sentence):
    **rejected** — style; the boundary sentence scopes profile specifics vs
    the floor, and the appended paragraph is floor content it covers.
  - [O] 6 ("report" term imported): **rejected** — the wording matches AC1's
    normative principle (4) verbatim; recognizable in context as a check's
    report.
  - [O] 7 (imperative line could be read as the declined per-check mandate):
    **rejected** — the craft register was the plan-gate choice; the declined
    form's falsifier (a vacuous check surviving review in an adopting repo)
    is recorded in Out and D-126.
  - [O] 8 (quarto-index citations ambiguous/unpinned, ids unpadded):
    **rejected** — AC3's required citation form followed; "its own" scopes
    the path and ids to quarto-index, whose ids are not cairn's to re-pad
    (D-125 is repo-local); module read pinned at 3fbf848.
  - [O] 9 (milestone-file edits uncommitted): **resolved** before the gate —
    committed as ea4f8fc.
- Return floor: no finding demonstrates an acceptance criterion failing and
  none is judged a load-bearing deliverable defect surviving the fix; F1
  fixed at the gate, no status return.
