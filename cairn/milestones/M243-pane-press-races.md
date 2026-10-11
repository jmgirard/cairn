# M243: A second press during a press's checks runs no second command

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing, because every adopter presses these Buttons in the band and the cairn pane
- **Branch/PR:** m243-pane-press-races, https://github.com/jmgirard/cairn/pull/253

## Goal

Each band and pane press that runs a command marks itself busy before its first await, so a second such press runs no second command.

## Scope

**In:** In `hooks/status/register.tsx`, four presses check `busy()` and
then await reads before `run` sets `running`. They are `pressNext`,
`pressStatus`, `pressClear`, and `pressBlocked`. Two presses in that
window both pass the check, and both run. Each of the four will set a
mark that `busy()` reads before its first await. `pressHome` and
`pressCandidate` already do this (M241 review, M242). The ✎ press's
`candidateCheck` becomes one shared press mark. A press whose checks
fail takes its mark back, so the next press is free. Mod tests press
each of the four Buttons twice at once. They also press `Status` and ⌂
at once, in both orders. DESIGN.md's text on `busy` and a CHANGELOG fix
entry describe the change. The README already says that a second press
does nothing while the first run is going. This change makes that true
from the moment of the press.

**Out:** The ↻ press, which its own `pressing` flag already guards
(M236). The other gaps in "⌂ edges (M241 review)" and "✎ edges (M242
review)" stay in those rows. Examples are a non-`clear` end that drops a
⌂ mark, two rows with one short title, and panes below 44 columns.
"Pane edges (M238 review)" stays as it is.

## Acceptance criteria

- [x] AC1: Four Buttons each take two presses started together with `Promise.all`, while every guard passes and with no session end between. The Buttons are the band's `cairn-next` (`pressNext`), `cairn-status` (`pressStatus`), and Clear (`pressClear`), and a pane blocked line's `Finish` (`pressBlocked`). Each pair calls `$.command.run` once. Verified by mod tests that assert the recorded calls.
- [x] AC2: The pane's `cairn-pane-status` press and its ⌂ press, started together with `Promise.all`, call `$.command.run` once, in either order. The call carries the command of the press listed first (`cairn:milestone` or `clear`). Verified by mod tests that assert the recorded calls for both orders.
- [x] AC3: `grep -n 'async function press' hooks/status/register.tsx` lists a set of functions. Each one contains no `await`, or it sets a mark that its own entry check reads before its first `await`. That mark is one that `busy()` reads, or `pressing` for `pressRefresh`. Where a press releases its mark and then runs a command, no `await` comes between the release and `run` setting `running` or the press setting `heldRun`.
- [x] AC4: In two cases, a press whose checks fail leaves the next free press able to run. In case one, a pane `Finish` press finds a step set, and a `classic.Stop` then clears the step. In case two, a pane `Finish` press reads a changed PR word. In both cases, a pane `cairn-pane-status` press after it calls `$.command.run` with `cairn:milestone`. Verified by mod tests that assert both cases.
- [x] AC5: CHANGELOG.md's `## Unreleased` `### Fixes` gains an entry. It says that a second press of these Buttons during the first press's checks starts no second command. DESIGN.md's current-behavior text on `busy` names the shared press mark, and it names the four presses and the ✎ press (`pressCandidate`) that set it. No DESIGN.md current-behavior text names `candidateCheck`.
- [x] AC6: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T1, T2, T3

## Tasks

- [x] T1: Write the tests first, in `hooks/status/band.test.tsx` and `pane.test.tsx`. Add a `Promise.all` double press for `cairn-next`, `cairn-status`, and `Clear` on the band. Add one for a blocked line's `Finish` in the pane. Add the pane `Status` and ⌂ pair in both orders, and the two AC4 cases. The band Clear case needs `ended` true from a skill end. The `Finish` cases need a `gh` fake that answers MERGED. AC4's changed word needs a `state.get` hook on `prs` during the press (the pattern at pane.test.tsx:3098). Run the tests against the current code and record which go red. The AC1 cases and the Status-first AC2 order are expected red. The ⌂-first order and the AC4 cases are expected green, because `pressHome` already marks itself.
- [x] T2: In register.tsx, rename `candidateCheck` to one shared press mark that `busy()` reads. Set it before the first await in `pressNext`, `pressStatus`, `pressClear`, and `pressBlocked`. Clear it in a `finally` when the checks end, with no await before `run` sets `running` or `heldRun` takes over. Keep `pressCandidate` on the same mark. Update the comments on each press and on `busy`. Run the T1 tests green and the AC3 read.
- [x] T3: Update DESIGN.md's current-behavior text on `busy`, the action presses, and `pressCandidate` (the M221 and M242 paragraphs). Add a CHANGELOG `### Fixes` entry. Run the five `verify` checks.

## Work log

- 2026-10-11: created by /milestone-plan.
- 2026-10-11: question set: what to plan, with no work named — the pane press races, from "⌂ edges (M241 review)" and "✎ edges (M242 review)".
- 2026-10-11: inbox sweep: no open issues and no open PRs on jmgirard/cairn.
- 2026-10-11: collision check: "⌂ edges (M241 review)" and "✎ edges (M242 review)" both carry the press-race item, and this milestone absorbs it. The rows stay until post-merge hygiene narrows them (records-hygiene §1). With "Pane edges (M238 review)" they form one finding-absorbing group (§7). This milestone is that group's bounded promotion for the items that guard shipped behavior. No D-entry covers press guards. M236, M241, and M242 shipped the pattern that this milestone extends.
- 2026-10-11: plan added `pressClear` to the row's three functions, because register.tsx:1069-1072 has the same check-then-await shape.
- 2026-10-11: plan chose one shared press mark over a mark per function. `busy()` treats every press alike, and a mark per function adds a `busy()` term per press with no behavior difference. Falsified by a case where one press's checks must not block another Button's press.
- 2026-10-11: plan chose a mark set at press entry over setting `running` at entry. `running` belongs to `run`'s numbering, where only the latest run clears it, and a press that never reaches `run` must then undo it. Falsified by a press whose mark outlives its checks and blocks a free press.
- 2026-10-11: criteria audit (full mode, fresh Opus reader) returned 7 findings on AC1-AC5 and the Goal, all fixed in this file. The Goal now names only presses that run a command, since ↻ and the open and close presses set no mark. AC1 names the Button tested per function and excludes a session end between the presses. AC1, AC2, and AC4 state their tests as "Verified by". AC2 names the pane's Status, and T1 expects the ⌂-first order green. AC3 says a mark that `busy()` reads and adds the no-await rule between the mark's release and `run`. AC4 names its two cases and Buttons, and T1 names the hooks they need. AC5 counts `pressCandidate` and drops `candidateCheck` from DESIGN.md. AC6 was clean.
- 2026-10-11: no live look planned. A desktop double click lands its two presses in separate events, and the `Promise.all` tests cover the narrower window.
- 2026-10-11: implement started on m243-pane-press-races. The untracked `cairn-probe.log` and `tsconfig.json` in the tree are not this milestone's and stay unstaged.
- 2026-10-11: T1 done. Against the unchanged code, `claude plugin test .` ran 1656 tests with 8 red, all new: the 6 band cases, the pane `Finish` case, and the Status-first AC2 order. Each red records the command twice (or Status then `clear`). The ⌂-first order and both AC4 cases pass. The AC4 changed-word case runs no Finish command, which shows that its `state.get` hook takes effect.
- 2026-10-11: T2 code: one helper, `pressChecked`, holds the shared mark `pressCheck` and runs or holds the command its checks give. `pressNext`, `pressStatus`, `pressClear`, `pressBlocked`, and `pressCandidate` pass their checks to it. Chosen over an inline try/finally in each press, which repeats the release-then-run rule five times. `pressHome` keeps its own `homeRun` mark. The five verify checks pass: 1656 mod tests with 0 red, 406 script tests, 174 hook tests, and both validates.
- 2026-10-11: AC3 read: the grep lists 9 functions. `pressPane` has no `await`. `pressRefresh` sets `pressing` and `pressHome` sets `homeRun` before their first `await`. `pressChecked` sets `pressCheck` before its first `await` and calls `run` or sets `heldRun` right after the `finally` release. The five presses that call it reach their first `await` only after the call has set the mark.
- 2026-10-11: planted-defect probe on the T2 commit: a `pressChecked` that frees the mark only when the checks give a command turned both AC4 tests and "a press while a cairn skill runs runs nothing" (M224) red, 3 of 1656. The file was restored from git, and the restored line is back.
- 2026-10-11: T3 done. DESIGN.md's M221 paragraph names `pressCheck`, `pressChecked`, and the five presses, and its M242 paragraph routes `pressCandidate` through `pressChecked`. CHANGELOG `### Fixes` gained the entry, without ✎, which had its mark since M242. The five verify checks pass again: 1656 mod tests with 0 red, and validate is green.
- 2026-10-11: claim audit: 24 claims read, 5 corrected — CHANGELOG.md, hooks/status/register.tsx, hooks/status/pane.test.tsx
- 2026-10-11: the 5 corrections: the CHANGELOG "Before" sentence now says `Plan` and `Implement` both ran `/clear`. The `busy` comment names the five press kinds. The `pressChecked` comment sets the hold before the release. The `pressCandidate` comment says `pressChecked` holds the command. The AC2 test comment says each press marks `busy`. The same reader's single re-read found all 5 hold. Verify passes after the edits: 1656 mod tests with 0 red.
- 2026-10-11: implement done, status review. No deviation from the plan beyond `pressChecked` as one helper and `pressCandidate` moved onto it.
- 2026-10-11: step-7 approval: m243-pane-press-races approved for merge

## Decisions

## Review

- Copilot arm: branch pushed, PR #253 opened, state query `none`, Copilot requested (exit 0).
- AC1: fresh `claude plugin test .` on 23ac8e8: 1656 tests, 0 red. The "two presses at once of a band Button" cases pass for `cairn-next`, `cairn-status`, and `cairn-clear` on the terminal and desktop surfaces, and "two presses at once of a blocked line Button" passes for `cairn-pane-finish-M111`. Each asserts one recorded `$.command.run` call. All 8 were red before T2 with two calls (T1 work-log line).
- AC2: same run. "a Status press and a ⌂ press at once run only the first one" passes in both orders: Status first records only `cairn:milestone`, ⌂ first records only `clear`. The Status-first order was red before T2.
- AC3: the grep on 23ac8e8 lists 9 functions. `pressPane` (958) has no `await`. `pressRefresh` (975) sets `pressing` before its first `await`. `pressHome` (1125) sets `homeRun` before its first `await`. `pressChecked` (1096) checks `busy()`, sets `pressCheck` before `await checks()`, sets `heldRun` inside the `try`, and calls `run` right after the `finally` release with no `await` between. `pressBlocked`, `pressNext`, `pressStatus`, `pressClear`, and `pressCandidate` have as their first `await` the call to `pressChecked`, which sets the mark before it suspends.
- AC4: same run. Both "a press whose checks fail leaves the next press free" cases pass: after a `Finish` press during a step and a `classic.Stop`, and after a `Finish` press that reads `closed`, a pane Status press records `cairn:milestone`, and the Finish press records nothing. The planted leak (work log) turned both red.
- AC5: on 23ac8e8, CHANGELOG.md:196 opens the first `### Fixes` entry under `## Unreleased`, saying a second press during the first press's reads does nothing. DESIGN.md:199-207 names `pressCheck`, `pressChecked`, the four presses, and `pressCandidate`. `grep -n candidateCheck cairn/DESIGN.md` finds nothing.
- AC6: on 23ac8e8, `scripts/tests` ran 406 tests OK (21 skipped), `hooks/tests` 174 OK, both `claude plugin validate` runs exit 0, and the mod test ran 1656 with 0 red.
- gate: `cairn_validate` all checks passed. The verify checks pass (AC6). The marketplace validate prints no `plugins[N].version` warning. CHANGELOG has the entry, with no milestone number. No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: `untilRuns(copy, 2, 10)` polls about 55 ms, so a late duplicate could go unseen — reject, false: the T1 reds recorded the duplicate inside that same window.
- diff-bug #2: no double-press test reaches the `/clear`-first path of Plan and Implement — fix now: "an Implement press holds once" on idle-order, fixed f04f2ec.
- diff-bug #3: AC4 case one never checks that Finish is drawn — fix now, fixed f04f2ec.
- diff-bug #4: AC4 case two infers the changed word, and an empty store would also pass — fix now: the test asserts a later drawing carries Check, fixed f04f2ec.
- diff-bug #5: the AC2 test never checks that both Buttons are drawn — fix now, fixed f04f2ec.
- diff-bug #6: DESIGN.md says the mark clears before `heldRun` is set — fix now, fixed f04f2ec.
- diff-bug #7: DESIGN.md says `pressNext` stores `heldRun` and runs `clear` — fix now, fixed f04f2ec.
- diff-bug #8: under a strict reading of AC3, the five presses set no mark themselves — reject, false: the call to `pressChecked` sets the mark before their first `await` suspends (AC3 evidence).
- diff-bug #9: the CHANGELOG lists labels and not the pane's own presses — reject, false: the pane's Next and Status carry the listed labels, and the reviewer found every label correct.
- diff-bug #10: a press in flight from a reloaded module can run while the new module's mark is free — follow-up: new row "Shared press mark edges (M243 review)" at hygiene.
- diff-bug #11: no test covers a second press in a later tick during the checks — fix now: "a second Status press during the first press's checks runs nothing", fixed f04f2ec.
- blame-history #1: DESIGN.md Known issues still says two quick presses can pass `busy` — fix now, fixed f04f2ec.
- blame-history #2: the "⌂ edges (M241 review)" and "✎ edges (M242 review)" rows still say three presses await before they mark — follow-up: post-merge hygiene narrows both rows (records-hygiene §1).
- blame-history #3: `session.end` does not clear `pressCheck`, so a read that never settles freezes every action press until a reload — follow-up: "Shared press mark edges (M243 review)".
- blame-history #4: no same-tick test of the `clears` path — fix now, the same test as diff-bug #2, fixed f04f2ec.
- blame-history #5: a ⌂ press during another press's checks now does nothing, with no toast — reject, planned change: AC2 promises exactly this.
- blame-history #6: the AC4 test hard-codes `prs-3` as a fallback shape — fix now: the Check-drawing assertion of diff-bug #4 reds if the override stops matching, fixed f04f2ec.
- blame-history #7: the CHANGELOG omits ✎, and a line wrapped mid-sentence — reject, false for ✎, which had its mark since M242, and style for the wrap, which the claim-audit commit rewrapped.
- prior-review #1: `pressCheck` is not cleared at a session end — follow-up: "Shared press mark edges (M243 review)".
- prior-review #2: the ROADMAP rows' stale sentence — follow-up: post-merge hygiene, as blame-history #2.
- prior-review #3: no double-press test of the hold path — fix now, the same test as diff-bug #2, fixed f04f2ec.
- prior-review #4: a session end between the hold and the `clear` run takes the hold — reject, false: `heldRun` is set and `run` called in one synchronous stretch, so no hook can run between them.
- prior-review #5: stale ✎ drawings are still untested after the refactor — follow-up: "✎ edges (M242 review)" already holds it.
- discrimination: on f04f2ec with main's register.tsx swapped in, the mod test ran 1660 with 12 red: the 8 T1 reds plus the 4 new band cases. The file was restored from git.
- copilot: cairn/milestones/M243-pane-press-races.md:10 (Branch/PR header lacks the PR URL) — fix now, fixed fd50f7c.
- copilot: review body — noted (its one finding is the thread above).
- Copilot level: Lite (set by GitHub's settings)
- conversation: no human reviews or comments on PR #253.
