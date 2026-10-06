# M221: Plan and Implement clear the conversation first

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — the band and pane Buttons ship to every plugin user
- **Branch/PR:** m221-clear-then-run

## Goal

A press of the `Plan` or `Implement` Button, on the band or in the pane, runs `/clear` and then its command in the cleared conversation.

## Scope

**In:** T1 is a live probe that finds how a second command can run after
`/clear`. The M216 comment at `register.tsx:340` says a `clear` run "may
never settle". Two candidate ways are to await the `clear` run, or to hold
the command and run it from the `session.end` hook when the reason is
`clear`. A held command is taken at press time, and it starts after that
hook resets `running`, under a new run number. Then `pressNext` runs `clear`
before `cairn:milestone-plan` and `cairn:milestone-implement`, on the band
and in the pane. The labels stay `Plan` and `Implement`. If the `clear` run
is refused, the second command does not run, and the prompt box and toast
act as a refused run does today, naming `/clear`. README, DESIGN, CHANGELOG,
and the `register.tsx` comments describe it. IP3 is touched because a press
now drops the conversation. The plan gate's answer is that the press is the
person's consent, as the Clear Button's is (M216), and the docs say so.

**Out:** `Resume`, `Review`, `Status`, and the Clear Button, which keep
their one command. Labels that name the clear: the plan gate declined them.
A held command that survives a module reload goes to a candidate row at
review if T1 picks the held-command way. If T1 finds no way that works in a
live session, implement stops with the goal-wrong stop, and the milestone
returns to `planned` for a re-cut.

## Acceptance criteria

- [x] AC1: For each fixture in `EMPTY_FIXTURES` (band) and each
      `WITH_ROADMAP` pane fixture whose next action is
      `plan the next milestone`, on the terminal and desktop surfaces, a
      press of `cairn-next` (band) or `cairn-pane-next` (pane) labeled
      `Plan`, followed by `$.session.end({ reason: 'clear' })`, leaves
      exactly two commands beneath, in order: `clear` with args `''`, then
      `cairn:milestone-plan` with args `''`. A second press of any action
      Button between the press and that session end adds no command. Mod
      tests assert both.
- [x] AC2: For each fixture that the band's idle-domain check
      (`IDLE_DRAWN`) lists, and each pane fixture whose next action is
      `implement`, on the terminal and desktop surfaces, a press of the
      Button labeled `Implement`, followed by the same session end, leaves
      exactly `clear` with `''`, then `cairn:milestone-implement` with the
      next step's id. Mod tests assert the list.
- [x] AC3: The Resume, Review, and Status cases of the M212, M213, and M218
      press tests pass with their expected lists unchanged, and the Plan and
      Implement cases change as AC1 and AC2 state. A Clear press followed by
      `$.session.end({ reason: 'clear' })` leaves only `clear`, and the M216
      press tests pass unchanged.
- [x] AC4: On the band, on both surfaces, for one empty-row and one
      idle-row fixture: when the `clear` run rejects and
      `$.session.end({ reason: 'clear' })` follows, the commands beneath are
      only `clear`, the prompt box gets `/clear` appended, and a toast names
      it. After a press, `$.session.end({ reason: 'resume' })` and then
      `$.session.end({ reason: 'clear' })` leave only `clear`. Mod tests
      assert both cases.
- [x] AC5: At a live look in the desktop app, in a fresh Code session in a
      cairn repo whose band shows the empty row, the operator presses `Plan`
      and sees the conversation clear and `/cairn:milestone-plan` start in
      the cleared conversation. In a fresh session in a cairn repo whose band
      shows an idle row, the operator presses `Implement` and sees the same
      with `/cairn:milestone-implement <id>`, and can then stop the run. The
      operator accepts the look.
- [x] AC6: README.md and `cairn/DESIGN.md` say that `Plan` and `Implement`
      clear the conversation before they run, and CHANGELOG.md's Unreleased
      section has an entry for it.
- [x] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T2, T3
- AC5 → T5
- AC6 → T4
- AC7 → T6

## Tasks

- [x] T1: Live probe. Load the plugin-authoring skill and write a throwaway
      mod in this session's hot-reload folder (LESSONS M205) with two
      Buttons: one awaits `$.command.run({ command: 'clear' })` and then
      runs a harmless command, and one holds the command and runs it from
      `session.end` with reason `clear`. Log each step with `$.fs.write` to
      a file in `.git/info/exclude` (LESSONS M201). The operator turns on
      hot reload and presses each Button. Record which way runs the second
      command in the cleared conversation, and remove the probe mod.
- [x] T2: Write the AC1 to AC4 tests first. The pane harness gains a
      `session.end` hook beneath the mod, and `runThrows` where AC4 needs it.
      Change the Plan and Implement cases of the M212, M213, and M218 press
      tests to the two-command lists.
- [x] T3: In `register.tsx`, make `pressNext` run `clear` and then the
      command for `Plan` and `Implement`, by the way T1 found. Keep the
      guards of `running`, the step, and `ended`, so a second press adds
      nothing.
- [x] T4: Update README.md, `cairn/DESIGN.md`, CHANGELOG.md, and the
      `register.tsx` comments.
- [x] T5: Live look (AC5): in a fresh Code session in ackwards (empty row),
      the operator presses `Plan`. In a fresh session in openac (idle row,
      M21), the operator presses `Implement` and stops the run.
- [x] T6: Run every `verify` command from the repo root and check each exit
      code.

## Work log

- 2026-10-06: created by /milestone-plan.
- 2026-10-06: collision check: M212, M213, M216, M218, and M219 (done) ship the Buttons and the Clear Button, and none clears before a command. D-148 starts the next milestone after a `/clear`, which this automates. No open issue or PR. Not a checker scope.
- 2026-10-06: criteria audit (full mode, fresh Opus reader): AC3 contradicted the M212, M213, and M218 press tests, so it now names the cases that change. AC4 assumed the held-command way, so it now states outcomes that hold for either way, and it covers a stale command after a refused clear. AC1 gained the second-press case. The pane harness needs a `session.end` hook and `runThrows` (T2). The IP3 point (a press drops the conversation) went to the question set, which chose consent by press with docs.
- 2026-10-06: question set: buttons — `Plan` and `Implement` clear first, and `Resume` and `Review` do not.
- 2026-10-06: question set: labels — keep `Plan` and `Implement`, and the docs say that they clear.
- 2026-10-06: question set: probe and look — the operator turns on hot reload and presses the probe's Buttons, and does the live look in ackwards and openac before review.
- 2026-10-06: plan gate chose clearing for Plan and Implement over every next-step Button because a resumed run keeps its conversation; falsified by a resumed run that suffers from the old context.
- 2026-10-06: plan gate chose the plain labels over `Clear + Plan` labels because they take 8 fewer columns; falsified by an operator who presses `Plan` and did not expect the clear.
- 2026-10-06: checkpoint: the ROADMAP is at 60 lines and 24112 bytes with the M221 row, over its caps. The plan waits on the operator's approval to drop the M219 done row before validate passes and the plan is pushed.
- 2026-10-06: the operator gave standing approval to drop archived done rows to meet the ROADMAP caps; the M219 row went.
- 2026-10-06: implement started on m221-clear-then-run. Untracked `cairn-probe.log` and `tsconfig.json` stay unstaged, as they are not milestone work.
- 2026-10-06: T1 probe written at `~/.claude/dev-mods/81d5525c-eb5f-4258-92f2-398cb5647ae8/clear-probe/` (validates). Its band row has `A: await` (await the `clear` run, then run `cairn:milestone`) and `B: hold` (hold `cairn:milestone`, start `clear` unawaited, run the held command from `session.end` with reason `clear`). Each step is logged to `m221-probe.log` (in `.git/info/exclude`). Each press clears this session's conversation, so the run resumes from `/milestone-implement M221`, which reads the log and the operator's report to finish T1.
- 2026-10-06: T1 done. The operator pressed both probe Buttons, and each cleared the conversation and then ran `/cairn:milestone` in it. B showed its run after a short delay. The log shows that `session.end` with reason `clear` arrives before the `clear` run resolves, in A as in B. Chose the held-command way (B, with the `clear` run still awaited for its refusal), because AC4's stale-command case holds only when the command waits for the clear's session end. In the test harness a run resolves at once, so the await way runs the command before any session end. The probe mod is removed.
- 2026-10-06: T2 done. The band tests gain the M221 AC1 to AC4 cases. The pane harness gains a `session.end` hook and the AC1 and AC2 cases. AC4 is band only, so the pane harness needs no `runThrows`. The M212 AC1 Implement case, the M213 Plan cases, and the M218 AC3 Implement and Plan cases now expect `clear` first. Before T3, 51 tests failed, and each was a changed or new M221 case.
- 2026-10-06: T3 done. For `implement` and `plan the next milestone`, `pressNext` holds the command and runs `clear`. If that run rejects, the press drops the held command. At a session end with reason `clear`, the `session.end` hook runs the held command unawaited. Any other session end drops it. While a command is held, the action Buttons do nothing, as during a run in flight. All 1287 mod tests pass. Two planted defects failed 32 of the new cases: a held command run at each session end, and a press guard that ignores a held command.
- 2026-10-06: T4 done. README (idle row, empty row, pane), DESIGN (the band paragraph and the module list), CHANGELOG (Unreleased, New), and the `register.tsx` header say that `Plan` and `Implement` run `/clear` first. The README and DESIGN text state the consent point. The plugin install is a symlink to this checkout, so a fresh session loads the branch's mod for T5. ackwards recommends planning and openac recommends `implement M21`, as T5 needs.
- 2026-10-06: T5 done. The operator reported that in fresh desktop sessions `Plan` and `Implement` both cleared the conversation and then ran the next step, and accepted the look. The band did not show in a new session until the first message. That is the desktop app starting the session's process at the first message, as DESIGN records for `/clear` (M200 live look), and it is outside M221.
- 2026-10-06: T6 done at a41f0ca. The two unittest suites, both `claude plugin validate` runs, and `claude plugin test .` (1287 pass, 0 fail) each exited 0.
- 2026-10-06: claim audit: 66 claims read, 2 corrected — README.md, hooks/status/band.test.tsx
- 2026-10-06: the corrections: the README's Plan refusal now names `/clear` only for a refused clear and `/cairn:milestone-plan` for a refused planning run, and the AC4 control's comment and name now say it covers `no-active` on one surface. The same reader re-read both and found them true. The mod tests pass after the change (1287, 0 fail). Status set to `review`.

## Review

Evidence at fc61a0c, after `git fetch`: the branch contains `origin/main`, and no PR exists. One fresh `claude plugin test .` run: 1287 pass, 0 fail.

- AC1 (evidence): the M221 AC1/AC2 band block passes for `all-waiting` and `candidates-skeleton` (the `EMPTY_FIXTURES`) on both surfaces, 4 tests. Each presses `Plan`, then every action Button (Clear, next, Status), sees only `clear`, then after `$.session.end({ reason: 'clear' })` sees `clear` with `''`, then `cairn:milestone-plan` with `''`. The pane block passes for both plan fixtures on both surfaces.
- AC2 (evidence): the same band block passes for the 5 `IDLE_DRAWN` fixtures on both surfaces, 10 tests, each ending with `clear`, then `cairn:milestone-implement` with the idle row's id. A domain test holds each fixture's next action as `implement` and its args as the idle id. The pane block passes for the 5 implement fixtures on both surfaces, and its domain test holds both actions covered (15 pane tests in all).
- AC3 (evidence): the M212 AC1 (9), M212 AC3 (2), M212 review (2), M213 AC2/AC3 (10), M218 AC3 (11), and M216 (28) tests pass. `git diff main...HEAD` removes `expect(copy.commands)` lines only in the M212 AC1, M213, and M218 AC3 blocks. The Resume and Review fixtures keep `[nextRun(name)]` and `[runOf(name)]` in the unchanged branch, and only the Implement and Plan cases now expect `clear` first. No M216 test line changed. The M221 AC3 test passes on both surfaces: a Clear press and the clear's session end leave only `clear`.
- AC4 (evidence): the M221 AC4 block passes, 9 tests: for `all-waiting` (empty row) and `no-active` (idle row) on both surfaces, a rejected `clear` then the clear's session end leaves only `clear`, the fill `/clear` with mode `append`, and the toast naming `(/clear)`. A press, a `resume` end, then a `clear` end leaves only `clear`. The control (no-active, no refusal, no resume end) leaves `clear`, then the command. Two planted defects at T3 turned the resume cases and the AC1/AC2 cases red.
- AC5 (evidence): the operator's report in this session, 2026-10-06: in fresh desktop Code sessions, `Plan` and `Implement` both cleared the conversation and then ran the next step. The band showed only after a first message, which the T5 work-log line records as the desktop app's own behavior. The operator accepted the look.
- AC6 (evidence): README.md:185 and :202 say `Implement` and `Plan` run `/clear` and then their command. cairn/DESIGN.md:186 says they clear the conversation before they run. CHANGELOG.md:7, inside `## Unreleased`, has the entry "Plan and Implement clear the conversation first".
- AC7 (evidence): at fc61a0c, `scripts/tests` (397 tests), `hooks/tests` (174 tests), `claude plugin validate` on the plugin manifest (passed with warnings) and on the marketplace manifest (passed), and `claude plugin test .` (1287 pass) each exited 0.
- Gate: `cairn_validate.py` exited 0 with all checks passed. No principle changed, so `cairn_impact` was skipped. Profile gate: the verify checks passed at fc61a0c, the marketplace validate output has no `version` warning, and CHANGELOG `## Unreleased` has this change's entry with no milestone number.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: a `/clear` run that settles with no clear session end leaves `held` set, so the action Buttons do nothing until some session end — follow-up, row "Clear-then-run follow-ons (M221 review)". Dropping it at the settle breaks a host whose end follows the settle, and the probe covered only the desktop order.
- diff-bug #2: such a stale command runs at a later, unrelated `/clear` — follow-up, the same row (it follows from #1).
- diff-bug #3: a non-clear session end drops the held command with no word, against IP3 — fix now: the prompt box gets its command line and a toast says the session ended before `/clear`.
- diff-bug #4: a reload between the press and the end loses the command, and Scope names a row for it — follow-up, the same row.
- diff-bug #5: no test has the clear's session end arrive while its run is pending, the live order — fix now: a test with separate holds for the clear and the command.
- diff-bug #6: two quick presses can both pass `busy` before `heldRun` is set — follow-up, the same row (the race predates M221).
- diff-bug #7: a drawn `Resume` or `Review` whose next step became planning or implement clears the conversation — fix now: the press clears only when the drawn label is the next step's label. No test, because the kit presses the current drawing (as M212 noted for the step check).
- diff-bug #8: a clear that rejects after its end would fill `/clear` into the new conversation — reject (false): a clear that ended the session resolved in each probe run, and a refused clear ends no session.
- diff-bug #9: a pane press during a turn holds the command for the rest of the turn — follow-up, the same row.
- diff-bug #10: the held run's refusal path uses the ending session's handle, untested — reject (planned change): the held-command way runs from the `session.end` hook by design, and the live look ran the command through that handle. The refusal is `run`'s catch, which M212 AC3 tests.
- diff-bug #11: local `held` names in `dismiss`, `reconcile`, and `refresh` shadow the module value — fix now: renamed `heldRun`.
- diff-bug #12: the negative checks wait about 55 ms — reject (false): the planted defects at T3 turned these checks red.
- diff-bug #13: AC4 has no pane case, though the CHANGELOG names the pane — fix now: a pane refused-clear test.
- diff-bug #14: no test shows the Buttons free after a resume end — fix now: the resume cases press Status after.
- diff-bug #15: `CLEARS_FIRST` is untyped and copied in three places — fix now: it moved to pane.ts beside the label map. The test copies stay, written by hand, as an expectation independent of the code.
- diff-bug #16: the README idle paragraph omits the dead window and the refused command — fix now.
- diff-bug #17: the CHANGELOG omits the dead window and the other-end drop — fix now.
- diff-bug #18: DESIGN's "drops it too, so the refusal names `/clear`" states a wrong cause — fix now.
- diff-bug #19: DESIGN cites IP3 for consent, which IP3 does not say — fix now: the text now says the plan gate settled the IP3 point this way.
- diff-bug #20: the plan did not offer the `ip-touching` escalation — reject (planned change): the plan put the IP3 point to the operator at the question set, who chose consent by press. This is a plan-phase gap, shown at the merge question.
- diff-bug #21: two README lines run past the wrap width — reject (style).
- blame-history #1: a settled clear no longer frees the Buttons without a session end — follow-up, the same row (as diff-bug #1).
- blame-history #2: the held command is not re-read when it runs — follow-up, the same row's pane-turn item. In an idle session nothing changes the next step between the press and the end.
- blame-history #3: a pane press in a non-cairn turn queues a conversation-dropping `/clear` — follow-up, the same row.
- blame-history #4: the clear decision follows the re-read action, not the drawn label — fix now (as diff-bug #7).
- blame-history #5: the consent rests on labels that do not name the clear — reject (planned change): the plan gate chose the plain labels.
- blame-history #6: any clear end runs the held command, such as a typed `/clear` while the Button's waits — follow-up, the same row's pane-turn item (only a queued clear leaves that window).
- blame-history #7: the hook takes the held command after `next(e)` and four awaits — fix now: it takes it first.
- blame-history #8a: the M213 in-flight test asserts a second clear, not a freed Plan — reject (false): a freed Plan press runs `clear` first, so that entry is the freed press.
- blame-history #8b: no test makes the held command's run reject — reject (false): it runs through `run`, whose refusal M212 AC3 tests.
- blame-history #8c: `CLEARS_FIRST` copied as literals — fix now (as diff-bug #15).
- blame-history #9: the double-press race predates M221 and costs more now — follow-up, the same row.
- prior-review #1: a pane press while Claude works queues `/clear`, as the M218 and M219 rows note — follow-up, the same row.
- prior-review #2: a rejecting `next(e)` leaves `held` set — fix now (as blame-history #7). Its settle-without-end part is diff-bug #1.
- prior-review #3: the held command runs without the as-it-is-now re-read — follow-up (as blame-history #2).
- prior-review #4: `CLEARS_FIRST` defined three times — fix now (as diff-bug #15).
- prior-review #5: no test of a pane press in a non-cairn turn, or of a stale Clear press — follow-up: the first in the same row, the second already in "Clear button follow-ons (M216 review)".
- prior-review #6: `untilRuns` polls with 5 ms waits — reject (false): the existing hold tests use the same polling, and the plants turned the new checks red.
- Return floor: no finding shows a criterion failing, and the fix-now items are edge paths off the accepted live path, so status stays `review`.
