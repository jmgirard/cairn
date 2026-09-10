# M186: The PR opens after approval, so CI first runs on the head that merges

- **Status:** review
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

- [x] AC1: `/milestone-review` step 2 pushes nothing and opens no PR; the branch push and `gh pr create` with no `--draft` sit in step 8 — owner arm: after the step-7 approval line is committed, before the marker write and the CI wait; guest arm: on the handoff selection, the push plus `gh pr create --repo <base-repo> --head <fork-owner>:<slug>` is the handoff, with no `gh pr ready`, no marker, no CI wait — and the `Closes`/`Refs` body rule, the no-cairn-vocabulary rule, and the header PR-URL record move with the create. Evidence: the shipped step 2, 7, and 8 text read, with a stated walk of owner and guest arms naming the ordering each produces.
- [x] AC2: The step-7 merge chip's recommended option and the `step-7 approval:` work-log line name the branch and default branch, not a PR number (`Merge <branch> into <default-branch>`; `step-7 approval: <branch> approved for merge`), the guest chip likewise names the branch and base repo; resume route (a) reads the line by its prefix, and routes (c) and (d) name the post-approval open (route (c): re-run step 1, push, re-pose the chip, then step 8 skipping `gh pr create` when the header already names an open PR). Evidence: the shipped text read, with a walk of fresh-PR and pre-existing-PR entries.
- [x] AC3: The PR-conversation read runs exactly once per review or hotfix, at review step 7 or hotfix step 6 before the chip, only when the milestone header or the hotfix argument already names an open PR; a fresh PR opened at step 8 (hotfix step 6) is merged with no read, and each step says so in one sentence. Evidence: the shipped step text read.
- [x] AC4: `/hotfix` step 5 pushes nothing and opens no PR for an authored fix; step 6 on approval pushes, opens the PR with no `--draft` (`Fixes #N` when an issue exists; the guest arm's handoff selection is the push plus `gh pr create --repo <base-repo> --head <fork-owner>:hotfix-<slug>`, no `gh pr ready`), writes the marker, waits on CI, merges; the adopted-PR path and step 1's open-PR re-entry read unchanged except that the re-entry names the post-approval open. Evidence: the shipped step 1, 5, and 6 text read, owner and guest arms walked.
- [x] AC5: The sites that describe PR timing — `/milestone-review` steps 2/7/8 and resume routes (c)/(d), `/hotfix` steps 1/5/6, tracking-rules "Git and approval model" and "Collaboration mode", `/milestone-implement` step 9's CI line, README's issue-linkage sentence — describe the post-approval open; corroborated by `git grep -n -i -e "draft PR" -e "--draft" -e "gh pr ready" -e "so CI runs" -- ':!cairn' ':!skills/tests' ':!CHANGELOG.md'` returning no match (history under `cairn/` and past changelog entries stay as written, IP4).
- [x] AC6: The tracking-rules bullet "A branch push starts CI" states that the milestone or hotfix PR is opened after approval so a `pull_request`-triggered suite first runs on the head that merges rather than on every pre-approval push, and names the D-entry this milestone appends (T4).

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
- [x] T4: Append the D-entry (post-approval open; the serial CI wait at the gate as its cost; the ready-for-review workflow alternative rejected); re-seed the hand-run pins quoting the old wording (`skills/tests/test_resume_routing.py:95`, `test_mutation_harness.py:3459`, `test_issue_linkage.py:307`) and hand-run `python3 -m unittest discover skills/tests`, expecting no red beyond the 4 reds + 1 error recorded at M185's hygiene; run the two gating suites.

## Work log

- 2026-09-10: created by /milestone-plan. Criteria audit ran in full mode ([O] fresh reader): 17 findings — PR number presupposed at step 7, guest arm anchors, deferred-read ordering and marker semantics, AC4 unbounded and hitting IP4 history, "runs once" unguaranteed, missing D-entry, evidence axes — all disposed: reworded into AC1–AC6 above, the fresh-PR read dropped at the gate.
- 2026-09-10: plan gate chose opening the PR after approval over opening it just before the gate because the approval commit's push re-runs a `pull_request` suite regardless, so the early open buys one wasted run; falsified by a repo where the serial CI wait after approval is reported as the bottleneck of its milestone loop.
- 2026-09-10: plan gate chose reading the PR conversation only where a PR pre-exists over a second read after CI green because the second read re-poses the chip after the marker is written and adds a gate path; falsified by a bot reviewer's comment on a fresh PR being found, post-merge, to have named a defect the fan-out missed.
- 2026-09-10: plan gate chose the skill-side move over per-repo workflow config (checks gated on ready-for-review via `/cairn-init`) because it touches every adopting repo's workflows and needs the non-default `ready_for_review` trigger type; falsified by an adopting repo that cannot accept a serial CI wait at the gate.
- 2026-09-10: /milestone-implement started on `m186-pr-after-approval`; question gate skipped (the plan gate settled the three design choices; AC1–AC6 fix the wording).
- 2026-09-10: T1 done — review step 2 pushes nothing; step 7 chip and approval line name the branch (guest: `<slug>` and base repo), conversation read conditioned on a header-named open PR; step 8 opens the push + `gh pr create` (no `--draft`) before the marker, guest handoff = push + create, no `gh pr ready`; routes (a)/(c)/(d) reworded; the two fix-now "re-pushed" clauses now point at step 8's push. Scripts 391 / hooks 146 green.
- 2026-09-10: T2 done — hotfix step 5's authoring arm pushes nothing (guest draft note removed); step 6 reads the PR conversation only where a PR pre-exists, names the branch in the chip for an unopened fix, pushes and opens the PR ready after approval, guest handoff = push + create; step 1's owed-items sentence names step 6's post-approval open. Both skills reworded to avoid the literal tokens AC5's grep forbids. Scripts 391 / hooks 146 green.
- 2026-09-10: T3 done — tracking-rules "A branch push starts CI" bullet states the post-approval open and names D-138, the Collaboration-mode create and handoff bullets follow; implement step 9's CI line names the post-approval open; README's conversation-read and issue-linkage sentences reworded; changelog entry under Unreleased "Changes that affect existing repos". AC5's grep returns no match (exit 1). Scripts 391 / hooks 146 green.
- 2026-09-10: minor amendment — T4's pin list grew from the three the plan named to nine: the hand-run suite also pinned the old wording in `test_pr_conversation_gate.py` (four tests: read-once, route (c) re-run, hotfix authored-and-adopted, README both-gates), `test_resume_routing.py`'s route (a) and hotfix owed-items strings, `test_issue_linkage.py`'s PR-body regex, and the matching mutation-harness blocks; all re-seeded to the shipped wording.
- 2026-09-10: T4 done — D-138 appended (post-approval open; serial CI wait as the cost; the ready-for-review workflow, the pre-gate open, and the post-CI read rejected with their reopening observations); hand-run `skills/tests`: 661 tests, 4 reds + 1 error, the same set M185's hygiene recorded (lesson-graduation, two default-branch recipe pins, hotfix two-way-check sentence, and the harness error for the recipe pin). Scripts 391 / hooks 146 green; `cairn_validate` all checks passed.
- 2026-09-10: claim audit: 47 claims read, 3 corrected — skills/milestone-review/SKILL.md (step 8's header PR-URL record now a docs-only commit left unpushed, so the first `pull_request` run is on the head that merges), skills/hotfix/SKILL.md (step 6's "push and open the PR first" → "before the marker write below"), CHANGELOG.md (the work-log line names the branch only, not the default branch). Deviation: the one re-read ran in a second fresh [O] reader, not the first — this harness exposes no tool to continue a finished subagent; all three corrections hold. Suites unchanged after the corrections; AC5's grep still empty.
- 2026-09-10: all tasks checked; status → review.

## Decisions

## Review

_2026-09-10, on branch `m186-pr-after-approval` at 5e80c2f; main not moved since the cut._

- AC1 — pass. Step 2 (review `SKILL.md:87-91`) states nothing is pushed or opened and points at step 8. Owner walk: step 7 commits the approval line → step 8 `git push -u origin <branch>` → `gh pr create` ready, `Closes`/`Refs` body from the `Resolves:` slot → header PR-URL record (unpushed docs commit) → marker → CI wait → merge (`:426-447`). Guest walk: handoff selection → push to fork → `gh pr create --repo <base-repo> --head <fork-owner>:<slug>` ready, no ready-marking, no marker, no CI wait; PR URL on disk (`:466-478`).
- AC2 — pass. Chip `Merge <branch> into <default-branch>`; line `step-7 approval: <branch> approved for merge` (`:400-409`); guest chip `Hand <slug> to the maintainers of <base-repo>` (`:414-424`). Route (a) reads the prefix (`:42-44`). Fresh-PR entry: route (d) → step 1 → step 8 opens. Pre-existing-PR entry: route (c) → step 1, push, chip re-posed, step 8 skipping `gh pr create` (`:62-73`).
- AC3 — pass. Review read conditioned on a header-named open PR, "at most once per review, here", fresh PR "merged with no read" (`:364-368`); hotfix read "only when a PR already exists", authored PR "opened below, after the chip, and is merged with no read — the read runs at most once per hotfix, here" (hotfix `:176-189`).
- AC4 — pass. Step 5 authoring arm pushes nothing (`:149-152`); step 6 chip `Merge hotfix-<slug> into <default-branch>` for an unopened fix, push + `gh pr create` ready with `Fixes #N` before the marker write at `:218`, then CI wait and merge (`:189-203`); guest handoff = push to fork + create against base, no ready-marking (`:227-236`). Adopted-PR path (`:153-172`) unchanged (diff read); step 1's owed-items sentence names step 6's post-approval open (`:84-91`).
- AC5 — pass. The grep `git grep -n -i -e "draft PR" -e "--draft" -e "gh pr ready" -e "so CI runs" -- ':!cairn' ':!skills/tests' ':!CHANGELOG.md'` returns nothing (exit 1). Implement step 9 CI line (`:211-218`), README `:296-301` and `:306-308`, tracking-rules `:238-244` and `:314-323` all describe the post-approval open.
- AC6 — pass. Tracking-rules bullet "A branch push starts CI" (`:238-244`) states the PR is opened after approval so a `pull_request` suite first runs on the head that merges rather than on every pre-approval push, and cites D-138; `### D-138` heading present at `cairn/DECISIONS.md:5103`.
- Verify slot: scripts 391 OK, hooks 146 OK. Hand-run `skills/tests`: 661, 4 fails + 1 error, the M185 baseline set. `cairn_validate`: all checks passed. No Driving RR.
- Consistency gate: `cairn_validate` exit 0 (all PASS/OK); no DESIGN principle changed → `cairn_impact` skipped; generic profile → no toolchain checks.
- Independent review, three lenses (user-facing tier). [S] blame-history: no findings (M177's read narrowed deliberately and recorded in D-138). [S] prior-PR-comments: no prior-review evidence. [O] diff-bug, 8 findings ranked:
  - F1 (review step 8): the unpushed header PR-URL record is destroyed with the local branch at a `--delete-branch` merge, so the resume routes and `/milestone` §2, keyed on a header URL, cannot fire after a merge whose session died before hygiene — fix now: the branch name is the durable key; resume routing, `/milestone` §2, and step 9's summary fall back to `gh pr list --head <branch>`.
  - F2 (review step 8, hotfix step 6): a PR created seconds before `gh pr checks` can report no checks before GitHub registers them, and the no-checks rule would merge without CI — fix now: where the profile does not declare the repo CI-less, re-read `gh pr checks` after a short wait before taking the no-checks case.
  - F3 (review step 8 parenthetical vs step 9 and the archive template): the summary's `PR #<N> <url>` cannot come from the local file once the branch is gone — fix now: folded into F1's step-9 fallback.
  - F4 (hotfix step 6): no skip-the-create clause for the PR-reference re-entry of an authored fix, where `gh pr create` on a branch with an open PR errors — fix now: the same parenthetical review step 8 carries.
  - F5 (D-138): the unpushed-record choice was absent from the entry — fix now: one Consequences sentence added (the entry is unmerged, so this is authoring, not a history edit).
  - F6 (implement step 9): the return-from-review clause now holds only between the post-approval open and the merge — fix now: reworded to say so.
  - F7 (both creates): a bare `gh pr create` prompts and fails without a terminal, now on the post-approval critical path — fix now: `--title`/`--body` spelled out.
  - F8 (review step 7): "at most once per review" is false across a route-(c) resume — fix now: "once per pass through this gate". AC3's "exactly once per review" evidence stands per pass; the user should eyeball whether the criterion's "per review" meant per pass.
  - Return floor: no finding demonstrates a criterion failing inside its domain; F1 is a load-bearing defect in what the skill does for a resumed session and was fixed at the gate, no return.
- Fix-now re-check: scripts 391 OK, hooks 146 OK; `skills/tests` back to the baseline 4 + 1 after two pins re-seeded (`test_reads_pr_state_before_step_one`, `test_merged_review_milestone_is_hygiene_owed`); AC5's grep still empty; `cairn_validate` passes.
- PR-conversation read: not run — the header names no PR (the PR opens at step 8).
