# Design

## Purpose & Scope

A Claude Code plugin providing one canonical milestone-driven development
workflow and markdown tracking system. The core is language-agnostic; each
adopting repo declares a **toolchain profile** (`cairn/PROFILE.md`, seven slots:
verify, consistency-gate, test-doctrine, release-walk, init-detection,
greenfield-openers, changelog) that supplies the language/toolchain-specific commands the
operational skills read, instead of the core hardcoding one language (M45
spine, M46 rewire, M47 release; D-024/D-025 keep the oracle doctrine universal,
orthogonal to the profile). Six profiles ship — `r-package` (devtools/CRAN),
`python` (pytest/PyPI), `claude-plugin` (`claude plugin validate`/`test`, M192),
`quarto-extension` (a render check, and a release walk that tags a version a
merge already raised or raises it at release, M303), `docker-image`
(hadolint+build/container registry), and `generic`. This repo
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
- `skills/<name>/SKILL.md` × 11 — workflow logic; each reads the shared
  rulebook first and never restates it. Includes `cairn-triage`, the
  on-demand whole-list pass over candidates and Known issues (M173), or
  over `cairn/LESSONS.md` with the argument `lessons` (M263),
  `copilot-review`, which settles Copilot's notes on one PR and answers its
  summary (M287), and
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
  M113, trimmed M146), and `copilot-review.md` (the Copilot review round
  that `/hotfix` and `/milestone-review` run on the PR in a repo whose
  `PROFILE.md` carries `# Copilot review: on`; in owner mode
  `/milestone-review` opens the PR at the start of review and its step-7
  read handles Copilot's threads, D-152, D-153 — M231; with the round off,
  four closes add a one-line note naming the opt-in line when Copilot is
  already on the PR — M244); each module carries a
  header-stated size budget (M154).
- `skills/shared/templates/` — milestone, brief, decision, CLAUDE.md section,
  source note, synthesis note, archive summary, and the LESSONS.md /
  DECISIONS.md file headers (M163).
- `skills/shared/profiles/` — the shipped reference toolchain profiles
  (`r-package`, `python`, `claude-plugin`, `quarto-extension`, `docker-image`, `generic`); `cairn-init` instantiates one into a repo's
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
- `hooks/status/` — the milestone band, a Claude Code mod (M191, D-143, rows restyled in M193, two-group rows and a close button in M194, skill rows and chapters in M195, one line per milestone in M196, one row for the band, shorter forms, and a one-glyph bar in M197, gray text with a muted label in M198, the idle row and the step's end at its turn's end in M199, a close state that a failed ROADMAP read alone does not change and every session end clears in M200, the step's end at a Stop with nothing in flight or an idle typed prompt in M201, the desktop flow track in M204, the cairn pane in M205, the id-and-title row with the track as its one progress form, a shorter desktop track, and a terminal braille track in M206, which removed the labels, chapters, skill rows, and the bar, the pane's candidate rows in M207, the pane's percent, headings, meters, and Next pill in M208, in M210 rows kept only within one repo root, a UNC share root, a step kept by a one-shot wakeup or a dropped prompt, and close-state writes only on a change, and the empty row with its `Plan` button in M213, and the `Clear` button after a cairn skill ends in M216, and the pane's Next button in M218, and the pane's Status and Clear buttons in M219, and the idle row's `Implement` button in place of its command in M220, and `Plan` and `Implement` clearing the conversation first in M221, and the pane open again after a `/clear` in M222, and the pane's blocked rows with their pull request numbers in M223, and each blocked PR's state word and Button in M224, and each open PR's unresolved thread count in M225, and the open hotfix PRs in M226, and opens that do not wait for the PR reads, a refill after an in-process `/clear`, a shared PR drawn once, and no remote credentials in the `gh` call in M230, and one ↻ Refresh on the pane's first line, the thread count alone, and the id in its phase color with no phase word in M236, and a refill after `/resume`, a PR read for a placed pane behind another tab, ⋯ only during this module's read, and one `gh api graphql` call per PR in M237, and a PR read at the first draw of a pane placed late and one PR read per start in M238, and a ⌂ Button that clears and opens the pane in place of the pane's Clear in M241, and a ✎ Button on each candidate line with a short title, while no cairn skill runs, that plans the row in M242, and an archived blocked row's PR and `archived` mark in M246, and the `◐` mark on a candidate row that an open PR's body names in M252, and `○` in place of `·` on a normal candidate row in M253, and a started row hidden in M261, and a `[parked]` row drawn last with a gray `⧗` in M284, and the summary card, goals wrapped per paragraph, headings with no accent or rule, the Next command with no pill, one layout for blocked and hotfix lines, desktop icons for the marks, hover cards, and no work-log section in M286, and each open PR's merge state mark in M301, and the count badges right after their labels in one gray in M302).
  `hooks/hooks.json` names its TypeScript hooks module,
  `hooks/status/register.tsx`, under a `modules` key beside the classic
  `hooks` key; `types/index.d.ts` is its `$.state` contract, named in
  `plugin.json`. It draws one row. If `/milestone-review` runs and a
  `review` milestone exists, the row is the first one. Else it is the
  first `in-progress` milestone, else the first `review` one. The row
  gives no sign of the others. The row sits above what the hooks beneath
  draw, and the band blocks nothing. A row has a left group (the bold id,
  one space, and the title) and a right group: the flow track and its
  percent, the idle row's track alone, or a `warning` label for a
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
  track with plan full and the pill `Planned`, and no command (M220): its
  `Implement` Button starts the milestone. A narrow row drops the track.
  The workable list is the `planned` rows whose dependencies are all done,
  by priority and then id, as `workable` in `scripts/cairn_next.py`
  computes it. In a guest repo with `# Push remote: base`, one dependency
  of a row may instead be a stack base: a `blocked` row whose milestone
  file's `Branch/PR` header names a PR URL (M268; tracking-rules
  "Collaboration mode"). `reader.ts` reads `cairn/PROFILE.md` for the mode
  and the line, and takes the stack bases from its blocked rows. A done id is a `done` row or an
  `M<digits>` file directly under `cairn/milestones/archive/`, compared at
  three-digit padding. With an empty list and a found ROADMAP (the pane
  state's `found`), the band draws the empty row (M213): key `plan-row`,
  no head Box, the gray text `No milestone ready`, and no track or tail.
  `stepLines` returns it when its `found` argument is true. The pane's next
  step is then planning, so the next-step Button reads `Plan`, and a press
  runs `clear` and then `cairn:milestone-plan` (M221), its args the short
  title of the first `[high]` candidate row that the Candidates list draws,
  under the list's `startedRefs` test, else empty (M272, M273,
  `nextTitle`). `actionsFit` keeps the action
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
  first. A press reads `ended` again and runs the built-in `clear` through
  `run`. `session.end` also sets `running` to false, because the run of a
  `/clear` that ends the session may never settle. Each run takes a number,
  and only the latest run clears `running` as it settles.
  `Plan` and `Implement` clear the conversation before they run (M221):
  for the next actions in pane.ts's `CLEARS_FIRST`, when the drawn label
  is still the next step's label, `pressNext`'s checks give the command
  with `clears`, and `pressChecked` stores the command and its args in the
  module's `heldRun` value and runs `clear` through `run` (M243).
  `session.end` takes `heldRun` before it calls `next(e)` and, when the
  reason is `clear`, runs it through `run`, unawaited. Any other end drops
  it and puts its command line in the prompt box with a toast, as `run`
  does for a refused run (`fallBack`). A `clear` run that rejects drops it
  too, and `run`'s own refusal names `/clear`. An end whose `next(e)`
  rejects, of either reason, gives a held command to `fallBack` with
  `the session end failed` (M260). While `heldRun` is set,
  `busy` makes every action press do nothing. `busy` also reads the
  shared press mark `pressCheck` (M243). The four presses `pressNext`,
  `pressStatus`, `pressClear`, and `pressBlocked`, and the ✎ press
  `pressCandidate`, pass their checks to `pressChecked`. It returns while
  `busy()`, else sets the mark before its first await, so a second press
  during the checks does nothing, in the same tick or later. When the
  checks give a held command, it sets `heldRun` before it clears the mark.
  After the mark clears, with no await between, it runs the command or
  `clear`. Checks that give no command
  clear the mark and run nothing. A session end counts itself in `ends`
  before it calls `next(e)`, and checks that settle after that count moved
  run and hold nothing. The end clears the mark beside `running`, after its
  own updates, so a press cut off by the end leaves the Buttons free
  (M255). An end whose `next(e)` rejects makes the same updates and
  clears both before it rethrows that error (M278). A write that rejects
  stops the updates but not what follows them, and its error goes on
  after them unless `next(e)` rejected first. Either way it clears only
  the run and the mark current when it began, so a press made while
  `next(e)` is pending keeps
  its own (M260). A live probe (M221 T1) showed
  that the session end of a Button's `/clear` arrives before that run
  resolves. The press is the person's consent to drop the conversation, as
  a press of Clear is, which is how the plan gate settled the IP3 point. A
  candidate line's ✎ holds `cairn:milestone-plan` in `heldRun` the same
  way (M242). A
  `Resume` or `Review` drawing whose next step has since become planning or
  implement runs the command without the clear. `Resume`, `Review`,
  `Status`, and Clear run their one command.
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
  pill in the phase's color, the pill in bold `inverseText` on the phase's
  color, and a `subtle` mark at each third past the fill edge. The phase
  colors are theme keys (`FLOW_COLORS` in `band.ts`, M217): `planMode` for
  plan, `claude` for implement, and `success` for review, so they change
  with the theme: the light theme changes plan and review, and the
  colorblind and ANSI themes change all three. M198 found the dim `claude`
  drew brown on the desktop dark theme, so the keys draw at full strength.
  The operator picked the shorter image track and the braille look from browser prototypes
  (M206).
  `track.ts` builds the SVG in the look the operator chose at the M204 live
  look: a translucent gray ground, 2-pixel specks from the left edge to the
  active phase's fill edge that thicken and take the phase's color toward
  the edge, two edge marks at the thirds, item ticks in the active segment
  past the fill edge when the items are 6 pixels apart or more, and a pill
  in the phase's color with its right edge 6 past the fill edge, clamped 1
  inside the track. An image cannot read the app's theme keys, and in a
  browser-pane preview such an image's `prefers-color-scheme` rule followed
  the browser, not the page, so the track draws from one palette and no
  such rule. The palette, between `// palette` comments in `track.ts`
  (M217), holds the mod's only raw colors: translucent grays, and the
  `PHASE_FILLS` that keep the M204 hues, darker, so the pill's white label
  and its count at 0.85 opacity reach WCAG 2.2's 4.5:1 text contrast on the
  fill (`references/wcag22.md`), which a band test computes from the built
  SVG. The track's `alt` opens with the phase, and a milestone
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
  with `- `, which the pane no longer draws (M286). `goalBlocks` in
  `pane.ts` joins the goal's lines into one wrapping line per paragraph or
  list item (M286). HTML comments are dropped from a section before it is read, so
  a box inside a comment is not a pane item, though the band counts it.
  The queue is `recommend`, `workable`, and `waiting` in
  `scripts/cairn_next.py`, which `reader.ts` mirrors and
  `scripts/tests/test_status_fixtures.py` holds to each fixture's `pane`
  and `next` keys. The next step's `title` is null except while planning,
  when `high_title` (`highTitle`) gives the short title of the first
  `[high]` candidate row whose short title no token `takenRows` counts
  names (M272, M273). The Plan press does not use that
  `title`: `nextTitle` in `pane.ts` picks the first `[high]` row the
  Candidates list draws. Since M305 the pane's Next line draws for a
  `/milestone-plan` step only while the list draws no row (the list draws
  none while a milestone is active, and `recommend` plans only with none
  active), so it names no row, and the band's Plan press is the pick's one
  reader in practice. The pane state also holds the candidate rows (M207):
  `candidateRows` in `reader.ts` reads each flush-left line that opens
  with `- ` under a `## Candidates` heading, after HTML comments are
  removed from that section, as a priority (`high`, `low`, or `parked` for
  an exact `[high] `, `[low] `, or `[parked] ` opening, else `normal`;
  `parked` since M284), the short title (the
  text before the first `: `, else before the first ` — `, else all of it;
  M251, tracking-rules "Candidate short title"), and the text: all of it
  after the token, trimmed as the title is (M293). It walks the sections
  `candidate_count` walks, but that count also takes indented lines and
  lines inside comments.
  `test_status_fixtures.py` holds the reader to each fixture's `candidates`
  key, and to that count where no comment sits in the section. The pane
  draws them only while no row is active. Every candidate line sets `grow`. While `acts`
  is true, a line whose short title is not empty carries the `plan`
  Button, drawn as a `secondary` Button labeled `✎`
  (`PLAN_CANDIDATE_LABEL`), key `cairn-pane-plan-<index>`, in a `-plan`
  Box (M242). Off the terminal that Box has no key and is placed
  `position: 'absolute'`, `top: 0`, `bottom: 0`, `right: -8`, past the row's
  edge, where the pane clips it, with `hover: { right: 0 }`, and centers its
  Button with `alignItems: 'center'`. So ✎ shows only while the
  pointer is over its line, in the 4 columns that the info glyph before it
  keeps as its right margin (M290). A Button drawn under `display: 'none'`
  takes no click in the desktop app even once revealed, and one moved in by
  an offset does (M290's probe). The terminal draws ✎ as before and has no
  info glyph. `paneLines` draws the lines by level (`LEVEL_RANK`: high,
  normal, low, parked), each level in ROADMAP order, and `state.candidates` stays
  in ROADMAP order (M280). A parked row's mark `⧗`
  (`PRIORITY_MARK.parked`) and its title draw in `PARKED_KEY`, the theme's
  `permission` blue, and its desktop icon in `ICON_COLORS.blue`, while a
  low row's stay gray (M284, M305, D-184, D-203). `high_title` and `nextTitle` pick only `[high]` rows, so they never
  name a parked row. `cairn_validate`'s `candidate order` advisory
  WARNs on each row the file holds below a row of a lower level, `parked`
  ranking lowest. The line's `target` is its index and its `title` the short
  title. `pressCandidate` in register.tsx runs its checks under the shared
  press mark through `pressChecked` (M243). Its checks give no command on
  a set step, on stored state that draws no candidates (no ROADMAP found,
  or an active milestone), or on a stored row at that index that is
  missing or has another title. Else `pressChecked` sets `heldRun` to
  `cairn:milestone-plan` with the title and runs `clear`, and the
  `session.end` hook runs the held command as it runs a `Plan` press's
  (M242 review).
  A candidate row whose non-empty short title equals a `started` item's
  title exactly (M252), or that a counted started token marks (M258),
  draws no line (M261). `paneLines` filters these rows out before the
  heading, so the heading's count is the number of drawn lines and no
  heading is drawn when none is left. A drawn line keeps its row's index in
  `state.candidates` as its key and `target`. `paneLines` takes the items as its
  `started` argument, which register.tsx passes only while the band's root
  is the stored root. The pane lists candidate rows only while no milestone
  is active, so a milestone PR hides its row only in a checkout whose
  ROADMAP has no active row, such as one of the default branch.
  The pane state also holds the `blocked` rows
  (M223), in ROADMAP order, each with the number of the pull request that
  its milestone file's first `Branch/PR` header line names. The number
  comes from the first `https://github.com/<owner>/<repo>/pull/<n>` URL
  before any `companion:` entry, and a missing file, a failed read, or no
  such URL gives none. `blocked` and `pr_number` in
  `scripts/cairn_next.py` compute the same list, which `reader.ts`
  mirrors and `test_status_fixtures.py` holds to each fixture's `blocked`
  key. `cairn_next.py` prints the number after each "Externally blocked"
  line. The pane draws a Blocked section after the queue in every
  state, the number in the line's tail. `prLine` in `pane.ts` draws a
  blocked line and a hotfix line in one layout (M286): a state mark, the
  id (`fix` for a hotfix), the title, and a tail of `#<n>`, `archived`,
  the word, and an open PR's merge mark (M301). A guest-mode handoff sets its
  milestone `blocked` with the PR URL in its header, so the section lists
  the PRs that wait on maintainers. The header is the text before the
  first `## ` heading, and a number has at most 15 digits, so both sides
  read it the same.
  Each blocked row also has `archived` (M246). It is true when the row's
  path is not a regular file and exactly one file under
  `cairn/milestones/archive/` has the row's canonical id, reads, and has a
  `**Status:**` paragraph (that line through the next line of only spaces
  and tabs) starting with `done`. The number and URL then come from the
  first pull URL in that paragraph (`archived_text` and
  `status_paragraph` in `cairn_next.py`, mirrored in `reader.ts`). The
  pane draws `archived` after the number and before the state word, and
  `cairn_next.py` prints `(PR #<n>, archived)` or `(archived)`. A merged
  one carries Finish, and an archived line carries no Revise or Check.
  In guest mode, `/milestone-review`'s archived-file arm (D-159) sets a
  `blocked` row to `done` and runs a named part of step 9, writing
  nothing to the archive and making no issue write. In owner mode it
  reports and stops. The pane state's shape tag is `pane-8` (M293).
  Each blocked row also keeps that pull request's URL up to its number
  (M224, `prUrl` and `pr_url`), and the pane reads each PR's state
  from it. `readPrs` in `register.tsx` runs one call per distinct URL
  through `$.process.run` (`readPr`), side by side, with a 15-second
  timeout each. It writes each word, with its counts since M225 and its
  merge state since M301, to the
  `prs` state value by URL. Since M237 a github.com URL takes one `gh api
  graphql` call for the word and the counts. A URL of another form, as a
  hotfix's on another host, takes one `gh pr view <url> --json
  state,reviewDecision,mergeable` call (`PR_VIEW_FIELDS`, `prViewRead`)
  for its word and merge state and gets no counts. It runs
  after each pane open (the `/cairn-pane` command, the band's open
  button, the session-start reopen, which skips it when its start
  already read, M238), at a press of the ↻ Refresh Button, which first
  reads the files again, and at the start hooks and the first draw
  described below. The three opens start the read with `void readPrs($)`,
  or the reopen skips it as above, and they return before it settles
  (M230). The press still waits for it. The ↻
  is the pane's one Refresh (M236). `paneLines` gives it to the first
  line, the card's `card-repo` line since M286, whenever a ROADMAP is
  found. While `acts` is true,
  `home` comes before it, drawn as a `secondary` Button labeled `⌂`
  (`HOME_LABEL`), key `cairn-pane-home`, in a `-home` Box (M241). That
  line sets `tailGrows`, and the render gives its tail Box `flexGrow: 1`,
  so the ↻ Box sits at the right end after the name and the counts (M291;
  before it, the line's empty text grew). The `reading` state value (tag `reading-1`) is true from the
  start of any read until the newest read started settles. The ↻
  Button's label is `⋯` (`READING_LABEL`) while it is true and
  `inFlight` is above 0 (M237). `inFlight` is a module-level count of
  this module's unsettled reads. So a stored true that a reload or a
  failed write left draws ↻ at the next draw. A `dimColor`
  drew no change on the desktop app's native Button at the M236 live
  look, so the label changes instead. A module-level `pressing` flag makes a press during an
  earlier press's read do nothing. The flag is not stored, so after a
  reload a press reads again even while a stored `reading` is still true.
  After its refresh, a `classic.SessionStart`
  with source `clear` or `resume` also starts the read without waiting
  (M230, M237). It does so when `$.ui.panes()` lists the pane placed,
  shown or behind another tab. A pane listed but not placed owes the
  read, and the Pane's first draw starts it (`owed`, M238). The hook
  then lists the panes again and reads if the pane is placed and still
  owed, so a pane placed and drawn during the first list reads with no
  further draw (M256). An open before that draw, or a session end, clears
  the debt. The hook counts `ends` before its first await, and after a
  session end it reads and owes nothing, so a later start's debt stays
  that start's (M260). A start's reopen,
  its `classic.SessionStart`, and the owed draw read once between them:
  the first to read sets `startRead`, which holds until the next session
  end. The hook checks `startRead` again after it awaits the pane list
  (M238 review).
  `paneOf` holds the one `$.ui.panes()` call (M238). No timer and no turn
  end starts a read, at the operator's word. A read that starts while another
  runs still runs, and only the newest read started writes its words
  (M224 review). `wordOf` in `pane.ts` maps a state and a decision:
  MERGED to `merged`, CLOSED to `closed`, OPEN by its review decision to
  `changes requested`, `approved`, or `in review` for any other or none,
  and another `state` to `unknown`. `prRead` in `counts.ts` reads it from
  a graphql reply, and `prViewRead` in `pane.ts` from a `gh pr view` reply.
  A rejected call, a non-zero exit, or a reply with no pull request reads
  `unknown`. The word follows the number in the
  line's tail. `PR_BUTTON` gives a `merged` line a `Finish` Button that
  runs `/cairn:milestone-review <id>`, a `changes requested` line a
  `Revise` Button that runs `/cairn:milestone-implement <id>`, and a
  `closed` line a `Check` Button that runs `/cairn:milestone`, three of
  the routes `/milestone` gives a handed-off PR (corrected M309). None of these three Buttons
  clears first. A press reads the word as it is now and runs through
  `run`, as the Status press does. Like the Status press, it does nothing
  while another run is in flight or a cairn skill's step runs (M224
  review). The Buttons stay drawn while a step runs. A test answers the mod's
  `$.process.run` with an `on('process.run')` hook (M224 probe), and a
  desktop Code session's mod runs `gh` from the app's `PATH`.
  The graphql query (M225, `counts.ts`) names the URL's owner, repo, and
  number, and returns `state`, `reviewDecision`, `mergeable` (M301), and
  `reviewThreads(last: 100)` with each thread's `isResolved` (M237).
  `mergeOf` in `pane.ts` gives a word in `OPEN_WORDS` its merge state:
  MERGEABLE reads `mergeable` and CONFLICTING reads `conflicts`. UNKNOWN,
  which GitHub answers while it computes the value, as just after a push,
  any other value, an absent field, and a word not in `OPEN_WORDS` read
  null. Threads that fail the shape check leave the merge state standing.
  `prLine` ends the tail of a line whose read has a merge state with its
  `MERGE_MARK` after the word: the `mergeable` icon, a green merge symbol
  (`✓` in the terminal), or the `conflicts` icon, a red disc with a cross
  (`✗`). A null merge state draws no mark until a later read. No timer
  re-reads an UNKNOWN answer. A row with a tail icon centers on the
  desktop (`centers` in register.tsx).
  Only a word in `OPEN_WORDS` carries counts. `prNodes` checks the
  threads' shape, and `countPr` gives one count, `unresolved`:
  the threads with `isResolved` false, a bot's threads included. Until
  M236 a second count showed the reviews and conversation comments after
  the author's last comment, review, or commit. GitHub links no reply to a
  review, so that count took items with nothing to answer, such as a
  Copilot summary review with no threads, and the operator dropped it. The
  count covers the newest 100 threads. Threads that fail the shape check
  leave the counts null and the word standing. The `prs` value holds `{ word, counts, mergeable }` per URL under the
  tag `prs-4` (M301). It is written once every call settles, so a ↻ press keeps
  the earlier count drawn until then. When the count is above zero,
  `paneLines` draws `blocked-<id>-counts` at indent 4 under the line. The
  count sits in the line's text part, which a narrow pane cuts.
  The summary card (M286) leads the pane: `cardLines` in `pane.ts` gives
  `card-repo` (the project name bold in the line's text, which is cut
  first, then open PRs and issues in a tail that grows, `?` with no
  numbers; M291), `card-candidates`
  (the rows `drawnCandidates` draws, per level, the same filter the
  Candidates list uses), `card-milestones` (planned is `workable` plus
  `waiting`, blocked is `blocked`), and `card-release` when the release
  read holds one. The render draws `card` lines in one Box with a round
  border in `subtle`. `readPrs` looks up the root, the guest flag, and the
  base remote URL once (`baseOf`) for `readHotfixes` and `readRepo`. In
  `readRepo` (`repo.ts` holds the pure parts), `repoArgv` turns a
  github.com remote URL (scp-like, `ssh://`, or `http(s)://`) into one `gh
  api graphql` call that counts open pull requests and issues by
  `totalCount`, and any other host runs none. `repoCounts` gives both
  numbers or none, and a read with none keeps the last good numbers for
  the same root. Outside guest mode, `git describe --tags --abbrev=0
  --match 'v*'`, `git log -1 --format=%ct <tag> --`, and `git diff
  --no-renames --diff-filter=A --name-only <tag> HEAD --
  cairn/milestones/archive/` give `doneSince` the tag, the whole days to
  the read's start, and the archived count. `projectName` gives the name:
  the repo part of a github.com URL, else the folder holding a `.git`
  common dir (`git rev-parse --path-format=absolute --git-common-dir`, run
  only when the base URL is not a github.com one or there is none), else
  the root's last segment. `webOf` gives the repo page,
  `https://github.com/<owner>/<repo>`, of a github.com URL whose owner and
  repo both match `[A-Za-z0-9._-]+`, are not `.` or `..`, and are at most
  GitHub's 39 and 100 characters, and null
  otherwise, since a `Link` whose `href` is not spelled as
  `new URL(href).href` refuses the whole pane (M311). The `repo` state
  value (`{ root, counts, done, name, web }`, tag `repo-4`) holds them,
  and the pane draws them only while its root is the band's. With none
  for that root, `paneLines` names the root's last segment (M291).
  With a `web`, `cardLines` gives the name span that page as its `href`,
  and each count and its word the page's `/pulls` or `/issues` (M311).
  Off the terminal the render draws the name, and each run of spans with
  one `href` (a count and its word), as one `Link` in a `Text` with
  `wrap: 'truncate-end'`, so a count and its word light as one link.
  Inside the `Link` each span is a `Text` with the same wrap, in its own
  style, the theme's `text` color where it names none, with
  `underline: false`: at the M311 live look the
  desktop drew a bare `Link` in a link's blue, underlined, and the
  operator asked for the card's look. The terminal
  draws no `Link`: one without OSC 8 draws the URL after the text, which
  would push ⌂ and ↻ off the row. No read for the root, a remote on
  another host, no remote, and a name `webOf` refuses draw no link.
  A mark span may name an icon (`icons.ts`, M286). On a surface other than
  the terminal the render draws it as a 14-pixel `Svg` in a fixed color,
  since an image has no theme signal, and centers the row. The terminal
  draws the span's glyph. A line's `full` holds its whole text on head,
  task, criterion, workable, waiting, blocked, hotfix, and candidate lines,
  and none when empty. A candidate line's `full` is its row's whole text
  after the priority token (`CandidateRow.text`, trimmed as the short title
  is), not the short title the line draws (M293). Off the terminal, a card
  is an unkeyed Box with `position: 'absolute'`, `display: 'none'`, a round
  border, and the `userMessageBackground` ground. The card of a head,
  task, criterion, workable, waiting, blocked, or hotfix line sits in the
  line's keyed Box at `bottom: 1`, with `hover: { display: 'flex' }`, so
  the pointer over the line reveals it above the row. A candidate line's
  card names the line's ⓘ hover group instead (described after the
  placement), and it sits in the line at `bottom: 1` when it opens above,
  or after every line in the pane's root Box when it opens below (M294).
  The card has no key, because a keyed Box scopes its own
  hover and a hidden scope is never under the pointer. A candidate line's
  parked ✎ Box has no key for the same reason (M290).
  Where a candidate card opens (M294): `cardRows` estimates its rows (a
  greedy wrap at spaces at the pane's `bodyColumns` less 4, in code
  points, plus 2 border rows), and the line's `rowsAbove` is its row in the
  pane's tree (each line one row, plus the summary card's 2 border rows).
  `cardPlaces` reads the Pane props `bodyColumns`, `scroll.offset`,
  `scroll.bodyRows`, and `placement`. The line's row in the window is its
  `rowsAbove` less the offset, and the room is `bodyRows` in a dock and,
  inline, the fewer of `bodyRows` and the tree's rows. `cardPlace` puts the
  card above when it fits, else below, else on the side with more rows
  (above on a tie), cut to that side's rows, and draws none on a side of
  fewer than 3 rows. A cut card holds `cardCut`'s text (the longest run of
  whole words that fits with ` …` after it) and sets no `height`, since a
  fixed height left empty rows where the desktop wraps more per row than
  `cardRows` counts; that wrap can also make a cut card a row or two
  shorter or longer than its cap. Each card that opens below is drawn
  after every line in the pane's root Box, at `top` equal to its line's
  `rowsAbove` plus 1, so it paints over the rows under its line. The
  cards of the other lines still open upward.
  A candidate line with a `full`, one whose short title is empty included,
  sets `info` (M293). Off the terminal it draws,
  just before ✎, a hidden unkeyed Box that the line reveals, holding a gray
  `Text` `ⓘ` (`INFO_LABEL`) with `hover: { scope: 'cairn-info-<line key>',
  bold: true }`. Its card's `hover` names the same `scope`, so the card
  opens only from the glyph and not with ✎ (M290). In the desktop app a
  `Text` in a group heats it, but a `Box` whose `hover` only names the group
  does not, around an image or a glyph, hidden or shown (M290's probe).
  The same read lists the open hotfix PRs (M226, `readHotfixes`). Since
  M230 the blocked URLs' reads (`readPr`) start beside the list call, and
  the hotfix URLs that no blocked row names are read once the list
  settles.
  A hotfix has no ROADMAP row, so the PR is its only record. The read
  needs the band's root. In it, the mod picks the base remote as
  `cairn_common.base_remote` does: `collaborationMode` in `reader.ts`
  reads `cairn/PROFILE.md`, and guest mode runs `git remote`. Then `git
  remote get-url` gives the remote's URL, and `withoutUserinfo` drops the
  userinfo of an `http://` or `https://` URL, keeping every other form
  (M230). No URL means no list call and
  an empty list. Otherwise one `gh pr list --repo <url> --state open
  --author @me --limit 100 --json number,title,url,headRefName,body` call
  runs in the root (`body` since M252). `hotfixPrs` in `pane.ts` keeps an entry only with a
  `headRefName` that starts with `hotfix-`, a string `url`, and an
  integer `number`. A call that rejects, exits non-zero, or prints no JSON
  array keeps the last good list when it was read for the same root. The
  list's URLs join the blocked URLs for the word and count reads. The
  `hotfixes` state value (`{ root, prs, started }`, tag `hotfixes-2` since
  M252) is written with the words. `startedRows` in `pane.ts` reads the
  same result into `started` (M252): for each entry with an integer
  `number` and a string `body`, whatever its branch, each body line that
  opens with exactly `Candidate row: ` gives `{ title, number }`, the rest
  trimmed, a blank rest giving none. A line inside a fence gives none
  (M257): a line opening with three backticks or three tildes after
  optional spaces toggles the fence, which starts closed in each body.
  A failed call keeps or empties
  `started` with `prs`. In owner mode `/hotfix` and `/milestone-review`
  write those lines in the PR body, one per candidate row that the merge
  removes or narrows; a guest PR body carries none. `takenRows` in
  `reader.ts` reads each candidate row's ` — started M<NNN>` or
  ` — started #<n>` token, followed by the row's end or a character that
  is not an ASCII letter or digit (corrected M272), into the pane state's
  `taken` list (`{ title, ref }`, tag `pane-6`, M258; `pane-8` since
  M293), keeping an M token only while
  the table holds its id as `planned` or `blocked` and the id is not an
  archived blocked row's (M246), and giving it at three-digit padding.
  `startedRefs` in `pane.ts` marks a row by its body lines, its `#<n>`
  tokens whose n the held hotfix list has, and its M tokens, and
  `paneLines` draws no line for a marked row (M261). `/milestone-plan` writes the M
  token on each row a plan absorbs, both modes, and `/hotfix`'s guest arm
  writes the #n token after its create. `/cairn-triage` proposes adding a
  missing M token and removing a dead token at its gate (M259), except a
dead token whose removal changes the row's short title (M299). The pane draws the list only while the band's root is
  its root, under a Hotfixes heading after Blocked and before the
  candidates. An entry whose URL is a blocked row's draws on that blocked
  line only, and the heading's count leaves it out (M230). The section has
  `hotfix-<n>` lines with the word and an open PR's merge mark in the tail and
  `hotfix-<n>-counts` at indent 4, and no Button.
  `pane.ts` lays out the lines, and each line's text is
  cut to one line with an ellipsis, but for the goal, which wraps (the
  M205 live look). A line's lead and tail Boxes keep their width with
  `flexShrink: 0`, and its text Box shrinks with `minWidth: 0`, so a long
  text is cut before the tail; the line Box also carries `minWidth: 0`
  (LESSONS M194), and the live look is what shows the cut (M208).
  A head line's lead is the milestone's id, bold, in its phase's color,
  with no phase word, which the operator dropped at the M236 live look.
  Each head line's tail is the band's percent for the row, from `flowOf`
  over the `band` value's counts, which `ui.render` reads beside `pane`.
  The rest of the look is the operator's pick from the M286 browser
  prototypes (look B), changed at its live looks: a blank row and a bold
  label for each section heading, with any tail at the right end, a
  six-cell `━`/`─` meter beside the Tasks and Criteria counts in the
  milestone's phase color, and since M289 a badge for the Blocked,
  Hotfixes, and Candidates counts (`badge.ts`: an `Svg` pill in one fixed
  gray fill with a white number on the desktop, the padded number in
  `inverseText` on `inactive` in the terminal). Since M302 the badge sits
  in the heading's lead right after the label and a space, and those
  three headings have no tail. The rest of the look has the head
  line's title in bold, and the Next
  command after a `→`, both bold in the color of the phase the command
  runs. The live looks dropped look B's rule after each heading, which the
  desktop drew as two lines, and took the desktop app's task-list marks.
  Each item mark takes two spaces after it. The M208 look (a `▎`, gray
  capitals, eight squares, and a pill) is gone, and with it the plan
  color the queue's headings took. The text colors are the theme keys of
  `FLOW_COLORS` (M217), and a high-priority candidate's `↑` glyph takes the
  implement key. The desktop icons, that `↑` included, take fixed colors
  (`icons.ts`), since an image has no theme signal.
  While `knownStep` reads no step, `paneLines` gives the Next line an
  `action` label from `NEXT_LABELS`, which moved to `pane.ts` so the band
  and the pane read one map (M218). The pane's `ui.render` draws it as a
  `secondary` Button, key `cairn-pane-next`, in a `next-action` Box with
  `flexShrink: 0` and `marginLeft: 1` after the command, so the command is
  cut first. A press is the band's `pressNext`. A pane gets no `isWorking`
  prop, so the Button also shows during a turn outside a cairn skill, and
  `$.command.run` queues such a press until the session is idle.
  At the same times, with that label, `paneLines` gives the Next line `buttons` (M219):
  `status`, which the pane's `ui.render` draws after `next-action`
  as a `secondary` Button, key `cairn-pane-status`,
  in a Box keyed `next-status` with `flexShrink: 0` and
  `marginLeft: 1`. In the desktop app, a click
  on a pane without keyboard focus only gives it focus, and no `ui.press`
  reaches the mod (M219 probe). A pane Button then takes a second click.
  The labels `STATUS_LABEL` and `CLEAR_LABEL` moved to `pane.ts`, so the
  band and the pane read one place (since M241 the pane reads only
  `STATUS_LABEL`). A press is the band's `pressStatus`.
  Until M241 the Next line also carried `clear` while `ended` was true.
  The first line's ⌂ took its place, and `paneLines` lost its `ended`
  parameter. A ⌂ press runs `pressHome`: under `busy`, with no `ended`
  check, it sets the module mark `homeRun` before its first await, so a
  second press in the same tick finds `busy` true. It takes the mark back
  when it finds a step set, when a session end came during its step
  read (M260), or when that read rejects, in a `finally` (M278), and
  otherwise runs `clear` through `run`. A
  refused run clears the mark. `busy` also reads the
  mark, so every action press does nothing while it is set. `session.end`
  takes and clears the mark, and at reason `clear` it calls `openHome`
  unawaited, which opens the pane and toasts a refused or unplaced open.
  The clear's start hooks read the files and the PRs, so `openHome` starts
  no read. The press is the person's consent to drop the conversation, as
  a press of Clear is (IP3).
  A cairn pane shown at a `/clear` is open after it (M222). A press
  of ⌂ or a Clear, `Plan`, or `Implement` Button ends the session with reason
  `clear` in the same process, and nothing closes the pane (M222 probe). The
  host's state starts empty under the new session id, and no
  `session.start` fires, so a `classic.SessionStart` hook with source
  `clear` refreshes the band and the pane, and a placed pane reads its PRs
  again (M230, M237). Source `resume` does the same (M237). The hook
  cannot tell a resume in the process from a resumed start, so a resumed
  start reads the files twice. A resumed start still reads the PRs once,
  and a pane listed but not placed reads them at its first draw (M238). A
  typed `/clear` in the desktop app ends the process with reason `other`,
  and the next process starts with no pane at the first message after the
  clear. So at an `other` end with the pane listed, shown, and placed, the
  `session.end` hook adds `$.session.root()`, which a shell `cd` does not
  move, to the store key `reopen`, and
  the next `session.start` in that folder clears the mark and opens the
  pane after its refresh, when a ROADMAP is found. A reopen that is not
  placed waits with no toast. A reopen of a pane not shown before it sets
  the in-process flag `reopened`, which the next `/cairn-pane`, turn end,
  or session end clears. A `/cairn-pane` that finds it set leaves the pane
  open and prints `cairn pane opened`, since that command is the first
  message after the clear. A pane behind another pane's tab or waiting
  undrawn at the `other` end is not marked. An app quit or a signal that
  ends with `other` also brings the pane back at the next session in that
  folder. The API does not say which ends those are, and none was checked.
  `resume`, `prompt_input_exit`, and `logout` ends mark nothing. The desktop
  app is the surface checked live, and tests cover the mod's side in the
  terminal.
- `scripts/` + python3 tools (M10) — the deterministic scripts layer, one
  writing mode among its readers (below):
  `cairn_status` (snapshot), `cairn_next` (Depends-on readiness),
  `cairn_validate` (mechanical consistency gate), `cairn_impact` (principle
  → citing `cairn/` file:line, for the Sync Impact Report on IPn/GPn changes;
  M15), `cairn_cost` (per-phase token attribution over the session store;
  M94), `cairn_ci_paths` (`--report`: per-workflow report of
  push/pull_request triggers and their path filters, read at `/cairn-init`
  §0, M178; `--apply [--dry-run]`: the `cairn/**` `paths-ignore` insertion
  under §0's chip, M181), `cairn_versions` (a version marker's `version:`
  line along the first-parent chain: the tip's version, the first commit of
  its unbroken run, and its tag state, or with `--changed-by` the version one
  commit set, for the quarto-extension release walk, M303, and the
  merge-time tag handoff in `/milestone-review` step 10, M304; it needs a git
  repository with full history, not a `cairn/` directory).
  Every script reads only, except `cairn_ci_paths --apply`, the layer's one
  writing mode (lines inserted into a workflow file after a PyYAML
  post-edit check; D-135). Every import is stdlib or the shared
  `cairn_common`/`cairn_scripts`, except `cairn_ci_paths`'s guarded
  `import yaml` inside its apply path — the one non-stdlib import
  `TestStdlibOnly` admits (exit 3 when it fails; `--report` stays stdlib).
  The tracking-file readers reuse the hooks' `cairn_common`
  parser (no duplication; `cairn_ci_paths` reads workflow files only and
  walks up to `.git` itself); exit 2 outside a cairn repo (`cairn_ci_paths`:
  outside a git repo, since `/cairn-init` §0 runs before `cairn/` exists;
  `cairn_versions`: outside a git repo or in a shallow clone, since it reads
  only git history and needs all of it).
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
  external-repo pass ran at M163 on bsync, the same author's r-package repo
  (corrected M163). Unrun: a second person driving an adoption and any
  non-macOS environment. Two concurrent cairn operators are unsupported. Both
  gaps are ROADMAP candidates. The rulebook's "Git and approval model" and
  "Collaboration mode" state the supported model (D-043, D-137).
- Hooks are unverified on Windows: stock Windows lacks `python3` on PATH (it
  is `py`/`python`), so `hooks.json` chains a best-effort `py -3` launcher
  fallback after each `python3` invocation (M61) — a no-op on macOS/Linux
  (every hook exits 0 and denies via JSON stdout), but no Windows run has
  verified it.
- The claude-plugin profile has gaps found at the M192 and M215 reviews,
  with no fix planned. The release walk bumps every plugin to one version
  and one `v<version>` tag, and cannot bump an entry whose `source` is
  another repo. A plugin with no `plugin.json`, or one only in a subfolder
  with no root marketplace, is neither validated nor detected. The verify
  commands and binary paths are POSIX and macOS only. The test-doctrine
  names the lowest Claude Code version the mod supports as a dependency,
  but cairn's own repo states no such version. If an adopter's real plugin
  repo hits one, it becomes a `/hotfix` or a candidate row. Routed from
  candidates 2026-10-06; added 2026-10-01 — M192 review (R10), M215 review.
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
- The status mod's band and pane have small gaps, accepted at the M191 to
  M221 reviews with no fix planned. On 2026-10-06 they moved here from
  fourteen ROADMAP candidate rows, and the git history of `cairn/ROADMAP.md`
  holds each row's full text. If a gap shows in a real session, it becomes
  a `/hotfix` or a candidate row.
  Reading the ROADMAP: a file cut mid-table during a write reads as
  shorter, and a file deleted and recreated reads as absent. An empty or
  unreadable file before any good read prints `no cairn ROADMAP found`.
  So do the first failed read after a reload from pre-M210 code and a
  moved pane shape tag (`pane-8` since M293) after a reload, until the
  next refresh (corrected M223, M246, M258, M272, M293). A pane parse
  throw keeps the band's old rows, and a throwing refresh skips the
  command's registration. Duplicate ids give duplicate pane keys and share
  one percent. The pane matches `## Candidates (dropped)` and draws a bare
  mark for an empty title. It shows the date and links of a row with no
  `: `. `cairn_next.py` reads no PRs, so its planning title counts every
  `#` token, and an open PR body hides nothing from it, where the pane's
  pick checks both (M273).
  `cairn_status` counts commented and indented candidate rows, and the pane
  does not. The band counts a box in an HTML comment, and the pane does not.
  JS and Python differ on a BOM, on `\x1f`, and on trim.
  Session state: the stored root is compared as an exact string, and
  `dirname` takes `//a/b` and `\\?\UNC\srv` heads as share roots. A
  bare-named project skill such as `hotfix` sets the band's skill.
  Background work or a one-shot wakeup that the skill did not start keeps
  a finished skill's step. A rejecting `next(e)` clears the step and loses
  Clear. A subagent's cairn skill shows Clear, a dropped cairn command loses
  it, and a closed band hides it. The Stop and drop branches write `ended`
  apart.
  Presses: a press that loses the version race, or comes mid-run, says
  nothing. A press drawn before a session end hides the band after it. A
  press before the `isWorking` redraw queues. A press queued outside a cairn
  skill can run after the turn starts one. A pane Plan or Implement press
  in a working turn queues its `/clear`. A `/clear` with no clear end holds the queued command, and a
  reload before the end loses it. A ⌂ press's `/clear` with no session end
  keeps `homeRun` set, so every action press does nothing, with no toast,
  until a session end (M241 review). A refused press with a draft sends
  `draft/cairn:…` as prose. `Review` can act on a hidden milestone, and
  `Plan` starts a milestone that just turned workable. Pane ⌂ shows
  outside a cairn skill and with the band closed (corrected M241: the
  pane's Clear, which this named, is gone).
  Layout: `refresh` writes band and pane apart, so a frame can drop a head
  line's percent or show `Plan` or the empty row out of date. Under about
  39 columns a band title gets less than its 10 columns, and under about 38
  the pane's Boxes overflow. At the 44-column dock the Next line's
  Buttons can cut its command (M286 live look). Desktop Buttons count at terminal
  width, and the track uses a 7-pixel column estimate (`TRACK_COLUMNS`, 52)
  that no test ties to the app. The engine's scrub can drop the track's
  `clipPath`. The `━`, `─`, `●`, `◌`, `⊙`, and `↑ ○ ↓` marks are
  ambiguous width in CJK terminals.
  Colors: nobody checked the gray Buttons or the terminal track in other
  themes. The desktop icons take fixed colors that no theme moves (M286),
  checked only in the dark theme at the live look. The desktop track's plan blue and implement orange differ
  from the pane's `planMode` teal and `claude` orange.
  Tests: none covers the `vscode` and `mobile` surfaces, presses a stale
  Clear, or starts a skill by a press. The M206 desktop sweep has no Button
  rows and starts at 40 columns. The press, refresh, and session-end suites
  draw on the terminal only. M219's Review lists four more gaps.
  Code: `CairnPaneState` and `PaneState` are hand-kept copies, and
  `render()` lists the archive three times. The desktop can draw `≡` as a
  native button over its 2 reserved columns.
- The pane's PR reads and reopen have small gaps, found at the M222 to
  M236 reviews with no fix planned. An ssh host alias remote shows no
  hotfix section, a non-github.com PR gets no counts, and titles draw as
  GitHub gives them. A primary PR URL written after a `companion:` entry
  gives no number. A non-UTF-8 milestone file can give a number in the
  pane and none from `cairn_next.py`. `counts.ts` keeps its own PR URL
  pattern. Any start in a marked root takes the reopen mark, a `-p` run
  included. The mark's store write has no version check, marks never
  expire, and `markReopen` runs before `next(e)`. Nobody looked at a
  `classic.SessionStart` with source `fork`, which can also start with
  empty state. After a reload, an old module's detached read can write
  older words or clear `reading` during a newer read. If the list read
  throws, the blocked views run on and their results are dropped. The
  hotfix filter compares URLs as exact strings, so a case or form
  difference draws a PR twice. A hotfix-only PR waits for the list before
  its own read. A head line shows its phase by color alone, as the
  operator chose at the M236 live look, so a red-green colorblind reader
  can confuse the implement orange and the review green. If a gap shows
  in a real session, it becomes a `/hotfix` or a candidate row. Routed
  from candidates 2026-10-10; added 2026-10-06 — M222–M226, M230, and
  M236 reviews.
- Issue intake and guest remotes have small gaps, found at the M232 and
  M234 reviews with no fix planned. M233 and M234 shipped six of M232's
  items, and these are the rest. `/hotfix` names no `issue <URL>`
  argument form. An orphaned issue cannot be closed from the look-in. In
  guest mode `/milestone` §2's orphan bullet still runs, so §3's `close`
  (`gh issue close --repo <base-repo>` since M234) can close an upstream
  issue (found at the M234 plan). `/milestone-review`'s companion arm
  still pushes to `origin`. A guest checkout with the fork at `origin` and
  no `upstream` remote stops at the fork recipe, since `<base-repo>` is
  then the fork, and the plan's access read for its assignment offer
  (M248) reads the fork too. The reply draft's fixed name in a shared temp
  directory can collide or meet a planted symlink. If a gap shows in a
  real session, it becomes a `/hotfix` or a candidate row. Routed from
  candidates 2026-10-16; added 2026-10-10 — M232 review (blame-history #2,
  #3, diff-bug #1; pass 2 diff-bug #12, blame-history #2, #5, live-run
  #9) and M234 review (diff-bug #12, blame-history #5, prior-review #2;
  Copilot thread on PR #243, checked 2026-10-16T04:10:01Z).
- The `/hotfix` rerun and row-graduation paths have small gaps, found at
  the M249 and M262 reviews. The gaps below have no fix planned. M266
  gave a rerun a route for a closed PR, for the operator's own open PR,
  and for a guest change request (narrowed M266). Rerun (M262): the merge
  guard reads only the marker's PR number, so a hand-typed
  `gh pr merge <N>` with no `--match-head-commit` passes on a moved head.
  A marker whose PR merged outside the session stays on disk. A closed
  PR's marker stays until an owner-mode `/hotfix` rerun on that PR
  removes it (M266). `latestReviews` keeps each reviewer's latest review,
  so a later comment can mask their change request, both for the resume
  and for the M266 guest change route's trigger
  (`latestOpinionatedReviews` would not). Step 6 states no stop for red
  CI, and the marker stays. A resume reads no comment posted since the
  approval. A resumed follow-up PR of the merged-PR re-entry may never
  close the merged PR's `Fixes #N` issue. The guest arm's report-and-stop
  takes any open `hotfix-` PR outside the change route, whoever opened
  it (narrowed M266). A
  server-side merge failure (M170) or a `/milestone-review` marker in the
  same file sends the rerun to the walk. Row graduation (M249): a guest
  rerun with owed items never reaches an accepted check, so the row edit
  has no route. An owner rerun after a CI stop on the owed path can lose
  the PR number. No prompt asks a guest to rerun after a merge. The
  decline path's row has no stated commit. Deleting a §7 group's head row
  orphans rows quoting its title, and §7 may read a `narrowed` note as an
  extension. `/milestone-plan`'s trivial route deletes and narrows rows the
  same way and shares both edges (M265 review, prior-review #5). If a gap shows in a real session, it becomes a `/hotfix` or a
  candidate row. Routed from candidates 2026-10-16; added 2026-10-12 —
  M249 review; added 2026-10-16 — M262 review (pass 1 diff-bug #6, #10,
  blame-history #6; pass 2 diff-bug #2, #3, #4, #6).
- Started tokens have small gaps in the cairn pane and in `/cairn-triage`,
  found at the M252 to M259 reviews with no fix planned. Since M261 the
  pane hides a started row instead of marking it, so each edge shows or
  hides a row with no on-screen sign. Body lines are set at PR open, so
  older PRs and later row edits leave rows shown. A cut `gh pr list` or a
  missing base-remote URL shows hidden rows again, and a failed newer read
  keeps an old row hidden. Fences differ from CommonMark (any fence
  closes, 4+ spaces open, `-`/`>` fences missed, inline triple backticks
  toggle). Tokens (M258): same-title rows hide together, a later `: `
  pulls one into the title, and `/hotfix` step 1 can match a taken row.
  Triage (M259): a merged guest PR's or done milestone's token goes with
  no shipped note, before `/hotfix` narrows its row. An M token on a
  `candidate` table row reads live. An empty-title row with a live token
  cannot be retitled. The §1 keep still follows §7. If a gap shows in a
  real session, it becomes a `/hotfix` or a candidate row. Routed from
  candidates 2026-10-16; added 2026-10-15 — M252 review, narrowed and
  extended by M257 and M258, narrowed by M259, reworded by M261; M259
  review.
- `/cairn-triage` has small gaps, found at the M235, M251, M254, and M263
  reviews with no fix planned. Guest stamp: in guest mode a pass names
  each already-shipped or refuted-premise drop's evidence in the ROADMAP
  stamp, and the next hygiene pass replaces it with no git history behind
  it. A guest lesson drop widens this, since an untracked LESSONS.md keeps
  no git copy. Lessons pass: the two-file cap check sends back a pass that
  trims a file already over its cap without getting under. Test comments
  cite lessons by line number ("LESSONS :49"). `git grep -l "LESSONS.md"`
  misses a test that builds the path. Retitle: rows sharing a title get
  identical triage subjects. An empty title not from a leading `: ` has no
  anchor. The Amend loop does not re-check a new title's uniqueness or
  icons, and a title the user types at Amend is not checked against the
  titles that open PRs' `Candidate row:` lines name (M299). A dead token
  whose removal changes the row's short title stays until a person edits
  the row (M299). An icon title cut at a late `: ` loses its detail in place. The
  icon removal has no stated scope (`⋯`, `≥` in detail). If a gap shows
  in a real pass, or
  a guest operator needs a dropped item's reason after a later stamp
  replaced it, it becomes a `/hotfix` or a candidate row. Routed from
  candidates 2026-10-16; added 2026-10-10 — M235 review (diff-bug #1,
  blame-history #3); added 2026-10-15 — M251 review (pass 2 diff-bug #3,
  #5, #7) and M254 review; added 2026-10-16 — M263 review (diff-bug #10,
  #16; blame-history #1, #10).
- `scripts/cairn_ci_paths.py`'s `--report` and `--apply` can disagree on a
  workflow file, found at the M181 review with no fix planned. `--report`'s
  stdlib reader and `--apply`'s PyYAML read some legal forms differently (a
  quoted `"push":` key, a block-scalar `cairn/**` item), so `/cairn-init`
  §0's by-hand hint can name an item already there (`--report` stays
  stdlib, D-135). `--apply` refuses two shapes M181's AC2 named editable, a
  null `push` and a block scalar whose last line opens with `#`, as
  `post-edit check failed`. If an adopter's real workflow file draws the
  verdicts apart or is refused, it becomes a `/hotfix` or a candidate row.
  Routed from candidates 2026-10-18; added 2026-09-06 — M181 review (G7,
  G8, H2, H3).
- Claim audits and amendment returns have small gaps, found at the M182
  and M211 reviews with no fix planned. Claim audit (M182): the same-reader
  re-read needs agent continuation, which a harness without `SendMessage`
  lacks (M182's first run went to a second fresh reader, logged). A
  milestone whose `Surface tier:` slot is still `—` fits neither not-owed
  reason, so its mandated line is unwritable. `/cairn-release` step 2's
  "release-prep commit" anchor is named only by the generic release-walk
  and the quarto-extension walk's release-time arm (corrected M303).
  Amendment returns (M211): an amendment return whose amendment never runs
  does not count toward the second-occurrence stop (D-150's falsifier).
  Implement step 1 does not read the `amendment routed:` line on a cold
  resume. The stop matches on `AC<N>` alone, so a renumbering amendment can
  hide a repeat. Overlapping records-hygiene §7 groups can draw several
  disposition chips over the same rows, and a triage rewrite can change a
  quoted title and break its group. If a gap shows in a real session, it
  becomes a `/hotfix` or a candidate row. Routed from candidates
  2026-10-18; added 2026-09-10 — M182 review; added 2026-10-04 — M211
  review, narrowed 2026-10-15 by M251.
- The Copilot review round's reads have small gaps, found at the M244 and
  M282 reviews with no fix planned. Round off (M244): since M283 the
  `/milestone` audit lists unresolved bot threads on your open PRs, so the
  gap left is a late review on a merged PR and the note's silence. The
  off-but-present note runs one query at the close, seconds after the PR
  opens or merges, while Copilot requests on easystats PRs landed about 2
  minutes after the open, so the note often stays silent. Reason line
  (M282): `skills/shared/copilot-review.md` §6 gives the not-recorded line
  as the reason only while the read's own state query prints `none`, but
  says nothing when that query fails, and a §4 wait that starts on
  `pending` and exits on `none` leaves the report giving a pending line for
  a PR with no request. §3's `pending` test matches the reviewer login
  `copilot-pull-request-reviewer`, which no read has checked against a
  live open request. If an opted-out repo's PR gets a Copilot review that
  no close or audit reported, or another gap shows in a real session, it
  becomes a `/hotfix` or a candidate row. Routed from candidates
  2026-10-18; added 2026-10-11 — M244 review (blame-history #1; diff-bug
  #1; prior-review #1), corrected M283; added 2026-10-18 — M282 review
  (diff-bug #4; blame-history #2).
- The `/milestone` audit's row and PR reads have small gaps, found at the
  M245, M246, and M283 reviews with no fix planned. Archived blocked rows
  (M246): `/milestone` §2 does not route them, owner mode has no route, a
  no-URL row gets no Button, and a Button drawn before a row turned
  archived still routes. Python and TS differ on a root with `[` and on
  invalid UTF-8, and some Status edges are untested. Linked-item read
  (M245): a linked PR merged by others also shows as an outside merge. Any
  later date in a row (a target date, a "narrowed" date, a triage rewrite)
  moves its cut-off past unreported news. The `checked` mark takes the edit
  time, not the read time. A review seconds after midnight can be skipped.
  The read runs in Bash or zsh only. Bot threads (M283): the bullet does
  not select `diffSide`, `startLine`, or a null author, so a removed-line
  thread is judged against the head, a multi-line thread gives its end
  line, and a deleted account's thread is dropped unstated. A deleted or
  renamed file, or a deleted fork, gives `cannot tell`. A thread on a PR a
  candidate row links to also shows in the linked-item read. If a gap shows
  in a real session or misleads a real audit, it becomes a `/hotfix` or a
  candidate row. Routed from candidates 2026-10-18; added 2026-10-11 —
  M245 review (blame #4, #5, #10; diff-bug #5, #12; pass 2 diff-bug #1, #3,
  prior #1); added 2026-10-12 — M246 review; added 2026-10-18 — M283
  review (diff-bug #3, #4, #8, #9, #11, #12).
- Candidate-row readers and the triage promote have small gaps, found at
  the M271, M272, M273, and M280 reviews with no fix planned. Readers
  (M272): every candidate reader (the pane list, `candidate_count`, the
  plan target) reads a row under `## Candidates (dropped)` or after an
  unclosed `<!--`, and an untokened row a planned or blocked milestone
  already quotes can be named again (narrowed 2026-10-17 by M273). Started
  token before the colon (M273): a ` — started M<n>` token written before a
  row's first `: ` becomes part of the short title in every reader, so it
  names no row and hides nothing; M258 AC4 covers end-of-row tokens only.
  Order advisory (M280): the `candidate order` WARN counts rows the pane
  hides (a counted started token, a row an open PR's body names), so it
  can name a row the pane never draws. A row with an empty short title
  WARNs as `""`. A misspelled token reads as normal, so the `[high]` rows
  below it WARN while the misspelled row is the fault. D-182's sentence on
  the first `[high]` row holds only when that row has a short title.
  Triage promote (M271): an Amend can set `promote` on a row that step 2
  holds as `keep` for a live started token, or since M295 because an open
  PR's `Candidate row:` line names it, which writes `[high]` and a
  `/milestone-plan` fence for work already taken. For a records-hygiene §7
  group the skill does not say whether each row takes `[high]` and its own
  fence. If a gap shows in a real session or misleads an operator, it
  becomes a `/hotfix` or a candidate row. Routed from candidates
  2026-10-18; added 2026-10-17 — M271 review (diff-bug #7, #8), M272
  review (diff-bug #7, #9; blame-history #10), and M273 review
  (blame-history #3); added 2026-10-18 — M280 review (diff-bug #1, #3, #4,
  #5; prior-review #1).
- Guest-mode pushes to the base repo and stacking have small gaps, found at
  the M267 and M268 reviews with no fix planned. Push remote (M267): with
  `# Push remote: base` set after a PR opened from the fork, review's
  access read still gates the push to the fork head, and a non-`true`
  answer stops a push the fork would take. The first push to the base repo
  does not check for a maintainers' branch already named `<slug>`; a
  non-fast-forward push is refused, a fast-forward is not. Stacking (M268):
  TS splits PROFILE.md lines on more characters than Python and has no
  catch-all on its read. No fixture holds a padded dependency id, a
  duplicate dependency, a BOM PROFILE.md, or a done-and-blocked row, and
  `stack_bases` and `_met` have no direct unit test. A stacked PR the
  maintainers merge into its base branch reaches `done` with its code off
  the default branch. A base branch deleted with no merge closes the
  stacked PR. A single-branch fetch refspec leaves no
  `<base>/<stack-base-branch>` after `ls-remote` passed. The readers count
  a chained base as a stack base, which implement refuses, and
  `cairn_next.py` marks no stacked row. A resume fails the dependency check
  once the base is back at `review`. If a gap shows in a real session, it
  becomes a `/hotfix` or a candidate row. Routed from candidates
  2026-10-18; added 2026-10-16 — M267 review (diff-bug #6, #17) and M268
  review (diff-bug #12, #16, #18, #20; blame-history #8, #9; prior-review
  #2; pass 2 diff-bug #1, #7; blame-history #7).
- Cut feature series have small gaps, found at the M276 review with no fix
  planned. A guest cut milestone's PR gets no series sentence, since only
  the later milestone carries the `feature series:` line. A cut inside a
  planned series adds a second line with two last parts, and cutting the
  later part again drops the first. A `/hotfix` before the later part is
  planned finds no series and adds a second entry. A milestone that absorbs
  a marked row only in part carries no line, and its started token hides
  the row from the release walk. `/milestone` §1 does not say it reads
  marked rows, and a plain "split from M<n>" in any row reads as the
  marker. If a gap shows in a real session, it becomes a `/hotfix` or a
  candidate row. Routed from candidates 2026-10-18; added 2026-10-18 —
  M276 review (diff-bug #2, #3, #4, #5, #7, #9; prior-review #1, #3).
- The `/hotfix` own-PR walk and guest change route have small gaps, found
  at the M266 review with no fix planned. The own-PR walk never refreshes
  the PR body's `Candidate row:` lines, so a later resume can fail its row
  condition and ask again. The guest change route compares a review's time
  with the head's commit time, not its push time, and reads the head from
  the last of `commits`, which `gh` may cut short. A contributor PR closed
  by the re-land fallback gets "start over" though its re-landed PR is
  open. A closed guest milestone PR (named `<slug>`) takes the hotfix
  closed stop, and a closed owner `m<nnn>-*` PR falls to the adopt walk.
  If a gap shows in a real session, it becomes a `/hotfix` or a candidate
  row. Routed from candidates 2026-10-18; added 2026-10-16 — M266 review
  (diff-bug #4, #6, #10, #14; blame-history #5, #8).
- The pane tests' "nothing more happened" checks for a rejected session end
  wait briefly, found at the M260 review with no fix planned:
  `untilRuns` and `untilOpens` at 10 tries wait about 55 ms, so a late run
  or open passes unseen, and M278's AC1 test adds one more such check. If
  one shows in a real session, it becomes a `/hotfix` or a candidate row.
  Routed from candidates 2026-10-18; added 2026-10-15 — M260 review
  (diff-bug #6, #7, #8; blame-history #1; prior-review #2), narrowed
  2026-10-18 by M278 (prior-review #2).
- The cairn pane has five gaps that only the desktop app or the mod API can
  close, accepted with no fix planned. A click on an unfocused pane only
  focuses it, so a Button takes two clicks. The bar uses a monospace font
  and the band the text font, and `Text` has no font prop. The desktop
  track's fixed-palette image has no theme signal, and its implement orange
  and review green look alike to red-green colorblind eyes. Nobody checked
  the dim `✕` by the gray row or 256-color terminals. The pointer over a
  pane Button keeps the arrow cursor, because no mod prop sets a hand. A Box
  in a hover group does not light the group, only a Text does, so a
  candidate row's card, opened from its ⓘ, closes when the pointer moves
  onto the card. If the app or the mod API gains the missing signal or
  prop, or a gap shows in a real session, it becomes a `/hotfix` or a
  candidate row. Routed from candidates 2026-10-20; added 2026-10-02 —
  M198 Out and review; added 2026-10-04 — M209, M219; added 2026-10-19 —
  M290 live look and review (blame-history #1, prior-review #6).
- The cairn pane's count badges (M289) have looks unchecked, with no fix
  planned. Nobody checked the terminal badge's `inverseText` on
  `inactive` in the light and other themes. M302 checked the gray pill in
  a browser preview only, so its place after the label, its row's
  centering, and any clipping by the lead Box wait for a desktop look
  after the merge. During M302 no badge heading drew in this repo:
  Candidates draws only with no active milestone, and the repo had no
  blocked milestone and no open hotfix PR, which draw either way. A
  16 px badge can make its heading row
  taller than the 14 px icon rows on the desktop, and since M294 a taller
  row, or a row of Buttons, also shifts a candidate card's `rowsAbove` and
  its `top`. If a badge reads poorly or a heading row draws taller in a
  real session, it becomes a `/hotfix` or a candidate row. Routed from
  candidates 2026-10-20; added 2026-10-19 — M289 review (diff-bug #1, #3;
  prior-review #1; blame-history #2); extended 2026-10-20 — M294 review
  (diff-bug #1); narrowed 2026-10-20 by M302, whose one gray removed the
  amber and orange hue clause.
