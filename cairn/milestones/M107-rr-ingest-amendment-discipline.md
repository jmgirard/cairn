# M107: RR-ingest / amendment discipline — the ingest surface carries the plan path's form, budget, and file hygiene

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, IP4
- **Branch/PR:** m107-rr-ingest-amendment-discipline · https://github.com/jmgirard/cairn/pull/105

## Goal

The brief-ingest and implement-amendment paths carry the form, budget, and
file-hygiene discipline the plan path already has, so folding review findings
into a live milestone no longer walks a compliant agent into a red gate or a
failed move.

## Scope

**In:**
- Prescribe the binding-criterion ingest form in milestone-brief step 3 and the
  milestone template AC comment: each BC lands as a numbered acceptance
  criterion carrying its trace tag — `- [ ] AC-N (BCn): <verbatim>` — so it is
  coverage-mappable and the verbatim body still satisfies the `binding
  criteria` check (`cairn_validate.py:651`).
- Wire the existing `cairn_budget` check + the tracking-rules one-pass-trim
  rule (`tracking-rules.md:128`) into the implement step-6 amendment gate and
  the brief ingest step — pointing at the tool and rule, not restating them.
- Make brief step 4's RB/RR archive move succeed whether or not the files are
  git-tracked (an in-session-generated or hand-dropped RR is untracked, so
  `git mv` fails today).
- Mutation-registered prose-guards for each new/changed skill + template block.

**Out:**
- No logic change to `check_coverage_complete` / `check_binding_criteria` — a
  BC-aware coverage message is a candidate row, not this milestone (Q1: guides
  + test only; the coverage check already enforces the mapping once BCs are
  numbered).
- Committing the RR at generation time → not taken; robust move covers every
  arrival path including a hand-dropped RR (Q2).
- Fresh budgeting prose on the amendment paths → not taken; extend the existing
  discipline (Q3).

## Acceptance criteria

- [x] AC1: milestone-brief step 3 prescribes the `- [ ] AC-N (BCn): <verbatim>`
      ingest form, and the milestone template's `## Acceptance criteria` comment
      states the same form.
- [x] AC2: a regression test builds a milestone with `Driving RR: RR<NN>` + a
      fixture RR whose binding criteria are ingested in the prescribed form and
      asserts both `binding criteria` and `coverage-complete` pass; the same
      milestone with the BCs as bare unnumbered `- [ ]` checkboxes fails
      `coverage-complete` (the intraclass failure, pinned).
- [x] AC3: milestone-implement step 6 (substantive amendment) and
      milestone-brief step 3 (BC ingest) each direct the agent to re-check the
      plan-owned body with `cairn_budget` after the amendment and, if over,
      compress the single heaviest plan-owned section in one pass per
      tracking-rules — by reference, not restated.
- [x] AC4: milestone-brief step 4's archive move succeeds whether or not the
      RB/RR files are git-tracked, and the step's prose names the robust
      mechanism.
- [x] AC5: every new/changed guarded block in milestone-brief,
      milestone-implement, and the template is registered in the mutation
      harness; the completeness meta-test passes.
- [x] AC6: `verify` clean — `python3 -m unittest` over scripts/tests,
      skills/tests, hooks/tests.

## Coverage

- AC1 → T2 · AC2 → T1 · AC3 → T3 · AC4 → T4 · AC5 → T2, T3, T4, T5 · AC6 → T5

## Tasks

- [x] T1: write the AC2 regression test first — reuse the temp-milestone +
      fixture pattern (`scripts/tests`, M102) to stand up a milestone + fixture
      RR, assert the prescribed form passes both checks and the bare-checkbox
      form fails `coverage-complete`.
- [x] T2: prescribe the ingest form in milestone-brief step 3 + template AC
      comment; register the changed blocks in the mutation harness.
- [x] T3: wire `cairn_budget` + the one-pass-trim rule into implement step 6 and
      brief ingest step 3 (by reference); register the changed blocks.
- [x] T4: make brief step 4's archive move robust to an untracked RB/RR (plain
      `mv` + `git add`, or a tracked-check); guard the step wording.
- [x] T5: run full `verify`; confirm the completeness meta-test and all three
      suites are green.

## Work log

- 2026-07-21: created by /milestone-plan.
- 2026-07-21: T1 — added scripts/tests/test_bc_ac_ingest_form.py pinning the ingest-form interaction (prescribed form quiet on both checks; bare ingest reds coverage-complete only, binding quiet). All three suites green.
- 2026-07-21: T2 — prescribed the `- [ ] AC-N (BCn): <verbatim>` ingest form in milestone-brief step 3 + template AC comment; two new mutation-registered guards; widened the section-owner parser to multi-line comments. skills 564 / scripts 274 green.
- 2026-07-21: T3 — wired the `cairn_budget` re-check + one-pass-trim rule into implement step-6 amendment gate and brief ingest step (by reference); new test_amendment_budget.py guard file + IMPLEMENT target, two mutation registrations. skills 566 green.
- 2026-07-21: T4 — brief step 4 archive move now uses plain `mv` + `git add`, never `git mv` (untracked RR fails it); guarded + mutation-registered. skills 567 green.
- 2026-07-21: T5 — full verify green (scripts 274, skills 567, hooks 72), cairn_validate exit 0; status → review.

## Decisions

## Review

**Acceptance-criteria evidence (2026-07-21, branch @ e18dd45):**
- AC1 — `- [ ] AC-N (BCn): <verbatim>` present in milestone-brief step 3 and
  the template AC comment (1 match each); TestIngestRule + TestMilestoneTemplate
  form guards pass.
- AC2 — scripts/tests/test_bc_ac_ingest_form.py (5 tests) green: prescribed
  form quiet on both `binding criteria` and `coverage-complete`; bare unnumbered
  ingest reds `coverage-complete` only, binding stays quiet.
- AC3 — `cairn_budget` re-check + one-pass-trim referenced in implement step 6
  and brief ingest step (1 each, by reference); test_amendment_budget.py
  (2 tests) green.
- AC4 — brief step 4 relocates with plain `mv` + `git add`, never `git mv`
  ("`git mv` fails on an untracked file" present); robust-move guard passes.
- AC5 — mutation harness green via discover (9 tests): completeness meta-test +
  per-block reddening of the four new guards.
- AC6 — verify clean: scripts 274, skills 567, hooks 72; `cairn_validate` exit 0.

**Consistency gate:** `cairn_validate` exit 0 (universal checks). Profile
`generic` → toolchain consistency-gate is a clean no-op. No DESIGN.md principle
changed (M107 works under IP3/IP4, does not alter them) → `cairn_impact`
skipped. Driving RR none → projection-vs-outcome no-ops.

**Independent fresh-context review (three lenses + scorer):**
- Diff-bug [O]: 1 finding (reproduced). Blame-history [S]: none. Prior-review
  [S]: no regression (GitHub probe empty; judged against archived Review
  sections), independently raised the same parser concern as sub-threshold.
- **F1 (scored 92, fixed)** — `test_section_allow_lists.py` `template_section_owners`:
  the widened owner-comment scan ran to the first `-->` anywhere below an H2
  with no section boundary, so a section missing its owner comment would borrow
  the next section's tag and skip the `assert m` (only the final H2 stayed
  protected). Fix: bound the scan to the section (up to the next `## ` or EOF);
  extracted `_owners_from_lines` + two regression tests (missing-owner middle
  section now asserts; multi-line comment still parses). skills 569, scripts 274.
- No sub-80 findings. Post-fix verify clean.
