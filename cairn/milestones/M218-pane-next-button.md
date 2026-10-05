# M218: A Next button in the cairn pane

- **Status:** review
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

- [x] AC1: The fixtures with a next step are `WITH_ROADMAP` in
      `pane.test.tsx`. For each one, on the terminal and desktop surfaces,
      with no cairn skill's step set, the pane's Next line draws the pill.
      After the pill it draws one Button with key `cairn-pane-next` and
      `variant` `secondary`. The label is `Start` for the action
      `implement`, `Resume` for `resume`, and `Review` for `review`. It is
      `Plan` for `plan the next milestone`. Mod tests assert the key, the
      variant, the label, and the order.
- [x] AC2: For one fixture with a next step, on the terminal and desktop
      surfaces, after a cairn skill's prompt starts its step, the pane draws
      no element with key `cairn-pane-next`, and the pill still draws. After
      a Stop with nothing in flight ends the step, the Button is back. A mod
      test asserts both states.
- [x] AC3: On the terminal and desktop surfaces, a press of
      `cairn-pane-next` runs `$.command.run`. The command is `cairn:` plus
      the next step's command less its `/`. The args are the next step's id,
      or `''` for planning. Mod tests press the Button for one fixture of
      each action and read the command and args that reached beneath. A
      second press while the first run is held runs no command, and a mod
      test asserts this.
- [x] AC4: On the terminal and desktop surfaces, the Box around
      `cairn-pane-next` has `flexShrink` 0. The pill's Box keeps
      `flexShrink` 1 and `minWidth` 0. A mod test asserts these props.
- [x] AC5: At a live look in the desktop app, in a real cairn repo, the
      operator presses the pane's Button, sees its command start, and
      accepts the look of the Next line.
- [x] AC6: README.md and `cairn/DESIGN.md` describe the pane's Button.
      CHANGELOG.md's unreleased section has an entry for it.
- [x] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

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
- [x] T3: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the header
      comments of `pane.ts` and `register.tsx`.
- [x] T4: Live look (AC5): the operator opens a new Code session in a real
      cairn repo whose state shows a Next line (LESSONS M195, M213), opens
      the pane, and presses the Button.
- [x] T5: Run every `verify` command from the repo root and check each exit
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
- 2026-10-04: correction to the T1+T2 line: "1136+" was not measured. The suite now runs 1193 tests. A planted-defect run (the Button ignoring the step, its Box with `flexShrink` 1) failed exactly the 4 AC2 and AC4 cases, 1189 pass, and the files were restored with `git checkout`.
- 2026-10-04: T3: README's pane section, DESIGN's status-mod entry and history list, a CHANGELOG entry, and the `register.tsx` header comment describe the Button (the `pane.ts` header changed at T1).
- 2026-10-04: T4 live look: in a new Code session in bsync (nothing workable), the operator pressed the pane's `Plan` Button, the planning command started, and the operator accepted the Next line's look.
- 2026-10-04: claim audit: 30 claims read, 1 corrected — hooks/status/register.tsx (the header comment called the pane's Button the band's own; it now says the pane's Button shares the band's label and press).
- 2026-10-04: the claim reader re-read the corrected comment once and found it true. T5: all 5 verify commands exit 0 (mod tests 1193 pass, 0 fail). Status set to review.
- 2026-10-04: step-7 approval: m218-pane-next-button approved for merge

## Decisions

## Review

Evidence at review head b222c89, main unmoved at d1bfdbc (2026-10-04).

- AC1: `claude plugin test .` ran 1193 tests, 0 fail. The "M218 AC1" describe passed 41 cases: the domain check plus each of the 20 `WITH_ROADMAP` fixtures on terminal and desktop, asserting one Button `cairn-pane-next`, its label from a hand-written map, `variant` `secondary`, and the line order `next-lead`, `next-text`, `next-action`.
- AC2: same run. The "M218 AC2" describe passed 2 cases (terminal, desktop) on `single-in-progress`: no `cairn-pane-next` after a `cairn:milestone-implement` skill prompt with the pill text unchanged, and the Button back after a Stop with no background tasks. A planted-defect run at implement (the Button ignoring the step) failed both.
- AC3: same run. The "M218 AC3" describe passed 11 cases: a press per action fixture (`single-in-progress` resume, `states-review` review, `idle-order` implement, `all-waiting` planning) on both surfaces, each reaching exactly `runOf(name)` beneath; the hand-written runs for planning (`cairn:milestone-plan`, `''`) and M002; and the held-run second press reaching no second run on both surfaces.
- AC4: same run. The "M218 AC4" describe passed 2 cases: `next-action` has `flexShrink` 0, and `next-text` has `flexShrink` 1 and `minWidth` 0, on both surfaces. The planted `flexShrink` 1 failed both at implement.
- AC5: at the T4 live look (work log, 2026-10-04), in a new Code session in bsync, the operator pressed the pane's `Plan` Button, saw the planning command start, and chose "Works, look is right" at the live-look chip.
- AC6: README.md:256-260 describes the button after the pill, its labels, and its press. `cairn/DESIGN.md`:271-278 describes `cairn-pane-next`, the `next-action` Box, and `pressNext`. CHANGELOG.md's `## Unreleased` section opens with "A Next button in the cairn pane."
- AC7: from the repo root at b222c89, each exit code read separately: `scripts/tests` 0, `hooks/tests` 0 (174 tests OK), plugin validate 0, marketplace validate 0, `claude plugin test .` 0 (1193 pass).

Consistency gate: `cairn_validate` all checks passed. No IP/GP changed, so no `cairn_impact` run. Profile slot: verify green at b222c89 (AC7); the marketplace validate printed no `plugins[N].version` warning; CHANGELOG.md has the entry, with no milestone number.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: a press queued during a working turn can still run after that turn starts a cairn skill — follow-up, new row "Pane button follow-ons (M218 review)".
- diff-bug #2: nothing shows the held-run test fails without the `running` guard, and no press after the release shows `running` clears — fix now, fixed 0628ab0 (a press after the release now runs again; with the guard planted out, each held-run test, the band's two included, failed by its 5-second timeout, the second press waiting behind the held run).
- diff-bug #3: `NEXT_LABELS[action]` returns an inherited property such as `toString` for an action of that name — fix now, fixed 0628ab0 (`nextLabel` reads own keys only, at both sites; its test failed on its assertion with the plain lookup planted back).
- diff-bug #4: `PaneLine.action` is documented as a general Button, but the renderer gives every such line key `cairn-pane-next` and `pressNext` — fix now, fixed 0628ab0 (the field's comment narrows to the Next line).
- diff-bug #5: a press while a run is in flight does nothing and says nothing, now reachable during a whole working turn — follow-up, new row "Pane button follow-ons (M218 review)".
- diff-bug #6: the `drawn` check is coarse, so a stale `Start` can run another milestone's command — follow-up, held by "Band button follow-ons (M212, M213 review)" ("`Review` can act on a milestone the row does not show"), which the shared `pressNext` carries to the pane.
- diff-bug #7: README and CHANGELOG say "while no cairn skill runs", but a step outlasts its skill while background work runs — fix now, fixed 0628ab0 ("runs or waits on its background work").

After the fixes, at 0628ab0, all 5 verify commands exit 0, and the mod suite runs 1194 tests with 0 failures.
- diff-bug #8: the AC1 order check does not assert the action Box's props — reject, false: the AC4 test asserts them.
- blame-history #1: the pane drops the band's `isWorking` half of the show condition — reject, planned change (Scope Out, plan work log).
- blame-history #2: the pane inherits the band's open press follow-ons through `pressNext` and adds a second press surface — follow-up, new row "Pane button follow-ons (M218 review)".
- blame-history #3: the pill is now cut first, so the M208 lost-pad `…` shows more often in a narrow pane — follow-up, new row "Pane button follow-ons (M218 review)".
- blame-history #4: the label map moved byte-identical with no other importer — noted, no defect.
- blame-history #5: the M205 text test and the M208 pill stand — noted, no defect.
- blame-history #6: the docs carry no stale text — noted, no defect.
- prior-review #1: at a 44-column dock a `Resume` or `Review` label cuts a 27-column pill — follow-up, new row "Pane button follow-ons (M218 review)".
- prior-review #2: the pane's Button is counted at terminal width, and a wider native desktop button is unmeasured — follow-up, new row "Pane button follow-ons (M218 review)".
- prior-review #3: the AC2 test starts the skill by a skill prompt, not by a press — follow-up, new row "Pane button follow-ons (M218 review)".
- prior-review #4: a refused press appends with no separator, and the press-time step check cannot be staged in the test kit — follow-up, held by "Band button follow-ons (M212, M213 review)", from the shared `run`.
- prior-review #5: the pane's gray `secondary` Button is not named in the theme row — follow-up, new row "Pane button follow-ons (M218 review)".
