# M202: One question set, then the agent runs the milestone to the merge question

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3
- **Resolves:** —
- **Surface tier:** user-facing, because the skills ship in the plugin to every adopter
- **Branch/PR:** m202-one-question-set-run

## Goal

After the one question set of the plan, the agent implements and reviews the milestone in the same run. It stops only at a named stop or at the merge question.

## Scope

**In:** The rulebook section "Question gates and phase closes" keeps two
gates and a closed list of stops between them. The plan question set asks
only what the user alone can settle, and it foresees what implement and
review will need from the user. The plan, implement, and review skills hand
off to the next phase through the Skill tool. Implement asks no question
round of its own. Review decides each finding itself and keeps one merge
question. After a merge, the run starts the next workable milestone that the
same plan created. Typed `/milestone-implement` and `/milestone-review`
stay as the commands that resume a stopped run. README, CHANGELOG, DESIGN,
the routing template, this repo's CLAUDE.md, and a D-entry describe the
run. The hand-run prose tests that pin the old wording change with it.

**Out:** Approval of the merge in the question set goes to M203. The
questions of `/hotfix` go to the candidate row "`/hotfix` keeps its own
questions". The criteria audit, the review lenses, and the repeated-failure
rule stay as they are. Only who settles their findings changes.

## Acceptance criteria

- [x] AC1: The "Question gates and phase closes" section of
      `skills/shared/tracking-rules.md` names two gates: the plan question
      set and the merge question. It names each stop allowed between them:
      - the user's eyes or hands are needed (a live look, a file, a login,
        a deployment),
      - an outward or irreversible action, or a dependency change, that the
        question set did not cover,
      - the goal is found wrong, or a change drops something the user asked
        for,
      - the repeated review-failure stop,
      - a CI wait that times out, or red CI that the agent cannot fix,
      - a guard hook's denial,
      - a stop at a task boundary for context hygiene,
      - the offer to escalate to a Fable review,
      - the user's yes before a risky or destructive action,
      - the guest-mode handoff.

      Its close-block paragraph states two facts. Inside a run, a phase
      ends with a call to the next skill through the Skill tool. The close
      block ends the run. The command
      `grep -rn -i -E 'three gates|third gate|three points|choices gate|pre-implementation (gate|question)|nothing runs but you'`
      over `skills/`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`, and
      `cairn/DESIGN.md` prints no line.
- [x] AC2: Step 3 of `skills/milestone-plan/SKILL.md` names the questions
      that the set asks:
      - what to work on, for a request that names no work,
      - choices that the request leaves open about what the user will get,
      - files, access, or looks that only the user can supply and that
        implement or review will need,
      - permission for the outward actions and dependency changes that the
        work foresees.

      It names what the agent decides itself, with a work-log line for
      each: criteria wording, criteria-audit findings, milestone splits and
      order, approach, test scope, and changelog entries. It states that a
      question the agent cannot phrase without the terms of cairn is a
      question the agent decides itself.
- [x] AC3: `skills/milestone-plan/SKILL.md` ends with its commit and push.
      Then it invokes `/milestone-implement` through the Skill tool for the
      first workable milestone that it planned. If another milestone is in
      progress, or the user asked for a plan alone, it ends with a close
      block instead.
- [x] AC4: `skills/milestone-implement/SKILL.md` has no question round
      before work starts. On completion it sets `review` and invokes
      `/milestone-review` through the Skill tool in place of its close
      block. Its amendment step makes an amendment with a work-log line. If
      an amendment drops something the user asked for, or changes what the
      user sees from the plan, the step stops for the user instead.
- [x] AC5: `skills/milestone-review/SKILL.md` poses `AskUserQuestion` only
      at the merge question and at the stops in AC1. Its step-7 sentence on
      clarifying questions is gone. Review rejects, with the reason in the
      Review section, a finding that it shows to be false against the code,
      a style or linter item, or a complaint about a change the plan called
      for. It fixes on the branch each other finding that it judges real and
      inside the milestone scope, and it sends the rest to candidate rows.
      Items from a PR conversation get the same dispositions from the agent,
      and an item that requests nothing is logged as noted. The merge
      question lists the disposition of each finding in plain words. If the
      same plan created another workable milestone, review invokes
      `/milestone-implement` for it after the merge. Otherwise it ends with
      its close block.
- [x] AC6: Six surfaces describe the run. In `README.md` they are the
      workflow section and the "What the system expects from you" section.
      The others are a `CHANGELOG.md` entry, the architecture in
      `cairn/DESIGN.md`, `skills/shared/templates/claude-md-section.md`,
      and the cairn section of `CLAUDE.md`. One command starts the run, one question set follows,
      and the agent works on to the merge question. Typed
      `/milestone-implement` or `/milestone-review` resumes a stopped run.
      A D-entry records the change. It supersedes the three-gate clause of
      the rulebook, the per-phase close-block handoff of D-124, and the
      plan-gate question for an arguable criteria-audit finding. It
      annotates D-003 and D-022.
- [x] AC7: The verify slot passes with exit code 0 for each command:
      `python3 -m unittest discover` over `scripts/tests` and over
      `hooks/tests`, `claude plugin validate`, and `claude plugin test`.

## Coverage

- AC1 → T1, T5, T6
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T7

## Tasks

- [x] T1: Rewrite "Question gates and phase closes" in
      `skills/shared/tracking-rules.md` (lines 351-393 today): the two
      gates, the stop list, the early-stop clause for a run, and the
      close-block paragraph. Adjust "Context hygiene" (lines 341-349) for a
      run that crosses phase seams in one session.
- [x] T2: `skills/milestone-plan/SKILL.md`: the step-3 rule for the
      questions of the set, criteria-audit findings settled by the agent,
      and step 7 with the Skill-tool handoff. The plan commit subject names
      the IDs of the run, so review can find the next one.
- [x] T3: `skills/milestone-implement/SKILL.md`: remove the step-3 question
      round (lines 70-81 today), keep the escalation offer as a stop, make
      step-6 amendments without a gate, and end step 9 with the handoff.
- [x] T4: `skills/milestone-review/SKILL.md`: findings settled by the agent
      (lines 283-304) and the PR-conversation triage (lines 375-407). Then
      the clarifying-questions sentence and the "third gate" wording (lines
      409-411), and the step-10 handoff to the next milestone of the plan.
- [x] T5: The surfaces in AC6, and the D-entry. Grep the repo for the old
      phrasing first (the M112 lesson), and fix each hit outside history.
- [x] T6: In `skills/tests`, update or delete the assertions that pin the
      retired wording: `test_gate_wording.py:93`,
      `test_chapter_marker_mandate.py:41-43`, `test_stakes_tier.py:83`,
      `test_gate_conclusion_preview.py:6-7`.
- [x] T7: Run the verify slot and `cairn_validate`.

## Work log

- 2026-10-03: created by /milestone-plan, in one run with M203.
- 2026-10-03: plan evidence from the session transcripts of all repos, 2026-09-22 to 2026-10-03: 1,467 answered questions, 92% took the first option. Merge 323 asked, 1 changed. Scope and goal 162, 25% changed. Live looks 16, 9 changed. Criteria wording 101, 4 changed. Review findings 119, 11% changed.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) returned 13 findings over M202 and M203. It fixed 11 by narrowing or by naming stale files, and posed 2 at the gate (run in a row, merge up front).
- 2026-10-03: plan gate chose a Skill-tool handoff between the three skills over one merged skill, because each skill keeps its trigger text and resume role. Falsified by a run that loses its place at a phase seam.
- 2026-10-03: plan gate chose to run the milestones of a plan in a row over a stop after each merge, at the user's answer. Falsified by a run whose condensed context drops a fact that the tracking files did not hold.
- 2026-10-03: plan gate chose findings settled by the agent over a fix-now question, because 89% of those answers took the recommended set. Falsified by merged runs whose finding dispositions the user reverses.
- 2026-10-03: implement started on branch m202-one-question-set-run. Untracked `tsconfig.json` on main left out of every commit.
- 2026-10-03: implement question gate chose to amend AC5 so that review rejects a finding it shows false against the code, with the reason in the Review section, over a candidate row for every unfixed finding (ROADMAP at 51 of 60 lines).
- re-audit: AC5 (full) — reviewers give no real-or-not verdict, so "the reviewers rank as real" points at nothing; the exception misses a real-ranked finding shown false; PR items that request nothing lose "noted"; style, linter, and planned-change items would fill the ROADMAP; D-110's triage clause is not in AC6's list (the D-entry will name it); the second amendment return stop is not in AC1's list (T1 folds it into the repeated review-failure stop).
- 2026-10-03: AC5 amended at a second mini gate (user chose the revised wording): review rejects false, style or linter, and planned-change findings with a reason, judges real itself, and logs PR items that request nothing as noted.
- re-audit: AC5 (full) — wording can be met; the step-9 records-hygiene chip and the step-10 release-parking chip fall outside "only" (T4 retires both, the D-entry annotates D-050); D-110 to be named by the D-entry. No further reader for AC5.
- 2026-10-03: T1 done. The rulebook names two gates, the closed stop list, a run-scoped early-stop clause, and a close block that ends the run; Context hygiene covers a run across seams; dependency changes go to the question set or a stop. Verify green (scripts 0 fail, hooks 0 fail, validate passed, plugin test 632 pass).
- 2026-10-03: T2 done. Plan step 3 names the four kinds of question and what the agent decides; audit findings, collisions, inbox hits, and the checker-regress shape are settled by the agent with a work-log line; step 7 hands off to `/milestone-implement` through the Skill tool, with a close block when another milestone is in progress, a plan alone was asked, or nothing is workable. Verify green.
- 2026-10-03: T3 done. Implement has no question round; uncovered dependency or outward actions and the escalation offer are stops; substantive amendments are made with a work-log line and stop only when they drop something asked for or change what the user sees; D-118 widening reaches criteria only at a stop; step 8 lists the stops with the stop close block and CI line; step 9 hands off to `/milestone-review` through the Skill tool.
- 2026-10-03: T4 done. Review settles each finding (reject with reason, fix now, follow-up) and each PR item (plus noted); gate and floor failures return to implement through the Skill tool; the clarifying-questions sentence is gone; the merge question lists dispositions; step 9 files a new cross-referencing row in place of the records-hygiene §7 chip (§7 now names `/milestone` alone); step 10 hands off to the next workable milestone of the plan, read from the plan commit subject, and moves release parking to `/milestone` in the close block.
- 2026-10-03: T5 done. README (core loop, worked example, session paragraph, skill table, "What the system expects from you", inbox and issue lines), CHANGELOG entry, DESIGN architecture and trigger convention, routing template, and this repo's CLAUDE.md describe the run; D-144 records it (supersedes the three-gate clause, D-124's per-phase handoff, D-067's arguable-finding question, D-110's maintainer triage; annotates D-003, D-022, D-050). AC1 grep outside `skills/tests` prints nothing. The CHANGELOG claim on repair was read against `/cairn-init` §3 (repair never rewrites authored content) and narrowed. README line 161's band example keeps the chapter "Question gate", which the band tests use as a fixture.
- 2026-10-03: T6 done, delegated to one Opus agent and its diff read here. The branch had added 39 failures and 28 errors in `skills/tests`; 11 files re-anchored or rewritten to the new rules, none deleted, 21 mutation-harness entries repointed, 2 tests added. The agent found `/hotfix` step 6 still citing review's four triage options, so hotfix now names them itself (hotfix keeps its questions) and its test follows. skills/tests 663, the same 4 reds and 1 error as main.
- claim audit: 41 claims read, 7 corrected — tracking-rules.md (refused fresh-reader stop folded into stop item 1; resume-command exception for the goal-wrong and guest stops), milestone-review/SKILL.md (guest arm reaches step 10 later; fix-now deadline is before the merge question; deferred row named in the handoff or close block; "displacement clause below"), records-hygiene.md (§7 chip posed when the audit finds such a row). Each correction re-read once by the same reader and holds.
- 2026-10-03: T7 done. Verify green: scripts 0 fail, hooks 0 fail, plugin validate passed, plugin test 632 pass 0 fail; cairn_validate all checks passed. Status set to review.
- 2026-10-03: review return 1 (defect, step-4 gate): AC1 fails as written. Its grep over `skills/` prints two lines, `skills/tests/test_gate_wording.py:74` and `:79`, which hold the retired phrase "exactly three gates" in a comment and an `assertNotIn` literal (T5's work-log line scoped the grep to outside `skills/tests`). AC2–AC7 and `cairn_validate` passed on this pass; nothing ticked. Status back to in-progress.
- 2026-10-03: return 1 fixed. `test_gate_wording.py` now asserts `assertNotRegex(text, r"exactly three\s+gates")` and its comment names "the three-gate clause", so AC1's grep prints no line. A planted "exactly three gates" makes the regex match, the real rulebook does not. Verify green (scripts 0, hooks 0, validate 0, plugin test 0). Status set to review.

## Decisions

## Review

Pass 2 (2026-10-03, after return 1), on branch head 3bc80e7. The branch contains `origin/main` (203e023), so no merge was needed.

- AC1: `tracking-rules.md:358` says interaction in a run "happens at two gates". It names the plan question set and the merge question. All ten stops of AC1 are bullets in the stop list. A grep for their openings counts 10. Line 401 opens the close-block paragraph with "Inside a run, a phase ends with a call to the next skill through the Skill tool". Line 402 says "The **close block** ends the run". The AC1 grep over the five named paths prints no line (exit 1). On pass 1 it printed two lines from `skills/tests/test_gate_wording.py`.
- AC2: `skills/milestone-plan/SKILL.md:142-147` lists the four kinds of question. Lines 149-151 name what the agent decides with a work-log line each: criteria wording, criteria-audit findings, milestone splits and order, approach, test scope, and changelog entries. Lines 151-152 say a question the agent cannot phrase without the terms of cairn is one it decides.
- AC3: Step 6 of the plan skill commits and pushes (lines 354-362). Step 7 (lines 368-374) then invokes `/milestone-implement M<NNN>` through the Skill tool for the first workable milestone of the plan. In lines 375-382, if another milestone is in progress or the user asked for a plan alone, the step ends with a close block instead.
- AC4: `skills/milestone-implement/SKILL.md:73` is step 3, "No question round". Step 9 (lines 240-249) sets `review` and invokes `/milestone-review <id>` through the Skill tool in place of a close block. Step 6 (lines 127-137) makes a substantive amendment with a work-log line. If the amendment drops something asked for or changes what the user sees, it stops for the user.
- AC5: `skills/milestone-review/SKILL.md:24` limits `AskUserQuestion` to the merge question and the stops. A grep for every chip and `AskUserQuestion` site finds only the merge chip, its resume re-posings, and the thrash-rule stop. A grep for "clarif" prints nothing. Lines 294-308 hold the three dispositions: reject with a reason, fix now, follow-up. Line 412 logs a PR item that requests nothing as noted. Line 312 has the merge question list each disposition. Lines 651-658 invoke `/milestone-implement <next-id>` for the next workable milestone of the plan. With no such milestone, the close block ends the run.
- AC6: Each surface states the run and the resume commands. The README workflow section is at lines 249-271 ("One command starts a run"). The README "What the system expects from you" bullets are at lines 409 and 414. The others are the `CHANGELOG.md:91` entry, `cairn/DESIGN.md:36`, `claude-md-section.md:14`, and `CLAUDE.md:22`. D-144 supersedes the three-gate clause, D-124's per-phase handoff, and D-067's arguable-finding question. It annotates D-003 and D-022.
- AC7: Each verify command exits 0. `scripts/tests` ran 395 tests, OK with 21 skipped. `hooks/tests` exits 0. `claude plugin validate` passed with warnings. `claude plugin test .` reports 632 pass and 0 fail.
- Consistency gate: `cairn_validate` passes all checks (exit 0). No DESIGN principle line changed, so `cairn_impact` was skipped. The `generic` profile names no toolchain checks.

Independent review, pass 2: the tier is user-facing, so three fresh reviewers ran (diff-bug on Opus, blame-history and prior-review on Sonnet). The PR-comment probe found no threads. Their 32 reports merge into 24 findings below (F1 to F24). The agent settled each one. No finding shows a criterion failing, and none is a load-bearing defect, so status stays `review`.

- F1, fix now. Previews and recaps that a skill shows just before a phase-end Skill call are not sure to render (plan step 7, implement steps 6 and 9, review step 9).
- F2, fix now. Old gate wording survives: the rulebook says the maintainer triages the ranked list and calls the merge question "the review gate". Plan steps 3 and 4, the milestone template, and `/milestone-brief` also name gates that are gone. Rejected parts: "gated amendment" stays, because the re-audit reader still gates amended wording. The freshness clause's "pending user gate" stays, because review still has the merge chip and implement's claim audit stops with a close block.
- F3, fix now. Resume route (b) runs on a merged head, but a gate or floor failure there now calls implement for a branch that is gone.
- F4, follow-up (new candidate row). No milestone after M166 re-seeded the rulebook-size baseline in `/milestone` and two tests. This branch adds to the drift.
- F5, fix now. The plan guest arm says "the close block is unchanged", and step 7 says "after the commit", which guest mode does not make.
- F6, rejected, planned change. The session that wrote the code settles the reviewers' findings. AC5 and D-144 call for this, and D-144 names its falsifier.
- F7, rejected, planned change. Pre-existing and unmodified-line findings go to candidate rows, not to rejection. AC5 sends "the rest" to candidate rows.
- F8, follow-up (new candidate row). New cross-referencing rows never trip the M161 two-milestone trigger, and every unfixed finding adds ROADMAP lines toward the cap.
- F9, fix now. The merge question does not show criteria the agent amended during the run.
- F10, fix now. The D-118 widening path points at "a stop above", and no stop there names a widening.
- F11, rejected, planned change. Plan step 1 no longer asks for sign-off to plan ahead. The question set still runs, and a plan made ahead ends with a close block.
- F12, follow-up (new candidate row). Review step 10 can chain into milestones from a plan that never ran as a run (made before M202, or a plan alone).
- F13, rejected, planned change. A run has no stop at the milestone seam. D-144 accepts this and records the falsifier, and the context-hygiene stop at a task boundary remains.
- F14, fix now. Answers from the question set (permissions, files, looks) are not written to disk, so a resumed run cannot read them.
- F15, fix now. A review return adds no task, so implement can hand back with nothing fixed.
- F16, fix now. "Ask the user" rules for a dirty tree and another in-progress milestone are not on the closed stop list.
- F17, follow-up (new candidate row). A release-window advisory for an unrelated release ends the run, and the close block always puts `/milestone` first.
- F18, fix now. "Defer the rest" of the plan questions points at a gate that is gone.
- F19, fix now. `records-hygiene.md` is 55 lines against its own "under 55 lines" budget.
- F20, fix now. A declined merge question names no close block or resume command.
- F21, fix now. Plan step 7 and review step 10 pick the next milestone in different orders, and a re-cut can leave two plan commits naming one id.
- F22, fix now. CHANGELOG and README say implement never asks anything and that typed implement or review resumes every stop.
- F23, fix now. The checker-regress rule lets the agent replace asked-for hardening with deletion, which drops what the user asked for.
- F24, fix now. Thrash trigger (b) does not say how a switch to the recorded alternative is made.
- F2 addendum: the milestone template's "plan gate chose" line and plan step 4's "Record the alternative the gate rejected" bullet stay. They are a fixed record shape that the work logs and the prose tests match on.
- Fix-now landed after checkpoint 5cfbff1, covering F1, F2, F3, F5, F9, F10, F14 to F16, and F18 to F24. Edited: the rulebook, the plan, implement, review, and brief skills, `records-hygiene.md` (now 54 lines), README, CHANGELOG, and three prose tests with one mutation entry. Verify re-run green: scripts 0, hooks 0, validate 0, plugin test 0. `cairn_validate` passes, and the AC1 grep prints no line. `skills/tests` shows 663 tests with the same 4 failures and 1 error as main.
