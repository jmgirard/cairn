# M07: Guardrail hooks (done 2026-07-11)

- PR: https://github.com/jmgirard/cairn/pull/4 (squash-merged)
- Goal: upgrade convention-only gates to technical enforcement via plugin hooks (python3 stdlib-only), no-op outside cairn repos.

Outcome: four hooks in `hooks/` (auto-loaded from hooks.json). SessionStart
injects ROADMAP + active milestone. Stop blocks turn-end while `cairn/`
tracking is uncommitted (excludes the ephemeral marker). PreToolUse denies
`gh pr merge`/`git merge`-to-main without the single-use, gitignored
`cairn/.merge-approved` marker, consumed per merge. Marker wired into
/milestone-review + /hotfix gates, tracking-rules, /cairn-init gitignore.
README documents both install paths + hooks caveat. 18 fixture tests; all
three active hooks LIVE-FIRED end-to-end (incl. merge-guard consumption at
this merge).

Key decisions: approval signal = single-use marker file (plan gate); Stop
block uses TOP-LEVEL decision/reason (not hookSpecificOutput); PreCompact
dropped — no hook API re-injects on compaction (SessionStart additionalContext
is ignored on compact/clear), criterion amended.

Notable: review attempt 1 FAILED — two green-but-inert hooks (wrong Stop
envelope; impossible PreCompact criterion) from a bad task-1 research doc +
fixture tests that check only the script's stdout, not that Claude Code honors
it. Lessons: pin hook JSON to primary-source contracts, live-fire each guard;
hooks snapshot at process start (live verify needs a fresh conversation).
