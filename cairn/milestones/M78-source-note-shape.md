<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M78: Source-note shape — dated observations and page provenance

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give `cairn/references/` pages an authored shape — page provenance plus dated
observations in place of standing claims about the repo's own state — so a
page carries its own age instead of aging silently.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a doctrine rule in `skills/shared/validation-doctrine.md` splitting a
references page's claims into **standing facts** (claims about the *source* —
values, formulas, page anchors) and **dated observations** (claims about the
*repo's own state* — "not present on the shelf", "not yet checked", "verify
when X is written"), which carry `— observed YYYY-MM-DD` and are never
recorded as standing fact. The rule binds both committed page types. Plus
`skills/shared/templates/source-note.md` instantiating it: the seven-field
provenance header, the content sections already mandated at
`validation-doctrine.md:76-79`, and a dated `## Open questions` shape. Plus
guards, mutation registration, and the `DESIGN.md:38` template inventory.

**Out:** content mechanization — a `check_references` that verifies a page has
a citation and provenance rather than merely existing, and the two enforcement
gaps found alongside it → M79. A synthesis-note template → candidate row. An
ingestion actor (a skill step that owns PDF → page, closing the "no skill owns
ingestion" gap) → candidate row. Citekey resolution and dependent discovery →
candidate row, against M56's standing rejection.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `skills/shared/validation-doctrine.md` states the standing-fact vs
      dated-observation split, naming both categories with their members on
      one physical line (the M74/M76 label→SET guard shape), and binds it to
      both committed page types.
- [ ] `skills/shared/templates/source-note.md` exists and carries all seven
      provenance fields — citekey, full citation, source PDF filename,
      ingested date, ingesting milestone, pagination basis, extraction-verified
      status — plus the content elements at `validation-doctrine.md:76-79` and
      a dated `## Open questions` section.
- [ ] The Source ingestion paragraph names the template path, so the page shape
      is reachable from the doctrine that mandates it.
- [ ] A prose guard locks the doctrine rule and is registered in
      `skills/tests/test_mutation_harness.py`; blanking its block fails the
      guard.
- [ ] A test runs the real field check over the **shipped**
      `skills/shared/templates/source-note.md` (not a fixture copy) and fails
      when a mandated field is removed — the M77 pairing rule.
- [ ] `cairn/DESIGN.md:38`'s template inventory names the new template, and a
      repo-wide grep confirms no other inventory or count word went stale.
- [ ] Verify clean per `cairn/PROFILE.md`: `python3 -m unittest discover` over
      `skills/tests`, `scripts/tests`, and `hooks/tests`, each exit 0, run from
      the repo root and not tail-piped (M56/M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4, T5
- AC5 → T4
- AC6 → T6
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [ ] T1. Author the standing-fact vs dated-observation rule in
      `skills/shared/validation-doctrine.md`, adjacent to Source ingestion
      (`:75-82`). Both category labels and their members sit on one physical
      line so a single assert pins the mapping and a swap cannot pass (M76).
- [ ] T2. Author `skills/shared/templates/source-note.md`: provenance header
      (seven fields), citation, extracted values with page/table anchors,
      verbatim-critical quotes, `## Traces to`, dated `## Open questions`.
      Model the header on intraclass's best existing pages, not invention.
- [ ] T3. Point `validation-doctrine.md`'s Source ingestion paragraph at
      `skills/shared/templates/source-note.md` by path.
- [ ] T4. Write `skills/tests/test_source_note_template.py` — the prose guard
      on T1's rule, plus a field check that reads the shipped template file
      itself and asserts each of the seven provenance fields.
- [ ] T5. Register T4's guard blocks in `skills/tests/test_mutation_harness.py`
      (per-file registration is not per-assert — M53); confirm each registered
      block is on one physical line and re-run the skills suite after any
      rewording near it (M59/M64/M77).
- [ ] T6. Update `cairn/DESIGN.md:38`'s template inventory; `git grep` the
      whole repo for other template inventories or count words, including
      `skills/tests/test_positioning_guard.py`'s hardcoded tuples — the sweep
      covers live directories, `cairn/references/` included (M48/M58).
- [ ] T7. Run the three suites from the repo root, check each exit code
      explicitly before any commit; append the work-log line.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-18: created by /milestone-plan. Diagnosis from intraclass evidence — the recurring staleness is a note asserting repo state (`M65-source-notes-interval-methods.md:220-223`, F1/95 and F7/92), a literal repeat of `LESSONS.md:45` (M63) and `:48` (M64).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
