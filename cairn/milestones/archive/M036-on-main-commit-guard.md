# M36: On-main commit-guard hook — done 2026-07-12

**Goal:** give the "never implement on main" git-model rule runtime teeth.

**Outcome:** shipped `hooks/commit_guard.py`, a warn-only PreToolUse(Bash)
hook. On the default branch, a `git commit` whose would-be-committed set
includes any path outside `cairn/` emits a non-blocking `additionalContext`
nudge (no `permissionDecision`); all-`cairn/` commits and feature-branch work
stay silent. Default branch resolved via remote HEAD (main/master fallback).
Registered as a second PreToolUse(Bash) entry in `hooks.json`; `TestCommitGuard`
(8 cases) + extended shared no-op/garbage suites. 162 tests green; independent
review (2 lenses) zero findings. PR #34.

**Key decisions (plan gate):** warn-only, not block — the "is this trivial?"
call is undecidable from a file list, and blocking taxes the frictionless
trivial-edit path (mirrors memory_guard / D-017). Silent allowlist = `cairn/**`
ONLY; top-level markdown deliberately excluded (this plugin's product is
markdown skills). Default-branch detection via remote HEAD, not hardcoded.

**Accepted non-defects (documented in the hook):** pathspec-limited
`git commit <file>` and multi-token `git -C`/`-c` are silent misses — warn-only,
never wrong-blocks (merge_guard's conservative stance).

**Not live until a fresh session:** hooks snapshot at process start (M19), so
live-fire confirmation is deferred to the next new conversation.
