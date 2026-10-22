<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M317: Report the open-PR caps in /milestone

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the operator reads `/milestone`'s status report
- **Branch/PR:** —

## Goal

`/milestone`'s status report shows how many of your open PRs count against each open-PR cap, beside the cap.

## Scope

**In:** A cap report in §2 of `skills/milestone/SKILL.md`, built from the list that the "Open hotfix PRs" bullet already reads. README's paragraph on `/milestone`'s audit. CHANGELOG Unreleased.

**Out:** A cap check that stops `/milestone`: it only reports, and `/hotfix` and `/milestone-review` keep the stops. The stacked milestone's base-PR exclusion: it applies only at that milestone's own review read. A script for the count: the neighbor bullets are prose. A live look with an open hotfix PR → the parked row "Live-check the open hotfix PRs bullet".

## Acceptance criteria

- [ ] AC1: `skills/milestone/SKILL.md`'s §2 audit states a cap report that uses the list the "Open hotfix PRs" bullet reads, with no second `gh` call. It reports the number of listed PRs whose `headRefName` starts with `hotfix-` beside the bug-fix cap, and the number of the other listed PRs beside the feature cap. Each cap comes from the `# Bug-fix PR cap:` or `# Feature PR cap:` line of `cairn/PROFILE.md` as tracking-rules' open-PR caps bullet reads it, else 3 and 1. A number at its cap is reported as reaching it, and a number over its cap as over it, with the number shown. A list of 100 PRs is reported as reaching both caps. A failed list read reports no number and names the gap. A cap line whose value is not taken is named. The report writes nothing to GitHub and carries no disposition to §3.
- [ ] AC2: A `/milestone` run in this repo, invoked after the edit is on disk, reports both numbers beside the default caps 3 and 1, equal to the numbers counted from `gh pr list --repo <base-repo> --author @me --state open --limit 100 --json headRefName` in the same session. A second run with a temporary `# Feature PR cap: 0` line in the header of `cairn/PROFILE.md` names that line and keeps the feature cap at 1.
- [ ] AC3: README's paragraph on `/milestone`'s audit and `CHANGELOG.md`'s Unreleased section say that `/milestone` reports the number of your open bug-fix and feature PRs beside each cap.
- [ ] AC4: The `verify` slot of `cairn/PROFILE.md` is green: each of its five commands exits 0.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T2
- AC4 → T3

## Tasks

- [ ] T1: Add the cap report to §2 of `skills/milestone/SKILL.md` after the "Open hotfix PRs" bullet (:223), reusing its list and citing tracking-rules' open-PR caps bullet for the cap values. Leave tracking-rules unchanged, so the rulebook-mass baseline needs no re-seed.
- [ ] T2: Update README's audit paragraph (near :941) and CHANGELOG Unreleased.
- [ ] T3: Run `/milestone` in this repo twice as AC2 states, remove the temporary PROFILE line, compare with the `gh pr list` count, and run the verify slot.

## Work log

- 2026-10-22: created by /milestone-plan.
- 2026-10-22: tier check: not run — work named at the question set.
- 2026-10-22: idea vet: no concern. The report counts by head branch as the caps rule does, the operator asked for it after M315's review stopped at a cap, and the name says what it does.
- 2026-10-22: collision check: source is the candidate row "Report the open-PR caps in /milestone", absorbed in full. The parked row "Live-check the open hotfix PRs bullet" reads the same list; its scope (a live look with an open hotfix PR) stays distinct and is cross-referenced in Out. D-214 sets the caps; this adds a report and changes no cap rule.
- 2026-10-22: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn, so no overlap.
- 2026-10-22: lessons harvest: LESSONS M112 (grep README and docs for restatements; a user-visible change owes a CHANGELOG task) and M149 (rulebook-mass pins, avoided by leaving tracking-rules unchanged).
- 2026-10-22: criteria audit (full mode, fresh Opus reader): 2 findings on this milestone, both fixed. AC1 now reports an over-cap number as over the cap, not as at it. AC2 narrowed to what a run with 0 open PRs can show, plus one untaken cap line. AC3 and AC4 had no finding.
- 2026-10-22: plan gate chose a prose report in the skill over a script that runs `gh`, because the neighbor bullets are prose reads of the same list and a script would add a second read; falsified by a `/milestone` run whose reported numbers differ from the `gh pr list` count.

## Decisions

## Review
