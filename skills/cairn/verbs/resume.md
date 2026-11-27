# resume

Picks work up where its plan says it stands.

## Steps

1. Find the plan with the status script's `plan` lookup: the current branch's with no argument, otherwise the one the slug or number names. Work on the plan's branch.
2. If the plan is missing on this machine, say so and offer to rebuild it from the branch and the PR. (stop)
3. If the plan says `Blocked on:`, check whether that has cleared. If it has not, say so and stop, unless the user says to go on. (stop)
4. If the plan's PR is open: read the new review comments and CI. Make the fixes and run the profile's `verify`. Draft any reply for the user. Show the fixes and the drafts, and push at the user's word. Never resolve a person's thread. (stop)
5. If the plan's PR has merged, do the last step of `review` for this kind of repo. In a guest repo, do it for a closed PR too.
6. Otherwise continue at the phase the plan shows: `plan` and `build` in `start`, and `review` in `review`.

## Done

The work is further on or waits at a stop, and the plan's `Phase:` line says where.
