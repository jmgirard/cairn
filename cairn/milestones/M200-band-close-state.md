<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M200: A close button that holds through refreshes and session ends

- **Status:** review
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

- [x] AC1: In `hooks/status/register.tsx`, the function that clears the close state at a refresh decides inside its `update` callback. It decides from the value that callback receives, so no await separates the decision from the write. This code check is the evidence for the lost-press fix. Two `claude plugin test` guard cases over `single-in-progress` hold the ROADMAP read open until a press resolves, and both also pass on main. With the file unchanged, the band stays hidden. With M002 moved from `in-progress` to `review`, the band shows again.
- [x] AC2: When `cairn/ROADMAP.md` is found but its read fails, a refresh keeps the band's rows, and the failed read alone does not hide or show the band. In these cases `fs.stat` reports the ROADMAP as a file and `fs.read` of it rejects. This code check is the evidence for the first sentence: `refresh` in `register.tsx` writes the `band` atom only when `loadBand` returns a band state, not null (`readText` turns the rejected read into null, and `loadBand` then returns null for a found ROADMAP), and then runs `reconcile`, which compares the close state against the `band` and `step` atoms alone. One `claude plugin test` case over `single-in-progress` presses and runs a turn end with the failing read. It then runs a turn end with a good read of the same file. It checks that the band is hidden after each turn end, and on main it fails at the good read. A second case, with no press, runs a turn end with the failing read and still draws `M002-row`. It fails on main. The existing `no-roadmap` cases, where no ROADMAP is found, stay green.
- [x] AC3: A session end brings back a band that a press hid, whether or not a cairn skill was running at the press. After `session.end` with reason `clear` or with reason `resume`, the next drawing shows the band's row. Shown by `claude plugin test` cases over `single-in-progress` on the terminal and desktop surfaces. They cover both reasons, once with no skill running and once with `milestone-plan` running. The no-skill cases fail on main. The `session.end` hook in `register.tsx` does not branch on `e.reason`.
- [x] AC4: A stored step whose skill is not a key of `SKILL_LABELS` counts as no step in two places: when the close button stores its mark, and when a refresh compares against that mark. The drawing of the band already reads it that way. A direct test covers the mark function, which moves to `hooks/status/band.ts`. Over the `no-active` band state, the mark for a step with the skill `milestone-gone` equals the mark for no step. Both marks name the idle id `M021`. A planted copy of the function that skips the label check turns the test red. `dismiss` and `reconcile` in `register.tsx` call the mark function from `band.ts`.
- [x] AC5: Three places state two behaviors. The places are the README's close-button paragraph, the CHANGELOG's Unreleased entry, and the `hooks/status/` bullet in `cairn/DESIGN.md`. First, a session end shows a hidden band again. Second, a failed read of a found ROADMAP leaves the band as it was. In those three places, each sentence about `/clear` states what a `/clear` does to a hidden band, as T5's live look showed. Run the sweep `grep -n -iE 'close button|hidden|press|session end|ROADMAP|cleared' README.md CHANGELOG.md cairn/DESIGN.md hooks/status/register.tsx hooks/status/band.ts hooks/status/reader.ts types/index.d.ts`. Each line it returns from those three places and from the five code files, read in context, states current behavior.
- [x] AC6: Each of the four verify commands in `cairn/PROFILE.md` exits 0 on the branch head.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6
- AC6 → T1, T2, T3, T4, T6

## Tasks

- [x] T1: Lost press. In `reconcile` (`register.tsx:218-223`), compute the current mark. Then decide inside `update($, dismissed, hidden => …)`. The callback returns null only for a set `hidden` that differs from the current mark. Add the two held-read guard cases. The `fs.read` handler awaits a promise the test holds, and the test waits on a timer until the read is held. A microtask loop does not reach the read, as the plan probe showed.
- [x] T2: Failed read. For a found ROADMAP that it cannot read, `loadBand` in `reader.ts` returns null. On null or on a throw, `refresh` keeps both atoms. With no root found, it still empties the band. Update the `refresh` comment ("No readable working directory or ROADMAP"). Add the AC2 cases, and show each red on main first. Check that `reader.test.ts` still passes over every fixture.
- [x] T3: Session end. After the step is cleared, the `session.end` hook sets `dismissed` to null, with no branch on the reason. Add the no-skill cases for `clear` and `resume` on both surfaces, red on main first. Keep the running-skill case at `band.test.tsx:1420` and add its `resume` twin.
- [x] T4: Unknown stored skill. Move `mark` and `same` from `register.tsx:192-205` to `band.ts`, exported. The mark reads the step through `knownStep`. `ui.render`, `dismiss`, and `reconcile` call it. Add the direct test and show it red against a planted copy that skips the label check.
- [x] T5: Live look. Open a new desktop Code session, because the mod loads at session start. Press the close button on a showing band, run `/clear`, and see whether the band returns. Log what showed. If the band stays hidden, stop at the amendment gate before T6.
- [x] T6: Docs. Update the README close-button paragraph, the CHANGELOG Unreleased entry, the DESIGN.md `hooks/status/` bullet, and the `register.tsx` header comment. Run the AC5 sweep and read each hit in context. Run the four verify commands.
- [x] T7: (review return, R1) Amend AC2 through the gated amendment protocol. Its first sentence then says the failed read alone does not hide or show the band.
- [x] T8: (review return, R2 to R4, R8) Narrow the "a press made during a refresh is kept" sentences in `cairn/DESIGN.md` and the `reconcile` comment to the window the fix closes. Fix the `CairnBandHidden` comment in `types/index.d.ts` and the "a read that throws" wording in the `refresh` comment. Even the wraps in the CHANGELOG entry, the README paragraph, the DESIGN bullet, and the `band.test.tsx` header comment. Rerun the AC5 sweep and the four verify commands.
- [x] T9: (review return, R9) Add a null check at the nine `reader.test.ts` sites that use the `loadBand` result.
- [x] T10: (review return, R4 to R7) Search the candidates first, then add four items to a candidate row. The items are the stale rows after a working-directory throw, a session end lost to a press's two reads, a ROADMAP read mid-write, and the AC2 test gap.

## Work log

- 2026-10-02: created by /milestone-plan, promoting the "Band close-state edge cases" candidate row (the row stays until post-merge hygiene).
- 2026-10-02: plan probe in a scratch copy of the mod: a press made while a turn-end refresh's ROADMAP read was held stayed hidden on main with the file unchanged. So M199 review item B7 loses no press. The lost-press window is the awaits inside `reconcile`, after the read returns.
- 2026-10-02: criteria audit (full mode, fresh Opus reader): 7 findings, all fixed before the gate. AC1's held-read cases became guards that pass on main, and the code check became the evidence. AC2 became one press case that fails at the good read. AC3 gained the no-branch-on-reason check. AC4 gained the call-site check. AC5 was limited to the close-button paragraph, the Unreleased entry, and the DESIGN bullet. Its sweep gained `ROADMAP|cleared`, `reader.ts`, and `types/index.d.ts`. AC5 ties `/clear` sentences to the mod's behavior, not to the log.
- 2026-10-02: plan gate chose to clear the close state at every session end over keeping the band hidden across session ends. The reason: one rule then holds whether or not the app keeps state across `/clear`. Falsified by a user who expects a hidden band to stay hidden in a new session.
- 2026-10-02: plan gate chose to keep the last state only for a found but unreadable ROADMAP over also keeping it for a missing one. The reason: a missing ROADMAP also means a move out of a cairn repo. Falsified by a real session whose band flickers back during a git checkout.
- 2026-10-02: plan gate chose the decide-inside-`update` fix over storing the drawn state at the press. The reason: it closes the window in one function and keeps M194's press behavior. Falsified by a press observed lost in a real session after the fix.
- 2026-10-02: implement started on branch m200-band-close-state; no question gate, as the plan left nothing open.
- 2026-10-02: T1 done: `reconcile` decides inside its `update` callback; two held-read guard cases added, green on the branch and on main's `register.tsx`; verify 4/4 green (plugin test 605 pass).
- 2026-10-02: T2 done. `loadBand` returns null for a found ROADMAP it cannot read. On null or a throw, `refresh` keeps the rows and still compares the close state against them, so a step that ended at the same turn end still clears it. The two AC2 cases failed on the unfixed code (the press case at the good read) and pass now. A reader test covers the null. Verify 4/4 green (608 pass).
- 2026-10-02: T3 done. The `session.end` hook sets `dismissed` to null after it clears the step, with no branch on the reason. The four no-skill cases failed on the unfixed code with the band hidden. The running-skill case now runs for `clear` and `resume`. Verify 4/4 green (614 pass).
- 2026-10-02: T4 done. `mark` and `same` moved to `band.ts`, exported, and `mark` reads the step through `knownStep`. `ui.render`, `dismiss`, and `reconcile` call them. The direct test went red against a planted copy that skipped the label check, with the skill kept and no idle id. Verify 4/4 green (615 pass).
- 2026-10-02: T5 done. The operator did the live look in a new desktop Code session in this repo, on the branch. After a press, a `/clear` left no band. The app log shows why: the desktop `/clear` stops the session's process (`Stopping session`, then `CLI process group 7734: nothing left`), and a new one starts at the next message. At the first message after the `/clear`, the M200 row showed again. So no amendment is needed. The look cannot tell whether the `session.end` hook or a fresh process cleared the close state.
- 2026-10-02: T6 done. The README close-button paragraph, the CHANGELOG Unreleased entry, the DESIGN `hooks/status/` bullet, and the `register.tsx` header now state both rules. The `/clear` sentences say the band draws again at the next message, as T5 showed. Every AC5 sweep hit in those places and the five code files was read in context and states current behavior. Verify 4/4 green (615 pass). `cairn_validate` green.
- claim audit: 25 claims read, 3 corrected — CHANGELOG.md, README.md, hooks/status/register.tsx
- 2026-10-02: the three corrected claims said a failed read keeps the close state as it was. A step that ends at the same turn end can still clear it, so they now say the failed read alone does not hide or show the band. The same reader re-read all three as true.
- 2026-10-02: implement complete. Verify 4/4 green (615 pass), `cairn_validate` green. Status set to review.
- 2026-10-02: review started. AC1, AC3, AC4, and AC6 verified. AC2 and AC5 not verified. Gate green. Three reviewers reported 16 findings.
- amendment return: AC2 — "When `cairn/ROADMAP.md` is found but its read fails, a refresh keeps the band's rows, and the failed read alone does not hide or show the band."
- 2026-10-02: defect return 1 (review): AC5 failed. `cairn/DESIGN.md` and the `reconcile` comment say a press made during a refresh is kept. A second hook can change the step between the reads and the write in `reconcile`, and that breaks the claim. Status set to in-progress. Requested changes are T7 to T10.
- 2026-10-02: implement resumed on the branch. The base is still `origin/main` (7a2ffc6), so no merge.
- re-audit: AC2 (full) — one finding, bounded promise: the first sentence covers every refresh trigger, and the named cases cover a turn end only. The reader proposed a code check as the evidence for the first sentence. The other five questions returned nothing.
- 2026-10-02: T9 done. A `loaded` helper in `reader.test.ts` throws on a null `loadBand` result, and the nine sites call it. Verify 4/4 green (615 pass).
- 2026-10-02: T10 done. The candidate search found no overlap outside the "Status mod follow-ons" row, which now lists the four M200 review items.
- 2026-10-02: T8 done. `cairn/DESIGN.md` and the `reconcile` comment now say a press made while the refresh reads is kept, and that a hook changing the rows or step before the `update` can still clear a press. The `CairnBandHidden` comment says the skill is null for a skill with no label. The `refresh` comment names a `loadBand` throw. The DESIGN component line no longer says the close state holds through session ends. The AC2 describe title follows the amended clause. Wraps are even in the CHANGELOG entry, the README paragraph, the DESIGN bullet, and the `band.test.tsx` header. AC5 sweep read, verify 4/4 green (615 pass), `cairn_validate` green.
- 2026-10-02: the amendment gate chose the AC2 wording with the code check added as the evidence for the first sentence.
- re-audit: AC2 (full) — one finding, satisfiability: the code check never ties a failed read to the null that `refresh` tests. The reader proposed a parenthesis naming `readText`'s catch and `loadBand`'s null. The other five questions returned nothing. This is AC2's second re-audit line, so no further reader runs.
- 2026-10-02: T7 done. The operator chose to add the parenthesis, and AC2 now carries the amended first sentence and the code check.
- claim audit: 81 claims read, 3 corrected — hooks/status/register.tsx, types/index.d.ts
- 2026-10-02: the three corrected claims were misleading, not false. The `reconcile` comment now names `reconcile`'s own reads of `band` and `step`, the `refresh` comment names `$.session.cwd()` as the one uncaught call, and the `CairnBandHidden` comment names the running step's skill. The DESIGN sentence took the same `reconcile` wording. The same reader re-read all four as true.
- 2026-10-02: implement complete after the return. Verify 4/4 green (615 pass), `cairn_validate` green. Status set to review.

## Decisions

## Review

Sync: the branch base equals `origin/main` (7a2ffc6), so no merge was needed. Route (d), because no PR exists yet.

- AC1 evidence (2026-10-02): `reconcile` (`register.tsx:203-206`) computes `now`, then calls `update($, dismissed, hidden => …)`. The callback returns null only for a set `hidden` that differs from `now`. No await sits between the decision and the write. The two AC1 guard cases pass on the branch. They also pass in a scratch copy with main's `register.tsx` and `reader.ts`.
- AC2 evidence (2026-10-02): When `findRoot` finds the ROADMAP and the read gives null, `loadBand` returns null. `refresh` then keeps the `band` atom and still runs `reconcile`. In the test seam, `fs.stat` answers the path as a file and `fs.read` of an unreadable path falls to the rejecting bottom of the chain. On the branch both AC2 cases pass. With main's code, the press case fails at the third check, after the good read, with the row drawn. The no-press case fails with no row drawn. The `no-roadmap` cases pass on the branch.
- AC3 evidence (2026-10-02): the `session.end` hook (`register.tsx:100-106`) clears the step and then sets `dismissed` to null, with no read of `e.reason`. The four no-skill cases, for `clear` and `resume` on the terminal and desktop surfaces, pass on the branch. With main's code, all four fail with no row drawn. The four `milestone-plan` cases, for both reasons on both surfaces, pass on the branch.
- AC4 evidence (2026-10-02): `mark` and `same` are exported from `band.ts`, and `mark` reads the step through `knownStep`. `register.tsx` imports both, and `ui.render`, `dismiss`, and `reconcile` call them. The direct test passes on the branch. In a scratch copy with `const current = step` planted in `mark`, it fails: the mark holds the skill `milestone-gone` and no idle id, where `M021` was expected. The other 614 cases pass there.
- AC2 not verified (2026-10-02): the named cases hold, but the first sentence fails outside them. At a skill prompt, `skill.prompt` sets the step and then calls `refresh`. With a failed read, `reconcile` then clears a close state stored under another skill. So a refresh with a failed read does not always leave the close state as it was. T2's work-log line and the claim audit chose this behavior, and the docs state it. The criterion text did not follow. Box unticked.
- AC5 evidence (2026-10-02): the README close-button paragraph, the CHANGELOG Unreleased entry, and the DESIGN `hooks/status/` bullet each state both rules. Their `/clear` sentences say the band draws again at the next message, as T5 logged. The sweep returned 101 lines, each read in context. One problem remains. `cairn/DESIGN.md:97-99` and `register.tsx:200-202` say a press made during a refresh is kept. The Opus reviewer traced an order of events that breaks this, not run as a test. A second hook changes the step after `reconcile` reads it and before its write. A press against the new state is then cleared by the stale comparison. Box left unticked until the gate decides.
- AC6 evidence (2026-10-02): all four commands exit 0 on the branch head. `scripts/tests` ran 395 tests (21 skipped) and `hooks/tests` ran 174. `claude plugin validate` passed with warnings. `claude plugin test .` gave 615 pass, 0 fail. The binary is the app's 2.1.286 build.
- Consistency gate (2026-10-02): `cairn_validate` exits 0, all checks pass. No principle changed, so `cairn_impact` was skipped. The `generic` profile names no toolchain checks.

Findings (three fresh reviewers: Opus diff, Sonnet blame-history, Sonnet prior-review. The PR-comment probe found none.) Merged across lenses, most severe first, with the disposition proposed at the gate:

- R1 (Opus 2): AC2's text says a failed read leaves the close state as it was, but `reconcile` still runs and a step change clears it. Proposed: amendment return, the AC2 clause narrowed to "the failed read alone does not hide or show the band", as the docs say.
- R2 (Opus 1, prior-review 5): `reconcile` builds `now` from reads taken before its `update`, so a second hook that changes the step in between can clear a fresh press. `cairn/DESIGN.md` and the `reconcile` comment say a press made during a refresh is kept. Proposed: fix with the return, narrowing both sentences to the window the fix closes.
- R3 (Opus 10): the `CairnBandHidden` comment in `types/index.d.ts` still says the stored skill is the running skill's bare name. It is null for a skill with no label. Proposed: fix with the return.
- R4 (Opus 3, blame 2): a throw from `loadBand`, which can only come from the working-directory read, now keeps the last rows, possibly another repo's. The plan chose this for throws, but the `refresh` comment calls it "a read that throws". Proposed: fix the comment with the return, and add the stale-rows case to a candidate row.
- R5 (Opus 4): `dismiss` reads twice and then writes, so a session end between them can be overwritten by the press. Proposed: candidate row.
- R6 (Opus 6): a ROADMAP read mid-write parses to no rows and empties the band. Proposed: candidate row.
- R7 (Opus 7): no AC2 case edits the ROADMAP before the failed read, so the branch tests alone cannot tell kept rows from a fresh read. Only the red run on main shows the stub works. Proposed: candidate row.
- R8 (Opus 12, prior-review 1 and 2, blame 7): uneven wraps in the CHANGELOG entry, the README paragraph, the DESIGN bullet, and one long line in the `band.test.tsx` header comment. Proposed: fix with the return.
- R9 (Opus 11): nine `reader.test.ts` sites use the `loadBand` result with no null check. They run, but a strict type check rejects them. Proposed: fix with the return.
- R10 (Opus 8, prior-review 4, blame 5): a revert of the decide-inside-`update` fix turns no test red. Proposed: reject, because AC1 names the code check as its evidence by plan.
- R11 (Opus 14, prior-review 3, blame 1 and 8): the desktop `/clear` result is not tied to the hook, and "whatever its reason" rests on a code reading. Proposed: noted, because the docs scope `/clear` to what T5 saw and AC3 names the no-branch check.
- R12 (Opus 5): if `next(e)` rejects, the session end clears nothing. Proposed: reject, a pattern main already had.
- R13 (Opus 9): the AC4 test covers `mark` as a unit only. Proposed: reject, because AC4's call-site check covers the wiring.
- R14 (Opus 13): the plan-gate choices sit only in the work log, and the claim-audit line has no date. Proposed: reject, because milestone-local choices belong in the milestone file and the work log is append-only.
- R15 (blame 3, prior-review 6): a stat that succeeds and a read that fails differ from a missing file, and `dismiss` still reads in two steps. Proposed: reject, both chosen at the plan gate.
- R16 (blame 4 and 6): `session.end` no longer calls `reconcile`, and `mark` moved with its comments. Proposed: noted, no effect.

Gate (2026-10-02): the maintainer chose "Send back to implement". Every proposed disposition above stands as the final one. R1 is an amendment return. R2 is a defect return on AC5. R3, R4's comment, R8, and R9 are fixes for the return (T7 to T9). R4's stale-rows case, R5, R6, and R7 go to a candidate row (T10).

Re-review (2026-10-02), at f49db87. Sync: the branch base still equals `origin/main` (7a2ffc6), so no merge. Route (d), because no PR exists. Since the return, `register.tsx`, `band.ts`, and `reader.ts` changed only in comments, so the AC1, AC3, and AC4 evidence above stands, and their cases pass in the 615 below.

- AC2 evidence (2026-10-02, re-review): the amended criterion's code check holds. `refresh` (`register.tsx:222-233`) writes `band` only for a non-null state and then runs `reconcile`. `readText` catches the rejected read and gives null, and `loadBand` (`reader.ts:244-245`) returns null for a found ROADMAP. `reconcile` reads only `band` and `step` before its `update`. Both AC2 cases pass on the branch. In a scratch copy with main's `register.tsx` and `reader.ts`, the press case fails after the good read with the `implement M002` row drawn, and the no-press case fails with no row drawn. The `no-roadmap` cases pass on the branch.
- AC5 evidence (2026-10-02, re-review): the sweep returns 102 lines. In the README close-button paragraph, the CHANGELOG Unreleased entry, and the DESIGN `hooks/status/` bullet, each hit read in context states both rules and current behavior. The press sentences in DESIGN and the `reconcile` comment now name `reconcile`'s own reads and the hook that can still clear a press, and the claim audit's re-read found them true. The `/clear` sentences say the band draws again at the next message, as T5 logged. The hits in the five code files state current behavior.
- AC6 evidence (2026-10-02, re-review): all four commands exit 0 at f49db87. `scripts/tests` ran 395 tests (21 skipped), `hooks/tests` ran 174, `claude plugin validate` passed, and `claude plugin test .` gave 615 pass, 0 fail, on the app's 2.1.286 binary.
- Consistency gate (2026-10-02, re-review): `cairn_validate` exits 0, all checks pass. No principle changed, so `cairn_impact` was skipped. The `generic` profile names no toolchain checks.

Re-review findings (three fresh reviewers: Opus diff, Sonnet blame-history, Sonnet prior-review; the PR-comment probe found none), merged across lenses, most severe first, with the disposition proposed at the gate:

- S1 (Opus 2): `cairn/DESIGN.md:65` says "a close state that a refresh keeps", but `reconcile` clears it when the rows or the step change. The line is an AC5 sweep hit, so the AC5 evidence above missed it and AC5 fails as written. Proposed: fix now, "a close state that a failed ROADMAP read alone does not change and every session end clears in M200". By the return floor this is a defect return. The proposal is a logged override of the floor, fixing the line on the branch.
- S2 (Opus 1): a found ROADMAP that cannot be read also keeps the last rows, which can belong to another repo after a working-directory move. Proposed: follow-up, the T10 item in "Status mod follow-ons" widened to name both cases.
- S3 (Opus 3, prior-review 1 and 2): T8 left a short line at `cairn/DESIGN.md:106` and kept one at `CHANGELOG.md:41`. Other short lines in the CHANGELOG entry and the DESIGN bullet predate M200. T8's work-log line says the wraps are even. Proposed: fix those two seams now, reject the older lines, and log that T8's line overstated.
- S4 (Opus 4): the `refresh` comment says the close state is compared against the kept rows, and leaves out the current step. Proposed: fix now.
- S5 (Opus 5): the `refresh` comment names `$.session.cwd()` as the throw, but a parse error inside `loadBand` also keeps the rows. Proposed: fix now.
- S6 (blame 1): `reconcile` now calls `update` at every refresh, and the mod API says `update` always writes. Main skipped the write when nothing was hidden. Whether a write of the same value redraws is not documented. Proposed: follow-up, an item in "Status mod follow-ons".
- S7 (blame 2): `loadBand` now gives null for an unreadable ROADMAP, where the Python reader reads it as empty, and no comment says so. Proposed: fix now, one sentence in the `loadBand` comment.
- S8 (Opus 6): the AC1 guard test leaves a held read pending when `untilHeld` gives up. Proposed: reject, because the failing expect rejects the test, and nothing awaits the pending turn end.
- S9 (Opus 7): the `dismissed` atom comment says null while the band shows, which is not always true. Proposed: reject, the comment predates M200.
- S10 (blame 3): `session.end` no longer calls `reconcile`. Proposed: noted, as R16, the plan's one-rule choice.
- S11 (blame 4): the session-end claim rests on T5 and tests. Proposed: noted, as R11.
- S12 (blame 5): the "Band close-state edge cases" row still describes the pre-M200 state, and its B7 item was disproved by the plan probe. Proposed: noted, the row is pruned at post-merge hygiene and B7 is not carried over.
