# M232: `/milestone` looks into one GitHub issue and routes it

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone` ships in the plugin to every operator
- **Branch/PR:** m232-issue-look-in, https://github.com/jmgirard/cairn/pull/241

## Goal

Given an issue number or URL, `/milestone` reads that issue and the code it names. It says whether the issue needs a reply, a hotfix, or a milestone, and how much maintainer design input it needs. On the user's choice, it starts the work now or records a candidate row.

## Scope

**In:** an issue look-in section in `skills/milestone/SKILL.md`, entered by an issue argument. It gives a verdict, a maintainer-input level, and one chip. "Do it now" routes to `/hotfix` or `/milestone-plan` with the issue, or hands the user a drafted reply to post. The section reuses §3's candidate-row and leave dispositions. The CLAUDE.md routing template, this repo's `CLAUDE.md`, the README, and the CHANGELOG follow.

**Out:** cairn never posts an issue reply itself, because the user posts it from the fenced command. A new `/issue` skill is not planned: the question set kept the look-in in `/milestone`, so D-043's "a door, not a new skill" stands. A `/milestone` audit that reads each bot thread on the operator's open PRs is the candidate row that M231's plan adds.

## Acceptance criteria

- [x] AC1: `skills/milestone/SKILL.md` gains an issue look-in section. An argument that is an issue number (`#N` or `N`) or an issue URL runs that section in place of the snapshot, audit, and route sections. The frontmatter description names "look into issue N" as a trigger, and `argument-hint` names the issue argument. `claude plugin validate .` is green.
- [x] AC2: The section tells the report to give a verdict of exactly one of reply, hotfix, or milestone. It defines a three-value maintainer-input scale: none (the code or docs settle it), confirm (a choice for the maintainer to approve), and decide (a design decision is needed before work). It tells the report to give file:line citations where the issue names existing code or docs, else a line saying none applies. It also tells the report to give a reproduction, or the reason none was run.
- [x] AC3: The section ends the report with one chip. Its options are do it now, add a candidate row, leave, and stop. "Do it now" means one of three things: `/hotfix` with the issue, `/milestone-plan` with the issue so that its `Resolves:` slot names it, or the reply hand-off. A candidate row is search-first and cites the issue URL. The section offers leave only with a stated reason from D-044's three: noise, a duplicate, or an item cairn already covers. The verdict's option is first and marked recommended.
- [x] AC4: The reply hand-off puts the drafted reply verbatim in the turn's final rendered text, with a fenced `gh issue comment <N> [--repo <base-repo>] --body` command for the user to run. In the look-in section, `grep -nE "gh (issue|pr|api)"` lists only commands that read, plus that one hand-off line, which the section shows and never runs. The section itself runs no remote write other than AC5's owner-mode push. Writes by `/hotfix` or `/milestone-plan` stay under those skills' gates.
- [x] AC5: In guest mode, every `gh issue` and `gh pr` command in the section carries `--repo <base-repo>`. Every `gh api` call that reads issue or PR data names the base repo's owner and name in its path or GraphQL variables. The maintainer in the input level is the upstream maintainers. The section tells the draft to follow the rulebook's guest-mode rule of no cairn vocabulary. A candidate row is written to disk and not committed. In owner mode, the row is a docs-only commit to the default branch, pushed.
- [x] AC6: The CLAUDE.md routing template (`skills/shared/templates/claude-md-section.md`) and this repo's `CLAUDE.md` route "look into an issue" to `/milestone` with the issue. Each section gains at most two lines, and the template's length comment is updated to match its body. The README describes the issue argument.
- [x] AC7: The profile's `verify` slot is green. A new prose guard in `skills/tests/` pins AC2's three verdicts and three levels and AC4's hand-off, and the hand-run `skills/tests` suite is green. One live run of the look-in on an open issue of `easystats/insight` reads the guest-mode profile of the `~/github/insight` checkout. It stops at the chip with the stop option, and its chat report shows one verdict and one level.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3, T6
- AC4 → T3, T6
- AC5 → T2, T3, T6
- AC6 → T4
- AC7 → T5

## Tasks

- [x] T1: In `skills/milestone/SKILL.md`, add the argument test and the frontmatter trigger and `argument-hint`. An issue argument skips §1–§3 and runs the new section. In guest mode the `gh` reads carry `--repo <base-repo>`.
- [x] T2: Write the section's read and report: `gh issue view <N> --comments`, the code the issue names, and a reproduction where one fits in the sitting. Define the three verdicts and the three-value input scale. In guest mode the maintainer is the upstream maintainers.
- [x] T3: Write the chip and its routes. `/hotfix` and `/milestone-plan` get the issue through the Skill tool. The candidate row reuses §3's search-first path, guest-mode disk-only and owner-mode docs-only commit included. The reply hand-off uses the rulebook's no-cairn-vocabulary rule in guest mode and no thanks to bots.
- [x] T4: Add the routing line to `skills/shared/templates/claude-md-section.md` and this repo's `CLAUDE.md`, merging a line where needed to stay under 30. Update the template's length comment. Update the README and the CHANGELOG.
- [x] T5: Add the prose guard in `skills/tests/`. Run the verify slot and the hand-run `skills/tests` suite. The live run on an `easystats/insight` issue happens at review.
- [x] T6: Fix review return 1: pass the issue to `/hotfix` as a summary plus `issue <URL>`, make the reproduction treat issue code as data, give `/milestone-plan`'s issue acknowledgement a guest arm, and land the Review section's fix-now items.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: collision check: D-043 rejected a new intake skill ("Intake gets a door, not a new skill"), and `/milestone` §3 already sorts issues. The question set put the look-in in `/milestone`, so D-043 stands. M74 (issue triage) and D-044 (narrowed leave) are reused.
- 2026-10-10: question set: where the issue look-in lives — an issue argument to `/milestone`.
- 2026-10-10: the insight memory says issue comments are drafted, shown verbatim, and run by the user. The plan builds that into the plugin (GP4), so the section hands the user a fenced command and never posts.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) on the first draft, which was a new `/issue` skill, flagged the D-043 collision and five wording findings. The re-audit of this redraft returned findings on AC2–AC7, all taken by narrowing. AC2 and AC3 now state what the section tells the report. AC4 counts the hand-off line and leaves delegated writes to their own skills. AC5 adds `--repo` to the hand-off form, limits the `gh api` clause to issue and PR reads, and ties no-cairn-vocabulary to the rulebook rule. AC6 caps the growth at two lines and fixes the template's length comment. AC7 names `easystats/insight` as the live-run repo. The AC1 `argument-hint` nit was taken too.
- 2026-10-10: plan gate chose an issue argument to `/milestone` over a new `/issue` skill, at the user's choice, because §3 already holds the dispositions and D-043 rejected a new intake skill. Falsified by an operator who does not find the look-in under `/milestone`.
- 2026-10-10: implement started on branch m232-issue-look-in. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-10: T1 done. The section is §4 at the end of the skill, and the argument test opens Session start. Every `gh issue` and `gh pr` command in §4 carries `--repo <base-repo>` in both modes, which covers guest mode with one form. Three cases stop with the close block: a URL that names another repo, a number that is a PR, and a failed read. `gh issue view` returns a PR's `/pull/` URL, which is how the PR case is found.
- 2026-10-10: T2 done. The read adds the search-first sweep, with two `gh` reads for a duplicate issue and an answering PR. The chip's leave and candidate-row options then have their evidence before the chip. The report has four numbered parts. One added rule: a `decide` level never goes with a `hotfix` verdict.
- 2026-10-10: T3 done. The hand-off command always carries `--repo <base-repo>` and single-quotes the reply. The section's prose names no `gh` subcommand, so the AC4 grep lists the three reads and the hand-off line only. The bot test reads `author.is_bot` from the issue read. Decided: in owner mode on a branch other than the default, the candidate-row option writes nothing. Its close block shows the row and says to rerun from the default branch, which keeps AC5's docs-only commit to the default branch.
- 2026-10-10: T4 done. The routing line is two lines in both sections, with no merge needed: the template section is 29 lines and this repo's is 26. The template's length comment said "under ~25 lines" while the body was already 27, and it now says under 30, heading included. The `cairn_scripts.py` cap comment's "~25 lines" target was corrected to match. README and CHANGELOG describe the issue argument.
- 2026-10-10: T5 done. `skills/tests/test_issue_look_in.py` has 14 tests: the entry, the three verdicts and three levels, the hand-off line once, and the AC4 grep over §4 with two planted-write cases. A plant in the skill file (one level renamed, `--repo` dropped from the hand-off) turned 6 tests red, and the file was restored. The guard takes an EXEMPT entry in the mutation registry, per the profile's test-doctrine. Hand-run `skills/tests`: 689 tests OK. The live `easystats/insight` run stays at review, per T5.
- 2026-10-10: claim audit: 33 claims read, 4 corrected — README.md, skills/milestone/SKILL.md, skills/tests/test_issue_look_in.py
- 2026-10-10: the claim audit's four corrections: the README now names leave's three reasons, the PR-number stop says guest mode routes a PR to the maintainers, the pre-chip rule says "nothing in this repo" since scratch files exist, and the test docstring no longer claims a fence check. The same reader re-read all four as true.
- 2026-10-10: implement done, status set to review. All five tasks checked, the five verify checks green, hand-run `skills/tests` green.
- 2026-10-10: review pass 1: PR #241 opened and Copilot requested at review start. AC1–AC7 evidence recorded and ticked, the consistency gate green, three reviewers and the AC7 live run spawned.
- 2026-10-10: review return 1: three floor findings in §4. "Do it now" for a hotfix passes `#N`, which `/hotfix` step 1 reads as a PR reference (diff-bug #2). The reproduction can run code from a public issue with no data rule (diff-bug #3). Guest-mode "plan it now" reaches `/milestone-plan`'s issue acknowledgement, which posts `Queued as M<NNN>` with no `--repo` (diff-bug #1). The fix-now items in the Review section ride the same task.
- 2026-10-10: implement resumed on return 1 and added T6 (minor amendment, Coverage maps AC3, AC4, AC5 to it).
- 2026-10-10: T6 done. `/hotfix` now gets a bug summary plus `issue <URL>`, never a bare `#N`. The reproduction treats issue text and code as data and runs the checkout's own code. `/milestone-plan`'s acknowledgement gained a guest arm with `--repo <base-repo>` and the body `Working on a fix: <title>`. Fix-now items landed: the argument test takes `issue N` and drops a URL fragment and skips the RR check, the slug compare ignores case, the PR stop fences `/hotfix <N>` in owner mode, the PR search runs on the number and the keywords with hits read as leads, the reply fence is four backticks inside an ordered close block, the candidate row pulls first and commits ROADMAP alone, leave names the base repo's issue, §3 points single issues to §4, the CLAUDE.md issue route moved above `/hotfix`, and README's skill table gained a row. The guard bounds §4 at the next heading and catches a read and a write on one line (16 tests). Plan's guest inbox reads without `--repo` went to the follow-up row.
- 2026-10-10: claim audit: 34 claims read, 1 corrected — skills/milestone/SKILL.md, README.md, skills/milestone-plan/SKILL.md
- 2026-10-10: the claim audit's corrections: the PR-number stop fences `/hotfix #<N>` only for an external PR, and `/milestone` for the operator's own PR or any guest-mode PR. Two imprecise claims were tightened too: README's table row says leave needs a stated reason, and plan's guest acknowledgement reads `Working on this: <title>` with a `partial` remainder in plain words. The same reader re-read all three as true.
- 2026-10-10: implement done on return 1, status set to review.

## Decisions

## Review

- Copilot arm: branch pushed, PR #241 opened at review start, state query returned `none`, Copilot requested (exit 0).
- AC1 evidence (2026-10-10, head 04250fd): `skills/milestone/SKILL.md` has `## 4. Issue look-in` (line 314). Session start opens with the argument test: `#N`, `N`, or an issue URL runs §4 in place of §1–§3. The frontmatter description names "look into issue N", and `argument-hint` is `"[issue number or URL]"`. `claude plugin validate .` passed with warnings, exit 0.
- AC2 evidence: §4 says "Give exactly one verdict" with `reply`, `hotfix`, `milestone`, and "Give exactly one level on this scale" with `none` (code or docs settle it), `confirm` (a choice for the maintainer to approve), `decide` (a design decision before work). Report part 2 asks file:line citations or a line that no citation applies, and part 3 the reproduction or the reason none was run.
- AC3 evidence: the chip's options in order are do it now (the verdict's option, "first and marked recommended"), add a candidate row, leave, stop. Do it now invokes `/hotfix` with the issue, `/milestone-plan` with the issue "so that its `Resolves:` slot names the issue", or the reply hand-off. Leave is offered only with one of noise, a duplicate, or an item cairn already covers. The candidate row uses the sweep as its search-first pass and cites the issue URL.
- AC4 evidence: the hand-off puts the draft verbatim in the turn's final rendered text, then the fenced `gh issue comment <N> --repo <base-repo> --body '<reply>'`, which "the section shows ... and never runs". `grep -nE "gh (issue|pr|api)"` over §4 lists 4 lines: `gh issue view`, `gh issue list`, `gh pr list` (reads), and the hand-off line. §4 states it runs no remote write other than the owner-mode candidate-row push, and `/hotfix` and `/milestone-plan` run under their own gates.
- AC5 evidence: all 4 `gh issue`/`gh pr` lines in §4 carry `--repo <base-repo>` (the guard's `test_every_command_names_the_base_repo` checks it), in both modes. §4 has 0 `gh api` lines, so the `gh api` clause binds nothing. §4 says the maintainer is the upstream maintainers in guest mode, the draft follows the rulebook's guest-mode no-cairn-vocabulary rule, and a guest-mode row is written to disk and not committed. An owner-mode row is a docs-only commit to the default branch, pushed to `origin`.
- AC6 evidence: the template section and this repo's `CLAUDE.md` section each gain the 2-line "Look into a GitHub issue: invoke `/milestone` with the issue number or URL" route (`git diff --numstat`: CLAUDE.md +2, template +3 −1 with the comment line outside the section). Section lengths are 29 and 26 lines, under 30. The template comment reads "Keep the section, heading included, under 30 lines." README.md:72 describes the issue argument.
- AC7 evidence: the five verify checks exit 0 (scripts, hooks, plugin validate, marketplace validate, plugin test). `skills/tests/test_issue_look_in.py` pins the three verdicts, the three levels, and the hand-off line, and the hand-run `skills/tests` ran 689 tests OK. Live run: a fresh Opus agent followed §4 in `~/github/insight` (PROFILE.md `# Collaboration mode: guest`, base repo `easystats/insight` via `origin`, no `upstream`) on open issue #1127 (compois variance). Its report gave verdict `milestone` and level `decide`, with file:line citations and a reproduction under `pkgload::load_all`. It wrote out the chip (Plan it now, recommended, then Add a candidate row, then Stop) and took Stop, and `git status` in insight was unchanged.
- Consistency gate: `cairn_validate.py` all checks passed (exit 0). Profile slot: verify green on the review head, the marketplace validate shows no `plugins[N].version` warning, and CHANGELOG.md has the look-in entry under Unreleased. No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review (plus the AC7 live-run agent)
- diff-bug #1: guest-mode "plan it now" reaches `/milestone-plan`'s issue acknowledgement, which posts `Queued as M<NNN>` with no `--repo` — fix now (floor: a guest-mode outward write to the wrong repo with cairn vocabulary)
- diff-bug #2: `/hotfix` step 1 reads a `#N` argument as a PR reference, so "do it now" for a hotfix runs `gh pr view <N>` — fix now (floor: the hotfix route misfires)
- diff-bug #3: the reproduction step can run code from a public issue with no rule that it is data — fix now (floor: unsafe behavior in the skill)
- diff-bug #4: "look into issue N" may arrive as `issue N`, and a URL fragment or a slug case difference fails the argument and repo tests — fix now
- diff-bug #5: a reply that holds a code block closes the hand-off's three-backtick fence early — fix now
- diff-bug #6: in guest mode a `confirm` or `decide` level still recommends "do it now" — reject, planned change (AC3 puts the verdict's option first and recommended)
- diff-bug #7: the candidate-row option is offered on a non-default branch where it writes nothing, and the chip does not say so — fix now
- diff-bug #8: the PR-number stop says PRs go through `/hotfix` but fences `/milestone` — fix now
- diff-bug #9: the reply hand-off's "then give the safety line" puts close-block parts out of order — fix now
- diff-bug #10: Session start's RR check ("before anything else") can preempt the look-in — fix now
- diff-bug #11: the owner-mode candidate-row push names no pull or dirty-tree check first — fix now
- diff-bug #12: the guard's read pattern passes a line that holds a read and a write — fix now
- diff-bug #13: the guard bounds §4 at end of file, so a later section would join it — fix now
- diff-bug #14: `test_argument_test_names_both_forms` checks neither form — fix now
- diff-bug #15: the CLAUDE.md issue route sits after the `/hotfix` route, so a bug issue can match `/hotfix` first — fix now
- diff-bug #16: the PR search on a bare number matches unrelated text — fix now (hits are read as leads before they are listed)
- blame-history #1: the template comment moved from "~25 lines" to under 30 against D-137's stated budget and D-018 — reject, planned change (AC6 updates the comment to match the body, and the 30-line cap is unchanged)
- blame-history #2: a `reply` to a declined new request writes no row, so the issue can be its only record (D-044, D-042) — follow-up (candidate row "Issue look-in edges (M232 review)")
- blame-history #3: the rulebook's Intake paragraph names neither the reply nor the plan route — follow-up (same row)
- blame-history #4: §3's "resolves here, and nowhere else" now reads as excluding §4 — fix now
- blame-history #5: the RR check ordering — fix now (same fix as diff-bug #10)
- blame-history #6: §4 reads upstream issues in guest mode where §2 skips the inbox — reject, planned change (AC5)
- blame-history #7: the `cairn_scripts.py` comment drops the old ~25 target — reject, style (the comment is accurate)
- blame-history #8: the EXEMPT reason matches precedent — reject, false (no defect)
- blame-history #9: `argument-hint: ""` was not pinned — reject, false (no defect)
- blame-history #10: the routing lines are within AC6 — reject, false (no defect)
- prior-review #1: the `/hotfix` route — fix now (same as diff-bug #2)
- prior-review #2: README's "Which skill, when" table has no issue look-in row (M112 lesson) — fix now
- prior-review #3: the PR search has no own-PR filter — reject, false (cairn's own PR that answers the issue is a correct hit)
- prior-review #4: the search commands carry no `--limit` — reject, style (M168 rejected the same)
- prior-review #5: owner-mode push is owner-only — reject, false (consistent)
- live-run #1: the RR check and Session start reads before the look-in — fix now (same fix as diff-bug #10)
- live-run #2: guest-mode `decide` still recommends "do it now" — reject, planned change (same as diff-bug #6)
- live-run #3: leave's "a duplicate" does not say whether an upstream issue counts — fix now
- live-run #4: §4 does not say how to run the checkout's code rather than an installed release — fix now
- live-run #5: the PR search takes only the number, and the issue search returns the issue itself — fix now (with diff-bug #16)
- live-run #6: unclear whether a one-phase look-in marks a chapter — reject, false (the phase header directive covers it)
- Pass 2 (2026-10-10, head 3e43c88): branch pushed to PR #241. The Copilot state query returned `reviewed head Lite`, so nothing was requested.
- Pass 2 evidence AC1–AC6: re-run on 3e43c88. The frontmatter trigger and `argument-hint` are present, §4 is at line 318, and `claude plugin validate .` exits 0 (AC1). §4 lists 6 scale entries, three verdicts and three levels (AC2). The chip's four options are in order (AC3). The AC4 grep lists 4 lines: `gh issue view`, `gh issue list`, `gh pr list`, and the hand-off, each with `--repo <base-repo>` (AC4, AC5). The template section is 29 lines and CLAUDE.md is 26, each +2 in the section, and the README carries the paragraph and the table row (AC6).
- Pass 2 evidence AC7: verify green on 3e43c88, hand-run `skills/tests` 691 OK, `cairn_validate` all passed, no marketplace version warning. A second fresh Opus live run followed the fixed §4 in `~/github/insight` (guest) on open issue #329 (`is_nested_models` and random effects). Its report gave verdict `reply` and level `none`, with citations and a reproduction under `pkgload::load_all`. It skipped the issue's network reprex as data, wrote out the chip (Draft the reply, recommended, then Add a candidate row, then Stop), and took Stop. `git status` in insight stayed clean.
- spawned: diff-bug, blame-history, prior-review (pass 2, plus the AC7 live-run agent)
- diff-bug #1 (pass 2): the candidate-row text wrote the row before its pull and its checks — fix now (ordered steps)
- diff-bug #2 (pass 2): the sweep skipped open milestones and their `Resolves:` slots — fix now
- diff-bug #3 (pass 2): no rule for a closed issue — fix now (a closed issue whose fix landed is a `reply` example)
- diff-bug #4 (pass 2): the candidate-row option warned about only one of its two no-write cases — fix now
- diff-bug #5 (pass 2): an argument such as "look into issue 12" failed the argument test — fix now
- diff-bug #6 (pass 2): the PR stop gave no way to tell an external PR from the operator's own — fix now (`/milestone` first, then `/hotfix #<N>` labeled for an external PR in owner mode)
- diff-bug #7 (pass 2): "the hand-off command as the first fence" is false when the draft holds a code block — fix now (the fence is named by its label)
- diff-bug #8 (pass 2): the reproduction can leave build files in the repo — fix now (`git status --short` the same before and after, ignored build output aside)
- diff-bug #9 (pass 2): the CHANGELOG missed the guest-mode plan acknowledgement change — fix now
- diff-bug #10 (pass 2): `<title>` in the guest acknowledgement was ambiguous — fix now (the issue's own title)
- diff-bug #11 (pass 2): no rule for a failed candidate-row push — fix now
- diff-bug #12 (pass 2): the `'\''` escape assumes a POSIX shell — follow-up (row "Issue look-in edges (M232 review)")
- blame-history #1 (pass 2): external versus own PR undefined — fix now (same as diff-bug #6)
- blame-history #2 (pass 2): `/hotfix` has no clause for an `issue <URL>` argument — follow-up (same row; the pass-2 diff-bug reviewer found steps 6 and 7 pick it up as an existing issue)
- blame-history #3 (pass 2): a PR URL or a non-issue argument ran §1–§3 silently — fix now
- blame-history #4 (pass 2): Stop leaves the issue as the only record — reject, planned change (AC3 names the stop option, and the rulebook requires one on every chip)
- blame-history #5 (pass 2): an orphaned issue cannot be closed from the look-in — follow-up (same row)
- blame-history #6 (pass 2): the guest acknowledgement's title may carry cairn wording — fix now (same as diff-bug #10)
- blame-history #7 (pass 2): the reply close block names no label for the hand-off fence — fix now
- blame-history #8 (pass 2): the first routing line can catch "fix issue #12" — reject, planned change (AC6 routes issues to the look-in, whose hotfix option leads on to `/hotfix`)
- blame-history #9 (pass 2): README's contributions bullet names only the audit's inbox sweep — reject, false (the bullet describes the audit, and the look-in has its own paragraph and table row)
- blame-history #10 (pass 2): §4 does not restate the phase header — reject, style
- prior-review #1 (pass 2): the guest acknowledgement has no guard — reject, false (the profile's test-doctrine owes no prose guard, D-109)
- prior-review #2 (pass 2): no blanket `--repo` clause in the plan skill — reject, false (owner mode needs none, and the inbox reads are in the follow-up row)
- prior-review #3 (pass 2): README and CHANGELOG miss the guest acknowledgement — fix now
- prior-review #4 (pass 2): README omits the `issue N` form — fix now
- live-run #1 (pass 2): unclear whether the issue read also runs with the number — fix now (the two reads are stated apart)
- live-run #2 (pass 2): no depth for reading a lead — reject, style
- live-run #3 (pass 2): `load_all` can write build files — fix now (same as diff-bug #8)
- live-run #4 (pass 2): docs in another package — reject, false (report part 2 covers what is out of reach)
- live-run #5 (pass 2): a `reply` example "an item already covered" blurred with leave — fix now (it now reads "an item the code or docs already cover")
- live-run #6 (pass 2): the candidate-row description said nothing for guest mode — fix now
- live-run #7 (pass 2): unclear whether a CI line is owed — reject, false (the look-in has no branch of its own)
- live-run #8 (pass 2): chapter markers for one phase — reject, false (same as pass 1)
- live-run #9 (pass 2): the rulebook's `<fork-owner>` recipe reads `origin`, which in the insight checkout is the upstream — follow-up (same row)
- fixed: every pass-1 fix-now line above, fixed e9cf3ba (diff-bug #8's wording again in 3e43c88). Every pass-2 fix-now line, fixed a0a6e35. One line stands for the per-line `, fixed <sha>` marks.
