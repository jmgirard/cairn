<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M36: On-main commit-guard hook

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] On the default branch in a cairn repo, a `git commit` whose would-be-
      committed set includes a non-`cairn/` path emits PreToolUse
      `additionalContext` (no `permissionDecision`) naming the git-model rule;
      a commit whose set is entirely under `cairn/` is silent. (test)
- [ ] On a non-default branch, the hook is silent regardless of file set. (test)
- [ ] The default branch is resolved via remote HEAD
      (`refs/remotes/origin/HEAD`, else `git ls-remote --symref origin HEAD`),
      falling back to `main`/`master` only with no remote; a repo whose default
      is `trunk` is detected and a `trunk` commit nudges. (test)
- [ ] `git commit -a`/`-am` counts modified-but-unstaged tracked files, not
      only staged ones. (test)
- [ ] Command-position matching: a `git commit` inside `echo`/as an argument,
      and non-`git commit` git commands (`git status`), do not fire. (test)
- [ ] `commit_guard.py` is silent+permissive outside cairn repos, on non-Bash
      tools, and on garbage stdin, and imports stdlib only — via the extended
      `TestNonCairnNoOp`, garbage-stdin, and `TestStdlibOnly` suites. (test)
- [ ] Full hook suite green: `python3 -m unittest discover -s hooks/tests`.

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

- [ ] T1 — Write `hooks/commit_guard.py`: match `git commit` in command
      position (CMD_POS pattern per `merge_guard.py:31`); resolve the default
      branch via remote HEAD with `main`/`master` fallback and no-op when
      detection is inconclusive; compute the committed set
      (`git diff --cached --name-only`, plus `git ls-files -m` when `-a`/`--all`
      is present); if on the default branch and any path is outside `cairn/`,
      `cc.emit` an `additionalContext` nudge with no `permissionDecision`.
      Fail-permissive, stdlib-only.
- [ ] T2 — Register the hook in `hooks/hooks.json` as a second PreToolUse
      `Bash` matcher entry alongside `merge_guard.py`.
- [ ] T3 — Add `TestCommitGuard` to `hooks/tests/test_hooks.py` covering AC1–5
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

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->
