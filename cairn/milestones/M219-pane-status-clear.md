# M219: Status and Clear buttons in the cairn pane

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m219-pane-status-clear

## Goal

The cairn pane carries the band's Status and Clear buttons on a row of their own under the Next line.

## Scope

**In:** The pane's Next line carries more Buttons after the M218 Next
Button. The Clear Button, key `cairn-pane-clear`, shows while the `ended`
atom (M216) is true. The Status Button, key `cairn-pane-status`, comes last. Each sits in its own Box
that does not shrink, so the pill is cut first. Both are `secondary` and use
the band's labels, `Clear` and `Status`. They show while no cairn skill's
step is set, as the Next Button does (M218). The operator moved them here
from a row of their own at the first live look (work log). A press runs the band's
press (`pressClear` or `pressStatus` in `register.tsx`), so it runs the same
command and does nothing in the same cases. README, DESIGN, CHANGELOG, and
the header comments of `pane.ts` and `register.tsx` describe it.

The milestone promotes the item "The pane has no Status or Clear Button
(M218 plan)" of "Pane button follow-ons (M218 review)".

**Out:** Changes to the band's Buttons. A pane line that hides while a turn
runs outside a cairn skill. A pane gets no `isWorking` prop, and
`$.command.run` queues a press until the session is idle. That item stays in
"Pane button follow-ons (M218 review)". A test that the pane redraws on a
change to `ended` alone, after a dropped typed prompt. The band's M216 tests
cover that path, and review files the gap in the same row.

## Acceptance criteria

- [x] AC1: The fixtures with a ROADMAP are `WITH_ROADMAP` in
      `pane.test.tsx`. For each one, on the terminal and desktop surfaces,
      with no cairn skill's step set and no cairn skill ended, the Next line
      draws its Buttons after the pill. Mod tests assert that the Next line's
      child Boxes are `next-lead`, `next-text`, `next-action`, then
      `next-status`; that its Button keys are exactly [`cairn-pane-next`,
      `cairn-pane-status`]; that the pane has no element with key
      `cairn-pane-clear`; and that `cairn-pane-status` has `variant`
      `secondary` and label `Status`.
- [x] AC2: For one fixture with a next step, on the terminal and desktop
      surfaces, after a cairn skill's prompt starts its step, the pane draws
      no element with key `cairn-pane-status` or `cairn-pane-clear`. After a
      Stop with nothing in flight ends the step, the Next line's Button keys
      are exactly [`cairn-pane-next`, `cairn-pane-clear`,
      `cairn-pane-status`], and `cairn-pane-clear` has `variant` `secondary`
      and label `Clear`. After an idle typed prompt that follows, they are
      exactly [`cairn-pane-next`, `cairn-pane-status`]. A mod test asserts
      the three states in order.
- [x] AC3: On the terminal and desktop surfaces, a press of
      `cairn-pane-status` runs `$.command.run` with the command
      `cairn:milestone` and the args `''`. A press of `cairn-pane-clear`,
      drawn after a Stop ends a step, runs the command `clear` with the args
      `''`. Mod tests press each Button and read the command and args that
      reached beneath. A press of `cairn-pane-status` while a run started by
      `cairn-pane-next` is held runs no command, and a mod test asserts this.
- [x] AC4: On the terminal and desktop surfaces, after a Stop ends a step,
      the Boxes `next-clear` and `next-status` have `flexShrink` 0, and the
      pill's Box `next-text` keeps `flexShrink` 1 and `minWidth` 0. A mod
      test asserts these props.
- [x] AC5: At a live look in the desktop app, in a real cairn repo, each
      press of the pane's Status or Clear Button that reaches the mod runs
      its command once. A Status press starts the status skill. After that
      skill ends, a Clear press clears the conversation. A first click that
      only gives the pane keyboard focus reaches no press, and the row "Mod
      pane placement (upstream)" holds it. The operator accepts the look of
      the Next line.
- [x] AC6: README.md and `cairn/DESIGN.md` describe the pane's Status and
      Clear Buttons. CHANGELOG.md's unreleased section has an entry for them.
- [x] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2, T4
- AC2 → T1, T2, T4
- AC3 → T2
- AC4 → T4
- AC5 → T5, T7
- AC6 → T3, T6
- AC7 → T8

## Tasks

- [x] T1: Write the AC1 and AC2 tests first in `pane.test.tsx`. Change the
      M218 AC1 test, which asserts that the pane's only Button is
      `cairn-pane-next` (`pane.test.tsx:746`), to read the Next line's
      Buttons alone. In `pane.ts`, give `paneLines` a flag for `ended`.
      While `acts` is true, add the `actions` line after `next`. It carries
      the Buttons to draw, in order. Move `STATUS_LABEL` and `CLEAR_LABEL`
      beside `NEXT_LABELS`, so the band and pane read one place.
- [x] T2: Write the AC3 tests first, with the press pattern of the M218 AC3
      tests (`copy.runHold`, `copy.commands`). In the pane's `ui.render` hook
      (`register.tsx:155-213`), read `ended`. Draw each Button of the
      `actions` line in a Box with `flexShrink` 0. Its `onPress` is
      `pressClear($)` or `pressStatus($)`.
- [x] T3: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the header
      comments of `pane.ts` and `register.tsx`.
- [x] T4: Move Clear and Status onto the Next line after `next-action`,
      each in a Box keyed `next-<kind>` with `flexShrink` 0 and
      `marginLeft` 1, and drop the `actions` line. Rewrite the M219 AC1 and
      AC2 tests and the M218 AC1 test for it, and add the AC4 test.
- [x] T5: Probe the double click: temporary logging to `m219-probe.log` at
      the plugin root, of each pane render's `isFocused`, each `ui.press`,
      each press function's checks, and each run. The operator repeats the
      look and the log shows where a first click goes. Where the cause is in
      the mod, fix it. Remove the probe before review.
- [x] T6: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the header
      comments for the Next-line placement.
- [x] T7: Live look (AC5): the operator opens a new Code session in a real
      cairn repo whose state shows a Next line (LESSONS M195, M213). The
      operator opens the pane and presses Status once. After the status
      skill ends, the operator presses Clear once.
- [x] T8: Run every `verify` command from the repo root and check each exit
      code.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: question set: what to build — the pane's Status and Clear Buttons (promotes that item of "Pane button follow-ons (M218 review)").
- 2026-10-04: question set: where the Buttons go — a row of their own under the Next line, lined up under the pill.
- 2026-10-04: question set: a live look in the desktop app before the merge question — yes, one live look.
- 2026-10-04: plan gate chose a row of its own under the Next line over the Next line itself. At the 44-column dock, the pill, Next, Clear, and Status do not fit on one line, and the pill gets cut. An operator rejection of the row at the AC4 look falsifies it.
- 2026-10-04: plan gate chose to show Status whenever no cairn skill's step is set. The band also needs a next-step label, but the pane's Next line exists for every found ROADMAP, because reader.ts `recommend` never returns null. Falsified by a pane state with no Next line in a real session.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 2 minor findings and a wording note. Each went toward the narrower promise. AC1 names the exact-keys assertion for its one-Button and no-Clear claims. T1 changes the M218 test that reds once Status draws. AC2 stays as written. Its three states each rewrite the pane, so the band's M216 tests keep the dropped-prompt path, and Out names it. AC4 says "the status skill" and not `/milestone`. AC3, AC5, and AC6 had no finding. No IP or D-entry blocks a criterion.
- 2026-10-04: collision check: the plan absorbs the Status-or-Clear item of candidate "Pane button follow-ons (M218 review)", and post-merge hygiene trims it. The GitHub inbox has no open issues or PRs. D-143 (the mod ships in the plugin) has no conflict. No D-entry rejects the change.
- 2026-10-04: the new row put ROADMAP.md at 24,117 bytes, over its 24,000 budget. The plan cut two `[low]` rows' asides, to 23,998 bytes.
- 2026-10-04: the plain-English lint hook keeps 12 hits on this file. They are cairn's required `—` slot markers and question-set separators, and three long sentences in the audited criteria, which stay as the audit read them.
- 2026-10-04: implement started on branch m219-pane-status-clear. The untracked `cairn-probe.log` and `tsconfig.json` predate the milestone and stay unstaged.
- 2026-10-04: minor amendment: T1 also draws the `actions` line's Buttons in `register.tsx`, because the AC1 and AC2 tests mount the pane. T2 keeps the presses and their tests.
- 2026-10-04: T1 done. `paneLines` takes `ended` and adds `actions` (indent 6, the Next lead's width) with `['clear', 'status']` or `['status']`. `STATUS_LABEL` and `CLEAR_LABEL` moved to `pane.ts`. The M218 AC1 test reads the Next line's Buttons alone. The press goes through an inline `onPress` to the top-level `pressClear` or `pressStatus` (LESSONS M191). A planted swap of the Clear and Status order turned both AC2 cases red, and it was restored. Verify: all five exit 0, mod tests 1237.
- 2026-10-04: T2 done. Six AC3 tests press Status, Clear after a Stop, and Status during a held Next run, on both surfaces. Planted swapped presses turned the 4 press cases red. A `pressStatus` with no `running` check turned the 2 held-run cases red. Both were restored. Verify: all five exit 0, mod tests 1243.
- 2026-10-04: T3 done. README's pane section, DESIGN's `hooks/status/` entry and pane paragraph, a CHANGELOG Unreleased entry, and the `pane.ts` and `register.tsx` header comments describe the `actions` line. Verify: all five exit 0.
- 2026-10-04: claim audit: 30 claims read, 6 corrected — CHANGELOG.md, README.md, cairn/DESIGN.md, hooks/status/pane.ts, hooks/status/register.tsx, hooks/status/pane.test.tsx
- 2026-10-04: the corrections narrow "after a cairn skill ends" to the `ended` span, from a Stop that ends a step to the next idle typed prompt, cairn skill prompt, or session end. They also fix a test comment on `acts`. The same reader re-read all six as accurate. It noted that the user docs leave out two edge cases, a prompt typed mid-turn and a step that an idle typed prompt ends. They stay out, as M216's own wording does. Verify: all five exit 0.
- 2026-10-05: live look (AC4): the operator reported "something is off" with no detail yet. The run waits for the description before a fix.
- 2026-10-05: live look (AC4 as then numbered): the operator reported "the status button was bumped to the next line below the plan button. each button had to be clicked twice to work". Plan was not pressed.
- 2026-10-05: question set at the live-look stop: where Status and Clear go — on the Next line after Plan (operator override of the plan's row under Next). The Goal's "on a row of their own under the Next line" clause is superseded by this choice. The Goal is not edited in place.
- 2026-10-05: substantive amendment: Scope In, AC1, and AC2 move the Buttons onto the Next line. New AC4 holds their Boxes' `flexShrink`. The live look becomes AC5 and asks for one press each. Docs become AC6 and verify AC7. T4 (the move), T5 (a double-click probe), and T6 (docs again) are new, and the look and verify become T7 and T8.
- 2026-10-05: re-audit: AC1 (full) — one-press placement after the pill not asserted, and the pane-wide no-Clear check dropped. Both were fixed by naming the child Boxes and the pane-wide check.
- 2026-10-05: re-audit: AC2 (full) — nothing
- 2026-10-05: re-audit: AC4 (full) — the Boxes had no keys. Fixed by naming `next-clear` and `next-status`.
- 2026-10-05: re-audit: AC5 (full) — two clicks passed the old wording. Fixed to one press each.
- 2026-10-05: re-audit: AC1 (full) — nothing
- 2026-10-05: re-audit: AC4 (full) — nothing. It noted that the not-ended `next-status` Box is unasserted, and the code is the same literal in both states.
- 2026-10-05: re-audit: AC5 (full) — "one press" can bind the desktop host. A click that focuses the pane can redraw it and retire the press handle (`ButtonProps.onPress`: a handle "for the drawing's life"), which the mod cannot change. This is AC5's second line, so its wording goes to the operator once T5's probe shows where the first click goes.
- 2026-10-05: AC3's wording is unchanged, and the first reader returned nothing on it.
- 2026-10-05: T4 done. `paneLines` sets `next.buttons`, and `register.tsx` draws `next-clear` and `next-status` after `next-action`. Mod tests 1244, exit 0. T5's probe code is in this commit, marked PROBE, and is removed before review.
- 2026-10-05: T5 done. At the probe look in bsync (desktop, docked pane 47 columns), each first click logged a render with `focused=true` and no `ui.press`. The second click logged `ui.press` for `cairn-pane-status` and then for `cairn-pane-clear`, and each ran its command once (`run start cairn:milestone #1`, `run start clear #2`). After each run the pane rendered `focused=false`. The cause is the desktop host, so the mod has no fix. The probe code is removed. The log stays local in `m219-probe.log`, excluded from git.
- 2026-10-05: question set at the probe stop: how AC5 treats the first click. The operator chose to count presses that reach the mod and file the focus-only click upstream. The alternative, refocusing the pane after each press, was declined because it takes the keyboard from the prompt. A host change that raises a press on a focusing click falsifies the choice. The operator also accepted the Next line's look.
- 2026-10-05: substantive amendment: AC5 is reworded at the operator's choice, so no further re-audit reader runs (its second line exists).
- 2026-10-05: T7 done: the probe look is the AC5 look. "Mod pane placement (upstream)" gains the first-click item, merged into that row to keep ROADMAP.md under 60 lines. Three rows were trimmed, to 23,998 bytes. An upstream report draft is in `pane-click-issue-draft.md`, local and excluded from git.
- 2026-10-05: T6 done. README, DESIGN, CHANGELOG, and the `register.tsx` layout comment describe the Next-line placement. README and DESIGN state the focus-only first click. That prose was written against the probe log and the code in this session, after the one claim-audit pass.
- 2026-10-05: T8 done. Verify: all five exit 0, mod tests 1244. Status set to review.

## Decisions

## Review

Review pass 1, 2026-10-05, on `beb769b` (branch current with `origin/main` `b671def`; resume route (d), no PR).

- AC1 evidence: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0, 1244 tests, 0 fail. The 40 cases of "the Next line carries the Status Button after Next (M219 AC1)" (20 `WITH_ROADMAP` fixtures × terminal and desktop) pass. Each asserts the child Boxes `next-lead`, `next-text`, `next-action`, `next-status`, the Button keys [`cairn-pane-next`, `cairn-pane-status`], no `cairn-pane-clear`, and Status `secondary`/`Status`.
- AC2 evidence: same run. Both cases of "a running skill hides Status, and its end adds Clear (M219 AC2)" pass, asserting the three states in order. A planted swap of the Clear and Status order turned both red at T1 (work log).
- AC3 evidence: same run. The 6 cases of "a press of Status or Clear runs its command (M219 AC3)" pass: Status → `cairn:milestone` `''`, Clear after a Stop → `clear` `''`, and a Status press during a held Next run reaches no run. Planted swapped presses and a `pressStatus` without its `running` check turned them red at T2 (work log).
- AC4 evidence: same run. Both cases of "the pill gives way before Clear and Status (M219 AC4)" pass, asserting `flexShrink` 0 on `next-clear` and `next-status` and 1/0 on `next-text`.
- AC5 evidence: `m219-probe.log` (local, from the probe look in bsync, desktop, 2026-10-05) shows one `ui.press element=cairn-pane-status` followed by one `run start cairn:milestone #1`, and later one `ui.press element=cairn-pane-clear` followed by one `run start clear #2`. The first clicks logged only a `focused=true` render, with no press, which AC5 leaves to "Mod pane placement (upstream)". The operator accepted the Next line's look at the 2026-10-05 chip (work log).
- AC6 evidence: README.md lines 257-266 describe the Status and Clear buttons on the Next line. `cairn/DESIGN.md` lines 73 and 280-288 describe them. CHANGELOG.md's `## Unreleased` `### New` opens with "Status and Clear buttons in the cairn pane."
- AC7 evidence: from the repo root, `python3 -m unittest discover -s scripts/tests` exit 0 (397 tests, OK, skipped 21), `python3 -m unittest discover -s hooks/tests` exit 0 (174, OK), `claude plugin validate .claude-plugin/plugin.json` exit 0, `claude plugin validate .claude-plugin/marketplace.json` exit 0, and the mod test above exit 0.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed. No principle changed, so no `cairn_impact`. The profile slot: verify green on the review head. The marketplace validate prints "Validation passed" with no `plugins[N].version` warning. CHANGELOG has the entry, with no milestone number.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the pane shows Clear during a turn outside a cairn skill (no `isWorking`), so a press queues `/clear` after that turn, where the band hides Clear — follow-up (the queueing is Scope Out; README wording fixed now, see blame-history #2)
- diff-bug #2: Status and Clear draw when the next action has no label, unlike the band's `canAct` and the docs' "after that button" — fix now (buttons only with a label)
- diff-bug #3: CHANGELOG lacks the desktop two-click note — fix now
- diff-bug #4: README's first-click sentence is garbled and states one probe's finding broadly — fix now (reworded)
- diff-bug #5: below about 38 columns the fixed Boxes push the line past the edge — follow-up
- diff-bug #6: test gaps: no pure `paneLines` test of `buttons`, the not-ended `next-status` Box unasserted, no stale pane Clear press, the M218 AC1 test no longer pins the pane's only Button — the last fixed now (a pane-wide Button check in the M219 AC1 test), the rest follow-up
- diff-bug #7: the Goal and T1/T2 still describe the dropped row, and DESIGN carries history prose — Goal and tasks rejected (planned: the work log supersedes them, never edited in place); DESIGN fixed now
- blame-history #1: "Pane button follow-ons (M218 review)" still says the pane has no Status or Clear Button — reject (planned change: post-merge hygiene trims a promoted item, records-hygiene §1)
- blame-history #2: README and CHANGELOG say any prompt removes Clear, but a prompt typed mid-turn keeps it — fix now ("while Claude is idle")
- blame-history #3: pane and band differ on when Status and Clear show (no label, a closed band, `next` null) — the label part fixed now (diff-bug #2), a closed band showing pane Clear follow-up, `next` null rejected (false: `recommend` never returns null for a found ROADMAP)
- blame-history #4: four unrelated ROADMAP rows were trimmed, and the work log's 23,998 is not the branch's size — trims noted (no content lost, per the lens), the figure rejected (false: it was the size at that edit, before the status change)
- blame-history #5: "Mod pane placement (upstream)" now holds two topics — noted (both upstream pane faults, merged to keep the 60-line cap)
- blame-history #6: the M218 AC1 test is weaker — fix now (as diff-bug #6)
- blame-history #7: the labels moved to `pane.ts` — noted (no behavior change)
- blame-history #8: stale Goal and task text — reject (planned, as diff-bug #7)
- blame-history #9: CHANGELOG long line and an ambiguous "Both", and the DESIGN list's chained clauses — the first two fixed now, the third rejected (style)
- blame-history #10: untracked `cairn-probe.log` and `tsconfig.json` — noted (predate the milestone)
- prior-review #1: the pill is cut harder at a 44-column dock, and no test bounds it — follow-up (with diff-bug #5)
- prior-review #2: the stale ROADMAP row, and the gray Buttons unchecked in other themes — row rejected (as blame-history #1), the theme item follow-up
- prior-review #3: the theme gap now covers two more pane Buttons — follow-up
- prior-review #4: the AC2 test starts the skill by a prompt, not a press — follow-up
- prior-review #5: no pane test of Clear during a held run, or of a press after the release — follow-up
- prior-review #6: the M218 AC1 test is weaker — fix now (as diff-bug #6)
- prior-review #7: the refused-press and queued-press items now cover Status and Clear — follow-up
- Follow-ups go to a new row, "Pane Status and Clear follow-ons (M219 review)", at post-merge hygiene, because "Pane button follow-ons (M218 review)" heads a finding-absorbing group (records-hygiene §7). No finding shows a criterion failing or a load-bearing defect, so no return.
