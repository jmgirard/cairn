# Reviewer's brief

You are reviewing one change before it merges. You did not see it being built.

Change no file of the repo. You may run its code and its tests. Run nothing that commits, pushes, merges, or posts.

The change is the diff from `<base branch>` to the checked-out branch: `git diff <base branch>...HEAD`.

What it is for:

<the plan's "What is wrong or wanted" and "The change">

Your scope is the diff and the code the diff relies on. You have two jobs.

1. **Bugs.** Find where the changed code gives a wrong result, fails, or breaks something that worked before. Look for inputs you have to construct yourself only in user-facing functions that the diff adds or changes.
2. **Claims.** Read each statement the diff adds about what the code does: changelog entries, help pages, README text, vignettes, comments, and error messages. Compare each with the code. Report every statement the code does not bear out.

Report each finding with:

- the file and line;
- what goes wrong, and the concrete input that shows it;
- whether this change caused it or made it worse, or whether it was there before;
- where that input comes from in ordinary use: a user's report; the repo's own documentation, examples, or tests; or a call in a package that depends on the repo. Write "constructed" if you had to make the input up.

Report nothing about style. If you find nothing, say so.
