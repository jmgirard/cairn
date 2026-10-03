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

- [ ] AC1: IP1 in `cairn/DESIGN.md` states that the user gives explicit
      approval either in the plan question set or at the merge question. A
      D-entry records the user decision that changes IP1 (RB tripwire:
      ip-touching). The D-entry states that the up-front approval comes
      before the diff exists.
- [ ] AC2: The milestone template carries a `Merge approval:` header slot.
      Step 3 of `skills/milestone-plan/SKILL.md` lists merge approval among
      the questions of the set. The plan writes the slot from the answer,
      as `up front YYYY-MM-DD` or `at the end`.
- [ ] AC3: If all of these hold, `skills/milestone-review/SKILL.md`
      merges without the merge question:
      - the slot reads `up front`,
      - CI is green, or the rulebook rule for a PR with no CI runs applies,
      - each criterion has passing evidence,
      - no finding that the reviewers rank as real and in scope is left
        unfixed,
      - no stop in the AC1 list of M202 fired,
      - no condition of step 7 that adds to the merge question applies (a
        PR review that requests changes, a Driving RR shortfall, guest
        mode, a companion PR, an issue write from `Resolves:`).

      In that case, before the merge it writes the `step-7 approval:`
      work-log line marked `up front`. It also writes the marker
      `M<NNN> approved up front YYYY-MM-DD for PR #<N>`. Otherwise it asks the merge question as before. The close block after the
      merge lists each finding that went to a candidate row.
- [ ] AC4: The deny text of `hooks/merge_guard.py` names both points of
      approval. A `hooks/tests` test shows that the guard allows
      `gh pr merge <N>` under an `approved up front` marker that names PR
      `<N>`. The same test shows that the guard denies the merge for
      another PR number.
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
- [ ] T3: `skills/milestone-review/SKILL.md` steps 7 and 8: the up-front
      path, the work-log line, the marker, and the close-block list of
      deferred findings. Read the resume routes that parse the
      `step-7 approval:` line, so a resume after a CI timeout finds it.
- [ ] T4: The deny text in `hooks/merge_guard.py` (lines 140-147 today)
      and the `hooks/tests` test.
- [ ] T5: The surfaces in AC5.
- [ ] T6: Run the verify slot and `cairn_validate`.

## Work log

- 2026-10-03: created by /milestone-plan, in one run with M202.
- 2026-10-03: criteria audit (full mode, fresh Opus reader) covered M202 and M203. The M202 work log has the result.
- 2026-10-03: plan gate chose one approval for each plan over a standing approval and over the end question, at the user's answer. Falsified by an up-front merge that the user reverts.
- 2026-10-03: implement started on branch m203-merge-approval-up-front, in the run after M202 merged. Untracked `tsconfig.json` left unstaged.

## Decisions

## Review
