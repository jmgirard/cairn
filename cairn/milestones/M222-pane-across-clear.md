# M222: The cairn pane stays open across /clear

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m222-pane-across-clear

## Goal

A cairn pane that is open when the conversation is cleared is open again after the clear.

## Scope

**In:** T1 is a live probe in a desktop Code session. A throwaway logging
copy of the mod sits in the session's hot-reload folder, and the operator
runs `/clear` with its pane open. The probe records what closes the pane:
each `ui.close` with its origin, `$.ui.panes()` before and after
`session.end`, and the order of these events. The mod API says that a
`/clear` raises `session.end` with reason `clear` and no `session.start`.
It also says that a `ui.close` hook can keep a pane on origin `plugin` or
`person`, and never on `unload`. The probe tries three ways to keep the
pane or open it again. The first is a `ui.close` hook that answers without
`next`. The second is an open after `next(e)` in `session.end`. The third
is an open from the first event after the clear, such as
`classic.SessionStart` with source `clear` or a band render. The probe
logs `isPlaced` for each open. An open that no press or typed command
caused is placed only from 110 columns for an id the person opened before.
So the probe also records the window in which the reopened pane is drawn.
`register.tsx` then uses the way the probe found for every clear. The
clears are a typed `/clear`, the band's or the pane's Clear Button (M216,
M219), and a `Plan` or `Implement` press that clears first (M221). A pane
that is open at the clear is open after it, whether it was shown, behind
another pane's tab, or waiting undrawn. README, DESIGN, CHANGELOG, and the
comments describe the change. Only the desktop app gets a live look, and
tests cover the terminal.

**Out:** If T1 finds that the app closes the pane in a way the mod can
neither stop nor undo, implement stops with the goal-wrong stop. The plan
gate chose to drop the milestone then and to add a candidate row that
waits for a change in the app. Nothing is posted anywhere. The pane's
column and width after the clear are the open row "Mod pane placement
(upstream)". Session ends for other reasons (`resume`, exit, logout) keep
today's behavior, because the request named only `/clear`. The plan gate
declined a terminal live look.

## Acceptance criteria

- [ ] AC1: When the cairn pane is open at a `session.end` whose reason is
      `clear`, it is open after the clear, and shown if it was shown. The
      `claude plugin test` cases in `hooks/status/pane.test.tsx` use stubs
      that close the pane in the order and with the origin that T1
      recorded. The cases drive that end with the pane shown, behind
      another pane's tab, and waiting undrawn. Each case asserts that
      `$.ui.panes()` lists `cairn` after the clear's events. The shown case
      also asserts that `isShown` and `isPlaced` are true.
- [ ] AC2: A `clear` end with no cairn pane open leaves none open. A test
      case with the same stubs asserts that `$.ui.panes()` does not list
      `cairn` after the clear's events.
- [ ] AC3: A `session.end` whose reason is `resume`, `prompt_input_exit`,
      `logout`, or `other` neither keeps nor opens the pane. One test case
      per reason closes the pane in its stubs as at a clear. Each case
      asserts that `$.ui.panes()` does not list `cairn` after the end.
- [ ] AC4: The operator uses a desktop Code session whose window is at
      least as wide as the one in which T1 saw a reopened pane drawn. With
      the cairn pane open and shown, four clears each leave the pane shown
      after the clear. They are a typed `/clear`, a press of the band's
      Clear Button, a press of the pane's Clear Button, and a press of a
      `Plan` or `Implement` Button that clears first. The operator sees
      this at a live look and accepts it.
- [ ] AC5: README.md, `cairn/DESIGN.md`, and CHANGELOG.md's Unreleased
      section each state that a cairn pane open at a `/clear` is open again
      after it. Each names the desktop app as the surface checked live.
- [ ] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T1, T5
- AC5 → T4
- AC6 → T3, T4

## Tasks

- [ ] T1: Probe. Write the logging mod `cairn-probe` in the session's
      hot-reload folder, with a pane and the three ways the Scope names.
      Its log goes to a file in `.git/info/exclude` (LESSONS M201, M205).
      The operator enables hot reload, opens the probe pane, and runs a
      typed `/clear` and a Clear Button press. Write one work-log line with
      the close origin, the event order, the way that kept or reopened the
      pane, and the window width. If no way works, take the goal-wrong stop.
- [ ] T2: Tests first. In `pane.test.tsx`, make the `session.end` and
      `ui.close` stubs close the pane as T1 recorded. A flag turns this on,
      so the other suites keep their stubs. Add the AC1, AC2, and AC3
      cases, and see the AC1 cases fail against the current `register.tsx`.
- [ ] T3: Implement the way T1 found in `register.tsx`, beside the M221
      held-run code in the `session.end` hook, so that the held command
      still runs. A reopen that is not placed waits with no toast. Run
      `verify`.
- [ ] T4: Describe the change in README.md, in `cairn/DESIGN.md` near the
      M219 pane text, and in CHANGELOG.md's Unreleased section. Run
      `verify`.
- [ ] T5: Live look in a new desktop Code session in a cairn repo, since
      a Code session keeps the mod it loaded at its start (LESSONS M195).
      Try each clear that AC4 names.

## Work log

- 2026-10-06: created by /milestone-plan.
- 2026-10-06: collision sweep: no ROADMAP row, archive entry, or D-entry covers keeping the pane across `/clear`. M209 (dropped) covered the pane's place after a session switch, which is a different case. The GitHub inbox has 0 open issues and 0 open PRs.
- 2026-10-06: criteria audit (full mode, fresh Opus reader): 9 findings, all taken toward the narrower promise. The red-against-old-code clause moved to T2, because it depends on the test stub. AC1 asserts shown and placed and covers the tabbed and undrawn states. AC2 and AC3 assert "not listed", so they hold for a keep or a reopen. AC4 names the pane's Clear Button and a window width. AC5 names the desktop as checked live.
- 2026-10-06: question set: live probe and live look in a desktop Code session — granted, both.
- 2026-10-06: question set: what to do if the app closes the pane beyond the mod's reach — drop the milestone and add an upstream candidate row, with nothing posted.
- 2026-10-06: question set: a terminal live look — declined, desktop only, and tests cover the terminal.
- 2026-10-06: plan chose a live probe before any code over building from the API docs alone, because the docs do not say what closes a pane at `/clear`. M209 and M221 used the same probe. Falsified by a doc or a type that states the close mechanism.
- 2026-10-06: plan chose to keep the behavior of other session ends over a reopen on every end, because the request named only `/clear`. Falsified by the operator asking for the pane after a resume.
- 2026-10-06: implement started on m222-pane-across-clear. Untracked `cairn-probe.log` and `tsconfig.json` stay unstaged, as they are not milestone work.
- 2026-10-06: T1 probe written at `~/.claude/dev-mods/a9a59434-d86a-4bc2-91e4-5e3eb7bac7dc/cairn-probe/` (validates). `/cprobe` opens its pane, and `/cprobe-mode` or the pane's mode Buttons set `none`, `keep`, `end`, or `after`. The pane has a Clear Button. Each event goes to `m222-probe.log` (in `.git/info/exclude`). Each clear wipes this conversation, so the run resumes from `/milestone-implement M222`, which reads the log and the operator's report to finish T1.

## Decisions

## Review
