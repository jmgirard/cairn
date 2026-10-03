# M203: Approve the merge in the question set

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M202
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing, because the skills and the merge guard ship in the plugin to every adopter
- **Branch/PR:** m203-merge-approval-up-front

## Goal

The user can approve the merge of a milestone in the plan question set, so a run whose review passes merges without a second question.

## Scope

**In:** IP1 and a D-entry that records the user decision of 2026-10-03.
A `Merge approval:` header slot that the plan writes from the question
set. The merge path of review for an up-front approval, with the cases that
go back to the merge question. The deny text of `merge_guard` and a test.
The rulebook, README, routing template, CLAUDE.md, and CHANGELOG text on
approval.

**Out:** A standing approval for every run of a repo. The user chose one
approval for each plan at the 2026-10-03 gate, so this has no row. The
merge question of `/hotfix` goes to the candidate row "`/hotfix` keeps its
own questions".

## Acceptance criteria

- [ ] AC1: IP1 in `cairn/DESIGN.md` keeps its sentence that nothing
      reaches the default branch without explicit user approval at a gate.
      It adds the two gates for a milestone merge. One is the merge
      question. The other is the plan question set, for a milestone whose
      promise, as that plan committed it, merges unchanged. That milestone
      also meets none of the route-back cases that the rulebook lists. A
      D-entry records the user decision that changes IP1 (RB tripwire:
      ip-touching). The D-entry states that the up-front approval comes
      before the diff exists. It names the route-back cases as the
      mechanism that keeps the promise unchanged, and states that removing
      or narrowing a route-back case changes IP1. It narrows D-138 and
      D-144 and annotates D-043 by name.
- [ ] AC2: The milestone template carries a `Merge approval:` header slot.
      Step 3 of `skills/milestone-plan/SKILL.md` lists merge approval among
      the questions of the set, with one answer for each milestone. When a
      plan creates several, the user can hold any of them `at the end`. The
      question states that a run with no route-back case merges unseen. It
      also states that the code and the finding dispositions of such a run
      appear only after the merge. For a user-facing or IP-touching
      milestone, it recommends `at the end`. The plan writes each slot as
      `up front YYYY-MM-DD` or `at the end`. A set that did not pose the
      question writes `at the end`. A re-cut via `/milestone-plan` asks
      again and rewrites the slot. Review and the guard read `—` or a
      missing slot as `at the end`.
- [ ] AC3: If all of these hold, `skills/milestone-review/SKILL.md` skips
      the merge question:
      - the default-branch copy of the slot reads `up front`,
      - the Goal, Scope, and Acceptance criteria text on the branch differs
        from that of the plan commit only in checkbox ticks (the plan
        commit is the newest default-branch commit whose subject is
        `plan …` and names M<NNN>),
      - no work-log line records a substantive amendment, an
        `amendment return:`, or a declined merge question,
      - each criterion has passing evidence,
      - no finding the agent disposed fix-now is left unfixed,
      - no finding that its lens ranked first was rejected as false,
      - on a user-facing milestone, no finding was rejected as false,
      - the Review section records the spawned reviewers,
      - `Principles touched:` names no IP, and `git diff <default>...HEAD`
        adds no `### D-` heading,
      - no condition of step 7 that adds to the merge question applies (a
        PR review that requests changes, a Driving RR shortfall, guest
        mode, a companion PR, an issue write from `Resolves:`).

      In that case, before the push of step 8, it commits the work-log
      line `step-7 approval: <branch> approved up front per plan <sha>`.
      After the PR opens, CI must be green, or the rulebook rule for a PR
      with no CI runs must apply. No commit was pushed after the PR opened
      (for a PR that already existed, after the push of step 8). When both
      hold, it writes the marker
      `M<NNN> approved up front YYYY-MM-DD per plan <sha> for PR #<N>`. If
      CI is red or a fix is pushed, it asks the merge question. In every
      other case it asks the merge question as before. The close block or
      merge question that ends the run lists each milestone merged up
      front in the run. For each, it gives the PR and each finding verbatim
      with its disposition and the reason for each reject.
- [ ] AC4: The deny text and the docstring of `hooks/merge_guard.py` name
      both points of approval. For a marker that carries `up front`, the
      guard reads the milestone file at the local remote-tracking ref of
      the default branch of the base remote. If the file, the ref, or the
      slot cannot be read, the guard denies the merge. If the slot does not
      read `up front`, the guard denies the merge. The deny text names the
      slot value it read, or that none could be read, and the ref and path
      it read from. `hooks/tests` tests show that the guard allows
      `gh pr merge <N>` in one case: an `approved up front` marker for PR
      `<N>` and a default-branch slot of `up front`. The tests show a
      denial for each of these:
      - another PR number,
      - a slot of `at the end`, a slot of `—`, and a missing slot,
      - `up front` only in the working tree,
      - `up front` only on the local default branch,
      - no remote-tracking ref,
      - an absent file,
      - a marker for one milestone while only another milestone's slot
        reads `up front`.

      A legacy marker without `up front` behaves as before.
- [ ] AC5: Five surfaces state the up-front approval and the cases that go
      back to the merge question. Two are bullets: the approval bullet of the git
      model in `skills/shared/tracking-rules.md`, and "Merges are yours" in
      `README.md`. The others are
      `skills/shared/templates/claude-md-section.md`, the cairn section of
      `CLAUDE.md`, and a `CHANGELOG.md` entry. The
      verify slot passes as in AC7 of M202.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6

## Tasks

- [ ] T1: Rewrite IP1 in `cairn/DESIGN.md` and append the D-entry (RB
      tripwire: ip-touching). The user decided it at the plan gate.
- [ ] T2: Add the `Merge approval:` slot to
      `skills/shared/templates/milestone.md`. Add the merge question to the
      step-3 list of `skills/milestone-plan/SKILL.md` and the slot write to
      step 4.
- [ ] T3: `skills/milestone-review/SKILL.md` steps 5, 7, and 8: the
      route-back cases, the up-front path, the work-log line, the marker
      after green CI, and the end-of-run list of dispositions. Step 5 gives
      each finding its lens, rank, and disposition, and records the spawned
      lenses. Read the resume routes that parse the `step-7 approval:` line.
      A resume after a CI timeout finds the up-front line and re-derives CI.
- [ ] T4: The slot read, the deny text, and the docstring in
      `hooks/merge_guard.py`, with the `hooks/tests` tests of AC4.
- [ ] T5: The surfaces in AC5.
- [ ] T6: Run the verify slot and `cairn_validate`.
- [x] T7: Before T1, take RR15 recs 1 to 9 to the step-6 amendment stop. Recs 1 to 5 are route-backs: a substantive amendment, a false-reject, an IP touched or a D-entry written, a degraded review, and a CI fix after the PR opens. Rec 6 binds the approval per milestone, rec 7 is the IP1 wording, and rec 8 has the guard read the slot. Rec 9 fixes the wording of AC2, AC3, T3, and T4. The other choice to offer is dropping the up-front path.

## Work log

- 2026-10-03: created by /milestone-plan, in one run with M202.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) covered M202 and M203. The M202 work log has the result.
- 2026-10-03: plan gate chose one approval for each plan over a standing approval and over the end question, at the user's answer. Falsified by an up-front merge that the user reverts.
- 2026-10-03: implement started on branch m203-merge-approval-up-front, in the run after M202 merged. Untracked `tsconfig.json` left unstaged.
- 2026-10-03: T1 escalation offer (ip-touching): the user chose to escalate the IP1 change via `/milestone-brief` before T1 starts.
- 2026-10-03: blocked on RB15. The brief is committed on this branch, not on main, because the milestone's state already lives on the branch, and a main commit would conflict with it.
- 2026-10-03: RR15 ingested (Fable, advisory, 16 recommendations). Apply: recs 1 to 9. They add route-backs to the merge question, bind the approval per milestone, add the slot read to the guard, and change the IP1, AC2, AC3, T3, and T4 wording. These widen AC2 to AC4 and change the per-plan approval the user chose, so T7 records them for the step-6 amendment stop. Follow-up row: recs 10 to 13. Rejected as RR15 reasons: rec 14 (stronger marker binding exceeds the stakes, D-043), rec 15 (a D-entry alone, against IP2), and rec 16 (dropping the path, unless recs 1 to 5 do not ship).
- 2026-10-03: T7 amendment stop: the user chose to apply RR15 recs 1 to 9.
- re-audit: AC1 (full) — IP1's new text would cover docs-only commits, D-138 and D-144 not narrowed, "every check of the run passed" unbounded; fixed.
- re-audit: AC2 (full) — the "seen only after the merge" clause false under route-backs, no recommended option; fixed.
- re-audit: AC3 (full) — CI condition after the pre-push approval line, "substantive" left to judgment, dead M202 AC1 citation, slot copy and D-entry scope unnamed, no list for a chained run; fixed.
- re-audit: AC4 (full) — probes vary only the PR number and one slot value; fixed.
- re-audit: AC1 (full) — D-043 not annotated, a rulebook edit to the route-back list would change IP1 without the IP procedure.
- re-audit: AC2 (full) — RR15's "a re-cut asks again" dropped.
- re-audit: AC3 (full) — stop detection reads close blocks that are not on disk, "amendment line" undefined, a declined merge question does not route back, plan commit ambiguous, no-push clause worded as a ban.
- re-audit: AC4 (full) — probes do not vary the milestone file or the ref, deny text cannot name a slot it never read.
- 2026-10-03: stop at the second re-audit of AC1 to AC4 (repeated review-failure stop). Amended text not yet written.
- 2026-10-03: substantive amendment of AC1 to AC4 at the user's answer: the second reader's seven fixes applied, the "no stop fired" condition dropped (the user is present at each stop and types the resume), no third reader. T3 and T4 widened to match, T7 ticked.

## Decisions

- 2026-10-03 (RR15 Q1): An up-front answer approves the promise as the plan commit carries it, not the code. It satisfies IP1 only if that promise merges unchanged and the cases where the merge question adds information go back to it. The 323-to-1 figure was measured with the read in place. The real gain is an unattended run, because CI waits on the approval (D-138).
- 2026-10-03 (RR15 Q2, Q6): Six cases pass AC3 as written. The agent rejects a real finding as false. The agent makes a substantive amendment that it judges wording only. The agent narrows the scope. A plan chains several milestones. The review is degraded, with no spawned reviewers. The diff rewrites the gate machinery or an IP. A self-fixed defect return is an acceptable risk. The fix is to send each of these cases back to the merge question.
- 2026-10-03 (RR15 Q3): The approval binds each milestone, not the plan. One question can answer for several ids and lets the user hold any of them `at the end`. A re-cut asks again.
- 2026-10-03 (RR15 Q4): The marker was always written by the agent. The guard's PR regex already accepts the `up front` form, so AC4's test is a regression guard. A stronger tie would have the guard read the milestone's `Merge approval:` slot from the base remote's default branch, with the marker and the work-log line citing the plan commit.
- 2026-10-03 (RR15 Q5): RR15 recommends the IP1 wording "Nothing reaches the default branch without the user's explicit approval at a gate of the run: at the merge question, or in the plan question set for a milestone whose promise, as that plan committed it, then merges unchanged and with every check of the run passed." It rejects a D-entry alone with IP1 unchanged. It does not recommend dropping the up-front path, but only if recommendations 1 to 5 ship with M203.

## Review
