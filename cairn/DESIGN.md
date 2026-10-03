# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system. The core is language-agnostic; each
adopting repo declares a **toolchain profile** (`cairn/PROFILE.md`, seven slots:
verify, consistency-gate, test-doctrine, release-walk, init-detection,
greenfield-openers, changelog) that supplies the language/toolchain-specific commands the
operational skills read, instead of the core hardcoding one language (M45
spine, M46 rewire, M47 release; D-024/D-025 keep the oracle doctrine universal,
orthogonal to the profile). Five profiles ship — `r-package` (devtools/CRAN),
`python` (pytest/PyPI), `claude-plugin` (`claude plugin validate`/`test`, M192),
`docker-image` (hadolint+build/container registry), and `generic`; this repo
runs `generic`. Logic lives here (skills, rules,
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
- `skills/<name>/SKILL.md` × 10 — workflow logic; each reads the shared
  rulebook first and never restates it. Includes `cairn-triage`, the
  on-demand whole-list pass over candidates and Known issues (M173), and
  `design-interview`, a
  standalone two-phase (facts → principles) DESIGN.md elicitation interview
  (D-013), offered from `/cairn-init`'s close block; it recommends running
  the session on Fable (D-014).
- The milestone run (M202): `/milestone-plan` asks the one question set,
  then invokes `/milestone-implement` through the Skill tool, which invokes
  `/milestone-review`; review asks the merge question, or merges a
  milestone approved up front in the question set (M203, D-145), and, after the merge,
  invokes implement for the next workable milestone of the same plan. The
  agent decides everything else with a work-log line and stops only at the
  rulebook's closed stop list. The three skills stay separate, so typed
  `/milestone-implement` or `/milestone-review` resumes a stopped run.
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
  (`r-package`, `python`, `claude-plugin`, `docker-image`, `generic`); `cairn-init` instantiates one into a repo's
  `cairn/PROFILE.md`, and the operational skills read its slots.
- `hooks/hooks.json` + python3 (stdlib) scripts (M07) — the enforcement
  layer, all no-op outside cairn repos. Eight hooks: `session_context`
  (SessionStart context injection; an active milestone's cap-exempt sections
  are read-bounded to their newest content, D-063); `stop_guard` (Stop-guard on uncommitted
  `cairn/` tracking); five PreToolUse guards — `merge_guard` (single-use
  `cairn/.merge-approved` marker, bound to the PR it approves since M72,
  and, for an up-front marker, to the milestone's `Merge approval:` slot read
  from the remote-tracking default branch since M203, technically backing
  IP1; a chip-form marker is not checked against the slot, so the read
  catches drift, not an agent that skips the question),
  `force_push_guard` (denies force-pushes to the default branch — IP1's
  never-force-push line, mechanically backed; M60), `commit_guard`
  (nudge against committing on the default branch), `memory_guard` (GP4
  memory-boundary nudge, D-017), and `idea_guard` (out-of-band idea-capture
  nudge toward a candidate row, D-042); and one PostToolUse/PostToolUseFailure
  companion — `merge_guard_post` (restores the approval marker a failed
  guarded merge consumed, deletes it on success; M60). The three nudges are
  advisory, never blocking.
- `hooks/status/` — the milestone band, a Claude Code mod (M191, D-143, rows restyled in M193, two-group rows and a close button in M194, skill rows and chapters in M195, one line per milestone in M196, one row for the band, shorter forms, and a one-glyph bar in M197, gray text with a muted label in M198, the idle row and the step's end at its turn's end in M199, a close state that a failed ROADMAP read alone does not change and every session end clears in M200, the step's end at a Stop with nothing in flight or an idle typed prompt in M201).
  `hooks/hooks.json` names its TypeScript hooks module,
  `hooks/status/register.tsx`, under a `modules` key beside the classic
  `hooks` key; `types/index.d.ts` is its `$.state` contract, named in
  `plugin.json`. It draws one row. If `/milestone-review` runs and a
  `review` milestone exists, the row is the first one. Else it is the
  first `in-progress` milestone, else the first `review` one. The row
  gives no sign of the others. The phase's section is `## Tasks` in implement and
  `## Acceptance criteria` in review. The row sits above what the hooks
  beneath draw, and the band blocks nothing. A row has a left group (phase
  or skill label, one space, id, and one text) and a right group (bar and
  counts, counts alone, or a state label). The text is the running skill's
  chapter, else the section's first open box, else the title. A chapter or
  an open box follows a `→`. The bar shows with no chapter or with a chapter
  that opens with a positional label (`T2:`, `AC3:`), and not at any other
  chapter. It draws ten `█` cells: the filled ones in the phase's theme key
  (`claude` or `success`), the empty ones in the theme key `subtle`. The
  phase or skill label takes a fixed raw color, `rgb(194,122,92)` or
  `rgb(106,165,122)`. In the desktop app's dark theme, `dimColor` turned the
  theme's orange brown at a live look (M198). Only the close button
  carries `dimColor`. The other Text leaves take the theme key `inactive`, the
  theme's gray, but for the space leaves and the `warning` labels. `band.ts`
  measures the parts that never shrink at one column per code point. The
  right group takes the first of its forms that leaves the text its room,
  else its last form. The room is 10 columns, or less for a shorter text. A
  skill row drops its slash command by the same measure. The engine cuts the
  text. The row ends in a plain `role: 'dismiss'` close button: `×` in the
  terminal, and a `✕` dim at rest on other surfaces. A press stores the
  active ids and statuses, the running skill, and the idle row's id or null
  in the `dismissed` state value. The band then passes to `next(e)` until
  that list, the skill, or the idle id changes. `mark` and `same` in
  `band.ts` build and compare that value, and `mark` reads the step through
  `knownStep`, as the drawing does. A refresh decides whether to clear
  `dismissed` inside its `update` callback, so a press made while
  `reconcile` reads the `band` and `step` values is kept when those reads
  match it. A hook that changes the rows or the step before that `update`
  can still clear a press made against the new state. Every `session.end`
  sets `dismissed` to null, with no branch on the reason. In the desktop app
  a `/clear` stops the session's process, and the band draws again at the
  next message (M200 live look). When the ROADMAP is found but its read
  fails, `loadBand` returns null and the refresh keeps the band's rows. When
  no ROADMAP is found, the band empties. A `skill.prompt` hook stores a
  cairn skill, by its bare or `cairn:` name, in the `step` state value.
  While a cairn skill runs, a `tool.call` hook on
  the desktop app's chapter tool stores the title of each main-loop chapter
  that went through. Every main-loop chapter that went through reads the
  files again. A `classic.Stop` with no `agent_id`, whose answer from
  beneath carries no `block`, clears `step` when its `background_tasks` is
  empty or absent (M201). So does a `prompt.submit` with origin kind
  `composer` or `bridge` and no `turnId`, unless the `expanded` state value
  is set. A cairn `skill.prompt` sets `expanded`, and every `classic.Stop`,
  `turn.complete`, and `prompt.submit` clears it. The engine raises a typed
  slash command's `skill.prompt` before its `prompt.submit` (M201 live
  look), so that prompt keeps the step the command just set. An interrupted
  turn raises `turn.complete` with reason `aborted` and no Stop, so it keeps
  the step. Every `session.end` clears it too. A Stop that lists work
  in flight, a blocked Stop, and a subagent's Stop keep it, and so do a
  `task-notification` prompt and every `turn.complete`, which reads the
  files again and clears `expanded`. The hooks do not read `session_crons`, so a skill that
  waits through `ScheduleWakeup` or a cron loses its step at that Stop. `SKILL_LABELS` in
  `band.ts` gives each skill's label, held to the `skills/*/SKILL.md` list
  that `gen_fixtures.py` writes: `plan`, `implement`, `review`, `hotfix`,
  `triage`, `release`, `status` (for `milestone`), `brief`, `design`, and
  `init`. The skill's label takes the place of the phase label on the row.
  It draws in the muted green for
  `/milestone-review` and the muted orange otherwise. With no active
  milestone, a skill row shows the label, the slash command, and the chapter
  after a `→`. A session without the desktop app's chapter tool, such as one
  in the terminal, sets no chapter: a milestone row shows its next open
  item, and a skill row shows the label and the command only. The skill
  event carries no agent id, so a subagent that loads a cairn skill sets it
  too. With no active milestone and no running skill, an idle row names the
  first row of the workable list: `next`, the bold id, and the title, all in
  `inactive`, and `/milestone-implement <id>` in the right group, which it
  drops by the skill row's measure. The workable list is the `planned` rows
  whose dependencies are all done, by priority and then id, as `workable` in
  `scripts/cairn_next.py` computes it. A done id is a `done` row or an
  `M<digits>` file directly under `cairn/milestones/archive/`, compared at
  three-digit padding. With an empty list the band draws nothing.
  `band.ts` builds the row and `register.tsx` draws it. `reader.ts`
  mirrors the Python ROADMAP and section helpers and
  `cairn_next.workable`, held to them by shared fixtures under
  `hooks/status/fixtures/` (`gen_fixtures.py` writes `fixtures.gen.ts` for
  the `claude plugin test` cases).
- `scripts/` + python3 tools (M10) — the deterministic scripts layer, one
  writing mode among its readers (below):
  `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate), `cairn_impact` (principle
  → citing `cairn/` file:line, for the Sync Impact Report on IPn/GPn changes;
  M15), `cairn_cost` (per-phase token attribution over the session store;
  M94), `cairn_ci_paths` (`--report`: per-workflow report of
  push/pull_request triggers and their path filters, read at `/cairn-init`
  §0, M178; `--apply [--dry-run]`: the `cairn/**` `paths-ignore` insertion
  under §0's chip, M181).
  Every script reads only, except `cairn_ci_paths --apply`, the layer's one
  writing mode (lines inserted into a workflow file after a PyYAML
  post-edit check; D-135). Every import is stdlib or the shared
  `cairn_common`/`cairn_scripts`, except `cairn_ci_paths`'s guarded
  `import yaml` inside its apply path — the one non-stdlib import
  `TestStdlibOnly` admits (exit 3 when it fails; `--report` stays stdlib).
  The tracking-file readers reuse the hooks' `cairn_common`
  parser (no duplication; `cairn_ci_paths` reads workflow files only and
  walks up to `.git` itself); exit 2 outside a cairn repo (`cairn_ci_paths`:
  outside a git repo, since `/cairn-init` §0 runs before `cairn/` exists).
  `/milestone` invokes them instead of re-deriving status by LLM;
  `/milestone-review` runs `cairn_impact --changed` when a milestone touches
  a principle; semantic checks stay LLM-owned.

## Conventions

- Skills state workflows; the rulebook states rules; nothing is said twice.
- Skill descriptions are written for trigger accuracy: `/hotfix`
  auto-triggers on bug reports *and on an incoming external PR* — it is
  bidirectional, authoring a fix or adopting one (M73); phase skills trigger
  on explicit intent or on the previous skill's Skill-tool handoff in a run.
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
  gate. For a milestone merge the gate is the merge question or the plan
  question set. The plan question set counts only for a milestone whose
  promise, as that plan committed it, merges unchanged and meets none of the
  route-back cases the rulebook lists (D-145).
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
- GP2: Reliable — one status authority; tracking travels with code (owner
  mode; in guest collaboration mode — a repo the operator does not own —
  tracking is local-only, written to disk in the turn that changes the code
  and never committed, because every write outside `cairn/` would touch the
  maintainers' files or authority, D-137); self-auditing; stateless resume.
- GP3: Portable — identical across repos; one-command adoption; repo
  specifics layer on top without forking the core.
- GP4: Generalizable fixes live in the shared artifact, not per-user memory.
  A defect or lesson that would recur for other users is encoded in the
  skills, rulebook, or a guard test; memory holds only per-user meta-context
  and never substitutes for shared plugin logic (corollary of D-001, GP3;
  see D-011).

## Known issues

- `cairn_impact --changed`'s merge-base probes run through `cc.git`, whose
  10-second timeout returns failure silently — a pathologically slow
  `git merge-base` falls through to `HEAD` (a working-tree-only diff) with
  no stderr warning. Accepted at the M164 gate: documented in
  `_base_commit`'s code comment; no test witnesses the timeout path.
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
  model — one operator per repo, in owner mode or in guest mode (D-137),
  contributions from people who do not run cairn — and the enforcement
  boundary it implies are stated in the rulebook's "Git and approval model"
  and "Collaboration mode" (D-043, M72, M184); two concurrent cairn
  operators remain unsupported (ROADMAP candidate).
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
- The band's `expanded` mark (M201) has narrow gaps, accepted at the M201
  review gate with no fix planned. A subagent's Stop or turn end in the
  milliseconds between a typed cairn command's `skill.prompt` and its prompt
  clears the mark, so that prompt ends the new step. A subagent that loads a
  cairn skill sets the mark, so one idle typed prompt keeps the step. The
  `prompt.submit` hook reads and clears the mark in two steps. A Stop that a
  hooks module above cairn blocks still ends the step. The keep cases in
  `band.test.tsx` do not check their closing Stop, and no case covers the
  first gap or a session end with the mark set. Each gap leaves a wrong
  label until the next Stop or typed prompt.
