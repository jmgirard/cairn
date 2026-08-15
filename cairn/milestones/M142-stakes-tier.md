# M142: The plan gate scales criteria rigor to the deliverable's stakes

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** m142-stakes-tier

## Goal

`/milestone-plan` classifies every scope's deliverable surface and holds
internal-tier criteria to a domain-bounded standard, so verification effort
tracks user-facing stakes instead of growing without limit on internal
tooling — the measured failure in intraclass M120 and circumplex M72–M86.

## Scope

**In:** the step-2 surface-tier rule and internal-tier criteria standard; the
step-3 criteria audit's proportionality question; the step-2 collision check's
checker-regress clause — all in `skills/milestone-plan/SKILL.md` — plus their
prose-guards, mutation-registry entries, and one D-entry.

**Out:** any change to D-090's own clauses — its cairn-scoped door and
Untouched clause stand, annotated only. Out: the review-side thrash remedy →
M143. Out: triage of intraclass M120 and circumplex's norms-audit arc → those
repos' own sessions. Out: adoption piloting for standing instruments → the
existing standing-instrument candidate row (ROADMAP), cross-referenced.

## Acceptance criteria

- [ ] AC1 `/milestone-plan` step 2 states the surface-tier rule: every plan
      classifies the milestone's deliverable as user-facing or internal, where
      internal means no external consumer of the repo relies on it — dev
      tooling, data-generation scripts, in-repo checkers over internal
      artifacts, tracking records — and user-facing is everything else,
      including any deliverable whose tier is unclear or that spans both; the
      tier and a one-clause reason are recorded in the milestone file's Goal
      or Scope prose. A registered prose-guard reds when the rule is deleted
      from the skill.
- [ ] AC2 The same step states the internal-tier criteria standard: an
      internal-tier acceptance criterion's promise quantifies over a domain
      its named procedure enumerates directly — never an exemption registry, a
      per-rendering enumeration, or a demonstration family spanning process or
      environment boundaries — and a draft needing those is repaired at the
      plan gate by narrowing the promise (step 4's bounded-promise rule) or by
      descoping, never by widening the specification. The standard governs a
      criterion's promise, never a guard's construction — a detector's
      per-rendering positive controls stay mandated by their own doctrine. A
      registered prose-guard reds when the standard is deleted.
- [ ] AC3 The step-3 criteria audit asks a proportionality question of each
      criterion — is the promise's domain proportionate to the declared
      tier — and an internal-tier criterion outside AC2's standard is a
      finding disposed at the gate like the audit's other findings. A
      registered prose-guard reds when the question is deleted from the
      audit's question list.
- [ ] AC4 The step-2 collision check names the checker-regress shape — a scope
      extending or hardening a checker that the ROADMAP or archive records an
      earlier milestone of the same repo shipping, where that checker verifies
      repo-internal artifacts — and directs that on such a hit the gate poses
      simplifying or deleting the checker as the recommended option and
      hardening it as a present, non-recommended alternative. A repair that
      leaves the checker's promise unchanged stays outside the shape (D-090's
      Untouched clause); one that widens the checker's promise is the regress
      shape however it is framed. A registered prose-guard reds when the
      regress clause is deleted.
- [ ] AC5 The three suites pass from the repo root with per-suite exit codes
      checked; every prose-guard this milestone adds or edits is registered in
      the mutation harness per protected block, and each new rule sentence
      survives relabel, negation, subject-transposition, and relocation probes
      red. A D-entry records the stakes-tier adoption and the regress question
      as a new rule beside D-090's cairn-scoped door — annotating D-090 with
      its Untouched clause intact, hosted per D-098 — and names the
      shipped-behavior defect clearing D-090's trigger: the plan gate as
      shipped accepts internal-tier scopes whose criteria demand unbounded
      specification, measured in the downstream repos.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4, T5

## Tasks

- [x] T1 Author the step-2 surface-tier rule and internal-tier criteria
      standard in `skills/milestone-plan/SKILL.md` (anchors copied from
      shipped bytes; adjacent-guard reflow check per the M104 lesson).
- [ ] T2 Add the proportionality question to the step-3 criteria-audit
      paragraph, beside the existing one-exemplar probe it must not oppose.
- [ ] T3 Add the checker-regress clause, with its repair discriminator, to the
      step-2 collision check.
- [ ] T4 Write prose-guards for the four new rules; register per protected
      block in the mutation harness; run relabel, negation,
      subject-transposition, and relocation probes red (commit fixes before
      any probe that restores — M140 lesson).
- [ ] T5 Append the D-entry (next free id); run `cairn_validate` and the three
      suites from the repo root with per-suite exit codes checked.

## Work log

- 2026-08-15: created by /milestone-plan, from the maintainer's churn/thrash report over intraclass and circumplex (measured: intraclass M120's four returns in one day; circumplex M72–M86's fifteen-milestone checker arc).
- 2026-08-15: criteria audit ran (fresh [O] reader, two rounds) — round 1 returned nine findings, all disposed at the gate; round 2 on the amended wording returned five residual scoping findings, fixed in place (AC4 repair discriminator, AC2 promise-scope clause, AC5 D-090-trigger naming, plus two on M143).
- 2026-08-15: plan gate chose a regress gate-question with deletion recommended over a D-090-style hard door because a hard door narrows D-090's Untouched clause and adds supersede ceremony to legitimate hardenings; falsified by a tracked repo accepting the recommended deletion where the checker's absence then admits a user-facing defect it would have caught.
- 2026-08-15: plan gate chose a domain-bounded lite standard over a numeric probe-count cap because the cap contradicted the shipped one-exemplar probe (audit round-1 finding 1); falsified by an internal-tier criterion within the standard still consuming three defect returns.
- 2026-08-15: T1 — surface-tier rule and internal-tier criteria standard authored into /milestone-plan step 2 (two paragraphs after the criteria-drafted rule); question gate skipped, nothing genuinely open — both approach choices were settled at the plan gate; three suites green (786/345/103, per-suite exit codes checked).

## Decisions

## Review
