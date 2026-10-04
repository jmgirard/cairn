# M205: A cairn pane in the status mod

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — every adopter loads the mod with the plugin (D-143)
- **Branch/PR:** m205-cairn-pane

## Goal

Give the status mod an optional pane that shows the active milestones in full and the planned queue with the next command.

## Scope

**In:** The mod registers a `/cairn-pane` slash command and adds an open
button to the band. Each of them opens a pane with id `cairn`, and the
command also closes an open pane. For each `in-progress` or `review`
milestone, the pane shows the goal, every task and criterion with its box,
and the last five work-log lines. Below them, it shows the command that
`scripts/cairn_next.py` recommends, the workable planned milestones, and
the planned milestones that wait on dependencies. The pane draws again at
each refresh the band takes. `cairn_next.py` gains `recommend` and
`waiting` functions, so the pane and the script share one rule. New
fixtures and new `pane` and `next` keys in each `expected.json` hold the
TypeScript reader and the Python helpers to the same values. README,
CHANGELOG, and DESIGN describe the pane.

**Out:** Candidate rows, decisions, and lessons in the pane go to the new
"Pane content follow-ons" candidate row. Buttons in the pane that run a
cairn command stay in the "Status mod follow-ons" row, with the clickable
band actions. The pane writes no tracking file. The terminal flow track
stays in the "Terminal flow track" row. If the desktop app places no plugin
pane, desktop pane support goes to a new candidate row (AC6).

## Acceptance criteria

- [x] AC1: The mod registers a `/cairn-pane` slash command at session start. If the session's working directory finds a cairn ROADMAP, the command opens a pane with id `cairn`. While that pane is open, the command closes it. If no ROADMAP is found, the command opens no pane and prints `no cairn ROADMAP found`. If the open returns `isPlaced: false`, the command prints the engine's reason. `claude plugin test` cases run the command through `$.command.run`. They assert these four outcomes through `ui.open`, `ui.close`, and `ui.panes` hooks beneath the mod.
- [x] AC2: The pane shows each `in-progress` or `review` ROADMAP row in ROADMAP order. For each row, it shows the id, title, and status, and the `## Goal` text of the milestone file. It shows each checkbox item of the `## Tasks` and `## Acceptance criteria` sections with its checked or open state. It shows the last five `## Work log` lines that open with `- `. If the milestone file is missing or its read fails, the row shows `no milestone file` in place of the file's parts. Each fixture's `expected.json` gains a `pane` key, which `gen_fixtures.py` carries into `fixtures.gen.ts`. An `unreadable` key in `expected.json` lists paths whose read fails in the tests. `claude plugin test` cases mount the pane over every fixture under `hooks/status/fixtures/` that has a ROADMAP. On the terminal and desktop surfaces, they assert each part against the `pane` key. The fixtures include a milestone file with more than five work-log lines and one with a goal of several paragraphs. One fixture uses the `unreadable` key.
- [x] AC3: Below the active milestones, the pane shows the slash command that a new `recommend(root, rows)` in `scripts/cairn_next.py` returns. The command carries an id when `recommend` names one. It shows the workable planned milestones in the order of `workable`, and the planned milestones that a new `waiting(root, rows)` returns. `render()` prints from those two functions. On every fixture with a ROADMAP, the pane's command and ids equal those of `cairn_next.py`. A `next` key in `expected.json` holds them. `scripts/tests/test_status_fixtures.py` compares that key to the Python functions, and `claude plugin test` cases compare it to the pane. One new fixture has only planned rows that wait on dependencies, so `recommend` returns `/milestone-plan`.
- [x] AC4: A band row drawn from a found ROADMAP carries an open button beside the close button. A press of the open button opens pane `cairn`. A skill row drawn with no ROADMAP carries no open button. `claude plugin test` cases press the button on the terminal and desktop surfaces and assert that the pane opened.
- [x] AC5: An open pane draws again from the files at each of six events. These are session start, turn end, a cairn skill prompt, a marked chapter, a Stop that ends a step, and an idle typed prompt that ends a step. A `claude plugin test` case for each event changes a fixture's milestone file before the event. It asserts that the next drawing shows the changed content.
- [x] AC6: The operator runs `/cairn-pane` in a new desktop Code session on this repo. If the app places the pane, the pane draws this repo's state and the operator accepts its look. If the app places no pane, the command prints the engine's reason, and a ROADMAP candidate row holds desktop pane support.
- [x] AC7: The verify slot in `cairn/PROFILE.md` runs clean. README, CHANGELOG, and DESIGN describe the pane, its command, and its open button.

## Coverage

- AC1 → T3, T5
- AC2 → T2, T4, T5
- AC3 → T2, T4, T5
- AC4 → T3, T5
- AC5 → T3, T5
- AC6 → T1, T6
- AC7 → T7

## Tasks

- [x] T1: Find out whether the desktop app places a plugin pane. Add a bare pane
      behind `/cairn-pane` on the branch. Ask the operator to run it in a new
      desktop Code session (LESSONS M195, M201), and log the result. If the
      app places no pane, the second arm of AC6 applies, and T6 skips the look.
- [x] T2: Reader and fixtures. Factor `recommend` and `waiting` out of
      `render()` in `scripts/cairn_next.py`. Extend `hooks/status/reader.ts`
      to read the goal, the item lists, the work-log tail, the recommended
      command, and the waiting rows. Add the `pane`, `next`, and `unreadable`
      keys to `gen_fixtures.py` and the `expected.json` files. Add the four
      new fixture shapes that AC2 and AC3 name, and extend
      `test_status_fixtures.py`.
- [x] T3: `register.tsx`. Register the command at `session.start`. Serve it
      with a `command.run` hook that opens or closes the pane. Add the open
      button to the band rows that a found ROADMAP draws. Keep the pane's
      data in the state that each refresh writes. Change the band tests that
      assert one Button to the `cairn-open` and `cairn-close` keys.
- [x] T4: Write a `pane.ts` layout module that turns the state into the
      pane's lines for a given width. Add a `ui.render` hook for
      `{ component: "Pane" }` that draws them on both surfaces.
- [x] T5: Write the `claude plugin test` cases for AC1 to AC5 in a new
      `hooks/status/pane.test.tsx`.
- [x] T6: Live look. First, prototype two or three pane looks in the browser
      pane (LESSONS M204). Then ask the operator to open the chosen look in a
      new desktop Code session.
- [x] T7: Write the README, CHANGELOG, and DESIGN text against the code.
      Run the verify slot.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision check absorbed the "roadmap pane opened by a slash command" item of the "Status mod follow-ons" candidate row. No D-entry rejects a pane, and D-143 covers the mod in the plugin. GitHub inbox has 0 open issues and 0 open PRs.
- 2026-10-04: criteria audit (full mode, fresh Opus reader) returned 9 findings. Command runs carry no surface, and the button clashed with the no-ROADMAP case. expected.json lacked keys, fixture shapes were thin, and `cairn_next` had no functions to mirror. AC3 bound an instrument, the band tests assert one Button, one case covered five triggers, and AC6 bound a work-log line. All were fixed by narrowing.
- 2026-10-04: re-audit of the narrowed and answer-changed criteria returned 3 findings, all fixed. A fixture file cannot fail its read, so an `unreadable` key was added. No fixture reached `/milestone-plan`, and `blocked` clashed with a local name, so a fixture was added and the function renamed `waiting`. The fifth trigger is two events, so AC5 has six cases.
- 2026-10-04: question set: pane content — active milestone (goal, tasks, criteria), last five work-log lines, and the queue with the next command. Candidate rows were declined and go to a new candidate row.
- 2026-10-04: question set: opening — the `/cairn-pane` command plus a band open button, with no automatic open.
- 2026-10-04: question set: desktop app places no pane — ship the terminal pane and record desktop support as a candidate row. The operator agreed to open new desktop Code sessions for the T1 check and the T6 live look.
- 2026-10-04: question set: command name — `/cairn-pane`.
- 2026-10-04: plan gate chose to mirror `cairn_next.py` through new `recommend` and `waiting` functions over a recommendation rule in TypeScript alone. One rule in two languages drifts unless a test holds them to the same fixtures. Falsified by a fixture where the two disagree and no test fails.
- 2026-10-04: plan gate chose a command plus a band button over a pane that opens itself at session start. The user asked for an optional pane. Falsified by the operator opening it at every session start.
- 2026-10-04: implement started on branch m205-cairn-pane. The untracked `tsconfig.json` at the repo root is not this milestone's and stays unstaged.
- 2026-10-04: T1 runs as a throwaway `pane-probe` mod in this session's hot-reload folder (`~/.claude/dev-mods/<session>/pane-probe`), not on the branch, so no probe code reaches the PR. It opens a pane at load and through `/pane-probe`, and logs `isPlaced` and the render props to `.git/pane-probe.log`. `claude plugin validate` passed on 2.1.286.
- 2026-10-04: T1 done. The operator enabled hot reload, and the desktop app placed the probe pane on the right. The log reads `isPlaced: true`, then `surface=desktop placement=dock bodyColumns=44`. The first arm of AC6 applies. The operator saw the band in its text form beside the docked pane. The likely cause is the narrower transcript column, below the width the M204 track needs. A probe log of the band's width will confirm it.
- 2026-10-04: T2 done. `cairn_next.py` gains `recommend` and `waiting`, and `render()` prints the same text as main on this repo and all 18 old fixtures. `reader.ts` gains `loadCairn`, which reads the band and pane state in one pass, and `loadBand` wraps it. Two fixtures were added: `pane-full` (long log, wrapped items, a goal of two paragraphs, an unreadable file, waiting rows) and `all-waiting`. The `next` key also carries `waiting`, and the workable ids stay in the existing `workable` key. Choice: the pane drops HTML comments from a section before it reads items, so a box inside a comment is not an item. The band and the validator still count it (`pane-full` M080 has 3 criteria in the band and 2 in the pane). Gates: scripts/tests 395 OK, hooks/tests OK, plugin validate passed, plugin test 1042 pass.
- 2026-10-04: T2 plants, each restored: `LOG_LINES` 6 and dropping the wrap join each failed the `pane-full` reader case, and `recommend` skipping review rows failed the Python fixture test on 4 fixtures.
- 2026-10-04: T3 to T5 done. New `hooks/status/pane.ts` (layout), a `pane` state atom (shape `pane-1`) written at each refresh, `/cairn-pane` registered after the session-start refresh in a try, so a refused registration leaves the band drawn. The open button is the glyph `≡` and one space, 2 columns, on the first row when a ROADMAP is found. It moves every band width threshold by 2: the band tests' worked sums now add `buttons 5`, and their one-Button checks name `cairn-open` and `cairn-close`. New `hooks/status/pane.test.tsx` holds 88 cases for AC1 to AC5. Gates: scripts/tests OK, hooks/tests OK, plugin validate passed, plugin test 1130 pass.
- 2026-10-04: T3 to T5 plants, each restored: a command that never closes failed AC1's toggle case, no `pane` write at refresh failed 307 cases, a chapter hook with no refresh failed AC5's chapter case, an open button that opens nothing failed both AC4 press cases, and dropped waiting rows failed 10 AC3 cases.
- 2026-10-04: T6 browser look: four looks of this repo's real pane at 44 columns, dark and light, served from the scratchpad. The operator picked D, one line per item: items, log lines, titles, and queue rows are cut with an ellipsis, and the goal wraps. Rejected: A (items wrap in full, M205 alone ran several screens tall), B (next command first, thin rules), C (card with a phase-colored edge and a command pill). Two cases pin the wrap props. The probe mod and its log were removed. Its band-width log never reloaded, so the cause of the text-form band beside the docked pane rests on the thresholds alone: the track needs 94 columns after the open button.
- 2026-10-04: T7 done. README gains "The cairn pane" and a sentence on the `≡` button, CHANGELOG a New entry, and DESIGN a pane paragraph in the `hooks/status/` entry, each written against the code read this session. The question-set chip said Esc closes the pane, but the API says the close mark or ctrl+x x closes it, so the README names the close mark only. Verify slot: scripts/tests OK, hooks/tests OK, plugin validate passed, plugin test 1132 pass. cairn_validate green.
- 2026-10-04: T6 closed. The operator was asked to open the pane in a new desktop Code session and resumed the run with no report of that look. No answer is recorded here, and AC6's acceptance goes to the merge question, as M204's in-app look did.
- 2026-10-04: claim audit: 54 claims read, 2 corrected — hooks/status/register.tsx, hooks/status/pane.ts
- 2026-10-04: after the audit, the unused `paneText` in `pane.ts` was deleted and its blank-row comment narrowed to what the code does. The desktop dock claim in the README rests on the T1 probe log (`placement=dock`), not on the API docs. Verify slot: scripts/tests OK, hooks/tests OK, plugin validate passed, plugin test 1132 pass. Status set to review.
- 2026-10-04: step-7 approval: m205-cairn-pane approved for merge

## Review

Evidence run 2026-10-04 on `m205-cairn-pane` at 1d4d74d, which contains `origin/main` (0d5d58a, unmoved since the cut).

- AC1 evidence: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` (2.1.286) passed all 3 "M205 AC1" cases. They raise `session.start`, run `/cairn-pane` through `$.command.run`, and assert through `ui.open`, `ui.close`, and `ui.panes` hooks beneath the mod: an open with id `cairn` and `cairn pane opened`, a close on the second run, `no cairn ROADMAP found` with no open on `no-roadmap`, and the engine's reason when the open is not placed.
- AC2 evidence: the same run passed all 40 "M205 AC2" cases: each of the 18 fixtures with a ROADMAP on the terminal and desktop surfaces, asserted against its `pane` key, plus the domain check, the no-ROADMAP pane, and the two wrap-prop cases. `pane-full` holds a file with 7 log lines, a two-paragraph goal, and an `unreadable` path. `gen_fixtures.py` carries `pane`, `next`, and `unreadable` (`test_generated_module_is_current` ok). The reader's 19 "pane's milestones and next step" cases also passed.
- AC3 evidence: `python3 -m unittest scripts.tests.test_status_fixtures` passed 4 of 4, including `test_python_helpers_match_expected`, which compares every fixture's `next` key to `cairn_next.recommend` and `cairn_next.waiting`. The plugin run passed all 37 "M205 AC3" cases (18 fixtures on 2 surfaces, and a check that the domain reaches all three commands and a waiting row). `all-waiting` gives `/milestone-plan`. `render()` printed the same bytes as main on the repo and every fixture (T2 and claim-audit runs).
- AC4 evidence: the plugin run passed all 4 "M205 AC4" cases: a press of `cairn-open` opens pane `cairn` on the terminal and desktop, and a `no-roadmap` skill row carries only `cairn-close` on both. The band suites' `buttonKeys` checks expect `cairn-open` then `cairn-close` on every row drawn from a ROADMAP.
- AC5 evidence: the plugin run passed all 6 "M205 AC5" cases, one per event: session start, turn end, cairn skill prompt, marked chapter, a Stop that ends a step, and an idle typed prompt that ends a step. Each ticks T2 in `single-in-progress` before the event and asserts the old line before it and the new line after it.
- AC7 evidence: verify slot clean: `scripts/tests` 395 OK (21 skipped), `hooks/tests` 174 OK, `claude plugin validate` passed with warnings, `claude plugin test` 1132 pass and 0 fail. README ("The cairn pane" and the `≡` sentence), CHANGELOG ("A cairn pane"), and DESIGN (the `hooks/status/` pane paragraph) name the pane, `/cairn-pane`, and the `≡` open button.
- AC6: no evidence yet. The operator's desktop look is asked at the merge question.
- AC6 evidence: at the merge question on 2026-10-04 the operator answered "Look accepted, merge": the pane was opened with `/cairn-pane` in a new desktop Code session and its look accepted. The desktop places the pane (T1 probe: `isPlaced: true`, `placement=dock`).

Consistency gate: `cairn_validate.py` all checks passed. No principle changed, so `cairn_impact` was skipped. The profile's consistency-gate slot names no toolchain checks.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: `/cairn-pane` closes the pane whenever `$.ui.panes()` lists it, so a second run closes an unplaced pane or one behind another tab — fix now, fixed 64fe152 (closes only when `isPlaced` and `isShown`, else opens).
- diff-bug #2: the test's `ui.open` and `ui.panes` mocks drop unplaced panes and report every pane placed, which hid #1 — fix now, fixed 64fe152.
- diff-bug #3: a ROADMAP with a duplicate id gives duplicate pane line keys — follow-up, row "Pane follow-ons (M205 review)".
- diff-bug #4: the desktop may draw the plain `≡` Button as a native button wider than the 2 columns reserved — follow-up, same row.
- diff-bug #5: the AC5 cases mount a new pane after each event, so they prove the state changed, not that an open pane redraws — fix now, fixed 64fe152 (one mount across the event).
- diff-bug #6: a found but unreadable ROADMAP before any good refresh makes the command print `no cairn ROADMAP found` — follow-up, same row.
- diff-bug #7: a throw from the refresh skips the command's registration, and a module reload may drop it — follow-up, same row.
- diff-bug #8: a refused `$.ui.open` or `$.ui.close` throws from the command, and the button ignores an unplaced open — fix now, fixed 64fe152 (a `cairn pane:` line, and a toast from the button).
- diff-bug #9: the band counts a box inside an HTML comment and the pane does not — follow-up, same row.
- diff-bug #10: whitespace parity gaps between JS and Python (BOM, `\x1f`) — follow-up, same row.
- diff-bug #11: the Python test matched `unreadable` paths as `/cairn/` plus the row path, wrong for a fixture whose root is a subdirectory — fix now, fixed 64fe152.
- diff-bug #12: `CairnPaneState` in `types/index.d.ts` and `PaneState` in `reader.ts` are separate copies — follow-up, same row.
- diff-bug #13: `refresh` writes `band` and `pane` in two updates, so one drawing can mix them — follow-up, same row.
- diff-bug #14: `render()` lists the archive three times — follow-up, same row.
- diff-bug #15: README said the command prints `no cairn ROADMAP found` outside a repo, but with a pane open it closes it — fix now, fixed 64fe152 (README and CHANGELOG).
- blame-history #1: a throw in the new pane parsing now keeps the band's old rows too — follow-up, same row.
- blame-history #2: band and pane counts differ on comment boxes — follow-up, same as diff-bug #9.
- blame-history #3: every band threshold rose by 2 columns, so a 92 to 93 column desktop loses the track — reject, planned change (AC4's button).
- blame-history #4: the `≡` button opens and does not toggle — reject, planned change (AC4 says the press opens).
- blame-history #5: registration after a throwing refresh — follow-up, same as diff-bug #7.
- blame-history #6: the command's `found` can be stale after a failed read — follow-up, same as diff-bug #6.
- blame-history #7: the archive listed three times — follow-up, same as diff-bug #14.
- blame-history #8: the type copies, and `reader.ts`'s header named only `workable` — fix now for the header, fixed 64fe152; the copies are follow-up, same as diff-bug #12.
- blame-history #9: the README's 110-column claim is not traced — reject, false: the API's `UiOpenResult` doc states the 110-column dock rule, and the claim audit read it there.
- prior-review #1: the pane joins the M200 deferred items (equal-value writes, stale rows after a move) — follow-up, same row, cross-referencing "Status mod follow-ons".
- prior-review #2: the lead's span Texts have no key — reject, style: the band's `spans()` draws the same way and its live looks drew correctly.
- prior-review #3: the pane's line Box has no `minWidth: 0` — follow-up, same row.
- prior-review #4: the `pane-1` shape tag needs a bump on a later layout change — reject, false: the reviewer reports no defect now.
- prior-review #5: the fixed phase colors and `warning` key carry the theme gap into the pane — follow-up, same row, cross-referencing "Band label colors in other themes".

After the fixes: scripts/tests OK, hooks/tests OK, plugin validate passed, plugin test 1136 pass (4 new). A plant of the old toggle rule failed the two new AC1 cases.
