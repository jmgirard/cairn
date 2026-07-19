<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M89: Partial verification is a state — the staleness advisory stops failing toward green

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** GP2
- **Branch/PR:** m89-partial-verification-false-green

## Goal

A references page that reports incomplete or undatable verification stays on
the staleness backlog instead of silently reading as fully checked.

## Scope

**In:** two defects in `scripts/cairn_validate.py`, both resolving toward
false-green, found live in the intraclass session 2026-07-19.

*Defect A — partiality is invisible.* `partly verified at ingestion` parses as
an affirmative `verified` claim (`_clause_claims:895-898` matches the verb and
finds no negator before it), carries no date, and falls through to the block's
`Ingested` date (`_last_verified:970-975`), returning `("ok", <ingest date>)`.
The qualifier is never read; the state lattice has no partial state, so a
partial verification resolves to the optimistic pole. Live on three pages here
(`spec-kit.md`, `bmad-method.md`, `backlog-meridian.md`) and on four intraclass
notes, where it dropped the advisory 15 → 11 with one passage checked in each.

*Defect B — the gate and the advisory disagree on what an ingested date is.*
`check_references_staleness:1008` skips `undated` because "the references CHECK
already FAILs that block" (`:982-985`), but `check_references:407` tests
`_PROV_INGESTED.search(block)` — regex match alone — while `_last_verified:971-975`
additionally requires `_iso()` to parse a date from the captured group. A block
whose ingested date matches but is not parseable ISO satisfies the CHECK *and*
returns `undated` to the advisory, falling silently through both.

**Out:** provenance-block concatenation (`_provenance_block`'s separator-free
join) → stays a candidate row; its trigger is misclassification via block
*collection*, upstream of and independent from status classification, and
neither defect here touches it. Citekey resolution → stays a candidate row.

## Acceptance criteria

- [x] A status whose verification verb carries a partiality qualifier in its own
      clause resolves to a new `partial` state, never `ok`; the advisory WARNs
      naming the page as only partly checked, distinct from the `never` message.
- [x] Negation still beats partiality: a negated verb in a clause that also
      carries a partiality qualifier resolves `never`, not `partial`.
- [x] The M79-F5 trap is not reintroduced — the shipped pages carrying
      `not re-read since` in a *later* clause are not swept up by the new
      qualifier search, proven by a fixture per page.
- [x] A provenance block whose ingested date matches `_PROV_INGESTED` but yields
      no parseable ISO date is reported by exactly one of the gate or the
      advisory, and by name — never silently skipped by both.
- [x] Every new fixture is built from wording that shipped: the four intraclass
      note statuses and this repo's three `partly` pages, quoted as-is.
- [x] `source-note.md` and `synthesis-note.md` teach the partial form in their
      verb-set comments, and each new prose guard is mutation-registered.
- [x] Profile `verify` clean: `python3 -m unittest discover -s scripts/tests`,
      `-s skills/tests`, `-s hooks/tests` (each exit code checked separately,
      from the repo root, unpiped — M56/M65), and `cairn_validate.py` exit 0.

## Coverage

- AC1 → T2, T3, T4
- AC2 → T2, T3
- AC3 → T1, T2
- AC4 → T5
- AC5 → T1
- AC6 → T6, T7
- AC7 → T8

## Tasks

- [x] T1 — Regression fixtures first: reproduce both defects as failing tests in
      `scripts/tests/`, quoting the live intraclass and in-repo wording verbatim.
      Give every false-positive fixture a realistic value on the axis it defends
      (M88) and check the test helper for defaulted parameters before believing
      any discrimination claim.
- [x] T2 — Add a `_PARTIAL` qualifier regex searched in `clause[:verb.start()]`,
      mirroring `_NEGATOR`'s clause-scoped placement (`_clause_claims:893-899`);
      emit a `partial` claim for an affirmative verb so qualified.
- [x] T3 — Thread `partial` through `_last_verified`'s precedence (`:910-985`),
      deciding and documenting how `{partial, verified}` and `{partial, never}`
      collapse; a partial claim must never reach the `ok` return.
- [x] T4 — Give `check_references_staleness` a `partial` branch with its own
      message; remove `partial` from any skip list.
- [x] T5 — Align the ingested-date predicate across `check_references:407` and
      `_last_verified:971-975` so one definition serves both, then re-derive
      whether the `undated` skip's stated justification now holds and rewrite
      the comment to match what the code does.
- [x] T6 — Update both note templates' verb-set comments to teach the partial
      form; run each member of the taught set through the implementation
      individually, never the set as a whole (M75/M85).
- [x] T7 — Mutation-register each new prose guard; author every anchor on its own
      physical line, unwrapped, with trailing punctuation (M78/M82), and verify
      by inversion — relabel the rule in place, require red, restore and diff (M74).
- [x] T8 — Re-run the advisory over this repo, report the count delta, and
      resolve any page the fix newly surfaces (D-045: corrected in place).

## Work log

- 2026-07-19: created by /milestone-plan; both defects found live in the intraclass session, with partial-state semantics, defect-B inclusion, and the evidence bar set at the question gate.
- 2026-07-19: implement gate settled three open choices — the never > partial > verified lattice ({never, verified} stays ambiguous), a tight qualifier set (partly | partially | in part | spot-check(ed)), and defect B fixed by tightening the CHECK behind a shared `_ingested_date` predicate.
- 2026-07-19: T2–T5 — `_PARTIAL` qualifier + `_resolve_claims` lattice + a `partial` advisory branch + one shared `_ingested_date` predicate behind both readers; all three verify suites green, validate exit 0.
- 2026-07-19: T1 — 10 regression fixtures red across both defects; the four intraclass note statuses (donner2002, konishi1989, naik2007, young1998, commit dea301f) and this repo's three `partly` pages quoted as shipped.
- 2026-07-19: T6–T7 — both templates teach the partiality set and its no-date-clears-it consequence; three new guards, five mutation entries (per template, per test), and an inversion check (`partly` → `mostly` in place) turned 4 guards red before restore.
- 2026-07-19: T8 — `references staleness` on this repo goes OK (0) → WARN (3); all three are true positives whose statuses already say what was and was not checked, so nothing is corrected in place and clearing them needs a re-read of three external clones (out of scope).
- 2026-07-19: all tasks done, three verify suites green and validate exit 0 — status → review.
- 2026-07-19: review — 3 lenses (1 finding scored 95, actioned; 2 clean), consistency gate clean, all 7 criteria verified with fresh evidence; AC5 initially failed on one fixture (spec-kit anchors abbreviated) and was fixed before the tick.
- 2026-07-19: review F1 fixed on branch — a partiality qualifier overlapping its verb (`spot-checked against`) read as a full verification; `_qualified_partial` now searches to `verb.end()`, and the T6 guard runs three clause shapes per qualifier.
## Decisions

### M89-D1 (2026-07-19): The verification lattice is never > partial > verified; `{never, verified}` alone stays ambiguous

**Context:** Adding a third state to `_last_verified` forced a rule for every
pair. M83 had answered the one pair that existed by reporting `{never,
verified}` as `ambiguous` — whichever is tested first is the bug.
**Decision:** Collapse claims most-conservative-first: `never` beats `partial`
beats `verified`. `{never, partial}` → `never`, because the four intraclass
notes that motivated this lead `unverified` and then record a spot-check, and
letting partiality win would UPGRADE a page that says plainly it was never
checked. `{partial, verified}` → `partial`, not `ambiguous`: a page saying
"the appendix was only partly checked" beside "verified against the source"
is qualifying itself, not contradicting itself. `{never, verified}` keeps
M83's `ambiguous`; partiality does not dissolve it.
**Consequences:** No qualification anywhere in a status can be cleared by an
unqualified clause elsewhere, and `partial` returns before any date is read —
what a partial pass lacks is coverage, which no threshold can age out.
Rejected: any-mixture-is-ambiguous, which would report this repo's three
`partly` pages as self-contradicting when they are simply honest.

## Review

_Reviewed 2026-07-19. PR: https://github.com/jmgirard/cairn/pull/88_

### Acceptance-criteria evidence

- **AC1** — `_last_verified` on each of the three shipped `partly` statuses returns
  `("partial", None)`, never `ok`, with a recent ingest so staleness cannot be
  what fires; advisory message is its own string ("records only a partial
  verification"), distinct from the `never` text.
  `test_partly_verified_pages_report_partial_not_ok`,
  `test_a_partial_page_is_flagged_however_fresh_its_dates`,
  `test_a_qualifier_fused_to_its_verb_still_reads_as_partial`.
- **AC2** — the four shipped intraclass spot-check notes each resolve `never`, and
  the advisory text contains no "partial verification"; the synthetic
  `{never, partial}` pair also resolves `never`. Lattice enumerated over all 8
  subsets of `{never, partial, verified}` — matches M89-D1 exactly.
  `test_negation_beats_partiality_on_the_shipped_spot_check_notes`,
  `test_a_never_clause_beside_a_partial_clause_resolves_never`.
- **AC3** — one fixture per page: all three `partly` pages carry `not re-read
  since` in a later clause and none is reported `never`; a fully-verified page
  with the same trailing clause still resolves `ok`. A 15-status misfire sweep
  by the diff-bug reviewer found no case where a partiality word qualifying
  something else leaked across a clause boundary.
  `test_partly_verified_pages_are_not_swept_up_as_never`,
  `test_a_fully_verified_page_with_a_later_not_clause_stays_ok`.
- **AC4** — `Ingested 2026-13-45`: `_PROV_INGESTED` matches the shape,
  `_ingested_date` returns None, the CHECK FAILs naming the value
  ("ingested date 2026-13-45 is not a real date"), and the advisory prints no
  line for the page — reported by exactly one reader, by name. A valid
  leap-day date still passes, so the predicate is not over-tightened.
  `test_impossible_ingested_date_fails_by_name`,
  `test_impossible_ingested_date_is_reported_by_exactly_one_reader`,
  `test_real_ingested_date_still_passes_the_tightened_predicate`.
- **AC5** — verified mechanically, not by eye: all seven fixture strings are
  exact substrings of the live `Extraction:` lines (three pages here, four in
  intraclass at commit `dea301f`). This initially FAILED on one fixture — the
  spec-kit string dropped two of its three anchors — and was fixed on the
  branch before the tick.
- **AC6** — both templates carry the partiality set and its consequence, each
  pinned label-with-members; 5 mutation entries registered (per template, per
  test) out of a 214-entry registry, and the harness blanks each and requires
  its guard to fail. Inversion check: `partly` → `mostly` in place turned 4
  guards red. `test_each_template_names_the_partiality_set_with_its_label`,
  `test_each_template_says_a_partial_claim_is_never_cleared`,
  `test_each_taught_partiality_qualifier_classifies_as_partial`.
- **AC7** — each exit code checked separately, unpiped, from the repo root:
  `scripts/tests` 0, `skills/tests` 0, `hooks/tests` 0, `cairn_validate.py` 0.

### Consistency gate

`cairn_validate.py` (plugin copy): 15 CHECKs PASS, exit 0; advisories OK except
`references staleness` WARN (3) — the three pages this milestone exists to
surface. Profile is `generic`, whose `consistency-gate` slot names no toolchain
checks, so that half is a clean no-op. No `DESIGN.md` principle changed, so
`cairn_impact --changed` was not run. No CI is configured in this repo (no
`.github/`), so the CI wait is a genuine no-op and the three local suites are
the whole gate.

### Independent review — three lenses, then a scorer

- **[O] diff-bug (Opus):** 1 finding, scored **95**, actioned (below). Its clean
  probes: the 8-subset lattice, a 15-status `_PARTIAL` misfire sweep, state
  reachability around the `partial` early return, `_ingested_date`'s
  forward reference to `_iso`, the double-`Ingested` block, and
  no new CHECK failures.
- **[S] blame-history (Sonnet):** 0 findings. Confirmed the repurposed
  `..._not_swept_up_as_never` test still defends what it always defended (these
  pages must never land in `never`; `ok` was merely the only other state that
  existed), that the ledger edit met its deliberate-update bar, and that D-023
  is not violated — `_iso` rejects only calendar-impossible dates, never a
  valid-but-odd format.
- **[S] prior-PR-comments (Sonnet):** no prior-PR evidence — zero review
  comments across ~90 merged PRs. Clean no-op; already covered by the standing
  candidate row about this lens.
- Findings below the 80 threshold: none logged (none were produced).

**F1 (95, fixed on the branch) — `spot-checked` could not fire as a qualifier
on the phrasing the templates teach.** `spot-checked` contains `checked`, and
`_VERIFY_VERB` matches `checked against` starting inside it (the hyphen
satisfies its lookbehind), so searching `clause[:verb.start()]` cut the
qualifier in half and left `spot-`, which matches nothing.
`spot-checked against the source 2026-07-15` returned `("ok", 2026-07-15)`, and
the at-ingestion form took the block's date — a page with one passage looked at
reading as fully verified on a day nobody verified anything. Worse, both
templates had just started teaching `spot-checked` as a partial form, so an
author following the instruction would land exactly there. The T6 guard missed
it because every fixture was built as `{qualifier} verified against the
source`, which supplies an independent verb and passes on a string no author
writes. Fixed by `_qualified_partial`, which searches to `verb.end()` and
counts a match beginning at or before the verb, plus `spot[-\s]check` so the
unhyphenated spelling reads too; the guard now runs each qualifier through
three clause shapes and forbids a bare `verified` in any of them. Inversion:
reverting the predicate turns 3 scripts tests and 1 skills test red.
