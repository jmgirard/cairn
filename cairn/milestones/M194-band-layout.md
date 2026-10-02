# M194: A right-aligned milestone band with a close button

- **Status:** review
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
- A close `Button` with `role: 'dismiss'` and the label `×` on the terminal and the desktop. A press stores the ordered list of active ids and statuses in a new session state value, declared in `types/index.d.ts`. The band stays hidden while the current list equals the stored one. A new session starts with the band shown.
- The item row's positional label (`T3:`, `AC2:`) draws bold, and the rest of the row stays dim.
- README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.

**Out:**
- The other "Band layout edge cases" items (under 30 columns, the desktop `░` width, more than five milestones) → that candidate row.
- A rounded border around the band → not planned. The gate did not select it.
- A command that brings the band back → not planned. The band comes back when the list changes or in a new session.
- A roadmap pane, clickable next-command actions, `vscode` and `mobile` tests, and the Windows UNC walk → the "Status mod follow-ons" candidate row.
- A dim idle line between milestones → the "Band idle line" candidate row.

## Acceptance criteria

- [x] AC1: Each header row draws as a `Box` with `justifyContent: 'space-between'` whose children are two `Box` groups. The left group carries `flexShrink: 1` and holds the phase label, the id, and the title. The title's `Text` holds the whole ROADMAP title with `wrap="truncate-end"`, inside a `Box` with `flexShrink: 1`. The right group carries `flexShrink: 0` and `marginLeft: 2`. It holds the bar (at `bodyColumns` 60 or more) and the counts, or the state label that M193's AC2 names. On the first row it also holds AC2's close button. Shown by `claude plugin test` cases on the terminal and desktop surfaces that read the drawn elements' props from `findAll`. The cases mount `mixed` at `bodyColumns` 59, 60, and 120. At `bodyColumns` 40 they also mount two more fixtures. One has a title longer than 120 characters. The other has a title with wide characters and an emoji outside the Basic Multilingual Plane.
- [x] AC2: When the band draws rows, its tree holds exactly one `Button`. It is keyed `cairn-close` and is the last child of the first header row's right group. It has `role: 'dismiss'` and `plain`, and its label is `×` on the terminal and the desktop. A press makes the next drawing of the band pass to `next(e)`. That drawing holds no cairn row. It holds what the hooks beneath draw: the engine's own slot, or in its place the row a plugin beneath draws. Shown by `claude plugin test` cases on the terminal and desktop surfaces over `mixed` and `single-in-progress`, and over `mixed` with a plugin beneath that draws its own row.
- [x] AC3: After a press, the band stays hidden at each turn end whose refreshed active rows have the same ids and statuses, in the same ROADMAP order, as at the press. It shows again at the first turn end where that ordered list differs. It then stays shown until the next press. A list that returns to its press-time value does not hide it again. Shown by edit cases on both surfaces in `hooks/status/band.test.tsx`. A checked task box, an added `planned` row, and an edited title each keep the band hidden. Four edits each show it again: a row moved from `in-progress` to `review`, an added active row, a removed active row, and two active rows that swap ROADMAP order. A row moved to `review` shows the band. A move back to `in-progress` keeps it shown.
- [x] AC4: When the item row's text after its arrow matches `^(T|AC)\d+[a-z]*:`, the matched label's `Text` carries `bold`, and neither it nor any `Text` that encloses it carries `dimColor`. Every other `Text` of the item row carries `dimColor`. An item text with no such label has `dimColor` on every `Text`. Shown by `claude plugin test` cases on both surfaces over `mixed` (`AC3:`), `single-in-progress` (`T2:`), `nested-first` (`T1a:`), and a fixture whose first unchecked task has no positional label.
- [x] AC5: The band keeps M193's rows, texts, colors, ROADMAP order, survey yield, and stacking above `next(e)`, except where AC1, AC2, and AC4 change them. Shown by M193's cases in `hooks/status/band.test.tsx`, restated where AC1, AC2, or AC4 changed the tree, and passing on the surfaces each ran on.
- [x] AC6: The verify slot in `cairn/PROFILE.md` runs clean. It holds both Python suites, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T3, T4
- AC2 → T2, T3, T4, T7
- AC3 → T2, T3, T5
- AC4 → T1, T3, T4
- AC5 → T4
- AC6 → T4, T5, T6, T7

## Tasks

- [x] T1: Layout in `band.ts`. Build each header row as a left and a right group, remove `fit()`, and split the item row's positional label from the rest. Add fixtures for a long title, a wide-character title, and an unlabeled first task, then regenerate `fixtures.gen.ts`.
- [x] T2: Close state. Add a `dismissed` session atom that holds the ordered id and status list, and declare it in `types/index.d.ts`. The press handler reads the `band` atom inside the handler, not from a value captured at draw time. If the new list differs from `dismissed`, the refresh clears it.
- [x] T3: Render in `register.tsx`. Draw the two groups, the close button with its per-surface label, and the bold label. Pass to `next(e)` while `dismissed` equals the current list.
- [x] T4: Tests. Restate M193's cases where the tree changed. Add the AC1, AC2, and AC4 cases on both surfaces, red first.
- [x] T5: Edit cases for AC3 on both surfaces.
- [x] T6: Docs. Update README "The milestone band", the DESIGN.md `hooks/status/` line, and the CHANGELOG `Unreleased` entry.
- [x] T7: Label the close button `×` on the terminal and the desktop. Remove `CLOSE_LABEL` and its comment in `register.tsx`, set the test's `CLOSE` to `×` on both surfaces, and correct README's close-button paragraph. Read the CHANGELOG and DESIGN.md wording against it.
- [x] T8: Look at the band live in the desktop app at a normal and a narrow width, in both phases, with a wide-character title, and press the close button. Record what it showed in the work log.

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
- 2026-10-01: claim audit: 43 claims read, 6 corrected — hooks/status/band.ts, hooks/status/band.test.tsx (the README, CHANGELOG, and types claims held). The same reader re-read the 6 fixes and 3 optional "or order" fixes in register.tsx and the AC3 describe name: all held. Mod tests 82/82, validate clean.
- 2026-10-01: T7 first live look (desktop, implement phase, operator's screenshot): the bar and counts sat at the right edge. Two defects. The item row read `→ T7:…`, the text after the label cut to a bare ellipsis. The close button drew its label `Close milestone band` as text, not a native close control.
- 2026-10-01: item row fix: the arrow, label, and rest are now sibling Texts in the row Box. The rest sits inside a `flexShrink: 1` Box, as the title does. Before, one Text nested all three. AC4's wording already allowed this. Mod tests 82/82, validate clean.
- 2026-10-01: amendment gate after the live look: the operator chose the label `×` on the terminal and the desktop, keeping `role: 'dismiss'` and `plain`. This reverses the plan gate's native-close-control choice, because the desktop drew `Close milestone band` as text in the band. It also drops the desktop accessible name the first plan audit added, so the name is now `×`. AC2 and the Scope bullet are amended. Falsified by a desktop drawing where `×` does not read as closing the band.
- re-audit: AC2 (full) — four findings. "Both surfaces" had no antecedent, reworded to "the terminal and the desktop". No task carried the change, so T7 was added. README, register.tsx, and the test's `CLOSE` carry the old label. The reversal needs a work-log line. "Exactly one Button" covers more row sets than its cases, kept as in the plan.
- re-audit: AC2 (full) — README's close-button paragraph and the reversal line, both covered by T7 and the line above. Nothing else.
- 2026-10-01: minor amendment: a new T7 carries the label change. The live look moves to T8 and runs after it. Coverage adds T7 to AC2 and AC6.
- 2026-10-01: T7 done. The test's desktop label went to `×` first and failed red on the two desktop AC2 cases. Then `CLOSE_LABEL` was removed and README's paragraph corrected. The CHANGELOG and DESIGN.md wording names no label and holds. Verify: scripts 394 OK, hooks 174 OK, validate clean, mod tests 82/82.
- 2026-10-01: T8 second live look (desktop, implement phase, operator's screenshot): the button drew `×` and the bar and counts sat at the right edge. The item row's arrow and `T8:` label shrank to nothing, and its text ran past the edge with no ellipsis.
- 2026-10-01: shrink fix: the shrinking Boxes (left group, title, item rest) take `minWidth: 0`. The phase and id, and the item's arrow and label, sit in a Box with `flexShrink: 0`. New shrink assertions in the AC1 and AC4 cases failed 9 cases on the old code. Mod tests 82/82, scripts 394 OK, hooks 174 OK, validate clean.
- 2026-10-01: T8 done, third live look in the desktop app: the operator reported it looks right. The item row's arrow and bold label show, and its long text ends in `…`. The wide-character title cuts cleanly when narrow, and `×` hides the band, which stays hidden after a turn that changes nothing. Status set to review.

## Decisions

## Review

Fresh evidence 2026-10-01 on `m194-band-layout` at ed8c087. The branch was cut from 184e04d, and `origin/main` is still at 184e04d, so no merge was needed. The mod tests ran with the 2.1.286 desktop binary.

- AC1: `claude plugin test .` exits 0 with 82 pass and 0 fail. The AC1 group passes for `mixed` at 59, 60, and 120 columns, and for `long-title` and `wide-title` at 40 columns. Each case mounts on the terminal and the desktop and reads props from `findAll`. The row has `justifyContent: 'space-between'` and two Box groups. The left group has `flexShrink: 1`, and the right group has `flexShrink: 0` and `marginLeft: 2`. The title Text holds the whole title with `wrap: 'truncate-end'` inside a `flexShrink: 1` Box. The bar shows only at 60 columns or more. The close button is last in the first row's right group. A sixth case shows that the wide-title fixture holds `宽字符` and `🚀`.
- AC2: The AC2 group passes six cases. `mixed` and `single-in-progress` each run on the terminal and on the desktop, one session per surface. Each case finds exactly one Button, keyed `cairn-close`, with `role: 'dismiss'`, `plain: true`, and the label `×`. After a press, the drawing is the engine's slot alone, with no cairn element and no Button. Over `mixed` with a plugin beneath, a press leaves only that plugin's row, on both surfaces. The AC1 cases show the button is the last child of the first row's right group.
- AC3: The AC3 group in `hooks/status/band.test.tsx` passes 16 cases, eight edits on each surface. Each case presses the button, ends a turn with nothing changed, and sees the band still hidden. A checked task box, an added `planned` row, and an edited title each keep it hidden after the next turn end. Four edits each show it again with the expected row keys. They are a move from `in-progress` to `review`, an added active row, a removed active row, and two active rows that swap order. The last case moves a row to `review`, and the band shows. A move back keeps it shown until a second press hides it.
- AC4: The AC4 group passes four cases, each mounted on the terminal and the desktop. For `mixed` (`AC3:`), `single-in-progress` (`T2:`), and `nested-first` (`T1a:`), exactly one Text holds the label. That Text has `bold: true`, and no Text that encloses it has `dimColor`. Every other Text of the item row has `dimColor: true`. For `unlabeled-item`, every Text of the item row has `dimColor: true` and none is bold.
- AC5: Every `describe` group of `band.test.tsx` on `origin/main` is still on the branch. The four AC-numbered groups now carry an `M193` prefix, and none was removed. All M193 groups pass. They cover the rows in ROADMAP order, the survey yield, and the header-only states. They also cover the style props at three widths, six edit cases on both surfaces, the empty band, and the stacking over a plugin beneath. The reader group in `reader.test.ts` passes over all 13 fixtures. The restated cases read a header row through `rowText`, which joins the two groups by the right group's margin.
- AC6: The four verify commands ran from the repo root, each exit code read. `scripts/tests` exits 0 with 394 tests OK and 21 skipped. `hooks/tests` exits 0 with 174 tests OK. `claude plugin validate .claude-plugin/plugin.json` exits 0, "passed with warnings", one warning. `claude plugin test .` exits 0 with 82 pass and 0 fail.
- Consistency gate: `cairn_validate.py` exits 0, every check PASS or OK, `coverage complete` among them. No DESIGN.md principle changed, so the impact report was skipped. The `generic` profile names no toolchain checks.

Independent review: three fresh readers. The diff-bug reader (Opus) reported 10 findings, the blame-history reader (Sonnet) 8, and the prior-review reader (Sonnet) 5. The prior-review probe found no PR review comments. Merged duplicates give 14 findings below. None shows a criterion failing, so no return. Each line gives the proposed disposition, and the gate decides.

- F1: At narrow widths a header row can overrun. The head Box and the right group never shrink. At 40 columns, a 15-cell head plus `all 10 criteria checked` and the `×` needs 43 cells. M193's `fit()` kept such a row in bounds. Proposed: follow-up, added to the "Band layout edge cases" row.
- F2: `refresh` compares `dismissed` outside its `update` closure. A press that lands during a turn-end refresh can be overwritten with `null`. Proposed: follow-up, in a new "Band close-state edge cases" row.
- F3: A failed ROADMAP read gives an empty list, which clears `dismissed`. The next good read then shows the band with the same list. This meets AC3 as written. Proposed: follow-up, same new row.
- F4: README and CHANGELOG say "A new session starts with the band shown." No test or live look observed it. The API holds state for the session, and it is not known whether `/clear` keeps it. Proposed: fix now, by removing the sentence from both files. The open question goes to the new row.
- F5: The first row's bar and counts sit 3 columns left of the other rows', because only that row ends in the `×`. Proposed: reject. The operator's T8 live look accepted the drawing.
- F6: Spaces-only Texts are separate flex items. A surface that collapses white space draws them at zero width. Proposed: reject. The T8 live look showed the spacing.
- F7: The Scope bullet names "T7's live look", which the amendment moved to T8. Proposed: noted. Hygiene reads the T8 record.
- F8: New README prose has a ragged wrap ("the desktop app. Pressing it hides the band. The"), as does the DESIGN.md `hooks/status/` bullet. Proposed: fix now, by reflowing.
- F9: README and CHANGELOG say the counts "keep their place", the phrase M193's review replaced as unclear. Proposed: fix now, as "stay at the right edge".
- F10: No AC2 case over `single-in-progress` asserts that the button is the last child of the first row's right group. The AC2 evidence line overstated this. Proposed: fix now, by adding the assertion to the AC2 cases and correcting the evidence line.
- F11: The test keeps a per-surface `CLOSE` map, and `register.tsx` keeps a `CLOSE_GLYPH` comment. Proposed: reject. T7 was done as written, and the comment says why the label is short.
- F12: The `dismissed` atom has no shape tag, and `types/index.d.ts` is not type-checked. Proposed: reject. The work log records the choice, and a new atom has no older layout.
- F13: `dismiss($)` is untyped. Proposed: reject. It matches `refresh` and `fsSource` on main.
- F14: The wide-title cases check props only, and the T8 line does not say an emoji was in the live title. Proposed: noted. `band.ts` no longer slices the title, so the UTF-16 cut and the split pair are gone in code.
