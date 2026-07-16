# M60: Git-safety hooks — force-push deny, merge-marker restore

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** IP1, GP2
- **Branch/PR:** m60-git-safety-hooks

## Goal

The two honor-system git rules with cheap mechanical teeth get hooks: a
force-push to the default branch is denied at PreToolUse, and a failed
guarded merge no longer consumes the approval marker (RR01 recs 8 + 13).

## Scope

**In:**

- New `hooks/force_push_guard.py`: PreToolUse(Bash) **deny** (not nudge) of
  `git push --force`/`-f` variants targeting the default branch, reusing
  commit_guard's default-branch detection machinery; false-positive-free by
  design (D-023 doctrine): force-pushes to feature branches and plain pushes
  pass through.
- New `hooks/merge_guard_post.py`: PostToolUse(Bash) companion that restores
  `cairn/.merge-approved` when a guarded merge command exits nonzero (ends
  the M33 rewrite-the-marker manual step); a successful merge stays consumed.
- Register both in `hooks/hooks.json`; unit tests in `hooks/tests/`.
- DESIGN.md Architecture hooks bullet updated to list all seven hooks;
  rulebook "never force-push" line notes its mechanical backing.

**Out:**

- Windows launcher fallback for hooks.json → release-prep candidate row.
- Mechanizing AC fencing or CI-state checks → not planned (RR01 Q6: leave
  honor-system).
- Live runtime verification of hook honoring → post-merge follow-up in a
  fresh conversation (M19: hooks snapshot at process start), recorded as a
  work-log note at review, not an AC.

## Acceptance criteria

- [ ] Unit tests prove force_push_guard denies `git push --force`/`-f` (flag
      order and `--force-with-lease` variants) targeting the default branch —
      both explicit-ref and on-default-branch forms — and passes through
      feature-branch force-pushes, plain pushes, and non-push commands.
- [ ] Unit tests prove merge_guard_post restores a consumed
      `cairn/.merge-approved` when the guarded merge command exits nonzero,
      leaves it consumed on success, and no-ops on non-merge commands.
      (RB tripwire: ip-touching)
- [ ] Both hooks registered in hooks/hooks.json with the existing
      python3/timeout envelope shape; all three unittest suites green from
      the repo root.
- [ ] DESIGN.md's hooks bullet names all seven hooks; the rulebook's
      force-push line reflects the new enforcement (guard re-anchors in the
      same commit, M46).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3, T5
- AC4 → T4

## Tasks

- [x] T1: Write `hooks/force_push_guard.py` (reuse cairn_common /
      commit_guard branch detection) + unit tests: deny cases and the
      false-positive matrix. (RB tripwire: ip-touching — this hardens IP1's
      perimeter; deny wording and scope must not block legitimate work.)
- [x] T2: Write `hooks/merge_guard_post.py` + unit tests (restore on fail,
      consumed on success, no-op otherwise). Touches the IP1 approval-marker
      lifecycle — keep single-use semantics: restore only what a *failed*
      attempt consumed, never mint approval.
- [x] T3: Register both in hooks/hooks.json; extend hooks/tests registration
      fixtures if any assert the hook list.
- [x] T4: Update DESIGN.md hooks bullet (5 → 7) and the rulebook's
      "Never force-push" line; re-anchor any guards on either (M46), register
      mutation blocks (M53/M54).
- [x] T5: Run all three suites from the repo root (M56: no exit-blind
      pipes); add the post-merge live-fire note to the work log (fresh
      conversation; retry flow per RR01 rec 13's caution).

## Work log

- 2026-07-16: created by /milestone-plan (promoted from the RR01 rec
  8/13 half of the skill/hook candidate row; recs 7/12 → M59).
- 2026-07-16: gate passed both recommendations (+refspec covered; rename
  lifecycle for the marker); T1 done — force_push_guard denies all three
  force forms (flags, +refspec, HEAD-form) in explicit-ref and
  on-default-branch shapes; default_branch/on_default_branch lifted from
  commit_guard into cairn_common for reuse (stdlib-only import rule); all
  three suites green (41/83/171).
- 2026-07-16: [S] claude-code-guide docs check pinned the T2 contract:
  Bash nonzero exit fires PostToolUseFailure (PostToolUse = success only;
  PreToolUse-denied calls fire neither) — merge_guard_post keys on the
  event name, no exit-code parsing; registers under both events.
- 2026-07-16: T2 done — rename lifecycle shipped (merge_guard consumes by
  rename → .pending; post hook restores on failure with an
  additionalContext note, deletes on success; never mints);
  is_guarded_merge + marker paths moved to cairn_common so both ends share
  one detection; stop_guard excludes the pending basename. Minor
  amendment: `cairn/.merge-approved.pending` added to this repo's
  .gitignore, REQUIRED_GITIGNORE (scaffold spec — adopters pick it up via
  the M24 drift check + init repair), and the cairn-init gitignore bullet;
  contract facts pinned into references/claude-code-hooks.md. Suites
  48/84/171 green.
- 2026-07-16: T3 done — force_push_guard registered PreToolUse(Bash);
  merge_guard_post under BOTH PostToolUse and PostToolUseFailure (Bash);
  no fixture asserted the hook list, so added TestHooksRegistration
  (per-hook registration, standard envelope, every-script-registered).
- 2026-07-16: T4 done — DESIGN bullet now names all seven hooks; rulebook
  force-push line names force_push_guard as its enforcement and the marker
  paragraph records the restore lifecycle; positioning guard re-anchored
  (HOOKS → 7, test renamed) and new test_git_safety_hooks.py added; 8
  mutation entries registered (2 DESIGN blocks + 4 rulebook blocks + 2
  renamed-test re-anchors). Skills suite 175 green.
- 2026-07-16: T5 done — all three suites green with raw exit codes 0/0/0
  (52/84/175 tests); cairn_validate all checks passed, exit 0. Status →
  review. POST-MERGE LIVE-FIRE (fresh conversation — hooks snapshot at
  process start, M19/D-017): (1) force_push_guard denies a real
  `git push --force origin main` and passes a feature-branch force-push;
  (2) the retry flow per RR01 rec 13's caution — deny a marker-less merge,
  approve, fail a merge (e.g. draft PR), confirm the marker was restored
  and the retry passes without rewriting it, then confirm a successful
  merge leaves it consumed.

## Decisions

- 2026-07-16 (gate): force_push_guard also denies the `+refspec` force
  syntax (`git push origin +main`) — the `+` prefix only ever means force,
  so covering it closes a real bypass with zero false-positive risk.
- 2026-07-16 (gate): marker restore uses a rename lifecycle — merge_guard
  consumes by renaming `.merge-approved` → `.merge-approved.pending`;
  merge_guard_post renames back on failed merge, deletes on success. Can
  never mint approval (only restores what a real approval created). Minor
  scope amendment: touches merge_guard.py + widens the gitignore pattern.

## Review
