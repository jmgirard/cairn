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
hooks load via a real plugin install (marketplace path — the skills-dir
symlink dev install loads skills only, not hooks); README install docs
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
- [ ] Scaffold `hooks/hooks.json` + shared cairn-repo detection helper
      (python3, stdlib); wire into plugin.json if required.
- [ ] Implement + fixture-test SessionStart/PreCompact re-injection.
- [ ] Implement + fixture-test Stop guard (uncommitted `cairn/` tracking).
- [ ] Implement + fixture-test PreToolUse merge guard incl. marker
      consumption; define marker path/format (e.g. `cairn/.merge-approved`,
      gitignored).
- [ ] Update `/milestone-review` skill to write the marker at the approval
      gate; update tracking-rules.md if the git/approval model section
      needs the marker mentioned.
- [ ] Verify hooks load via real plugin install; capture evidence.
- [ ] README: install-paths section (marketplace vs symlink, hooks caveat).

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: task 1 — hook API contracts verified against official docs ([S] subagent); summary → references/claude-code-hooks.md.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-11 (plan gate): merge-guard approval signal = single-use marker
  file written by /milestone-review; hook language = python3 stdlib;
  marketplace install-docs candidate absorbed here.

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
