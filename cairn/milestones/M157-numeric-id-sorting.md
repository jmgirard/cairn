<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M157: Milestone IDs sort numerically — three-digit padding, numeric resolution

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] AC1: The Milestone IDs rule in `skills/shared/tracking-rules.md` states
      that IDs are zero-padded to three digits (`M001`), that spellings of the
      same number at other zero-pad widths resolve to the same milestone, that
      milestone filename prefixes carry the padded form, and that a repo
      passing M999 re-pads filenames in one hygiene commit; a
      whitespace-normalized sweep of `skills/` and `README.md` finds no
      occurrence of "zero-padded to two digits" or "past M99", and the same
      sweep extended to `hooks/` and `scripts/` finds no `M<NN>` placeholder
      (not followed by a third N) and no `m<nn>`; the hand-run `skills/tests`
      suite shows zero reds.
- [ ] AC2: A milestone number spelled at two-digit and three-digit widths
      resolves to the same milestone on each of the scripts' ID surfaces — a
      prose token against the known-id set (`check_dangling_ids`), a ROADMAP
      row id against a milestone filename, and a `Depends on` cell against a
      ROADMAP row — in both directions (padded spelling against a narrower one
      on disk, and the reverse), including an id ≥ 100 whose spellings
      coincide; this behavior is test-covered per surface and direction, and
      both gating suites pass.
- [ ] AC3: The lexicographic listing of `cairn/milestones/archive/` filenames
      equals the same listing sorted by numeric milestone id (procedure: one
      python comparison of `sorted(names)` against `sorted(names, key=numeric
      id)`).
- [ ] AC4: Every path-shaped milestone token (`M[0-9]+-<slug>.md`) in
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

- [ ] T1: Tests first (`scripts/tests`): numeric-equivalence cases for the
      three ID surfaces, both directions, widths two/three plus an id ≥ 100
      whose spellings coincide; red against current string matching.
- [ ] T2: Implement numeric id canonicalization in `scripts/cairn_scripts.py`
      (`_ID_RE`, `id_num`, `parse_depends` consumers) and
      `scripts/cairn_validate.py` (`_known_ids`, `check_dangling_ids` max and
      legacy ceilings, roadmap↔file checks); both gating suites green.
- [ ] T3: Doctrine + surface sweep: rewrite the ID rule at
      `skills/shared/tracking-rules.md:150-151`; replace `M<NN>`→`M<NNN>` and
      `m<nn>`→`m<nnn>` across skills/, README.md, hooks/
      (`hooks/commit_guard.py:67`), scripts/ (`scripts/cairn_cost.py:74,417`,
      `scripts/cairn_validate.py:1694`); modernize two-digit teaching examples
      best-effort (README M07 walkthrough, `skills/shared/templates/milestone.md:25`,
      `skills/shared/migration-protocol.md:84`, tracking-rules "tidymedia
      M07"); update pinned `skills/tests` fixtures; hand-run skills/tests,
      zero reds; append the D-entry recording the format change.
- [ ] T4: Migration: `git mv` the 99 two-digit archive files to M001–M099
      names; update the `archive/M56-…` cite in ROADMAP's citekey candidate
      row; run AC3's comparison and AC4's extract-and-stat; log the known
      history-side path cites left dangling (D-051's `archive/M53-…:17`, plus
      any a DECISIONS/archive grep finds — logged, never edited);
      `cairn_validate` green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-23: created by /milestone-plan.
- 2026-08-23: plan gate: criteria audit ran in full mode ([O] fresh reader, three rounds): round 1 returned 8 findings (sweep proxy, unpinned prose guards, probe variance, two instrument-bound clauses, unreachable promise via D-051's live path cite, AC4 grep proxy, circular diff clause, validate-green misplacement); round 2 returned 3 (residual exemplar proxy, hooks/ fixture churn, one-digit probe unsatisfiable on the prose surface); round 3 returned 1 (scripts/ outside the placeholder sweep) — each disposed by rewording before the criteria were written; the round-3 domain extension adopted verbatim.
- 2026-08-23: plan gate chose fixed three-digit padding over expand-at-each-magnitude because expansion renames the corpus at M10 and again at M100 for the same end state; falsified by an overflow event where the one-commit re-pad at M999 proves costlier than staged expansion.
- 2026-08-23: plan gate chose width 3 over width 4 because width 4 would also rename the 57 three-digit files for headroom the repo may never need; falsified by the repo approaching M999.
- 2026-08-23: plan gate chose numeric resolution plus filename-only rename over rewriting history's two-digit tokens because DECISIONS.md and archive bodies are never edited (IP4); falsified by nothing — the principle is inviolable.
- 2026-08-23: plan gate chose milestone-files-only scope over folding in RB/RR because 13 review files at ~1 per 3 weeks are years from RR100 and RR cites in shipped prose add their own sweep (user's choice); falsified by reviews/archive approaching RR99.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->
