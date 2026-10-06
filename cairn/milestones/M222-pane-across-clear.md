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

A cairn pane that is open when the conversation is cleared is open after the clear:
left open by the mod where the clear stays in the same process, and opened
again when the next session starts in the same folder, which in the desktop
app is at the first message after a typed `/clear`.

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
tests cover the mod's side in the terminal.

**Out:** If T1 finds that the app closes the pane in a way the mod can
neither stop nor undo, implement stops with the goal-wrong stop. The plan
gate chose to drop the milestone then and to add a candidate row that
waits for a change in the app. Nothing is posted anywhere. The pane's
column and width after the clear are the open row "Mod pane placement
(upstream)". Session ends for `resume`, `prompt_input_exit` (/exit, ctrl+c,
ctrl+d), and `logout` keep today's behavior, because the request named only
`/clear`. An `other` end with the pane open reopens it at the next session in
that folder. So an app quit, a closed terminal, or another signal that ends
with `other` also brings the pane back (the operator's choice). The plan gate
declined a terminal live look.

## Acceptance criteria

- [ ] AC1: When the cairn pane is open at a `session.end` whose reason is
      `clear`, the mod neither closes nor hides it. T1 saw that a press in
      the desktop app then leaves the pane open and shown. The `claude
      plugin test` cases in `hooks/status/pane.test.tsx` drive that end with
      the pane shown, behind another pane's tab, and waiting undrawn, with
      stubs that close no pane. Each case asserts that `$.ui.panes()` lists
      `cairn` after the clear's events. The shown case also asserts that
      `isShown` and `isPlaced` are true.
- [ ] AC2: A `clear` end with no cairn pane open leaves none open. A test
      case with the same stubs asserts that `$.ui.panes()` does not list
      `cairn` after the clear's events.
- [ ] AC3: After a `session.end` whose reason is `resume`,
      `prompt_input_exit`, or `logout`, the next `session.start` opens no
      cairn pane. One test case per reason ends the session with the pane
      open, empties the open panes between the end and the next
      `session.start`, so the case sees only what the mod opens, and then
      starts a session in the same cwd. Each case asserts that
      `$.ui.panes()` does not list `cairn`.
- [ ] AC4: The operator uses a desktop Code session in a window no
      narrower than T1's (its probe read 106 columns). With the cairn pane
      open and shown, four clears each leave the pane shown once the first
      message after the clear is sent (for a `Plan` or `Implement` press,
      that message is its held command). They are a typed `/clear`, a press
      of the band's Clear Button, a press of the pane's Clear Button, and a
      press of a `Plan` or `Implement` Button that clears first. The
      operator sees this at a live look and accepts it.
- [ ] AC5: README.md, `cairn/DESIGN.md`, and CHANGELOG.md's Unreleased
      section each state that a cairn pane open at a `/clear` is open again
      after it. Each names the desktop app as the surface checked live.
- [ ] AC6: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.
- [ ] AC7: When the cairn pane is open and shown at a `session.end` whose
      reason is `other`, which is how the desktop app ends a session at a
      typed `/clear`, the next `session.start` in the same cwd opens it.
      Test cases end with reason `other`, empty the open panes, and start a
      new session. The case with the pane open at the end and the same cwd
      asserts that `$.ui.panes()` lists `cairn`. The cases with another cwd,
      or with no pane open at the end, assert that it does not.

## Coverage

- AC1 → T1, T2
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T1, T5
- AC5 → T4
- AC6 → T3, T4
- AC7 → T1, T2, T3

## Tasks

- [x] T1: Probe. Write the logging mod `cairn-probe` in the session's
      hot-reload folder, with a pane and the three ways the Scope names.
      Its log goes to a file in `.git/info/exclude` (LESSONS M201, M205).
      The operator enables hot reload, opens the probe pane, and runs a
      typed `/clear` and a Clear Button press. Write one work-log line with
      the close origin, the event order, the way that kept or reopened the
      pane, and the window width. If no way works, take the goal-wrong stop.
- [x] T2: Tests first. In `pane.test.tsx`, install `mock.store(on)` in the
      stubs and add a way to empty the open panes between a session end and
      the next start. Add the AC1, AC2, AC3, and AC7 cases, and a case in
      which an `other` reopen, a close, a `prompt_input_exit` end, and a
      start list no `cairn`. The another-cwd case changes the cwd that
      `$.session.cwd()` gives, which the flag keys on. See the AC7 reopen
      case fail against the current `register.tsx`. The other cases pass
      against it and guard what must not change.
- [x] T3: In `register.tsx`, store a flag for the cwd at a `session.end`
      whose reason is `other` with the pane open and shown. At each
      `session.start`, open the pane when that cwd's flag is set, and clear
      the flag. Keep the M221 held-run code in the `session.end` hook. A
      reopen that is not placed waits with no toast. Run `verify`.
- [x] T4: Describe the change, and that an `other` end such as an app quit
      also brings the pane back, in README.md, in `cairn/DESIGN.md` near the
      M219 pane text, and in CHANGELOG.md's Unreleased section. Run
      `verify`.
- [x] T6: A press of a Clear Button leaves the pane open but showing `no
      cairn ROADMAP found` until the next prompt, as the host's state starts
      empty under the new session id. Refresh at `classic.SessionStart`
      with source `clear`, test first in the M205 AC5 event list. Run
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
- 2026-10-06: T1 first clear (typed `/clear`, mode `none`): `session.end` came with reason `other`, which the API defines as a signal, not `clear`. The pane was still listed after `next(e)`, and no `ui.close` or `session.start` was logged. The next session had a new id and did not load the probe from the old id's hot-reload folder, so the desktop app starts a new process at a typed `/clear`. The probe moved to `.claude/skills/cairn-probe/` (in `.git/info/exclude`), which loads in every process here. It now appends to the log and keeps its mode and an open-at-end flag in `$.store`, so mode `after` tries a reopen at the new process's `session.start`.
- 2026-10-06: T1 second clear (typed `/clear`, mode `after`, 106 columns): the end again had reason `other`, and the next process (`5o1m`) got `classic.SessionStart` with source `startup`, not `clear`. Its opens at `session.start` and at the first band render both returned `isPlaced: true`, and `$.ui.panes()` listed the probe pane as shown, with no `ui.close` logged. The operator reported that the pane was gone after the clear. The app's layout still listed a `plugin` pane open beside `tasks` and `terminal`, so the open may land behind a tab or undrawn. The operator's look at that tab decides the next step.
- 2026-10-06: T1 operator look: the probe pane was in the plugin tab, but it appeared only after the operator's first message following the clear. The log agrees: each new process started when that message was sent (first clear 4 min after the end, second clear 14 s after it), and `prompt.submit` followed `session.start` by 0.3 s. So the desktop app starts the next process only at the next message, and between the clear and that message no process exists to open the pane. Mode `after` reopens the pane at that start, which is the earliest point the mod can reach.
- 2026-10-06: stop answered: the operator chose to narrow the Goal and AC4 to a pane that is open again when the next session starts (in the desktop app, at the first message after the clear), and to continue. Proposed Goal: "A cairn pane that is open when the conversation is cleared is open again when the next session starts, which in the desktop app is at the first message after the clear." Proposed AC4 clause: "each leave the pane shown after the first message that follows the clear." The amendment waits for T1's Clear Button press, because a typed `/clear` ended with reason `other`, which AC3 says must not reopen the pane, and M221's held run relies on a press giving reason `clear`. The amended criteria must say how a typed `/clear` is told apart from the other ends, and they get the fresh-Opus re-audit before they are written.
- 2026-10-06: T1 Clear Button press (pane's Clear, mode `after`, 106 columns): the end came with reason `clear` in the same process (`5o1m`), then `classic.SessionStart` with source `clear` 0.1 s later. No `ui.close` was logged, and `$.ui.panes()` listed the probe pane as shown right after `next(e)`, before mode `after` reopened it 7 ms later. The operator saw the pane stay. So an in-process clear does not close a mod pane, and `register.tsx` does not close its pane at `session.end`. Only a typed `/clear` loses the pane, because the desktop app ends that process with reason `other` and starts a new one at the next message. T1 is done: close origin none, kept by doing nothing for a press, reopened at the next `session.start` for a typed `/clear`, at 106 columns.
- 2026-10-06: stop answered: the operator chose to treat an `other` end with the pane open as a typed `/clear` and reopen the pane at the next session start in the same folder, accepting that an app quit or another signal also brings it back. This narrows the plan's choice to keep the behavior of other ends: `resume`, `prompt_input_exit`, and `logout` keep it, and `other` does not.
- 2026-10-06: substantive amendment: the Goal now reads "A cairn pane that is open when the conversation is cleared is open after the clear: left open by the mod where the clear stays in the same process, and opened again when the next session starts in the same folder, which in the desktop app is at the first message after a typed `/clear`." The Scope's Out line names the `other` cost. AC1 now promises the mod's side only, AC3 asserts at the next start, AC4 waits for the first message, and AC7 is new (texts as in the criteria). T2 and T3 follow, and AC1 no longer needs T3.
- re-audit: AC1 (full) — 2 findings: narrow to the mod's own property; the stub-driven assertions are a guard, not red-first.
- re-audit: AC3 (full) — 5 findings: assert at the next start, empty panes between end and start instead of closing in the end stub, split `other` into AC7, add a one-shot case to T2.
- re-audit: AC4 (full) — 2 findings: point at T1's window, not a number; name the held command as the first message for a press.
- re-audit: AC7 (full) — first audited as part of AC3's findings; its wording came from finding 4.
- re-audit: AC1 (full) — 1 finding: say T1 saw the result only for a desktop press.
- re-audit: AC3 (full) — nothing (one optional reason phrase, taken).
- re-audit: AC4 (full) — 1 finding: "once the first message after the clear is sent".
- re-audit: AC7 (full) — 1 finding: narrow to a pane open and shown at the end.
- 2026-10-06: stop answered: the second reader's narrowings to AC1, AC4, and AC7 went to the operator as the repeat-churn stop, and the operator accepted them as shown.
- 2026-10-06: T2 added 11 cases in `pane.test.tsx` with `mock.store(on)` and a `panesOf` helper that both the `ui.panes` stub and the cases read, since the test-side `$` has no `$.ui.panes()`. Against the old `register.tsx`, the AC7 same-cwd case and the once-only case failed, and the other 9 passed. The another-cwd case uses `/sub`, which still finds the fixture's ROADMAP, so only the cwd key keeps the pane closed.
- 2026-10-06: T3 chose a store key `reopen` holding a list of cwds, marked before `next(e)` at an `other` end when the pane is listed, shown, and placed, and read at `session.start` after the refresh. The start clears its cwd's mark and opens only when the refresh found a ROADMAP. Store and pane failures are caught, because the band and the other suites do not answer `$.store`. verify: 1302 mod tests pass, both unittest suites and both validates exit 0.
- 2026-10-06: T4 added the reopen to README.md's pane section, to `cairn/DESIGN.md` after the M219 pane text and in the `hooks/status/` component line, and to a new Unreleased section in CHANGELOG.md, since 2.0.0 was cut today. Each names the app-quit cost and the desktop app as the surface checked live. verify: all five commands exit 0.
- 2026-10-06: claim audit pass (fresh Opus reader): 33 claims read, 7 wrong, all corrected toward the narrower claim. A typed `/clear` reopens only a pane that was shown, the app-quit cost is stated as a condition that was not checked, the reopen needs a found ROADMAP, and a press keeps the process, not the session. The reader's re-read found 5 holding and 2 still wrong (the README and CHANGELOG lead sentences), now "shown at a `/clear`".
- claim audit: 33 claims read, 7 corrected — README.md, CHANGELOG.md, hooks/status/register.tsx
- 2026-10-06: T5 operator look, typed `/clear` (new desktop session in this repo): the pane closed at the clear and opened again when the operator sent "hi" in the new session. That meets AC4 for a typed `/clear`. No Clear Button showed, because the band and pane draw it only after a cairn skill's step ends, and `Plan` or `Implement` show only with no active milestone. The press cases go next: Clear after a short cairn skill here, and `Plan` in a throwaway repo with one done row at the session scratchpad's `m222-look`.
- 2026-10-06: T5 operator look, the band's or pane's Clear Button after `/cairn:milestone`: the pane stayed open but showed `no cairn ROADMAP found` until the operator typed "hi", then filled again. The pane draws that line when its state's `found` is false, which is the empty state, and the mod refreshes only at `session.start`, a turn end, a Stop, or a prompt, none of which a press raises. So the host's state starts empty under the new session id. Minor amendment: discovered sub-task T6 before T5 refreshes at `classic.SessionStart` with source `clear`, which T1 saw 0.1 s after a press's end.
- 2026-10-06: T6 the `session start after a clear` case in the M205 AC5 event list failed against `register.tsx` (the T2 tick did not show), then passed with a `classic.SessionStart` hook that refreshes when the source is `clear`. DESIGN names the hook. verify: 1303 mod tests pass, and the other four commands exit 0.
- 2026-10-06: T5 operator look after T6, Clear Button press in a new desktop session: the pane's contents disappeared very briefly and then came back, with no prompt typed. The operator called this great. The `Plan` press in `m222-look` is the one AC4 clear not yet seen.

## Decisions

## Review
