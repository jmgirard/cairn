---
name: cairn
description: Track and ship project work as plans and PRs. Use when the user asks where a project stands or what to do next, wants to start work on an idea, a GitHub issue, or a bug, wants to resume work in flight, or wants work reviewed and merged.
argument-hint: "status [slug|#N] | start <idea, issue, or bug> | resume [slug|#N] | review [slug|#N] | source add <file or URL> | copilot <PR> | setup"
---

# cairn

This page is the Rulebook. It applies to every verb.

## Verbs

| Verb | What it does | Steps |
|---|---|---|
| `status [slug \| #N]` | Shows work in flight, open PRs, and candidates. Changes nothing. | `verbs/status.md` |
| `start <idea, issue, or bug>` | Investigates, plans, builds, and goes on to review. | `verbs/start.md` |
| `resume [slug \| #N]` | Picks work up at the phase its plan shows. | `verbs/resume.md` |
| `review [slug \| #N]` | Checks the work, asks the merge question, and ships on approval. Also reads someone else's PR. | `verbs/review.md` |
| `source add <file or URL>` | Puts a source on the shelf and writes its reference note. | `verbs/source-add.md` |
| `copilot <PR>` | Handles Copilot's review notes on a PR, in a guest repo. | `verbs/copilot.md` |
| `setup` | Sets cairn up in a repo, or converts a repo from cairn v2. | `verbs/setup.md` |

The verb files are in this skill's folder, `${CLAUDE_SKILL_DIR}`. Read the verb's file, then follow its steps in order. A step marked (stop) waits for the user. Between stops, decide and go on. If the request names no verb, pick the one that fits and say which. With no request at all, run `status`.

`triage` and `release` are not built yet. If the user asks for one, say so.

The status script is `python3 "${CLAUDE_SKILL_DIR}/../../scripts/cairn_status.py"`. It prints the listing: the kind of repo, the home folder, the work in flight, and the candidates. With `plan`, `plan <slug>`, or `plan '#N'` it prints the path of one plan: the current branch's, the one whose slug starts that way, or the one with that issue or PR number.

The Zotero script is `python3 "${CLAUDE_SKILL_DIR}/../../scripts/cairn_zotero.py"`. `find` looks a source up, `add` adds one with its file, and `collect` puts an existing item in a collection. `-h` after a command lists its options. It starts Zotero in the background if Zotero is not running.

The migration script is `python3 "${CLAUDE_SKILL_DIR}/../../scripts/cairn_migrate.py"`. It converts a repo's cairn v2 files. With no flag it says what it would change, and with `--apply` it changes it.

## Sizes

- **Trivial**: an edit with no runtime surface, such as a typo, a comment, or a ROADMAP row. It has no plan.
- **Trail**: work that fits one sitting and one PR and leaves the user no design choice.
- **Road**: everything larger.

Trail and road work each have a plan and end in a PR. A bug gets a regression test written first, at either size.

## Approval

- Work happens on a branch. Nothing reaches the default branch without the user's approval at the merge question. A trivial edit is the one exception: the user's request approves it.
- Nothing is pushed, merged, posted to GitHub, tagged, or deleted except at a step that names it. No push is ever forced.
- Ask only what the user alone can decide, in one batch.

## Where files live

Each repo has a home folder outside git, `~/.cairn/<owner>/<repo>/`. The owner and repo come from the base remote: `origin` in the user's own repos, and in a guest repo `upstream` where that remote exists, else `origin`. The status listing opens with the kind of repo and the folder's path.

| | The user's own repo | A guest repo |
|---|---|---|
| `ROADMAP.md`, `PROFILE.md`, `references/` | the checkout, under `cairn/` | the home folder |
| `plans/` (active plans) | the home folder | the home folder |
| `shelf/` (source files) | the home folder | the home folder |
| `done/` (plans of finished work) | not kept | the home folder |

- A guest repo is one other people share.
- `references/` holds `INDEX.md` and one note for each source.
- `~/.cairn/samples.md` holds pieces of the user's own writing.
- `~/.cairn` is the user's private git repo. Commit to it only at a step that says so. Never push it.

## File formats

Each file is a fixed set of questions, and the answers are the file. Give each item one sentence. An empty section says "none". The templates are in `${CLAUDE_SKILL_DIR}/templates/`.

### ROADMAP

`ROADMAP.md` lists candidates: work that is proposed and not started. Work in flight is read from plans and branches and has no row. Each row is one list item: its marks, a title, a colon, and one sentence on what the work is and why.

- The title says what the work would do in about six words, starting with a verb. It is unique in the file. It ends with `(#N)` when the row comes from an issue.
- `[high]` marks a bug that gives wrong answers or misleads users now, in ordinary use as "Review findings" defines it. The row says what goes wrong and points to that use. Set or propose `[high]` only for that kind of bug. The user may put it on any row.
- `[blocked]` marks work that cannot move until something outside happens. The row ends with a sentence that starts "Waits for" and names the issue, PR, or release to look at, where there is one.
- Marks open the row, and a row may carry both. `[high]` rows come first in the file.

### Plan

A plan is `plans/<slug>.md` in the home folder. The slug is two to four lowercase words joined by hyphens. It differs from the slug of every active plan and, in a guest repo, of every plan in `done/`. The user may type any unique start of it.

The plan opens with labeled lines:

- `Route:` is `trail` or `road`.
- `Branch:` is the branch the work is on. Lookups go through this line, since an app or a host repo may name the branch.
- `Issue:` is `#N` where the work starts from a GitHub issue.
- `Phase:` is `plan`, `build`, `review`, or `pr #N` once the PR is open.
- `Blocked on:` is what the work waits for, where it cannot move.

Then comes one heading for each question. A trail plan has four:

- **What is wrong or wanted**
- **The change**
- **How to check it**: the checks, one to a line.
- **Review**: one evidence line for each check, and one line for each dropped finding.

A road plan has three more:

- **Scope**: what is in, and everything the user asked for that is not, each marked as later, a candidate row, or dropped.
- **Choices**: each answer the user gave to the question set, and each choice of the session's that changes what the user gets.
- **Tasks**

In a road plan, "How to check it" holds the acceptance criteria: at most 7, each naming one check. More means two plans. A trail plan that grows becomes a road plan by gaining the three sections. Nothing is renamed.

### Merge record

The merge record is written once, from the plan. It is the PR description and the squash commit message, so it has labeled lines and no `#` headings. Each label is complete when it covers its list, with one sentence for each item. Drop a label that has nothing under it.

- `What changed:` covers every changelog entry in the PR.
- `Why:` says what was wrong or wanted.
- `Choices made:` covers every answer the user gave to the question set, and every choice of the session's that changes what the user gets.
- `Left out:` covers every item the plan marks as later, a candidate row, or dropped. It does not list dropped findings.
- `How it was checked:` covers every check in the plan, with its result.

### PROFILE

`PROFILE.md` has three headings: **Verify** (the commands that check the repo), **Changelog** (the file, and how an entry is added), and **Release** (the release steps). Two labeled lines may sit above them:

- `Maintainer: yes`, in a guest repo the user maintains. Only the user adds this line.
- `Zotero collection: <name>`, which turns the Zotero steps on and names the collection the repo's sources go in.

### Reference note

A reference note is `references/<citekey>.md`, and the source's file sits on the shelf under the same citekey. The note has two labeled lines and one heading:

- `Citation:` is the full citation.
- `Read:` is what was read and when, or `not obtained` with the date.
- **Taken from it**: each value or claim taken from the source, with its page number.

Each note has one line in `references/INDEX.md`: the note's file name and what the source is for.

## Review findings

Sort every finding first by its ordinary-use pointer. A pointer is a user's report; the repo's own documentation, examples, or tests showing that use; or a call in a package that depends on the repo. An input the reviewer had to construct has no pointer. Judge by the pointer, never by a guess at how many users do it.

A finding with a pointer goes through three questions in order. The first yes decides.

1. Did this PR cause it or make it worse? Fold it in.
2. Is it older, but fixed in lines the PR already changes, with no new check needed in the plan? Fold it in.
3. Is it older, with a concrete input that fails today and comes from ordinary use? Propose an issue. The issue is the failing input in a code block and where that input comes from.

Otherwise drop it.

- An input that worked before the PR and fails after it is always folded in.
- A statement the diff adds about what the code does, which the code does not bear out, is a finding the PR caused.
- A finding without a pointer is an edge case. Never fix one by making the input work. Add an input check, or drop it.
- An input check is one assertion at the entry of a user-facing function that refuses the input with a clear error. Add one when three things hold: the PR adds or changes that function; today's result for the input is a wrong answer or an unclear error; and one assertion at the entry is enough. Write it in the repo's own idiom, with one test line and one changelog line. In a guest repo, add one only where the host's nearby code already asserts its inputs.
- Each dropped finding gets one line in the plan.
- Issues are proposed at the merge question and opened only after the user approves them.
- A finding never becomes a candidate row. The one exception is a `[high]` finding. At the merge question the user chooses a fix to start now, which gets no issue, or a row, which gets an issue and carries its number.

## Sources

- Look for a cited source in this order: the references index and the shelf; then Zotero, where the profile has a `Zotero collection:` line; then the web. Look in Zotero with the Zotero script's `find`. Copy a file it finds to the shelf, and put its item in the repo's collection with `collect`.
- If a cited source is not on the shelf and its full text cannot be found, ask the user for the file before going on with anything that rests on it. Never treat the source as nonexistent. Never use an abstract or someone else's summary in its place. If the user cannot supply the file, record the source as not obtained, with the date, and rest nothing on it. (stop)

## Guest repos

- Nothing of cairn goes in the checkout.
- Never push the default branch. Even a trivial edit goes through a PR.
- Push a work branch to the host repo where the user may push there, and to the user's fork otherwise.
- Never merge or release unless the profile says `Maintainer: yes`, and then only at the user's word.
- Post nothing upstream without the user's approval.
- Match the host's conventions. No cairn vocabulary reaches a host repo.

## Text for other readers

- Standalone prose is what the work produces for readers: changelog entries, vignettes, new help pages, README sections, and PR and issue text in a guest repo. A fresh subagent that never saw the session drafts it. Its brief holds the facts, two or three existing texts of the same kind from the repo, and the user's samples where `~/.cairn/samples.md` exists. The brief labels each for its job. The examples set the conventions: length, structure, format, and terms. The samples set the voice: phrasing, and never subject or length.
- A second fresh subagent reads the draft cold and reports what it says and what it asks of the reader. If that differs from the brief, redraft from the brief. For text posted after the review, give the cold reader the diff too, and have it report any statement about behavior that the diff does not support.
- Inside a cairn verb, this step writes what the work produces, even where a writing skill of the user's says it covers them. That skill writes replies and messages to people.
- Text woven into code is written inline: code comments, edits to existing help text, and error and warning messages. It says what the code does or why, never the story of the change, and it matches the neighboring text.
- The merge record, and issues in the user's own repos, are written directly from their questions.
- The user sees each text once, at the merge question. Never preview an internal file in chat.
