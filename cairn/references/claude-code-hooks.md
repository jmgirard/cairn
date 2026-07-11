# Claude Code plugin hooks API (contracts used by M07)

Sources: https://code.claude.com/docs/en/hooks-guide.md and
https://code.claude.com/docs/en/hooks.md (fetched 2026-07-11 via [S]
claude-code-guide subagent).

## Placement

- Plugin hooks live in `hooks/hooks.json` at the plugin root; loaded
  automatically when the plugin is enabled — `plugin.json` does not
  reference them. Skills-directory plugins (`<name>@skills-dir`,
  incl. symlinks) DO register hooks: `claude plugin details
  cairn@skills-dir` lists `Hooks (4)` from this repo's hooks.json
  (verified 2026-07-11; corrects the earlier subagent claim that only
  marketplace installs load hooks). Symlink consequence: hooks go live
  from whatever branch the checkout has, in every repo, at next session
  start.
- `${CLAUDE_PLUGIN_ROOT}` expands to the plugin install dir, in hook
  `command` fields only.

## Input (stdin JSON)

Common: `session_id`, `cwd`, `hook_event_name`, `transcript_path`,
`permission_mode`. Event-specific: SessionStart `source`
(startup|resume|clear|compact); PreCompact `compaction_type`; Stop
`stop_hook_active` (true ⇒ a prior Stop block already fired — must exit 0
to avoid infinite loops); PreToolUse `tool_name` + `tool_input` (Bash
command string at `tool_input.command`).

## Output (stdout JSON, exit 0)

- SessionStart/PreCompact context injection:
  `{"hookSpecificOutput": {"hookEventName": "<event>",
  "additionalContext": "<text>"}}` (bare stdout text also works).
- Stop block: `{"hookSpecificOutput": {"hookEventName": "Stop",
  "decision": "block", "reason": "<told to Claude>"}}`.
- PreToolUse deny: `{"hookSpecificOutput": {"hookEventName": "PreToolUse",
  "permissionDecision": "deny", "permissionDecisionReason": "<reason>"}}`
  (`allow` / `ask` also valid; prefer this over legacy `decision: block`).
- Exit 2 = block with stderr as feedback; other nonzero = non-blocking
  error. Prefer exit 0 + structured JSON.

## Matchers & execution

- PreToolUse matcher `"Bash"` scopes to Bash calls (plain string = exact;
  regex chars ⇒ JS regex). SessionStart matches on `source`; Stop needs no
  matcher. Hooks matching one event run in parallel; default command
  timeout 600s (`"timeout"` per hook, seconds); cwd = session cwd (not
  necessarily repo root — walk up to find `cairn/ROADMAP.md`).
