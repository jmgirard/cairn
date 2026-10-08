# M224: The pane shows each handed-off PR's review state

- **Status:** in-progress
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

- [ ] AC1: For each Blocked line with a PR number, the mod reads the PR
      with `gh pr view <url> --json state,reviewDecision` through
      `$.process.run`. The line shows one state word. MERGED shows
      `merged`, and CLOSED shows `closed`. OPEN with CHANGES_REQUESTED
      shows `changes requested`, and OPEN with APPROVED shows `approved`.
      OPEN with REVIEW_REQUIRED, an empty decision, or no decision shows
      `in review`. A line not yet read shows no state word and no Button.
      Register tests answer the `gh` call with each of these seven shapes,
      one case each, and one case runs before any read.
- [ ] AC2: A `merged` line carries a `Finish` Button that runs
      `/cairn:milestone-review <id>`. A `changes requested` line carries a
      `Revise` Button that runs `/cairn:milestone-implement <id>`. A
      `closed` line carries a `Check` Button that runs `/cairn:milestone`.
      No Button runs `/clear` first. `approved` and `in review` lines carry
      no Button. Register tests press each Button and assert the command it
      submits, and find no Button on the other two lines.
- [ ] AC3: The mod reads the PR states when the pane opens and at a press
      of the `Blocked` heading's `Refresh` Button. The pane opens by the
      `/cairn-pane` command, by the band's open button, or by the
      session-start reopen (M222), and each open reads the states once.
      The mod makes no `$.clock.after`, `$.clock.every`, or `$.clock.sleep`
      call, and it runs no `gh` call at a `turn.complete`. Register tests
      cover each of the four triggers and a turn-complete case. Each of
      these five tests records no such clock call.
- [ ] AC4: A line shows `unknown` and no Button in four cases. In the
      first two, the `gh` call rejects or exits non-zero. In the other two,
      it prints text that is not JSON, or JSON whose `state` is not MERGED,
      CLOSED, or OPEN.
      The other lines draw as before, and the hook does not throw. One
      register test covers each case.
- [ ] AC5: The operator looks at the desktop app's docked pane in the
      guest-mode insight checkout (`~/github/insight`). Each handed-off PR
      shows the state word read from GitHub, and its Button where AC2 gives
      one. The operator accepts this at the merge question.
- [ ] AC6: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the state words, the three
      line Buttons, the `Refresh` Button, and when the states are read.
      Each claim is read against the code at implement time.
- [ ] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T2, T4
- AC3 → T2, T3
- AC4 → T2, T3, T4
- AC5 → T1, T6
- AC6 → T5
- AC7 → T4, T5

## Tasks

- [ ] T1: Probe. First, a `claude plugin test` case answers
      `$.process.run` with `{ value: { exitCode, stdout, stderr } }` and
      with a throw (LESSONS M191). Second, a throwaway mod in the session's
      hot-reload folder runs `gh pr view` on one insight PR. It logs the
      result and `PATH` to a file in `.git/info/exclude` (LESSONS M201,
      M205). The operator enables hot reload. Write one work-log line with
      both results. If either fails, take the goal-wrong stop.
- [ ] T2: Tests first. Add the AC1 to AC4 register cases, with a
      `process.run` answer per case and a clock-call recorder. Make sure
      that they fail against the M223 code.
- [ ] T3: Add the read in `register.tsx`: one `$.process.run` per
      numbered line, run in parallel with a timeout. The pane's open paths
      call it (`command.run` near line 172, the band's open button, and
      `reopen`), and so does the `Refresh` press. Keep the states in their own
      atom with its own shape tag (LESSONS M193, M210). Map each result to
      a state word in a pure function that the tests call.
- [ ] T4: Draw the state word and the line Buttons in `pane.ts` and
      `register.tsx`, with the Box widths of LESSONS M194. Reuse the
      Status Button's submit path for the three commands. Run `verify`.
- [ ] T5: Describe the states, Buttons, and reads in README.md's "The cairn
      pane", in `cairn/DESIGN.md`, and in CHANGELOG.md's Unreleased
      section. Run `verify`.
- [ ] T6: Live look in a new desktop Code session in `~/github/insight`
      (LESSONS M195, M213). Press `Refresh` and one line Button.

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

## Decisions

## Review
