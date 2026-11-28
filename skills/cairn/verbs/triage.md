# triage

Goes over every candidate row with the user, and leaves the ROADMAP in order.

## Steps

1. Fetch, and bring the default branch up to date, so work others have merged is seen.
2. List every candidate row.
3. Check each row against the code and git: already done, subject gone, or still true.
4. For each `[blocked]` row, check whether what it waits for has happened.
5. For each `[high]` row that names a failing input, check that the input still fails.
6. Show one table that proposes promote, keep, or drop for each row, with a one-line reason and any mark to clear. Promote adds `[high]`. Propose it only for a bug that gives a wrong answer in ordinary use. The user may promote any row. (stop)
7. Order the rows: `[high]` first, then the rest, each group from most to least important.
8. Apply the accepted outcomes in one commit to the default branch, and push it. In a guest repo the ROADMAP is in the home folder, and the commit lands in `~/.cairn`.

## Done

Every row has an outcome the user accepted, and the rows are in order. In the user's own repos the one commit is pushed. In a guest repo it is in `~/.cairn`.
