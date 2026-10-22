<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M317: Report the open-PR caps in /milestone

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the operator reads `/milestone`'s status report
- **Branch/PR:** m317-milestone-pr-caps https://github.com/jmgirard/cairn/pull/330

## Goal

`/milestone`'s status report shows how many of your open PRs count against each open-PR cap, beside the cap.

## Scope

**In:** A cap report in §2 of `skills/milestone/SKILL.md`, built from the list that the "Open hotfix PRs" bullet already reads. README's paragraph on `/milestone`'s audit. CHANGELOG Unreleased. Naming `/milestone` among the cap lines' readers in tracking-rules (its `cairn/PROFILE.md` row and its open-PR caps bullet) and in `hooks/cairn_common.py`'s comment, with the rulebook-mass seed re-seeded in its three pins.

**Out:** A cap check that stops `/milestone`: it only reports, and `/hotfix` and `/milestone-review` keep the stops. The stacked milestone's base-PR exclusion: it applies only at that milestone's own review read. A script for the count: the neighbor bullets are prose. A live look with an open hotfix PR → the parked row "Live-check the open hotfix PRs bullet".

## Acceptance criteria

- [x] AC1: `skills/milestone/SKILL.md`'s §2 audit states a cap report that uses the list the "Open hotfix PRs" bullet reads, with no second `gh` call. It reports the number of listed PRs whose `headRefName` starts with `hotfix-` beside the bug-fix cap, and the number of the other listed PRs beside the feature cap. Each cap comes from the `# Bug-fix PR cap:` or `# Feature PR cap:` line of `cairn/PROFILE.md` as tracking-rules' open-PR caps bullet reads it, else 3 and 1. A number at its cap is reported as reaching it, and a number over its cap as over it, with the number shown. A list of 100 PRs is reported as reaching both caps. A failed list read reports no number and names the gap. A cap line whose value is not taken is named. The report writes nothing to GitHub and carries no disposition to §3.
- [x] AC2: A `/milestone` run in this repo, invoked after the edit is on disk, reports both numbers beside the default caps 3 and 1, equal to the numbers counted from `gh pr list --repo <base-repo> --author @me --state open --limit 100 --json headRefName` in the same session. A second run with a temporary `# Feature PR cap: 0` line in the header of `cairn/PROFILE.md` names that line and keeps the feature cap at 1.
- [x] AC3: README's paragraph on `/milestone`'s audit and `CHANGELOG.md`'s Unreleased section say that `/milestone` reports the number of your open bug-fix and feature PRs beside each cap.
- [x] AC4: The `verify` slot of `cairn/PROFILE.md` is green: each of its five commands exits 0.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T2
- AC4 → T3

## Tasks

- [x] T1: Add the cap report to §2 of `skills/milestone/SKILL.md` after the "Open hotfix PRs" bullet (:223), reusing its list and citing tracking-rules' open-PR caps bullet for the cap values. Name `/milestone` as a reader where tracking-rules and `hooks/cairn_common.py` list them, and re-seed the rulebook-mass figure in its three pins (LESSONS M149).
- [x] T2: Update README's audit paragraph (near :941) and CHANGELOG Unreleased.
- [x] T3: Run `/milestone` in this repo twice as AC2 states, remove the temporary PROFILE line, compare with the `gh pr list` count, and run the verify slot.

## Work log

- 2026-10-22: created by /milestone-plan.
- 2026-10-22: tier check: not run — work named at the question set.
- 2026-10-22: idea vet: no concern. The report counts by head branch as the caps rule does, the operator asked for it after M315's review stopped at a cap, and the name says what it does.
- 2026-10-22: collision check: source is the candidate row "Report the open-PR caps in /milestone", absorbed in full. The parked row "Live-check the open hotfix PRs bullet" reads the same list; its scope (a live look with an open hotfix PR) stays distinct and is cross-referenced in Out. D-214 sets the caps; this adds a report and changes no cap rule.
- 2026-10-22: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn, so no overlap.
- 2026-10-22: lessons harvest: LESSONS M112 (grep README and docs for restatements; a user-visible change owes a CHANGELOG task) and M149 (rulebook-mass pins, avoided by leaving tracking-rules unchanged).
- 2026-10-22: criteria audit (full mode, fresh Opus reader): 2 findings on this milestone, both fixed. AC1 now reports an over-cap number as over the cap, not as at it. AC2 narrowed to what a run with 0 open PRs can show, plus one untaken cap line. AC3 and AC4 had no finding.
- 2026-10-22: plan gate chose a prose report in the skill over a script that runs `gh`, because the neighbor bullets are prose reads of the same list and a script would add a second read; falsified by a `/milestone` run whose reported numbers differ from the `gh pr list` count.
- 2026-10-22: implement started on branch m317-milestone-pr-caps, cut from main at fef549f2. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-22: T1 done: an "Open-PR caps" bullet after "Open hotfix PRs" in §2 of `skills/milestone/SKILL.md`, reusing its list; tracking-rules unchanged. T2 done: one sentence in README's audit paragraph and a CHANGELOG Unreleased New entry. The added lines pass the simple-english lint (checked on the added lines alone, with a control file that it flags).
- 2026-10-22: T3 live runs: two fresh Opus agents each followed the §2 "Open hotfix PRs" and "Open-PR caps" bullets as written, read-only, so the full `/milestone` skill and its chips did not start inside this run. Run 1 reported `bug-fix PRs: 0 of 3` and `feature PRs: 0 of 1` from one `gh pr list` call; my own `gh pr list --repo jmgirard/cairn --author @me --state open --limit 100 --json headRefName` gave 0 PRs, 0 `hotfix-`. Run 2, with a temporary `# Feature PR cap: 0` header line, reported the same numbers, named that line as not taken, and kept the feature cap at 1. The line was removed after run 2 and never committed. Both agents noted that the rulebook does not spell out how the `# Collaboration mode:` line is read (M315 wording, outside this scope) and that an empty list has no set wording.
- 2026-10-22: verify slot green: scripts 445 OK (21 skipped), hooks 202 OK, both validates exit 0, `claude plugin test` 2466 pass, 0 fail.
- 2026-10-22: claim audit: 20 claims read, 0 corrected — CHANGELOG.md, README.md, skills/milestone/SKILL.md
- 2026-10-22: minor amendment: the claim auditor found tracking-rules' `cairn/PROFILE.md` row listing the cap lines' readers without `/milestone`. Added it, so T1's "leave tracking-rules unchanged" no longer holds. The rulebook-mass seed moved to 820 lines / 80,301 bytes in its three pins (skills/milestone/SKILL.md, test_cost_audit_line.py, test_mutation_harness.py, per LESSONS M149). Scripts 445 OK, hooks 202 OK, skills/tests 958 OK after the change.
- 2026-10-22: substantive amendment: the line above was a scope change, not a minor one (diff-bug #1). Scope In now reads: "A cap report in §2 of `skills/milestone/SKILL.md`, built from the list that the "Open hotfix PRs" bullet already reads. README's paragraph on `/milestone`'s audit. CHANGELOG Unreleased. Naming `/milestone` among the cap lines' readers in tracking-rules (its `cairn/PROFILE.md` row and its open-PR caps bullet) and in `hooks/cairn_common.py`'s comment, with the rulebook-mass seed re-seeded in its three pins." T1's "Leave tracking-rules unchanged" clause is replaced to match. What the user sees is unchanged, so no stop.
- 2026-10-22: step-7 approval: m317-milestone-pr-caps approved for merge (PR #330)

## Decisions

## Review

- copilot: request on PR #330 exited 0, but the state query read `none` before and after; Copilot request on PR #330 may not be recorded by GitHub (used-up Copilot credits are one cause). No second request.
- AC1: the "Open-PR caps" bullet at `skills/milestone/SKILL.md:236` holds each of 15 clauses checked by `grep -F` on its whitespace-joined text (the hotfix bullet's list, no second `gh` call, `hotfix-` split, both caps, both cap lines, defaults 3 and 1, the rulebook citation, naming an untaken line, at and over the cap, the 100-PR case, a failed read, no GitHub write, no §3 disposition); the bullet holds no `gh` command.
- AC3: README.md:958-961, in the paragraph on `/milestone`'s health audit, says the audit reports open PRs against each cap (`hotfix-` beside the bug-fix cap, others beside the feature cap) and says when a count is at or over its cap. CHANGELOG.md:282, inside `## Unreleased` (before `## 2.1.0`), carries the New entry "`/milestone` reports your open PRs against the two caps".
- AC2: two fresh Opus agents each ran `/milestone` §1 and §2 read-only on this branch, after the edit was on disk (§3's chips not run). Run 1 reported "bug-fix PRs: 0 of 3; feature PRs: 1 of 1 (at the cap)" from the hotfix bullet's one `gh pr list` call, the open PR being #330; my `gh pr list --repo jmgirard/cairn --author @me --state open --limit 100 --json headRefName` counted 1 PR, 0 on `hotfix-` heads. Run 2, with a temporary `# Feature PR cap: 0` header line, reported the same numbers, named that line as not taken, and kept the feature cap at 1; the line put PROFILE.md at 120 lines, so its validate run read a `weight caps` FAIL, gone once the line was removed. The line was never committed.
- gate: `cairn_validate` all passed (exit 0); coverage complete; no principle changed, so `cairn_impact` skipped. Profile gate: verify green on the review head (code unchanged since 49766320), marketplace validate has no `plugins[N].version` warning, CHANGELOG Unreleased has the entry with no milestone ids. No CI on this repo.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: a scope change (tracking-rules row, two test pins) was logged as a minor amendment, with stale Scope In and T1 text — fix now, fixed 906c121a (substantive amendment line; Scope In and T1 updated)
- diff-bug #2: a stacked guest milestone's base PR makes the report read at or over the cap while that review can still open its PR — fix now, fixed 906c121a (one added line in guest mode with `# Push remote: base`)
- diff-bug #3: "report both caps as reached" at 100 PRs did not say how it combines with the numbers — fix now, fixed 906c121a (no number; says the list reached 100)
- diff-bug #4: unclear whether untaken cap lines are named after a failed list read — fix now, fixed 906c121a
- diff-bug #5: no set wording for an empty list — reject (false): the `0 of 3` / `0 of 1` form covers it, as the T3 runs showed
- diff-bug #6: the bullet dropped "header", and the rulebook never states how a header line is read — fix now for the word, fixed 906c121a; the parse rule, M315 wording outside this scope, is follow-up: candidate row "State how PROFILE header lines are read"
- diff-bug #7: `hooks/cairn_common.py:414-416` comment named only `/milestone-review` and `/hotfix` — fix now, fixed 906c121a
- diff-bug #8: the CHANGELOG entry asserts a behavior no test enforces — reject (planned change): the profile's test-doctrine slot says a new skill rule owes no prose guard (D-109)
- diff-bug #9: one bullet line runs past the wrap width — reject (style)
- blame-history #1: the audit counts a stacked base PR that D-214 and README leave out — fix now, fixed 906c121a (same fix as diff-bug #2; the rulebook limits the exclusion to the stacked milestone's own read)
- blame-history #2: the re-seed resets 14 bytes of reported growth and drops the M313 seed note — reject (false): the seed text allows a re-seed when a pass changes the file deliberately, and it names the prior seed, M315's
- prior-review #1: the report and the review gate count a stacked base PR differently — fix now, fixed 906c121a (same fix as diff-bug #2)
- prior-review #2: the rulebook's open-PR caps bullet did not name `/milestone` — fix now, fixed 906c121a; rulebook re-seeded to 821 lines / 80,381 bytes in its three pins
- prior-review #3: the new bullet has no prose guard, as Copilot asked on PR 326 — reject (planned change): D-108 and D-109 stand, as decided on PR 326
- ripple #1: tracking-rules:347-348 reader list omits `/milestone` — fix now, fixed 906c121a (same as prior-review #2)
- ripple #2: `hooks/session_context.py:308-309` names only the two gates — reject (false): that text says where the caps stop work, which stays true, and `/milestone` stops nothing
- ripple #3: `hooks/cairn_common.py:416` comment — fix now, fixed 906c121a (same as diff-bug #7)
- ripple #4: README and CHANGELOG cap entries list only the gates — reject (false): they describe the gates, which is still accurate
- AC1 re-check after 906c121a: the fixed bullet at `skills/milestone/SKILL.md:236` holds all 15 clauses by the same `grep -F` check (a planted absent phrase read MISSING, so the check can fail). The 100-PR clause now reads "the list reached 100, so both caps count as reached". AC2's runs predate the fix, which changed only the 100-PR, failed-read, and stacked-base wording, none of them on the runs' paths (0 or 1 open PRs, one untaken line).
- verify re-run on the fixed head: scripts 445 OK, hooks 202 OK, skills/tests 958 OK, both validates exit 0, `cairn_validate` passed, `claude plugin test` 2466 pass, 0 fail at dd31d961.
- conversation: PR #330 — empty read (no reviews, no conversation comments, no unresolved threads).
- copilot: Copilot review not present; the request on PR #330 may not be recorded by GitHub (used-up Copilot credits are one cause), and the state query before the merge question still read `none`.
- snapshot: none (no `_snaps` or `__snapshots__` path in the diff).
- ripple #5: ROADMAP row "Report the open-PR caps in /milestone" says `/milestone` reports nothing — reject (false): post-merge hygiene removes the graduated row
- AC4: verify slot at 69ef6cb4 (code as of 49766320), each exit code read: scripts 445 OK (21 skipped), hooks 202 OK, `claude plugin validate` plugin.json exit 0 and marketplace.json exit 0, `claude plugin test .` 2466 pass, 0 fail.
