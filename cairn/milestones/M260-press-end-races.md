# M260: Press and placement races end cleanly

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane's Buttons and PR read, shipped in the plugin's status mod
- **Branch/PR:** m260-press-end-races

## Goal

A rejected session end, an end during a ⌂ press's state read, and an end during a start's second pane listing each leave the pane's Buttons and PR read in the state a person expects.

## Scope

**In:** `hooks/status/register.tsx`: the session-end handler frees the action Buttons and reports a held command when the end beneath it rejects; `pressHome` stops when a session end lands during its step read; the classic SessionStart hook's second listing reads nothing once a session end has passed since it began. `hooks/status/pane.test.tsx`: a `prompt.fill` record in the test `seat`, `copy.panesHold` used on the second listing, and the tests below. A `CHANGELOG.md` entry.

**Out:**
- The other 15 items of the six pane and press rows ("Pane edges (M238 review)", "Home Button edges (M241 review)", "Plan Button edges (M242 review)", "Shared press mark edges (M243 review)", "Press end edges (M255 review)", "Late placement edges (M256 review)"): rare or unlooked races, cosmetic gaps, and tests for behavior that already works → pruned at the user's choice (question set); the six rows go at M260's post-merge hygiene, git keeps their text.
- The open that a ⌂ press's mark gives a typed `/clear` end ("Home Button edges" item) → pruned with the rest; AC3 keeps today's open for a `clear` end.

## Acceptance criteria

- [ ] AC1: When the session end beneath a press's `/clear` rejects, the action Buttons work again afterwards: a test in `hooks/status/pane.test.tsx` makes the end reject (`copy.endThrows`) after a press whose `/clear` run never settles (`copy.runHold`), then presses an action Button again and finds that press's command in `copy.commands`.
- [ ] AC2: When a session end of either reason rejects while a command is held for it, the prompt box gets the command's line and a toast reads `cairn: the session end failed (<line>)`: tests in `hooks/status/pane.test.tsx` cover a rejected `clear` end and a rejected `other` end and assert both the prompt-box text and the toast text.
- [ ] AC3: A session end that lands while a ⌂ press waits on its step read cancels that press, so the press runs no `/clear`: tests in `hooks/status/pane.test.tsx` hold the step read (`holdStep`), end the session with a resolving `clear` end, a rejecting `clear` end, and a resolving `other` end, release the read, and find no `/clear` in `copy.commands`; for the two `clear` ends they find the one pane open that the end itself gives, and for the `other` end none.
- [ ] AC4: A start's second pane listing that is still pending at a session end reads nothing: a test in `hooks/status/pane.test.tsx` holds the old start's second listing with a placed answer, ends the session, has a new start list the pane unplaced twice, releases the held listing, and finds no PR-state read added; the pane's next draw then makes exactly one.
- [ ] AC5: `CHANGELOG.md`'s Unreleased section carries one entry naming these fixes, and each behavior it claims is asserted by one of the AC1–AC4 tests.
- [ ] AC6: The `cairn/PROFILE.md` verify slot is clean: `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .`, both `python3 -m unittest` suites, and `claude plugin validate` on the plugin and marketplace manifests.

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

## Decisions

## Review
