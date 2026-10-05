# M218: A Next button in the cairn pane

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m218-pane-next-button

## Goal

The cairn pane's Next line carries a button that runs the next command, as the band's next-step button does.

## Scope

**In:** The pane's Next line keeps its colored pill and gains a
`secondary` Button after it, with key `cairn-pane-next`. Its label is the
band's next-step label for the next step's action: `Start`, `Resume`,
`Review`, or `Plan` (M212, M213). The band and the pane read that label map
from one place. The Button shows while no cairn skill's step is set. A
press runs the band's next-step press (`pressNext` in `register.tsx`), so it
runs the same command and argument and does nothing in the same cases. The
Button sits in a Box that does not shrink, so at a narrow pane the pill's
text is cut first. README, DESIGN, CHANGELOG, and the header comments of
`pane.ts` and `register.tsx` describe it.

The milestone promotes the pane part of "Status mod follow-ons"
("clickable next-command actions in the cairn pane").

**Out:** A Button in place of the pill. The mod API's Button takes no fill
color and no child elements. Such a Button loses the phase color that the
operator asked for at the M208 live look (work log). Two items go to
"Status mod follow-ons": a Status or Clear Button in the pane, and a
Button that hides while a turn runs outside a cairn skill. A pane gets no
`isWorking` prop. A press during such a turn waits until the session is
idle, because `$.command.run` queues.

## Acceptance criteria

- [ ] AC1: The fixtures with a next step are `WITH_ROADMAP` in
      `pane.test.tsx`. For each one, on the terminal and desktop surfaces,
      with no cairn skill's step set, the pane's Next line draws the pill.
      After the pill it draws one Button with key `cairn-pane-next` and
      `variant` `secondary`. The label is `Start` for the action
      `implement`, `Resume` for `resume`, and `Review` for `review`. It is
      `Plan` for `plan the next milestone`. Mod tests assert the key, the
      variant, the label, and the order.
- [ ] AC2: For one fixture with a next step, on the terminal and desktop
      surfaces, after a cairn skill's prompt starts its step, the pane draws
      no element with key `cairn-pane-next`, and the pill still draws. After
      a Stop with nothing in flight ends the step, the Button is back. A mod
      test asserts both states.
- [ ] AC3: On the terminal and desktop surfaces, a press of
      `cairn-pane-next` runs `$.command.run`. The command is `cairn:` plus
      the next step's command less its `/`. The args are the next step's id,
      or `''` for planning. Mod tests press the Button for one fixture of
      each action and read the command and args that reached beneath. A
      second press while the first run is held runs no command, and a mod
      test asserts this.
- [ ] AC4: On the terminal and desktop surfaces, the Box around
      `cairn-pane-next` has `flexShrink` 0. The pill's Box keeps
      `flexShrink` 1 and `minWidth` 0. A mod test asserts these props.
- [ ] AC5: At a live look in the desktop app, in a real cairn repo, the
      operator presses the pane's Button, sees its command start, and
      accepts the look of the Next line.
- [ ] AC6: README.md and `cairn/DESIGN.md` describe the pane's Button.
      CHANGELOG.md's unreleased section has an entry for it.
- [ ] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T2
- AC5 → T4
- AC6 → T3
- AC7 → T5

## Tasks

- [x] T1: Write the AC1 and AC2 tests first in `pane.test.tsx`. In
      `hooks/status/`, move `NEXT_LABELS` and `PLAN_LABEL`
      (`register.tsx:110-116`) to `pane.ts` or `band.ts`. The band and the
      pane then read one map. Give `PaneLine` an optional action label. If
      no cairn skill's step is set and the action has a label, set it on the
      `next` line (`pane.ts:174-187`).
- [x] T2: Write the AC3 and AC4 tests first. Use the press pattern of
      `band.test.tsx`, a `command.run` hook beneath that records the run. In
      the pane's `ui.render` hook (`register.tsx:158-200`), draw the action
      label after the pill. It is a `secondary` Button with key
      `cairn-pane-next`, in a Box with `flexShrink` 0. Its `onPress` is
      `pressNext($, label)`.
- [ ] T3: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the header
      comments of `pane.ts` and `register.tsx`.
- [ ] T4: Live look (AC5): the operator opens a new Code session in a real
      cairn repo whose state shows a Next line (LESSONS M195, M213), opens
      the pane, and presses the Button.
- [ ] T5: Run every `verify` command from the repo root and check each exit
      code.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to build — the pane's Next as a button (promotes the pane part of "Status mod follow-ons").
- 2026-10-04: question set: a live look in the desktop app before the merge question — yes, one live look.
- 2026-10-04: plan gate chose a Button after the colored pill over a Button in place of the pill because the mod API's Button takes no fill color and no child elements, so the pill loses the phase color the operator asked for at the M208 live look; falsified by the operator rejecting the Next line at the AC5 look, or a mod API Button that takes a fill color.
- 2026-10-04: plan gate chose showing the Button whenever no cairn skill's step is set over a new atom that tracks a running turn because the pane gets no `isWorking` prop and `$.command.run` already queues until idle; falsified by a press during a running turn that misbehaves in a real session.
- 2026-10-04: plan gate weighed a browser-pane prototype before the live look (LESSONS M204) and skipped it because the Button is the app's native control, which a browser mockup cannot draw; falsified by the operator rejecting the look at AC5.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 5 findings, each decided toward the narrower promise. AC3 drops its step-set press case, because the test kit presses the current drawing, which then has no Button (band.test.tsx:3132-3134). The step check stays `pressNext`'s own, shared with the band. AC3 names both surfaces. AC4 drops the fixture and the 44 columns, which change nothing in the asserted props. AC2 narrows to the one fixture and the surfaces its test sweeps. AC6 leaves out the header comments, which T3 still updates and which no user reads. AC1, AC5, and AC7 had no finding.
- 2026-10-04: the new row put ROADMAP.md at 60 lines and 24,291 bytes. The plan removed the stale R-package note line, which PROFILE.md replaces since M215, and cut two candidate rows' asides, to 58 lines and 23,966 bytes.
- 2026-10-04: collision check: candidate "Status mod follow-ons" absorbed in part (its pane-button item), trimmed at post-merge hygiene; no open issues or PRs; no D-entry rejects the change.
- 2026-10-04: implement start: branch m218-pane-next-button cut from origin/main at d1bfdbc. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-04: T1+T2 landed in one commit, the code written before its tests in one pass (a deviation from tests-first). `NEXT_LABELS` and `PLAN_LABEL` moved to `pane.ts`. `paneLines` takes an `acts` flag, and `register.tsx` passes true while `knownStep` reads no step. The Button sits in a `next-action` Box with `marginLeft` 1 rather than a space Text, so the Next line's text stays as the M205 AC3 test reads it. Mod tests went from 1136+ to 1193, all 5 verify commands exit 0.

## Decisions

## Review
