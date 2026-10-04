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
`docker-image` (hadolint+build/container registry), and `generic`. This repo
runs `claude-plugin` (M215). Logic lives here (skills, rules,
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
  `/milestone-review`; review asks the merge question, and the merge ends
  the run. The close block names the plan's next workable milestone, which
  the user starts after a `/clear` (D-148). The
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
  technically backing IP1),
  `force_push_guard` (denies force-pushes to the default branch — IP1's
  never-force-push line, mechanically backed; M60), `commit_guard`
  (nudge against committing on the default branch), `memory_guard` (GP4
  memory-boundary nudge, D-017), and `idea_guard` (out-of-band idea-capture
  nudge toward a candidate row, D-042); and one PostToolUse/PostToolUseFailure
  companion — `merge_guard_post` (restores the approval marker a failed
  guarded merge consumed, deletes it on success; M60). The three nudges are
  advisory, never blocking.
- `hooks/status/` — the milestone band, a Claude Code mod (M191, D-143, rows restyled in M193, two-group rows and a close button in M194, skill rows and chapters in M195, one line per milestone in M196, one row for the band, shorter forms, and a one-glyph bar in M197, gray text with a muted label in M198, the idle row and the step's end at its turn's end in M199, a close state that a failed ROADMAP read alone does not change and every session end clears in M200, the step's end at a Stop with nothing in flight or an idle typed prompt in M201, the desktop flow track in M204, the cairn pane in M205, the id-and-title row with the track as its one progress form, a shorter desktop track, and a terminal braille track in M206, which removed the labels, chapters, skill rows, and the bar, the pane's candidate rows in M207, the pane's percent, headings, meters, and Next pill in M208, in M210 rows kept only within one repo root, a UNC share root, a step kept by a one-shot wakeup or a dropped prompt, and close-state writes only on a change, and the empty row with its `Plan` button in M213, and the `Clear` button after a cairn skill ends in M216).
  `hooks/hooks.json` names its TypeScript hooks module,
  `hooks/status/register.tsx`, under a `modules` key beside the classic
  `hooks` key; `types/index.d.ts` is its `$.state` contract, named in
  `plugin.json`. It draws one row. If `/milestone-review` runs and a
  `review` milestone exists, the row is the first one. Else it is the
  first `in-progress` milestone, else the first `review` one. The row
  gives no sign of the others. The row sits above what the hooks beneath
  draw, and the band blocks nothing. A row has a left group (the bold id,
  one space, and the title) and a right group: the flow track and its
  percent, the idle row's track and command, or a `warning` label for a
  row whose counts cannot be read (M206). The empty row (M213) has no id,
  so its left group is the title alone, and its right group only the
  buttons. The phase or skill label, the
  chapter, the next open box, the skill row, and the ten-cell bar went in
  M206. Off the terminal, only the open and close buttons carry
  `dimColor`, and in the terminal nothing does. The other Text
  leaves take the theme key `inactive`, the theme's gray, but for the
  space leaves, the `warning` labels, and the terminal track's cells.
  `band.ts` measures the parts that never shrink at one column per code
  point. The track takes the columns the row leaves after the title's
  room, at most `TRACK_COLUMNS` (52) and at least `MIN_TRACK_COLUMNS`
  (12). The room is 10 columns, or less for a shorter title. The engine
  cuts the title. The row ends in a plain `role: 'dismiss'` close button: `×` in the
  terminal, and a `✕` dim at rest on other surfaces. A press stores the
  active ids and statuses, `milestone-review` while that skill moves the
  band from the first `in-progress` row to the first `review` row, and the
  idle row's id while no row is active, in the `dismissed` state value
  (shape `dismissed-4`). The band then passes to `next(e)` until that value
  changes, so any other skill's start or end keeps a hidden band hidden
  (M206 review). An Edit, Write, or MultiEdit call that went through, on a
  path under a `cairn/` directory, reads the files again, so the track
  moves inside a long turn. `mark` and `same` in
  `band.ts` build and compare that value, and `mark` reads the step through
  `knownStep`, as the drawing does. A refresh reads `dismissed` with
  `$.state.get` and clears it with `$.state.set` at that version, reading
  again on a miss, so a press made while `reconcile` reads the `band` and
  `step` values is kept when those reads match it. A hook that changes the
  rows or the step before that clear can still clear a press made against
  the new state. A refresh writes `dismissed` only when it holds a value to
  clear (M210, made exact at the M210 review). The failed-read path in
  `refresh` decides keep or empty and writes `band` at one version the same
  way. A dropped prompt puts back the close state its own refresh cleared
  as well as the step (M210 review). A press takes
  `dismissed`'s version with `$.state.get` before it reads `band` and
  `step`, and writes through `$.state.set` with `ifVersion`, so a session
  end between the reads and the write wins (M210). Any other write in
  between drops the press too. Every `session.end`
  sets `dismissed` to null, with no branch on the reason. In the desktop app
  a `/clear` stops the session's process, and the band draws again at the
  next message (M200 live look). When the ROADMAP is found but its read
  fails, or its text is empty or only whitespace, `loadCairn` returns null
  (M210). `readCairn` returns the same state with the root it found, and a
  null state when a throw ends the read of a found ROADMAP. The
  `band` value stores that root (shape `band-4`, M210), and a failed read
  keeps the rows only when the stored root equals the found one. A failed
  read in another root, a throw from `$.session.cwd()`, and stored rows with
  no root empty the band and the pane. A throw while parsing a found
  ROADMAP keeps the rows of the same root. When no ROADMAP is found, the
  band empties. `dirname` treats a UNC share root (`\\host\share` or
  `//host/share`) as a root, so the walk stops there (M210). A `skill.prompt` hook stores a
  cairn skill, by its bare or `cairn:` name, in the `step` state value
  (shape `step-2`, with no chapter since M206). A `classic.Stop` with no `agent_id`, whose answer from
  beneath carries no `block`, clears `step` when its `background_tasks` is
  empty or absent (M201) and its `session_crons` holds no entry with
  `recurring` false (M210). So does a `prompt.submit` with origin kind
  `composer` or `bridge` and no `turnId`, unless the `expanded` state value
  is set. That hook clears `step` before `next`, and when `next` resolves
  to a `drop` it puts back the step it cleared, unless a step was set
  meanwhile (M210). A cairn `skill.prompt` sets `expanded`, and every `classic.Stop`,
  `turn.complete`, and `prompt.submit` clears it. The engine raises a typed
  slash command's `skill.prompt` before its `prompt.submit` (M201 live
  look), so that prompt keeps the step the command just set. An interrupted
  turn raises `turn.complete` with reason `aborted` and no Stop, so it keeps
  the step. Every `session.end` clears it too. A Stop that lists work
  in flight, a blocked Stop, and a subagent's Stop keep it, and so do a
  `task-notification` prompt and every `turn.complete`, which reads the
  files again and clears `expanded`. A recurring cron does not keep the
  step, so a skill that waits on one loses its step at that Stop. A
  one-shot cron that the skill did not create keeps a finished skill's step.
  `CAIRN_SKILLS` in `band.ts` lists the cairn skills, held to the
  `skills/*/SKILL.md` list that `gen_fixtures.py` writes. The skill
  event carries no agent id, so a subagent that loads a cairn skill sets it
  too. With no active milestone, whether or not a skill runs, an idle row
  names the first row of the workable list: the bold id and the title, a
  track with plan full and the pill `Planned`, and
  `/milestone-implement <id>`. A narrow row drops the track, then the
  command. The workable list is the `planned` rows
  whose dependencies are all done, by priority and then id, as `workable` in
  `scripts/cairn_next.py` computes it. A done id is a `done` row or an
  `M<digits>` file directly under `cairn/milestones/archive/`, compared at
  three-digit padding. With an empty list and a found ROADMAP (the pane
  state's `found`), the band draws the empty row (M213): key `plan-row`,
  no head Box, the gray text `No milestone ready`, and no track or tail.
  `stepLines` returns it when its `found` argument is true. The pane's next
  step is then planning, so the next-step Button reads `Plan`, and a press
  runs `cairn:milestone-plan` with empty args. `actionsFit` keeps the action
  Buttons on the empty row while its text keeps `TEXT_ROOM`, which with
  both Buttons, the open button, and the close button is 37 columns or
  more. `mark` stores no ids and a null idle id for it, so a press hides it
  until a row becomes active or workable, or the session ends. With no ROADMAP found, the band
  draws nothing.
  The Clear Button (M216, key `cairn-clear`) draws before the next-step
  Button while the `ended` value is true, on a row that draws the action
  Buttons and has room for it. A `classic.Stop` that ends a non-null step
  sets it. An idle typed prompt that enters, a cairn skill's
  `skill.prompt`, and `session.end` clear it, and a dropped prompt puts it back while no
  step is set. The render tries the row with all three action Buttons'
  columns reserved, then with two, then with none, so the row drops Clear
  first. A press runs the built-in `clear` through `run`. `session.end`
  also sets `running` to false, because the run of a `/clear` that ends
  the session may never settle.
  The flow track (M204) is the row's one progress form (M206). `flowOf`
  and `idleFlow` in `band.ts` give the model: three equal segments, plan,
  implement, and review, each a whole-number fraction. Plan is full on a
  milestone row, implement fills by tasks (full on a `review` row), review
  by criteria, and a section of zero items is empty. The percent is
  `floor(100 × sum / 3)` in whole numbers. The pill is the phase and its
  counts, `no tasks` or `no criteria` for zero items, or `Planned` on the
  idle row. Its short text, the counts alone or `none`, shows when the
  whole pill would take more than a third of the track. Off the terminal
  the track is the `Svg` element, `min(TRACK_PX (360), columns × 7)` pixels
  wide. In the terminal `brailleSpans` in `track.ts` draws it as braille
  cells on the theme key `userMessageBackground`: dots in `inactive` or the
  phase's color, denser toward the fill edge, the last speck before the
  pill in the phase's color, the pill in white bold on the phase's color,
  and a `subtle` mark at each third past the fill edge. The operator picked
  the shorter image track and the braille look from browser prototypes
  (M206).
  `track.ts` builds the SVG in the look the operator chose at the M204 live
  look: a translucent gray ground, 2-pixel specks from the left edge to the
  active phase's fill edge that thicken and take the phase's color toward
  the edge, two edge marks at the thirds, item ticks in the active segment
  past the fill edge when the items are 6 pixels apart or more, and a pill
  in the phase's color with its right edge 6 past the fill edge, clamped 1
  inside the track. An image cannot read the app's theme keys, and in a
  browser-pane preview such an image's `prefers-color-scheme` rule followed
  the browser, not the page, so the track uses one set of translucent grays
  and no such rule. The track's `alt` opens with the phase, and a milestone
  row's alt also names the counts and the percent.
  `band.ts` builds the row and `register.tsx` draws it. `reader.ts`
  mirrors the Python ROADMAP and section helpers and
  `cairn_next.workable`, held to them by shared fixtures under
  `hooks/status/fixtures/` (`gen_fixtures.py` writes `fixtures.gen.ts` for
  the `claude plugin test` cases).
  The cairn pane (M205) is a `Pane` with id `cairn`. A `/cairn-pane`
  command, registered after the `session.start` refresh, closes it when
  `$.ui.panes()` lists it open, and otherwise opens it, prints
  `no cairn ROADMAP found` when the reader finds none, or prints the
  engine's reason when the open is not placed. The band's first row also
  carries an open button, a plain `≡` and one space before the close
  button, when a ROADMAP is found, so every fit leaves 2 more columns free
  there. `loadCairn` in `reader.ts` reads the band's state and the pane's
  in one pass, and each refresh writes the `pane` state value beside
  `band`. For each active row the pane state holds the goal, the
  `## Tasks` and `## Acceptance criteria` checkbox items, a wrapped item's
  indented lines joined, and the newest five `## Work log` lines that open
  with `- `. HTML comments are dropped from a section before it is read, so
  a box inside a comment is not a pane item, though the band counts it.
  The queue is `recommend`, `workable`, and `waiting` in
  `scripts/cairn_next.py`, which `reader.ts` mirrors and
  `scripts/tests/test_status_fixtures.py` holds to each fixture's `pane`
  and `next` keys. The pane state also holds the candidate rows (M207):
  `candidateRows` in `reader.ts` reads each flush-left line that opens
  with `- ` under a `## Candidates` heading, after HTML comments are
  removed from that section, as a priority (`high` or `low` for an exact
  `[high] ` or `[low] ` opening, else `normal`) and the text before the
  first `: `. It walks the sections `candidate_count` walks, but that
  count also takes indented lines and lines inside comments.
  `test_status_fixtures.py` holds the reader to each fixture's `candidates`
  key, and to that count where no comment sits in the section. The pane draws them only
  while no row is active. `pane.ts` lays out the lines, and each line's text is
  cut to one line with an ellipsis, but for the goal, which wraps (the
  M205 live look). A line's lead and tail Boxes keep their width with
  `flexShrink: 0`, and its text Box shrinks with `minWidth: 0`, so a long
  text is cut before the tail; the line Box also carries `minWidth: 0`
  (LESSONS M194), and the live look is what shows the cut (M208).
  Each head line's tail is the band's percent for the row, from `flowOf`
  over the `band` value's counts, which `ui.render` reads beside `pane`.
  The rest of the M208 look is the operator's pick from browser
  prototypes: a blank row, a `▎`, and a gray bold uppercase label for each
  section heading, eight `■`/`□` squares beside the Tasks and Criteria
  counts, and the Next command in a pill. At the live look the operator
  asked for the phase colors (`FLOW_COLORS`): a milestone's `▎` marks and
  `■` squares take its phase's color, the queue's `▎` marks take plan's
  blue, and the pill takes the color of the phase its command runs.
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
  step until the next Stop or typed prompt, which can change the row shown
  during `/milestone-review` or show a band hidden over the row it moves
  (corrected M206: the band no longer draws a skill label).
