# M265: Close the tier check's five open edges

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP3
- **Resolves:** —
- **Surface tier:** user-facing — the shipped tier check and routing template change
- **Branch/PR:** m265-tier-check-edges, https://github.com/jmgirard/cairn/pull/277

## Goal

`/milestone-plan`'s tier check graduates the candidate row a trivial edit fixes, routes guest pull requests and `/milestone` §3 picks without a wrong second judgment, and the rulebook and routing template describe the route it takes.

## Scope

**In:** the five edges of the candidate row "Tier check edges" (M250 review). They are in `skills/milestone-plan/SKILL.md` step 1 and step 4, the git model in `skills/shared/tracking-rules.md`, records-hygiene §1, `skills/shared/templates/claude-md-section.md`, this repo's `CLAUDE.md`, one D-entry, and `CHANGELOG.md`. In both routing files the last bullet ("nothing reaches it without the user's explicit approval at the merge question") also names the tier chip for a trivial edit (amended at implement).

**Out:**
- `/hotfix`'s own resume routes for an unmarked, closed, or changes-requested PR. These stay in the candidate row "`/hotfix` has no resume route for an open PR".
- The pane hotfix Button, the pane fixes, and the open-PR audit. These stay candidate rows, at the user's choice in the question set.
## Acceptance criteria

- [x] AC1: `skills/milestone-plan/SKILL.md` step 1's trivial route matches each row of `cairn/ROADMAP.md`'s Candidates section whose short title the request quotes. It skips a row whose title a `planned`, `in-progress`, `blocked`, or `review` milestone file quotes. The trivial option's description names each matched row. The edit deletes a matched row it covers in full and narrows one it covers in part, as `/hotfix` step 7 does. In owner mode `cairn/ROADMAP.md` is then a file the edit touches, so the five checks and the `git commit -- <paths>` cover it. In guest mode the row changes on disk with no commit. Records-hygiene §1 names the trivial route as a completion that graduates its row.
- [x] AC2: The git model's default-branch bullet in `skills/shared/tracking-rules.md` names trivial-tier commits that the user approved at the tier chip, beside docs-only tracking commits and squash-merges. The same file's "Nothing reaches the default branch" bullet names that chip as an approval too. `git grep -n "only docs-only" -- skills README.md CLAUDE.md` prints no line. This grep checks one spelling only.
- [x] AC3: `skills/milestone-plan/SKILL.md` step 1 says that in guest mode the check does not run on a request that names a pull request. Examples are a PR URL, "PR 12", and "adopt PR 12". A bare `#N` stays an issue. For a PR whose head branch starts with `hotfix-`, the plan ends with a close block whose fenced command is `/hotfix` with the PR reference. For any other PR, the close block says that guest mode does not adopt a third party's PR.
- [x] AC4: `skills/milestone-plan/SKILL.md` step 1 names one more already-tiered invocation: a `/milestone-plan` disposition that the user selected in `/milestone` §3 earlier in this session. The check classifies it `milestone` without re-judging, and the work-log reason names `/milestone` §3.
- [x] AC5: The existing `/milestone-plan` bullet of `skills/shared/templates/claude-md-section.md` and of this repo's `CLAUDE.md` is reworded. It says that the plan can offer the hotfix or trivial route before its one question set. The template's Trivial bullet says that the direct commit is for owner mode and that guest mode leaves the edit on disk. The template's section stays at 29 lines or fewer, heading included. `git grep -n "One question set follows" -- . ':!cairn' ':!CHANGELOG.md'` prints no line.
- [x] AC6: `CHANGELOG.md`'s `## Unreleased` section has entries for row graduation on the trivial route (AC1), guest pull-request requests (AC3), and no second tier chip after a `/milestone` §3 pick (AC4). The router wording (AC5) has an entry under "Changes that affect existing repos". That entry says that an adopter's CLAUDE.md section keeps the old wording until the adopter updates it.

## Coverage

- AC1 → T1, T6
- AC2 → T3, T6
- AC3 → T2, T6
- AC4 → T2, T6
- AC5 → T4, T6, T7
- AC6 → T5

## Tasks

- [x] T1: In `skills/milestone-plan/SKILL.md` step 1, add the candidate-row match to the trivial-route checks and the trivial option's description (AC1). Reuse `/hotfix` step 1's match and step 7's delete-or-narrow wording by reference where it fits. Reword records-hygiene §1's hotfix sentence to name the trivial route in the same line, inside the module's 55-line, 4,000-byte budget (`wc -l -c`). Extend `skills/tests/test_plan_tier_check.py` to pin the new sentences.
- [x] T2: In step 1, add the guest pull-request clause (AC3) next to the issue clause, with the `gh pr view <N> --repo <base-repo> --json headRefName` read it needs. Add the §3 invocation to the already-tiered list and its form to step 4's `tier check:` line (AC4). Update the "Two invocations" sentences, their pins in `test_plan_tier_check.py`, and any `test_mutation_harness.py` entry that quotes them.
- [x] T3: Reword the two git-model bullets in `skills/shared/tracking-rules.md` (AC2). Re-run the hand-run guards that read that file: `test_default_branch_parameterized.py`, `test_gate_wording.py`, `test_plan_tier_check.py`.
- [x] T4: Reword the `/milestone-plan` and Trivial bullets of the template and the `/milestone-plan` bullet of `CLAUDE.md` (AC5). Count the template section's lines. Re-run `hooks/tests` (the guest injection reads the template) and `test_positioning_guard.py`.
- [x] T5: Append a D-entry to `cairn/DECISIONS.md` that annotates D-162. It records the git-model reconciliation, the guest pull-request rule, the §3 exemption, and the trivial route's row graduation. Write the AC6 CHANGELOG entries.
- [x] T6: Run both gating suites (`scripts/tests`, `hooks/tests`), `claude plugin validate`, `claude plugin test`, the marketplace validate, every hand-run `skills/tests` file that T1 to T4 touched, the AC2 and AC5 greps, and `python3 scripts/cairn_validate.py`.
- [x] T7: Review return 1: reword the template's Trivial bullet to name owner mode for the direct commit and guest mode for the on-disk edit, inside the 29-line section (AC5).

## Work log

- 2026-10-16: created by /milestone-plan.
- 2026-10-16: tier check: not run — work named at the question set.
- 2026-10-16: question set: which group of candidate rows — "Tier check fixes"; pane hotfix Button — left out (applies to the pane group only); the other two groups — kept as candidate rows.
- 2026-10-16: question set: the user chose the option that also closes "`/hotfix` keeps its own questions". Its premise is refuted: `skills/hotfix/SKILL.md` step 1 poses no chip, and the file's chips are the step-6 approval, the re-entry acceptance, and the Copilot findings chip. Post-merge hygiene deletes the row with that reason.
- 2026-10-16: collision check: absorbs the candidate "Tier check edges" in full. Extends archived M250. D-162's Consequences left the git-model sentence to a candidate row, so T5's entry annotates D-162 and supersedes nothing. D-108's door does not apply, because these are routing fixes and not a conduct rule about verification or records. No planned or in-progress milestone overlaps.
- 2026-10-16: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-16: lessons harvested: M112 (sweep every surface that restates the wording), M249 (a user-visible change owes a CHANGELOG task), M56 (a `skills/*/SKILL.md` edit runs both gating suites), M148 (reword the new sentence, never a pinned one), M169 (a guard that spells a forbidden phrase is in its own grep's domain).
- 2026-10-16: criteria audit (full mode, fresh Opus reader): 8 findings, all fixed. AC1 now deletes or narrows as `/hotfix` step 7 does and adds the records-hygiene §1 clause. AC2 names both git-model bullets and states that its grep checks one spelling. AC3 no longer plans a third party's PR as a milestone, which tracking-rules "Collaboration mode" forbids, and its work-log clause went with it. AC4 gained "earlier in this session". The D-entry moved to T5, because a recording act is not a deliverable property. AC5 rewords the existing bullets inside the 29-line template and its grep skips CHANGELOG.md. AC6 names its entries. The audit found no probe criteria and no proportionality problem.
- 2026-10-16: plan gate chose a close block for a guest PR request over planning the PR as a milestone because tracking-rules "Collaboration mode" routes a third party's PR to the maintainers; falsified by a guest user who needs to plan work that names a PR they did not open.
- 2026-10-16: plan gate chose matching a candidate row by its quoted short title over `/hotfix`'s "a row that describes the bug" judgment because a pane press sends the title and a string match needs no judgment; falsified by a trivial edit that fixes a row the request did not quote.
- 2026-10-16: plan gate chose to leave the routing template's merge-question bullet unchanged over rewording it because that bullet is about code outside a branch; falsified by a reader who takes it to forbid the trivial route's commit.
- 2026-10-16: implement: branch m265-tier-check-edges cut from origin/main at b0b2d50a. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-16: T1 done: step 1 gains a "Candidate-row match (trivial route)" paragraph that runs before the checks, so a matched row's ROADMAP edit is covered by them; the trivial option names each row. records-hygiene §1 re-wrapped to keep 54 lines (3,344 bytes). New guard method in `test_plan_tier_check.py`. Verify green (408 + hooks + 1777 mod tests).
- 2026-10-16: implement: the simple-english style hook reports pre-existing hits across whole files it sees (190 in `skills/milestone-plan/SKILL.md`). Only the added sentences are held to it, since rewriting untouched skill prose is outside this scope.
- 2026-10-16: T2 done: the guest pull-request clause sits after the issue clause, and its three close blocks (own `hotfix-` handoff, other PR, failed read) write nothing, so it needs no `tier check:` line form. The §3 pick is the third already-tiered invocation, and step 4's existing "`milestone` line naming the router" form covers it. Guard pins updated. No mutation-harness entry quoted the old sentences (`git grep`).
- 2026-10-16: T3 done: the default-branch bullet names trivial-tier commits approved at the tier chip and pushes them at once like docs-only ones; the merge-question bullet names that chip. `git grep -n "only docs-only" -- skills README.md CLAUDE.md` exits 1. Rulebook now 680 lines / 65,521 bytes; the baseline is re-seeded at its three sites (`skills/milestone/SKILL.md`, `test_cost_audit_line.py`, `test_mutation_harness.py`).
- 2026-10-16: T1 and T2 pins shown red: an in-memory probe deleted each of the 10 new clauses from the read text, one at a time. Each run failed its test, and the unmutated control passed. `test_plan_tier_check` stays exempt from the mutation registry as at M250.
- 2026-10-16: T4 done: the template's and `CLAUDE.md`'s `/milestone-plan` bullet now says the plan first offers a fitting hotfix or trivial route, then one question set. The template's Trivial bullet says guest mode leaves the edit on disk. Sections stay at 29 (template) and 26 (`CLAUDE.md`) lines. The AC5 grep exits 1. README.md already describes the tier question (its "Answer two questions in a run" bullet), so it is unchanged.
- 2026-10-16: T5 done: D-170 annotates D-162 with the four rule changes. CHANGELOG gains three Fixes entries (row graduation, guest PR requests, no second tier question after a §3 pick) and one "Changes that affect existing repos" entry for the routing wording. That entry says to update an old section by hand, because `/cairn-init` §3 repair "never rewrites content the repo authored".
- 2026-10-16: T6 done: scripts (408 OK), hooks (175 OK), skills/tests (787 OK), both `claude plugin validate` runs, `claude plugin test` (1777 pass, 0 fail), the AC2 and AC5 greps (both exit 1), and `cairn_validate` (all checks passed).
- 2026-10-16: claim audit: 22 claims read, 0 corrected — CHANGELOG.md, CLAUDE.md, skills/milestone-plan/SKILL.md, skills/milestone/SKILL.md, skills/shared/records-hygiene.md, skills/shared/templates/claude-md-section.md, skills/shared/tracking-rules.md.
- 2026-10-16: substantive amendment: Scope moves the routing files' last bullet from Out to In. The claim reader read it as conflicting with the new tracking-rules approval sentence, which is the plan's recorded falsifier for leaving it. Both files now name the tier chip beside the merge question. No criterion changed, so no re-audit is owed. The template section stays at 29 lines and `CLAUDE.md`'s at 27.
- 2026-10-16: claim reader side notes: a guest `CLOSED` unmerged `hotfix-` PR has no `/hotfix` arm (added to the candidate row "`/hotfix` has no resume route for an open PR"). A trivial-route narrowing does not say what happens to a `started #<n>` token, which only a guest `/hotfix` writes. That is left as is, since that token names another record and the trivial route does not own it.
- 2026-10-16: implement complete: after the amendment, hooks (175 OK), scripts (408 OK), skills/tests (787 OK), plugin validate, and `cairn_validate` passed again. Status set to review.
- 2026-10-16: review: Copilot arm opened PR #277 and requested Copilot (state query `none`, request exit 0).
- 2026-10-16: review return 1: AC5 fails as written. The template's Trivial bullet reads "commit directly to the default branch (in guest mode, leave the edit on disk)", which names guest mode but does not say the direct commit is for owner mode. The other AC text checks, both greps, `cairn_validate`, and the marketplace version check pass.
- 2026-10-16: implement: minor amendment adds T7 for review return 1 (Coverage AC5 gains T7).
- 2026-10-16: T7 done: the template's Trivial bullet now reads "in owner mode, commit to the default branch. In guest mode, leave the edit on disk." The section stays at 29 lines. hooks (175 OK), scripts (408 OK), skills/tests (787 OK), and both plugin validates pass. The mod code is unchanged since T6's `claude plugin test` run. Status set to review.
- 2026-10-16: review pass 2: resume route (d), PR #277 `OPEN` at head 9759948b with no box ticked. Branch contains origin/main.

## Review

Evidence on head 9759948b, 2026-10-16. Text checks are whitespace-collapsed substring reads of the named files, run by a stdin Python script.

- AC1: `skills/milestone-plan/SKILL.md` step 1 holds the "Candidate-row match (trivial route)" paragraph: quoted-short-title match, the live-milestone skip for `planned`/`in-progress`/`blocked`/`review`, delete-in-full and narrow-in-part "as `/hotfix` step 7 does", `cairn/ROADMAP.md` then a file the checks and commit cover, and the guest on-disk change. The paragraph sits before the chip and says "before the checks". The trivial option names each matched row. records-hygiene §1 names the trivial edit as its own completion (54 lines, 3,344 bytes). `test_plan_tier_check` OK. PASS.
- AC2: `skills/shared/tracking-rules.md`'s default-branch bullet reads "It accepts docs-only tracking commits, trivial-tier commits that the user approved at `/milestone-plan`'s tier chip, and squash-merges", and the approval bullet adds "or for a trivial-tier commit at `/milestone-plan`'s tier chip". `git grep -n "only docs-only" -- skills README.md CLAUDE.md` exit 1 (one spelling only, as AC2 states). PASS.
- AC3: step 1 says "In guest mode a request that names a pull request is not checked either", gives the PR URL, "PR 12", and "adopt PR 12" examples, keeps a bare `#N` an issue, routes a `hotfix-` head to a close block fencing `/hotfix` with the PR reference, and for any other PR a close block saying guest mode does not adopt a third party's PR. PASS.
- AC4: step 1 reads "The third is a `/milestone-plan` disposition that the user selected in `/milestone` §3 earlier in this session. The check classifies all three `milestone` without re-judging, and the work-log reason names the router." PASS.
- AC5: the template and `CLAUDE.md` `/milestone-plan` bullets read "Where a hotfix or trivial route fits, it offers that first. Then one question set comes". The template's Trivial bullet reads "in owner mode, commit to the default branch. In guest mode, leave the edit on disk." The template section, heading included, is 29 lines (`awk` from `## Project tracking`). `git grep -n "One question set follows" -- . ':!cairn' ':!CHANGELOG.md'` exit 1. PASS (failed on pass 1, fixed by T7).
- AC6: `CHANGELOG.md` `## Unreleased` has, under Fixes, "A direct edit from `/milestone-plan` removes the candidate row it fixes." (AC1), "In guest mode, `/milestone-plan` no longer sends a pull request to `/hotfix`." (AC3), and "A plan picked at `/milestone`'s triage gate asks no tier question." (AC4). Under "Changes that affect existing repos" it has "The routing section names the tier question." (AC5), which says "In a repo set up earlier, `CLAUDE.md` keeps the old wording." No entry names a milestone number. PASS.
