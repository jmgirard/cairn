<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M199: A band that names the next milestone

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m199-band-idle-line

## Goal

Name the next workable milestone in the band between milestones, after the last cairn skill ends.

## Scope

**In:** An idle row in the band. When no milestone is `in-progress` or `review` and no cairn skill runs, it shows.
It names the next workable `planned` milestone, by the same rule as `scripts/cairn_next.py`.
A reader in `hooks/status/reader.ts` that computes the ordered workable list.
A helper in `cairn_next.py` that the parity test calls, so the test reads the script's own logic.
The end of a cairn skill's step at the end of its turn.
The close button's mark gains the idle row's id.
README.md, CHANGELOG.md, `cairn/DESIGN.md`, and `types/index.d.ts` describe the new behavior.

**Out:** A line that suggests `/milestone-plan` when no milestone is workable. The gate chose an empty band, so this work is dropped.
A clickable next command stays in the "Status mod follow-ons" row.
The label colors in other themes stay in the "Band label colors in other themes" row.
The lost-press and read-then-clear cases stay in the "Band close-state edge cases" row.
A skill that a plain reply resumes in a new turn shows no skill label. This limit is accepted at the gate, and no row holds it.

## Acceptance criteria

- [x] AC1: If no ROADMAP row is `in-progress` or `review` and no cairn skill runs, the band draws one idle row. The row names the first milestone in the workable list. With an empty list, the band draws nothing. The workable list holds each `planned` row whose `Depends on` ids are all done. A done id is a `done` row, or the id of an `M<digits>…md` file directly under `cairn/milestones/archive/`. Ids compare at three-digit padding, so `M57` equals `M057` and `M0057`. The list is ordered high, normal, low, with the cell case-folded and an unknown value read as normal. Ties go by id number, with a non-numeric id last. The idle row draws `next`, the bold id, and the title on the left, all in the theme's gray. It draws `/milestone-implement <id>` on the right. If the title gets less than the room it needs, the row leaves the command out. For a title under 10 columns, the room is the title's width. For any other title, the room is 10 columns. Shown by `claude plugin test` cases on the terminal and desktop surfaces at the default width and at 36 columns.
- [x] AC2: For each fixture directory under `hooks/status/fixtures/`, the TypeScript reader's ordered workable list equals the list that `cairn_next.py` computes for that tree. The reader computes the list whether or not a row is active. The fixtures cover these cases. A priority order that differs from id order, `High` in mixed case, an unknown priority, and M999 before M1000. A dependency met by a `done` row, met only by an archive file, and met at another padding. A dependency on a `planned` milestone, and on an id with no row and no file. The Depends-on forms `M001, M002` with one met, `M001 M002`, `—`, and a malformed `m001` token. A blocked row that ranks above every workable row. A tree with no planned row. Shown by each fixture's `expected.json`. The `claude plugin test` cases hold the reader to it. `scripts/tests/test_status_fixtures.py` holds the helper in `cairn_next.py` to it.
- [x] AC3: A cairn skill's step ends at the first main-loop `turn.complete` with reason `answer` after the skill's prompt was expanded. The band then draws the active milestone's row with its phase label, the idle row, or nothing. A chapter marked after that point sets no chapter. A main-loop turn that ends `aborted`, `refusal`, or `error` leaves the step as it was. A subagent's turn end also leaves it. Shown by `claude plugin test` cases for each of those endings and for a chapter marked after the step ended.
- [x] AC4: A press of the close button stores the drawn idle row's id. With no idle row drawn, it stores null. If the idle row to draw changes, the hidden band shows again. If a row becomes `in-progress` or `review`, a cairn skill starts, or a skill's step ends, it also shows again. A checked box, an edited title, or a new planned row during an active milestone leaves it hidden. Shown by `claude plugin test` cases for each of those changes.
- [x] AC5: Three docs describe the idle row, its command, and the step's end at its turn's end. They are README.md, the Unreleased section of CHANGELOG.md, and the `hooks/status/` paragraph of `cairn/DESIGN.md`. The sweep is `git grep -niE 'draws nothing|stay until|until a cairn skill starts|session ends|can end|run again|until that list|until the active|shows again|while a cairn skill runs'`. It runs over README.md, `cairn/DESIGN.md`, CHANGELOG.md, `hooks/status/`, and `types/index.d.ts`. Each line that it returns states the new behavior or a behavior that this milestone leaves unchanged. CHANGELOG lines under released versions are exempt.
- [x] AC6: A live look in a new desktop Code session shows three things. The session runs in a scratch cairn repo with a workable `planned` milestone and no active one. The band draws the idle row. After `/milestone` ends its turn, its skill row gives way to the idle row. During a `/milestone-plan` question chip, the plan skill row stays.
- [x] AC7: The verify slot of `cairn/PROFILE.md` runs clean: `python3 -m unittest` over `scripts/tests` and `hooks/tests`, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T2
- AC3 → T4
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Move the done-set and workable logic of `cairn_next.py` into one helper that `render()` and the test both call. Add the AC2 fixtures, in a few trees that each carry several cases. Add the ordered workable list to every `expected.json`. Carry it through `gen_fixtures.py` and the `Fixture` type. Hold it to the helper in `test_status_fixtures.py`.
- [x] T2: In `reader.ts`, parse the depends and priority cells and canonicalize ids. Add a `list` call to `FileSource` and to `memorySource`, and list `cairn/milestones/archive/`. Compute the workable list. Bump the `band` shape tag. Add `reader.test.ts` cases first and see them fail.
- [x] T3: In `band.ts`, add the idle row, its two forms, and its place in the row choice after the skill row. Add `band.test.tsx` cases first, on both surfaces at both widths.
- [x] T4: In `register.tsx`, end the step at a main-loop `turn.complete` with reason `answer`. Add the drawn idle id to the close mark under a new `dismissed` shape tag. Update `types/index.d.ts`. Add the AC3 and AC4 cases first.
- [x] T5: Update README.md, CHANGELOG.md, and `cairn/DESIGN.md`. Run the AC5 sweep and read each line it returns.
- [x] T6: Do the AC6 live look in a new desktop Code session, because a running session keeps the mod it loaded at its start. If a question chip ends the turn, stop and amend through the gate.
- [x] T7: Run the verify slot from the repo root and check each exit code.

## Work log

- 2026-10-02: created by /milestone-plan. Promotes the candidate row "Band idle line" at the operator's choice, before its real-session trigger fired. The row is pruned at post-merge hygiene.
- 2026-10-02: criteria audit (full mode, fresh Opus reader) returned 14 findings. Fixed before the gate: the fixture list miscounted its cases, and ids were not canonicalized. The archive-file form, the priority case and tie order, the Depends-on cell forms, and a done-row dependency were unstated or unprobed. A reader that ignores dependencies passed the drafted blocked fixtures. Parity read a copy of the logic. The reader's list was undefined while a row is active. The close mark's id was undefined, the docs sweep missed four stale phrasings and a file, and the live look named no skill. Posed at the gate: whether a question chip ends the turn, and whether a step's end brings a closed band back.
- 2026-10-02: plan gate chose to end a skill's step at its turn's end over a finished-skill look kept until the next skill. A finished look keeps the idle row from showing after any skill in the session. Falsified by a live session where a cairn skill's work runs on across turns and the band drops its label mid-skill.
- 2026-10-02: plan gate chose an empty band when no milestone is workable over a line that suggests `/milestone-plan`. With the suggestion, the band draws in nearly every session. Falsified by a session between milestones that misses the plan step because the band was empty.
- 2026-10-02: plan chose a TypeScript reader with shared fixtures over running `cairn_next.py` through `$.process.run`. M191 rejected python3 at every turn end, and a test cannot fake the process call. Falsified by a parity failure that the fixtures did not catch in a real repo.
- 2026-10-02: implement started on branch `m199-band-idle-line`. No question gate: the plan left no choice open for the operator.
- 2026-10-02: T1 done. `cairn_next.py` gains `done_ids` and `workable`, and `render()` calls `done_ids`. Two new fixtures, `idle-order` and `idle-deps`, have hand-written workable lists, and `cairn_next.workable` matches both. All 17 `expected.json` files carry `workable`. `idle-*` joins the band test's no-row list until T3. Verify: scripts, hooks, validate, and 536 plugin tests green.
- 2026-10-02: T2 done. `loadBand` returns `{ rows, workable }`, and `FileSource` gains `list`. A `band-3` atom holds the new shape, and `types/index.d.ts` gains `CairnBandState`. The band test answers `fs.list`. The new reader tests failed to load before the code existed. Verify: 561 plugin tests and the other three checks green.
- 2026-10-02: plants in `reader.ts`, each restored after its run. Ignoring dependencies reddened 6 tests, skipping the archive id's padding 2, and a text sort of ids 1. Keeping the priority's case reddened nothing, because the `High` row had the lowest id. That row moved from M020 to M500, and the plant then reddened `idle-order`.
- 2026-10-02: T3 done. `idleLines` and the idle branch of `stepLines` landed before their tests, a deviation from tests-first. Plants each reddened tests: a command never dropped 5, an orange label 4, and the last workable row named 6. Tests that expected an empty band on a fixture with a workable row now expect the idle row. 575 plugin tests green.
- 2026-10-02: T4 done. A main-loop `turn.complete` with reason `answer` clears the step. The close mark gains `idle` under `dismissed-3`. One M195 test ended a turn mid-skill to reread a file, and now rereads at a chapter. Plants each reddened tests: any reason ends the step 3, no reason ends it 5, a subagent ends it 1, and the idle id left out of the comparison 3. 595 plugin tests green.
- 2026-10-02: T5 done. README gains the idle row paragraph, its example, the step's end, and three close-button conditions. The CHANGELOG band entry and the DESIGN.md `hooks/status/` paragraph say the same. The AC5 sweep returned 21 lines. One test comment named only the active list and now names all three marks. The claim that a question chip keeps the step waits for T6, so the `register.tsx` comment no longer states it. Verify green, validate green.
- 2026-10-02: T6 paused at the operator's choice before the live look. The scratch repo is at `scratchpad/idle-look` in this session's scratch directory, with M002 workable and M003 waiting on M002. On resume, recreate it if it is gone, then do the look.
- 2026-10-02: T6 done. The operator did the live look in a copy at `~/Desktop/cairn-idle-look`, because Finder hides `/private/tmp`. After `/milestone` ended its turn, its skill row (`status /milestone → Route`) gave way to `next M002`. During the `/milestone-plan` question chip, the plan row stayed (`→ Question gate`), so a chip keeps the step. That claim went into README and the `register.tsx` comment. The idle row drew only after the first message, not at session open. A new test shows `session.start` draws it in the harness. In this repo the M199 row drew at open. In the Desktop copy, M002 set to in-progress drew no row before the first message either. So the gap belongs to that folder or to how the app starts a session, not to the idle row. It joins the "Status mod follow-ons" row.
- 2026-10-02: correction to the line above. The operator's screenshot shows the app's "New" page with no session running: the session starts at the first message. So no band can draw before it, and the note was taken back out of the "Status mod follow-ons" row. The cairn-repo look that drew the M199 row at once was not re-checked.
- 2026-10-02: T7 done. Verify green: scripts 395, hooks 174, plugin validate, and 596 plugin tests. Validate green, and ROADMAP is 18,953 bytes.
- claim audit: 58 claims read, 2 corrected — hooks/status/reader.ts (the header named `parse_depends` as a helper that `workable` calls, and the mirror comments left out that it reads ASCII digits only, where Python also takes other Unicode digits). The same reader re-read the three corrected comments and found them correct.

## Decisions

## Review

Review run 2026-10-02 on `m199-band-idle-line` at 970c904, which contains `origin/main` (no sync needed). Claude Code 2.1.286, from the app's binary path.

- AC1: `claude plugin test .` exit 0, 596 pass. The block "the idle row names the next workable milestone (M199 AC1)" passes on both surfaces, because `mountEach` loops over `SURFACES`. At 120 columns, each of the four fixtures that draw an idle row matches a hand-written row with its command. At 36 columns, each row leaves the command out. The 10-column rule passes at its edges. The title `Go` keeps the command at 42 columns and drops it at 41. A 29-column title keeps it at 50 and drops it at 49. An active row wins over a workable row, and a running skill wins over the idle row. The session start draws the idle row. The colors test asserts the gray label, the bold id, and the gray text. The block "the band draws nothing" passes for `no-roadmap`, and for `no-active` and `idle-deps` with nothing workable. The block "the workable list (M199 AC1)" covers the Depends-on forms, padding, priority words, and blocked dependencies.
- AC2: All 17 fixtures under `hooks/status/fixtures/` carry a `workable` list. The block "reader over every fixture (M193 AC5, M199 AC2)" passes "the workable list matches expected.json" for each of the 17. It also passes "the workable list is computed while a row is active". `python3 -m unittest scripts.tests.test_status_fixtures -v` runs 4 tests, all OK. `python_workable` calls `cairn_next.workable` itself, and a separate test checks that the idle fixtures discriminate. Read by hand: `idle-order` holds `High` on M500 above lower ids, `someday` read as normal, M999 before M1000, and `Mfoo` last. `idle-deps` holds a done-row dependency (M041) and an archive-only one at another padding (`M57` against `M0057-pruned.md`). It holds a planned dependency (M050) and an unknown id (M051). It holds `M001, M002` with one met (M052), the space form, the dash, and `m077`. The blocked rows M050 to M052 are `high`, above every workable row. Trees with no planned row are among the other fixtures.
- AC3: The block "a cairn skill's step ends at its main-loop turn end (M199 AC3)" passes all 7 tests. At a main-loop turn end with reason `answer`, a milestone row goes back to its phase label, and a later chapter sets nothing. A skill row gives way to the idle row. With no workable milestone, it gives way to nothing. Turn ends with reason `aborted`, `refusal`, or `error` each keep the step, and so does a subagent's turn end.
- AC4: The block "a press stores the idle row's id (M199 AC4)" passes all 13 tests on both surfaces. After a press on the idle row, a checked box and an edited title keep the band hidden. A new next workable milestone shows it, and the band then names M022. A row that becomes `in-progress`, a cairn skill that starts, and a skill's step that ends each show it again. The M194 case "an added planned row keeps it hidden" passes on both surfaces under the new mark. That case covers a new planned row during an active milestone. If no row is active and no skill runs, the `mark` function in `register.tsx` stores the idle id. Otherwise it stores null.
- AC5: The sweep, run over the five named paths, returned 21 lines. Each one read in context states the new behavior or a behavior this milestone leaves unchanged. In CHANGELOG.md, lines 23 to 25, 40, and 62 sit under Unreleased and state the new close, step-end, and empty-band behavior. In README.md, line 167 states the step's end at the answer turn. Line 189 states the empty band, and lines 197 to 202 state the three close-button conditions. In `cairn/DESIGN.md`, line 96 states the unchanged skill hook, and line 121 the empty band. In `hooks/status/`, the `band.test.tsx` comments and test names, the `band.ts` row-choice comment, and the `register.tsx` comments state current behavior. `types/index.d.ts` returned no line.
- AC6: Review did not repeat the live look, because it needs the operator in a new desktop session. The evidence is the operator's look on 2026-10-02 at T6, in the scratch repo `~/Desktop/cairn-idle-look` with M002 workable and none active. The band drew `next M002`. After `/milestone` ended its turn, its skill row gave way to the idle row. During the `/milestone-plan` question chip, the plan row stayed. Since 3cdd2c4, the commit before that look, `git diff` shows no change to `band.ts`, `reader.ts`, or `register.tsx` outside comments. So the look holds for the code under review.
- AC7: From the repo root, each exit code read. `scripts/tests` exit 0, 395 tests OK with 21 skipped. `hooks/tests` exit 0, 174 tests OK. `claude plugin validate .claude-plugin/plugin.json` exit 0, passed with warnings. `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0, 596 pass and 0 fail.
- Consistency gate: `cairn_validate.py` exit 0, every check PASS or OK, coverage complete included. The milestone touches no principle, so `cairn_impact` does not run. The `generic` profile's consistency-gate slot names no toolchain check.

### Independent review findings

Three fresh reviewers ran: diff-bug (Opus, D), blame-history (Sonnet, B), and prior-review (Sonnet, P). The PR-comment probe returned no comments. Each finding is listed most severe first within its lens, with the proposed disposition.

- D1: The step ends mid-skill whenever a skill waits on background work. A background subagent or command ends the main-loop turn with reason `answer`, and the completion notice starts a new turn with no `skill.prompt`. So during `/milestone-review`'s reviewer fan-out, the skill label and later chapters are gone. With both an `in-progress` and a `review` row, the band switches to the `in-progress` row mid-review. This is the falsifier the plan gate recorded for its choice. AC3 as written holds. Proposed: follow-up, with a README note naming the limit now. B1 reports the same change from M195's side.
- D2: The done-row ids in `workableRows` can lose `canonId`, and no test fails. The reviewer planted it and saw 596 pass. Proposed: fix now with a reader test.
- D3: `archivedIds` can drop its `.md` check, and no test fails. The reviewer planted it and saw 596 pass. Proposed: fix now with a reader test.
- D4: Non-ASCII digits in ids and Depends-on cells make the TypeScript list differ from Python's. A scratch run showed the band naming a row Python holds back. The `reader.ts` header states the gap. Proposed: reject, because no real ROADMAP spells ids that way. P2 reports the same gap.
- D5: After a reload, the stored skill can be one that the label map no longer knows. Then the press mark and the render mark differ, and the close button cannot hide the idle row. The skill half predates M199. Proposed: follow-up in the "Band close-state edge cases" row.
- D6: The AC4 case "a checked box keeps it hidden" checks a box in a `planned` file. The reader never reads that file, so the case cannot fail through the idle mark. No fixture tests an empty band from dependency blocks alone. Proposed: reject, because the case states what AC4 names and the M194 cases cover a checked box during an active milestone.
- D7: `render()` in `cairn_next.py` calls `_workable` and `done_ids`, not the `workable()` that the parity test calls, and a local name shadows `workable`. Proposed: fix now.
- D8: README line 168 says a question waits inside the turn, which holds only for a question chip. README line 74 still says the band shows one row for the milestone in flight. The `band.test.tsx` describe title at line 994 names only the active list. The `reader.ts` header names helpers loosely. Proposed: fix the README lines and the header now, and note the describe title.
- B2: One M195 test now rereads at a chapter instead of a turn end, because a turn end now ends the step. Its intent survives. Proposed: noted.
- B3: The "Band close-state edge cases" ROADMAP row says a session end shows the band again after a press during a skill. That stays true, and the band now also shows at the skill's turn end. Proposed: reject, the row is not false.
- B4: The fixtures `no-active` and `repo-at-cut` now draw an idle row, so the "draws nothing" tests run on a copy with planned rows set to blocked. Proposed: noted.
- B5: The idle row is not in M197's width sweep from 36 to 120 columns. Proposed: fix now by adding it.
- B6: A failed archive listing makes archive-only dependencies read as not done. The band then skips a milestone but never names a held-back one. Proposed: reject, it fails soft like the rest of the reader.
- B7: The step clear and the refresh are two awaits, so a press between them is stored against the old state. This is the same class as the open lost-press case. Proposed: follow-up in the "Band close-state edge cases" row.
- B8: Checked and consistent, no action.
- P1: Ragged wraps in the edited prose, which M193, M195, M196, and M198 each fixed at their gates. Four added lines exceed 80 columns in README.md, `cairn/DESIGN.md`, and `gen_fixtures.py`, and CHANGELOG.md and DESIGN.md have short orphan lines. Proposed: fix now by reflowing.
- P2: Same as D4.
