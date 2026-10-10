# M232: `/milestone` looks into one GitHub issue and routes it

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing — `/milestone` ships in the plugin to every operator
- **Branch/PR:** m232-issue-look-in

## Goal

Given an issue number or URL, `/milestone` reads that issue and the code it names. It says whether the issue needs a reply, a hotfix, or a milestone, and how much maintainer design input it needs. On the user's choice, it starts the work now or records a candidate row.

## Scope

**In:** an issue look-in section in `skills/milestone/SKILL.md`, entered by an issue argument. It gives a verdict, a maintainer-input level, and one chip. "Do it now" routes to `/hotfix` or `/milestone-plan` with the issue, or hands the user a drafted reply to post. The section reuses §3's candidate-row and leave dispositions. The CLAUDE.md routing template, this repo's `CLAUDE.md`, the README, and the CHANGELOG follow.

**Out:** cairn never posts an issue reply itself, because the user posts it from the fenced command. A new `/issue` skill is not planned: the question set kept the look-in in `/milestone`, so D-043's "a door, not a new skill" stands. A `/milestone` audit that reads each bot thread on the operator's open PRs is the candidate row that M231's plan adds.

## Acceptance criteria

- [ ] AC1: `skills/milestone/SKILL.md` gains an issue look-in section. An argument that is an issue number (`#N` or `N`) or an issue URL runs that section in place of the snapshot, audit, and route sections. The frontmatter description names "look into issue N" as a trigger, and `argument-hint` names the issue argument. `claude plugin validate .` is green.
- [ ] AC2: The section tells the report to give a verdict of exactly one of reply, hotfix, or milestone. It defines a three-value maintainer-input scale: none (the code or docs settle it), confirm (a choice for the maintainer to approve), and decide (a design decision is needed before work). It tells the report to give file:line citations where the issue names existing code or docs, else a line saying none applies. It also tells the report to give a reproduction, or the reason none was run.
- [ ] AC3: The section ends the report with one chip. Its options are do it now, add a candidate row, leave, and stop. "Do it now" means one of three things: `/hotfix` with the issue, `/milestone-plan` with the issue so that its `Resolves:` slot names it, or the reply hand-off. A candidate row is search-first and cites the issue URL. The section offers leave only with a stated reason from D-044's three: noise, a duplicate, or an item cairn already covers. The verdict's option is first and marked recommended.
- [ ] AC4: The reply hand-off puts the drafted reply verbatim in the turn's final rendered text, with a fenced `gh issue comment <N> [--repo <base-repo>] --body` command for the user to run. In the look-in section, `grep -nE "gh (issue|pr|api)"` lists only commands that read, plus that one hand-off line, which the section shows and never runs. The section itself runs no remote write other than AC5's owner-mode push. Writes by `/hotfix` or `/milestone-plan` stay under those skills' gates.
- [ ] AC5: In guest mode, every `gh issue` and `gh pr` command in the section carries `--repo <base-repo>`. Every `gh api` call that reads issue or PR data names the base repo's owner and name in its path or GraphQL variables. The maintainer in the input level is the upstream maintainers. The section tells the draft to follow the rulebook's guest-mode rule of no cairn vocabulary. A candidate row is written to disk and not committed. In owner mode, the row is a docs-only commit to the default branch, pushed.
- [ ] AC6: The CLAUDE.md routing template (`skills/shared/templates/claude-md-section.md`) and this repo's `CLAUDE.md` route "look into an issue" to `/milestone` with the issue. Each section gains at most two lines, and the template's length comment is updated to match its body. The README describes the issue argument.
- [ ] AC7: The profile's `verify` slot is green. A new prose guard in `skills/tests/` pins AC2's three verdicts and three levels and AC4's hand-off, and the hand-run `skills/tests` suite is green. One live run of the look-in on an open issue of `easystats/insight` reads the guest-mode profile of the `~/github/insight` checkout. It stops at the chip with the stop option, and its chat report shows one verdict and one level.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3
- AC5 → T2, T3
- AC6 → T4
- AC7 → T5

## Tasks

- [x] T1: In `skills/milestone/SKILL.md`, add the argument test and the frontmatter trigger and `argument-hint`. An issue argument skips §1–§3 and runs the new section. In guest mode the `gh` reads carry `--repo <base-repo>`.
- [x] T2: Write the section's read and report: `gh issue view <N> --comments`, the code the issue names, and a reproduction where one fits in the sitting. Define the three verdicts and the three-value input scale. In guest mode the maintainer is the upstream maintainers.
- [x] T3: Write the chip and its routes. `/hotfix` and `/milestone-plan` get the issue through the Skill tool. The candidate row reuses §3's search-first path, guest-mode disk-only and owner-mode docs-only commit included. The reply hand-off uses the rulebook's no-cairn-vocabulary rule in guest mode and no thanks to bots.
- [ ] T4: Add the routing line to `skills/shared/templates/claude-md-section.md` and this repo's `CLAUDE.md`, merging a line where needed to stay under 30. Update the template's length comment. Update the README and the CHANGELOG.
- [ ] T5: Add the prose guard in `skills/tests/`. Run the verify slot and the hand-run `skills/tests` suite. The live run on an `easystats/insight` issue happens at review.

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
- 2026-10-10: T3 done. The hand-off command always carries `--repo <base-repo>` and single-quotes the reply. The section's prose names no `gh` subcommand, so the AC4 grep lists the three reads and the hand-off line only. The bot test reads `author.is_bot` from the issue read. Decided: in owner mode on a branch other than the default, the candidate-row option writes nothing and the close block shows the row and says to rerun from the default branch, which keeps AC5's docs-only commit to the default branch.

## Decisions

## Review
