# cairn v3 design (2026-11-25)

**Provenance.** Citekey `v3-design` · ingested 2026-11-25 from a design conversation between the user and a Claude session in this repo, outside any milestone.
Pagination: —.
Extraction: first-hand record of that conversation, with nothing to re-verify against — observed 2026-11-25.

**Role.** The design for a v3.0.0 rewrite of cairn. Each section says whether the user agreed to it or the session proposed it and the user did not object. Nothing here is built.

## Why change

Status: agreed.

- The user wants to keep: tracking of planned work and candidates, the review step, the reference library, and a status view.
- The user wants to shed: documentation nobody rereads, and rule text that makes the agent over-apply principles or skip wanted steps.
- The user may move from Claude Desktop to T3 Code, to use Claude and Codex together (Codex for review and second opinions). T3 Code runs one thread per task in its own worktree. Only the pane mod is tied to Claude Desktop.
- Measured in this repo, observed 2026-11-25: skills and rulebook hold about 82,000 words (rulebook 14,180); `DECISIONS.md` holds 248 entries in 595 KB; session start injects 22 KB; hooks and scripts are 6,480 lines of Python with 30,378 lines of tests; 340 milestones and 1,225 commits in 4.5 months.
- Across the user's machine, observed 2026-11-25: 23 repos carry `cairn/` (21 tracked, 2 guest), with 582 candidate rows and 290 Known issues entries.

## What stays and what goes

Status: agreed.

- Stays: `ROADMAP.md` (candidates), plans, review, triage, the reference library, `PROFILE.md`, a status view, the Copilot-notes handler, release, setup.
- Goes or is frozen: `DECISIONS.md` and `LESSONS.md` (moved to an archive folder, loaded by nothing), Known issues in `DESIGN.md`, the design interview, the review-brief skill, the health audit, the prose-guard tests, most guard hooks. `DESIGN.md` is written only on request.

## Vocabulary and sizes

Status: agreed, except the slug rules, which are proposed.

- The words "milestone" and "hotfix" and the M-numbers are dropped. Old archives keep them as history.
- Every piece of non-trivial work has a **plan** and ends in a **PR**. There are two sizes, named for the route:
  - **Trail**: fits one sitting and one PR and leaves the user no design choice. Its plan answers three questions: what is wrong or wanted, the change, how to check it. It has no ROADMAP row.
  - **Road**: everything larger. Its plan holds scope, acceptance criteria, tasks and review evidence, and starts with one question set to the user.
- A trail plan that grows becomes a road plan by gaining sections. Nothing is renamed.
- A bug gets a regression test written first, at either size.
- A trivial edit (no runtime surface) still commits to main.
- Each piece of work has one slug of two to four words. It is the branch name, the plan's file name, and the handle the user types. The route is a line inside the plan.

## Where files live

Status: agreed.

- A home folder holds what must not be in git: `~/.cairn/<owner>/<repo>/`.
- In the user's own repos, the repo keeps `cairn/ROADMAP.md`, `cairn/PROFILE.md` and the reference notes. The home folder holds active plans and the source shelf.
- In guest repos, the home folder holds everything, and nothing of cairn sits in the host checkout. The session-start hook finds the folder from the repo's base remote.
- `~/.cairn` is a private git repo the user syncs by hand when changing machines. If a plan is missing on another machine, resume says so and offers to rebuild it from the branch and PR.
- After a merge in the user's own repos, the plan is deleted, trail or road. In guest repos it moves to `done/` in the home folder, since the PR text there is written in the host's style and may not carry the user's reasoning.

## Git model

Status: agreed.

- Main gets one commit per piece of work, through a PR the user approved. There are no plan commits and no post-merge tracking commits on main. ROADMAP edits ride in the PR.
- "Planned" and "in progress" are read from plans and branches, not stored as rows.
- The merge record is written once from the plan and answers five questions: what changed, why, the choices made, what was left out, how it was checked. It becomes the PR description and the squash commit message (`gh pr merge` sets the message).

## Commands

Status: proposed. The user agreed there is no separate verb for small work, that status takes an id, the verb `start`, one reviewer, and Copilot handling in guest repos only.

One skill, `/cairn`, takes a verb. Each verb's text is its own file, loaded when used.

- `status [slug | #N]`: read-only. No argument lists road and trail work, open PRs and the candidate count, with one recommended next action. A slug reports that plan. A GitHub number is an issue or a PR; one call says which.
- `start <idea, issue or bug>`: investigates, picks trail or road and says which, writes the plan, builds, and goes on to review. The user can overrule the size.
- `resume [slug]`: picks work up at the phase its plan shows. No argument means the current branch.
- `review [slug | #N]`: one review for both sizes; also takes someone else's PR.
- `copilot <PR>`: handles Copilot's notes, in guest repos only. Review in the user's own repos has no Copilot round; observed 2026-11-25, only this repo had it switched on.
- `triage`, `source add <file or URL>`, `release`, `setup`. `release` stays in substance; observed 2026-11-25, 13 of 23 repos have release commits.

Removed skills get no stubs. Whether anyone else has cairn installed is unknown (observed 2026-11-25: 3 stars, no forks, no issues or PRs from others). The session-start hook names a v2 repo and points to `/cairn setup`, which covers any other user who updates.

Draft steps per verb, not yet marked up by the user:

- **start**: check whether the request is trivial; investigate before asking; for a road plan, one question set with recommendations; write the plan; account for everything the user asked for; per task, test first, then code, then a commit; add the changelog entry the profile calls for; run `verify`; go to review.
- **review**: sync with the default branch; run every check in the plan fresh; run `verify`; one independent reviewer reading the diff for bugs, Codex when available and otherwise a fresh subagent (of 63 recorded v2 findings that name their reviewer, 52 came from the diff reader); apply the findings rule; ask the merge question showing the merge record, each finding's outcome and the issues proposed; on approval only, push, open the PR, wait for CI, squash-merge; open the approved issues and delete the plan and branch.
- **triage**: list every candidate; check each against code and git; propose promote, keep or drop per row in one table for the user; apply in one commit.
- **setup**: detect a new repo, a v2 repo or a v3 repo with pieces missing; scaffold, migrate or repair.
- **source add**: put the file on the shelf, write a note with citation and what was read, add the index line.
- **copilot**: read the notes; decide fix, reject or defer; fix and push; draft at most one comment per review for the user; resolve the threads; never reply on a thread.

## Review findings

Status: agreed.

Three questions in order; the first yes decides.

1. Did this PR cause it or make it worse? Fold it in.
2. Is it older, but the fix sits in lines the PR already changes and needs no new check? Fold it in.
3. Is it older, and can the reviewer name a concrete input that fails today? Open an issue, with the failing input in it.

Anything else is dropped. The review decides 1, 2 and the drops; issues are listed at the merge question for the user's approval. Nothing is opened upstream in a guest repo without the user's word. Review findings never become candidate rows.

## Triage

Status: agreed.

Candidates are things the user or the agent proposes to build. Triage has one list and three outcomes. Priority tags, parked conditions, routing to Known issues and the lessons pass are gone. In this repo, observed 2026-11-25, 36 of 39 rows were parked and all traced to a milestone; 15 triage commits routed about 46 rows to Known issues, dropped 7 and promoted 3.

## Text for other readers

Status: proposed.

- cairn writes no prose for other readers. It hands the facts to the user's `writing-for-people` skill as the brief, and a fresh drafter writes the text.
- The user sees each text once, at the gate that already exists. Internal files are never previewed in chat.
- With Codex available, it reads the draft cold and reports what the text says and asks. A mismatch with the brief means a rewrite from the brief.
- The only style rule cairn keeps is the guest rule: match the host maintainers' own text.
- A review of the writing skill is a separate candidate row.

## Length

Status: proposed.

v2 required text to be complete and to fit a size, and sessions gamed the unit or reworded in circles. v3 uses no line, word or byte limits and no length checker.

- Each document is a fixed set of questions; the answers are the document.
- Omission is allowed. The diff and PR hold the detail.
- Where a limit is needed it counts whole items. A road plan has at most 7 acceptance criteria, each naming one check; more means two plans (agreed). Seven is v2's figure: in 400 v2 plans read before archiving, the median was 6, and 27% sat at exactly 7, which suggests criteria were combined to fit.
- The one remedy for "too long" is removing an item or splitting the work, never rewording to fit.
- Rules describe the reader and give no example.

## Rewriting the skills

Status: proposed.

- Each verb is written from a blank page as its steps and what done looks like. The v2 text stays under the v2.2.0 tag to consult.
- A rule goes in only if it guards something public or hard to undo, or the user names it as a step wanted every time.
- Error branches and rare cases get no text; the agent uses judgment and asks when unsure.
- Guest mode is stated once, in the rulebook.
- The rulebook becomes a format spec of a page or two.
- A line is added back only after a real failure.
- The kept v2 skills and rulebook total about 72,500 words. The target is under 8,000, a guess to adjust in the pilot.

## Hooks and status view

Status: proposed.

- Session start injects the home-folder path, ROADMAP and the active plan.
- GitHub branch protection replaces most guard hooks, since it covers Claude and Codex alike.
- The pane mod becomes optional. A status view is built on the status script so it works outside Claude Desktop.

## Migration

Status: proposed.

- The new core ships as v3.0.0 under the same plugin name, in this repo.
- A script does the mechanical part per repo in one commit: move `DECISIONS.md`, `LESSONS.md` and the old archive aside, swap the cairn section of `CLAUDE.md`, add an `AGENTS.md` for Codex. Guest repos move to the home folder.
- A triage pass per repo does the judgment part: each Known issues entry becomes a GitHub issue if it has a failing input and is otherwise dropped; each candidate is promoted, kept or dropped.
- All repos are cut over in one sitting; triage passes follow as each repo is next worked in.
- In flight, observed 2026-11-25: hitop 5, glmmTMB 3, ackwards 1. These finish under v2 or have their files renamed to slugs.
- Order: test T3 Code, write the format spec, build the script while piloting on chromodoris, run it on the rest, triage.

## To test in T3 Code

- Whether a thread loads Claude Code plugins, meaning cairn's skills and hooks.
- Whether `/cairn start` reaches Claude unchanged.
- Whether a thread can write to `~/.cairn` without a permission prompt each time.
- How Codex gets the skill and the plan; Codex reads `AGENTS.md` and its own skills folder.

## Open

- How a candidate row shows that it is needed soon. The user wants that signal and file order does not give it; the Triage section's removal of priority tags is not settled.
- The T3 Code tests above.
