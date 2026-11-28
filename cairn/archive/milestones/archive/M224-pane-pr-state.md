# M224: The pane shows each handed-off PR's review state

**Status:** done (2026-10-08, PR #231 https://github.com/jmgirard/cairn/pull/231)

**Goal:** On request, the cairn pane shows the GitHub state of each blocked milestone's pull request and a Button for its next step.

**Outcome:** Blocked rows gained `url`, the PR URL up to its number
(`pr_url`, `prUrl`). `readPrs` in `register.tsx` runs one `gh pr view
<url> --json state,reviewDecision` per URL, 15 s timeout. It runs after
each pane open and at the BLOCKED heading's `Refresh` press, never on a
timer or a turn end, and only the newest read writes. `prWord` gives
`merged`, `closed`, `changes requested`, `approved`, `in review`, or
`unknown`, kept by URL in the `prs` atom (tags `prs-1`, `pane-4`).
Finish, Revise, and Check run review, implement, and `/milestone` with
no `/clear`, and do nothing while a cairn skill runs. Docs describe it.

**Decisions:** none promoted. The T1 probe showed a test hook answers the
mod's `$.process.run`, and a desktop mod runs `gh` from the app's `PATH`.
The look ran in the operator's insight session, where M006 read `in
review`. The merge was approved with no `Refresh` press seen.

**Review:** claim audit, 46 claims, 3 corrected. Three lenses: 8 fixed
(step check, newest read writes, one word type, test gaps), 4 to "Pane
PR-state edges (M224 review)", 6 rejected. Mod tests went to 1469.
Nothing retired.
