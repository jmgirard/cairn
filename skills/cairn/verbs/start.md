# start

Takes an idea, a GitHub issue, or a bug from the request to the review.

## Steps

1. If the request is trivial, say so and do it. In the user's own repos, commit to the default branch and push. In a guest repo, make the edit on a branch and open a PR at the user's word. The rest of this file does not apply.
2. If the item is a `[blocked]` row, check whether what it waits for has happened. If it has not, say so and stop, unless the user says to go on. (stop)
3. Fetch. Investigate the code as it stands on the remote's default branch before asking anything. For an issue, read the issue and its comments.
4. Pick trail or road, and propose the slug. Say both in one line and go on. The user can overrule either, and the slug can change until the first commit. In a guest repo, also say how many of the user's PRs are open on the host.
5. Road only: ask one question set, each question with a recommendation. (stop)
6. Guest repos, road only: check that a maintainer has agreed to the change in an issue before planning it. If none has, say so and stop. Skip this step where the profile says `Maintainer: yes`. (stop)
7. Write the plan in the home folder from its template, with its `Route:`, `Branch:`, and `Issue:` lines. Cut the branch from the remote's default branch and name it for the slug. If the app already made a branch for this work, record that one. In a guest repo, name the branch the way the host does.
8. Account for everything the user asked for: in this plan, in a later one, as a candidate row, or dropped at the user's word. Record each in the plan.
9. For a bug, write the regression test first and see it fail.
10. Work task by task: the test first, then the code, then a commit. Keep the plan's `Phase:` line current.
11. When the work takes a value or a claim from a source, add a reference note for it. The note rides in the PR. Until `source add` is built, write the note and its index line by hand: the citation, what was read and when, and the values or claims taken, with page numbers.
12. New user-facing functions assert what their documentation says they expect.
13. If trail work turns out to need a design choice from the user or a second sitting, stop building and say so. Add the road sections to the plan and ask the question set. (stop)
14. Add the changelog entry the profile calls for, in user-facing words.
15. Run the profile's `verify`.
16. Set `Phase: review` and go straight to `review`.

## Done

The plan is in the home folder. The branch holds the work, with one commit for each task. Nothing has been pushed. `verify` passes, and `review` has begun.
