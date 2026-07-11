# M07: Guardrail hooks (blocking enforcement + context re-injection)

- **Status:** in-progress   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** high
- **Depends on:** —
- **Branch/PR:** m07-guardrail-hooks

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
      ROADMAP content and the active milestone file (fixture test);
      PreCompact re-injects the same.
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
- [x] Implement + fixture-test SessionStart/PreCompact re-injection.
- [x] Implement + fixture-test Stop guard (uncommitted `cairn/` tracking).
- [x] Implement + fixture-test PreToolUse merge guard incl. marker
      consumption; marker = `cairn/.merge-approved`, gitignored,
      single-use.
- [x] Update `/milestone-review` skill to write the marker at the approval
      gate; update tracking-rules.md if the git/approval model section
      needs the marker mentioned (done; also /hotfix gate + /cairn-init
      .gitignore scaffolding — discovered sub-tasks).
- [ ] Verify hooks load via real plugin install; capture evidence.
      (Loading evidence done: `plugin details` lists all 4 hooks.
      Firing evidence diagnosed 2026-07-11: hooks snapshot at harness
      *process* start; both running Desktop processes predate
      hooks.json, and `/clear` reuses the process — so no session in
      those processes can fire them. Script verified healthy by manual
      run. Needs a brand-new Desktop conversation (fresh process) or
      `claude login` + headless run.)
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

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-11 (plan gate): merge-guard approval signal = single-use marker
  file written by /milestone-review; hook language = python3 stdlib;
  marketplace install-docs candidate absorbed here.

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
