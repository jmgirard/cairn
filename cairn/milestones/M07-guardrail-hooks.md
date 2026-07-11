# M07: Guardrail hooks (blocking enforcement + context re-injection)

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** —
- **Branch/PR:** m07-guardrail-hooks · https://github.com/jmgirard/cairn/pull/4

## Goal

Upgrade cairn's convention-only gates to technical enforcement via plugin
hooks: block merges to main without recorded user approval, block ending a
turn with uncommitted `cairn/` tracking, and re-inject ROADMAP + active
milestone at session start.

## Scope

**In:** `hooks/hooks.json` + Python 3 (stdlib-only) hook scripts under
`hooks/`; SessionStart (and PreCompact) re-injection of `cairn/ROADMAP.md`
and any active milestone file as additionalContext; Stop hook blocking
turn-end while tracked `cairn/` files have uncommitted changes; PreToolUse
merge guard denying `gh pr merge` / `git merge` into main unless an
approval marker file exists (written by `/milestone-review` at the user
approval gate, consumed by the merge); all hooks no-op in repos without
`cairn/ROADMAP.md`; fixture-driven tests for every hook decision; verify
hooks load via a real plugin install (finding 2026-07-11: skills-dir
installs register hooks too — see work log); README install docs
contrasting the two install paths (absorbs the marketplace install-docs
candidate).

**Out:** skill-less routing rewrite of the claude-md-section template →
stays a candidate (needs empirical testing in openac first); `read_when`
doc-routing frontmatter → milestone-file mechanics candidate; session-end
learning harvest → candidate; promoting the marketplace as the advertised
default install (D-007: manual until pilots pass) → future release prep.

## Acceptance criteria

- [ ] Merge guard: with no approval marker, a `gh pr merge`/`git merge`
      Bash call in a cairn repo is denied (fixture test shows deny
      decision); with the marker present, it passes and the marker is
      consumed (single-use).
- [ ] Stop guard: turn-end with uncommitted tracked `cairn/` changes is
      blocked with a message naming the files; clean tree passes (fixture
      tests for both).
- [ ] SessionStart injection: in a cairn repo, hook output contains
      ROADMAP content and the active milestone file (fixture test).
      (Amended 2026-07-11: dropped "PreCompact re-injects the same" — no
      hook API re-injects on compaction; injection is startup/resume only.)
- [ ] No-op guarantee: every hook exits permissively, quickly, and silently
      in a repo without `cairn/ROADMAP.md` (fixture test per hook).
- [ ] Hook scripts run on python3 stdlib only (no third-party imports;
      grep-verifiable) and every fixture test passes from a clean checkout.
- [ ] Live verification: hooks demonstrably fire in a session using a real
      plugin install of this repo (evidence: transcript/log line, install
      path documented).
- [ ] README documents both install paths (marketplace snapshot vs
      dev symlink) and states that hooks require the plugin install;
      `/milestone-review`'s approval gate writes the marker file.

## Tasks

- [x] Research exact hook API contracts (SessionStart/PreCompact
      additionalContext, Stop block, PreToolUse deny JSON shapes; hooks.json
      schema for plugins) against current Claude Code docs.
- [x] Scaffold `hooks/hooks.json` + shared cairn-repo detection helper
      (python3, stdlib); wire into plugin.json if required (not required —
      hooks.json auto-loads).
- [x] Implement + fixture-test SessionStart injection (PreCompact dropped
      2026-07-11 — API can't inject on compaction; hooks.json unwired,
      criterion amended).
- [x] Implement + fixture-test Stop guard (uncommitted `cairn/` tracking).
      Fixed 2026-07-11: emits TOP-LEVEL decision/reason (was nested under
      hookSpecificOutput → silently no-op'd); regression test asserts
      top-level + absence of the nesting.
- [x] Correct references/claude-code-hooks.md contracts (Stop top-level; no
      compaction re-injection; SessionStart ignored on compact/clear) +
      test-methodology note (fixtures prove print-shape, not live honoring).
- [x] Implement + fixture-test PreToolUse merge guard incl. marker
      consumption; marker = `cairn/.merge-approved`, gitignored,
      single-use.
- [x] Update `/milestone-review` skill to write the marker at the approval
      gate; update tracking-rules.md if the git/approval model section
      needs the marker mentioned (done; also /hotfix gate + /cairn-init
      .gitignore scaffolding — discovered sub-tasks).
- [x] Verify hooks load via real plugin install; capture evidence.
      (Loading evidence: `plugin details` lists all 4 hooks. Firing
      evidence CAPTURED 2026-07-11 in a brand-new Desktop conversation:
      the SessionStart hook auto-injected the "# cairn tracking context
      (auto-injected by the cairn plugin)" block carrying both
      cairn/ROADMAP.md and the active M07 milestone file — header string
      unique to hooks/session_context.py:18. Confirms both hook loading
      AND firing via the live symlink install.)
- [x] README: install-paths section (symlink vs marketplace, hooks caveat,
      branch-checkout footgun).

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: task 1 — hook API contracts verified against official docs ([S] subagent); summary → references/claude-code-hooks.md.
- 2026-07-11: tasks 2–5 — hooks.json + 3 hook scripts + shared helper; 17 fixture tests green; merge guard scoped to command-position git/gh (echo-style false positives excluded); missing cwd = strict no-op.
- 2026-07-11: task 6 — marker protocol wired into /milestone-review + /hotfix approval gates, tracking-rules approval model, and /cairn-init .gitignore scaffolding (minor amendment: hotfix + init were discovered sub-tasks).
- 2026-07-11: task 7 finding — skills-dir installs DO register hooks (`plugin details` shows Hooks (4)); corrected references/claude-code-hooks.md + Scope wording. Firing evidence blocked: CLI logged out, headless runs can't start.
- 2026-07-11: task 8 — README install section rewritten (two paths, hooks activation note, keep-checkout-on-main footgun).
- 2026-07-11: user chose fresh-session verification for task 7. NEXT SESSION: if a "cairn tracking context" block was auto-injected at session start, that is the firing evidence — quote its header in the work log, check task 7 off, set status review, route to /milestone-review M07. If nothing was injected, hooks did not fire: investigate before review.
- 2026-07-11: task 7 diagnosis — no injection + `gh pr merge --help` probe passed undented ⇒ hooks not executing here; cause: hooks snapshot at harness PROCESS start, both live Desktop processes (12:35, 16:17) predate hooks.json (16:27), and /clear reuses the process. Script healthy via manual run (emits injection JSON, exit 0). Supersedes prior NEXT SESSION line: evidence requires a BRAND-NEW Desktop conversation, not /clear.
- 2026-07-11: user chose new-conversation verification (2nd attempt). NEXT SESSION (must be a brand-new Desktop conversation, fresh process): if the "cairn tracking context" block was auto-injected at session start, quote its header in the work log, check task 7 off, set status review, route to /milestone-review M07. If still nothing, hooks don't fire from skills-dir installs in Desktop despite registering — investigate that hypothesis next.
- 2026-07-11: task 7 VERIFIED — brand-new Desktop conversation (fresh process) auto-injected at session start: `# cairn tracking context (auto-injected by the cairn plugin)`, carrying cairn/ROADMAP.md + the active M07 milestone file. Header string is unique to hooks/session_context.py:18, so the injection is unambiguously our hook firing (not /clear reuse of a pre-hooks process). Firing evidence captured; task 7 checked; all 8 tasks done. Status → review; routing to /milestone-review M07.
- 2026-07-11: review attempt 1 FAILED (PR #4) → back to in-progress. Primary-source check (official hooks docs) + [O] fresh review found: (blocker) Stop guard nests decision/reason under hookSpecificOutput but the contract is top-level → block silently no-ops; (should-fix) PreCompact can't inject additionalContext and SessionStart ignores it on compact/clear → "PreCompact re-injects" criterion is unachievable as written, needs gated amendment. Root cause: task-1 research doc recorded wrong contracts; fixture tests only assert the script's own stdout so they masked both. Merge guard, no-op, stdlib, README, SessionStart-on-startup all sound. First trip back from review (thrash count 1/3). Next: /milestone-implement — fix Stop shape + test, drop dead PreCompact wiring + amend criterion, correct the research doc, add live-fire checks.
- 2026-07-11: fixes applied (implement). Stop guard → top-level decision/reason (regression test asserts top-level + no nesting). PreCompact unwired from hooks.json + criterion amended (user gate: drop it) — SessionStart-only. Research doc contracts corrected + test-methodology note added. 16 fixture tests green (was 17; PreCompact test removed). Status → review.
- 2026-07-11: Stop-guard LIVE-FIRE verified in this session. Command-type hooks run the current on-disk script per firing, and the Stop event was already registered at process start (SessionStart fired), so the fixed stop_guard.py executes live here. Dropped an untracked cairn/.livefire-probe, ended the turn; Claude Code BLOCKED turn-end and returned the guard's exact message ("Uncommitted cairn tracking changes: cairn/.livefire-probe…"). Confirms the top-level decision/block shape is honored — the blocker is fixed for real, not just green in fixtures. Probe deleted. Two of four hooks now live-fired (SessionStart + Stop).

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-11 (plan gate): merge-guard approval signal = single-use marker
  file written by /milestone-review; hook language = python3 stdlib;
  marketplace install-docs candidate absorbed here.

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

### Attempt 1 — 2026-07-11 (FAILED; back to in-progress). PR #4.

Per-criterion (17 fixture tests green; JSON shapes cross-checked vs official
docs): merge guard, no-op, stdlib, README — PASS; SessionStart startup
injection PASS + live-verified this session. FAILED: Stop guard (finding 1),
PreCompact clause of SessionStart criterion (finding 2). Live verification
PARTIAL — only SessionStart fired live.

Independent review ([O] fresh-context) findings + triage:
1. BLOCKER — Stop emits `hookSpecificOutput.{decision,reason}`; contract is
   top-level. Confirmed vs primary docs. → FIX (reopened task).
2. SHOULD-FIX — PreCompact wiring is dead (no additionalContext support);
   criterion built on false premise. Confirmed vs docs, incl. that
   SessionStart additionalContext is ignored on compact/clear. → FIX +
   gated criterion amendment (reopened task).
3. NIT — `gh pr merge --help`/`--disable-auto` are treated as guarded and
   consume the marker. → accept or tighten during fix; logged.
4. NIT — marker consumed on attempt not success (documented trade-off). →
   reject (intended; deny reason + skill cover the retry).
Method finding (accepted): fixture tests assert the script's own stdout,
not that Claude Code honors the shape — false confidence; add doc-contract
checks + one live-fire per guard.
