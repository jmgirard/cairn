# M64: Durable-record preview — show authored record text verbatim before docs-only commits

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP4
- **Branch/PR:** m64-durable-record-preview · https://github.com/jmgirard/cairn/pull/62

## Goal

Every newly authored durable record — D-entry, plan-owned milestone section,
LESSONS line, archive summary, ROADMAP candidate/graduation row — is shown
verbatim in chat before the docs-only commit that lands it.

## Scope

**In:** a "Durable-record preview" rule in tracking-rules.md Output &
interaction discipline (mechanics per D-036: verbatim, same turn, no new
stop) + an explicit carve-out in the "Deltas, not dumps" rule; a one-line
preview directive at each durable-record commit step of the four gap skills
(/milestone-plan, /milestone-review, /milestone-implement, /milestone-brief);
guard tests + mutation registration.

**Out:** /cairn-release changelog-consolidation preview → declined at the
2026-07-16 plan gate (D-036; re-raise as a candidate if release-time text
proves surprising). /hotfix NEWS + code-branch content → already reviewable
at the PR/merge gate. /design-interview → co-authors its text in chat by
construction. /cairn-init → template boilerplate. Work-log one-liners,
checkbox ticks, status mirrors → exempt mechanical noise (D-036).

## Acceptance criteria

- [x] AC1: tracking-rules.md Output & interaction discipline contains a
      Durable-record preview rule naming the covered record types (D-entries;
      plan-owned milestone sections, new + gated amendments; LESSONS lines;
      archive summaries; ROADMAP candidate/graduation rows), the mechanic
      (verbatim in chat immediately before the commit, same turn, no new
      stop), and the exemptions (work-log one-liners, checkbox ticks, status
      mirrors, PR-branch content).
- [x] AC2: the "Deltas, not dumps" rule names the preview carve-out (drafted
      durable text is the deliverable, not a dump) so the two rules cannot be
      read as contradicting.
- [x] AC3: each of the four covered skills carries a one-line preview
      directive at its durable-record commit step(s): milestone-plan step 6,
      milestone-review post-merge hygiene, milestone-implement Decisions
      appends + amendment protocol, milestone-brief RR ingestion — evidenced
      by file:line grep hits scoped to `skills/*/SKILL.md`.
- [x] AC4: `skills/tests/test_durable_record_preview.py` exists, asserts
      AC1–AC3 with unique single-line anchors, and is registered in the
      mutation harness (harness + completeness meta-test green).
- [x] AC5: verify clean — all three suites (`skills/tests`, `scripts/tests`,
      `hooks/tests`) discover-run exit 0 from the repo root.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4

## Tasks

- [x] T1: Author the Durable-record preview rule in tracking-rules.md
      (Output & interaction discipline) + the carve-out clause in "Deltas,
      not dumps" — single-line unique anchor phrases (M59/M23), tokens
      inside bold (M26).
- [x] T2: Add the one-line preview directive at each commit step:
      milestone-plan/SKILL.md step 6; milestone-review/SKILL.md post-merge
      hygiene (~L175–185); milestone-implement/SKILL.md Decisions append +
      amendment protocol (step 6); milestone-brief/SKILL.md RR-ingestion
      commit (~L65).
- [x] T3: Write skills/tests/test_durable_record_preview.py (central-rule
      assert + four per-skill asserts, word-bounded) and register
      Mutation(...) entries; read targets per-test, never setUpClass cache
      (M61).
- [x] T4: Whole-repo grep sweep for contradicting phrasings ("never paste",
      "deltas, not dumps") on live surfaces — exclusions may name only
      history files (M48/M58); run all three suites from the repo root with
      exit codes gating the chain (M56).

## Work log

- 2026-07-16: created by /milestone-plan (promotes the durable-record-preview
  candidate row banked 2026-07-16; row graduates at completion per M35).
- 2026-07-16: T1 done — preview rule + Deltas-not-dumps carve-out in
  tracking-rules.md; all three suites green.
- 2026-07-16: T2 done — preview directives in plan (step 6), review
  (post-merge hygiene), implement (task loop + substantive amendments),
  brief (RR ingestion step 4); skills suite green.
- 2026-07-16: T3 done — guard file (9 tests) + 10 Mutation entries; skills
  suite 200 tests green (harness proves each block fails when blanked).
- 2026-07-16: T4 done — sweep found no live contradiction (remaining "never
  paste" hits govern tracking files, not chat); all three suites + validate
  green; status → review.
- 2026-07-16: review F1 (93) correction — the guard file has 8 tests, not
  the 9 claimed in the T3 line above and AC4 evidence (evidence fixed).

## Decisions

## Review

PR: https://github.com/jmgirard/cairn/pull/62 (draft; base main @ a2271b0).

- AC1 (2026-07-16): rule at tracking-rules.md:362–369 — types, mechanic
  ("shown verbatim in chat immediately before", "same turn, no added stop"),
  exemptions all grepped; guard TestDurableRecordPreviewRule green.
- AC2 (2026-07-16): carve-out at tracking-rules.md:361 ("not a dump — see
  the Durable-record preview rule below."); guard green.
- AC3 (2026-07-16): directive grep hits — plan:107, review:186,
  implement:63+79, brief:65. First grep missed review (directive wrapped
  mid-name, M59 reflow trap); fixed on branch: reflowed + guard/mutation
  re-anchored, suite re-run green.
- AC4 (2026-07-16): guard file exists (8 tests); 10 Mutation entries;
  harness + completeness meta-test green (skills suite 200 tests OK).
- AC5 (2026-07-16): skills/tests, scripts/tests, hooks/tests all OK from
  repo root; cairn_validate all checks passed.
- Consistency gate (2026-07-16): validate exit 0; generic profile
  consistency-gate slot names no toolchain checks (clean no-op); no
  IP/GP changed → cairn_impact skipped.
- Fan-out (2026-07-16): diff-bug 2 findings; blame + prior-PR lenses clean
  (prior-PR: no inline-comment evidence, expected no-op). Scored: F1 93
  (record said "9 tests", guard has 8) → fixed (evidence corrected,
  work-log correction appended); F2 70 (rule's PR-branch exemption drops
  D-036's hotfix-scoping parenthetical; implement's own directive is
  unconditional so no practical gap) → sub-threshold, logged not actioned;
  surfaced at the approval gate. Gate: user directed the F2 fix — exemption
  scoped to hotfix/code-branch content per D-036; suite re-run green.
