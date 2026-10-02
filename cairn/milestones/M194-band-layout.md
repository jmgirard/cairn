# M194: A right-aligned milestone band with a close button

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — every adopter's session draws the band
- **Branch/PR:** m194-band-layout

## Goal

Lay out the milestone band with its bar and counts at the right edge, and give it a close button that hides it until the active milestones or their phases change.

## Scope

**In:**
- Each header row in `hooks/status/` becomes two groups. The left group holds the phase, the id, and the title. The right group holds the bar, the counts or the state label, and on the first row the close button. The engine cuts the title by screen width, so `fit()` in `band.ts` is removed. This absorbs two items of the "Band layout edge cases" candidate row: the UTF-16 title cut and the split surrogate pair. Post-merge hygiene narrows the row only if T7's live look records a wide-character title cut with no split character.
- A close `Button` with `role: 'dismiss'`. A desktop draws its native close control at the band's trailing edge, and the terminal draws `×`. A press stores the ordered list of active ids and statuses in a new session state value, declared in `types/index.d.ts`. The band stays hidden while the current list equals the stored one. A new session starts with the band shown.
- The item row's positional label (`T3:`, `AC2:`) draws bold, and the rest of the row stays dim.
- README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.

**Out:**
- The other "Band layout edge cases" items (under 30 columns, the desktop `░` width, more than five milestones) → that candidate row.
- A rounded border around the band → not planned. The gate did not select it.
- A command that brings the band back → not planned. The band comes back when the list changes or in a new session.
- A roadmap pane, clickable next-command actions, `vscode` and `mobile` tests, and the Windows UNC walk → the "Status mod follow-ons" candidate row.
- A dim idle line between milestones → the "Band idle line" candidate row.

## Acceptance criteria

- [ ] AC1: Each header row draws as a `Box` with `justifyContent: 'space-between'` whose children are two `Box` groups. The left group carries `flexShrink: 1` and holds the phase label, the id, and the title. The title's `Text` holds the whole ROADMAP title with `wrap="truncate-end"`, inside a `Box` with `flexShrink: 1`. The right group carries `flexShrink: 0` and `marginLeft: 2`. It holds the bar (at `bodyColumns` 60 or more) and the counts, or the state label that M193's AC2 names. On the first row it also holds AC2's close button. Shown by `claude plugin test` cases on the terminal and desktop surfaces that read the drawn elements' props from `findAll`. The cases mount `mixed` at `bodyColumns` 59, 60, and 120. At `bodyColumns` 40 they also mount two more fixtures. One has a title longer than 120 characters. The other has a title with wide characters and an emoji outside the Basic Multilingual Plane.
- [ ] AC2: When the band draws rows, its tree holds exactly one `Button`. It is keyed `cairn-close` and is the last child of the first header row's right group. It has `role: 'dismiss'` and `plain`. Its label is `×` on the terminal and `Close milestone band` on the desktop. A press makes the next drawing of the band pass to `next(e)`. That drawing holds no cairn row. It holds what the hooks beneath draw: the engine's own slot, or in its place the row a plugin beneath draws. Shown by `claude plugin test` cases on both surfaces over `mixed` and `single-in-progress`, and over `mixed` with a plugin beneath that draws its own row.
- [ ] AC3: After a press, the band stays hidden at each turn end whose refreshed active rows have the same ids and statuses, in the same ROADMAP order, as at the press. It shows again at the first turn end where that ordered list differs. It then stays shown until the next press. A list that returns to its press-time value does not hide it again. Shown by edit cases on both surfaces in `hooks/status/band.test.tsx`. A checked task box, an added `planned` row, and an edited title each keep the band hidden. Four edits each show it again: a row moved from `in-progress` to `review`, an added active row, a removed active row, and two active rows that swap ROADMAP order. A row moved to `review` shows the band. A move back to `in-progress` keeps it shown.
- [ ] AC4: When the item row's text after its arrow matches `^(T|AC)\d+[a-z]*:`, the matched label's `Text` carries `bold`, and neither it nor any `Text` that encloses it carries `dimColor`. Every other `Text` of the item row carries `dimColor`. An item text with no such label has `dimColor` on every `Text`. Shown by `claude plugin test` cases on both surfaces over `mixed` (`AC3:`), `single-in-progress` (`T2:`), `nested-first` (`T1a:`), and a fixture whose first unchecked task has no positional label.
- [ ] AC5: The band keeps M193's rows, texts, colors, ROADMAP order, survey yield, and stacking above `next(e)`, except where AC1, AC2, and AC4 change them. Shown by M193's cases in `hooks/status/band.test.tsx`, restated where AC1, AC2, or AC4 changed the tree, and passing on the surfaces each ran on.
- [ ] AC6: The verify slot in `cairn/PROFILE.md` runs clean. It holds both Python suites, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T3, T4
- AC2 → T2, T3, T4
- AC3 → T2, T3, T5
- AC4 → T1, T3, T4
- AC5 → T4
- AC6 → T4, T5, T6

## Tasks

- [x] T1: Layout in `band.ts`. Build each header row as a left and a right group, remove `fit()`, and split the item row's positional label from the rest. Add fixtures for a long title, a wide-character title, and an unlabeled first task, then regenerate `fixtures.gen.ts`.
- [x] T2: Close state. Add a `dismissed` session atom that holds the ordered id and status list, and declare it in `types/index.d.ts`. The press handler reads the `band` atom inside the handler, not from a value captured at draw time. If the new list differs from `dismissed`, the refresh clears it.
- [x] T3: Render in `register.tsx`. Draw the two groups, the close button with its per-surface label, and the bold label. Pass to `next(e)` while `dismissed` equals the current list.
- [x] T4: Tests. Restate M193's cases where the tree changed. Add the AC1, AC2, and AC4 cases on both surfaces, red first.
- [x] T5: Edit cases for AC3 on both surfaces.
- [x] T6: Docs. Update README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.
- [ ] T7: Look at the band live in the desktop app at a normal and a narrow width, in both phases, with a wide-character title, and press the close button. Record what it showed in the work log.

## Work log

- 2026-10-01: created by /milestone-plan, from the operator's request to add right alignment, a close button, and other polish to the band.
- 2026-10-01: criteria audit, full mode, one fresh Opus reader, 16 findings. Ten had one clear fix and were fixed before the gate. AC1 lost a paint claim and gained the group shrink and gap. AC2 says "exactly one Button" and has a desktop accessible name. AC3 gained a change-back case, an order case, and keep-hidden cases. AC4's label pattern and fixtures were fixed, and AC5 lists every changed case. Four went to the gate. Two were settled in the plan: a new session starts shown (Scope), and T7 stays a task.
- 2026-10-01: the gate changed AC1 (a wide-character title fixture) and reworded AC3. The same reader was asked to re-audit them; its result is logged in a later line.
- 2026-10-01: re-audit of the gate-changed wording, same reader, 3 findings. Fixed: AC2 now says what the hooks beneath draw, since a plugin beneath may replace the engine's slot. AC4 now binds the label's and its parents' `dimColor` props, not how the label looks. The row narrowing in Scope now waits on T7's live look.
- 2026-10-01: plan gate chose to hide the band until the ordered list of active ids and statuses changes, over hiding it for the session and over shrinking it to header rows. A phase change is then never missed. Falsified by sessions where the band comes back too often to be useful.
- 2026-10-01: plan gate chose the desktop's native close control (`role: 'dismiss'`) over a plain `×` on both surfaces. The native control matches the app, though it hides only cairn's rows when another plugin draws in the band. Falsified by a desktop drawing that puts the control where it reads as closing another plugin's rows.
- 2026-10-01: plan chose flex groups with the engine cutting the title over keeping `fit()`'s width math, because the engine measures screen cells. Falsified by a live drawing where the title overruns the right group.
- 2026-10-01: implement started on branch m194-band-layout. Question gate skipped: nothing was open. The `dismissed` atom holds a list of `{ id, status }` with no shape tag.
- 2026-10-01: minor amendment: T1 to T5 land in one checkpoint commit. The new line shape, the drawing, and the restated tests must change together, or the verify slot fails.
- 2026-10-01: T1-T5 done. The new tests ran red first on the old band code (28 fail, the AC3 cases for want of a close button). Two planted defects went red: a refresh that never clears `dismissed`, and a mark that also compares titles. Verify: scripts 394 OK, hooks 174 OK, validate clean, mod tests 82/82.
- 2026-10-01: a press hides the band for the rest of a test's session, so each AC2 case runs on one surface. A first draft mounted both surfaces in one session and failed on the second mount.
- 2026-10-01: T6 done. README "The milestone band" gains the two groups, the bold label, and a close-button paragraph. The `…` claim is gone, since the engine now cuts the title. DESIGN.md and the CHANGELOG entry follow. Verify green.

## Decisions
