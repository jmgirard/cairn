# status

Read-only. Never change files, branches, or anything on GitHub.

## With no argument

1. Run the status script and show its listing as printed.
2. Add the user's open PRs on the repo and the state of each: its checks, its reviews, and whether it waits on someone else. Read them from GitHub. In a guest repo, read the host repo.
3. Recommend one next action.

## With a slug or a GitHub number

1. Find the plan with the status script's `plan` lookup.
2. For a number with no plan, ask GitHub in one call whether it is an issue or a PR: `gh api repos/<owner>/<repo>/issues/<N>` answers for both, and a PR carries a `pull_request` field.
3. Report on that one item. For a plan: its route, its phase, what is done and what is left, what it is blocked on, and the state of its PR. For an issue or a PR with no plan: what it asks for and where it stands.
4. Recommend one next action.

## Done

The user has the listing or the report, and one recommended next action. Nothing has changed.
