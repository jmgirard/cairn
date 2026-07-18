<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M83: Staleness-parser hardening — the extraction status stops being guessed at

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m83-staleness-parser-hardening` · https://github.com/jmgirard/cairn/pull/81   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Make `_last_verified` classify an extraction status from what the status
actually claims, and say so when it cannot tell, instead of silently
resolving a contradiction the author never sees.

## Scope

**In:** `_last_verified` in `scripts/cairn_validate.py:771-803` and its
`references staleness` advisory. Three M81 review findings, all in that one
function: F3 (`_UNVERIFIED` tested before any date, so a dated `verified`
status with any later mention of a prior unverified state reports "no
verified re-check"), F4 (negative-verified synonyms escape the flag and fall
through to the ingested-date fallback, classifying `ok`), F5 (a future
verified date yields a negative age and permanently exempts the page with no
diagnostic). Classification moves to the status's leading clause, with two
new diagnostic states — `ambiguous` (leading token contradicted later) and
`unrecognized` (no state token and no date) — both WARN.

**Out:** widening either note template's sanctioned vocabulary → stays a
candidate row (the parser is being made to fit the prose that already
exists, not the reverse). Rewriting any shipped `references/` page to suit
the parser → not done; AC4 makes reclassification visible instead. Touching
`_extraction_status`, `_provenance_block`, or the hard `references` CHECK →
explicitly out, and AC5 proves it (M81 F1: a gate and an advisory need
opposite protections against the same parser).

## Acceptance criteria

- [x] F3: a status whose leading clause claims a dated verification and whose
      later prose mentions a prior unverified state classifies `ambiguous`,
      not `never`, and the advisory names the page and says the status
      contradicts itself. Regression test uses the 2026-07-18 `task-master.md`
      wording verbatim and fails against the pre-fix function.
- [x] F4: `never verified against the source` no longer classifies `ok`,
      **and** all three shipped `partly verified at ingestion` pages
      (`bmad-method`, `backlog-meridian`, `spec-kit`) still classify `ok`.
      Both directions are tested — the second is the M79-F5 trap this fix
      must not walk into.
- [x] F5: a verified date later than today WARNs with its own diagnostic
      instead of producing a negative age and a permanent exemption.
- [x] No shipped page is reclassified silently: the milestone file records a
      before/after state for all 16 committed `references/` pages, and every
      page whose state changes carries a one-line justification. A change is
      allowed; an unexplained one is not (IP2).
- [x] Blast radius holds: `_last_verified` still has exactly one caller, and
      `check_references` output over the 16 pages is byte-identical before
      and after.
- [x] `verify` clean — all three suites green:
      `python3 -m unittest discover -s scripts/tests`,
      `-s skills/tests`, `-s hooks/tests`.

## Coverage

- AC1 → T3, T6
- AC2 → T2, T4, T6
- AC3 → T5, T6
- AC4 → T1, T7
- AC5 → T2, T7
- AC6 → T7

## Tasks

- [x] T1. Characterization test pinning the current `_last_verified` state of
      each of the 16 committed pages, as the AC4 baseline. Written and green
      against the *unmodified* function first.
- [x] T2. Restructure `_last_verified` to split the status into a leading
      clause and a remainder, and classify from the leading clause. Keep the
      `nothing to re-verify` exemption at precedence 1. Define the clause
      boundary explicitly (em-dash / semicolon / end-of-status) and test it.
- [x] T3. `ambiguous` state + diagnostic (F3) — leading clause says verified,
      remainder contradicts it.
- [x] T4. `unrecognized` state + diagnostic (F4) — no recognized state token
      and no date. Verified-family must cover the verification verbs the
      corpus actually uses (`verified`, `read against`, `checked against`),
      or T7 will surface the newly-flagged pages for a decision.
- [x] T5. Future-date guard (F5): a verified date after today gets its own
      WARN, never a negative age.
- [x] T6. Fixture matrix over the axes this classification is free in —
      where the contradicting token sits, wrapping *at the clause boundary*,
      decoration on the token. Per M81's lesson, vary the axis where the
      value under test lives: a wrap that does not fall at the boundary
      proves nothing here.
- [x] T7. Run the real advisory over the real 16 pages, reconcile against
      T1's baseline, record the before/after in this file with
      justifications, and run all three suites.

## Work log

- 2026-07-18: created by /milestone-plan. Absorbs the grouped M81 candidate row (F3/68, F4/63, F5/62); F3 confirmed live 2026-07-18 during the task-master re-verification.
- 2026-07-18: T1 — ledger test pins all 16 shipped pages (14 ok, 2 exempt); green against the unmodified function, mutation-checked (flipping one entry fails).
- 2026-07-18: T2-T6 — classifier restructured; ambiguous/unrecognized/future states added; 5 regression tests + a 48-cell matrix, all failing pre-fix. Two defects found by the tests themselves, recorded as M83-D1/D2.
- 2026-07-18: fixed a red main of my own making — the 2026-07-18 task-master re-verification wrapped its Extraction status over five lines, which M78's one-physical-line guard rejects; I ran cairn_validate then but not the suites. Fixed on main (be19ff4), branch rebased onto it.
- 2026-07-18: `git merge main` into this branch was denied by merge_guard (direction-blind containment match) though tracking-rules prescribes exactly that when main moves; synced by rebase instead, which never touches main. Reported, not worked around silently.
- 2026-07-18: T7 — 0 of 16 pages reclassified (14 ok, 2 exempt, unchanged); `_last_verified` still has exactly one caller; `check_references` output identical. All three suites green by explicit exit code.
- 2026-07-18: out-of-scope defect found and left alone: `_provenance_block` joins collected blocks with no blank line (`cairn_validate.py:294`), so a body line matching the provenance heading starts a second block that the extraction status then absorbs — `oracle-discipline-notes.md`'s status parses as 652 chars, not 186. Candidate row added; no classification changes today.
- 2026-07-18: review — PR #81 opened (draft); all six criteria carry fresh evidence recorded in the Review section, consistency gate green; prior-PR lens returned no findings, diff-bug and blame lenses still running.
- 2026-07-18: review findings — 3 lenses + scorer; 5 diff-bug findings, 3 scored >=80 and 4 sub-threshold, all fixed on the branch (F1/F2/F3 were one root cause: negation read as a phrase list instead of a clause property). 4 regression tests added; shipped-page classification unchanged.

## Decisions

- **M83-D1: the contradiction test reads the whole status; the clause split
  only picks the state.** The plan said "classify from the leading clause".
  That alone is not enough: `_extraction_status` rejoins a hard-wrapped status
  with a space, so a status wrapped *at* its em-dash arrives with the
  separator gone and both claims sitting in the leading clause — the F3 bug
  intact. So a never-claim and an independent verification claim anywhere in
  the status is `ambiguous`, and the leading/remainder split only decides
  which single state applies when there is no contradiction. Found by the
  boundary-wrap fixture, not by reading — the pre-existing midpoint-wrap axis
  could not reach it (M81's "vary the axis where the value lives").
- **M83-D2: never-phrases are removed before testing for a verification
  claim.** `never verified` contains `verified`; read naively, every plainly-
  never page becomes a self-contradiction. The suite caught this, as it caught
  `read against` matching inside `re-read against` — the source-note
  template's own unverified wording, which would have turned the template's
  sanctioned form into a contradiction.

- **M83-D3 (supersedes M83-D1 and M83-D2; review, 2026-07-18).** Both earlier
  decisions describe the first cut, which the review broke in both directions
  (F1/92, F2/92). The shipped mechanism is neither "leading clause decides"
  (D1) nor "strip never-phrases, then look for a verification" (D2): a status
  is split into clauses, and **every** verification-verb occurrence in each
  clause is read as affirmative or negated according to whether a negator
  precedes it *in that clause*. Both a `never` and a `verified` claim anywhere
  → `ambiguous`. D1 and D2 stand as the record of what was tried; this is what
  ships. Consequence for the plan text: Scope and AC1 describe classification
  in leading-clause terms. Every acceptance criterion still passes **as
  written** — the behavior AC1 names is delivered — but the Scope sentence
  "Classification moves to the status's leading clause" now describes the
  superseded mechanism rather than the shipped one. Surfaced at the merge gate
  rather than silently reinterpreted (IP2); Scope is amend-via-gate and was
  deliberately not edited review-side.

## Review

**PR** https://github.com/jmgirard/cairn/pull/81 · reviewed 2026-07-18.

### Acceptance-criteria evidence (fresh, by command)

- **AC1 (F3 ambiguous).** `test_dated_verification_with_a_prior_unverified_note_is_ambiguous`
  passes, using the verbatim status `task-master.md` carried on 2026-07-18.
  Pre-fix evidence gathered at review by restoring `main`'s
  `cairn_validate.py` under the new tests: suite exits 1 with this test
  among 6 failing methods; restored, exits 0.
- **AC2 (F4 both directions).** `test_negative_synonym_no_longer_reads_as_verified`
  and `test_partly_verified_pages_are_not_swept_up` both pass — the second
  runs the three shipped `partly verified at ingestion` statuses
  (`backlog-meridian`, `bmad-method`, `spec-kit`) and asserts each stays
  clean, which is the M79-F5 trap direction.
- **AC3 (F5 future).** `test_future_verification_date_is_flagged_not_silently_exempt`
  passes; a date 30 days ahead reports `dated <date>, in the future` instead
  of a negative age.
- **AC4 (no silent reclassification).** `test_every_shipped_page_keeps_its_pinned_state`
  passes over the real `cairn/references/` tree. The criterion asks *this
  file* to carry the before/after state, so it is recorded here rather than
  left in the test's `EXPECTED` map (review F7/58: the states lived only in
  the test, and ticking the box on the strength of a summary line would have
  been the charitable reading the never-reinterpret rule forbids). `before` is
  `main`'s `_last_verified`, `after` is this branch's, both over the same 16
  pages. 0 changed, so no justifications are owed.

  | Page | Before | After |
  |---|---|---|
  | `anthropic-code-review.md` | ok | ok |
  | `backlog-meridian.md` | ok | ok |
  | `bmad-method.md` | ok | ok |
  | `ccpm.md` | ok | ok |
  | `claude-code-hooks.md` | ok | ok |
  | `claude-md-management.md` | ok | ok |
  | `competitive-landscape.md` | ok | ok |
  | `design-interview-notes.md` | exempt | exempt |
  | `desktop-toc-mechanism.md` | ok | ok |
  | `feature-dev.md` | ok | ok |
  | `llm-wiki.md` | ok | ok |
  | `migration-pilot-notes.md` | exempt | exempt |
  | `oracle-discipline-notes.md` | ok | ok |
  | `oracle-doctrine-intraclass-notes.md` | ok | ok |
  | `spec-kit.md` | ok | ok |
  | `task-master.md` | ok | ok |
- **AC5 (blast radius).** `_last_verified` occurs twice in the file — one
  definition, one call site (the advisory). `check_references` output over
  the 16 pages is identical pre and post.
- **AC6 (verify clean).** All three suites green by explicit exit code, not
  through a pipe (LESSONS M56+M65): scripts 155 / skills 356 / hooks 72,
  each `rc=0`.

### Consistency gate

- `cairn_validate.py` exit 0 — 15 PASS, no FAIL, no WARN.
- Profile `generic`: the `consistency-gate` slot names no toolchain checks,
  so that half is a clean no-op.
- No `DESIGN.md` principle changed (IP2 is worked *under*, not modified), so
  `cairn_impact.py --changed` is skipped per the gate's own condition.

### Independent review — 3 lenses + scorer

Blame-history: faithful to prior intent (M81's `for_extraction` separation and
paragraph-collection both untouched; the M81 precedence is superseded openly,
not overwritten). Prior-PR: no findings — this repo records review findings in
milestone archives, not GitHub comments, and none is regressed. Diff-bug: five
findings, all reproduced by the orchestrator before triage.

**Actioned (≥80), all fixed on the branch:**

- **F1/92** — the contradiction test stripped only negations of the word
  `verified`, so a negated `checked against` / `read against` survived and read
  as an independent verification. `unverified — … with no claim checked against
  the source at ingestion` — verbatim the prose `task-master.md` carried on
  2026-07-18 — reported "extraction status contradicts itself". A false
  positive on the very wording that motivated the milestone (D-023).
- **F2/92** — the same gap in the other direction: `not checked against the
  source at ingestion` read as verified and reached the ingested-date fallback,
  so a page saying in plain words it was never checked got a clean bill. F4's
  own failure shape, surviving under the verbs M83 itself added.
- **F4/83** — the future guard took `max()` over every date in the status, so
  `verified <date>; next re-check due <later date>` reported a page verified 17
  days ago as dated in the future.

**Sub-threshold, folded into the same fix rather than deferred** (LESSONS M73 —
the score gates the actioned list, not the operator's judgment):

- **F3/76** — excluding a `re-` prefix wholesale also rejected affirmative
  re-verifications (`re-verified against the source` → `unrecognized`). Same
  root cause as F1/F2: negation belongs to the clause, not to a phrase list.
- **F5/72** — `_split_status` was provably dead for the outcome (0 divergences
  over 104 reachable combinations) while the docstring documented it as the
  mechanism deciding ambiguity. Replaced by the clause scan it now describes.
- **F6/74** — `_UNVERIFIED` left unreferenced above a comment asserting the
  premise F3 disproved. Now carries its own negation and is referenced again.
- **F7/58** — AC4 asked *this file* for the before/after state; the states
  lived only in the test's `EXPECTED` map. Recorded above rather than waved
  through on a charitable reading.

**Root cause.** F1–F3 were one defect: the fix matched affirmative verbs against
a fixed list of negative phrases, and the list only covered `verified`.
Negation is a property of a clause, so it is now detected as one —
`_clause_claims` reads every verb occurrence and asks whether a negator
precedes it in that clause. Clause scope is what keeps it narrow: the three
`partly verified at ingestion` pages carry `not re-read since` in a *later*
clause, which a status-wide negation search would have swept up.

The `wrapped-at-boundary` fixture earned its place twice — it failed the first
review-fix too, catching a first-match-wins read that reproduced F3 one layer
down once the rejoined wrap put both claims in a single clause.

4 regression tests added (159 tests, was 155); 3 of the 4 fail against the
pre-review-fix code, the fourth is a no-regression guard for F5. Shipped-page
classification is unchanged by the review fixes: still 14 ok, 2 exempt.
