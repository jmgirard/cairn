# review

One review for both sizes. It checks the work, asks the merge question, and ships on approval.

Find the plan with the status script's `plan` lookup: the current branch's with no argument, otherwise the one the slug or number names. If the argument is someone else's PR, go to "Someone else's PR".

## Steps

1. Fetch, and sync the branch with the remote's default branch. If the branch moved, rerun the tests.
2. Run every check in the plan fresh. Record one evidence line for each under the plan's Review heading.
3. Run the profile's `verify`.
4. Get one independent review of the diff. The reviewer's brief is `reviewer-brief.md` in this skill's folder, with the base branch and the plan's first two sections filled in. Where Codex is installed and signed in (`codex login status`), run it from the command line in its own copy of the repo, with no network and with its input closed: `codex exec --sandbox workspace-write -c sandbox_workspace_write.network_access=false --worktree "<the brief>" < /dev/null`. In its own copy Codex can run the code and the tests, and it cannot change this checkout, commit, or push. With its input left open, Codex waits and never starts. Wait for the Codex process to exit. Its report is the last thing it prints, and a run that is still going has not failed. After it exits, remove the copy Codex made: `git worktree list` shows it, under Codex's own folder. Otherwise, or if Codex exits without a report, give the brief to a fresh subagent.
5. Sort each finding by its ordinary-use pointer, then put it through the Rulebook's three questions. Fix the fold-ins, add the input checks, and rerun what they touch. Give each dropped finding one line in the plan, marked as an edge case or as other.
6. Make the ROADMAP edits on the branch, so they ride in the PR: remove the row this work came from, and add the rows the plan leaves as candidates.
7. Write the merge record from the plan, as answers to its five questions.
8. Ask the merge question. (stop) Show:
   - the merge record;
   - the changelog entry, quoted in full;
   - other changed documentation, by file;
   - the findings that changed something;
   - the issues proposed;
   - any `[high]` finding, offered as a fix to start now, with no issue, or as a row with an issue;
   - the two counts of dropped findings, edge cases and other;
   - which reviewer ran.
9. On approval only: for each `[high]` finding kept as a row, open its issue and add the row with its `(#N)`. Push the branch and open the PR. Its title says what the work does in one line, and its description is the merge record. Set `Phase: pr #N`. Wait for CI. Squash-merge with the merge record as the commit message: `gh pr merge <N> --squash --subject "<title> (#<N>)" --body-file <file>`. If a CI fix changes what the user approved, ask again.
10. After the merge: open the other approved issues. Commit `~/.cairn` where it is a git repo, so the plan stays in its history. Then delete the plan and the branch. A fix the user chose to start now begins with `start`.

## Guest repos

Steps 1 to 5 are the same. The ROADMAP edits are made in the home folder. No merge record is written. Then:

6. A fresh subagent drafts the PR text to the host's conventions and in the user's voice, and a second reads it cold against the diff.
7. Ask whether to open the PR. (stop) Show the PR text, the items of the merge question apart from the merge record, and how many of the user's PRs are open on the host.
8. On approval only: push the branch, open the PR, and set `Phase: pr #N`. Stop at the open PR. (stop)
9. Where the profile says `Maintainer: yes`, merge at the user's word, with the host's merge method and message. Never use the admin override unless the user says so.
10. Once the PR is merged or closed, move the plan to `done/`.

## Someone else's PR

Read it, test it, and report the findings to the user. Post nothing without the user's word.

## Done

In the user's own repos: the default branch has one squash commit for the work, with the merge record as its message; the approved issues are open; the plan and the branch are gone. In a guest repo: the PR is open and the plan says `pr #N`, or the PR is merged or closed and the plan is in `done/`.
