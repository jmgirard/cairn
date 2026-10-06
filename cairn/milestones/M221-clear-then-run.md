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
