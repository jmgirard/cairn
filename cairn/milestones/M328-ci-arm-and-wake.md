<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M328: Wait for CI without stopping the session

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes how `/milestone-review` and `/hotfix` wait on CI before a merge in every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m328-ci-arm-and-wake, https://github.com/jmgirard/cairn/pull/342   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
- A time bound on the watch: none; a check that never settles is a
  DESIGN.md Known issue (descoped at the thrash stop, D-231).
- The smaller merge-wait edge cases from review pass 3: candidate row
  "Close the merge CI wait's edge cases".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: The wait rule in `skills/shared/tracking-rules.md` ("Waiting on CI and background work") states the
      merge CI wait in four steps. (a) The session arms `gh pr checks <N> --watch --fail-fast` as a Bash
      `run_in_background` task. (b) After the watch exits, that task prints one wake line that names the PR number,
      the exit status of the watch, and the resume command of the invoking skill. (c) The session ends the turn with
      a close block. Its CI line says that the session resumes by itself when CI ends, and its fenced next command
      is the resume command, for a host where no wake comes. (d) At the completion notification of that task, the
      session reads the check state with `gh pr checks <N>` and the merge state with `gh pr view <N> --json state`.
      If any check failed, it takes the red-CI path. Otherwise, if a check is pending, it arms the watch again. If
      every check passed, it goes on to the merge. A PR that is no longer open, or one that reports no checks,
      follows the rule's resume and no-checks clauses. The rule prescribes no foreground `gh pr checks --watch` for
      a merge wait, and its stop list and timeout clause name no ceiling stop for one.
- [x] AC2: Two clauses name the armed merge CI watch of AC1 as the one watcher that a turn can end on: the
      stop-point clause of the wait rule and the early-stop clause in "Question gates and phase closes". The
      stop-point clause still bars a watcher at a commit. It states that a `/clear` while the merge watch is armed
      is safe. It also states what a session does with a wake line from a watch that it did not arm: it shows the
      user the line and its resume command, and it runs nothing.
- [x] AC3: Each merge wait in `skills/milestone-review/SKILL.md` step 8, the primary merge and the companion arm,
      and in `skills/hotfix/SKILL.md` step 6 states the wait of AC1 and names its own resume command:
      `/milestone-review M<NNN>`, or `/hotfix` with the PR reference. No line in those two steps that
      `git grep -nE "gh pr checks|ceiling|TaskStop|moved to the background" -- skills/milestone-review/SKILL.md skills/hotfix/SKILL.md`
      lists describes a foreground or ceiling-bound merge wait.
- [x] AC4: The one-watcher clause of the wait rule names one exception: a host app's PR monitor that the user
      turned on, such as the desktop app's Auto-fix. The rule states that a session never turns such a monitor on
      for a merge wait, and that a red result for a head commit the session already acted on is not acted on again.
- [x] AC5: In `jmgirard/cairn-wait-lab`, a Claude Code desktop session arms the watch as AC1 states and ends its
      turn. When the run ends, the session starts again with no user message and runs step (d) of AC1, taking the
      branch that matches the run. This occurs once on a green run longer than 600 s and once on a red run whose
      failure lands after the turn ended. The wait rule cites the rows of `cairn/references/wait-mechanisms.md`
      that record these wakes, and it names the desktop app as the host observed.
- [x] AC6: Each line that
      `git grep -nE "times out|ceiling|TaskStop|gh pr checks|CI wait|waits on CI" -- README.md skills/*/SKILL.md skills/shared/tracking-rules.md cairn/PROFILE.md`
      lists, and that describes the CI wait of a merge, agrees with AC1 and AC2. The Unreleased section of
      `CHANGELOG.md` has an entry for the change.

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
- [x] T3: `/milestone-review` step 8, primary and companion arm, and its
      session-start resume prose about a stopped CI wait (~line 79, ~750).
- [x] T4: `/hotfix` step 6 and its resume prose (~lines 120, 208).
- [x] T5: README's two stop lists (~709, ~892), the implement-stop CI line
      (`milestone-implement` ~335), `cairn/PROFILE.md:68` and its
      `skills/shared/profiles/` copy, the `/cairn-release` site, and a
      CHANGELOG entry. Run the AC6 grep.
- [x] T6: Update `skills/tests/test_wait_rule.py` and its
      `test_mutation_harness.py` entries; re-seed the rulebook-mass baseline
      in its three places. Run both gating suites, `claude plugin validate`,
      and the hand-run `skills/tests`.
- [x] T7: Review return 1: make the stop-point clause state that a
      `/clear` while the merge watch is armed is safe, keeping the W20 note
      that its notification's delivery is unobserved.
- [x] T8: Review return 2: in the wait rule and both skill sites, read
      checks first and arm only while one is pending; bound the watch at
      one hour; check the head before re-arming; count skipped checks as
      passed and stop on a failed read; stop an armed watch on a typed
      resume; have a wake off the milestone branch run nothing; name the
      desktop app in the CI line and the armed close's wait note; add the
      two stops to the stop list; fix the W20 wording, docstrings, the
      CHANGELOG line, and the reference page's implications.
- [x] T9: Descope at the thrash stop: remove the `perl` bound and the 142
      handling from the rule and both sites; stop at the wake on a moved
      head or `CHANGES_REQUESTED` before any fix, re-arm, or merge; write
      D-231; file the edge-case row; propose the known issue; re-pin tests.

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
- 2026-10-31: T3, T4 done: `/milestone-review` step 8 (primary and companion arm) and `/hotfix` step 6 arm the watch with a one-line command printing the wake line and its resume command, end the turn with a close block naming it, and act at the notification; the ceiling and TaskStop text left both sites; resume prose names "a CI wait whose wake never came". `test_resume_routing` updated for that wording; two mutation blocks kept on one line; hand-run `skills/tests` green (977).
- 2026-10-31: T5 done: README's two stop lists now say red CI it cannot fix, and that a merge's CI wait resumes by itself; CHANGELOG Unreleased entry added. AC6 sweep: `cairn/PROFILE.md:68` (no-CI note), `milestone-implement:335` (waits on CI at its merge step), hotfix 194/208/217 (marker resume, step 6's CI wait), `milestone:167` (status read) still agree; `/cairn-release` site is local checks (Out); `skills/shared/profiles/` has no copy of the no-CI line.
- 2026-10-31: T6 done: `test_wait_rule.py` gains five pins (merge wait arms in the background, failed before pending, host-monitor exception, armed turn-end exception, unarmed wake line runs nothing), each registered in the mutation table and red when blanked; rulebook baseline re-seeded to 872 lines / 86,398 bytes in `milestone/SKILL.md` and its two pins. verify: scripts 446 OK, hooks 210 OK, plugin and marketplace validate exit 0 (warnings are the untracked `cairn-probe.log`/`tsconfig.json`), plugin test 2466 pass; hand-run skills/tests 982 OK; cairn_validate green.
- 2026-10-31: claim audit: 52 claims read, 8 corrected — skills/hotfix/SKILL.md (red path defined: fix, then step 1's walk and approval again, or stop; resume wording), README.md (desktop-only wake, resume command elsewhere), CHANGELOG.md (red wording, "to resume", "can get"), skills/shared/tracking-rules.md (red ends at first failed check, W2/W24; `/clear` cites W20 and marks delivery unobserved; moved-head check), skills/milestone-review/SKILL.md (CI line says typing the command re-poses approval; a head moved by someone else since approval merges nothing). Baseline re-seeded to 875 lines / 86,622 bytes; skills/tests 982 OK, scripts and hooks suites, both validates, cairn_validate green; plugin test last run at T6 (no `hooks/` change since).
- 2026-10-31: review return 1: AC2 — the stop-point clause says a `/clear` while the merge watch is armed "loses nothing", but AC2 requires it to state that such a `/clear` is safe; review ticks were written by a `python3` script against the Write/Edit rule.
- 2026-10-31: T7 added for review return 1 (minor amendment) and done: the stop-point clause now reads a `/clear` while armed "is safe and loses nothing", W20 note kept; baseline re-seeded to 875 lines / 86,634 bytes; skills/tests 982 OK, scripts and hooks suites, both validates exit 0; status back to review.
- 2026-10-31: review return 2: load-bearing defects in the merge wait from pass 2's lenses (diff-bug #1–#9, blame-history #1–#3, prior-review #1, ripple #1/#5/#7) — a second watcher on typed resume, no rule for a watch that exits before the turn ends, a wake that can merge mid-other-work, no branch for skipped checks or a failed read, no bound on a watch that never settles, re-arm before the head check, the moved-head stop off the stop list, host-unconditional CI line, overstated W20.
- 2026-10-31: T8 added for review return 2 (minor amendment) and done: the merge wait reads `gh pr checks` before arming and arms only while a check is pending; the watch runs under a one-hour `perl` alarm (exit 142 checked live) whose exit stops with fresh state; the wake acts only on the armed branch with no uncommitted tracked change, reads state and head together, stops on a failed read or a foreign head before re-arming, counts skipped checks as passed; a typed resume `TaskStop`s the armed watch; CI line and the armed close's safety line name the desktop app and that `/clear` or other work ends the self-resume; stop list gains the bound, a foreign head, a failed read; W20 wording fixed; both skill sites mirror it (hotfix's typed-resume text moved after the wake handling); D-230 annotates D-229; CHANGELOG, wait-mechanisms implications, test docstrings and comments updated; `test_wait_rule` re-pinned (arm under the bound, arm only while pending); two parked rows filed (diff-bug #14, blame-history #5); baseline 889 lines / 88,073 bytes; skills/tests 983 OK, scripts and hooks suites, both validates exit 0, cairn_validate green.
- 2026-10-31: correction: the T8 line's "exit 142 checked live" was checked with `sleep`, not `gh`; `gh` ignores SIGALRM, so the alarm bound does not end the watch (pass-3 diff-bug #1).
- 2026-10-31: review return 3: pass 3 found load-bearing defects in the merge wait (diff-bug #1: the bound never ends `gh`; blame-history #1: a changes-requested review during the wait is merged past; diff-bug #3–#5, #8). Third defect return: thrash rule (a) fires; disposition goes to the user at the descope-or-park chip.
- 2026-10-31: question set (thrash stop): user chose "Descope and ship": keep the background wait, remove the broken bound, add the moved-head and changes-requested guards, send the edge cases to parked rows and the never-settling check to a known issue, then one short review (diff-bug and ripple lenses over the descope diff) and the merge question.
- 2026-10-31: substantive amendment: Scope Out gains "A time bound on the watch: none; a check that never settles is a DESIGN.md Known issue (descoped at the thrash stop, D-231)" and "The smaller merge-wait edge cases from review pass 3: candidate row "Close the merge CI wait's edge cases"". No criterion changed.
- 2026-10-31: T9 done: `perl` bound and 142 handling removed from the rule and both sites; the wake reads `state,headRefOid,reviewDecision` and stops on a head other than the approved one (review: the head step 8 pushed; hotfix: the marker's head oid) or `CHANGES_REQUESTED` before any fix, re-arm, or merge; stop list updated; D-231 supersedes D-230's bound; parked row "Close the merge CI wait's edge cases" filed; known issue proposed in the Review section; CHANGELOG and `wait-mechanisms.md` reworded; `test_wait_rule` re-pinned (no bound, head and review guard) with mutation entries; baseline 889 lines / 88,037 bytes; AC section rewrapped wider (same words) for the 150-line cap; skills/tests 984 OK, scripts and hooks suites, both validates exit 0, cairn_validate green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->

Pass 1 (2026-10-31). PR #342 opened at review start (Copilot arm); Copilot request made, state query read `none` after it: may not be recorded by GitHub (used-up Copilot credits are one cause).

- AC1: tracking-rules wait rule, read at HEAD: "has four steps. (a) Arm `gh" (1 match); wake line naming PR, status, resume command (line 403); close block with CI line and fenced resume command (404-406); (d) reads `gh pr checks <N>` and `gh pr view <N> --json state`, "If any check failed, take the red-CI path. Otherwise, if a check is pending" (1 match), all passed → merge; closed PR and no-checks clauses named; foreground `gh pr checks` in the section: 0 matches; stop list reads "a local check that times out" (588); On timeout names local commands and Monitors (418). Pass.
- AC2: early-stop clause names the armed turn end (600-602); stop-point clause names the merge watch as the one exception (426), still bars a commit, and an unarmed wake line "runs nothing" (430). The clause says a `/clear` while armed "loses nothing", not that it "is safe" as the criterion requires. Fail.
- AC3: `/milestone-review` step 8 (713, 722) and its companion arm (752-753) and `/hotfix` step 6 (506, 519) state the background watch with their own resume command (1 match each); the AC3 grep lists 7 lines, none a foreground or ceiling-bound wait. Pass.
- AC4: one-watcher clause names the host app's PR monitor exception, "A session never turns such a monitor on for a merge wait", and the head-commit rule (lines 397-400). Pass.
- AC5: `wait-mechanisms.md` W24 (late red, PR #2 run 41215432313, failure at 15:36:54 after the turn ended ~15:34; woken turn read `gate` fail, `long` pending → red path) and W25 (green, PR #1 run 41215428891, 12 min 5 s; woken turn read both pass → merge branch), each an idle wake with no user message; the rule cites "(W24, W25 — the host observed)" and names the Claude Code desktop session. Pass.
- AC6: the AC6 grep, outside the rewritten blocks, lists 23 lines; each that describes a merge's CI wait (README 710, hotfix 120/194/208/217/530, review 79, implement 335, tracking-rules 352/588/602/612-614) agrees; PROFILE:68 and cairn-release 122-126 (local checks, Out) do not describe a merge wait in conflict. CHANGELOG Unreleased line 7 entry. Pass.

Pass 2 (2026-10-31). Default branch unmoved; PR #342 open; Copilot state `none`, requested again (exit 0), still `none` after: may not be recorded by GitHub (used-up Copilot credits are one cause).

- AC2: stop-point clause at HEAD now reads "a `/clear` while it is armed is safe and loses nothing (the watch is documented to survive it, W20, and whether its notification then reaches the new session is unobserved)"; the merge watch is still the one turn-end exception, a commit still bars a watcher, an unarmed wake line "runs nothing", and the early-stop clause names the armed turn end (600-602). Pass.
- AC1, AC3–AC6: the T7 diff (`git diff 75d56fb9..HEAD -- skills`) changes only the stop-point sentence and the baseline figure; their pass-1 evidence stands.
- Gate: `cairn_validate` exit 0, no FAIL or WARN lines; verify on the review head: skills/tests 982 OK, scripts and hooks suites exit 0, plugin and marketplace validate exit 0, `claude plugin test` 2466 pass; marketplace validate prints no `version` warning; CHANGELOG Unreleased has the entry, with no milestone number; no DESIGN principle changed, so `cairn_impact` skipped.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a typed resume while armed arms a second watch; its stale wake re-enters after the merge (review route (a) reruns hygiene; hotfix's merged-PR re-entry says the bar never ran) — fix now
- diff-bug #2: a watch that exits before the turn ends (no-checks PR, finished CI, fast red) has no rule, and no wake follows — fix now (read `gh pr checks` first; arm only while a check is pending)
- diff-bug #3: the armed close block's "adjusting course or `/clear` are both safe" line lets a later wake merge mid-other-work — fix now (armed close says to wait; a wake that finds the session off the milestone branch shows its line and runs nothing)
- diff-bug #4: step (d) has no branch for skipped or neutral checks or a failed `gh` read — fix now
- diff-bug #5: no bound for a watch that never settles (fork PR awaiting approval) — fix now (one-hour `perl` alarm, then the old timeout route)
- diff-bug #6: a foreign push re-arms before the head check — fix now (head check before re-arming)
- diff-bug #7: the moved-head stop is not on the closed stop list — fix now
- diff-bug #8: hotfix places the typed-resume sentence between the turn end and the wake handling — fix now
- diff-bug #9: the companion's wake reads are spelled bare — fix now
- diff-bug #10: red path on a fork-head PR names no fork remote — reject (false: "red CI the agent cannot fix stops" covers it)
- diff-bug #11: `test_wait_rule.py` docstring describes the stop point with no exception — fix now
- diff-bug #12: CHANGELOG "On red it fixes the run" is imprecise — fix now
- diff-bug #13: compaction can kill the armed watch — reject (false: the close block's fenced resume command covers a wake that never comes)
- diff-bug #14: a typed resume via route (c) pushes the unpushed header-URL commit and restarts CI — follow-up: parked row "Keep a typed resume from restarting CI" (pre-existing D-138 path)
- blame-history #1: the watch has no bound; D-133's required check left pending by a path skip hangs it — fix now (same as diff-bug #5)
- blame-history #2: the CI line promises a self-resume in every host — fix now (desktop app named)
- blame-history #3: a `/clear` after arming stalls the merge while the CI line promises resumption — fix now (armed close says `/clear` or other work stops the self-resume; type the command then)
- blame-history #4: D-128's reopening observation now fires by design — reject (planned change: D-229 supersedes that clause)
- blame-history #5: red-CI "re-request approval if the fix was nontrivial" now runs unattended — follow-up: parked row "Ask again before merging a red-CI fix" (pre-existing rule on main)
- blame-history #6: a typed resume in a host that keeps the watch makes a second watcher — fix now (same as diff-bug #1)
- blame-history #7: `/cairn-release` keeps the foreground model — reject (false: its slow local checks follow the local-command clause, which keeps it)
- prior-review #1: "documented to survive" `/clear` overstates W20 — fix now
- prior-review #2: the merge watch exempt from the turn-end bar reopens M170's runaway-watcher case — reject (planned change, D-229), its unbounded part fixed with blame-history #1
- prior-review #3: `/cairn-release` restatement drift — reject (false, as blame-history #7)
- prior-review #4: the merge-wait close states no fresh check state (M183) — reject (planned change: no timeout stop on a merge wait; the CI line rule is met)
- prior-review #5: "On timeout" no longer covers merge waits — reject (planned change), the bound's stop restores a timeout route
- ripple #1: the flat stop-point bar sits before its exception with no marker — fix now
- ripple #2: "documented to survive" — fix now (same as prior-review #1)
- ripple #3: `test_wait_rule.py` docstrings — fix now (same as diff-bug #11)
- ripple #4: `/cairn-release` wording — reject (false, as blame-history #7)
- ripple #5: `test_resume_routing.py:337` and `test_mutation_harness.py` comments name a hotfix timeout close — fix now
- ripple #6: DESIGN Known issue's "CI stop" — reject (false: red CI and the new bound are still CI stops)
- ripple #7: `wait-mechanisms.md` implications paragraph omits W24–W26 — fix now

Pass 3 (2026-10-31), after return 2 (T8, fixed 017b2472 for every pass-2 fix-now line above). Default branch unmoved.

- AC1: wait-rule section, whitespace-collapsed, 1 match each for: "Otherwise arm `gh pr checks <N> --watch --fail-fast` as a Bash `run_in_background` task"; the wake line naming PR number, status, resume command; "End the turn with a close block whose CI line says that in the Claude Code desktop app the session resumes by itself when CI ends"; "its fenced next command is that resume command"; "If any check failed, take the red-CI path. Otherwise, if a check is pending, arm the watch again"; "If every check passed (a skipped check counts as passed), go on to the merge"; closed-PR and no-checks clauses; reads with `gh pr checks <N>` and `gh pr view <N> --json state,headRefOid`; foreground `gh pr checks` in the section: 0; stop list (600) names a one-hour bound, not a harness-ceiling stop; On timeout names local commands and Monitors. Pass.
- AC2: "The one exception is a merge's armed CI watch above, the one watcher a turn can end on" (1); commit still barred; "is safe and loses nothing" (1); unarmed wake line "shows the user the line and its resume command and runs nothing" (1); early-stop clause names the armed turn end (613-615). Pass.
- AC3: AC3 grep lists 11 lines in the two skills; each states the background watch (review 710-729, 760; hotfix 504-521, 536) or reads state with no wait (review 743, hotfix 543); none is a foreground or ceiling-bound wait; resume commands `/milestone-review M<NNN>` and `/hotfix <PR reference>` in each wake line. Pass.
- AC4: "A session never turns such a monitor on for a merge wait" (1) with the head-commit rule. Pass.
- AC5: W24, W25 unchanged; the rule cites "(W24, W25 — the host observed)" and names the Claude Code desktop session. Pass.
- AC6: the AC6 grep outside the rewritten blocks lists 23 lines; README 710 (desktop app, resume command elsewhere), hotfix 120/194/208/217/417, review 79, implement 335, tracking-rules 352/600/615/625-627 agree; PROFILE:68 and cairn-release 122-126 are local or no-CI text; CHANGELOG Unreleased entry present. Pass.
- Gate: `cairn_validate` exit 0, 0 FAIL/WARN lines; verify on the review head: skills/tests 983 OK, scripts and hooks suites exit 0, plugin and marketplace validate exit 0, `claude plugin test` 2466 pass, 0 fail; marketplace validate prints no `version` warning; CHANGELOG entry present with no milestone number; no DESIGN principle changed.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the one-hour `perl` alarm never ends `gh` (Go ignores SIGALRM; verified: `gh` under a 2 s alarm exited 0, `cat` exited 142), so a never-settling watch still hangs — load-bearing; held for the thrash-stop choice
- diff-bug #2: a 142 exit with a pending check reads as re-arm before the 142 stop — held (moot until #1 is fixed)
- diff-bug #3: no head check before the red path, so a foreign failing head is "fixed" on a stale local branch — held
- diff-bug #4: "the head the session pushed" never holds for an adopted fork PR — held
- diff-bug #5: `/milestone-review` has no recorded head (marker has no oid, merge has no `--match-head-commit`) — held; overlaps the existing DESIGN Known issue on bare merges
- diff-bug #6: neutral and cancelled checks still have no branch — held
- diff-bug #7: "a failed read" is undefined against `gh pr checks` exit 1 and 8 — held
- diff-bug #8: a tree already dirty at arm time stalls every wake — held
- diff-bug #9: the typed-resume `TaskStop` sits in step 8/6, after the routes that run first — held
- diff-bug #10: a failed `exec` reports exit 0 — held
- diff-bug #11: `wait-mechanisms.md` states a no-wake-for-early-exit claim with no W row — held
- diff-bug #12: a wake can merge an hour later with no check that the default branch moved — held (pre-existing, window longer)
- blame-history #1: the wake merges with no read of `reviewDecision`, so a changes-requested review during the wait is merged past — load-bearing (outward, irreversible); held
- blame-history #2: as diff-bug #5 — held
- blame-history #3: review's "merges and re-arms nothing" reads as authorizing a merge — held
- blame-history #4: the `cancel` bucket has no branch — held (as diff-bug #6)
- blame-history #5: no observable test for "a watch it did not arm" — held
- blame-history #6: (a)'s "straight to (d)" names a notification step; companion branch check runs in the primary checkout — held
- blame-history #7: README's self-resume lacks the `/clear`-or-other-work exception — held
- prior-review #1: as blame-history #3 — held
- prior-review #2: "W20 reports the watch surviving" still overstates an unobserved row — held
- prior-review #3: the rule's no-checks path skips the fresh-PR re-read the skill sites keep — held
- prior-review #4: as diff-bug #5 — held
- ripple #1: "loses nothing" is not observed — held (as prior-review #2)
- ripple #2: `wait-mechanisms.md` implications paragraph still states the foreground conclusion — reject (false: framed as M170's finding, with M328's note above it)
- ripple #3: DESIGN Known issue's "CI stop" — reject (false: red CI and the bound are CI stops)
- ripple #4: test names keep "timeout" vocabulary — reject (style: names only)
- ripple #5: copilot-review's unconditional safety line — reject (false: that skill arms no merge watch)
- Pass-3 dispositions after the user chose descope at the thrash stop: diff-bug #1 — fix now (bound removed; the never-settling check is the known issue below); diff-bug #2 and #10 — reject (false: no bound and no `perl` wrapper remain); diff-bug #3, #4 and blame-history #1 — fix now (at the wake, a head other than the approved one, or `CHANGES_REQUESTED`, stops before any fix, re-arm, or merge; hotfix compares with the marker's head oid); blame-history #3 and prior-review #1 — fix now (sentence rewritten); diff-bug #11 — fix now (claim marked unobserved); diff-bug #5–#9, #12, blame-history #2, #4–#7, prior-review #2–#4, ripple #1 — follow-up: parked row "Close the merge CI wait's edge cases"
- known issue: A merge CI watch has no time bound. A check that never settles, such as a required check that a path filter skips or a fork run waiting for approval, keeps the watch armed, and the session never wakes. Look at the PR, then type the resume command that the turn ended with. Accepted at the M328 gate
