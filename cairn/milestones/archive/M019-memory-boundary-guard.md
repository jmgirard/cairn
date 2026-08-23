# M19: Memory-boundary write guard (GP4 enforcement) — done 2026-07-12

**Goal:** Give GP4 a runtime enforcement arm — a write-time guard reminding
Claude of the memory→`cairn/`-files boundary when it writes to per-user memory
in a cairn repo (the write-time counterpart to `merge_guard.py`/IP1).

**Outcome:** `hooks/memory_guard.py` (PreToolUse on `Write`) fires when a Write
targets a `.claude/projects/*/memory/` path while cwd is a cairn repo, emitting
a non-blocking `additionalContext` nudge (no `permissionDecision`); silent
no-op otherwise, fail-permissive. Registered in `hooks.json` (Write matcher).
`tracking-rules.md` gained the "Memory intake gate (GP4)" rule. Tests:
`TestMemoryGuard` + shared no-op/garbage cases (hooks suite 22 green).

**Key decisions:** D-017 — non-blocking `additionalContext`, no
`permissionDecision` (softest lever; rejected `ask`=nag, `allow`=override).
Prose-only fallback not needed (T1 confirmed the contract).

**Review:** all 5 ACs verified fresh; [O]+[S]+scorer — 1 finding (78,
sub-threshold), cheap slice actioned (recorded PreToolUse `additionalContext`
in `references/claude-code-hooks.md`). Residual: live-fire needs a fresh
post-merge session (hooks snapshot at process start) — D-017.

**PR:** #17 (squash-merged).
