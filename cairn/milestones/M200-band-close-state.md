<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M200: A close button that holds through refreshes and session ends

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the band and its close button ship to every plugin user
- **Branch/PR:** m200-band-close-state

## Goal

Make the band's close button follow one rule through the four edge cases in the "Band close-state edge cases" candidate row.

## Scope

**In:**
- Lost press: `reconcile` in `hooks/status/register.tsx` (lines 218-223) reads `dismissed` and writes null in two steps. The decision moves inside the `update` callback.
- Failed read: when `cairn/ROADMAP.md` is found but its read fails, a refresh keeps the band's rows and its close state. A ROADMAP that is not found still empties the band, as today.
- Session end: every session end clears the close state, so a band hidden by a press shows again after any reason, with or without a running skill.
- Unknown stored skill: `mark` and `same` move to `hooks/status/band.ts`. The mark reads the step through `knownStep`, so the press, the refresh, and the drawing agree.
- A desktop live look at a press followed by `/clear`, and the docs that state the new rules.

**Out:**
- A skill's label across background waits → the "Band skill label across background waits" candidate row.
- The press storing the drawn state instead of reading it again: the plan gate rejected it (see the work log).
- A ROADMAP that briefly vanishes, for example during a git checkout: still empties the band. The plan gate kept the missing-file case as it is.
- Other band follow-ons → the "Status mod follow-ons" candidate row.

## Acceptance criteria

- [ ] AC1: In `hooks/status/register.tsx`, the function that clears the close state at a refresh decides inside its `update` callback. It decides from the value that callback receives, so no await separates the decision from the write. This code check is the evidence for the lost-press fix. Two `claude plugin test` guard cases over `single-in-progress` hold the ROADMAP read open until a press resolves, and both also pass on main. With the file unchanged, the band stays hidden. With M002 moved from `in-progress` to `review`, the band shows again.
- [ ] AC2: When `cairn/ROADMAP.md` is found but its read fails, a refresh leaves the band's rows and its close state as they were. In these cases `fs.stat` reports the ROADMAP as a file and `fs.read` of it rejects. One `claude plugin test` case over `single-in-progress` presses and runs a turn end with the failing read. It then runs a turn end with a good read of the same file. It checks that the band is hidden after each turn end, and on main it fails at the good read. A second case, with no press, runs a turn end with the failing read and still draws `M002-row`. It fails on main. The existing `no-roadmap` cases, where no ROADMAP is found, stay green.
- [ ] AC3: A session end brings back a band that a press hid, whether or not a cairn skill was running at the press. After `session.end` with reason `clear` or with reason `resume`, the next drawing shows the band's row. Shown by `claude plugin test` cases over `single-in-progress` on the terminal and desktop surfaces. They cover both reasons, once with no skill running and once with `milestone-plan` running. The no-skill cases fail on main. The `session.end` hook in `register.tsx` does not branch on `e.reason`.
- [ ] AC4: A stored step whose skill is not a key of `SKILL_LABELS` counts as no step in two places: when the close button stores its mark, and when a refresh compares against that mark. The drawing of the band already reads it that way. A direct test covers the mark function, which moves to `hooks/status/band.ts`. Over the `no-active` band state, the mark for a step with the skill `milestone-gone` equals the mark for no step. Both marks name the idle id `M021`. A planted copy of the function that skips the label check turns the test red. `dismiss` and `reconcile` in `register.tsx` call the mark function from `band.ts`.
- [ ] AC5: Three places state two behaviors. The places are the README's close-button paragraph, the CHANGELOG's Unreleased entry, and the `hooks/status/` bullet in `cairn/DESIGN.md`. First, a session end shows a hidden band again. Second, a failed read of a found ROADMAP leaves the band as it was. In those three places, each sentence about `/clear` states what a `/clear` does to a hidden band, as T5's live look showed. Run the sweep `grep -n -iE 'close button|hidden|press|session end|ROADMAP|cleared' README.md CHANGELOG.md cairn/DESIGN.md hooks/status/register.tsx hooks/status/band.ts hooks/status/reader.ts types/index.d.ts`. Each line it returns from those three places and from the five code files, read in context, states current behavior.
- [ ] AC6: Each of the four verify commands in `cairn/PROFILE.md` exits 0 on the branch head.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6
- AC6 → T1, T2, T3, T4, T6

## Tasks

- [x] T1: Lost press. In `reconcile` (`register.tsx:218-223`), compute the current mark. Then decide inside `update($, dismissed, hidden => …)`. The callback returns null only for a set `hidden` that differs from the current mark. Add the two held-read guard cases. The `fs.read` handler awaits a promise the test holds, and the test waits on a timer until the read is held. A microtask loop does not reach the read, as the plan probe showed.
- [ ] T2: Failed read. For a found ROADMAP that it cannot read, `loadBand` in `reader.ts` returns null. On null or on a throw, `refresh` keeps both atoms. With no root found, it still empties the band. Update the `refresh` comment ("No readable working directory or ROADMAP"). Add the AC2 cases, and show each red on main first. Check that `reader.test.ts` still passes over every fixture.
- [ ] T3: Session end. After the step is cleared, the `session.end` hook sets `dismissed` to null, with no branch on the reason. Add the no-skill cases for `clear` and `resume` on both surfaces, red on main first. Keep the running-skill case at `band.test.tsx:1420` and add its `resume` twin.
- [ ] T4: Unknown stored skill. Move `mark` and `same` from `register.tsx:192-205` to `band.ts`, exported. The mark reads the step through `knownStep`. `ui.render`, `dismiss`, and `reconcile` call it. Add the direct test and show it red against a planted copy that skips the label check.
- [ ] T5: Live look. Open a new desktop Code session, because the mod loads at session start. Press the close button on a showing band, run `/clear`, and see whether the band returns. Log what showed. If the band stays hidden, stop at the amendment gate before T6.
- [ ] T6: Docs. Update the README close-button paragraph, the CHANGELOG Unreleased entry, the DESIGN.md `hooks/status/` bullet, and the `register.tsx` header comment. Run the AC5 sweep and read each hit in context. Run the four verify commands.

## Work log

- 2026-10-02: created by /milestone-plan, promoting the "Band close-state edge cases" candidate row (the row stays until post-merge hygiene).
- 2026-10-02: plan probe in a scratch copy of the mod: a press made while a turn-end refresh's ROADMAP read was held stayed hidden on main with the file unchanged. So M199 review item B7 loses no press. The lost-press window is the awaits inside `reconcile`, after the read returns.
- 2026-10-02: criteria audit (full mode, fresh Opus reader): 7 findings, all fixed before the gate. AC1's held-read cases became guards that pass on main, and the code check became the evidence. AC2 became one press case that fails at the good read. AC3 gained the no-branch-on-reason check. AC4 gained the call-site check. AC5 was limited to the close-button paragraph, the Unreleased entry, and the DESIGN bullet. Its sweep gained `ROADMAP|cleared`, `reader.ts`, and `types/index.d.ts`. AC5 ties `/clear` sentences to the mod's behavior, not to the log.
- 2026-10-02: plan gate chose to clear the close state at every session end over keeping the band hidden across session ends. The reason: one rule then holds whether or not the app keeps state across `/clear`. Falsified by a user who expects a hidden band to stay hidden in a new session.
- 2026-10-02: plan gate chose to keep the last state only for a found but unreadable ROADMAP over also keeping it for a missing one. The reason: a missing ROADMAP also means a move out of a cairn repo. Falsified by a real session whose band flickers back during a git checkout.
- 2026-10-02: plan gate chose the decide-inside-`update` fix over storing the drawn state at the press. The reason: it closes the window in one function and keeps M194's press behavior. Falsified by a press observed lost in a real session after the fix.
- 2026-10-02: implement started on branch m200-band-close-state; no question gate, as the plan left nothing open.
- 2026-10-02: T1 done: `reconcile` decides inside its `update` callback; two held-read guard cases added, green on the branch and on main's `register.tsx`; verify 4/4 green (plugin test 605 pass).

## Decisions

## Review
