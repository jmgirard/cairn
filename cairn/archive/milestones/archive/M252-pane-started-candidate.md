# M252: The cairn pane marks a candidate row that an open pull request names

**Status:** done (2026-10-15, PR #263 https://github.com/jmgirard/cairn/pull/263)

**Goal:** In the cairn pane, a candidate row that the body of one of the operator's open pull requests names draws a started mark and that pull request's number.

**Outcome:** The pane's one `gh pr list` call asks for `body`.
`startedRows` in `pane.ts` reads each body line that opens with exactly
`Candidate row: ` into `{ title, number }`, from any head branch. The
items share the `hotfixes` value (tag `hotfixes-2`), kept or emptied with
the hotfix list. `paneLines` draws a matched line with `STARTED_MARK` ◐
in the review color, `#<n>` (lowest) in its tail, and no ✎, and
`pressCandidate` refuses a stale ✎ press on such a row. In owner mode
`/hotfix` and `/milestone-review` write one unwrapped line per row the
merge removes or narrows; guest and companion PRs carry none. README,
DESIGN, CHANGELOG, and types describe it. Mod tests 1729.

**Decisions:** none promoted. The question set chose ◐ in green, ✎
hidden, milestone PRs included with the checkout limit documented, and no
live look. The plan chose a PR-body line over a ROADMAP row marker.

**Review:** claim audit, 41 claims, 6 corrected. Three lenses and Copilot
(Lite), 28 findings: 12 fixed (the stale ✎ check, 3 test fixes, skill
wording, README limits), 5 to "Started mark edges (M252 review)", 11
rejected. Copilot: 2 rejected, 1 noted. Nothing retired.
