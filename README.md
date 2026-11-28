# cairn

*A cairn is built one stone at a time, and marks the trail for whoever comes next.*

## What cairn is

When Claude Code does the work in a repository, you still need to know where that work stands and why each change was made.

cairn is a Claude Code plugin that tracks project work as plans and pull requests (PRs). It is one skill, `/cairn`, that takes a verb, such as `status` or `start`. The agent does the work, and you approve every merge.

It grew out of maintaining many R packages with Claude Code and rebuilding similar tracking systems in each. It is not specific to R.

## What you get

- A list of candidates (i.e., work that is proposed and not started).
- A plan for each piece of work larger than a trivial edit.
- An independent review before every merge.
- A status view.
- A reference library for the sources your work relies on.

cairn is also short on purpose, so the agent has less to read each session and fewer rules to over-apply. Its text is about 5,700 words. The version before this one, 2.2.0, had about 82,000.

## What it needs

- Claude Code
- git
- The GitHub CLI (`gh`), signed in
- Python 3 (the scripts use the standard library only)
- Optional: the Codex CLI, signed in, which then acts as the independent reviewer. Without it, a fresh Claude subagent reviews.
- Optional: Zotero 10 or later, if you want sources added to a Zotero collection.

## Install

Pick one of these two ways, because using both installs the plugin twice.

The first is to clone the repo and symlink it into your Claude Code skills folder (`~/.claude/skills` by default). The plugin loads from your checkout, so `git pull` updates it.

```bash
git clone https://github.com/jmgirard/cairn
ln -s /path/to/cairn ~/.claude/skills/cairn
```

One caution: the symlink is live. Your next session, in every repo, loads whatever branch the checkout is on. To try cairn for one session without installing:

```bash
claude --plugin-dir /path/to/cairn
```

The second is the marketplace, which is a frozen snapshot that you reinstall to update.

```bash
claude plugin marketplace add jmgirard/cairn
claude plugin install cairn@cairn
```

Then, in a repo, run `/cairn setup`. In a new repo of your own, it writes `cairn/ROADMAP.md`, a profile (`cairn/PROFILE.md`) that holds your repo's test command, a references index, and a short section in `CLAUDE.md`. It also offers two GitHub rules for your default branch: no force-push and no deletion. Claude Code may list the skill as `cairn:cairn`, but typing `/cairn` works.

The install includes two hooks. Both do nothing outside cairn repos. One prints a short status listing at session start. The other is a guard for repos you share with other people, described below.

## A day with cairn

`/cairn status` shows the work in flight with its phase (planning, building, in review, or waiting on its PR) and what blocks it, your open PRs, the candidates, and one recommended next action. It changes nothing.

`/cairn start`, followed by an idea, an issue number, or a bug, investigates the code first. Then it picks a size and tells you which. There are three sizes:

- A **trivial edit** does not change how the code runs (e.g., a typo or a comment). In your own repos, it is committed straight to the default branch.
- A **trail** fits one sitting and one PR, and leaves you no design choice.
- A **road** is everything larger. It starts with one set of questions, each with a recommendation.

You can overrule the size. For a trail or a road, cairn writes a plan, cuts a branch, and builds test-first with one commit per task. For a bug, it writes the regression test first and sees it fail. Then it goes straight to review.

Review ends at the merge question, which is the one place cairn always stops. It shows you:

- the merge record, which is a written account of the change;
- the changelog entry in full;
- other changed documentation, by file;
- the review findings that changed something;
- any issues it proposes to open;
- how many findings it dropped;
- which reviewer ran.

Nothing is pushed before you approve. On your approval, it pushes, opens the PR, waits for CI, squash-merges, and deletes the plan and the branch.

`/cairn resume` picks work up in a new session, at the phase its plan shows.

For example, a user reports that `summarize()` drops the last group when the grouping column has missing values. You type:

```text
/cairn start summarize() drops the last group when the grouping column has NAs
```

cairn reads the code, calls it a trail, and names it `fix-na-group-drop`. It writes a test that fails, makes the fix, adds a changelog entry, and has the change reviewed. It stops and shows you the merge record. You approve, and your default branch gains one commit.

## The other verbs

`/cairn triage` goes over every candidate row with you. It checks each against the code: whether the work is already done, whether the thing it is about still exists, and whether it is still true. It proposes one outcome for each row in one table (promote it to urgent, keep it, or drop it) and applies your choices in one commit.

`/cairn source add <file or URL>` puts a source's file on the shelf (i.e., a folder outside your repo) and writes a reference note. The note has the citation, what was read and when, and the values or claims taken from the source, with page numbers. If cairn cannot get the full text, it asks you for the file. It never writes a note from an abstract. If your profile names a Zotero collection, it also adds the source there.

`/cairn release` checks that the tree is clean and the checks pass, asks you for the version, and consolidates the changelog. It has a fresh subagent, which has not seen the session, check that section against the code, runs your profile's release steps, and hands you a checklist. It never submits or publishes anything. It pushes and tags only when you say so.

`/cairn copilot <PR>` is for repos you share with other people. It handles GitHub Copilot's review notes on your PR: it fixes, rejects, or defers each one, and drafts at most one comment per review. It pushes, posts, and resolves only when you say so. It never resolves a person's thread.

## What lives where

In the table below, the first three paths are in your repo. The last two are outside the repo, in a home folder.

| Path | What it holds |
| --- | --- |
| `cairn/ROADMAP.md` | The candidates, and nothing else |
| `cairn/PROFILE.md` | This repo's commands, in three sections: Verify (the checks to run), Changelog, and Release |
| `cairn/references/` | An index and one note per source |
| `~/.cairn/<owner>/<repo>/plans/` | One file per piece of work in flight, named for a slug of two to four words |
| `~/.cairn/<owner>/<repo>/shelf/` | Source files, such as PDFs |

A ROADMAP row is one list item: a title, a colon, and one sentence on what the work is and why. Two marks can open a row. `[high]` marks a bug that gives users wrong answers now. `[blocked]` marks work that waits on something outside, and the row says what.

The merge record answers five questions: what changed, why, the choices made, what was left out, and how it was checked. It is the PR description and the squash commit message. So your default branch gets one commit per piece of work, and each commit explains itself. In your own repos, the plan is deleted after the merge.

`~/.cairn` can be a private git repo that you sync yourself. cairn commits to it locally and never pushes it.

## How review works

Review reruns every check in the plan, and the commands in your profile.

Then one independent reviewer, which did not see the work being built, reads the diff. Where the Codex CLI is installed and signed in, the reviewer is Codex, working in its own copy of the repo with no network access. Otherwise it is a fresh Claude subagent.

The reviewer has two jobs. One is to find bugs. The other is to check, against the code, each statement the change adds about what the code does. Those statements are in the changelog, help pages, README, comments, and error messages.

Findings are sorted by whether they come from ordinary use. That means a user's report, the repo's own documentation, examples, or tests, or a call in a package that depends on the repo.

- A problem the change caused is fixed in the same PR.
- An older problem with a failing input from ordinary use is proposed to you as an issue.
- A problem that only shows on an input the reviewer had to make up gets an input check (i.e., one assertion that refuses the input with a clear error) or is dropped. It is never fixed by making that input work.

## Working in someone else's repo

A repo that other people share is, to cairn, a guest repo. There, nothing of cairn goes in the checkout. The ROADMAP, the profile, the references, and the plans all live in the home folder, and a finished plan is kept there.

Every change goes through a PR, a trivial one included. cairn never pushes the default branch. It never merges or releases unless the profile says `Maintainer: yes`. You add that line by hand, and even then cairn merges or releases only when you say so. It posts nothing upstream without your approval, and what it writes follows the host repo's conventions.

The guard hook denies a push to the default branch, and denies a merge without that line.

## Coming from cairn 2.x

Run `/cairn setup` in each repo. It shows what the migration would change, and changes it only after you say yes. Your old decisions, lessons, and milestone archive move to `cairn/archive/`, where nothing reads them. Work in flight is carried over. Setup then goes through your old Known issues (a section of `DESIGN.md` in v2) and your candidates with you in one table. `CHANGELOG.md` lists everything that was removed.

## What cairn does not do

- It has no format validator. The status listing names any file it cannot read.
- It puts no cap on open PRs or on candidates.
- It never submits or publishes a release.
- It posts nothing to GitHub without your word.
- It keeps no decision log. The reasoning for a change lives in its merge record and in code comments.
- It runs in Claude Code only. Codex is used only as a reviewer.

## Status

Version 3.0.0 is a rewrite of 2.x. So far, it has been used for real work in one repository.

Release history is in `CHANGELOG.md`, and the license is MIT.
