# Claude Code plugin hooks API (contracts used by M07, M60)

Sources: https://code.claude.com/docs/en/hooks-guide.md and
https://code.claude.com/docs/en/hooks.md (fetched 2026-07-11 via [S]
claude-code-guide subagent; PostToolUse/PostToolUseFailure facts fetched
2026-07-16 the same way, for M60).

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
(startup|resume|clear|compact — additionalContext honored on the first
two only); PreCompact `compaction_type`; Stop
`stop_hook_active` (true ⇒ a prior Stop block already fired — must exit 0
to avoid infinite loops); PreToolUse `tool_name` + `tool_input` (Bash
command string at `tool_input.command`).

## Output (stdout JSON, exit 0)

Two envelopes exist and they are NOT interchangeable — the M07 review
found a Stop block nested in the wrong one, which silently no-ops.
Verified against https://code.claude.com/docs/en/hooks.md (2026-07-11):
event-specific output nests under `hookSpecificOutput`; **decision control
(`decision`/`reason`) is TOP-LEVEL** for Stop, SubagentStop, PreCompact,
PostToolUse, UserPromptSubmit, ConfigChange.

- SessionStart context injection: `{"hookSpecificOutput":
  {"hookEventName": "SessionStart", "additionalContext": "<text>"}}` (bare
  stdout text also works). **Honored only when `source` is `startup` or
  `resume`; IGNORED on `clear` and `compact`.**
- Stop / SubagentStop block: **top-level** `{"decision": "block",
  "reason": "<told to Claude>"}` — do NOT nest under hookSpecificOutput
  (a nested `decision` is ignored). Stop/SubagentStop may also carry
  `hookSpecificOutput.additionalContext` for non-blocking feedback.
- PreToolUse deny: `{"hookSpecificOutput": {"hookEventName": "PreToolUse",
  "permissionDecision": "deny", "permissionDecisionReason": "<reason>"}}`
  (`allow` / `ask` also valid; prefer this over legacy `decision: block`).
- PreToolUse non-blocking nudge: `{"hookSpecificOutput": {"hookEventName":
  "PreToolUse", "additionalContext": "<text>"}}` — `additionalContext` is
  honored on PreToolUse with `permissionDecision` **optional**; omitting it
  injects the text as context Claude reads next turn while the tool proceeds
  through the normal permission flow (no allow-override, no ask-dialog). This
  is the softest PreToolUse lever; `memory_guard.py` (M19) uses it. Source:
  official hooks docs (code.claude.com/docs/en/hooks.md), confirmed 2026-07-12
  for M19 T1. Live-fire (does the running client honor an
  `additionalContext`-only PreToolUse payload) still pending — hooks snapshot
  at process start, so it needs a fresh session after the hook is registered
  (D-017).
- PreCompact: block-only (top-level `decision: "block"`). It does **NOT**
  support `additionalContext` — there is NO hook that re-injects context on
  compaction (PreCompact fires before compaction with nowhere to attach;
  SessionStart(compact) ignores additionalContext). cairn injects at
  SessionStart(startup/resume) only.
- Exit 2 = block with stderr as feedback; other nonzero = non-blocking
  error. Prefer exit 0 + structured JSON.

## PostToolUse / PostToolUseFailure (M60, fetched 2026-07-16)

- **Outcome routing**: PostToolUse fires "after a tool call succeeds";
  PostToolUseFailure "after a tool call fails". **For Bash specifically,
  "a failure occurs when the command exits with a non-zero exit status"**
  (docs, verbatim) — so a nonzero-exit command fires PostToolUseFailure,
  not PostToolUse. No exit-code field is needed or documented for the
  success case: the event name IS the outcome signal. `merge_guard_post.py`
  keys on this.
- A PreToolUse-denied call fires **neither** (a separate PermissionDenied
  event exists for that); both Post events are observational — nothing
  they output can un-run the tool. Decision control: top-level
  `decision: "block"`/`reason`; `hookSpecificOutput.additionalContext`
  also honored.
- Failure input carries `tool_input` plus `tool_output`
  (`{"isError": true, "text": "..."}`); the success-case `tool_output`
  shape for Bash is NOT documented — don't parse it, key on the event.
- Registration envelope in hooks.json is identical to PreToolUse
  (`{"matcher": "Bash", "hooks": [{"type": "command", ...}]}`) under the
  `PostToolUse` / `PostToolUseFailure` keys.
- **Fixture tests prove only what a hook prints, not that Claude Code
  honors it — pin asserted envelopes to this contract + one live-fire.**

## Matchers & execution

- PreToolUse matcher `"Bash"` scopes to Bash calls (a literal matcher is split
  on `|`/`,` and each alternative exact-matched; a regex metacharacter ⇒ JS
  regex — full dispatch below) (corrected M76). SessionStart matches on `source`; Stop needs no
  matcher. Hooks matching one event run in parallel; default command
  timeout 600s (`"timeout"` per hook, seconds); cwd = session cwd (not
  necessarily repo root — walk up to find `cairn/ROADMAP.md`).
- **Matcher dispatch, as implemented** (read out of the shipped binary,
  2.1.207 — the `GFy` matcher; not from the docs, which state it loosely).
  Three paths: `*` or empty matches every tool. Otherwise a matcher made up
  ONLY of `[a-zA-Z0-9_|]` (or `[a-zA-Z0-9_|, -]` in the variant that admits
  commas/spaces/dashes) takes the **literal** path — it is split on `|`/`,`,
  each alternative is trimmed and alias-expanded, and the tool name must
  **equal one of them exactly**. So `Edit|Write` matches both Edit and Write:
  the literal path is per-alternative set membership, NOT a whole-string
  compare. Any character outside that class (`.`, `*`, `(` …) sends the whole
  matcher to `new RegExp(t)`, tested **unanchored** against the tool name and
  its aliases; an unparseable pattern logs `Invalid regex pattern in hook
  matcher` and matches nothing.
- **What that means for MCP tool names.** `_` is in the literal class, so a
  bare `mcp__ccd_session__spawn_task` is an exact compare bound to one server
  and silently unwires on a server rename. Adding `|` does NOT buy regex
  treatment — it keeps the matcher on the literal path with more
  alternatives. Only a metacharacter escapes it: `mcp__.*__spawn_task`. Claude
  Code ships its own warning for the narrower case of a matcher like
  `mcp__server` with no second `__`: "matches no tool (it is compared as an
  exact string). To match all tools from this server, use `mcp__server__.*`."
  Because the regex path is unanchored, keep patterns tight — `Edit.*` (a
  metacharacter, so genuinely regex) also hits `NotebookEdit` and `MultiEdit`;
  a bare `Edit` does not, because it never leaves the literal path. Keep the hook's own
  tool-name regex the same suffix shape as its matcher so the two agree
  (`hooks.json:67` + `idea_guard.py:28` are the live exemplar).
