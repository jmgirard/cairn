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
- `hooks/status/` — the milestone band, a Claude Code mod (M191, D-143, rows restyled in M193, two-group rows and a close button in M194, skill rows and chapters in M195, one line per milestone in M196, one row for the band, shorter forms, and a one-glyph bar in M197, gray text with a muted label in M198, the idle row and the step's end at its turn's end in M199, a close state that a failed ROADMAP read alone does not change and every session end clears in M200, the step's end at a Stop with nothing in flight or an idle typed prompt in M201, the desktop flow track in M204, the cairn pane in M205, the id-and-title row with the track as its one progress form, a shorter desktop track, and a terminal braille track in M206, which removed the labels, chapters, skill rows, and the bar, the pane's candidate rows in M207, the pane's percent, headings, meters, and Next pill in M208, in M210 rows kept only within one repo root, a UNC share root, a step kept by a one-shot wakeup or a dropped prompt, and close-state writes only on a change, and the empty row with its `Plan` button in M213, and the `Clear` button after a cairn skill ends in M216, and the pane's Next button in M218, and the pane's Status and Clear buttons in M219, and the idle row's `Implement` button in place of its command in M220, and `Plan` and `Implement` clearing the conversation first in M221, and the pane open again after a `/clear` in M222, and the pane's blocked rows with their pull request numbers in M223, and each blocked PR's state word and Button in M224, and each open PR's unresolved and unanswered counts in M225, and the open hotfix PRs in M226, and opens that do not wait for the PR reads, a refill after an in-process `/clear`, a shared PR drawn once, and no remote credentials in the `gh` call in M230).
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
  computes it. A done id is a `done` row or an
  `M<digits>` file directly under `cairn/milestones/archive/`, compared at
  three-digit padding. With an empty list and a found ROADMAP (the pane
  state's `found`), the band draws the empty row (M213): key `plan-row`,
  no head Box, the gray text `No milestone ready`, and no track or tail.
  `stepLines` returns it when its `found` argument is true. The pane's next
  step is then planning, so the next-step Button reads `Plan`, and a press
  runs `clear` and then `cairn:milestone-plan` with empty args (M221). `actionsFit` keeps the action
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
  is still the next step's label, `pressNext` stores the command and its
  args in the module's `heldRun` value and runs `clear` through `run`.
  `session.end` takes `heldRun` before it calls `next(e)` and, when the
  reason is `clear`, runs it through `run`, unawaited. Any other end drops
  it and puts its command line in the prompt box with a toast, as `run`
  does for a refused run (`fallBack`). A `clear` run that rejects drops it
  too, and `run`'s own refusal names `/clear`. While `heldRun` is set,
  `busy` makes every action press do nothing. A live probe (M221 T1) showed
  that the session end of a Button's `/clear` arrives before that run
  resolves. The press is the person's consent to drop the conversation, as
  a press of Clear is, which is how the plan gate settled the IP3 point. A
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
  while no row is active. The pane state also holds the `blocked` rows
  (M223), in ROADMAP order, each with the number of the pull request that
  its milestone file's first `Branch/PR` header line names. The number
  comes from the first `https://github.com/<owner>/<repo>/pull/<n>` URL
  before any `companion:` entry, and a missing file, a failed read, or no
  such URL gives none. `blocked` and `pr_number` in
  `scripts/cairn_next.py` compute the same list, which `reader.ts`
  mirrors and `test_status_fixtures.py` holds to each fixture's `blocked`
  key. `cairn_next.py` prints the number after each "Externally blocked"
  line. The pane draws a `BLOCKED` section after the queue in every
  state, the number in the line's tail. A guest-mode handoff sets its
  milestone `blocked` with the PR URL in its header, so the section lists
  the PRs that wait on maintainers. The header is the text before the
  first `## ` heading, and a number has at most 15 digits, so both sides
  read it the same.
  Each blocked row also keeps that pull request's URL up to its number
  (M224, `prUrl` and `pr_url`), and the pane reads each PR's state
  from it. `readPrs` in `register.tsx` runs one `gh pr view <url> --json
  state,reviewDecision` per distinct URL through `$.process.run`, side
  by side, with a 15-second timeout each, and writes each word, with its
  counts since M225, to the `prs` state value by URL. It runs after each pane open (the
  `/cairn-pane` command, the band's open button, the session-start
  reopen) and at a press of the `Refresh` Button on the `BLOCKED`
  heading, which first reads the files again. The three opens start the
  read with `void readPrs($)` and return before it settles (M230). The
  press still waits for it. After its refresh, a `classic.SessionStart`
  with source `clear` also starts the read without waiting. It does so
  only when `$.ui.panes()` lists the pane placed and shown (`isShown`). No timer and no turn end
  starts a read, at the operator's word. A read that starts while another
  runs still runs, and only the newest read started writes its words
  (M224 review). `prWord` in `pane.ts` maps each result:
  MERGED to `merged`, CLOSED to `closed`, OPEN by its review decision to
  `changes requested`, `approved`, or `in review` for any other or none,
  and a rejected call, a non-zero exit, text that is not a JSON object, or
  another `state` to `unknown`. The word follows the number in the
  line's tail. `PR_BUTTON` gives a `merged` line a `Finish` Button that
  runs `/cairn:milestone-review <id>`, a `changes requested` line a
  `Revise` Button that runs `/cairn:milestone-implement <id>`, and a
  `closed` line a `Check` Button that runs `/cairn:milestone`, the
  routes `/milestone` gives a handed-off PR. None of these three Buttons
  clears first. A press reads the word as it is now and runs through
  `run`, as the Status press does. Like the Status press, it does nothing
  while another run is in flight or a cairn skill's step runs (M224
  review). The Buttons stay drawn while a step runs. A test answers the mod's
  `$.process.run` with an `on('process.run')` hook (M224 probe), and a
  desktop Code session's mod runs `gh` from the app's `PATH`.
  In the same read, each URL whose word is in `OPEN_WORDS` gets one `gh
  api graphql` call with the same timeout (M225, `counts.ts`). The query
  names the URL's owner, repo, and number, and returns the PR author's
  login, `reviewThreads(last: 100)`, `reviews(last: 100)`,
  `comments(last: 100)`, and `commits(last: 1)`. `prCounts` checks the
  reply's shape, and `countPr` gives two counts. The first is the threads
  with `isResolved` false. The second is the COMMENTED or
  CHANGES_REQUESTED reviews and the conversation comments strictly after
  the anchor, by anyone but the PR author. A null author counts as another
  person. The anchor is the latest of the author's newest such review,
  the author's newest conversation comment, and the `committedDate` of
  the PR's newest commit. That commit can be anyone's. The times compare
  as ISO-8601 UTC text, and a commit time given with an offset is first
  converted to UTC (M225 review). GitHub gives no reply link for a review or a
  conversation comment, so the anchor rule stands in for per-item reply
  tracking. Bots are others, so one Copilot review can count in both
  counts. The counts cover the newest 100 of each kind. A failed call or
  reply leaves the counts null. The `prs` value holds `{ word, counts }`
  per URL under the tag `prs-2`. It is written once every call settles, so
  a `Refresh` keeps the earlier counts drawn until then. When a count is
  above zero, `paneLines` draws `blocked-<id>-counts` at indent 4 under
  the line. The counts sit in the line's text part, which a narrow pane
  cuts.
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
  --author @me --limit 100 --json number,title,url,headRefName` call runs
  in the root. `hotfixPrs` in `pane.ts` keeps an entry only with a
  `headRefName` that starts with `hotfix-`, a string `url`, and an
  integer `number`. A call that rejects, exits non-zero, or prints no JSON
  array keeps the last good list when it was read for the same root. The
  list's URLs join the blocked URLs for the word and count reads. The
  `hotfixes` state value (`{ root, prs }`, tag `hotfixes-1`) is written
  with the words. The pane draws the list only while the band's root is
  its root, under a `HOTFIXES` heading after `BLOCKED` and before the
  candidates. An entry whose URL is a blocked row's draws on that blocked
  line only, and the heading's count leaves it out (M230). The section has
  `hotfix-<n>` lines with the word in the tail and
  `hotfix-<n>-counts` at indent 4, and no Button. The heading's `Refresh`
  carries the target `hotfixes`, so its key is
  `cairn-pane-refresh-hotfixes`.
  `pane.ts` lays out the lines, and each line's text is
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
  color, and the pill takes the color of the phase its command runs, with
  `inverseText` text. All are the theme keys of `FLOW_COLORS` (M217), and a
  high-priority candidate's `↑` takes the implement key.
  While `knownStep` reads no step, `paneLines` gives the Next line an
  `action` label from `NEXT_LABELS`, which moved to `pane.ts` so the band
  and the pane read one map (M218). The pane's `ui.render` draws it as a
  `secondary` Button, key `cairn-pane-next`, in a `next-action` Box with
  `flexShrink: 0` and `marginLeft: 1` after the pill, so the pill is cut
  first. A press is the band's `pressNext`. A pane gets no `isWorking`
  prop, so the Button also shows during a turn outside a cairn skill, and
  `$.command.run` queues such a press until the session is idle.
  At the same times, with that label, `paneLines` gives the Next line `buttons` (M219):
  `status`, with `clear` before it while the `ended` atom (M216) is true.
  The pane's `ui.render` reads `ended`, and draws each after `next-action`
  as a `secondary` Button, key `cairn-pane-status` or `cairn-pane-clear`,
  in a Box keyed `next-status` or `next-clear` with `flexShrink: 0` and
  `marginLeft: 1`. In the desktop app, a click
  on a pane without keyboard focus only gives it focus, and no `ui.press`
  reaches the mod (M219 probe). A pane Button then takes a second click.
  The labels `STATUS_LABEL` and `CLEAR_LABEL` moved to `pane.ts`, so the
  band and the pane read one place. A press is the band's `pressStatus` or
  `pressClear`.
  A cairn pane shown at a `/clear` is open after it (M222). A press
  of a Clear, `Plan`, or `Implement` Button ends the session with reason
  `clear` in the same process, and nothing closes the pane (M222 probe). The
  host's state starts empty under the new session id, and no
  `session.start` fires, so a `classic.SessionStart` hook with source
  `clear` refreshes the band and the pane, and a shown pane reads its PRs
  again (M230). A
  typed `/clear` in the desktop app ends the process with reason `other`,
  and the next process starts with no pane at the first message after the
  clear. So at an `other` end with the pane listed, shown, and placed, the
  `session.end` hook adds `$.session.root()`, which a shell `cd` does not
  move, to the store key `reopen`, and
  the next `session.start` in that folder clears the mark and opens the
  pane after its refresh, when a ROADMAP is found. A reopen that is not
  placed waits with no toast. A pane behind another pane's tab or waiting
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
  moved pane shape tag (`pane-3` since M223) after a reload, until the
  next refresh (corrected M223). A pane parse
  throw keeps the band's old rows, and a throwing refresh skips the
  command's registration. Duplicate ids give duplicate pane keys and share
  one percent. The pane matches `## Candidates (dropped)` and draws a bare
  mark for an empty title. It shows the date and links of a row with no
  `: `.
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
  in a working turn queues its `/clear`. Two quick presses can pass
  `busy`. A `/clear` with no clear end holds the queued command, and a
  reload before the end loses it. A refused press with a draft sends
  `draft/cairn:…` as prose. `Review` can act on a hidden milestone, and
  `Plan` starts a milestone that just turned workable. Pane Clear shows
  outside a cairn skill and with the band closed.
  Layout: `refresh` writes band and pane apart, so a frame can drop a head
  line's percent or show `Plan` or the empty row out of date. Under about
  39 columns a band title gets less than its 10 columns, and under about 38
  the pane's Boxes overflow. At the 44-column dock the Next pill gets about
  3 columns, and `Resume` or `Review` cuts it. A cut Next command loses its
  pad, so `…` draws on the pill's color. Desktop Buttons count at terminal
  width, and the track uses a 7-pixel column estimate (`TRACK_COLUMNS`, 52)
  that no test ties to the app. The engine's scrub can drop the track's
  `clipPath`. The `▎`, `■`, `□`, and `↑ · ↓` marks are ambiguous width in
  CJK terminals.
  Colors: nobody checked the gray Buttons or the terminal track in other
  themes. In the light colorblind theme the implement pill is 2.1:1
  (light: 3.2:1). The desktop track's plan blue and implement orange differ
  from the pane's `planMode` teal and `claude` orange.
  Tests: none covers the `vscode` and `mobile` surfaces, presses a stale
  Clear, or starts a skill by a press. The M206 desktop sweep has no Button
  rows and starts at 40 columns. The press, refresh, and session-end suites
  draw on the terminal only. M219's Review lists four more gaps.
  Code: `CairnPaneState` and `PaneState` are hand-kept copies, and
  `render()` lists the archive three times. The desktop can draw `≡` as a
  native button over its 2 reserved columns.
