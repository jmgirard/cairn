<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M328: Wait for CI without stopping the session

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes how `/milestone-review` and `/hotfix` wait on CI before a merge in every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m328-ci-arm-and-wake   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A merge's CI wait arms a background watch and ends the turn, and the
session resumes by itself when CI ends, so the user no longer reruns the
skill after a long CI run.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the tracking-rules wait rule for a merge's CI wait (arm, wake
line, close block, wake handling, stop-point and one-watcher clauses, the
early-stop clause, the stop list); the merge waits of `/milestone-review`
step 8 (primary and companion arm) and `/hotfix` step 6; a live probe in
`jmgirard/cairn-wait-lab`; the README, PROFILE, CI-line, and CHANGELOG
text that describes the wait; a superseding D-entry; the wait-rule prose
guard.

**Out:**
- Waking on review comments or merge conflicts: not planned. The user
  chose CI results only at the plan question set; the Copilot round keeps
  handling Copilot's comments.
- `/cairn-release`'s slow local checks keep today's rule, since they are
  local commands and not a PR's CI.
- Turning on the desktop app's own PR monitor: never done by cairn (AC4).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: The wait rule in `skills/shared/tracking-rules.md` ("Waiting on
      CI and background work") states the merge CI wait in four steps.
      (a) The session arms `gh pr checks <N> --watch --fail-fast` as a Bash
      `run_in_background` task. (b) After the watch exits, that task prints
      one wake line that names the PR number, the exit status of the watch,
      and the resume command of the invoking skill. (c) The session ends the
      turn with a close block. Its CI line says that the session resumes by
      itself when CI ends, and its fenced next command is the resume
      command, for a host where no wake comes. (d) At the completion
      notification of that task, the session reads the check state with
      `gh pr checks <N>` and the merge state with
      `gh pr view <N> --json state`. If any check failed, it takes the
      red-CI path. Otherwise, if a check is pending, it arms the watch
      again. If every check passed, it goes on to the merge. A PR that is no
      longer open, or one that reports no checks, follows the rule's resume
      and no-checks clauses. The rule prescribes no foreground
      `gh pr checks --watch` for a merge wait, and its stop list and timeout
      clause name no ceiling stop for one.
- [ ] AC2: Two clauses name the armed merge CI watch of AC1 as the one
      watcher that a turn can end on: the stop-point clause of the wait rule
      and the early-stop clause in "Question gates and phase closes". The
      stop-point clause still bars a watcher at a commit. It states that a
      `/clear` while the merge watch is armed is safe. It also states what a
      session does with a wake line from a watch that it did not arm: it
      shows the user the line and its resume command, and it runs nothing.
- [ ] AC3: Each merge wait in `skills/milestone-review/SKILL.md` step 8,
      the primary merge and the companion arm, and in
      `skills/hotfix/SKILL.md` step 6 states the wait of AC1 and names its
      own resume command: `/milestone-review M<NNN>`, or `/hotfix` with the
      PR reference. No line in those two steps that
      `git grep -nE "gh pr checks|ceiling|TaskStop|moved to the background" -- skills/milestone-review/SKILL.md skills/hotfix/SKILL.md`
      lists describes a foreground or ceiling-bound merge wait.
- [ ] AC4: The one-watcher clause of the wait rule names one exception: a
      host app's PR monitor that the user turned on, such as the desktop
      app's Auto-fix. The rule states that a session never turns such a
      monitor on for a merge wait, and that a red result for a head commit
      the session already acted on is not acted on again.
- [ ] AC5: In `jmgirard/cairn-wait-lab`, a Claude Code desktop session arms
      the watch as AC1 states and ends its turn. When the run ends, the
      session starts again with no user message and runs step (d) of AC1,
      taking the branch that matches the run. This occurs once on a green
      run longer than 600 s and once on a red run whose failure lands after
      the turn ended. The wait rule cites the rows of
      `cairn/references/wait-mechanisms.md` that record these wakes, and it
      names the desktop app as the host observed.
- [ ] AC6: Each line that
      `git grep -nE "times out|ceiling|TaskStop|gh pr checks|CI wait|waits on CI" -- README.md skills/*/SKILL.md skills/shared/tracking-rules.md cairn/PROFILE.md`
      lists, and that describes the CI wait of a merge, agrees with AC1 and
      AC2. The Unreleased section of `CHANGELOG.md` has an entry for the
      change.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T2
- AC2 → T2
- AC3 → T3, T4
- AC4 → T2
- AC5 → T1, T2
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Live probe (granted at the question set). In
      `jmgirard/cairn-wait-lab`, make the red `gate` job fail after about
      3 minutes, not 6 s. From a desktop session, arm the AC1 watch on a
      green run that includes the 720 s job, and on a late red run; end the
      turn each time. If no wake arrives within a few minutes, the user types
      "continue". Record rows W24 onward in `wait-mechanisms.md`: run URL,
      wake line, what the woken turn did. No idle wake → goal-wrong stop,
      close block with `/milestone-plan`.
- [x] T2: Rewrite the wait rule (`tracking-rules.md:396-415`): the CI-checks
      sentence, the one-watcher exception, the stop-point clause, the
      On-timeout clause for merge waits, the stop list's "a CI wait that
      times out", the early-stop clause, and the close block's list of four
      timeout-stop sites. Write the D-entry that supersedes D-128's
      foreground CI clause and stop-point clause and narrows its one-watcher
      clause, and annotates D-130. Diff every removed sentence against main.
- [ ] T3: `/milestone-review` step 8, primary and companion arm, and its
      session-start resume prose about a stopped CI wait (~line 79, ~750).
- [ ] T4: `/hotfix` step 6 and its resume prose (~lines 120, 208).
- [ ] T5: README's two stop lists (~709, ~892), the implement-stop CI line
      (`milestone-implement` ~335), `cairn/PROFILE.md:68` and its
      `skills/shared/profiles/` copy, the `/cairn-release` site, and a
      CHANGELOG entry. Run the AC6 grep.
- [ ] T6: Update `skills/tests/test_wait_rule.py` and its
      `test_mutation_harness.py` entries; re-seed the rulebook-mass baseline
      in its three places. Run both gating suites, `claude plugin validate`,
      and the hand-run `skills/tests`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-31: created by /milestone-plan.
- 2026-10-31: tier check: milestone — changes skill behavior and a recorded decision (D-128).
- 2026-10-31: idea vet: gap — a wake line reaching a session after `/clear` (reading taken: show the line and command, run nothing); gap — which events wake (sent to the set: CI results only); gap — the desktop app's PR monitor (sent to the set: cairn's own watch); no flaw.
- 2026-10-31: lessons used: 2026-07-16 (M56+M65), 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-17 (M149), 2026-08-22 (M152), 2026-10-25 (M323).
- 2026-10-31: collision: D-128 (stop-point, foreground CI, and one-watcher clauses) superseded or narrowed by T2's D-entry; D-130 annotated (its resume route stays as the no-wake fallback); D-138 unchanged; no ROADMAP row or archive milestone overlaps. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-31: source: t3code's PR watcher (`apps/server/src/orchestration-v2/pullRequestWatch.ts`, pingdotgg/t3code at 15fe2832), read in this session.
- 2026-10-31: question set: wake events — CI results only.
- 2026-10-31: question set: host app PR monitor — cairn arms its own watch in every host and never turns the app monitor on.
- 2026-10-31: question set: live probe — granted: push to jmgirard/cairn-wait-lab, edit its workflow, end turns on purpose; the user types "continue" if no wake comes.
- 2026-10-31: criteria audit (full mode, fresh Opus): 9 findings, all fixed — (d) branch order and closed/no-checks PRs; close block with resume command; `/clear` stated safe; one-watcher exception and head-commit dedupe; probe over 600 s green and late red; woken turn runs (d); rule cites ledger rows; AC3 and AC6 grep patterns widened, PROFILE added.
- 2026-10-31: plan gate chose always arming over a foreground wait that arms only at the ceiling because one mechanism is simpler to state and to resume; falsified by a wake observed lost or late where a foreground wait would have caught the result.
- 2026-10-31: plan gate chose Bash `run_in_background` over a Monitor with `timeout_ms` because `gh --watch` exits on its own and a Monitor dies at one hour at most; falsified by an armed watch observed running past an hour on a hung run.
- 2026-10-31: implement started on branch m328-ci-arm-and-wake; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-31: question set (implement stop): jmgirard/cairn-wait-lab no longer existed — user granted creating it again as a private repo with one workflow and two draft PRs.
- 2026-10-31: T1 armed: lab PR #1 (green, 720 s job, run 41215428891) and PR #2 (gate fails after 180 s, run 41215432313), each `gh pr checks <N> --watch --fail-fast` in `run_in_background` with a wake line; turn ended at ~15:34 UTC to observe idle wakes.
- 2026-10-31: T1 red wake: the idle session was started with no user message by PR #2's task notification (task exit 0; wake line "watch exited 1 at 15:36:54"); step (d) read `gate` fail and `long` pending, so the failed check won over the pending one (red path); turn ended again for PR #1.
- 2026-10-31: T1 done: green wake on PR #1 (run 12 min 5 s, watch exited 0 at 15:45:47, idle session started with no user message, step (d) read both checks pass → merge branch); rows W24–W26 added to `wait-mechanisms.md`, W26 recording that the task's exit code is the `echo`'s, so the rule reads the status from the wake line; hand-run `skills/tests` green (977).
- 2026-10-31: T2 done: wait rule gains the four-step merge CI wait, the host-monitor exception to one watcher per wait, the stop-point exception with the `/clear` and unarmed-wake-line handling; the ceiling note moved to the local-command clause; On timeout now names local commands and Monitors; stop list reads "a local check that times out"; early-stop clause names the armed turn end; CI-line site list updated. D-229 written (appended by shell heredoc against the Write/Edit rule; content checked). Removed lines diffed against main: only the foreground CI clause and the old site list went.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
