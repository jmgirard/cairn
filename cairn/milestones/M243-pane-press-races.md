# M243: A second press during a press's checks runs no second command

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing, because every adopter presses these Buttons in the band and the cairn pane
- **Branch/PR:** m243-pane-press-races

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

- [ ] AC1: Four Buttons each take two presses started together with `Promise.all`, while every guard passes and with no session end between. The Buttons are the band's `cairn-next` (`pressNext`), `cairn-status` (`pressStatus`), and Clear (`pressClear`), and a pane blocked line's `Finish` (`pressBlocked`). Each pair calls `$.command.run` once. Verified by mod tests that assert the recorded calls.
- [ ] AC2: The pane's `cairn-pane-status` press and its ⌂ press, started together with `Promise.all`, call `$.command.run` once, in either order. The call carries the command of the press listed first (`cairn:milestone` or `clear`). Verified by mod tests that assert the recorded calls for both orders.
- [ ] AC3: `grep -n 'async function press' hooks/status/register.tsx` lists a set of functions. Each one contains no `await`, or it sets a mark that its own entry check reads before its first `await`. That mark is one that `busy()` reads, or `pressing` for `pressRefresh`. Where a press releases its mark and then runs a command, no `await` comes between the release and `run` setting `running` or the press setting `heldRun`.
- [ ] AC4: In two cases, a press whose checks fail leaves the next free press able to run. In case one, a pane `Finish` press finds a step set, and a `classic.Stop` then clears the step. In case two, a pane `Finish` press reads a changed PR word. In both cases, a pane `cairn-pane-status` press after it calls `$.command.run` with `cairn:milestone`. Verified by mod tests that assert both cases.
- [ ] AC5: CHANGELOG.md's `## Unreleased` `### Fixes` gains an entry. It says that a second press of these Buttons during the first press's checks starts no second command. DESIGN.md's current-behavior text on `busy` names the shared press mark, and it names the four presses and the ✎ press (`pressCandidate`) that set it. No DESIGN.md current-behavior text names `candidateCheck`.
- [ ] AC6: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T1, T2, T3

## Tasks

- [x] T1: Write the tests first, in `hooks/status/band.test.tsx` and `pane.test.tsx`. Add a `Promise.all` double press for `cairn-next`, `cairn-status`, and `Clear` on the band. Add one for a blocked line's `Finish` in the pane. Add the pane `Status` and ⌂ pair in both orders, and the two AC4 cases. The band Clear case needs `ended` true from a skill end. The `Finish` cases need a `gh` fake that answers MERGED. AC4's changed word needs a `state.get` hook on `prs` during the press (the pattern at pane.test.tsx:3098). Run the tests against the current code and record which go red. The AC1 cases and the Status-first AC2 order are expected red. The ⌂-first order and the AC4 cases are expected green, because `pressHome` already marks itself.
- [ ] T2: In register.tsx, rename `candidateCheck` to one shared press mark that `busy()` reads. Set it before the first await in `pressNext`, `pressStatus`, `pressClear`, and `pressBlocked`. Clear it in a `finally` when the checks end, with no await before `run` sets `running` or `heldRun` takes over. Keep `pressCandidate` on the same mark. Update the comments on each press and on `busy`. Run the T1 tests green and the AC3 read.
- [ ] T3: Update DESIGN.md's current-behavior text on `busy`, the action presses, and `pressCandidate` (the M221 and M242 paragraphs). Add a CHANGELOG `### Fixes` entry. Run the five `verify` checks.

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
