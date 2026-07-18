<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M78: Source-note shape — dated observations and page provenance

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m78-source-note-shape` · https://github.com/jmgirard/cairn/pull/76   <!-- owner: implement (branch) / review (PR URL) · create -->

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
Plus a backfill of this repo's own 16 committed `references/` pages with a
`**Provenance.**` block, so cairn does not ship a rule its own repo breaks.
Each block's ingested date and ingesting milestone are derived from
`git log --diff-filter=A` for that file (`--follow` where the page was
renamed), never invented; the extraction-verified status records what the
page itself evidences, defaulting to unverified.

**Out:** content mechanization — a `check_references` that verifies a page has
a citation and provenance rather than merely existing, and the two enforcement
gaps found alongside it → M79. A synthesis-note template → candidate row. An
ingestion actor (a skill step that owns PDF → page, closing the "no skill owns
ingestion" gap) → candidate row. Citekey resolution and dependent discovery →
candidate row, against M56's standing rejection.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] `skills/shared/validation-doctrine.md` states the standing-fact vs
      dated-observation split, naming both categories with their members on
      one physical line (the M74/M76 label→SET guard shape), and binds it to
      both committed page types.
- [x] `skills/shared/templates/source-note.md` exists and carries all seven
      provenance fields — citekey, full citation, source pointer (the shelf
      PDF path, or the URL and retrieval record for a non-PDF source),
      ingested date, ingesting milestone, pagination basis (`—` where the
      source is unpaginated), extraction-verified status — plus the content
      elements at `validation-doctrine.md:76-79` and a dated `## Open
      questions` section.
- [x] The Source ingestion paragraph names the template path, so the page shape
      is reachable from the doctrine that mandates it.
- [x] A prose guard locks the doctrine rule and is registered in
      `skills/tests/test_mutation_harness.py`; blanking its block fails the
      guard.
- [x] A test runs the real field check over the **shipped**
      `skills/shared/templates/source-note.md` (not a fixture copy) and fails
      when a mandated field is removed — the M77 pairing rule.
- [x] `cairn/DESIGN.md:38`'s template inventory names the new template, and a
      repo-wide grep confirms no other inventory or count word went stale.
- [x] Verify clean per `cairn/PROFILE.md`: `python3 -m unittest discover` over
      `skills/tests`, `scripts/tests`, and `hooks/tests`, each exit 0, run from
      the repo root and not tail-piped (M56/M65).
- [x] All 16 committed pages in this repo's `cairn/references/` carry a
      `**Provenance.**` block whose ingested date and ingesting milestone
      match `git log --diff-filter=A` for that file (`--follow` where
      renamed). No date or milestone is asserted that git does not evidence,
      and a page whose extraction has not been re-read against its source
      says so.

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
- AC8 → T8

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1. Author the standing-fact vs dated-observation rule in
      `skills/shared/validation-doctrine.md`, adjacent to Source ingestion
      (`:75-82`). Both category labels and their members sit on one physical
      line so a single assert pins the mapping and a swap cannot pass (M76).
- [x] T2. Author `skills/shared/templates/source-note.md`: provenance header
      (seven fields), citation, extracted values with page/table anchors,
      verbatim-critical quotes, `## Traces to`, dated `## Open questions`.
      Model the header on intraclass's best existing pages, not invention.
- [x] T3. Point `validation-doctrine.md`'s Source ingestion paragraph at
      `skills/shared/templates/source-note.md` by path.
- [x] T4. Write `skills/tests/test_source_note_template.py` — the prose guard
      on T1's rule, plus a field check that reads the shipped template file
      itself and asserts each of the seven provenance fields.
- [x] T5. Register T4's guard blocks in `skills/tests/test_mutation_harness.py`
      (per-file registration is not per-assert — M53); confirm each registered
      block is on one physical line and re-run the skills suite after any
      rewording near it (M59/M64/M77).
- [x] T6. Update `cairn/DESIGN.md:38`'s template inventory; `git grep` the
      whole repo for other template inventories or count words, including
      `skills/tests/test_positioning_guard.py`'s hardcoded tuples — the sweep
      covers live directories, `cairn/references/` included (M48/M58).
- [x] T7. Run the three suites from the repo root, check each exit code
      explicitly before any commit; append the work-log line.
- [x] T8. Backfill the 16 pages. Derive date and milestone per file from git;
      take the source pointer from the page's own existing prose; set
      extraction status to what the page evidences — `claude-code-hooks.md`
      records a 2026-07-11 verification, the rest default to unverified.
      These pages are current knowledge under D-045: the block is *added*,
      existing text is not rewritten.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-18: created by /milestone-plan. Diagnosis from intraclass evidence — the recurring staleness is a note asserting repo state (`M65-source-notes-interval-methods.md:220-223`, F1/95 and F7/92), a literal repeat of `LESSONS.md:45` (M63) and `:48` (M64).
- 2026-07-18: implement gate — provenance takes the bold-label prose form (no frontmatter exists anywhere in `cairn/`), dated observations mark inline, and the rule binds all committed pages, not only new ones.
- 2026-07-18: AC2 amended via step-6 gate — "source PDF filename" → "source pointer (shelf PDF path, or URL + retrieval record)", pagination basis takes `—` when unpaginated. All 16 of this repo's own `references/` pages are non-PDF, so the planned field could not apply under all-pages enforcement.
- 2026-07-18: T1–T3 — doctrine rule + `Provenance.` block spec authored in `validation-doctrine.md`; Source ingestion now names the template path; `skills/shared/templates/source-note.md` shipped, modelled on `koo2016.md`/`mehta2018.md`'s existing bold-label idiom.
- 2026-07-18: T4 — the shipped-artifact field check (M77) caught a live mismatch on its first run: the template's `Pagination:` field wrapped mid-line, so the `—` option sat on the next physical line. Tightened the template's option list rather than loosening the assert.
- 2026-07-18: T5 — mutation registration hit the M59/M64 reflow trap ("found 0"): the frontmatter sentence spanned a line break. Reflowed the provenance paragraph so each registered block is one physical line. Four blocks registered; skills suite 319 tests green.
- 2026-07-18: scope amended via step-6 gate at the user's direction — the milestone shipped a rule this repo itself broke (16 pages, zero provenance blocks). Backfill pulled forward from M79 T5 as AC8/T8; status returned review → in-progress.
- 2026-07-18: T6–T7 — `DESIGN.md:38` template inventory updated (the only inventory in the repo; no test pins it, and `test_positioning_guard.py`'s hardcoded tuple is hooks-only). Three suites rc=0 from the repo root, unpiped; validate 18/18.

- 2026-07-18: T8 — 16 pages backfilled, purely additive (`git diff --numstat`: 4 added / 0 removed on every file), so D-045's added-not-rewritten discipline holds mechanically. A verification script re-derives each block from `git log --follow --diff-filter=A`: 16/16 match on citekey, ingested date and ingesting milestone; nothing asserted that git does not evidence.
- 2026-07-18: sizing tripwire WARNs at 8 ACs (>7). Accepted, not split: AC8 is a compliance backfill for the rule this milestone ships, not independent capability, and deferring it would merge a rule the repo itself breaks. Recorded rather than silently tolerated.
- 2026-07-18: known cosmetic overlap for review — on the M06 comparanda the new `Provenance.` pointer restates the URL already in the page's `Source:` line. Left as-is because collapsing them means rewriting existing text, which D-045 forbids here.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

### D-M78-1 (2026-07-18): a dated observation marks inline, not in a dedicated section

The implement gate delegated the marker form. Chosen: `— observed YYYY-MM-DD`
on the claim itself, where a reader meets it. **Rejected** a dedicated
`## Observations` section — it only catches claims whose author already
recognized them as observations, which is precisely the recognition that
failed: M65's F1 (`mehta2018.md:267-272`) and F7 (`saha2012.md:235-245`) were
both written inline, mid-argument, by an author who believed they were stating
facts. **Rejected** date-required-placement-free as giving M79 nothing to
check. **Cost:** an inline marker is easy to omit and, until M79 lands,
nothing detects the omission.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

### Acceptance-criteria evidence (2026-07-18, fresh)

- **AC1** — `validation-doctrine.md:88,89`: each definition present exactly once
  and complete on one physical line; `:86` binds both page types
  ("source note and synthesis note alike"). Falsifiability proven by live
  mutation: inverting which label owns which enumeration failed both label
  asserts (`test_standing_fact_label_carries_its_members`,
  `test_dated_observation_label_carries_its_members`); file restored byte-clean.
  This closes the M74/M76 label→SET trap for this rule.
- **AC2** — field-by-field check over the shipped template: all seven
  provenance fields present, plus all six content elements from
  `validation-doctrine.md:76-79` (dated `## Open questions`, `— observed
  YYYY-MM-DD` marker, `## Traces to`, `## Extracted values`, verbatim quoting,
  page/table anchors).
- **AC3** — `validation-doctrine.md:77` names
  `skills/shared/templates/source-note.md` inside the Source ingestion
  paragraph.
- **AC4** — `test_mutation_harness.py` 9 tests rc=0; the four M78 registrations
  each blank cleanly and fail their guard. Registry-completeness meta-test
  green (it FAILed before registration, which is how the gap was found).
- **AC5** — demonstrated by deletion, not by construction: removing the
  `Extraction:` field from the SHIPPED template failed 2 tests
  (`test_every_provenance_field_is_present` at
  `field='extraction-verified status'`, and
  `test_unverified_extraction_is_an_expressible_state`); restore returned the
  suite to rc=0 with an empty diff.
- **AC6** — `DESIGN.md:38-39` names the new template. Repo-wide sweep for
  other inventories/count words: `DESIGN.md:38` is the only one;
  `test_positioning_guard.py`'s hardcoded tuple is hooks-only, not templates.
- **AC7** — from the repo root, unpiped, exit codes read explicitly:
  skills 319 rc=0 · scripts 111 rc=0 · hooks 72 rc=0.
- **AC8** — a verification script re-derived citekey, ingested date and
  ingesting milestone for all 16 pages from
  `git log --follow --diff-filter=A`: 16/16 match, 0 problems, every block
  carrying `Pagination:` and `Extraction:`. Diff is `+64 / -0` across the 16
  files, so D-045's added-not-rewritten discipline is proven mechanically, not
  asserted. 5 pages now carry an unverified or partly-verified extraction
  status that was previously indistinguishable from a verified one.

### Consistency gate

`cairn_validate` rc=0 — 15 PASS, 3 advisory OK, and one advisory WARN:
`M78: 8 acceptance criteria (>7 tripwire)`. The WARN was raised and accepted at
implement with the rationale logged (AC8 is a compliance backfill for the rule
this milestone ships, not independent capability; deferring it would merge a
rule the repo itself breaks). Not a gate failure.
Profile is `generic` — its `consistency-gate` slot names no toolchain checks,
so that half is a clean no-op. No IP/GP line changed in the diff, so
`cairn_impact` is not run (step 4).

### Independent review — three lenses + scorer

- **[S] prior-PR-comments lens:** clean no-op. 7 PRs that previously touched
  these files examined (#31, #40, #51, #55, #56, #63, #74) — 0 inline review
  comments, 0 review bodies. A repo-wide search confirmed exactly one PR in
  cairn's history carries any comment at all (#29, dropped, unrelated
  substance). Zero findings; no lesson regressed.

- **[O] diff-bug lens (Opus)** and **[S] blame-history lens (Sonnet)**: 5
  findings, scored by a fresh **[S] scorer** that did not generate them.

**Actioned.**
- **F1 (87) — module placement violated D-031.** The two new sections were
  written into `validation-doctrine.md`, a domain-conditional module read only
  "whenever a milestone touches a numeric result or scoring/algorithmic
  content" — but the rule is universal, and this milestone proved it by
  backfilling 16 non-numeric pages in a `generic`-profile repo with no numeric
  work. The unmodified sentence directly above the insertion point states the
  same boundary. Consequence: a session editing a non-numeric references page
  would never be pointed at the anti-staleness rule — self-defeating.
  *Fixed:* both sections moved to `tracking-rules.md` "References pages" (the
  universal home D-031 designates); the module keeps a pointer. Guard and all
  four mutation registrations retargeted; a new assert locks the deferral.
- **F3 (90) — the backfill introduced the very failure this milestone stops.**
  The 16 `Extraction:` lines said "not re-read since" with no date — verbatim
  the doctrine's own dated-observation category ("what has or has not been
  read"). Re-read a page later without touching that line and it stays
  readable and becomes false: the M63/M64/M65 pattern, reintroduced by the
  compliance fix for it. *Fixed:* all 16 dated `— observed 2026-07-18`; the
  rulebook now states explicitly that an extraction status carries its own
  date; `TestBackfilledPages.test_every_extraction_status_is_dated` guards it,
  proven falsifiable by un-dating one page (fails on `page='spec-kit.md'`).
- **F2 (74) — actioned over the threshold, by operator judgment (M73).** The
  doctrine said the Provenance block "names citekey, full citation", but the
  template puts citekey in the H1 and the citation in its own block, and the
  field check matches anywhere in the file so structure went unchecked. The
  scorer correctly docked it for overstating M79's dependency; the
  contradiction is still real and M79 would inherit it. *Fixed:* the rulebook
  now describes what the block records and says the citekey and citation are
  carried by the page itself. AC2 is unaffected — it requires the template to
  carry the seven fields, not to nest them all in one block.

**Logged, not actioned (sub-threshold, surfaced per IP3).**
- **F4 (52)** — delivered extraction vocabulary ("verified at ingestion",
  "partly verified") is richer than T8's "default to unverified". Rejected:
  the plan-owned Scope says the status "records what the page itself
  evidences, defaulting to unverified", which permits evidence-based
  variation, and the granular wording is honest rather than overstated.
- **F5 (22)** — `references/INDEX.md` carries no Provenance block though the
  rule says "every committed page". Rejected: the file map governs `INDEX.md`
  as a distinct artifact (one line per page), not as a page.

**Verified clean by both lenses.** The M74/M76 label→SET trap is closed
(independently re-mutated: swapping the two labels fails both asserts). AC8's
provenance derivation re-checked against `git log --follow` — all 16 match,
additive only, D-045 holds. M56's rejections cleared: a governed template is
the opposite of the "free-form-page structural steals" it declined. M57's
INDEX rule untouched. Prior-PR lens: 0 findings from 7 PRs.

### Re-verification after fixes

skills 324 rc=0 (up from 319: 3 new asserts + the backfill guard) · scripts
111 rc=0 · hooks 72 rc=0 · `cairn_validate` rc=0 with the one accepted sizing
advisory. Both fixes proven by live mutation, each file restored byte-clean.
