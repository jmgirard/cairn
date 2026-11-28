# release

Prepares a release. It never submits or publishes one.

## Steps

1. In a guest repo, stop unless the profile says `Maintainer: yes`: a release is the maintainers' act.
2. Check the preconditions: a clean tree, on the default branch and up to date with the remote, and the profile's `verify` passing.
3. Ask for the version decision. The question lists the work in flight and any open `[high]` rows. (stop)
4. Consolidate the changelog under that version: retitle the heading, group the entries, and remove noise. Reword an entry only where the reader in the next step finds a fault.
5. Have a fresh subagent read the consolidated section cold, against the code at the release commit. It reports what a user would take from the section, and any statement the code does not bear out. Fix what it finds.
6. Run the profile's release steps. Leave any push, tag, or submission among them for step 8.
7. Commit the version bump and the changelog: to the default branch in the user's own repos, and through a PR in a guest repo the user maintains.
8. Hand the user the submission checklist, with the release section quoted in full. Never submit or publish. Push and tag at the user's word. (stop)

## Done

The version bump and the consolidated changelog are committed. The user has the checklist and the release section. Nothing is pushed, tagged, submitted, or published except what the user said to push or tag.
