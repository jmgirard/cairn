# M248: The plan offers to assign you to an issue it resolves, in place of a comment

**Status:** done (2026-10-12, PR #258 https://github.com/jmgirard/cairn/pull/258)

**Goal:** When a plan resolves a GitHub issue, the question set offers to assign the operator's own account to it, in both modes, and never offers a comment.

**Outcome:** `/milestone-plan` step 3's "Issue acknowledgement" paragraph
became "Issue assignment (one option)". The `Queued as` comment (owner
mode) and the `Working on this` comment (guest mode) are gone. The option
runs `gh issue edit <N> --add-assignee @me` (guest mode adds `--repo`)
only on selection, after step 4 and before step 6's commit. It is posed
only when `gh repo view --json viewerPermission` reads `ADMIN`, `MAINTAIN`,
`WRITE`, or `TRIAGE`. Otherwise one line, shown in question text or final
text and written to the work log, says the account cannot assign. The
description names current assignees from `gh issue view --json assignees`.
A failed or silently dropped assignment is reported with no other write.
README, CHANGELOG, and `test_issue_linkage.py` follow (`TestPlanGateAssignment`).

**Decisions:** one milestone-local entry: the reversal of M166's comment
and its guest-mode cost, at the user's choice.

**Review:** three lenses, 24 findings: 9 fixed, 1 follow-up (the fork
edge in "Intake and guest edges (M234 review)"), 8 rejected (5 planned
trade-offs), 6 noted. Copilot (Lite, earlier head): 3 items, 2 fixed, 1
rejected. Claim audit corrected 2 of 30 claims. Nothing retired.
