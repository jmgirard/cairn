# M262: A rerun of /hotfix on an open PR resumes the merge

**Status:** done (2026-10-16, PR #274 https://github.com/jmgirard/cairn/pull/274)

**Goal:** A `/hotfix` rerun with the PR reference of a hotfix PR that is still open goes back to where the earlier run stopped, in place of starting the adopt-a-PR walk.

**Outcome:** `/hotfix` step 6 notes the head the gate shows, and in owner mode writes the marker `hotfix <slug> approved YYYY-MM-DD for PR #<N> at <headRefOid>` after any push and create and before the CI wait; a head that moved by the marker write stops with no marker. Every owner merge runs `gh pr merge <N> --squash --delete-branch --match-head-commit <oid>`; a refused merge stops with no retry; a decline at the chip removes the PR's marker. Step 1 gains "Open-PR re-entry (M262)": owner arm, for an `OPEN` PR not on `m<nnn>-*` that a `hotfix ` marker names, resumes at the CI wait with no chip only when the marker's oid is the PR's `headRefOid`, `latestReviews` has no `CHANGES_REQUESTED`, and the row match equals the body's `Candidate row:` lines (reads `isCrossRepository` for a fork PR); otherwise the tier-check walk. Guest arm reports an open `hotfix-` PR's state and review decision and stops. README (pane paragraph, line 790), the `pane.ts` comment, and a CHANGELOG Fixes entry follow. `TestHotfixOpenPrReentry` (14 tests) and 24 mutation entries in `skills/tests`.

**Decisions:** D-168 (annotates D-130 and D-131). At the review stop the user chose the narrowed AC2 over re-posing the chip on every rerun.

**Review:** Two passes, one amendment return (AC2, after pass 1 found the first design re-posed the gate on untested commits, skipped the changes-requested check, and dropped promised row edits); the second AC2 re-audit went to the user. Scope Out amended for guest PRs with requested changes; AC1's proposed head sentence withdrawn and shipped as a fix. Claim audits: 28 claims (4 corrected), then 38 (4 corrected). Pass 2: 9 fixed, 4 to "Hotfix resume edges (M262 review)", 9 rejected. Copilot (Lite): 2 threads fixed, 1 rejected, all resolved. No lesson captured (D-168 and the skill own the approval-binding rule); nothing retired.
