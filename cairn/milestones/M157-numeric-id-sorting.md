<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M157: Milestone IDs sort numerically — three-digit padding, numeric resolution

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m157-numeric-id-sorting · https://github.com/jmgirard/cairn/pull/158   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Milestone filenames sort in id order: the rulebook pads IDs to three digits,
the scripts resolve id spellings numerically, and this repo's 99 two-digit
archive files are renamed once. User-facing tier: the rulebook, scripts, and
README ship to adopting repos.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the tracking-rules ID-format rule (three-digit padding, numeric
equivalence for other widths, one-commit re-pad at M999 overflow); numeric id
canonicalization in the scripts' three ID surfaces; placeholder/branch-shape
sweep (`M<NN>`→`M<NNN>`, `m<nn>`→`m<nnn>`) across skills/, README.md, hooks/,
scripts/; one-time `git mv` of M01–M99 archive files to M001–M099 with
current-knowledge path cites updated.

**Out:** RB/RR review files stay two-digit (user's explicit choice — 13 files
at ~1 per 3 weeks; no follow-up row). One-digit id spellings stay outside the
resolved domain (D-023; they never occur in cairn's format). History prose is
never rewritten (IP4): D-051's body cite of `archive/M53-prose-guard-mutation-harness.md:17`
dangles permanently and is logged in T4, not repaired. Two-digit example
numbers in teaching prose are modernized best-effort in T3 with no
acceptance-criterion claim over them.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: The Milestone IDs rule in `skills/shared/tracking-rules.md` states
      that IDs are zero-padded to three digits (`M001`), that spellings of the
      same number at other zero-pad widths resolve to the same milestone, that
      milestone filename prefixes carry the padded form, and that a repo
      passing M999 re-pads filenames in one hygiene commit; a
      whitespace-normalized sweep of `skills/` and `README.md` finds no
      occurrence of "zero-padded to two digits" or "past M99", and the same
      sweep extended to `hooks/` and `scripts/` finds no `M<NN>` placeholder
      (not followed by a third N) and no `m<nn>`; the hand-run `skills/tests`
      suite shows zero reds.
- [x] AC2: A milestone number spelled at two-digit and three-digit widths
      resolves to the same milestone on each of the scripts' ID surfaces — a
      prose token against the known-id set (`check_dangling_ids`), a ROADMAP
      row id against a milestone filename, and a `Depends on` cell against a
      ROADMAP row — in both directions (padded spelling against a narrower one
      on disk, and the reverse), including an id ≥ 100 whose spellings
      coincide; this behavior is test-covered per surface and direction, and
      both gating suites pass.
- [x] AC3: The lexicographic listing of `cairn/milestones/archive/` filenames
      equals the same listing sorted by numeric milestone id (procedure: one
      python comparison of `sorted(names)` against `sorted(names, key=numeric
      id)`).
- [x] AC4: Every path-shaped milestone token (`M[0-9]+-<slug>.md`) in
      `cairn/ROADMAP.md`, `cairn/LESSONS.md`, and `cairn/DESIGN.md` names a
      file that exists under `cairn/milestones/` or
      `cairn/milestones/archive/` (procedure: extract each such token and stat
      it); and every renamed archive file's content is byte-identical across
      the rename (procedure: `git diff --name-status` on the migration commit
      shows status `R100` for each archive path).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T3
- AC2 → T1, T2
- AC3 → T4
- AC4 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Tests first (`scripts/tests`): numeric-equivalence cases for the
      three ID surfaces, both directions, widths two/three plus an id ≥ 100
      whose spellings coincide; red against current string matching.
- [x] T2: Implement numeric id canonicalization in `scripts/cairn_scripts.py`
      (`_ID_RE`, `id_num`, `parse_depends` consumers) and
      `scripts/cairn_validate.py` (`_known_ids`, `check_dangling_ids` max and
      legacy ceilings, roadmap↔file checks); both gating suites green.
- [x] T3: Doctrine + surface sweep: rewrite the ID rule at
      `skills/shared/tracking-rules.md:150-151`; replace `M<NN>`→`M<NNN>` and
      `m<nn>`→`m<nnn>` across skills/, README.md, hooks/
      (`hooks/commit_guard.py:67`), scripts/ (`scripts/cairn_cost.py:74,417`,
      `scripts/cairn_validate.py:1694`); modernize two-digit teaching examples
      best-effort (README M07 walkthrough, `skills/shared/templates/milestone.md:25`,
      `skills/shared/migration-protocol.md:84`, tracking-rules "tidymedia
      M07"); update pinned `skills/tests` fixtures; hand-run skills/tests,
      zero reds; append the D-entry recording the format change.
- [x] T4: Migration: `git mv` the 99 two-digit archive files to M001–M099
      names; update the `archive/M56-…` cite in ROADMAP's citekey candidate
      row; run AC3's comparison and AC4's extract-and-stat; log the known
      history-side path cites left dangling (D-051's `archive/M53-…:17`, plus
      any a DECISIONS/archive grep finds — logged, never edited);
      `cairn_validate` green.
- [x] T5 (return 1): coverage tests for the release-window row-id→filename
      lookup, both directions; `canon_id` isdecimal fix + crash regression
      test; dep FAIL-message as-written spelling + test; modernize the
      SKILL.md description example and fixture fill ids.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-23: created by /milestone-plan.
- 2026-08-23: plan gate: criteria audit ran in full mode ([O] fresh reader, three rounds): round 1 returned 8 findings (sweep proxy, unpinned prose guards, probe variance, two instrument-bound clauses, unreachable promise via D-051's live path cite, AC4 grep proxy, circular diff clause, validate-green misplacement); round 2 returned 3 (residual exemplar proxy, hooks/ fixture churn, one-digit probe unsatisfiable on the prose surface); round 3 returned 1 (scripts/ outside the placeholder sweep) — each disposed by rewording before the criteria were written; the round-3 domain extension adopted verbatim.
- 2026-08-23: plan gate chose fixed three-digit padding over expand-at-each-magnitude because expansion renames the corpus at M10 and again at M100 for the same end state; falsified by an overflow event where the one-commit re-pad at M999 proves costlier than staged expansion.
- 2026-08-23: plan gate chose width 3 over width 4 because width 4 would also rename the 57 three-digit files for headroom the repo may never need; falsified by the repo approaching M999.
- 2026-08-23: plan gate chose numeric resolution plus filename-only rename over rewriting history's two-digit tokens because DECISIONS.md and archive bodies are never edited (IP4); falsified by nothing — the principle is inviolable.
- 2026-08-23: plan gate chose milestone-files-only scope over folding in RB/RR because 13 review files at ~1 per 3 weeks are years from RR100 and RR cites in shipped prose add their own sweep (user's choice); falsified by reviews/archive approaching RR99.
- 2026-08-23: T1 done — 11 equivalence tests added (TestNumericIdEquivalence): 3 per surface-and-direction pairs plus dropped-status and two >=100 coincident pins; 9 red against current string matching, the 2 coincident pins green by construction.
- 2026-08-23: T2 done — `canon_id` added to cairn_scripts (M%03d re-pad, non-numeric pass-through); comparison sites canonicalized in cairn_next (by_id/done/deps) and cairn_validate (check_dependencies, check_id_uniqueness, _known_ids, check_dangling_ids membership, release-nomination lookup); display spellings untouched; scripts 319 + hooks 103 both green.
- 2026-08-23: T3 done — ID rule rewritten (three-digit padding, cross-width resolution, padded filename prefixes, M999 one-commit re-pad); `M<NN>`/`m<nn>` swept to three-N forms across skills/, README.md, hooks/, scripts/ (23 files); teaching examples modernized (README M007 walkthrough, milestone template M013, migration-protocol M053/M054, tidymedia M007); cairn/LESSONS.md header format line corrected in place; AC1 whitespace-normalized sweep clean; skills/tests 528 zero reds; D-125 appended.
- 2026-08-23: T4 done — 99 archive files `git mv`'d M01–M99 → M001–M099; ROADMAP citekey row's archive/M56 cite updated to M056; AC3 comparison True, AC4 extract-and-stat True; history-side dangling path cites after rename: exactly one, D-051's `archive/M53-prose-guard-mutation-harness.md:17` (DECISIONS.md:1318, logged per plan, never edited); validate green, scripts 319 + hooks 103 green.
- 2026-08-23: defect return #1 (review fan-out, [O] diff-bug F5): AC2's row-id→filename surface not test-covered as stated (check_release_window lookup untested) — AC2 tick withdrawn; riding the return: F4 canon_id ValueError on unicode digits, F2 dep FAIL-message spelling, F6/F7 teaching-example modernization; F1 → candidate row; F8 rejected (pre-existing). Supersedes T2's "display spellings untouched" (wrong for FAIL messages) and T4's "exactly one" dangling cite (three: D-051's M53, RB02's M84 + M87 — reviews/archive was not swept; files stay unedited per IP4).
- 2026-08-23: T5 done (return 1) — 4 tests added (release-window lookup both directions — the T2 fix was already in place, the gap was coverage; unicode-digit dep FAILs clean; dep message keeps as-written spelling); canon_id switched to isdecimal; check_dependencies messages print the cell's spelling; "work on M107" in the implement SKILL description; fixture fills M080/M085; scripts 323 + hooks 103 + skills 528 (hand-run) all green.
- 2026-08-23: re-review after return 1 — fresh evidence all four ACs (AC2 ticked: 15 equivalence tests incl. release-window lookup both directions; scripts 323 / hooks 103 / skills 528 green; validate exit 0); three-lens fan-out spawned.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

Fresh evidence, 2026-08-23, this session (PR #158):

- AC1: tracking-rules.md:150-155 read — states three-digit padding (`M001`),
  cross-width resolution, padded filename prefixes, and the M999 one-commit
  re-pad. Whitespace-normalized sweep (python, git ls-files over skills/,
  README.md, hooks/, scripts/): no "zero-padded to two digits", no
  "past M99" in skills/+README, no `M<NN>` (not followed by a third N), no
  `m<nn>` anywhere in the four surfaces. skills/tests hand-run: 528 tests,
  zero reds.
- AC2: TestNumericIdEquivalence run -v: 11/11 pass — prose-token surface
  both directions (padded→narrow, narrow→padded), roadmap↔file surface both
  directions (live/archive width conflict detected both ways, dep→archive
  filename both ways), Depends-on surface both directions plus dropped-status
  across widths, and two ≥100 coincident-spelling cases. Gating suites fresh:
  scripts 319 OK, hooks 103 OK.
- AC3: python comparison — sorted(names) == sorted(names, key=numeric id)
  over cairn/milestones/archive/: True (156 files).
- AC4: extract-and-stat over ROADMAP/LESSONS/DESIGN — 7 path-shaped tokens,
  all exist under milestones/ or archive/: True. Migration commit a3b8ba4
  `git diff --name-status`: 99 archive paths, all R100 (only non-R lines are
  the same-commit tracking-file updates).

Fan-out (2026-08-23, three lenses, ranked findings and dispositions — IP3):

- [O] diff-bug F5 (→ defect return #1): AC2's second surface ("a ROADMAP row
  id against a milestone filename") is not test-covered as stated — the
  surface-2 tests compare filename↔filename (check_id_uniqueness) and
  dep-cell↔filename; the one genuine row-id→filename lookup,
  check_release_window's `live.get(canon_id(row id))`, got the fix but no
  test, and a regression there silently skips the check. Demonstrates AC2
  failing as written → floor return; fix: add both-direction tests through
  the release-window advisory.
- [O] F4 (fix on return): `canon_id("M²")` raises ValueError (isdigit True,
  int() rejects) and parse_depends' isdigit gate passes such a token, so a
  malformed dep cell crashes the validator instead of FAILing — reproduced
  this session; fix with isdecimal() + regression test (D-023 tolerance).
- [O] F2 (fix on return, part): check_dependencies interpolates the
  canonicalized dep into its FAIL message ("depends on M005" from a cell
  reading M05) — fix to print the as-written spelling; check_id_uniqueness
  keeps canonical ids in its messages (it aggregates across spellings) —
  accepted, logged. T2's work-log claim "display spellings untouched" is
  wrong for these FAIL paths; superseded by today's work-log line.
- [O] F3 = [S] blame-history B1 (record correction, on return): T4's
  "exactly one" dangling history cite is wrong — cairn/reviews/archive/ was
  not swept; RB02:129-130 cites archive/M84-record-density-advisory.md and
  M87-density-threshold-recalibration.md, both renamed. Three cites total
  (D-051's M53 + RB02's two), all left unedited (IP4, RB/RR out of scope);
  count corrected by work-log supersession, no file edits.
- [O] F1 (follow-up, candidate row): cairn_cost's `--milestone` filter
  compares milestone_of() (branch-derived) by raw string equality — a
  fourth ID surface outside this plan's three-surface In-scope; captured as
  a ROADMAP candidate row (search-first: no existing row covers it).
- [O] F6 (fix on return): skills/milestone-implement/SKILL.md description
  still teaches "work on M07" — modernized under T3's best-effort mandate.
- [O] F7 (fix on return): test_references_pages.py fills the swept
  placeholder with two-digit ids (M80/M85) — modernized to M080/M085.
- [O] F8 (rejected): dead `row_ids` set in check_orphans — pre-existing,
  on an unmodified line the diff did not introduce (out-of-scope taxonomy);
  removable any time as trivial cleanup.
- [S] blame-history: no other findings — tolerance rules, pinned fixtures,
  history prose, D-entries all verified consistent.
- [S] prior-PR-comments: no prior-review evidence of regression (archived
  Review sections checked; PR-comments probe returned empty), zero findings.

Re-review after return 1 (2026-08-23, fresh evidence, this session):

- AC1: whitespace-normalized sweep over skills/, README.md, hooks/, scripts/
  — zero hits on all four probes; skills/tests hand-run 528, zero reds.
- AC2: TestNumericIdEquivalence 15/15 pass, now including the
  release-window row-id→filename lookup both directions
  (test_narrow_row_id_resolves_to_padded_live_filename and the padded→narrow
  reverse), unicode-digit dep FAILs clean (no crash), dep FAIL message keeps
  the as-written spelling; gating suites fresh: scripts 323 OK, hooks 103 OK
  — AC2 ticked against this evidence.
- AC3: sorted(names) == sorted(names, key=numeric id) over archive/: True
  (156 files).
- AC4: 7 path-shaped tokens in ROADMAP/LESSONS/DESIGN all stat: True;
  migration commit a3b8ba4 shows 99 R100 lines, non-R lines are the
  same-commit tracking updates only.
- Consistency gate: cairn_validate exit 0, all checks pass; no DESIGN.md
  principle change (cairn_impact skipped); generic profile — no toolchain
  checks.
