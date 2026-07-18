<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M81: References staleness advisory — the provenance block gets a reader

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M80   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m81-references-staleness-advisory` · https://github.com/jmgirard/cairn/pull/79   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give the extraction-verified status and ingested date a reader, so a page that
has never been checked against its source says so out loud.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A WARN-tier advisory in `cairn_validate.py` that parses each committed
`references/` page's `**Provenance.**` block and surfaces never-verified and
long-unverified pages. The matching doctrine line in `tracking-rules.md`
"References pages". A first run over this repo's own 16 pages, with every
flagged page dispositioned.

**Lineage.** This completes an `Adopt` verdict, not a new proposal. M56
surveyed LLM Wiki's Lint op — described in `references/llm-wiki.md:49-50` as
covering "contradictions between pages, **stale claims that newer sources have
superseded**, orphan pages with no inbound links" — and its verdict cell reads
"**Adopt** — the one genuine gap." The disposition banked only the INDEX↔disk
half and M57 shipped only that; the staleness clause was inside the adopted
element and lost in scoping. This milestone executes the remainder, so it does
**not** need to supersede M56's query-op or graph-tooling rejections.

**Out:**
- A hard-FAIL `CHECKS` entry → **refused** at the plan gate under D-029
  ("never a validate gate"), whose reasoning M79-D1's structural-vs-judgment
  test confirms: block *presence* is structural, "this page is too old" is a
  judgment about evidence quality.
- A central ledger, registry file, or `references/log.md` → **refused**;
  rejected independently by M56 ("a second log is a divergence vector") and
  D-029 (no central file). The record marks inline in the existing provenance
  block, per D-M78-1.
- Query op, graph tooling, citekey traversal → the existing ROADMAP candidate
  row; still blocked on an M56 supersession.
- The authoring trigger and synthesis template → M80.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: a new advisory is registered in `ADVISORIES` (`cairn_validate.py:797-806`)
      and never in `CHECKS`; `cairn_validate`'s exit code is unchanged when it
      fires. It flags (i) a page whose extraction status records no verified
      re-check and (ii) a page whose last verified re-check predates the
      threshold this milestone states. Fixtures prove both flags fire and that
      a recently verified page is not flagged.
- [x] AC2: the parser's fixtures vary decoration, phrasing, and layout
      *independently* — including a label alone on its line and a decoy
      `## Provenance` heading — and no page the shipped templates sanction is
      falsely flagged (D-023; LESSONS `:24`, where varying one axis alone
      passed vacuously on the others).
- [x] AC3: `tracking-rules.md` "References pages" states the re-verification
      expectation and that a re-check marks inline in the provenance block,
      never in a new file or section; guard-locked and mutation-registered.
- [x] AC4: a milestone-local decision records WARN-tier severity with its
      reasoning against D-029 and M79-D1 — recorded milestone-locally because
      both precedents it argues from are themselves milestone-local
      (LESSONS `:47`).
- [x] AC5: the advisory is run over this repo's 16 committed pages; its output
      is recorded in this file and every flagged page carries a stated
      disposition — re-verified here, or a named ROADMAP candidate row. The
      milestone runs its own new rule over its own artifacts (LESSONS `:48`).
- [x] AC6: verify clean — `python3 -m unittest discover` for `skills/tests`,
      `scripts/tests`, `hooks/tests` each exit 0, checked individually and
      never through a pipe (LESSONS `:23`); `cairn_validate` exit 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence. -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Write the advisory function in `scripts/cairn_validate.py` beside
      `check_worklog_format` (`:663`) and register it in `ADVISORIES`. It reads
      the `Extraction:` line — today parsed by nothing; the word appears once
      in the file, inside a comment describing a tolerated miss (`:223-225`) —
      and the ingested date `_PROV_INGESTED` (`:227`) already captures into
      group 1 and discards. **The threshold value is the one open decision;
      confirm it at the implement gate before writing the comparison.**
- [x] T2: Fixtures in `scripts/tests/test_scripts.py` covering both flags, the
      clean case, and the three variation axes. Extend the shared `Tree.build()`
      fixture if the advisory needs pages present (LESSONS `:15`).
- [x] T3: Add the doctrine line to `tracking-rules.md` "References pages"; guard
      it in `skills/tests/test_references_pages.py` and register the anchor in
      the mutation harness, on its own physical line (LESSONS `:27`).
- [x] T4: Record the milestone-local decision in `## Decisions` below.
- [x] T5: Run the advisory over `cairn/references/`; record the output summary
      (counts, not pasted output) and one disposition line per flagged page.
- [x] T6: Run the three suites and `cairn_validate`, checking each exit code
      individually.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-18: created by /milestone-plan; planned alongside M80 from the M78/M79 grouped candidate row.
- 2026-07-18: implement gate settled the three open parse decisions — 180-day threshold, undated "at ingestion" ages from the ingested date, exemption earned by the explicit "nothing to re-verify" phrase.
- 2026-07-18: review — 3 lenses + scorer; 2 findings ≥80 both fixed on the branch (F1/93 the widened continuation test erased M79 CHECK failures — widening made advisory-only; F2/87 a wrapped status invented staleness — status now read to end of paragraph), 4 regression tests added, suites 343/147/72 all exit 0.
- 2026-07-18: review — F3/68, F4/63, F5/62 logged not actioned (IP3), grouped into one ROADMAP candidate row; all six acceptance criteria ticked against recorded evidence.
- 2026-07-18: T6 — skills 343, scripts 143, hooks 72 tests, each run unpiped with its exit code read individually: all 0; `cairn_validate` exit 0 with 1 advisory warning. Status → review.
- 2026-07-18: T5 — first run over the repo's 16 pages: 13 ok, 2 exempt, 1 flagged (`task-master.md` → new ROADMAP candidate row); `migration-pilot-notes.md`'s status aligned to the sanctioned exemption phrase, heading off a false positive scheduled for ~174 days out.
- 2026-07-18: T5 — the run's new sections put the file 11 lines over cap; Decisions and the run summary compressed in one pass (cross-referencing `_last_verified`'s docstring and the ROADMAP row rather than restating them). Plan-owned sections untouched.
- 2026-07-18: T4 — M81-D1 (WARN-tier severity, argued against D-029 + M79-D1) and M81-D2 (the three gate-settled parse decisions) recorded milestone-locally.
- 2026-07-18: T3 — "Re-verification." paragraph added to tracking-rules "References pages"; 6 guards in `TestReVerification` and both anchors mutation-registered, each on its own physical line.
- 2026-07-18: T2 — 15 fixtures + a 36-cell decoration×layout×phrasing cross-product; it caught a real false positive (a label-alone `Extraction:` reported as no status at all), fixed by adding the extraction field to `_provenance_block`'s continuation test. Fixture dates are relative to today, never literal, so the suite cannot rot past the threshold.
- 2026-07-18: T1 — `check_references_staleness` written and registered in `ADVISORIES`; stdlib allowlist extended for `datetime`; first run flags 1 of 16 pages, exit 0.

## First run over this repo (T5, 2026-07-18)

16 committed pages: **13 ok** (last verified 2026-07-11 → 2026-07-18, none past
the 180-day threshold), **2 exempt** (nothing to re-verify against), **1
flagged**. `cairn_validate` exit 0. Dispositions:

- `task-master.md` — flagged, never verified: an [S] subagent study with no
  claim checked against the source. Re-reading the source is not this
  milestone's work → **ROADMAP candidate row**, added 2026-07-18.
- `migration-pilot-notes.md` — not flagged today, but a scheduled false
  positive: a first-hand record carrying no exemption phrase, so it would have
  aged from its ingested date and flagged in ~174 days. Wording aligned in
  place to the template's sanctioned "nothing to re-verify against"; the claim
  is unchanged, so this is phrasing, not a D-045 correction.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

**M81-D1 (2026-07-18): the staleness reader is a WARN-tier advisory, never a
`CHECKS` entry.** D-029 rules that judgment "is never a validate gate";
M79-D1's structural-vs-judgment test says which side this falls on. Block
*presence* is structural — a page carries a `**Provenance.**` block or it does
not — which is why M79 made that a hard CHECK. "Not re-read in 180 days" is a
judgment about evidence quality: the page may be correct, the source may not
have moved, and a FAIL would block an unrelated milestone's merge over a
reference page's age — the cry-wolf failure D-023 and D-029 both guard
against. Milestone-local rather than a D-entry because both precedents it
argues from are themselves milestone-local (LESSONS `:47`).

**M81-D2 (2026-07-18): the three parse decisions, settled at the implement
gate.** (i) 180-day threshold. (ii) A status naming no date of its own
("verified at ingestion", the commonest shipped form) ages from the block's
ingested date, which that wording literally names — demanding an explicit
date would falsely flag five template-sanctioned pages (D-023). (iii) A
first-hand record is exempt by *saying* "nothing to re-verify against", never
by page type: a derived synthesis note does age. The reasoning is carried
where it acts — `_last_verified`'s docstring — and the rulebook's
"Re-verification" paragraph states (i)–(iii) for readers.

## Review
<!-- owner: review · exclusive; EXEMPT from the 150-line cap (M55). -->

**Reviewed 2026-07-18 · PR #79 · branch `m81-references-staleness-advisory`
(8 commits, 8 files, +578/−14).** `main` was in sync with origin and had not
moved under the branch; no merge was needed before gathering evidence.

### Acceptance-criteria evidence (fresh, by command)

- **AC1 — registered in `ADVISORIES`, never `CHECKS`; exit unchanged; both
  flags fire.** Introspected the shipped module: `references staleness` is in
  `ADVISORIES` = True, in `CHECKS` = False, `_STALE_DAYS` = 180. Run over this
  repo it emits 1 WARN and exits **0** — the advisory fires without moving the
  exit code. Both flags proven by fixture:
  `test_never_verified_page_is_flagged` (flag i) and
  `test_long_unverified_page_is_flagged` (flag ii), with
  `test_recently_verified_page_is_not_flagged` and
  `test_page_just_inside_the_threshold_is_not_flagged` proving a fresh page
  stays quiet. 15 tests in `TestReferencesStaleness`, exit 0.
- **AC2 — axes varied independently; no sanctioned page falsely flagged.**
  `test_decoration_layout_and_phrasing_vary_independently` crosses 4
  decorations × 3 layouts × 3 phrasings = **36 cells** (verified non-vacuous:
  the 12 deco×layout combinations render 12 *distinct* pages). Includes the
  label-alone layout and the decoy `## Provenance` heading, the latter with
  both halves — it must not swallow a real block
  (`test_decoy_provenance_heading_does_not_swallow_the_block`) and must not
  manufacture one (`test_decoy_heading_over_a_fresh_page_stays_quiet`).
  `test_no_shipped_template_status_is_falsely_flagged` reads the **real**
  shipped templates (M77 pairing), extracts every `|`-separated sanctioned
  alternative, and asserts none is falsely flagged — with a floor assert so a
  failed parse cannot make the subTests vacuous.
- **AC3 — doctrine stated, guard-locked, mutation-registered.** The
  "Re-verification." paragraph is in `tracking-rules.md` "References pages"; 6
  guards in `TestReVerification` pass. Mutation coverage proven **directly**,
  not by eye: blanking each registered anchor makes its guard fail (both
  returned True from `mutation_engine.guard_fails_when_blanked`). Each anchor
  verified to sit on exactly one physical line.
- **AC4 — WARN-tier severity recorded milestone-locally.** M81-D1 (`:141`)
  argues the severity against D-029 and M79-D1's structural-vs-judgment test
  and states why it is milestone-local; M81-D2 (`:152`) records the three
  gate-settled parse decisions.
- **AC5 — first run recorded, every flagged page dispositioned.** Re-run at
  review: 16 pages → **13 ok, 2 exempt, 1 flagged**, findings list containing
  exactly `task-master.md`. Recorded in "First run over this repo" (`:123`)
  with a disposition line per page; the `task-master.md` ROADMAP candidate row
  is present (1 match).
- **AC6 — verify clean, each exit code read individually, never through a
  pipe.** skills 343 tests exit 0 · scripts 143 exit 0 · hooks 72 exit 0 ·
  `cairn_validate` exit 0. Re-run a second time at gate time from the repo
  root after a stray `cd` was caught mid-review (LESSONS `:23` live again).

### Consistency gate

Universal cairn-file checks: the plugin's `cairn_validate` exits **0** — 15
PASS, 4 OK, 1 WARN (`references staleness`, the milestone's own advisory
reporting `task-master.md`). `DESIGN.md` is untouched by the diff, so no
principle changed → `cairn_impact` correctly skipped. Toolchain checks: the
`generic` profile's `consistency-gate` slot names none — a clean no-op.

**CI:** this repo configures no workflows (`.github/workflows/` absent), so
`gh pr checks` reports none and the local suites above are the verification of
record. Noted rather than waited on.

### Independent fresh-context review (3 lenses + scorer)

- **[S] prior-PR-comments — 0 findings.** Established that this repo carries
  *no* inline PR review comments at all (`pulls/{78,77,76,55,54,51}/comments`
  each returned `[]`); its review record lives in the archive files' Review
  sections and `LESSONS.md`, which it used as the prior-review base.
- **[S] blame-history — 0 findings.** Verified the M56 "second log is a
  divergence vector" citation is verbatim-accurate, and that the
  `migration-pilot-notes.md` edit is a template-vocabulary retrofit rather
  than a D-045 correction. Corrected a provenance detail: `_provenance_block`
  is **M79's** (`8d4fd8e`), not M78's — M78 defined only the block schema.
- **[O] diff-bug — 2 findings, both actioned.** Both reproduced independently
  by the scorer before triage.

**F1 (93) — FIXED.** *Widening `_provenance_block`'s continuation test
silently weakens M79's hard `references index<->disk` CHECK.* The docstring's
claim ("no page that passed before can fail now") was true but the **wrong
invariant**: that CHECK asks only existence questions, so a wider block cannot
create a FAIL — it **erases** FAILs. A page whose provenance names no source
pointer passed once the following `**Citation.**` paragraph was absorbed,
because `_PROV_LOCATOR`'s `[\w.-]+/[\w.-]` arm matches the `volume/issue/pages`
the shipped source-note template itself prints. Three reviewers and the
implementing session all verified the *stated* invariant and missed the one
that mattered. Fixed by making the widening opt-in
(`_provenance_block(..., for_extraction=True)`): the hard CHECK keeps M79's
two-field test untouched, and only the advisory passes the flag. The root
cause of the blind spot is locked too — the `page()` fixture always put the
provenance block last, so no test in the class had a trailing paragraph to
absorb; two regression tests now supply one, one per erasable arm.

**F2 (87) — FIXED.** *`_extraction_status` "never invents staleness" was
false; it invents staleness on exactly the pages that were re-verified.*
Reading only the line the status starts on lost a wrapped continuation and
fell back to the **ingested** date, which for a re-verified page is older than
the verification — a page re-read 17 days ago reported as 929 days stale, a
D-023 false positive rather than the claimed preferred miss. The `wrapped`
axis in the 36-cell cross-product could not catch it: the split point put the
date before the cut in all three phrasings, so the axis was exercised but
never where wrapping changes the answer. Fixed by reading the status to the
end of its **paragraph**, stopping at a blank line or the next
`Label:`/bolded field so it cannot swallow the citation below it. Both
directions are now tested.

Both fixes verified against the reviewers' own counterexamples, and proven
non-vacuous: the CHECK's narrowed block finds no source pointer where the
wide one does. The repo's 16 pages classify identically before and after
(13 ok / 2 exempt / 1 flagged) — no real page's outcome changed.

**Logged, below the 80 threshold — surfaced, not actioned (IP3):**

- **F3 (68)** — `_UNVERIFIED` is tested before any date, so a partly-verified
  status that happens to contain the word ("verified 2026-07-15 …; the
  appendix remains unverified") reports "no verified re-check". Dormant: all
  three real partly-verified pages avoid the token. Not actioned because the
  reordering that fixes it re-opens the opposite misread ("unverified — first
  pass 2026-01-01" would then read as verified).
- **F4 (63)** — synonyms escape the flag: "never verified against the source"
  classifies `ok`. A false negative (D-023's preferred direction), and
  widening risks flagging partial-verification prose wholesale.
- **F5 (62)** — a future date ("verified 2099-01-01") yields a negative age
  and permanently exempts a page with no diagnostic. Narrow, and no other
  date field in the codebase is sanity-checked against today either.

F3–F5 share one shape — the parser trusting free prose further than the
templates sanction — and are carried as a single ROADMAP candidate row rather
than three.
