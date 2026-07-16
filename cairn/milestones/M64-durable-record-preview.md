# M64: Durable-record preview — show authored record text verbatim before docs-only commits

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP4
- **Branch/PR:** m64-durable-record-preview

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

- [ ] AC1: tracking-rules.md Output & interaction discipline contains a
      Durable-record preview rule naming the covered record types (D-entries;
      plan-owned milestone sections, new + gated amendments; LESSONS lines;
      archive summaries; ROADMAP candidate/graduation rows), the mechanic
      (verbatim in chat immediately before the commit, same turn, no new
      stop), and the exemptions (work-log one-liners, checkbox ticks, status
      mirrors, PR-branch content).
- [ ] AC2: the "Deltas, not dumps" rule names the preview carve-out (drafted
      durable text is the deliverable, not a dump) so the two rules cannot be
      read as contradicting.
- [ ] AC3: each of the four covered skills carries a one-line preview
      directive at its durable-record commit step(s): milestone-plan step 6,
      milestone-review post-merge hygiene, milestone-implement Decisions
      appends + amendment protocol, milestone-brief RR ingestion — evidenced
      by file:line grep hits scoped to `skills/*/SKILL.md`.
- [ ] AC4: `skills/tests/test_durable_record_preview.py` exists, asserts
      AC1–AC3 with unique single-line anchors, and is registered in the
      mutation harness (harness + completeness meta-test green).
- [ ] AC5: verify clean — all three suites (`skills/tests`, `scripts/tests`,
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

## Decisions

## Review
