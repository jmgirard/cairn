# M249: A hotfix removes the candidate row it fixes, once the fix merges

**Status:** done (2026-10-12, PR #259 https://github.com/jmgirard/cairn/pull/259)

**Goal:** When a hotfix fixes the bug that a ROADMAP candidate row describes, the hotfix removes that row, or narrows it to the part left, once the fix merges.

**Outcome:** `/hotfix` step 1 gained a "Candidate-row match" paragraph: on
every entry, before any stop and never from memory, it matches rows by a
quoted title (text up to the first `: `, or all of it) or by description,
reads a PR's title, body and `Fixes #N` line, names each match in chat,
and skips a row a live milestone file quotes. The step 6 approval chip and
the "Nothing owed" chip (both modes) name each row and remove-or-narrow.
Step 7's "Matched candidate rows" paragraph deletes a fully covered row or
narrows it with a `narrowed YYYY-MM-DD by the PR #N hotfix` note after a
merge that passed the bar, and lands every step-7 ROADMAP edit in one
docs-only commit on the default branch after a `git status` check, with a
verbatim preview. Guest mode edits on disk at the merged re-entry. Also
records-hygiene §1, README, CHANGELOG, `test_hotfix_candidate_graduation.py`.

**Decisions:** none (plan gate: post-merge commit, not in-PR; guest edit at the merged re-entry).

**Review:** two defect returns (a missing CHANGELOG entry; the guest
"Nothing owed" chip named no rows, against AC2). Two three-lens passes plus
Copilot (Lite): 23 fixed, 6 to the new row "Hotfix row-graduation edges
(M249 review)", 9 rejected, 10 noted. Claim audit: 2 of 29 claims corrected. M112 lesson extended.
