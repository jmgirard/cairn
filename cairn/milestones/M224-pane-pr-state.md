# M224: The pane shows each handed-off PR's review state

- **Status:** review
- **Priority:** normal
- **Depends on:** M223
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m224-pane-pr-state

## Goal

On request, the cairn pane shows the GitHub state of each blocked milestone's pull request and a Button for its next step.

## Scope

**In:** T1 is a probe. It checks that a `claude plugin test` case can
answer `$.process.run`, and that a desktop Code session can run `gh`
through `$.process.run`. The type file calls `$.process.run` "CLI only",
and the M191 archive once said that tests cannot fake it. The mod then
reads each Blocked line's PR with `gh pr view <url> --json
state,reviewDecision`. The URL names the PR's repo, so the call needs no
`--repo`. The reader keeps each row's PR URL beside its number (M223
keeps only the number), and M225 reads it too. Each line shows a state word and, for three states, a Button.
The Buttons follow the routes that `/milestone` gives a handed-off PR
(`skills/milestone/SKILL.md`, the blocked-with-a-PR bullet). The reads
happen at two moments: the pane's open, and a press of a `Refresh` Button
on the `Blocked` heading. Nothing reads on a schedule, because the operator does
not want repeating tasks. A failed read shows `unknown` and never breaks
the pane. README, DESIGN, and CHANGELOG describe the states and Buttons.

**Out:** The band does not change, because the plan gate kept the PR view
in the pane only. The mod writes nothing to GitHub and nothing under
`cairn/`. `/milestone` still owns status changes, such as `blocked` to
`done`. If T1 finds that tests cannot answer `$.process.run`, or that the
desktop app cannot run `gh`, implement takes the goal-wrong stop. The
unresolved threads and unanswered comments are M225 (planned 2026-10-08,
depends on M224), which also reads each OPEN PR with a GraphQL call.

## Acceptance criteria

- [x] AC1: For each Blocked line with a PR number, the mod reads the PR
      with `gh pr view <url> --json state,reviewDecision` through
      `$.process.run`. The line shows one state word. MERGED shows
      `merged`, and CLOSED shows `closed`. OPEN with CHANGES_REQUESTED
      shows `changes requested`, and OPEN with APPROVED shows `approved`.
      OPEN with REVIEW_REQUIRED, an empty decision, or no decision shows
      `in review`. A line not yet read shows no state word and no Button.
      Register tests answer the `gh` call with each of these seven shapes,
      one case each, and one case runs before any read.
- [x] AC2: A `merged` line carries a `Finish` Button that runs
      `/cairn:milestone-review <id>`. A `changes requested` line carries a
      `Revise` Button that runs `/cairn:milestone-implement <id>`. A
      `closed` line carries a `Check` Button that runs `/cairn:milestone`.
      No Button runs `/clear` first. `approved` and `in review` lines carry
      no Button. Register tests press each Button and assert the command it
      submits, and find no Button on the other two lines.
- [x] AC3: The mod reads the PR states when the pane opens and at a press
      of the `Blocked` heading's `Refresh` Button. The pane opens by the
      `/cairn-pane` command, by the band's open button, or by the
      session-start reopen (M222), and each open reads the states once.
      The mod makes no `$.clock.after`, `$.clock.every`, or `$.clock.sleep`
      call, and it runs no `gh` call at a `turn.complete`. Register tests
      cover each of the four triggers and a turn-complete case. Each of
      these five tests records no such clock call.
- [x] AC4: A line shows `unknown` and no Button in four cases. In the
      first two, the `gh` call rejects or exits non-zero. In the other two,
      it prints text that is not JSON, or JSON whose `state` is not MERGED,
      CLOSED, or OPEN.
      The other lines draw as before, and the hook does not throw. One
      register test covers each case.
- [x] AC5: The operator looks at the desktop app's docked pane in the
      guest-mode insight checkout (`~/github/insight`). Each handed-off PR
      shows the state word read from GitHub, and its Button where AC2 gives
      one. The operator accepts this at the merge question.
- [x] AC6: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the state words, the three
      line Buttons, the `Refresh` Button, and when the states are read.
      Each claim is read against the code at implement time.
- [x] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T2, T4
- AC3 → T2, T3
- AC4 → T2, T3, T4
- AC5 → T1, T6
- AC6 → T5
- AC7 → T4, T5

## Tasks

- [x] T1: Probe. First, a `claude plugin test` case answers
      `$.process.run` with `{ value: { exitCode, stdout, stderr } }` and
      with a throw (LESSONS M191). Second, a throwaway mod in the session's
      hot-reload folder runs `gh pr view` on one insight PR. It logs the
      result and `PATH` to a file in `.git/info/exclude` (LESSONS M201,
      M205). The operator enables hot reload. Write one work-log line with
      both results. If either fails, take the goal-wrong stop.
- [x] T2: Tests first. Add the AC1 to AC4 register cases, with a
      `process.run` answer per case and a clock-call recorder. Make sure
      that they fail against the M223 code.
- [x] T3: Add the read in `register.tsx`: one `$.process.run` per
      numbered line, run in parallel with a timeout. The pane's open paths
      call it (`command.run` near line 172, the band's open button, and
      `reopen`), and so does the `Refresh` press. Keep the states in their own
      atom with its own shape tag (LESSONS M193, M210). Map each result to
      a state word in a pure function that the tests call.
- [x] T4: Draw the state word and the line Buttons in `pane.ts` and
      `register.tsx`, with the Box widths of LESSONS M194. Reuse the
      Status Button's submit path for the three commands. Run `verify`.
- [x] T5: Describe the states, Buttons, and reads in README.md's "The cairn
      pane", in `cairn/DESIGN.md`, and in CHANGELOG.md's Unreleased
      section. Run `verify`.
- [x] T6: Live look in a new desktop Code session in `~/github/insight`
      (LESSONS M195, M213). Press `Refresh`. Insight has no line that
      carries a Button (amended at T6).

## Work log

- 2026-10-08: created by /milestone-plan.
- 2026-10-08: criteria audit (full mode, fresh Opus reader) over M223 and M224: 12 findings, all taken toward the narrower promise. In M224, the probe became T1, and AC1 covers each empty decision form and a line not yet read. No Button clears first, as the Review and Resume Buttons keep the conversation. AC4 counts a rejection once and adds JSON with an unknown `state`. AC6 names the `Refresh` Button and the claim read.
- 2026-10-08: question set: how the pane learns each PR's state — live from GitHub, with no timer and no scheduled read. The operator does not want repeating tasks.
- 2026-10-08: question set: live look in the desktop app at review in `~/github/insight` — granted, with read-only `gh` calls.
- 2026-10-08: question set: a band note for a PR that needs the operator — declined, pane only.
- 2026-10-08: AC3 re-audit after the answers removed the timer: 3 findings, all taken. Every trigger test records no clock call, `$.clock.sleep` is banned too, and one open reads once. Then the plan dropped the read at a session start with the pane closed, because nobody sees it. The four triggers are all pane opens or a press.
- 2026-10-08: plan chose `gh` reads in the mod over a Button that runs `/milestone`, because a model turn costs tokens and time. Falsified by T1 finding that the desktop app cannot run `gh` from a mod.
- 2026-10-08: plan chose reads on demand over a 15-minute timer, at the operator's word. Falsified by the operator asking for the pane to notice changes on its own.
- 2026-10-08: plan amendment before start (M223 merge question): the operator asked for unresolved threads and unanswered comments per PR. They became M225, which depends on this milestone. Scope In now keeps each row's PR URL for both reads, and Scope Out points to M225. The criteria do not change.
- 2026-10-08: started implement on branch m224-pane-pr-state. The untracked `cairn-probe.log` and `tsconfig.json` at the repo root are not this milestone's and stay unstaged.
- 2026-10-08: T1 probe, test half: a `claude plugin test` hook on `process.run` answers the mod's call with `{ value: { exitCode, stdout, stderr } }`, and the mod sees the argv. A hook that throws is skipped, so the mod's call rejects with "no implementation for process.run", as it does with no hook. The test's own `$` has no `process` noun, so the call must come from the mod. The probe code was removed.
- 2026-10-08: T1 probe, desktop half: a throwaway mod `m224probe` in this session's hot-reload folder logs `PATH` and `gh pr view` on insight PR 1250 (bare `gh` and `/opt/homebrew/bin/gh`) to `m224-probe.log`, which `.git/info/exclude` lists. Waiting for the operator to enable hot reload.
- 2026-10-08: T1 done. In the desktop session, the probe mod's `$.process.run` ran bare `gh` and `/opt/homebrew/bin/gh` at two session starts. Both exited 0 with `{"reviewDecision":"","state":"OPEN"}` for insight PR 1250. The mod's `PATH` holds `/opt/homebrew/bin`, so the mod calls bare `gh`. Both probe halves passed, so no goal-wrong stop. The probe mod was deleted.
- 2026-10-08: T2 implementation choice: each blocked row keeps its PR URL as `url` beside `pr`. `cairn_next.blocked` gains it too, through a new `pr_url`, so the fixtures' expected.json stays the one oracle for both readers.
- 2026-10-08: T2 tests written: 21 new register cases fail against the M223 code, and the two silent cases (a line not yet read, a turn end) pass. The Python URL cases pass with the new `pr_url`. Unticked until `verify` is green after T3.
- 2026-10-08: T3 done. `readPrs` in register.tsx runs one `gh pr view <url> --json state,reviewDecision` per distinct URL, side by side, with a 15 s timeout each. The command, the band's open button, and the reopen call it after their open, and so does the Refresh press after a file refresh. A guard skips a read that starts while one runs. The words go to a new `prs` atom (tag `prs-1`), keyed by URL, and the pane atom's tag moved to `pane-4` for the URL. `prWord` in pane.ts maps a result to a word.
- 2026-10-08: T4 done. A blocked line's tail gains the word after its number, colored by the review color for merged and approved, the warning key for changes requested, gray otherwise. The line's Button sits in its own no-shrink Box, as the Next line's do, and its key ends in the milestone id. A press reads the word as it is now and runs its command through `run`, the Status path, with no `/clear`. It checks only that no run is in flight, so it does not wait for a cairn skill's step to end. The M219 "no other Button" case now allows the Blocked heading's Refresh. `verify` green: 401 script tests, 174 hook tests, both validates, 1465 mod tests.
- 2026-10-08: T5 done. README's pane section gains a paragraph and a table of the six words, their GitHub states, and their Buttons. DESIGN's pane text gains `readPrs`, `prWord`, and `PR_BUTTON`, and CHANGELOG's Unreleased section gains one entry. Each claim was written from this session's read of pane.ts and register.tsx. `verify` green, `cairn_validate` all checks passed.
- 2026-10-08: minor amendment to T6: insight's blocked rows are M006 (PR 1250, OPEN, empty decision, so `in review` and no Button) and M007 (no URL), and M005 is done. So the live look has no line Button to press. T6 now presses `Refresh` only, and the register tests stay the evidence for the line Buttons. AC5 asks for a Button only where AC2 gives one, so it does not change.
- 2026-10-08: claim audit: 46 claims read, 3 corrected — README.md, cairn/DESIGN.md, hooks/status/register.tsx
- 2026-10-08: T6 live look: the operator ran `/cairn-pane` in their own insight desktop session, which had loaded this branch's mod, in place of a new session. The M006 line ends `#1250  in review`, the word `gh` gives for PR 1250 (OPEN, empty decision). The operator did not report a `Refresh` press, so the merge question asks for it.
- 2026-10-08: review: three fresh reviewers (diff-bug, blame-history, prior-review). 8 findings fixed on the branch, 4 sent to the candidate row "Pane PR-state edges (M224 review)", 6 rejected, all logged in the Review section. No return.
- 2026-10-08: step-7 approval: m224-pane-pr-state approved for merge. The operator chose merge over checking `Refresh` first, which accepts the live look with no `Refresh` press seen.

## Decisions

## Review

Review head 64a5f56 (plus this record). Default branch unchanged since the cut (origin/main 5f2d674).

- AC1: `claude plugin test .` on 64a5f56, describe "each blocked line shows its pull request state (M224 AC1)": 8 pass, 0 fail. Seven cases answer `gh` with MERGED, CLOSED, OPEN with CHANGES_REQUESTED, APPROVED, REVIEW_REQUIRED, an empty decision, and no decision. Each asserts the argv `gh pr view <url> --json state,reviewDecision` and the line text with the hand-written word. One case before any read finds no word and no Button.
- AC2: same run, describe "the merged, changes-requested, and closed lines carry a Button (M224 AC2)": 6 pass, 0 fail. Finish, Revise, and Check presses submit exactly `cairn:milestone-review M111`, `cairn:milestone-implement M111`, and `cairn:milestone` with no `clear` before them. The `approved` and `in review` lines carry no Button, with their exact text. A review-added case shows a press during a running cairn skill runs nothing, and it fails with the step check removed (planted on the branch, then restored).
- AC3: same run, the AC3 describes: 7 pass, 0 fail. The `/cairn-pane` command, the band's open button, the session-start reopen, and the Refresh press each record exactly one `gh` call for the one URL, and a turn-complete case records none. Each of these five records no `clock.sleep`, `clock.after`, or `clock.every` call. Two review-added cases show a close and a refused open run no `gh`. `grep -n "\$.clock" hooks/status/*.ts*` finds no call in the mod.
- AC4: same run, describe "a failed read shows `unknown` and no Button (M224 AC4)": 4 pass, 0 fail. On blocked-prs, M101's call rejects, exits 1, prints non-JSON text, or prints JSON with state DRAFT. M101 shows `#12  unknown` with no Button, M102 and M104 still read `merged` with M102's Finish, M103 and M105 draw as before, and the command returns `cairn pane opened`, so the hook did not throw.
- AC5: the operator looked at the docked pane in their insight desktop session (work log, T6). The M006 line ends `#1250  in review`, which matches `gh pr view` for PR 1250 at review time (OPEN, empty decision). Insight has no line that AC2 gives a Button. Acceptance is asked at the merge question, and the box waits for it. The operator accepted it at the merge question on 2026-10-08.
- AC6: README "The cairn pane" gains the read paragraph and the six-word table, DESIGN's pane text names `readPrs`, `prWord`, `PR_BUTTON`, the four reads, and the Refresh Button, and CHANGELOG Unreleased gains one entry naming the words, the three line Buttons, Refresh, and when the states are read, with no milestone number. The implement-time claim audit read 46 claims and corrected 3 (work log), and the review fixes rewrote the two DESIGN sentences they changed.
- AC7: on 64a5f56, every `verify` command exited 0. `scripts/tests` ran 401 tests, OK with 21 skipped. `hooks/tests` ran 174, OK. Both `claude plugin validate` runs passed with warnings, and `claude plugin test .` ran 1469 pass, 0 fail.
- Gate: `cairn_validate` exit 0, all checks passed. The marketplace validate shows no `plugins[N].version` warning. CHANGELOG has the entry. No IP or GP changed, so `cairn_impact` is skipped. Coverage is complete per `cairn_validate`.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: line Buttons run while a cairn skill runs — fix now, fixed d1f0b44 (also blame-history #1, prior-review #1)
- diff-bug #2: an in-process `/clear` empties the words of a pane that stays open — follow-up, row "Pane PR-state edges (M224 review)" (also blame-history #2)
- diff-bug #3: the in-flight guard drops a read started during another — fix now, fixed 64a5f56 (newest read writes, every read runs)
- diff-bug #4: `/cairn-pane` and the reopen wait on `gh` before they return — follow-up, same row (also blame-history #3, prior-review #2)
- diff-bug #5: the approved and in-review no-Button case did not check the word — fix now, fixed 64a5f56
- diff-bug #6: untested paths: close, refused open, busy press, changed-word press, read race — fix now for close and refused open, fixed 64a5f56, and follow-up for the rest, same row
- diff-bug #7: no test calls `prWord` directly, as T3 says — fix now, fixed 64a5f56 (table test)
- diff-bug #8: the word list is typed in two places — fix now, fixed 64a5f56 (`PrWord = CairnPrWord`)
- diff-bug #9: README and CHANGELOG leave out the dropped read — fix now, fixed 64a5f56 by diff-bug #3's fix, so the claims hold
- diff-bug #10: Refresh shows only while a row has a PR URL — reject, planned change: Refresh reads PR states, and with no URL there is nothing to read
- diff-bug #11: Button keys assume unique ids — reject, false: ROADMAP ids are unique by the ID rule, and M223's `blocked-<id>` line keys rest on the same fact
- diff-bug #12: the clock recorder has no positive control — follow-up, same row
- blame-history #4: a reopen that is not placed still reads — reject, planned change: AC3 has each open read, and the waiting pane draws the words once placed
- blame-history #5: the M219 no-other-Button case builds Refresh from fixture data — reject, false: the fixture's `url` comes from expected.json, held to `cairn_next.py`, not from the pane code. The running-step case it asked for is added (diff-bug #1)
- prior-review #3: the read has no run number, so a late read can write — fix now, fixed 64a5f56 (`prReads`). The hang part is rejected, false: the types say a call still running at its timeout rejects
- prior-review #4: the `BLOCKED_COMMANDS` comment about `/clear` can confuse — reject, style: the comment is true
