<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M25: Parameterize the default branch in the operational skill steps

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M22   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] The tracking-rules git model carries a single canonical runtime
      default-branch **detection recipe** (the `git symbolic-ref --short
      refs/remotes/origin/HEAD` command + its fallback), stated as what an
      operational skill runs when it needs the branch name. Evidence: the
      snippet is present and the four operational skills reference detection
      rather than re-specifying it.
- [ ] `/milestone-implement`'s git steps (sync, branch-from, branch-sync
      merge) name the detected default branch, with no hardcoded-`main` git
      command. Evidence: grep of the skill + guard test.
- [ ] `/milestone-review`'s git steps are parameterized — specifically the
      diff command (`git diff main..HEAD` → default-branch form), the
      merge-approval **chip label** (`Merge PR #N to main` → default-branch
      form), the sync-with-origin step, and the post-merge hygiene
      checkout/pull. Evidence: grep + guard test.
- [ ] `/hotfix`'s git steps (branch-from, merge chip label, branch-sync) name
      the detected default branch. Evidence: grep + guard test.
- [ ] `/cairn-release`'s git steps (release-from-clean, up-to-date check,
      release-prep commit) name the detected default branch. Evidence: grep +
      guard test.
- [ ] `test_default_branch_parameterized.py` is extended with per-skill
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

- [ ] T1 — Add the canonical runtime detection recipe to the tracking-rules
      git model (`skills/shared/tracking-rules.md`, "Git and approval model",
      near line 188 where it currently defers detection to cairn-init): one
      snippet giving `git symbolic-ref --short refs/remotes/origin/HEAD` (strip
      `origin/`) + the local/ask fallback, noting operational skills detect at
      runtime. Do not reintroduce any retired hardcoded-`main` phrase the
      existing guard forbids.
- [ ] T2 — Parameterize `/milestone-implement` (`skills/milestone-implement/
      SKILL.md:30,32,35,36`): sync-with-origin, branch-from, and the
      "if main has moved … merge main into the branch" branch-sync step now
      name the detected default branch.
- [ ] T3 — Parameterize `/milestone-review` (`skills/milestone-review/
      SKILL.md`): sync step (21–23), the diff command `git diff main..HEAD`
      (94), the merge-gate chip label `Merge PR #N to main` (139/42-style),
      and the post-merge hygiene checkout/pull (150–151). Preserve the
      merge-gate chip's AskUserQuestion shape (test_gate_wording lock).
- [ ] T4 — Parameterize `/hotfix` (`skills/hotfix/SKILL.md:27,42,49,56`):
      branch-from-default, merge chip label, marker-consumption note, and the
      branch-sync line.
- [ ] T5 — Parameterize `/cairn-release` (`skills/cairn-release/
      SKILL.md:19,21,50`): release-from-clean-default, up-to-date-with-origin
      check, and the release-prep commit target.
- [ ] T6 — Extend `skills/tests/test_default_branch_parameterized.py` with a
      per-operational-skill test asserting each of the four contains no
      hardcoded-`main` git command and references default-branch detection;
      run the full `skills/tests` + `scripts/tests` suites and confirm green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan (direction/detection/scope set at the plan gate: runtime-detect, all four skills, date-scan kept separate).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
