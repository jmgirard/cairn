# M202: One question set, then the agent runs the milestone to the merge question

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3
- **Resolves:** —
- **Surface tier:** user-facing, because the skills ship in the plugin to every adopter
- **Branch/PR:** —

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
      clarifying questions is gone. Review fixes on the branch each finding
      that the reviewers rank as real and inside the milestone scope. It
      sends the other findings to candidate rows. Items from a PR
      conversation get the same dispositions from the agent. The merge
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

- [ ] T1: Rewrite "Question gates and phase closes" in
      `skills/shared/tracking-rules.md` (lines 351-393 today): the two
      gates, the stop list, the early-stop clause for a run, and the
      close-block paragraph. Adjust "Context hygiene" (lines 341-349) for a
      run that crosses phase seams in one session.
- [ ] T2: `skills/milestone-plan/SKILL.md`: the step-3 rule for the
      questions of the set, criteria-audit findings settled by the agent,
      and step 7 with the Skill-tool handoff. The plan commit subject names
      the IDs of the run, so review can find the next one.
- [ ] T3: `skills/milestone-implement/SKILL.md`: remove the step-3 question
      round (lines 70-81 today), keep the escalation offer as a stop, make
      step-6 amendments without a gate, and end step 9 with the handoff.
- [ ] T4: `skills/milestone-review/SKILL.md`: findings settled by the agent
      (lines 283-304) and the PR-conversation triage (lines 375-407). Then
      the clarifying-questions sentence and the "third gate" wording (lines
      409-411), and the step-10 handoff to the next milestone of the plan.
- [ ] T5: The surfaces in AC6, and the D-entry. Grep the repo for the old
      phrasing first (the M112 lesson), and fix each hit outside history.
- [ ] T6: In `skills/tests`, update or delete the assertions that pin the
      retired wording: `test_gate_wording.py:93`,
      `test_chapter_marker_mandate.py:41-43`, `test_stakes_tier.py:83`,
      `test_gate_conclusion_preview.py:6-7`.
- [ ] T7: Run the verify slot and `cairn_validate`.

## Work log

- 2026-10-03: created by /milestone-plan, in one run with M203.
- 2026-10-03: plan evidence from the session transcripts of all repos, 2026-09-22 to 2026-10-03: 1,467 answered questions, 92% took the first option. Merge 323 asked, 1 changed. Scope and goal 162, 25% changed. Live looks 16, 9 changed. Criteria wording 101, 4 changed. Review findings 119, 11% changed.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) returned 13 findings over M202 and M203. It fixed 11 by narrowing or by naming stale files, and posed 2 at the gate (run in a row, merge up front).
- 2026-10-03: plan gate chose a Skill-tool handoff between the three skills over one merged skill, because each skill keeps its trigger text and resume role. Falsified by a run that loses its place at a phase seam.
- 2026-10-03: plan gate chose to run the milestones of a plan in a row over a stop after each merge, at the user's answer. Falsified by a run whose condensed context drops a fact that the tracking files did not hold.
- 2026-10-03: plan gate chose findings settled by the agent over a fix-now question, because 89% of those answers took the recommended set. Falsified by merged runs whose finding dispositions the user reverses.

## Decisions

## Review
