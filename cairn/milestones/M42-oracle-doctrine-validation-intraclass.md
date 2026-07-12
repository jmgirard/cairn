<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M42: Oracle-doctrine validation against intraclass

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M41   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m42-oracle-doctrine-validation-intraclass · https://github.com/jmgirard/cairn/pull/40   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Validate cairn's D-024 oracle-type doctrine and the two deferred oracle candidates
against intraclass's real oracle system — the practice cairn's doctrine descends
from — recording fit findings that sharpen (but do not yet build) the registry.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** classify intraclass's 34 `data-raw/oracle-*.R` scripts + `PRINCIPLES.md` #1
against cairn's D-024 doctrine (frozen/live/invariant/closed-form vocabulary, the
≥2-independent-types bar, the reproducibility hard-stop); assess whether the two
deferred candidates — the `ORACLES.md` registry and the R-provenance guard — fit
intraclass's actual practice; record the assessment in a cairn reference file and
sharpen the two candidate rows with the evidence; fix in cairn any concrete defect
the assessment exposes in the Validation-doctrine text (guard-tested).

**Out:** building `ORACLES.md` as a cairn tracking file (the deferred candidate,
entangled with toolchain-profiles — this milestone informs it, does not build it);
building the R-provenance guard test (the deferred R-profile-slot candidate); any
change to the intraclass repo (read-only assessment); promoting either candidate
to a `planned` milestone (that is a later plan-gate decision, fed by these findings).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: Every `data-raw/oracle-*.R` script in intraclass is classified into one
      of cairn's four oracle types (frozen/live/invariant/closed-form) in a table in
      the findings file, with a per-type count; any script fitting no type is flagged
      as a doctrine gap. (Evidence: the findings table + the script list it covers.)
- [x] AC2: intraclass `PRINCIPLES.md` #1 (≥2 independent oracle types) is compared
      against cairn's D-024 ≥2-types bar, with an explicit agree/diverge verdict
      citing `PRINCIPLES.md` #1 and the tracking-rules "Validation doctrine" section.
- [x] AC3: Each of the two deferred candidates (ORACLES.md registry; R-provenance
      guard) is assessed for fit against intraclass's real system with a
      keep-deferred / revise / promote verdict, and its ROADMAP candidate row is
      updated to cite this evidence. (Evidence: the diff of the two candidate rows +
      the findings section.)
- [x] AC4: Any concrete defect the assessment exposes in cairn's Validation-doctrine
      text (D-024) is fixed this milestone with a `test_oracle_doctrine.py` update
      that fails before the fix; if none is found, that null result is recorded in
      the findings file.
- [x] AC5: cairn's own guard-test suite passes
      (`python3 -m unittest discover -s scripts/tests` and the `skills/tests`
      suite). (R gates are waived here — cairn is a plugin, not an R package.)

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Read intraclass's 34 `data-raw/oracle-*.R` scripts (+ the `tests/testthat`
      oracle tests that assert against them) and record what each oracle actually is
      — its source and how it is reproduced.
- [x] T2: Classify each script against the four cairn oracle types in a table with
      per-type counts; flag any that fit no type; compare intraclass `PRINCIPLES.md`
      #1 to cairn's ≥2-types bar with an agree/diverge verdict. Write both into a new
      `references/oracle-doctrine-intraclass-notes.md` (declares its own scope).
- [x] T3: Assess the two deferred candidates against the real system — does the
      `ORACLES.md` registry shape (ID, type, asserting test:line, source, provenance)
      match intraclass's oracles; does the `provenance`-attr + guard-test convention
      match intraclass's fixture practice — with a keep-deferred/revise/promote
      verdict each; update the two ROADMAP candidate rows to cite the findings.
- [x] T4: Fix any concrete Validation-doctrine defect the assessment exposes (with a
      `test_oracle_doctrine.py` update that fails first); if none, record the null
      result; run the cairn guard-test suites green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (oracle-doctrine reality-check; depends on M41 per user's follow-on choice).
- 2026-07-12: T1+T2 — read all 34 intraclass oracle scripts + test consumption; wrote references/oracle-doctrine-intraclass-notes.md. Finding: 31/34 use simulation-coverage (SC), an oracle mapping to NONE of cairn's four types (defining oracle for 21). PRINCIPLES.md #1 AGREES on the ≥2-types bar, DIVERGES on taxonomy (its cat (c) = SC, unnamed by cairn). intraclass's frozen-when-expensive / live-when-cheap split corroborates D-024.
- 2026-07-12: T3 — both deferred candidate rows → REVISE/keep-deferred. Registry: shape matches + earns keep at scale, but intraclass proves a distributed shape and it's downstream of the taxonomy fix. R-provenance guard: content corroborated, but mechanism varies across the two exemplars (attr+guard vs. embedded-fields-no-guard) → mandate content, leave shape to the repo.
- 2026-07-12: T4 — defect confirmed (not null). User chose fix framing at the implement gate: add simulation-coverage as the 5th oracle type (D-025). Updated test_oracle_doctrine.py to assert the 5th type (confirmed failing pre-fix), added it to the Validation doctrine (priority item (5) + type paragraph), added D-025. Both guard suites green (94→95 skills + 53 scripts); cairn_validate all-pass.
- 2026-07-12: review — all 5 ACs verified fresh + ticked; consistency gate pass (R gates waived, no DESIGN principle text changed). PR #40 (no CI on repo). 3-lens review: blame-history + prior-PR 0 findings; diff-bug found 1 (count summary vs. table mismatch, leaked into D-025) — verified by recount (95), fixed (any-use IN 16/CF 6; dropped subjective defining tally; reworded D-025). Gap claim unaffected.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

_Reviewed 2026-07-12 on branch `m42-…`; PR #40._

**Acceptance criteria (fresh evidence).**

- AC1 ✓ — `references/oracle-doctrine-intraclass-notes.md` classifies all **34**
  scripts in a table (34 data rows verified); per-mechanism counts recorded
  (SC 31, FZ 24, LV 16, IN 15, CF 7); 21 scripts whose defining oracle is
  simulation-coverage are flagged as fitting none of the four types (the gap).
- AC2 ✓ — the T2/AC2 section states an explicit **AGREE on the bar, DIVERGE on
  the taxonomy** verdict, citing intraclass `PRINCIPLES.md #1` and cairn's
  `tracking-rules.md` "Validation doctrine"/D-024 ≥2-types bar.
- AC3 ✓ — both candidates assessed → **REVISE/keep-deferred**; both ROADMAP rows
  carry the "M42 verdict: REVISE" text and cite `oracle-doctrine-intraclass-notes.md`
  (grep: 2 rows each).
- AC4 ✓ — defect **confirmed, not null**; fixed via D-025 (fifth type
  `simulation-coverage`) with `test_oracle_doctrine.py` updated to assert it —
  demonstrated failing against the pre-fix doctrine (`'**simulation-coverage**'
  not found`) during implement, passing after the doctrine edit.
- AC5 ✓ — `python3 -m unittest discover -s skills/tests` → 95 OK;
  `… -s scripts/tests` → 53 OK.

**Consistency gate.**

- `cairn_validate.py` → exit 0, all checks pass.
- Coverage completeness ✓ — AC1→T1,T2 · AC2→T2 · AC3→T3 · AC4→T4 · AC5→T4;
  every AC maps to ≥1 existing task.
- Principle-impact report — skipped: M42 touches GP4 conceptually but **changed
  no `DESIGN.md` principle text** (diff touches no `DESIGN.md`), so no Sync
  Impact Report is due.
- R gates (`document()`, README knit, pkgdown, NEWS, `.Rbuildignore`) — **waived**:
  cairn is a plugin, not an R package (CLAUDE.md); no new top-level files (the new
  file is under `cairn/references/`).

**Independent review (three lenses + scorer).** Three fresh-context reviewers,
ref-based git only.

- **[O] diff-bug (Opus):** 1 finding. Spot-checked the findings file's claims
  about intraclass (34 scripts, no `ORACLES.md`, 24 fixtures, `PRINCIPLES.md`
  #1(a)/(b)/(c) + #4, line citations) — all accurate; doctrine change internally
  coherent; guard test non-fragile (asserted phrases on single physical lines);
  D-025 accurate. **Finding (score 95, CONFIRMED by my own recount → fixed):**
  the findings file's per-type count summary contradicted its own table — any-use
  IN/CF were off by one (prose 15/7 vs. table 16/6) and the precise "defining
  oracle: SC 21/IN 5/LV 5/CF 3" line didn't match the table's bold markers and
  had leaked into D-025. Fixed: any-use corrected to IN 16 / CF 6 (SC 31, FZ 24,
  LV 16 were right); the subjective per-type *defining* tally dropped for a robust
  claim (SC used by 31/34, leads all 20 Bayesian CI oracles; only 3 scripts use no
  SC); the D-025 echo reworded. The load-bearing gap claim (31/34 use SC, an
  oracle cairn's four types don't name) was verified independently correct — the
  decision to add the fifth type stands.
- **[S] blame-history (Sonnet):** 0 findings. Confirmed the change is a strict
  superset — all four prior guard phrases retained, D-024's taxonomy intact,
  D-025 correctly additive/annotating (not a supersede).
- **[S] prior-PR-comments (Sonnet):** 0 findings — no prior-PR evidence (this
  repo reviews in-session, not via GitHub PR comments); clean no-op as designed.

Scorer: the single finding is an objectively checkable count error, verified by
direct recount rather than a confidence estimate (95, well above the 80 gate);
actioned = fixed this review. No sub-threshold findings to log.
