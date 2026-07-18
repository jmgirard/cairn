<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M79: References content check — the lint stops being a filename census

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M78   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create/amend-via-gate -->

Make `check_references` verify that a committed references page carries
provenance and a citation, and close the two enforcement gaps that let pages
escape the check entirely.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `cairn_validate.check_references` (`cairn_validate.py:177-202`) gains
content checks over M78's shipped shape — a page must carry a citation line
and an ingested-date provenance field. Plus the two gaps found in the M78
audit: the flat `os.listdir` at `:189`, which makes any nesting under
`references/` silently unenforced, and the outright PASS at `:185-186` when
`INDEX.md` is absent. Advisory-vs-hard placement is decided in T1 against
D-023's no-false-positive doctrine and D-029's precedent that the oracle
registry stays review-judgment, never a CHECK.

**Out:** citekey resolution and dependent discovery — un-excluding
`references/` from `cairn_impact.py:45` so a corrected page surfaces its
consumers → candidate row, blocked on M56's standing rejection of "a formal
query op" and "graph tooling". Re-verification scheduling (a page declaring
when it was last checked against its PDF) → candidate row. Any change to the
doctrine or template shape → M78 owns those.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `check_references` reports a committed `references/` page that carries
      no citation line and one that carries no ingested-date field, at the
      severity T1 selects, with the emitted label used verbatim in any prose
      that names it (M64).
- [ ] The check reads `references/` recursively, so a page in a subdirectory
      is enforced exactly as a top-level page is — proven by a fixture with a
      nested page that currently passes and must not.
- [ ] A `references/` directory holding committed pages but no `INDEX.md` no
      longer renders PASS from this check.
- [ ] The parser tolerates cosmetic decoration on every semantic token it
      reads — backticks, markdown links, bold — pinned by fixtures for the
      decorated variants, not only the bare format (M57 / D-023).
- [ ] Every existing page in this repo's own `cairn/references/` passes the
      new check, or is corrected in place under D-045 with the correction
      marked; no page is grandfathered silently.
- [ ] `scripts/tests/test_scripts.py`'s shared `Tree.build()` fixture is
      extended so the stricter check does not fail unrelated validate tests
      (M24), and the full suite is green.
- [ ] Verify clean per `cairn/PROFILE.md`: `python3 -m unittest discover` over
      `skills/tests`, `scripts/tests`, and `hooks/tests`, each exit 0, run from
      the repo root and not tail-piped (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T3
- AC4 → T2, T4
- AC5 → T5
- AC6 → T4
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1. Decide hard-CHECK vs ADVISORY for the content conditions and record
      it as a milestone-local decision: D-023 tolerates a miss over a false
      positive, and D-029 kept the oracle registry out of the validator
      entirely. Human-authored markdown argues advisory; the shipped M78
      template argues enforceable. (RB tripwire: ip-touching — the answer sets
      whether a repo can be blocked by its own reference prose.)
- [ ] T2. Implement the citation and ingested-date content checks against
      M78's template shape, decoration-tolerant per D-023.
- [ ] T3. Replace the flat `os.listdir` (`cairn_validate.py:189`) with a
      recursive walk, and remove the absent-`INDEX.md` PASS (`:185-186`) —
      keeping the M45 no-op only where it is genuinely a not-adopted signal.
- [ ] T4. Extend `scripts/tests/test_scripts.py`: fixtures for the nested
      page, the missing-INDEX directory, the decorated variants, and each new
      failing condition. Extend the shared `Tree.build()` fixture first (M24).
- [ ] T5. Run the new check over this repo's real `cairn/references/` pages;
      correct any failing page in place with the correction marked (D-045).
- [ ] T6. Run the three suites from the repo root, check each exit code
      explicitly before any commit; append the work-log line.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-18: created by /milestone-plan. Gaps sourced from the M78-planning audit of `cairn_validate.py:177-202` — the check is a filename census, so an empty page with an INDEX line passes clean.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
