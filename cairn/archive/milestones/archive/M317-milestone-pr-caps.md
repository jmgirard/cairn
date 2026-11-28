# M317: Report the open-PR caps in /milestone

**Status:** done (2026-10-22, PR #330 https://github.com/jmgirard/cairn/pull/330)

**Goal:** `/milestone`'s status report shows how many of your open PRs count against each open-PR cap, beside the cap.

**Outcome:** An "Open-PR caps" bullet in §2 of `skills/milestone/SKILL.md` counts the "Open hotfix PRs" bullet's list, with no second `gh` call: `hotfix-` heads beside the bug-fix cap, the rest beside the feature cap, caps from the `cairn/PROFILE.md` header lines (else 3 and 1). It reports at or over the cap, no numbers at a 100-PR list or a failed read, names an untaken cap line, and in guest mode with `# Push remote: base` notes that a stacked review leaves its stack base's PR out. It writes nothing to GitHub and stops nothing. tracking-rules (the `cairn/PROFILE.md` row and the open-PR caps bullet) and the `hooks/cairn_common.py` comment name `/milestone` as a reader; the rulebook-mass seed moved to 821 lines / 80,381 bytes in its three pins. README's audit paragraph and a CHANGELOG Unreleased New entry describe the report.

**Decisions:** none promoted. The plan gate chose a prose report over a script that runs `gh`.

**Review:** Criteria audit at plan (full, 2 findings, both taken). Claim audit: 20 claims, 0 corrected. One substantive amendment (scope: the rulebook rows and pins). Live checks: two fresh-agent `/milestone` §1–§2 runs (0 of 3, 1 of 1 at the cap; an untaken `# Feature PR cap: 0` line named). Four reviewers gave 19 findings: 11 fixed, 1 follow-up (candidate row "State how PROFILE header lines are read"), 8 rejected (none as `edge`). Copilot: no review recorded on PR #330. Hygiene: the "Report the open-PR caps in /milestone" row graduated; the M315 row pruned to the terminal cap. No lesson added (LESSONS at its byte cap), and no row unparked.
