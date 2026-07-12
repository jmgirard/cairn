<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M36: On-main commit-guard hook

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m36-on-main-commit-guard · https://github.com/jmgirard/cairn/pull/34   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Add a PreToolUse(Bash) hook that nudges when a `git commit` on the default
branch would include non-`cairn/` files, giving the "never implement on main"
git-model rule runtime teeth. Promotes the M08-Out candidate.

## Scope

**In:** a new `hooks/commit_guard.py` fail-permissive PreToolUse(Bash) hook
that fires on a `git commit`, resolves the default branch, computes the
would-be-committed file set, and — only when on the default branch and the set
contains ≥1 path outside `cairn/` — emits a non-blocking `additionalContext`
nudge (no `permissionDecision`) citing the git model; its `hooks.json`
registration; and its `test_hooks.py` coverage (including the shared non-cairn
no-op + garbage-stdin suites). Mirrors `memory_guard.py`'s softest-lever
pattern (D-017) and reuses `cairn_common.py`.

**Out:**
- Blocking / override-marker enforcement → rejected at plan (warn-only chosen;
  the "is this trivial?" call is semantically undecidable from a file list,
  and blocking taxes the frictionless trivial-edit path the rulebook allows).
- Any change to the CLAUDE.md router → out; D-009 keeps the router
  routing-only, and this hook is additive enforcement, not a router edit.
- A configurable/broader silent allowlist beyond `cairn/**` → candidate row if
  over-nudging ever bites (YAGNI now).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] On the default branch in a cairn repo, a `git commit` whose would-be-
      committed set includes a non-`cairn/` path emits PreToolUse
      `additionalContext` (no `permissionDecision`) naming the git-model rule;
      a commit whose set is entirely under `cairn/` is silent. (test)
- [x] On a non-default branch, the hook is silent regardless of file set. (test)
- [x] The default branch is resolved via remote HEAD
      (`refs/remotes/origin/HEAD`, else `git ls-remote --symref origin HEAD`),
      falling back to `main`/`master` only with no remote; a repo whose default
      is `trunk` is detected and a `trunk` commit nudges. (test)
- [x] `git commit -a`/`-am` counts modified-but-unstaged tracked files, not
      only staged ones. (test)
- [x] Command-position matching: a `git commit` inside `echo`/as an argument,
      and non-`git commit` git commands (`git status`), do not fire. (test)
- [x] `commit_guard.py` is silent+permissive outside cairn repos, on non-Bash
      tools, and on garbage stdin, and imports stdlib only — via the extended
      `TestNonCairnNoOp`, garbage-stdin, and `TestStdlibOnly` suites. (test)
- [x] Full hook suite green: `python3 -m unittest discover -s hooks/tests`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each AC → task(s), positional. -->

- AC1 → T1, T3
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T1, T3
- AC5 → T1, T3
- AC6 → T2, T3
- AC7 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Write `hooks/commit_guard.py`: match `git commit` in command
      position (CMD_POS pattern per `merge_guard.py:31`); resolve the default
      branch via remote HEAD with `main`/`master` fallback and no-op when
      detection is inconclusive; compute the committed set
      (`git diff --cached --name-only`, plus `git ls-files -m` when `-a`/`--all`
      is present); if on the default branch and any path is outside `cairn/`,
      `cc.emit` an `additionalContext` nudge with no `permissionDecision`.
      Fail-permissive, stdlib-only.
- [x] T2 — Register the hook in `hooks/hooks.json` as a second PreToolUse
      `Bash` matcher entry alongside `merge_guard.py`.
- [x] T3 — Add `TestCommitGuard` to `hooks/tests/test_hooks.py` covering AC1–5
      (nudge on code commit / silent on cairn-only / silent off-default /
      trunk detection / `-a` modified-tracked / command-position + non-commit);
      extend `TestNonCairnNoOp` payloads and the garbage-stdin tuple to include
      `commit_guard.py`. Run the full suite green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-12: created by /milestone-plan. Design gate: warn-only
  `additionalContext` (not block); silent allowlist = `cairn/**` only
  (top-level markdown deliberately excluded — this plugin's product is
  markdown skills); default-branch detection via remote HEAD. Absorbs the
  "On-main commit-guard hook" candidate (M08 Out).
- 2026-07-12: T1–T3 done. Wrote `hooks/commit_guard.py`, registered it in
  `hooks/hooks.json`, added `TestCommitGuard` (8 cases) + extended the shared
  no-op/garbage suites. Full hook suite green (30 tests); live smoke on the
  m36 branch correctly stays silent (feature branch ≠ default).

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

**Reviewed 2026-07-12 · PR #34 · branch synced (main unmoved since cut).**

Per-criterion evidence (fresh, by command; R gates waived — not an R package):

- AC1 → `TestCommitGuard.test_nudges_on_noncairn_commit_on_default` (nudge,
  `hookEventName` PreToolUse, no `permissionDecision`) +
  `test_silent_on_cairn_only_commit` — pass.
- AC2 → `test_silent_on_feature_branch` — pass.
- AC3 → `test_default_branch_resolved_via_remote_head` (real bare-remote
  `trunk` fixture; origin/HEAD→trunk) — pass.
- AC4 → `test_stage_all_counts_modified_tracked` +
  `test_unstaged_modified_ignored_without_dash_a` — pass.
- AC5 → `test_command_position_and_non_commit_ignored` (echo/status/commit-tree)
  + `test_ignores_other_tools` — pass.
- AC6 → `TestNonCairnNoOp` (incl. commit_guard) + garbage-stdin + `TestStdlibOnly` — pass.
- AC7 → full hook suite `python3 -m unittest discover -s hooks/tests` — 30 pass.

Consistency gate: `cairn_validate` 11/11 (exit 0), incl. "coverage complete"
(the mechanical AC→task Coverage-completeness check). DESIGN.md untouched → Sync
Impact Report skipped. Whole-repo suites green: 30 hooks / 49 scripts / 83 skills.

Independent fresh-context review (two distinct-evidence lenses):

- **[O] diff-bug reviewer (Opus)** — no findings. Verified the `GIT_COMMIT`
  and `STAGE_ALL` regexes (positive+negative cases incl. `--amend`,
  `commit-tree`, env-prefixed commits), default-branch resolution (slashed
  branch names, detached HEAD, no-remote fallback), repo-root-relative path
  handling, and the `hookSpecificOutput`/`additionalContext`-no-`permissionDecision`
  envelope. Confirmed the `trunk` fixture is non-vacuous (branch ≠ main/master,
  so a nudge can only come via the remote-HEAD path).
- **[S] blame-history reviewer (Sonnet)** — no findings. Confirmed the change
  is purely additive to `hooks.json` and `test_hooks.py` (existing
  `merge_guard`/`memory_guard` registrations + assertions byte-identical),
  envelope matches the M07-pinned contract, and design follows D-017 and the
  M07/M19 hook lessons.

Zero surviving findings → scorer/triage not needed (nothing to rank). Both
lenses independently noted the same two conservative-by-design, already-
documented non-defects (accepted, not findings): a pathspec-limited
`git commit <file>` and a multi-token `git -C`/`-c` prefix are silent misses —
warn-only, so neither can wrong-block, mirroring `merge_guard.py`'s documented
stance.

Process note: a reviewer subagent isolated itself in a git worktree, which
parked the primary checkout on `main` mid-review; no data lost (all commits on
the branch), worktree auto-cleaned, branch restored. Lesson captured at merge.
