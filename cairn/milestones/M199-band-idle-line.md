<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M199: A band that names the next milestone

- **Status:** in-progress
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

- [ ] AC1: If no ROADMAP row is `in-progress` or `review` and no cairn skill runs, the band draws one idle row. The row names the first milestone in the workable list. With an empty list, the band draws nothing. The workable list holds each `planned` row whose `Depends on` ids are all done. A done id is a `done` row, or the id of an `M<digits>…md` file directly under `cairn/milestones/archive/`. Ids compare at three-digit padding, so `M57` equals `M057` and `M0057`. The list is ordered high, normal, low, with the cell case-folded and an unknown value read as normal. Ties go by id number, with a non-numeric id last. The idle row draws `next`, the bold id, and the title on the left, all in the theme's gray. It draws `/milestone-implement <id>` on the right. If the title gets less than the room it needs, the row leaves the command out. For a title under 10 columns, the room is the title's width. For any other title, the room is 10 columns. Shown by `claude plugin test` cases on the terminal and desktop surfaces at the default width and at 36 columns.
- [ ] AC2: For each fixture directory under `hooks/status/fixtures/`, the TypeScript reader's ordered workable list equals the list that `cairn_next.py` computes for that tree. The reader computes the list whether or not a row is active. The fixtures cover these cases. A priority order that differs from id order, `High` in mixed case, an unknown priority, and M999 before M1000. A dependency met by a `done` row, met only by an archive file, and met at another padding. A dependency on a `planned` milestone, and on an id with no row and no file. The Depends-on forms `M001, M002` with one met, `M001 M002`, `—`, and a malformed `m001` token. A blocked row that ranks above every workable row. A tree with no planned row. Shown by each fixture's `expected.json`. The `claude plugin test` cases hold the reader to it. `scripts/tests/test_status_fixtures.py` holds the helper in `cairn_next.py` to it.
- [ ] AC3: A cairn skill's step ends at the first main-loop `turn.complete` with reason `answer` after the skill's prompt was expanded. The band then draws the active milestone's row with its phase label, the idle row, or nothing. A chapter marked after that point sets no chapter. A main-loop turn that ends `aborted`, `refusal`, or `error` leaves the step as it was. A subagent's turn end also leaves it. Shown by `claude plugin test` cases for each of those endings and for a chapter marked after the step ended.
- [ ] AC4: A press of the close button stores the drawn idle row's id. With no idle row drawn, it stores null. If the idle row to draw changes, the hidden band shows again. If a row becomes `in-progress` or `review`, a cairn skill starts, or a skill's step ends, it also shows again. A checked box, an edited title, or a new planned row during an active milestone leaves it hidden. Shown by `claude plugin test` cases for each of those changes.
- [ ] AC5: Three docs describe the idle row, its command, and the step's end at its turn's end. They are README.md, the Unreleased section of CHANGELOG.md, and the `hooks/status/` paragraph of `cairn/DESIGN.md`. The sweep is `git grep -niE 'draws nothing|stay until|until a cairn skill starts|session ends|can end|run again|until that list|until the active|shows again|while a cairn skill runs'`. It runs over README.md, `cairn/DESIGN.md`, CHANGELOG.md, `hooks/status/`, and `types/index.d.ts`. Each line that it returns states the new behavior or a behavior that this milestone leaves unchanged. CHANGELOG lines under released versions are exempt.
- [ ] AC6: A live look in a new desktop Code session shows three things. The session runs in a scratch cairn repo with a workable `planned` milestone and no active one. The band draws the idle row. After `/milestone` ends its turn, its skill row gives way to the idle row. During a `/milestone-plan` question chip, the plan skill row stays.
- [ ] AC7: The verify slot of `cairn/PROFILE.md` runs clean: `python3 -m unittest` over `scripts/tests` and `hooks/tests`, `claude plugin validate`, and `claude plugin test`.

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
- [ ] T3: In `band.ts`, add the idle row, its two forms, and its place in the row choice after the skill row. Add `band.test.tsx` cases first, on both surfaces at both widths.
- [ ] T4: In `register.tsx`, end the step at a main-loop `turn.complete` with reason `answer`. Add the drawn idle id to the close mark under a new `dismissed` shape tag. Update `types/index.d.ts`. Add the AC3 and AC4 cases first.
- [ ] T5: Update README.md, CHANGELOG.md, and `cairn/DESIGN.md`. Run the AC5 sweep and read each line it returns.
- [ ] T6: Do the AC6 live look in a new desktop Code session, because a running session keeps the mod it loaded at its start. If a question chip ends the turn, stop and amend through the gate.
- [ ] T7: Run the verify slot from the repo root and check each exit code.

## Work log

- 2026-10-02: created by /milestone-plan. Promotes the candidate row "Band idle line" at the operator's choice, before its real-session trigger fired. The row is pruned at post-merge hygiene.
- 2026-10-02: criteria audit (full mode, fresh Opus reader) returned 14 findings. Fixed before the gate: the fixture list miscounted its cases, and ids were not canonicalized. The archive-file form, the priority case and tie order, the Depends-on cell forms, and a done-row dependency were unstated or unprobed. A reader that ignores dependencies passed the drafted blocked fixtures. Parity read a copy of the logic. The reader's list was undefined while a row is active. The close mark's id was undefined, the docs sweep missed four stale phrasings and a file, and the live look named no skill. Posed at the gate: whether a question chip ends the turn, and whether a step's end brings a closed band back.
- 2026-10-02: plan gate chose to end a skill's step at its turn's end over a finished-skill look kept until the next skill. A finished look keeps the idle row from showing after any skill in the session. Falsified by a live session where a cairn skill's work runs on across turns and the band drops its label mid-skill.
- 2026-10-02: plan gate chose an empty band when no milestone is workable over a line that suggests `/milestone-plan`. With the suggestion, the band draws in nearly every session. Falsified by a session between milestones that misses the plan step because the band was empty.
- 2026-10-02: plan chose a TypeScript reader with shared fixtures over running `cairn_next.py` through `$.process.run`. M191 rejected python3 at every turn end, and a test cannot fake the process call. Falsified by a parity failure that the fixtures did not catch in a real repo.
- 2026-10-02: implement started on branch `m199-band-idle-line`. No question gate: the plan left no choice open for the operator.
- 2026-10-02: T1 done. `cairn_next.py` gains `done_ids` and `workable`, and `render()` calls `done_ids`. Two new fixtures, `idle-order` and `idle-deps`, have hand-written workable lists, and `cairn_next.workable` matches both. All 17 `expected.json` files carry `workable`. `idle-*` joins the band test's no-row list until T3. Verify: scripts, hooks, validate, and 536 plugin tests green.
- 2026-10-02: T2 done. `loadBand` returns `{ rows, workable }`, and `FileSource` gains `list`. A `band-3` atom holds the new shape, and `types/index.d.ts` gains `CairnBandState`. The band test answers `fs.list`. The new reader tests failed to load before the code existed. Verify: 561 plugin tests and the other three checks green.

## Decisions

## Review
