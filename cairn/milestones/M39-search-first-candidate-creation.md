<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M39: Search-first candidate creation

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m39-search-first-candidate-creation · https://github.com/jmgirard/cairn/pull/37

## Goal

Before any candidate row is added — by any skill or conversationally — sweep
existing candidates, the archive, and DECISIONS for overlap and absorb or
cross-reference a hit instead of adding a duplicate.

## Scope

**In:** a "search-first candidate creation" rule in `tracking-rules.md`
(sweep targets + on-hit action), generalizing the plan-time collision check
to every candidate-creation point; brief pointers at the ad-hoc creation
steps that run outside that check (`/hotfix`, `/milestone-review`); a
prose-guard test.

**Out:** a mechanical duplicate-detector (fuzzy row-overlap script/validate
check → candidate; noisy, over-scope — the rule is judgment-based like the
plan collision check); restating the rule in each skill (the rulebook states
it once; skills bind through it per the "nothing is said twice" convention).

## Acceptance criteria

- [x] `tracking-rules.md` states a search-first candidate-creation rule: before
      adding a candidate row, sweep existing candidates + `milestones/archive/`
      + `DECISIONS.md` for overlap; on a hit, absorb into or cross-reference the
      existing row rather than duplicate, and a standing rejection follows the
      existing supersede discipline. Binds any skill and conversational adds.
- [x] The ad-hoc candidate-creation steps in `/hotfix` and `/milestone-review`
      carry a one-line pointer to the rule (a pointer, not a restatement).
- [x] A guard test locks the rule's presence in `tracking-rules.md` (single-line
      anchor per the M23/M26 lessons).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks

- [x] T1 — Add the search-first candidate-creation rule to `tracking-rules.md`,
      at/near the Intake "Candidates may be added ... at any time" line.
- [x] T2 — Add a brief pointer at `/hotfix` step 7 and the `/milestone-review`
      follow-up-candidate step referencing the rule.
- [x] T3 — Add a prose-guard test in `skills/tests/` asserting the rule text on
      a single line; run the skills guard suite green.

## Work log

- 2026-07-12: created by /milestone-plan.
- 2026-07-12: T1 — added the "Search-first candidate creation" rule to `tracking-rules.md` after the Intake paragraph; branch cut, status → in-progress.
- 2026-07-12: T2 — one-line pointers at `/hotfix` step 7 and the `/milestone-review` follow-up-candidate triage step (pointers, not restatements).
- 2026-07-12: T3 — added `test_search_first_candidates.py` (rule + both pointers); skills guard suite green (89 tests).
- 2026-07-12: all tasks done; skills (89) + scripts (53) suites green, cairn_validate clean; status → review.
- 2026-07-12: review — PR #37; all 3 ACs verified with fresh evidence; independent review found 1 finding (guard-test coverage gap, scored 88), fixed on-branch by re-anchoring the sweep-target assertions; suites re-run green.

## Decisions

## Review

Reviewed 2026-07-12 (same-session implement→review; PR #37).

**Acceptance-criteria evidence (fresh):**
- AC1 → tracking-rules.md:187–194 states the rule after the Intake paragraph;
  `grep` confirms all four elements (sweep targets, absorb/cross-reference,
  supersede discipline, binds any skill + conversational adds).
- AC2 → one-line pointers at `hotfix/SKILL.md:57` and
  `milestone-review/SKILL.md:127`; both are pointers ("sweep first per the
  search-first candidate-creation rule (`tracking-rules.md`, Intake)"), not
  restatements — Scope Out honored.
- AC3 → `test_search_first_candidates.py` (4 tests) green; full skills suite
  89/89, scripts suite 53/53, `cairn_validate` exit 0 (coverage complete).

**Consistency gate:** cairn_validate all-pass (mirror, one-in-progress, caps,
coverage complete, ISO dates, scaffold). No DESIGN principle changed → impact
report skipped. R gates (devtools/README.Rmd/pkgdown/NEWS) waived per CLAUDE.md.

**Independent review (two lenses + scorer):**
- [O] diff-bug: 1 finding — guard test's `milestones/archive/` + `decisions.md`
  assertions were trivially satisfiable by pre-existing occurrences elsewhere in
  the file, so the "all three sweep targets" guarantee wasn't enforced.
- [S] blame-history: no findings (rule is a pure addition; not a duplicate of
  the plan-time collision check — deliberately generalizing it).
- [S] scorer: finding scored 88 (≥80, actioned). **Fixed now** — assertions
  re-anchored on the rule's own contiguous phrasing
  (`sweep existing candidates + \`milestones/archive/\``, `\`decisions.md\` for
  overlap`); suite re-run green. No sub-threshold findings.
