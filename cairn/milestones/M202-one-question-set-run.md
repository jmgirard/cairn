# M202: One question set, then the agent runs the milestone to the merge question

- **Status:** in-progress
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

- [ ] AC1: The "Question gates and phase closes" section of
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
- [ ] AC2: Step 3 of `skills/milestone-plan/SKILL.md` names the questions
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
- [ ] AC3: `skills/milestone-plan/SKILL.md` ends with its commit and push.
      Then it invokes `/milestone-implement` through the Skill tool for the
      first workable milestone that it planned. If another milestone is in
      progress, or the user asked for a plan alone, it ends with a close
      block instead.
- [ ] AC4: `skills/milestone-implement/SKILL.md` has no question round
      before work starts. On completion it sets `review` and invokes
      `/milestone-review` through the Skill tool in place of its close
      block. Its amendment step makes an amendment with a work-log line. If
      an amendment drops something the user asked for, or changes what the
      user sees from the plan, the step stops for the user instead.
- [ ] AC5: `skills/milestone-review/SKILL.md` poses `AskUserQuestion` only
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
- [ ] AC6: Six surfaces describe the run. In `README.md` they are the
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
- [ ] AC7: The verify slot passes with exit code 0 for each command:
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

## Decisions

## Review
