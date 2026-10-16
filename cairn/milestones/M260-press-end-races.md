# M260: Press and placement races end cleanly

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane's Buttons and PR read, shipped in the plugin's status mod
- **Branch/PR:** m260-press-end-races · https://github.com/jmgirard/cairn/pull/271

## Goal

A rejected session end, an end during a ⌂ press's state read, and an end during a start's second pane listing each leave the pane's Buttons and PR read in the state a person expects.

## Scope

**In:** `hooks/status/register.tsx`: the session-end handler frees the action Buttons and reports a held command when the end beneath it rejects; `pressHome` stops when a session end lands during its step read; the classic SessionStart hook's second listing reads nothing once a session end has passed since it began. `hooks/status/pane.test.tsx`: a `prompt.fill` record in the test `seat`, `copy.panesHold` used on the second listing, and the tests below. A `CHANGELOG.md` entry.

**Out:**
- The other 15 items of the six pane and press rows ("Pane edges (M238 review)", "Home Button edges (M241 review)", "Plan Button edges (M242 review)", "Shared press mark edges (M243 review)", "Press end edges (M255 review)", "Late placement edges (M256 review)"): rare or unlooked races, cosmetic gaps, and tests for behavior that already works → pruned at the user's choice (question set); the six rows go at M260's post-merge hygiene, git keeps their text.
- The open that a ⌂ press's mark gives a typed `/clear` end ("Home Button edges" item) → pruned with the rest; AC3 keeps today's open for a `clear` end.

## Acceptance criteria

- [x] AC1: When the session end beneath a press's `/clear` rejects, the action Buttons work again afterwards: a test in `hooks/status/pane.test.tsx` makes the end reject (`copy.endThrows`) after a press whose `/clear` run never settles (`copy.runHold`), then presses an action Button again and finds that press's command in `copy.commands`.
- [x] AC2: When a session end of either reason rejects while a command is held for it, the prompt box gets the command's line and a toast reads `cairn: the session end failed (<line>)`: tests in `hooks/status/pane.test.tsx` cover a rejected `clear` end and a rejected `other` end and assert both the prompt-box text and the toast text.
- [x] AC3: A session end that lands while a ⌂ press waits on its step read cancels that press, so the press runs no `/clear`: tests in `hooks/status/pane.test.tsx` hold the step read (`holdStep`), end the session with a resolving `clear` end, a rejecting `clear` end, and a resolving `other` end, release the read, and find no `/clear` in `copy.commands`; for the two `clear` ends they find the one pane open that the end itself gives, and for the `other` end none.
- [x] AC4: A start's second pane listing that is still pending at a session end reads nothing: a test in `hooks/status/pane.test.tsx` holds the old start's second listing with a placed answer, ends the session, has a new start list the pane unplaced twice, releases the held listing, and finds no PR-state read added; the pane's next draw then makes exactly one.
- [x] AC5: `CHANGELOG.md`'s Unreleased section carries one entry naming these fixes, and each behavior it claims is asserted by one of the AC1–AC4 tests.
- [x] AC6: The `cairn/PROFILE.md` verify slot is clean: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`, both `python3 -m unittest` suites, and `claude plugin validate` on the plugin and marketplace manifests.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T4

## Tasks

- [x] T1: Rejected end. Add a `prompt.fill` record to `pane.test.tsx`'s `seat` (`band.test.tsx:159` records fills). Write the AC1 and AC2 tests and see them fail; then in the end handler (`register.tsx` about :534-566) free `running` and `pressCheck` on the rejecting path too, and hand a held command to `fallBack` with `the session end failed`, for both reasons, before the rethrow.
- [x] T2: ⌂ press during an end. Write the AC3 tests with `holdStep` (`pane.test.tsx` about :4363; the unawaited-press pattern at about :4405) and see them fail; then make `pressHome` (`register.tsx` about :1179-1188) return after its step read when a session end came during it (compare `ends`, as `pressChecked` does at about :1157).
- [x] T3: Second listing across an end. Write the AC4 test, re-arming `copy.panesHold` for the second listing (pattern at `pane.test.tsx` about :3663-3676; set `unplaced` before release, as the held answer is computed at hold time) and see it fail; then snapshot `ends` before the second listing (`register.tsx` about :282) and read only when it has not moved.
- [x] T4: Write the CHANGELOG entry from the tests' observed behavior; run the full verify slot from the repo root and check each exit code.

## Work log

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — three behavior fixes across one handler, one press, and one hook, chosen from a finding-absorbing group at the /milestone audit (router: /milestone §3 disposition chip).
- 2026-10-15: investigation (one Sonnet Explore over `hooks/status/`): all 21 items of the six rows real at e2ae8271; none seen in normal use; 6 test gaps, 15 rare or unlooked; three cheap fixes picked.
- 2026-10-15: criteria audit (full mode, fresh Opus reader): AC1 and AC5 clean; AC2 widened to both end reasons, stated toast text, and a `prompt.fill` stub; AC3 given three end kinds and the open asserted; AC4 rewritten to observable reads, since one-read-total passed on today's code and the `$` used was not observable. All taken toward the narrower or testable form.
- 2026-10-15: question set: scope — the three race fixes only; the other 15 items — pruned, no Known issues entry.
- 2026-10-15: plan gate chose a new `the session end failed` reason over reusing `the session ended before /clear`, because that text is wrong for a `clear` end; falsified by a toast reader keyed to the old text.
- 2026-10-15: plan gate chose an `ends` snapshot for the ⌂ press and the second listing over per-press tokens, because `pressChecked` already guards with `ends`; falsified by an end that leaves `ends` unchanged.
- 2026-10-15: implement started on `m260-press-end-races`; untracked `cairn-probe.log` and `tsconfig.json` at the repo root are not this milestone's and stay unstaged.
- 2026-10-15: T1 done: the three AC1/AC2 tests failed first (Status press did not run; no prompt fill), then the end handler's catch frees `running` and `pressCheck` and hands a held command to `fallBack` with `the session end failed`; plugin test 1762 pass, both Python suites and both validates clean.
- 2026-10-15: T2 done: the three AC3 tests failed first (each ran a late `/clear`), then `pressHome` returns when `ends` moved during its step read; plugin test 1765 pass, verify clean.
- 2026-10-15: T3 done: the AC4 test failed first (the old start's held second listing added one PR read after `await old`; the in-try assertion before the release passed), then the classic SessionStart hook snapshots `ends` before the second listing and reads only when it has not moved; plugin test 1766 pass, verify clean.
- 2026-10-15: T4 done: CHANGELOG Fixes entry written from the AC1–AC4 tests (held-command claim narrowed to the next-step Button, the press the AC2 tests drive); full verify slot exit 0 on each of its five commands. The simple-english lint hook flags 341 pre-existing hits across CHANGELOG.md; only the new entry's one over-long sentence was fixed.
- 2026-10-15: claim audit: 21 claims read, 4 corrected — CHANGELOG.md, hooks/status/register.tsx, hooks/status/pane.test.tsx (the owed-read sentence in the changelog and the AC4 comment narrowed to "a later start's read is its own"; the catch comment names the `clear` end; the `ends` comment names its M260 readers; the ✎ and `/resume` widenings were declined as untested; the same reader re-read the four: accurate).
- 2026-10-15: all tasks done, verify clean (plugin test 1766 pass, both Python suites, both validates exit 0); status → review.

## Decisions

## Review

Pass 1, 2026-10-15, branch head 1b247a00 + PR record; PR #271 opened at review start (Copilot round on), Copilot requested (state `none` before the request).

- AC1: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exit 0, 1766 pass; "a rejected session end frees the action Buttons (M260 AC1)" passes (⌂ press with `copy.runHold`, `copy.endThrows` end rejects, a later Status press's run in `copy.commands`); it failed before T1's fix with only `[CLEAR_RUN]` (work log).
- AC2: same run; both "a rejected session end hands its held command to the prompt box (M260 AC2)" tests pass, one with a rejected `clear` end, one with a rejected `other` end, each asserting `copy.fills` `[{ text: '/cairn:milestone-plan', mode: 'append' }]` and `copy.toasts` `['cairn: the session end failed (/cairn:milestone-plan)']`.
- AC3: same run; the three "a session end during a ⌂ press's step read cancels its /clear (M260 AC3)" tests pass (resolving `clear`, rejecting `clear`, resolving `other`), each holding the step read with `holdStep`, finding `copy.commands` empty, and finding one pane open for the two `clear` ends and none for the `other` end.
- AC4: same run; "a second listing pending at a session end reads nothing (M260 AC4)" passes: the old start's second listing held placed, a session end, a new start listing unplaced twice, `calls.reads` `[]` after the release, then `[URL_1250]` after one `draw($)`.
- AC5: `CHANGELOG.md` Unreleased › Fixes has one new entry, "Three session-end races in the cairn pane are closed."; its claims read against the tests: Buttons work after a failed end with a `/clear` that never finishes (AC1 test), the next-step Button's held command to the prompt box with the stated toast (AC2 tests), the ⌂ press cancelled and a `/clear` end still opening the pane (AC3 tests), the pending second listing reading nothing and the later start's read its own (AC4 test); no milestone number in the added lines (grep count 0).
- AC6: verify slot on the review head, each exit code read: plugin test 0 (1766 pass, 0 fail), `scripts/tests` 0, `hooks/tests` 0, `claude plugin validate` plugin.json 0 and marketplace.json 0.
- Consistency gate: `cairn_validate.py` exit 0, all checks passed; no principle changed, so `cairn_impact` skipped; marketplace validate output has no `version` warning (grep count 0); the changelog has the entry (AC5).
- spawned: diff-bug, blame-history, prior-review.
- diff-bug #1: the `ends` snapshot sits after the first listing, so an end during `refresh` or the first listing still lets the old start read or set `owed` — fix now, fixed c875fae0 (snapshot at hook entry, checked after the first listing; new test fails without it).
- diff-bug #2: a press made during a pending end that then rejects is freed under its checks, so a double press can overlap — follow-up, row "Rejected end edges (M260 review)" (the success path has had the same exposure since M255).
- diff-bug #3: a rejected `clear` end opens the pane for ⌂ yet fills the held command — reject, planned change (AC2 asks for the fill on both reasons; AC3 keeps the open).
- diff-bug #4: no test covers the catch's `pressCheck = null` — fix now, fixed c875fae0 (rejecting-end variant of M255's cut-off press test; fails without the line).
- diff-bug #5: a cancelled ⌂ press still gets the pane open on a `clear` end — reject, planned change (Scope Out; AC3 asserts it).
- diff-bug #6: `homeRun` stays set if the step read rejects — follow-up, row "Rejected end edges (M260 review)" (predates M260).
- diff-bug #7: the catch skips the end's `step`/`expanded`/`dismissed`/`ended` updates while the Buttons are free — follow-up, row "Rejected end edges (M260 review)" (M255 kept the skip; presses re-read `step`).
- diff-bug #8: absence checks wait about 10 ms — follow-up, row "Rejected end edges (M260 review)" (the kit's `untilRuns`/`untilOpens` convention).
- diff-bug #9: the AC2 test checks fills only after polling toasts — fix now, fixed c875fae0 (polls both).
- diff-bug #10: AC4's meaning depends on the hold computing its answer at hold time — reject, false (the `Copy.panesHold` comment states that contract).
- diff-bug #11: "the pane Buttons now work again" is wider than the Status-press test — reject, false (every action press gates on the one `busy()` check, register.tsx `busy`).
- blame-history #1: same as diff-bug #7 — follow-up, same row.
- blame-history #2: if the end's failure also rejects the `/clear` run, two fills and two toasts appear — reject, planned change (each names a line that did not run, as AC2 asks).
- blame-history #3: DESIGN.md lines on a rejecting end, the ⌂ press, and the start hook are stale; README has no failed-end case — fix now, fixed c875fae0.
- blame-history #4: same as diff-bug #1 — fix now, fixed c875fae0.
- blame-history #5: same as diff-bug #5 — reject, planned change.
- blame-history #6: same as diff-bug #3 — reject, planned change.
- blame-history #7: the catch does not bump `runs` — reject, false (the reviewer found no failing path; a stale run cannot free a newer one).
- blame-history #8: the start hook's comments overlap — reject, style.
- prior-review #1: same as diff-bug #2 — follow-up, same row.
- prior-review #2: same as diff-bug #8 — follow-up, same row.
- prior-review #3: the ✎ held-command path is not tested through the catch — reject, false (the catch reads `heldRun` alone, and the changelog claims only the next-step Button).
- prior-review #4: the AC3 table has no rejecting `other` end — fix now, fixed c875fae0.
- prior-review #5: the open on a rejecting `clear` end is now asserted though an older row listed it — reject, planned change (AC3).
- prior-review #6: second-listing not-placed/throws and `/resume` gaps stay open — reject, planned change (pruned at the question set).
- prior-review #7: the toast cause is not reintroduced wrong — noted.
- Return floor: no finding shows a criterion failing or a load-bearing defect; no status change. Fix-now verify after c875fae0: plugin test exit 0 (1769 pass), both Python suites 0, both validates 0, `cairn_validate` green. The follow-up row lands at post-merge hygiene, when the six graduated rows leave (ROADMAP is at its 59-line limit now).
