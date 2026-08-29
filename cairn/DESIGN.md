# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system. The core is language-agnostic; each
adopting repo declares a **toolchain profile** (`cairn/PROFILE.md`, seven slots:
verify, consistency-gate, test-doctrine, release-walk, init-detection,
greenfield-openers, changelog) that supplies the language/toolchain-specific commands the
operational skills read, instead of the core hardcoding one language (M45
spine, M46 rewire, M47 release; D-024/D-025 keep the oracle doctrine universal,
orthogonal to the profile). Four profiles ship — `r-package` (devtools/CRAN),
`python` (pytest/PyPI), `docker-image` (hadolint+build/container registry), and
`generic`; this repo runs `generic`. Logic lives here (skills, rules,
templates); state lives in each adopting repo under `cairn/`. The founding
spec is superseded by this file, the shared rulebook, and DECISIONS.md; git
history preserves it (removed at v1.0, M62).

Positioning (M06, references/competitive-landscape.md): cairn is change
control + longitudinal project memory for agent-driven work — a niche no
surveyed system occupies. Markdown state is commodity; the differentiators
are governed state (sole authority, caps, archives), skill-gated
transitions, human-gated merges, and a domain verification doctrine.

## Architecture

- `.claude-plugin/plugin.json` — manifest.
- `skills/<name>/SKILL.md` × 9 — workflow logic; each reads the shared
  rulebook first and never restates it. Includes `design-interview`, a
  standalone two-phase (facts → principles) DESIGN.md elicitation interview
  (D-013), offered from `/cairn-init`'s close block; it recommends running
  the session on Fable (D-014).
- `skills/shared/tracking-rules.md` — the single rulebook. Conditional
  modules beside it: `validation-doctrine.md` (domain doctrine for
  numeric/scoring work, referenced from the rulebook — M58),
  `migration-protocol.md` (cairn-init §2's body, read only on precursor
  footprint detection — M59), and `records-hygiene.md` (candidate-row
  lifecycle and supersede discipline, read at hygiene/plan gates —
  M113, trimmed M146); each module carries a header-stated size
  budget (M154).
- `skills/shared/templates/` — milestone, brief, decision, CLAUDE.md section,
  source note, synthesis note, archive summary, and the LESSONS.md /
  DECISIONS.md file headers (M163).
- `skills/shared/profiles/` — the shipped reference toolchain profiles
  (`r-package`, `python`, `docker-image`, `generic`); `cairn-init` instantiates one into a repo's
  `cairn/PROFILE.md`, and the operational skills read its slots.
- `hooks/hooks.json` + python3 (stdlib) scripts (M07) — the enforcement
  layer, all no-op outside cairn repos. Eight hooks: `session_context`
  (SessionStart context injection; an active milestone's cap-exempt sections
  are read-bounded to their newest content, D-063); `stop_guard` (Stop-guard on uncommitted
  `cairn/` tracking); five PreToolUse guards — `merge_guard` (single-use
  `cairn/.merge-approved` marker, bound to the PR it approves since M72,
  technically backing IP1),
  `force_push_guard` (denies force-pushes to the default branch — IP1's
  never-force-push line, mechanically backed; M60), `commit_guard`
  (nudge against committing on the default branch), `memory_guard` (GP4
  memory-boundary nudge, D-017), and `idea_guard` (out-of-band idea-capture
  nudge toward a candidate row, D-042); and one PostToolUse/PostToolUseFailure
  companion — `merge_guard_post` (restores the approval marker a failed
  guarded merge consumed, deletes it on success; M60). The three nudges are
  advisory, never blocking.
- `scripts/` + python3 (stdlib) reporters (M10) — the deterministic read
  layer: `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate), `cairn_impact` (principle
  → citing `cairn/` file:line, for the Sync Impact Report on IPn/GPn changes;
  M15), `cairn_cost` (per-phase token attribution over the session store;
  M94).
  Read-only; reuse the hooks' `cairn_common` parser (no duplication);
  exit 2 outside a cairn repo. `/milestone` invokes them instead of
  re-deriving status by LLM; `/milestone-review` runs `cairn_impact --changed`
  when a milestone touches a principle; semantic checks stay LLM-owned.

## Conventions

- Skills state workflows; the rulebook states rules; nothing is said twice.
- Skill descriptions are written for trigger accuracy: `/hotfix`
  auto-triggers on bug reports *and on an incoming external PR* — it is
  bidirectional, authoring a fix or adopting one (M73); phase skills trigger
  on explicit intent/chips.
- Repos never pin plugin versions — whatever plugin version is installed is
  the law; a breaking change to the state-file format ships with migration
  handling in `/cairn-init` (ported from the founding spec at its removal,
  M62).

## Design Principles

IP<n> = Inviolable Principle (hard constraint; changing one requires an
explicit user decision + D-entry). GP<n> = Guiding Principle (default
stance; tradeable with stated justification). IP block first; numbers run
within each type and are never reused.

- IP1: Nothing reaches the default branch without explicit user approval at a
  gate.
- IP2: Prior state is surfaced, never silently obeyed or silently
  overridden.
- IP3: Nothing the user asked for is silently dropped (conservation:
  remainder ledger, migration ledger).
- IP4: History is never fabricated, rewritten, or renumbered — append-only
  work-logs and DECISIONS (supersede, never edit), no-invention migration,
  entomb-verbatim, IDs never reused (D-032).
- GP1: Efficient — store decisions and outcomes, not minutiae; every
  always-read surface keeps a bounded read cost: caps with outflows bound the
  item-listed files, recorded editorial passes bound the rulebook, and history
  is bounded by reading less of it, never by shrinking it (D-053).
- GP2: Reliable — one status authority; tracking travels with code;
  self-auditing; stateless resume.
- GP3: Portable — identical across repos; one-command adoption; repo
  specifics layer on top without forking the core.
- GP4: Generalizable fixes live in the shared artifact, not per-user memory.
  A defect or lesson that would recur for other users is encoded in the
  skills, rulebook, or a guard test; memory holds only per-user meta-context
  and never substitutes for shared plugin logic (corollary of D-001, GP3;
  see D-011).

## Known issues

- The merge guard's cross-repo detection is token-level only (M162): a
  spelling that restructures the command — `env GH_REPO=… gh pr merge`, a
  prior `export GH_REPO=…`, `GH_HOST`, an assignment value carrying
  whitespace, quoting, or substitution — hides the merge from the guard
  entirely (no denial, no marker check). Accepted at the M162 gate:
  documented in the merge guard's limitations docstring and the rulebook's
  approval model rather than chased mechanically (D-043's
  boundary-over-machinery stance); the enforced path stays the plain
  `gh pr merge <N>` convention the skills emit. (The `cd ../other &&`
  compound before a `gh pr merge` left this list at M163: the guard now
  denies that spelling with session-cwd guidance; the `git merge` compound
  and near-neighbours like `pushd` remain unseen per the docstring —
  corrected M163.)
- Single-author, single-environment: every workflow has been exercised only
  by the author, on macOS + Claude Code with the full model roster. The first
  external-repo pass ran at M163 (corrected M163) — `/cairn-init`'s migration
  path plus a full milestone loop on bsync, an r-package repo with a
  precursor tracking system, solo-driven with a 4-entry friction ledger — so
  "only on repos shaped around cairn's assumptions" no longer holds (bsync
  is the same author's repo, so the single-author claim itself stands); what
  remains unrun is a second person driving an adoption (author-blind
  friction; ROADMAP candidate) and any non-macOS environment. The supported collaboration
  model — one operator, contributions from people who do not run cairn — and
  the enforcement boundary it implies are stated in the rulebook's "Git and
  approval model" (D-043, M72); two concurrent cairn operators remain
  unsupported (ROADMAP candidate).
- Hooks are unverified on Windows: stock Windows lacks `python3` on PATH (it
  is `py`/`python`), so `hooks.json` chains a best-effort `py -3` launcher
  fallback after each `python3` invocation (M61) — a no-op on macOS/Linux
  (every hook exits 0 and denies via JSON stdout), but no Windows run has
  verified it.
- Conduct rules (question gates, phase closes, chapter markers, AC fencing)
  are enforced as prose: since M144 the prose-guard tests are retained but
  hand-run and gate nothing (D-109), so wording drift is caught by PR diff
  review rather than by a suite, and live honoring is only spot-verified
  (hooks snapshot at process start, so a rule's runtime effect needs a fresh
  session to observe). A deliberate architectural bet, noted plainly rather
  than papered over (corrected M144).
