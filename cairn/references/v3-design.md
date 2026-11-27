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
- `~/.cairn/samples.md` holds pieces of the user's own writing, which the drafting brief includes where the file exists (see "Text for other readers"). It sits in the home folder because the plugin repo is public. Added 2026-11-27.
- After a merge in the user's own repos, the plan is deleted, trail or road. In guest repos it moves to `done/` in the home folder, since the PR text there follows the host's conventions and may not carry the user's reasoning.

## Git model

Status: agreed.

- Main gets one commit per piece of work, through a PR the user approved. There are no plan commits and no post-merge tracking commits on main. ROADMAP edits ride in the PR.
- "Planned" and "in progress" are read from plans and branches, not stored as rows.
- The merge record is written once from the plan and answers five questions: what changed, why, the choices made, what was left out, how it was checked. It becomes the PR description and the squash commit message (`gh pr merge` sets the message).

## Commands

Status: agreed. The steps of each verb are in "Steps per verb" below.

One skill, `/cairn`, takes a verb. The skill's own text is the rulebook plus a table of verbs, so the rulebook is in context whenever any verb runs; separate skills would each have to start by reading a shared rules file, a step that can be skipped. Each verb's steps are a separate file, read when used. The cost is that the `/` menu shows one entry, so its argument hint lists the verbs.

- `status [slug | #N]`: read-only. No argument lists road and trail work, open PRs and the candidate count, with one recommended next action. A slug reports that plan. A GitHub number is an issue or a PR; one call says which.
- `start <idea, issue or bug>`: investigates, picks trail or road and says which, writes the plan, builds, and goes on to review. The user can overrule the size.
- `resume [slug]`: picks work up at the phase its plan shows. No argument means the current branch.
- `review [slug | #N]`: one review for both sizes; also takes someone else's PR.
- `copilot <PR>`: handles Copilot's notes, in guest repos only. Review in the user's own repos has no Copilot round; observed 2026-11-25, only this repo had it switched on.
- `triage`, `source add <file or URL>`, `release`, `setup`. `release` stays in substance; observed 2026-11-25, 13 of 23 repos have release commits.

Removed skills get no stubs. Whether anyone else has cairn installed is unknown (observed 2026-11-25: 3 stars, no forks, no issues or PRs from others). The session-start hook names a v2 repo and points to `/cairn setup`, which covers any other user who updates.

## Steps per verb

Status: agreed 2026-11-26. The user and a session went through the markup sheet part by part that day; this section replaces the draft steps and the sheet.

Each line is one step. A line ending in (stop) is a point where the agent waits for the user. The Rulebook is the skill's own text and is in context for every verb.

**Rulebook (loaded with every verb)**

- Sizes: a trivial edit commits to main; trail work is one sitting, one PR, no design choice for the user; road work is everything larger.
- Work happens on a branch. Nothing reaches main without the user's approval at the merge question.
- Nothing is pushed, merged, posted to GitHub, tagged, or deleted except at a step that names it.
- Where files live (the repo and the home folder), and the file formats: ROADMAP rows and their marks, the trail and road plan, the merge record, PROFILE lines.
- A row's title says what the work would do in about six words, starting with a verb. It is unique in the file and ends with `(#N)` when the row comes from an issue.
- Review findings: sort each finding by its ordinary-use pointer first; then fold in, open an issue, add an input check, or drop, by three questions asked in order. Did this PR cause it or make it worse? Is it older, but fixed in lines the PR already changes, with no new check? Is it older, with a concrete input that fails today and comes from ordinary use?
- Look for a cited source in this order: the references index and shelf; then Zotero, where the profile has a `Zotero collection:` line; then the web. A file found in Zotero is copied to the shelf, and its item is added to the repo's collection. If Zotero is not running, start it in the background.
- If a cited source is not on the shelf and its full text cannot be found, ask the user for the file before going on with anything that rests on it. Never treat the source as nonexistent, and never use an abstract or someone else's summary in its place. If the user cannot supply it, record it as not obtained, with the date, and rest nothing on it. (stop)
- Guest repos, stated once: nothing of cairn in the checkout. Never push the default branch, even for a trivial edit. Never merge or release unless the profile says `Maintainer: yes`, and then only at the user's word. Post nothing upstream without the user's approval. Match the host's conventions.
- Ask only what the user alone can decide, in one batch.
- Text for other readers: standalone prose is drafted by a fresh subagent from the facts, two or three examples from the repo, and the user's samples, then read cold by a second. The examples set the conventions (length, structure, format, terms), and the samples set the voice. Inside a cairn verb this step writes what the work produces (changelog entries, vignettes, help pages, README sections, PR text), even where the user's writing skill says it covers them. That skill writes replies and messages to people. Text woven into code is written inline and matches the neighboring text. The user sees each text once, at the gate.

**status**

- No argument: show the status script's listing as printed (road and trail work with its phase, what is blocked and on what, candidates marked `[high]`, the candidate count, and any file the script could not read), then add the user's open PRs and their state from GitHub.
- Recommend one next action.
- With a slug or a GitHub number: report on that one item.
- Never change files, branches or anything on GitHub.
- Left out of v3: the health audit of tracking files against git; the hygiene stamp in ROADMAP.

**start**

- If the request is trivial, say so and do it: commit to main and push in the user's own repos, a PR in a guest repo.
- If the item is marked `[blocked]`, check whether the block has cleared; stop if it has not, unless the user says to go on.
- Fetch, then investigate the code as it stands on the remote's default branch before asking anything.
- Pick trail or road and propose the slug; say both in one line. The user can overrule either. In a guest repo, also say how many of the user's PRs are open on the host.
- Road only: one question set, each question with a recommendation. (stop)
- Guest repos, road only: check a maintainer has agreed to the change in an issue before planning it; stop if none has. Skipped where the profile says `Maintainer: yes`.
- Write the plan in the home folder with its `Route:`, `Branch:`, and `Issue:` lines. Cut the branch, or record the one the app already made.
- Account for everything the user asked for: in this plan, a later one, a candidate row, or dropped at the user's word.
- For a bug: write the regression test first and see it fail.
- Per task: test first, then code, then a commit. Keep the plan's `Phase:` line current.
- When the work takes a value or a claim from a source, run `source add` for it; the note rides in the PR.
- If trail work turns out to need a design choice from the user or a second sitting, say so, add the road sections to the plan, and ask the question set. (stop)
- New user-facing functions assert what their documentation says they expect.
- Add the changelog entry the profile calls for, in user-facing words.
- Run the profile's `verify`.
- Go straight to review.
- Left out of v3: showing the drafted plan in chat before saving it; reading past decisions before planning; a separate check of user-facing prose against the code before review (v2's claim audit; the check now lives in the reviewer's brief); rules for which model each subagent uses; a formal record when the plan changes during the build.

**resume**

- No argument: the work on the current branch. Otherwise the named slug.
- If the plan says `Blocked on:`, check whether it has cleared; stop if it has not, unless the user says to go on.
- If the plan is missing on this machine, say so and offer to rebuild it from the branch and PR. (stop)
- If the plan's PR is open: read new review comments and CI, make the fixes, run `verify`, and push at the user's word; draft any reply for the user; never resolve a person's thread. (stop)
- Otherwise continue at the phase the plan shows.

**review**

- Sync the branch with the default branch; rerun tests if it moved.
- Run every check in the plan fresh and record one evidence line each.
- Run the profile's `verify`.
- One independent reviewer reads the diff for bugs, and reads each statement the diff adds about what the code does (changelog, help pages, README, vignettes, comments, error messages) against the code: Codex from the command line, read-only, where it is installed and signed in; otherwise, or if the Codex run fails, a fresh subagent. The merge question says which one ran.
- Sort each finding by its ordinary-use pointer, then put it through the Rulebook's three questions. Fix the fold-ins, add the input checks, and rerun what they touch. Each dropped finding gets one line in the plan.
- Make the ROADMAP edits on the branch, so they ride in the PR.
- Write the merge record from the plan as answers to its five questions. In a guest repo, the PR text is drafted by a fresh subagent to the host's conventions and in the user's voice, and read cold against the diff.
- Merge question: the merge record, the changelog entry quoted in full, other changed documentation by file, the findings that changed something, the issues proposed, any `[high]` finding offered as a fix to start now or as a row, and the two counts of dropped findings. (stop)
- On approval only: push, open the PR, wait for CI, squash-merge with the merge record as the message. If a CI fix changes what the user approved, ask again.
- After the merge: open the approved issues, commit `~/.cairn`, then delete the plan and the branch.
- Guest repos: the question is whether to open the PR, and it shows the PR text and how many of the user's PRs are open on the host. Stop at the open PR. Where the profile says `Maintainer: yes`, merge at the user's word with the host's merge method and message, never with the admin override unless the user says so. The plan moves to `done/` once the PR is merged or closed. (stop)
- With someone else's PR as the argument: read it, test it, report findings to the user; post nothing without the user's word.
- Left out of v3: the format validator run as a gate; two to four reviewers, scaled by how user-facing the change is; a Copilot round in the user's own repos; caps on how many of the user's PRs may be open at once (in guest repos the count is shown at `start` and at the open-PR question instead); a rule for stopping after repeated failed reviews of the same plan.

**triage**

- Fetch and bring the default branch up to date, so work others have merged is seen.
- List every candidate row.
- Check each against the code and git: already done, subject gone, still true.
- For each `[blocked]` row, check whether the block has cleared.
- For each `[high]` row that names a failing input, check that it still fails.
- One table proposing promote, keep, or drop per row, with a one-line reason and any mark to clear. Promote adds `[high]`: the agent proposes it only for a wrong answer in ordinary use; the user may promote any row. (stop)
- Order the rows: `[high]` first, then the rest, each group from most to least important.
- Apply the accepted outcomes in one commit to main and push it. In a guest repo the commit lands in `~/.cairn`.
- Left out of v3: retitling and compressing rows; a written record for each drop.

**source add**

- Given a URL whose full text cannot be fetched (a paywall, a refused request): stop and ask the user for the file; write no note from an abstract. (stop)
- Put the file on the shelf in the home folder.
- Write a note: citation, what was read and when, the values or claims taken from it with page numbers.
- Add the index line. Commit the note and the index line to main and push; during work on a branch they ride in the PR. In a guest repo both live in the home folder.
- If the profile has a `Zotero collection:` line, look the source up in Zotero by DOI, then by title and year. If it is absent, add the item with the file attached, in that collection. Say what was added or was already there. A failure here never blocks the note.

**copilot (guest repos)**

- Find the PR and check out its head.
- Read each unresolved Copilot thread and the review summary.
- Decide fix, reject or defer per note; ask the user about any the agent cannot decide. (stop)
- Make the fixes and run `verify`.
- Draft at most one comment per review, holding only what the maintainers need; if they need nothing, there is no comment. Show it with the fixes. (stop)
- At the user's word: push, post the comment if there is one, and resolve Copilot's threads, never a person's. Never reply on a thread; never thank Copilot.

**release**

- Preconditions: clean tree, on the default branch and up to date with the remote, `verify` passes.
- Version decision; the question lists work in flight and any open `[high]` rows. (stop)
- Consolidate the changelog under that version: retitle the heading, group the entries, and remove noise. Reword an entry only where the reader in the next step finds a fault.
- A fresh subagent reads the consolidated section cold, against the code at the release commit. It reports what a user would take from it and any statement the code does not bear out. Fix what it finds.
- Run the profile's release steps.
- Commit the version bump and the changelog: to main in the user's own repos, through a PR in a guest repo the user maintains.
- Hand the user the submission checklist, with the release section quoted in full. Never submit or publish. Push and tag at the user's word. (stop)
- In a guest repo, stop unless the profile says `Maintainer: yes`: a release is the maintainers' act.

**setup**

- Detect the case: no cairn files, a v2 repo, or a v3 repo with pieces missing.
- New repo of the user's: write ROADMAP, PROFILE with the detected `verify` command, the references index, and the cairn section of `CLAUDE.md`. No `AGENTS.md`.
- The user's own repos: show what was written and propose the two GitHub rules on the default branch (no force-push, no deletion). Commit, push, and apply the rules on the user's yes. (stop)
- Someone else's repo: create its home folder with ROADMAP, PROFILE, and the references index. Write nothing in the checkout and never change the host's settings. The commit lands in `~/.cairn`. `Maintainer: yes` is the user's to add by hand.
- v2 repo: run the migration script, show the diff, and commit on approval. A status listing with no problem lines is the sign it worked. (stop)
- v2 repo, then or the next time the repo is worked in: one table for the old Known issues and the candidates. A Known issues entry becomes a proposed GitHub issue only if it has a failing input and points to ordinary use; otherwise it is dropped. Each candidate is promoted, kept, or dropped. Apply on the user's yes; in a guest repo no issue is opened without the user's word. (stop)
- v3 repo with pieces missing: write only the missing pieces and show them.
- Propose a `Zotero collection:` line for the profile, with the repo's name as the default; the user can decline. Where a repo gains the line, add every shelf file not already in Zotero, at the user's yes. (stop)
- Left out of v3: seeding a `DESIGN.md`; offering the design interview.

What the markup changed in sections agreed earlier, each at the user's word on 2026-11-26:

- Nothing public without a named step. The Rulebook states the public-or-hard-to-undo list once, so no verb repeats it.
- A trivial request is done at once and pushed in the user's own repos. A local main with unpushed commits would carry them into the next PR.
- A trail that outgrows its size stops the build and asks the question set. Finishing first would mean redoing the build if the user overturned the choice.
- `start` and `triage` fetch first, so work others have merged in a shared repo is seen (the user's point).
- Open PRs in guest repos. v2 capped them at 3 bug-fix and 1 feature PR per repo (D-213 and D-214, 2026-10-22, after an audit found sessions holding many open PRs on one host). v3 has no cap; the count is shown at `start` and at the open-PR question, where the user already decides. Observed 2026-11-26, the user had 4 open PRs in correlation, 2 in datawizard, and 1 in glmmTMB.
- A maintainer's review comments on an open guest PR are handled by `resume`. No verb covered them, and the pilot would not have shown the gap, since chromodoris is the user's own repo. A person's thread is never resolved, as D-213 required.
- `copilot` pushes only after its stop, so no fix reaches the maintainers' PR before the user has seen it.
- `release` loses the "nothing in progress" precondition: work in flight sits on branches and cannot reach the release. The version question lists it, with any open `[high]` rows.
- `release` gains a cold reader for the consolidated changelog (the user's suggestion). It is the one verb that commits to main with no reviewer, and a later PR can make an earlier entry false. v2 had the session read its own text here and logged no counts.
- The release commit goes to main in the user's own repos and through a PR in a guest repo the user maintains; the push and the tag wait for the user's word.
- One reviewer, not two to four: of 63 recorded v2 findings that name their reviewer, 52 came from the diff reader.
- If the Codex run fails, a fresh subagent reviews, and the merge question says which reviewer ran. Observed 2026-11-26 from the desktop app: `codex` 0.172.0 is on the path and signed in, `CODEX_HOME` is unset, and `codex review` lists both `--base` and a prompt in its help. No review was run, and nothing was checked in T3 Code.

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
- The reviewer's brief has a second job, the claim check (agreed 2026-11-26): read each statement the diff adds about what the code does against the code. This covers changelog entries, help pages, README text, vignettes, comments, and error messages. A statement the code does not bear out is a finding the PR caused, so question 1 folds it in.
- Dropped findings are one line each in the plan. The merge question gives two counts, edge cases and other, and the user can ask to see them. The merge record does not list them: its "what was left out" covers scope, not findings.
- The same test gates `[high]`.
- Observed 2026-11-26: 27 of the 105 Known issues entries in the user's R packages name an empty, all-missing, zero-length, single-element, or similar input. This is a keyword count, not a classification.

Anything else is dropped. The review decides 1, 2, and the drops; issues are listed at the merge question for the user's approval. Nothing is opened upstream in a guest repo without the user's word. Review findings never become candidate rows, with one exception settled on 2026-11-27: a `[high]` finding the user chooses to keep as a row at the merge question. That one gets an issue, opened at approval before the push, and the row carries its `(#N)`. A `[high]` finding the user chooses to fix now gets no issue.

## Triage

Status: agreed.

Candidates are things the user or the agent proposes to build. Triage has one list and three outcomes. Routing to Known issues and the lessons pass are gone.

Two marks, agreed after the user set the requirements for both:

- `[high]`: a bug that gives wrong answers or misleads users now, in ordinary use as the findings rule defines it. The row says what goes wrong and points to that use. The agent sets or proposes it only for that kind of bug; the user may put it on any row. The user works these off quickly, so few exist at once: about 101 such rows have existed across 21 repos and 5 were present, observed 2026-11-25. A review finding of this kind is offered at the merge question as a fix to start right away or as a `[high]` row.
- `[blocked]`: work that cannot move until something outside happens. The row says what it waits for and, where there is one, names the issue, PR or release to look at. A plan in flight carries the same fact as a `Blocked on:` line.
- A row may carry both. `[low]` and `[parked]` are gone; an unmarked row can wait.
- Status shows at a glance what can move and what is blocked, with what each blocked item waits for. A PR waiting on someone else's review or on CI is read from GitHub. `start` and `resume` on a blocked item check whether the block has cleared and do not go on unless it has or the user says so.
- The three outcomes are promote, keep, and drop (agreed 2026-11-26). Promote adds `[high]`. The agent proposes it only for the kind of bug above; the user may promote any row. Triage then orders the rows: `[high]` first, then the rest, each group from most to least important. Since a `[high]` row of the user's need not be a bug, triage does not re-test each one as a wrong answer; it checks that a row naming a failing input still fails.
- In migration, a `[parked]` row with a real outside condition becomes `[blocked]`; the rest lose the tag or are dropped. `[low]` rows lose the tag. In this repo, observed 2026-11-25, 36 of 39 rows were parked and all traced to a milestone; 15 triage commits routed about 46 rows to Known issues, dropped 7 and promoted 3.

## Text for other readers

Status: agreed. Voice and conventions were separated on 2026-11-27, at the user's word.

The cause of bad text is the same everywhere: the session knows too much and writes about its own work. The split is by how the text is written, not where it is posted.

- Standalone prose is drafted by a fresh subagent that never saw the session: changelog entries, vignettes, new help pages, README sections, PR text in guest repos, and messages to people. The brief is the facts, two or three existing examples of the same kind from that repo, and the user's samples (`~/.cairn/samples.md`) where that file exists. Replies and messages to people go through the user's `writing-for-people` skill. What a cairn verb produces (changelog entries, vignettes, help pages, README sections, and PR text) goes through cairn's own drafting step, which adds no stop. A second fresh subagent reads the draft cold and reports what it says and asks; a mismatch with the brief means a rewrite from the brief.
- Text woven into code is written inline by the session: code comments, edits to existing help text, error and warning messages. Two rules apply: say what the code does or why, never the story of the change; and match the neighboring text. The independent reviewer reads these cold as part of the diff.
- Claim check (agreed 2026-11-26; the user's worry is posting incorrect things once v2's claim audit is gone). The cold reader compares a draft to its brief, which catches a draft that drifts but not a brief that is wrong about the code. Two readers that already exist cover this. For text in the diff, the independent reviewer reads each added statement about what the code does against the code (see Review findings). For text written after the review and posted, such as PR text in a guest repo, issue text, and comments, the cold reader is given the diff with the brief and reports any statement about behavior the diff does not support. v2's separate step is gone: no extra subagent in `start`, no owed-or-not test, no log line with counts.
- Observed 2026-11-26: v2 review lines in 11 of the user's repos log 104 claim audits since the step was added on 2026-09-10, with 4,018 statements read and 309 corrected (7.7%); 10 runs corrected none. The counts are the sessions' own, and 50 of the runs are in this repo. They cannot show how many of the 309 a reviewer briefed for both jobs would have caught, since the audit always ran first.
- If, in the pilot or after, the user finds a wrong statement at the merge question that the reviewer passed, that is the case for a dedicated claim reader in `review`, at the cost of one more subagent for each PR that changes user-facing text.
- The merge record and issues in the user's own repos are written directly from their questions.
- One rule covers all repos: the conventions come from the setting, and the voice is the user's. Changed 2026-11-27 from "match the repo's existing text of the same kind"; the user's requirement is that anything posted under their name sounds like them and is fitted to the setting, so a text in a guest repo is as short as the host's and still reads as the user's.
- Conventions are length, structure, format, and terms. The drafter takes them from the repo's existing text of the same kind, which in a guest repo is the maintainers'. Voice is how the user phrases and explains things. The drafter takes it from the user's samples. The brief labels each for its job: the examples for length and form, the samples for phrasing and not for subject or length. No cairn vocabulary reaches a host repo. cairn has no other style rules.
- Text woven into existing text still matches its neighbors, since a change of voice inside a paragraph would stand out. This is the agent's choice, and the user may overrule it.
- The samples are one file, `~/.cairn/samples.md`, read by cairn's drafting step and by the user's skill. The plugin holds only the instruction to read it, and a user with no samples file gets text that follows the repo's conventions. The user asked whether the plugin repo should become private; with the samples in the home folder, it stays public. Observed 2026-11-27: the samples are 570 words in `~/.claude/skills/writing-for-people/samples.md`, `~/.cairn` exists but is empty and is not yet a git repo, and the plugin repo is public with 3 stars and 0 forks. Later that day the file was moved to `~/.cairn/samples.md` and the skill was pointed at it.
- The user's skill changed on 2026-11-26: its description now names vignettes, READMEs, and PR descriptions, and still excludes release notes. It can therefore load itself inside a cairn verb, so the Rulebook says which applies: cairn's step for what a verb produces, the skill for replies and messages. With the samples in both briefs, the two differ only in their stops. The skill shows the user the points when a text makes more than three, and shows the draft in chat. Rejected: the skill drafts all standalone prose, which would add those stops to a build.
- Observed 2026-11-27, as reported by the session that reran the skill on one email outside cairn: adding four of the user's old GitHub replies to the brief changed the phrasing of the draft but not what went into it (1,020 words and 52 numbers), and the user's cuts to the point list brought it to 510 words and 16 numbers. That is one email in one session. It is a reason to expect samples to carry voice and not length, not a test of it.
- The user sees each text once, at the gate that already exists. The merge question quotes the changelog entry in full and lists other changed documentation by file. Internal files are never previewed in chat.
- The review of the writing skill ran in its own session on 2026-11-26 and 2026-11-27, and the user stopped it there. Documentation stays with cairn's step, as above. Whether Codex can run the skill needs no test: Codex only reviews, and on 2026-11-25 it was observed to receive none of the Claude skills.

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
- One exception, at the user's word on 2026-11-26: a candidate row's title is about six words. Matching the titles already in the file gives a new repo nothing to match. No checker reads the number, so nothing fails and no rewording loop starts. Observed 2026-11-26: v2 required at least 5 words and at most 40 characters, and of 527 titles parsed across the user's repos the median is 6 words and 36 characters, 80% have 5 to 7 words, and 36 run over 40 characters.
- The one remedy for "too long" is removing an item or splitting the work, never rewording to fit.
- Rules describe the reader and give no example.

## Sources and Zotero

Status: agreed 2026-11-26. The user raised both problems during the markup: a source that could not be found was sometimes treated as nonexistent, and a PDF cairn found itself never reached the user's Zotero, so a paper about the project lacked sources.

- A cited source is looked for in order: the references index and shelf, then Zotero, then the web, then the user.
- When the full text cannot be found, the agent asks the user for the file before going on with anything that rests on it. Only that work stops. It never treats the source as nonexistent and never uses an abstract or someone else's summary in its place. If the user cannot supply the file, the source is recorded as not obtained, with the date, and nothing rests on it.
- Work that takes a value or a claim from a source runs `source add` for it, and the note rides in the PR. v2 required a note in that case; the draft steps had dropped it.
- A `Zotero collection:` line in the repo's profile turns the Zotero steps on and names the collection, so a project's sources sit together. `setup` proposes the line, with the repo's name as the default, and the user can decline.
- With the line, `source add` looks the source up in Zotero by DOI, then by title and year, and adds the item with the file attached if it is absent. A file found in Zotero during a search is copied to the shelf and its item is added to the collection. If Zotero is not running, the agent starts it in the background. A script does the work, and a failure never blocks the note.
- Where a repo gains the line, `setup` adds every shelf file not already in Zotero, at the user's yes. Observed 2026-11-26: the shelves hold 169 PDFs in 10 repos (circumplex 45, ackwards 45, intraclass 35, hitop 28).
- Observed 2026-11-26: Zotero 10.0.9 is installed, its local API is switched on in the user's settings, and `~/Zotero/storage` holds 7,185 PDFs. Zotero's documentation says the local API takes writes and file uploads from version 10, that reads need no key, and that Zotero shows a dialog to allow a write. None of it was tested: Zotero was not running, and a test would have put an item in the user's library.
- Observed 2026-11-26: of 267 reference notes in the user's repos, 14 in 5 repos mention something not retrieved, mostly supplementary data and code. A source that was silently skipped leaves no note to count.

## Rewriting the skills

Status: agreed 2026-11-26, after the section was checked against the agreed ones and seven points were changed.

- Each verb is written from a blank page as its steps, its stopping points, and what done looks like. The v2 text stays under the v2.2.0 tag to consult.
- A rule goes in only if it guards something public or hard to undo, or the user names it as a step wanted every time. Public or hard to undo means: pushing, merging, posting to GitHub, a tag or release, deleting, and writing in a guest checkout.
- Error branches and rare cases get no text unless they pass that test. Two agreed ones do: a plan missing on another machine, and a blocked item.
- Each verb names its stopping points. Outside them the agent decides and goes on, and asks only what the user alone can decide.
- The rulebook holds what more than one verb needs: sizes, the approval rule, guest mode, the findings rule, the ask rule, and the file formats. Guest mode is stated once, there.
- After drafting a verb, the v2 skill is read once as a checklist, only for something public or hard to undo that was missed.
- Size is counted in steps and rules, not words, as the Length section requires. Too long is fixed by removing a step or a rule. There is no word target. The words per verb are printed at release as a number with no threshold.
- Order: the rulebook and templates; then the session-start hook, `status`, `start`, `review`, and `resume`; then the pilot; then the other verbs. Settled 2026-11-27: `source add` and the Zotero script are built together, first among the verbs after the pilot, and the guest hook is built with `copilot`, before the datawizard cutover. Scripts get unit tests; verb text gets none, and the pilot is its test.
- The pilot is three pieces of real work in chromodoris: one road, one bug trail, and one with standalone prose. At least one is reviewed by Codex and one is resumed in a second sitting. Observed 2026-11-25, chromodoris has 6 candidate rows, which include each kind.
- Measured, observed 2026-11-25: the kept v2 skills and rulebook total about 79,300 words (82,255 in the 12 skill folders, less design-interview and milestone-brief). All markdown under `skills/` grew from 19,600 words at v1.0.0 (2026-07-16) to 90,515 at v2.2.0 (2026-11-05).

Fixing v3 without regrowth (agreed 2026-11-26):

- A change to skill text cites a real session where something went wrong. Hypothetical gaps in prose do not count. This binds the reviewer of a skill-text PR too: a finding that a line could be misread, with no session behind it, is dropped.
- During the pilot, any real failure may change the text, between pieces of work. From 3.0.0 on, a one-off gets no text change and the second occurrence does. Anything public or hard to undo is fixed the first time.
- The first response is to delete or reword the line that was misread. A new line is added only if nothing existing is at fault, and only if it passes the tests above.
- Occurrences are logged, at the user's word, as one line each in `~/.cairn/log.md`: date, repo, branch or slug, verb, what happened. The file sits outside the per-repo folders, so no shipped script reads it, and nothing reads it during work. Occurrences are not candidate rows (the user's requirement). They are not issues either: the cairn repo is public, the lines name other people's repos, and a one-off would stay open.
- A feature goes in only if the user needs it now in a repo being worked in. No record types, validators, or hooks are added to the plugin to stop a failure recurring. The log is the one record kept for that, and it is outside the plugin.
- Shipped text serves users of cairn; maintainer practice lives outside the plugin (the user's point). A personal skill in the user's own skills folder writes the log line and, when asked, groups the lines and proposes a fix for a group of two or more. `/cairn triage` does neither. These habits go in the cairn repo's `CLAUDE.md`; the words-per-verb readout at release goes in the cairn repo's `PROFILE.md`.
- The personal skill is `cairn-log`, written 2026-11-27 and kept by the user as drafted (474 words, in `~/.claude/skills/` with a link in `~/.claude_personal/skills/`). Its line is `- YYYY-MM-DD | owner/repo | branch or slug | verb | what happened`, with no guess at the cause. It adds three things to the bullets above: it commits `~/.cairn` after a line where that folder is a git repo, and never pushes; it marks a line `→ fixed <commit>` once its fix has merged, so that going over the log does not propose the same fix again; and a fix cites the log lines by date and verb, leaving other people's repo names out of anything committed to the public cairn repo. Observed 2026-11-27: a `claude -p` run with `CLAUDE_CONFIG_DIR` set to `~/.claude_personal` listed the skill. It has not logged a line yet.

## Hooks and status view

Status: agreed 2026-11-26.

- Session start prints the home-folder path, the status script's local listing (work in flight with its phase and what blocks it, the candidate count, and the `[high]` rows), and the path of the current branch's plan. It does not inject ROADMAP or a plan's body, and it makes no GitHub call. `/cairn` also works the path out itself, so a session where the hook did not run still works. Observed 2026-11-25: v2's injection is 23.6 KB in this repo, and ROADMAP's median size across the 33 repos is 15.5 KB, with 14 over 21 KB.
- v2 has six guard hooks. Four go with no replacement, since what they guarded is gone or is not public or hard to undo: the stop guard (plans leave git) and the commit, memory, and idea nudges.
- The force-push guard is replaced by two GitHub rules on the default branch: no force-push and no deletion. `setup` proposes them at its existing stop and applies them on the user's yes. It never changes a guest repo's settings. No rule requires a PR, since a trivial edit, the triage commit, and a source note go straight to main. Observed 2026-11-25, 1 of the 21 own repos has rules (circumplex).
- The merge guard goes in the user's own repos, where the approval rule is held by text: an unapproved merge there costs one revert. GitHub cannot hold it, since the agent acts as the user. No record of an agent merging without approval was found in this repo's LESSONS or DECISIONS.
- One hook stays, for guest repos. It denies a push to the default branch, and it denies a merge unless the repo's profile says `Maintainer: yes`. It keeps no approval marker. It covers Claude only, and whether such hooks run in T3 Code is untested. Observed 2026-11-25: the user is admin on all 10 easystats repos, admins are exempt from protection on the 5 read, and the user has no push right on brms or glmmTMB.
- The pane mod is not ported to the `v3` branch. The status view is text from `/cairn status`; a visual view, if wanted after the pilot, is built on the status script's output (agreed).

## No format validator

Status: agreed 2026-11-26.

- v3 has no separate validator. The status script is the only parser of cairn's files, and where it cannot read one it says so in its listing, one line per problem.
- Session start prints that listing, so a broken file shows at the start of the next session in that repo. Nothing gates `review`, and nothing waits on an exit code.
- The script never checks anything it does not need for the listing. A problem line is a by-product of reading, not a check of its own.
- What scripts read, and so what can produce a problem line: a plan's labeled lines; ROADMAP rows and their `[high]` and `[blocked]` marks; and the profile's lines, which the guest merge hook also reads.
- What goes unchecked: the references index against its files, a plan's body headings, the limit of 7 acceptance criteria, and the wording of a candidate row. If one goes wrong in real sessions, the fix rule applies.
- After the migration script runs on a repo, a status listing with no problem lines is the sign the conversion worked.
- Measured in this repo, observed 2026-11-26: v2's validator is 1,957 lines and 24 checks, with 8,765 lines of tests in the files that exercise it. 42 of 1,249 commits touch it, and 52 of the 340 archived milestone files mention it. About 3 of the 24 checks still have a subject in v3.

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
- The build happens in a second worktree. `~/.claude/skills/cairn` is a symlink to this checkout, so checking out `v3` here would switch every repo at once. The worktree is linked into `~/.claude_personal/skills/`, and the pilot runs in T3 Code under an instance named PILOT whose home is that folder, while the desktop app and T3 Code's PERSONAL instance keep loading v2 from `~/.claude`.
- cairn is never installed in `~/.claude_work`. v3's text and scripts name no config folder.
- Changed 2026-11-26: T3 Code made the user move its personal Claude instance to `~/.claude` that morning, so the folder split no longer came for free. The user added PILOT, a third Claude instance, for the pilot only. Observed that day in T3 Code's settings: PERSONAL uses `~/.claude`, WORK uses `~/.claude_work`, and PILOT uses `~/.claude_personal`; `claude auth status` reports gmail.com for `~/.claude` and `~/.claude_personal` and fluidconcepts.ai for `~/.claude_work`. `~/.claude_personal` had been signed out by the move and the user signed it in again. The rejected alternative was per-repo loading in chromodoris, with v2 switched off in that repo's local settings, since every piece of it is untested.
- `writing-for-people` is in `~/.claude_personal` as a symlink to the copy in `~/.claude`. Observed 2026-11-27: a `claude -p` run with `CLAUDE_CONFIG_DIR` set to that folder listed the skill. Before the pilot, the three T3 Code checks (the hook runs, the skill is listed, a write to `~/.cairn` raises no prompt) are rerun there.
- chromodoris is migrated by hand before the pilot. Observed 2026-11-25, it has 13 commits, 6 candidates, and no work in flight. The script is written after the pilot, when the formats have stopped changing.
- After the pilot, datawizard is cut over alone and one piece of work is done there. The pilot covers none of the guest path: files in the home folder only, host style, `done/`, the Copilot verb, the merge hook, and the maintainer line. datawizard has no work in flight and no Known issues, and it carries the maintainer line.
- Then the other 31 repos are cut over in one sitting. v3 merges to main, the PILOT instance is deleted, and `~/.claude_personal` retires.
- For one of the user's own repos, the script makes one commit: it moves `DECISIONS.md`, `LESSONS.md`, and the old archive aside, and swaps the cairn section of `CLAUDE.md`. It adds no `AGENTS.md`, as agreed under Codex's part. Observed 2026-11-26, none of the 21 own repos has one, and the 11 that are R packages would each have needed a `.Rbuildignore` line.
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
- `~/.claude_personal` is still the folder of T3 Code's HOME instance, signed in with gmail.com. This changed later that day: see the Migration section.
- A sign-in lands in the default folder unless `CLAUDE_CONFIG_DIR` is set on the same line as `claude auth login`. The Keychain entry for a folder is named by the first eight hex digits of the SHA-256 of its path.

Still untested: a "New worktree" thread; the other permission modes; hooks other than SessionStart; how a skill named `cairn` in the plugin `cairn` is listed.

What the results change (agreed 2026-11-26, after the draft was revised that day):

- The plugin form holds. No plain-skills fallback is needed for Claude in T3 Code. This was tested under `~/.claude` only and is rerun under the PILOT instance before the pilot.
- Accounts (agreed, the user's decision): a personal Codex account goes in `~/.codex`, the default folder, and the work account moves to `~/.codex_work`, as was done for Claude. cairn therefore sets no `CODEX_HOME`. Observed 2026-11-26: `~/.codex` is signed in with ChatGPT, T3 Code names its one Codex instance WORK, and the move is not yet done. T3 Code's Codex instance settings have a "CODEX_HOME path" field and a "Shadow home path" field; the second keeps only `auth.json` apart and shares the rest. The command-line review reads the default folder's login, so the personal login must sit in `~/.codex` itself, not in a shadow home.
- `review` runs Codex itself from the command line, read-only, with the reviewer's brief as the prompt. A fresh process has not seen the build, so the review needs no new thread and no extra stop. Observed 2026-11-26: Codex 0.171.0 is installed and has `codex review --base <branch> [PROMPT]` and `codex exec` with a `read-only` sandbox. Neither was run.
- There is one brief and two runners: Codex, or a fresh Claude subagent where Codex is not installed or not signed in. No Codex skill is installed, and `setup` never touches Codex's folder. Findings come back as the command's output, so there is no findings file.
- The read-only sandbox is what keeps Codex from pushing, merging, or editing. Branch rules do not do that job: they hold only force-push and deletion.
- The migration script adds no `AGENTS.md`. Review does not need one, and nothing in this note has Codex doing build work.
- The cold read of text for other readers is done by a fresh Claude subagent.
- State after the user's move, observed 2026-11-26: `~/.codex_work` holds the fluidconcepts.ai login and T3 Code's WORK instance points at it. `~/.codex` holds the jmgirard.com login, so a `codex` started from the command line with no `CODEX_HOME` is the personal account. T3 Code's HOME Codex instance is in "managed" setup mode with no home path and keeps its own login.
- For the pilot: whether a Claude thread in T3 Code can start `codex`, whether that thread's environment carries a `CODEX_HOME`, and whether `codex review` takes a prompt together with `--base`.

## Open

The walk-through and the markup of the steps are complete: every section is agreed as of 2026-11-26, and "Text for other readers" was revised on 2026-11-27. What is left before the build:

- The user's setup before the pilot is done as of 2026-11-27: `writing-for-people` and the logging skill, `cairn-log`, are in `~/.claude` and linked into `~/.claude_personal`, and the samples are at `~/.cairn/samples.md`.
- To cover in the pilot, all untested: the v3 worktree loading from `~/.claude_personal/skills/`; the three T3 Code checks under the PILOT instance; a "New worktree" thread; the other permission modes; whether a hook other than SessionStart runs in T3 Code, which the guest merge hook needs; how a skill named `cairn` in the plugin `cairn` is listed; whether a Claude thread in T3 Code can start `codex` and what `CODEX_HOME` it carries; whether `codex review` takes a prompt together with `--base`; whether a drafter given both the repo's examples and the user's samples keeps conventions and voice apart; and whether a session leaves the writing skill alone for documentation when the skill's description matches.

The build of the core, 2026-11-27:

- A separate session built the core on branch `jg/v3-7406cc`: six commits on 94b23e2a, in the worktree `.claude/worktrees/v3-7406cc`, not pushed. It holds the Rulebook (2,088 words), `status` (190), `start` (509), `resume` (205), `review` (645), the reviewer's brief (237), five templates, the status script, and the session-start hook. Its full report is `v3-core-build-report.md` in the sessions' shared notes folder, outside the repo.
- Observed 2026-11-27 from the design session: the two unittest suites pass (42 and 6 tests); `claude plugin validate` passes with two warnings (a `CLAUDE.md` at the plugin root is not loaded as context, and the plugin has no icon); the status script, run in this checkout and in chromodoris, prints only the v2 notice and writes nothing; and a `claude -p --plugin-dir` run with `CLAUDE_CONFIG_DIR` set to `~/.claude_personal` lists the skill as `cairn:cairn` and, in chromodoris, receives the hook's text. The four verb files were read against "Steps per verb" and no step was found missing or changed, apart from the choices below.
- Not done: no verb has run, Codex was not run, and nothing was tried in T3 Code.
- Choices the build made where this note was silent, to confirm or change after the pilot. The home folder has `plans/`, `shelf/`, and `done/`. A repo is the user's own if `cairn/ROADMAP.md` is in the checkout, a guest if the home folder has a `ROADMAP.md`, and v2 if `cairn/DECISIONS.md` or `cairn/milestones/` is in the checkout. `Phase:` is `plan`, `build`, `review`, or `pr #N`. A road plan has a Choices section, so the user's answers to the question set last into a second sitting. The reviewer runs as `codex exec --sandbox read-only`, since `codex review` in 0.172.0 has no sandbox flag. `resume` checks for a missing plan before `Blocked on:`, and for a merged PR it does `review`'s last step. The Rulebook says no push is ever forced. The guest guard hook is not built.
- Settled 2026-11-27 by the user in the build session, as that session's report records, on the questions the build raised. The build branch holds the first, second, and fourth.
  1. A `[high]` finding kept as a row gets an issue and its `(#N)`; one fixed now gets none (see "Review findings").
  2. The Zotero steps are out of the pilot. The Rulebook's Zotero sentences and the `Zotero collection:` profile line are cut until `source add` and the Zotero script are built, and they come back with them.
  3. `setup` stays after the pilot, so a v2 repo's notice points to a verb that is not built yet.
  4. A guest work branch is pushed to `origin`, never to `upstream`. v2's `Push remote:` line is gone, and migration carries over no guest profile line except `Maintainer: yes`.
  5. v3 ships no reference profiles. Migration copies each repo's verify, changelog, and release sections into the new profile unchanged. A new repo's Release says "none" until its first release, when `release` works the steps out with the user and writes them in.
  6. Migration moves `DECISIONS.md`, `LESSONS.md`, `milestones/`, and `reviews/` to `cairn/archive/`, and in a guest repo to `archive/` in the home folder. The status script reads a repo as v3 once `DECISIONS.md` and `milestones/` are no longer directly under `cairn/`.
  7. A PR in the user's own repo that closes without merging gets no step.
  8. The guest hook is built after the pilot (see the build order). Whether a hook other than SessionStart runs in T3 Code is tested in the pilot with a throwaway hook in the PILOT instance's own settings.
- Setup done on 2026-11-27, at the user's word. The build session made `~/.cairn` a git repo with one commit holding `samples.md` and no remote, and migrated chromodoris by hand in one pushed commit (7fc39fe): the v2 files moved to `cairn/archive/`, ROADMAP became six v3 rows, and `CLAUDE.md` got a v3 section. The design session made a lasting checkout, `~/github/cairn-v3`, on a new branch `v3` at cc543dcf, and pointed `~/.claude_personal/skills/cairn` at it, since the build session's worktree may go when that session is archived. Observed that day: a `claude -p` run with `CLAUDE_CONFIG_DIR` set to `~/.claude_personal`, in chromodoris, lists `cairn:cairn` and receives the hook's listing, which opens "cairn: jmgirard/chromodoris (own repo)". Further v3 changes go on `v3` in that checkout.
- Left before the pilot, all the user's: the T3 Code checks under PILOT (the hook runs, the skill is listed, a write to `~/.cairn` raises no prompt, and `/cairn status` finds the status script); the throwaway hook; and the choice of the three pieces of work. Until the cutover, chromodoris is worked only from PILOT, since v2 no longer reads it correctly. Its first row asks to re-run the design interview, which v3 does not have.
- Expected in the pilot: deleting the local branch after a merge fails in a worktree that has it checked out, which is how a "New worktree" thread in T3 Code runs.
