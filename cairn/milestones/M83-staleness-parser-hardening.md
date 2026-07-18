<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M83: Staleness-parser hardening — the extraction status stops being guessed at

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m83-staleness-parser-hardening`   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] F3: a status whose leading clause claims a dated verification and whose
      later prose mentions a prior unverified state classifies `ambiguous`,
      not `never`, and the advisory names the page and says the status
      contradicts itself. Regression test uses the 2026-07-18 `task-master.md`
      wording verbatim and fails against the pre-fix function.
- [ ] F4: `never verified against the source` no longer classifies `ok`,
      **and** all three shipped `partly verified at ingestion` pages
      (`bmad-method`, `backlog-meridian`, `spec-kit`) still classify `ok`.
      Both directions are tested — the second is the M79-F5 trap this fix
      must not walk into.
- [ ] F5: a verified date later than today WARNs with its own diagnostic
      instead of producing a negative age and a permanent exemption.
- [ ] No shipped page is reclassified silently: the milestone file records a
      before/after state for all 16 committed `references/` pages, and every
      page whose state changes carries a one-line justification. A change is
      allowed; an unexplained one is not (IP2).
- [ ] Blast radius holds: `_last_verified` still has exactly one caller, and
      `check_references` output over the 16 pages is byte-identical before
      and after.
- [ ] `verify` clean — all three suites green:
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
- [ ] T2. Restructure `_last_verified` to split the status into a leading
      clause and a remainder, and classify from the leading clause. Keep the
      `nothing to re-verify` exemption at precedence 1. Define the clause
      boundary explicitly (em-dash / semicolon / end-of-status) and test it.
- [ ] T3. `ambiguous` state + diagnostic (F3) — leading clause says verified,
      remainder contradicts it.
- [ ] T4. `unrecognized` state + diagnostic (F4) — no recognized state token
      and no date. Verified-family must cover the verification verbs the
      corpus actually uses (`verified`, `read against`, `checked against`),
      or T7 will surface the newly-flagged pages for a decision.
- [ ] T5. Future-date guard (F5): a verified date after today gets its own
      WARN, never a negative age.
- [ ] T6. Fixture matrix over the axes this classification is free in —
      where the contradicting token sits, wrapping *at the clause boundary*,
      decoration on the token. Per M81's lesson, vary the axis where the
      value under test lives: a wrap that does not fall at the boundary
      proves nothing here.
- [ ] T7. Run the real advisory over the real 16 pages, reconcile against
      T1's baseline, record the before/after in this file with
      justifications, and run all three suites.

## Work log

- 2026-07-18: created by /milestone-plan. Absorbs the grouped M81 candidate row (F3/68, F4/63, F5/62); F3 confirmed live 2026-07-18 during the task-master re-verification.
- 2026-07-18: T1 — ledger test pins all 16 shipped pages (14 ok, 2 exempt); green against the unmodified function, mutation-checked (flipping one entry fails).

## Decisions

## Review
