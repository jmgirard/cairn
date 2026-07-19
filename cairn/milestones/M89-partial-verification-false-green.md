<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M89: Partial verification is a state — the staleness advisory stops failing toward green

- **Status:** in-progress
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

- [ ] A status whose verification verb carries a partiality qualifier in its own
      clause resolves to a new `partial` state, never `ok`; the advisory WARNs
      naming the page as only partly checked, distinct from the `never` message.
- [ ] Negation still beats partiality: a negated verb in a clause that also
      carries a partiality qualifier resolves `never`, not `partial`.
- [ ] The M79-F5 trap is not reintroduced — the shipped pages carrying
      `not re-read since` in a *later* clause are not swept up by the new
      qualifier search, proven by a fixture per page.
- [ ] A provenance block whose ingested date matches `_PROV_INGESTED` but yields
      no parseable ISO date is reported by exactly one of the gate or the
      advisory, and by name — never silently skipped by both.
- [ ] Every new fixture is built from wording that shipped: the four intraclass
      note statuses and this repo's three `partly` pages, quoted as-is.
- [ ] `source-note.md` and `synthesis-note.md` teach the partial form in their
      verb-set comments, and each new prose guard is mutation-registered.
- [ ] Profile `verify` clean: `python3 -m unittest discover -s scripts/tests`,
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
- [ ] T8 — Re-run the advisory over this repo, report the count delta, and
      resolve any page the fix newly surfaces (D-045: corrected in place).

## Work log

- 2026-07-19: created by /milestone-plan; both defects found live in the intraclass session, with partial-state semantics, defect-B inclusion, and the evidence bar set at the question gate.
- 2026-07-19: implement gate settled three open choices — the never > partial > verified lattice ({never, verified} stays ambiguous), a tight qualifier set (partly | partially | in part | spot-check(ed)), and defect B fixed by tightening the CHECK behind a shared `_ingested_date` predicate.
- 2026-07-19: T2–T5 — `_PARTIAL` qualifier + `_resolve_claims` lattice + a `partial` advisory branch + one shared `_ingested_date` predicate behind both readers; all three verify suites green, validate exit 0.
- 2026-07-19: T1 — 10 regression fixtures red across both defects; the four intraclass note statuses (donner2002, konishi1989, naik2007, young1998, commit dea301f) and this repo's three `partly` pages quoted as shipped.

- 2026-07-19: T6–T7 — both templates teach the partiality set and its no-date-clears-it consequence; three new guards, five mutation entries (per template, per test), and an inversion check (`partly` → `mostly` in place) turned 4 guards red before restore.

## Decisions

## Review
