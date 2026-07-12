<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M25: Parameterize the default branch in the operational skill steps

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M22   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m25-default-branch-operational-skills · https://github.com/jmgirard/cairn/pull/23   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make the four operational skills (`/milestone-implement`, `/milestone-review`,
`/hotfix`, `/cairn-release`) issue git operations against the repo's detected
default branch instead of a hardcoded `main`, finishing at the operational
layer what M22 established as doctrine.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Parameterize every `main`-named git step in the four operational
skills so a `master` (or otherwise-named) repo gets correct commands. Skills
learn the branch name by **runtime detection** (per the M25 gate). Add one
canonical detection recipe to the tracking-rules git model that the
operational skills reference, so detection is specified once, not four times.
Extend `test_default_branch_parameterized.py` to lock the four skills.

**Out:**
- The `cairn_validate` date-scan false positive → stays candidate G-C2
  (separate surface: the Python script), planned as its own next unit.
- Storing the detected branch name in a tracking file → rejected at the M25
  gate in favor of runtime detection; not a candidate.
- Any change to the doctrine/template/`cairn-init` layer → already shipped by
  M22; this milestone touches only the operational skill *steps* + the shared
  detection recipe.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] The tracking-rules git model carries a single canonical runtime
      default-branch **detection recipe** (the `git symbolic-ref --short
      refs/remotes/origin/HEAD` command + its fallback), stated as what an
      operational skill runs when it needs the branch name. Evidence: the
      snippet is present and the four operational skills reference detection
      rather than re-specifying it.
- [x] `/milestone-implement`'s git steps (sync, branch-from, branch-sync
      merge) name the detected default branch, with no hardcoded-`main` git
      command. Evidence: grep of the skill + guard test.
- [x] `/milestone-review`'s git steps are parameterized — specifically the
      diff command (`git diff main..HEAD` → default-branch form), the
      merge-approval **chip label** (`Merge PR #N to main` → default-branch
      form), the sync-with-origin step, and the post-merge hygiene
      checkout/pull. Evidence: grep + guard test.
- [x] `/hotfix`'s git steps (branch-from, merge chip label, branch-sync) name
      the detected default branch. Evidence: grep + guard test.
- [x] `/cairn-release`'s git steps (release-from-clean, up-to-date check,
      release-prep commit) name the detected default branch. Evidence: grep +
      guard test.
- [x] `test_default_branch_parameterized.py` is extended with per-skill
      assertions covering all four operational skills (no bare-`main` git
      command; default-branch detection referenced) and the whole
      `skills/tests` + `scripts/tests` suites pass. Evidence: `unittest`
      output green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Canonical runtime detection recipe added to the tracking-rules git model (`git symbolic-ref` + remote-querying fallback).
- [x] T2 — `/milestone-implement` git steps (sync, branch-from, branch-sync) parameterized to the detected default branch.
- [x] T3 — `/milestone-review` parameterized: diff cmd, merge-gate chip label, sync step, post-merge hygiene (gate-wording lock preserved).
- [x] T4 — `/hotfix` git steps (branch-from, chip label, marker note, branch-sync) parameterized.
- [x] T5 — `/cairn-release` git steps (release-from-clean, up-to-date check, commit target) parameterized.
- [x] T6 — `test_default_branch_parameterized.py` extended (+5 tests) locking the 4 skills + the recipe; full suites green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (direction/detection/scope set at the plan gate: runtime-detect, all four skills, date-scan kept separate).
- 2026-07-12: in-progress; cut m25-default-branch-operational-skills. T1 — added the canonical runtime detection recipe to the tracking-rules git model.
- 2026-07-12: T2/T3 — parameterized /milestone-implement and /milestone-review git steps (incl. `git diff <default-branch>..HEAD` and the merge-gate chip label) to the detected default branch.
- 2026-07-12: T4/T5 — parameterized /hotfix and /cairn-release git steps; all four operational skills now free of hardcoded `main` git commands.
- 2026-07-12: T6 — extended test_default_branch_parameterized.py (5 new tests locking the 4 operational skills + the recipe); full skills/tests (63) + scripts/tests (43) + cairn_validate green. All tasks done → review.
- 2026-07-12: review — AC evidence + consistency gate recorded, 6 AC boxes ticked; draft PR #23.
- 2026-07-12: review — independent 2-lens+scorer done; both diff-bug findings (sub-80: recipe fallback F1/60, dangling ref F2/75) fixed anyway; recipe fallback now remote-querying. Suites green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

_Reviewed 2026-07-12 · PR #23 · diff `main..HEAD`: 8 files, +122/−39._

**Acceptance-criteria evidence (fresh):**

- AC1 ✓ — recipe present in tracking-rules git model: `git symbolic-ref
  --short refs/remotes/origin/HEAD` (line 195) + "re-detects it at runtime"
  (line 192); all four skills reference "tracking-rules git model".
- AC2 ✓ — `milestone-implement`: `grep -woc main` = 0.
- AC3 ✓ — `milestone-review`: `grep -woc main` = 0; diff cmd is
  `git diff <default-branch>..HEAD` (line 95); merge chip label is
  `Merge PR #N to <default-branch>` (line 132–133).
- AC4 ✓ — `hotfix`: `grep -woc main` = 0.
- AC5 ✓ — `cairn-release`: `grep -woc main` = 0.
- AC6 ✓ — guard test extended (+5 tests: 2 recipe, 3 per-skill); full suites
  green — `skills/tests` 63, `scripts/tests` 43.

**Consistency gate:** `cairn_validate.py` exit 0 (10/10 PASS). Coverage
complete: AC1→T1 … AC6→T6, every criterion maps to an existing task. No
DESIGN principle changed → `cairn_impact` skipped. R gates waived (plugin repo).

**Independent fresh-context review:** two lenses (diff-bug [O] + blame-history
[S]) then scorer [S].

- Blame-history [S]: no findings. Confirmed M25 only *inserts* the recipe
  bullet (M22 doctrine untouched), the merge-gate chip discipline is
  byte-identical pre/post, and `merge_guard.py` already matches any branch.
- Diff-bug [O]: 2 findings, both scored **below the 80 action threshold** —
  logged here per IP3, and **both fixed anyway** as cheap correctness wins:
  - F1 (scored 60) — the recipe's local fallback (`git symbolic-ref --short
    HEAD`) returns the *feature* branch when run on one with `origin/HEAD`
    unset, silently wrong for review/hotfix/resume. **Fixed:** fallback now
    queries the remote (`git ls-remote --symref origin HEAD`); only a
    no-remote repo asks the user; never guesses local HEAD.
  - F2 (scored 75) — "a step below" had no referent in tracking-rules (the
    `<default-branch>` placeholders live in the skills). **Fixed:** reworded
    to "a skill step".
- Also fixed a punctuation byproduct at `cairn-release:19` (blame-lens
  cosmetic, taxonomy-dropped, but mine).

Suites re-run green after fixes: `skills/tests` 63, `scripts/tests` 43.
