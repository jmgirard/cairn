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
- The user has a work account and a personal account for Claude and wants them kept separate. cairn is primarily for personal use (stated 2026-11-26).
- Measured in this repo, observed 2026-11-25: skills and rulebook hold about 82,000 words (rulebook 14,180); `DECISIONS.md` holds 248 entries in 595 KB; session start injects 22 KB; hooks and scripts are 6,480 lines of Python with 30,378 lines of tests; 340 milestones and 1,225 commits in 4.5 months.
- Across the user's machine, observed 2026-11-25: 33 repos carry `cairn/` (21 tracked, 12 guest), with about 900 candidate rows. Ten of the guest repos sit under `easystats/` and the first count missed them, so figures in this note that say "of 23" cover the 21 tracked repos plus brms and glmmTMB. Those 23 hold 290 Known issues entries; the easystats repos were not counted for that.

## What stays and what goes

Status: agreed.

- Stays: `ROADMAP.md` (candidates), plans, review, triage, the reference library, `PROFILE.md`, a status view, the Copilot-notes handler, release, setup.
- Goes or is frozen: `DECISIONS.md` and `LESSONS.md` (moved to an archive folder, loaded by nothing), Known issues in `DESIGN.md`, the design interview, the review-brief skill, the health audit, the prose-guard tests, most guard hooks. `DESIGN.md` is written only on request.

## Vocabulary and sizes

Status: agreed.

- The words "milestone" and "hotfix" and the M-numbers are dropped. Old archives keep them as history.
- Every piece of non-trivial work has a **plan** and ends in a **PR**. There are two sizes, named for the route:
  - **Trail**: fits one sitting and one PR and leaves the user no design choice. Its plan answers three questions: what is wrong or wanted, the change, how to check it. It has no ROADMAP row.
  - **Road**: everything larger. Its plan holds scope, acceptance criteria, tasks and review evidence, and starts with one question set to the user.
- A trail plan that grows becomes a road plan by gaining sections. Nothing is renamed.
- A bug gets a regression test written first, at either size.
- A trivial edit (no runtime surface) still commits to main.
- Each piece of work has one slug of two to four lowercase words, proposed at `start` and open to change before the first commit. It is the plan's file name and the handle the user types; any unique start of it works. The route is a line inside the plan.
- The plan records its branch in a `Branch:` line, and lookups go through that line. The branch carries the slug only where cairn creates it; an app that starts a thread in a new worktree names the branch itself, and guest repos have their own conventions.
- Work that starts from a GitHub issue records it as an `Issue:` line; `status #N` and `resume #N` find the plan that way.
- A new slug must differ from the active plans, and in a guest repo from those in `done/`. Across 1,883 archived v2 plans, observed 2026-11-25, no slug repeats within a repo and 95% use two to four words.

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

Status: agreed, except the draft steps, which wait for the user's markup.

One skill, `/cairn`, takes a verb. The skill's own text is the rulebook plus a table of verbs, so the rulebook is in context whenever any verb runs; separate skills would each have to start by reading a shared rules file, a step that can be skipped. Each verb's steps are a separate file, read when used. The cost is that the `/` menu shows one entry, so its argument hint lists the verbs.

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
3. Is it older, can the reviewer name a concrete input that fails today, and can it point to where that input comes from in ordinary use? Open an issue, with both in it.

Ordinary use (agreed 2026-11-26; the user's requirement is to keep rare cases from flooding the list):

- Every finding is sorted first by whether the reviewer can point to ordinary use. A pointer is a user's report; the repo's own documentation, examples, or tests showing that use; or a call in a package that depends on the repo. A finding with a pointer goes through the three questions. A finding without one is an edge case, whichever question it would have reached.
- An input the reviewer had to construct, such as an empty vector, an all-missing column, or an undocumented argument combination, has no pointer. Likelihood is judged by the pointer, never by a guess at how many users do it, so a wrong result for a documented model class counts even if few people fit it.
- One exception: an input that worked before the PR and fails after it is always folded in. The earlier behavior is the pointer.
- An edge case is never fixed by making the input work. It gets an input check, or it is dropped.
- An input check is one assertion at the entry of a user-facing function that refuses the input with a clear error. It turns a silent wrong answer into a loud one (the user's point: cheap assertions alongside other work are good practice). The PR adds one when three things hold: the PR adds or changes that function; today's result for the input is a wrong answer or an unclear error, not merely unspecified; and one assertion at the entry is enough. It is written in the repo's own idiom, with one test line and a changelog line.
- New user-facing functions assert what their documentation says they expect. Input checks do not extend to internal helpers, to functions the PR does not touch, or to a sweep across the package. In a guest repo one is added only where the host's nearby code already asserts its inputs.
- "Input check" names that assertion. "Check" alone means a verification step in a plan, as in question 2.
- The reviewer's brief limits it to the diff and the code the diff relies on. It looks for constructed inputs only in user-facing functions the PR adds or changes, the one place such a finding can lead to an input check.
- Dropped findings are one line each in the plan. The merge question gives two counts, edge cases and other, and the user can ask to see them. The merge record does not list them: its "what was left out" covers scope, not findings.
- The same test gates `[high]`.
- Observed 2026-11-26: 27 of the 105 Known issues entries in the user's R packages name an empty, all-missing, zero-length, single-element, or similar input. This is a keyword count, not a classification.

Anything else is dropped. The review decides 1, 2, and the drops; issues are listed at the merge question for the user's approval. Nothing is opened upstream in a guest repo without the user's word. Review findings never become candidate rows.

## Triage

Status: agreed.

Candidates are things the user or the agent proposes to build. Triage has one list and three outcomes. Routing to Known issues and the lessons pass are gone.

Two marks, proposed after the user set the requirements for both:

- `[high]`: a bug that gives wrong answers or misleads users now, in ordinary use as the findings rule defines it. The row says what goes wrong and points to that use. The agent sets or proposes it only for that kind of bug; the user may put it on any row. The user works these off quickly, so few exist at once: about 101 such rows have existed across 21 repos and 5 were present, observed 2026-11-25. A review finding of this kind is offered at the merge question as a fix to start right away or as a `[high]` row.
- `[blocked]`: work that cannot move until something outside happens. The row says what it waits for and, where there is one, names the issue, PR or release to look at. A plan in flight carries the same fact as a `Blocked on:` line.
- A row may carry both. `[low]` and `[parked]` are gone; an unmarked row can wait.
- Status shows at a glance what can move and what is blocked, with what each blocked item waits for. A PR waiting on someone else's review or on CI is read from GitHub. `start` and `resume` on a blocked item check whether the block has cleared and do not go on unless it has or the user says so.
- In migration, a `[parked]` row with a real outside condition becomes `[blocked]`; the rest lose the tag or are dropped. `[low]` rows lose the tag. In this repo, observed 2026-11-25, 36 of 39 rows were parked and all traced to a milestone; 15 triage commits routed about 46 rows to Known issues, dropped 7 and promoted 3.

## Text for other readers

Status: agreed.

The cause of bad text is the same everywhere: the session knows too much and writes about its own work. The split is by how the text is written, not where it is posted.

- Standalone prose is drafted by a fresh subagent that never saw the session: changelog entries, vignettes, new help pages, README sections, PR text in guest repos, and messages to people. The brief is the facts plus two or three existing examples of the same kind from that repo. Messages to people go through the user's `writing-for-people` skill; documentation goes through cairn's own drafting step, since that skill excludes READMEs and release notes. A second fresh subagent reads the draft cold and reports what it says and asks; a mismatch with the brief means a rewrite from the brief.
- Text woven into code is written inline by the session: code comments, edits to existing help text, error and warning messages. Two rules apply: say what the code does or why, never the story of the change; and match the neighboring text. The independent reviewer reads these cold as part of the diff.
- The merge record and issues in the user's own repos are written directly from their questions.
- One rule covers all repos: match the repo's existing text of the same kind. In a guest repo that text is the maintainers'. No cairn vocabulary reaches a host repo. cairn has no other style rules.
- The user sees each text once, at the gate that already exists. The merge question quotes the changelog entry in full and lists other changed documentation by file. Internal files are never previewed in chat.
- A review of the writing skill is a separate candidate row; whether that skill should take over documentation is a question for it.

## Length

Status: agreed.

v2 required text to be complete and to fit a size, and sessions gamed the unit or reworded in circles. v3 uses no line, word or byte limits and no length checker.

- Each document is a fixed set of questions; the answers are the document. A candidate row is a title, one sentence on what and why, and for a marked row what goes wrong or what it waits for. An issue from a finding is the failing input in a code block and where it comes from.
- Detail may be left out; the facts each question asks for may not. Each merge record question is complete when it covers a list that already exists: what changed covers every changelog entry in the PR; choices made covers every answer the user gave in the question set, plus any choice the session made that changes what the user gets; what was left out covers every item the plan marked as later, a candidate or dropped; how it was checked covers every check in the plan with its result. Each item gets one sentence.
- What can still be lost is the reasoning behind implementation choices. It survives as a line under choices made or, better, as a code comment where the odd choice lives. As a safety net, `review` commits `~/.cairn` locally just before deleting a plan, so deleted plans stay in that repo's history.
- cairn ships empty templates, headings and labeled lines with nothing under them, and no filled-in examples. A plan is markdown with labeled lines at the top (`Route:`, `Branch:`, `Issue:`, `Phase:`, `Blocked on:`) and one heading per question; an empty section says "none". A merge record uses labeled lines with no `#` headings, since the same text is the commit message; an empty label is dropped. Text for a guest repo follows the host's template where it has one.
- Where output is a readout of files, a script prints it: the status listing comes from the script, and the model adds only the recommended next action.
- There is no cap on the number of candidates; status shows the count and the user decides when to triage.
- Where a limit is needed it counts whole items. A road plan has at most 7 acceptance criteria, each naming one check; more means two plans (agreed). Seven is v2's figure: in 400 v2 plans read before archiving, the median was 6, and 27% sat at exactly 7, which suggests criteria were combined to fit.
- The one remedy for "too long" is removing an item or splitting the work, never rewording to fit.
- Rules describe the reader and give no example.

## Rewriting the skills

Status: agreed 2026-11-26, after the section was checked against the agreed ones and seven points were changed.

- Each verb is written from a blank page as its steps, its stopping points, and what done looks like. The v2 text stays under the v2.2.0 tag to consult.
- A rule goes in only if it guards something public or hard to undo, or the user names it as a step wanted every time. Public or hard to undo means: pushing, merging, posting to GitHub, a tag or release, deleting, and writing in a guest checkout.
- Error branches and rare cases get no text unless they pass that test. Two agreed ones do: a plan missing on another machine, and a blocked item.
- Each verb names its stopping points. Outside them the agent decides and goes on, and asks only what the user alone can decide.
- The rulebook holds what more than one verb needs: sizes, the approval rule, guest mode, the findings rule, the ask rule, and the file formats. Guest mode is stated once, there.
- After drafting a verb, the v2 skill is read once as a checklist, only for something public or hard to undo that was missed.
- Size is counted in steps and rules, not words, as the Length section requires. Too long is fixed by removing a step or a rule. There is no word target. The words per verb are printed at release as a number with no threshold.
- Order: the rulebook and templates; then the session-start hook, `status`, `start`, `review`, and `resume`; then the pilot; then the other verbs. Scripts get unit tests; verb text gets none, and the pilot is its test.
- The pilot is three pieces of real work in chromodoris: one road, one bug trail, and one with standalone prose. At least one is reviewed by Codex and one is resumed in a second sitting. Observed 2026-11-25, chromodoris has 6 candidate rows, which include each kind.
- Measured, observed 2026-11-25: the kept v2 skills and rulebook total about 79,300 words (82,255 in the 12 skill folders, less design-interview and milestone-brief). All markdown under `skills/` grew from 19,600 words at v1.0.0 (2026-07-16) to 90,515 at v2.2.0 (2026-11-05).

Fixing v3 without regrowth (agreed 2026-11-26):

- A change to skill text cites a real session where something went wrong. Hypothetical gaps in prose do not count. This binds the reviewer of a skill-text PR too: a finding that a line could be misread, with no session behind it, is dropped.
- During the pilot, any real failure may change the text, between pieces of work. From 3.0.0 on, a one-off gets no text change and the second occurrence does. Anything public or hard to undo is fixed the first time.
- The first response is to delete or reword the line that was misread. A new line is added only if nothing existing is at fault, and only if it passes the tests above.
- Occurrences are logged, at the user's word, as one line each in `~/.cairn/log.md`: date, repo, branch or slug, verb, what happened. The file sits outside the per-repo folders, so no shipped script reads it, and nothing reads it during work. Occurrences are not candidate rows (the user's requirement). They are not issues either: the cairn repo is public, the lines name other people's repos, and a one-off would stay open.
- A feature goes in only if the user needs it now in a repo being worked in. No record types, validators, or hooks are added to the plugin to stop a failure recurring. The log is the one record kept for that, and it is outside the plugin.
- Shipped text serves users of cairn; maintainer practice lives outside the plugin (the user's point). A personal skill in the user's own skills folder writes the log line and, when asked, groups the lines and proposes a fix for a group of two or more. `/cairn triage` does neither. These habits go in the cairn repo's `CLAUDE.md`; the words-per-verb readout at release goes in the cairn repo's `PROFILE.md`.

## Hooks and status view

Status: agreed 2026-11-26.

- Session start prints the home-folder path, the status script's local listing (work in flight with its phase and what blocks it, the candidate count, and the `[high]` rows), and the path of the current branch's plan. It does not inject ROADMAP or a plan's body, and it makes no GitHub call. `/cairn` also works the path out itself, so a session where the hook did not run still works. Observed 2026-11-25: v2's injection is 23.6 KB in this repo, and ROADMAP's median size across the 33 repos is 15.5 KB, with 14 over 21 KB.
- v2 has six guard hooks. Four go with no replacement, since what they guarded is gone or is not public or hard to undo: the stop guard (plans leave git) and the commit, memory, and idea nudges.
- The force-push guard is replaced by two GitHub rules on the default branch: no force-push and no deletion. `setup` proposes them at its existing stop and applies them on the user's yes. It never changes a guest repo's settings. No rule requires a PR, since a trivial edit, the triage commit, and a source note go straight to main. Observed 2026-11-25, 1 of the 21 own repos has rules (circumplex).
- The merge guard goes in the user's own repos, where the approval rule is held by text: an unapproved merge there costs one revert. GitHub cannot hold it, since the agent acts as the user. No record of an agent merging without approval was found in this repo's LESSONS or DECISIONS.
- One hook stays, for guest repos. It denies a push to the default branch, and it denies a merge unless the repo's profile says `Maintainer: yes`. It keeps no approval marker. It covers Claude only, and whether such hooks run in T3 Code is untested. Observed 2026-11-25: the user is admin on all 10 easystats repos, admins are exempt from protection on the 5 read, and the user has no push right on brms or glmmTMB.
- The pane mod is not ported to the `v3` branch. The status view is text from `/cairn status`; a visual view, if wanted after the pilot, is built on the status script's output (agreed).

## Guest repos the user maintains

Status: agreed 2026-11-26. The user is the primary maintainer of easystats/datawizard and will soon be of easystats/correlation.

- A guest repo is one other people share. That fact sets where cairn's files live, whose style text follows, the Copilot round, and the move to `done/`.
- Whether the user may merge and release there is a separate fact. A guest repo the user maintains carries `Maintainer: yes` in its `PROFILE.md` in the home folder. The user sets the line by hand.
- With the line: `review` still stops at the open PR, since others may review, and merges at the user's word with the host's merge method and message; `release` runs; `start` skips the check for a maintainer's agreement before a road plan. cairn never uses the admin override unless the user says so.
- Without the line, cairn never merges and never releases there.
- In every guest repo, even a trivial edit goes through a PR.
- Observed 2026-11-26: of datawizard's last 100 merged PRs the user wrote 24 and merged 17 of those; in insight, 64 and 2. nestedtune sits under tidymodels but is one of the user's own repos: the user wrote and merged all of its last 100 PRs.

## Migration

Status: agreed 2026-11-26.

- The new core ships as v3.0.0 under the same plugin name, in this repo. It is built on one `v3` branch outside v2's milestone process and merged to main once, as the release.
- The build happens in a second worktree. `~/.claude/skills/cairn` is a symlink to this checkout, so checking out `v3` here would switch every repo at once. The worktree is linked into `~/.claude_personal/skills/`, and the pilot runs in T3 Code under the HOME instance, while the desktop app keeps loading v2 from `~/.claude`.
- cairn is never installed in `~/.claude_work`. v3's text and scripts name no config folder.
- Before the pilot, `writing-for-people` must be in `~/.claude_personal`, and the three T3 Code checks (the hook runs, the skill is listed, a write to `~/.cairn` raises no prompt) are rerun there.
- chromodoris is migrated by hand before the pilot. Observed 2026-11-25, it has 13 commits, 6 candidates, and no work in flight. The script is written after the pilot, when the formats have stopped changing.
- After the pilot, datawizard is cut over alone and one piece of work is done there. The pilot covers none of the guest path: files in the home folder only, host style, `done/`, the Copilot verb, the merge hook, and the maintainer line. datawizard has no work in flight and no Known issues, and it carries the maintainer line.
- Then the other 31 repos are cut over in one sitting. v3 merges to main, T3 Code's HOME instance is pointed at `~/.claude`, and `~/.claude_personal` retires.
- For one of the user's own repos, the script makes one commit: it moves `DECISIONS.md`, `LESSONS.md`, and the old archive aside, and swaps the cairn section of `CLAUDE.md`. Whether it adds an `AGENTS.md` is decided with Codex's part. Observed 2026-11-26, none of the 21 own repos has one, and the 11 that are R packages would each need a `.Rbuildignore` line.
- For a guest repo, the script moves the untracked `cairn/` to the home folder, removes its line from `.git/info/exclude`, and carries over the profile's guest lines. Its commit lands in `~/.cairn`. Observed 2026-11-26, none of the 12 guest checkouts has a `CLAUDE.md` or `AGENTS.md`.
- The script converts work in flight. It moves each file to the home folder under a slug and writes the `Route:`, `Branch:`, `Issue:`, and `Phase:` lines, leaving the body as written. Nothing waits to finish under v2, since guest PRs wait on other people. Observed 2026-11-26: 12 pieces in 5 repos (hitop 4, glmmTMB 3, easystats/correlation 2, easystats/insight 2, ackwards 1), 7 of them in guest repos.
- A pass per repo does the judgment part, as each repo is next worked in. It belongs to `setup`'s v2 case, not to `triage`. Each Known issues entry becomes a GitHub issue only if it has a failing input and points to ordinary use, as the findings rule requires, and is otherwise dropped. In a guest repo the issue is proposed to the user and never opened without the user's word. Each candidate is promoted, kept, or dropped. Observed 2026-11-26: 315 Known issues entries across the 33 repos, 25 of them in easystats repos.

## To test in T3 Code

Read from T3 Code's own docs, observed 2026-11-25 (app version 0.1.12 installed): it drives the user's Claude Code installation, and skills load from the config directory's `skills` folder, the project's `.claude/skills` and enabled plugins. Skills are invoked with a `$` prefix, not `/`. A thread can take a "New worktree". The default permission mode for new threads is "Full access". The docs say nothing about hooks. cairn is installed as a skills-directory plugin at `~/.claude/skills/cairn`, so it should load there.

Tested by the user in one thread on chromodoris, observed 2026-11-25. The thread ran in "Current checkout" on main with "Full access", on Claude Opus 5.5 and then Codex.

- cairn's SessionStart hook ran and its text reached the session. The session also saw a notice that the hook was "skipped" because "cc-plugin-sec-default" ran first; the notice is unexplained.
- All 11 `cairn:` skills were available. Typing `/` in the composer listed the cairn skills; typing `$` listed only `simple-english` and `writing-for-people`. A `$writing-for-people` message with arguments invoked that skill.
- Writing to `~/.cairn` raised no approval prompt in "Full access".
- Switching to Codex inside the thread worked and carried a summary of the conversation. Codex ran in the same folder and could read `~/.cairn` and `~/.claude`. It received no `AGENTS.md` (the repo has none), no `CLAUDE.md`, none of the Claude skills and no hooks.

Config folders, observed 2026-11-26. This machine has two Claude config folders, `~/.claude` and `~/.claude_personal` (an underscore, not a hyphen). T3 Code's settings confirm the user's account of them: its HOME instance sets `homePath` to `~/.claude_personal`, and its WORK instance sets none, so it uses `~/.claude`. Its one Codex instance is also named WORK. `~/.claude.json` names a gmail.com account all the same, which fits the user's guess that the Claude desktop app writes to `~/.claude` whichever account is signed in.

- T3 Code uses both. The chromodoris test thread above is stored under `~/.claude/projects`, so every result above holds for `~/.claude` only. Eight other T3 Code projects sit under `~/.claude_personal/projects`, five of them worktrees under `~/.t3/worktrees/`.
- cairn, `writing-for-people`, and the user's global `CLAUDE.md` exist only in `~/.claude`. `~/.claude_personal` has none of them.
- v2 names `~/.claude` in 13 places outside its tests, and `scripts/cairn_cost.py` reads `~/.claude/projects`.
- `~/.cairn` and `~/.codex` are one folder each, shared by both accounts.
- The Claude Code docs, read 2026-11-26 through a subagent and not tested: `CLAUDE_CONFIG_DIR` moves settings, session history, and plugins, and credentials are keyed to the folder, so two accounts can stay signed in. The desktop app has no folder setting per account and no documented second profile. It accepts the variable through a saved local environment, which applies to sessions started from it.

Folder arrangement, set by the user and observed 2026-11-26. The Claude desktop app is for personal use only. T3 Code is for both accounts, each in its own folder.

- `~/.claude` is personal: the desktop app uses it, and it is signed in with the gmail.com account. cairn, `writing-for-people`, and the global `CLAUDE.md` stay there.
- `~/.claude_work` is work: T3 Code's WORK instance now sets `homePath` to it, and it is signed in with the fluidconcepts.ai account. cairn is not installed there.
- `~/.claude_personal` is still the folder of T3 Code's HOME instance, signed in with gmail.com.
- A sign-in lands in the default folder unless `CLAUDE_CONFIG_DIR` is set on the same line as `claude auth login`. The Keychain entry for a folder is named by the first eight hex digits of the SHA-256 of its path.

Still untested: a "New worktree" thread; the other permission modes; hooks other than SessionStart; how a skill named `cairn` in the plugin `cairn` is listed.

What the results change. The Codex account arrangement is agreed 2026-11-26; the other bullets were revised that day and wait for the user's word.

- The plugin form holds. No plain-skills fallback is needed for Claude in T3 Code. This was tested under `~/.claude` only and is rerun under the HOME instance before the pilot.
- Accounts (agreed, the user's decision): a personal Codex account goes in `~/.codex`, the default folder, and the work account moves to `~/.codex_work`, as was done for Claude. cairn therefore sets no `CODEX_HOME`. Observed 2026-11-26: `~/.codex` is signed in with ChatGPT, T3 Code names its one Codex instance WORK, and the move is not yet done. T3 Code's Codex instance settings have a "CODEX_HOME path" field and a "Shadow home path" field; the second keeps only `auth.json` apart and shares the rest. The command-line review reads the default folder's login, so the personal login must sit in `~/.codex` itself, not in a shadow home.
- `review` runs Codex itself from the command line, read-only, with the reviewer's brief as the prompt. A fresh process has not seen the build, so the review needs no new thread and no extra stop. Observed 2026-11-26: Codex 0.171.0 is installed and has `codex review --base <branch> [PROMPT]` and `codex exec` with a `read-only` sandbox. Neither was run.
- There is one brief and two runners: Codex, or a fresh Claude subagent where Codex is not installed or not signed in. No Codex skill is installed, and `setup` never touches Codex's folder. Findings come back as the command's output, so there is no findings file.
- The read-only sandbox is what keeps Codex from pushing, merging, or editing. Branch rules do not do that job: they hold only force-push and deletion.
- The migration script adds no `AGENTS.md`. Review does not need one, and nothing in this note has Codex doing build work.
- The cold read of text for other readers is done by a fresh Claude subagent.
- For the pilot: whether a Claude thread in T3 Code can start `codex`, and whether `codex review` takes a prompt together with `--base`.

## Open

- The user's markup of the draft steps per verb, which supplies the steps wanted every time.
- The user's word on the sections still marked proposed. A walk-through on 2026-11-25 settled one skill, slugs, text for other readers, and length; on 2026-11-26 it settled rewriting the skills and how v3 is fixed later. It also settled hooks and status view, added the maintainer line for guest repos, and settled migration and the ordinary-use test. Still to walk through: Codex's part.
- Whether a small format validator survives.
- The untested T3 Code items above, to be covered in the pilot.
