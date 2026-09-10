# M186: The PR opens after approval, so CI first runs on the head that merges

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, GP1
- **Resolves:** —
- **Surface tier:** user-facing — skill conduct every adopting repo's review and hotfix run under
- **Branch/PR:** m186-pr-after-approval

## Goal

Review and hotfix push the branch and open the pull request only after the user approves at the merge gate, so a `pull_request`-triggered suite first runs on the head that merges instead of on every pre-approval push.

## Scope

**In:** `/milestone-review` step 2 stops pushing and opening a draft PR; the push and `gh pr create` (ready, never draft) move to step 8 after the approval line is committed, before the marker write and the CI wait, carrying the `Closes`/`Refs` body rule, the no-cairn-vocabulary rule, and the header PR-URL record; the step-7 merge chip and its `step-7 approval:` work-log line name the branch, not a PR number, and resume routes (a)/(c)/(d) read accordingly; the guest handoff becomes the push plus the create; the M177 PR-conversation read runs only where a PR already exists; `/hotfix` steps 5–6 make the same move for an authored fix, guest arm included; the tracking-rules git-model bullet and the README/implement sites that describe PR timing follow; one D-entry; the hand-run prose pins quoting the old wording re-seeded.

**Out:** a post-CI conversation read of a fresh PR (gate: read only pre-existing PRs — a bot reviewer's comment on a fresh PR is not read by cairn); per-repo workflow config gating checks on ready-for-review (gate: dropped, rejected alternative in the work log); the adopted-external-PR path of `/hotfix` (its PR already exists; unchanged); branch-protection interplay (candidate row "Branch-protection compatibility").

## Acceptance criteria

- [ ] AC1: `/milestone-review` step 2 pushes nothing and opens no PR; the branch push and `gh pr create` with no `--draft` sit in step 8 — owner arm: after the step-7 approval line is committed, before the marker write and the CI wait; guest arm: on the handoff selection, the push plus `gh pr create --repo <base-repo> --head <fork-owner>:<slug>` is the handoff, with no `gh pr ready`, no marker, no CI wait — and the `Closes`/`Refs` body rule, the no-cairn-vocabulary rule, and the header PR-URL record move with the create. Evidence: the shipped step 2, 7, and 8 text read, with a stated walk of owner and guest arms naming the ordering each produces.
- [ ] AC2: The step-7 merge chip's recommended option and the `step-7 approval:` work-log line name the branch and default branch, not a PR number (`Merge <branch> into <default-branch>`; `step-7 approval: <branch> approved for merge`), the guest chip likewise names the branch and base repo; resume route (a) reads the line by its prefix, and routes (c) and (d) name the post-approval open (route (c): re-run step 1, push, re-pose the chip, then step 8 skipping `gh pr create` when the header already names an open PR). Evidence: the shipped text read, with a walk of fresh-PR and pre-existing-PR entries.
- [ ] AC3: The PR-conversation read runs exactly once per review or hotfix, at review step 7 or hotfix step 6 before the chip, only when the milestone header or the hotfix argument already names an open PR; a fresh PR opened at step 8 (hotfix step 6) is merged with no read, and each step says so in one sentence. Evidence: the shipped step text read.
- [ ] AC4: `/hotfix` step 5 pushes nothing and opens no PR for an authored fix; step 6 on approval pushes, opens the PR with no `--draft` (`Fixes #N` when an issue exists; the guest arm's handoff selection is the push plus `gh pr create --repo <base-repo> --head <fork-owner>:hotfix-<slug>`, no `gh pr ready`), writes the marker, waits on CI, merges; the adopted-PR path and step 1's open-PR re-entry read unchanged except that the re-entry names the post-approval open. Evidence: the shipped step 1, 5, and 6 text read, owner and guest arms walked.
- [ ] AC5: The sites that describe PR timing — `/milestone-review` steps 2/7/8 and resume routes (c)/(d), `/hotfix` steps 1/5/6, tracking-rules "Git and approval model" and "Collaboration mode", `/milestone-implement` step 9's CI line, README's issue-linkage sentence — describe the post-approval open; corroborated by `git grep -n -i -e "draft PR" -e "--draft" -e "gh pr ready" -e "so CI runs" -- ':!cairn' ':!skills/tests' ':!CHANGELOG.md'` returning no match (history under `cairn/` and past changelog entries stay as written, IP4).
- [ ] AC6: The tracking-rules bullet "A branch push starts CI" states that the milestone or hotfix PR is opened after approval so a `pull_request`-triggered suite first runs on the head that merges rather than on every pre-approval push, and names the D-entry this milestone appends (T4).

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1, T2
- AC4 → T2
- AC5 → T1, T2, T3
- AC6 → T3, T4

## Tasks

- [x] T1: Rewrite `skills/milestone-review/SKILL.md` step 2 (one sentence: nothing pushed or opened here, the reason, pointer to step 8), step 7 (chip and approval-line wording naming the branch; conversation read conditioned on a pre-existing PR), step 8 (push, create, body rules, header record, then marker, CI wait, merge; guest handoff = push + create), and the resume routes (a)/(c)/(d) at `SKILL.md:36-72`.
- [x] T2: Rewrite `skills/hotfix/SKILL.md` step 5 (`SKILL.md:148-153`: no push, no PR, guest note removed), step 6 (push + create after approval; conversation read conditioned on an existing PR; guest handoff = push + create, `SKILL.md:220-229`), and step 1's open-PR re-entry sentence.
- [x] T3: Update tracking-rules `Git and approval model` bullet (`tracking-rules.md:238-246`) and `Collaboration mode` (`:311-320`), `skills/milestone-implement/SKILL.md:211-217`, README `:303`; add a changelog entry under the development version; run AC5's grep.
- [ ] T4: Append the D-entry (post-approval open; the serial CI wait at the gate as its cost; the ready-for-review workflow alternative rejected); re-seed the hand-run pins quoting the old wording (`skills/tests/test_resume_routing.py:95`, `test_mutation_harness.py:3459`, `test_issue_linkage.py:307`) and hand-run `python3 -m unittest discover skills/tests`, expecting no red beyond the 4 reds + 1 error recorded at M185's hygiene; run the two gating suites.

## Work log

- 2026-09-10: created by /milestone-plan. Criteria audit ran in full mode ([O] fresh reader): 17 findings — PR number presupposed at step 7, guest arm anchors, deferred-read ordering and marker semantics, AC4 unbounded and hitting IP4 history, "runs once" unguaranteed, missing D-entry, evidence axes — all disposed: reworded into AC1–AC6 above, the fresh-PR read dropped at the gate.
- 2026-09-10: plan gate chose opening the PR after approval over opening it just before the gate because the approval commit's push re-runs a `pull_request` suite regardless, so the early open buys one wasted run; falsified by a repo where the serial CI wait after approval is reported as the bottleneck of its milestone loop.
- 2026-09-10: plan gate chose reading the PR conversation only where a PR pre-exists over a second read after CI green because the second read re-poses the chip after the marker is written and adds a gate path; falsified by a bot reviewer's comment on a fresh PR being found, post-merge, to have named a defect the fan-out missed.
- 2026-09-10: plan gate chose the skill-side move over per-repo workflow config (checks gated on ready-for-review via `/cairn-init`) because it touches every adopting repo's workflows and needs the non-default `ready_for_review` trigger type; falsified by an adopting repo that cannot accept a serial CI wait at the gate.
- 2026-09-10: /milestone-implement started on `m186-pr-after-approval`; question gate skipped (the plan gate settled the three design choices; AC1–AC6 fix the wording).
- 2026-09-10: T1 done — review step 2 pushes nothing; step 7 chip and approval line name the branch (guest: `<slug>` and base repo), conversation read conditioned on a header-named open PR; step 8 opens the push + `gh pr create` (no `--draft`) before the marker, guest handoff = push + create, no `gh pr ready`; routes (a)/(c)/(d) reworded; the two fix-now "re-pushed" clauses now point at step 8's push. Scripts 391 / hooks 146 green.
- 2026-09-10: T2 done — hotfix step 5's authoring arm pushes nothing (guest draft note removed); step 6 reads the PR conversation only where a PR pre-exists, names the branch in the chip for an unopened fix, pushes and opens the PR ready after approval, guest handoff = push + create; step 1's owed-items sentence names step 6's post-approval open. Both skills reworded to avoid the literal tokens AC5's grep forbids. Scripts 391 / hooks 146 green.
- 2026-09-10: T3 done — tracking-rules "A branch push starts CI" bullet states the post-approval open and names D-138, the Collaboration-mode create and handoff bullets follow; implement step 9's CI line names the post-approval open; README's conversation-read and issue-linkage sentences reworded; changelog entry under Unreleased "Changes that affect existing repos". AC5's grep returns no match (exit 1). Scripts 391 / hooks 146 green.

## Decisions

## Review
