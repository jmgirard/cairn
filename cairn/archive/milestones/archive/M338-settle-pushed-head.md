# M338: Note the pushed head after a merge push

**Status:** done (2026-11-06, PR #353 https://github.com/jmgirard/cairn/pull/353)

**Goal:** In owner mode, after a merge push, `/milestone-review` and `/hotfix` wait until GitHub reports the pushed commit as the PR head before they write the approval marker or read the PR's checks.

**Outcome:** `skills/milestone-review/SKILL.md` step 8 gains "Settle the pushed head". After every owner-mode push of the step (a new PR, an existing one, a Red CI rerun), it reads `git rev-parse origin/<branch>`, not local `HEAD`. A spelled one-call loop then re-reads `headRefOid` up to 12 times, 5 s apart, before the marker write and the first `gh pr checks` read. A mismatch writes no marker, arms no watch, and stops naming both commits. A rejected or failed push is never forced and stops. The companion arm settles each companion's head inside `cd <abs-path> && { … }` before its wait. `skills/hotfix/SKILL.md` step 6 runs the same loop for an authored fix against the gate's head and keeps one read for an adopted PR. Its stop names the PR head read and the gate's head. The rulebook's merge CI wait step (a) and its recorded-head clause say so, and so does a CHANGELOG entry. The rulebook baseline is re-seeded to 898 lines / 89,181 bytes.

**Decisions:** D-246 (supersedes D-232's head-read clause), D-247 (corrects D-246's reach and its lag claim; the rejected-push stop). Rejected in the work log: recording the local pushed commit with no PR read.

**Review:** Criteria audit at plan (full, 8 findings, all taken); claim audit 34 claims, 5 corrected. Pass 1, four lenses plus Copilot: 31 items, 11 fixed, 2 to a row, 18 rejected (1 `edge`: a second pusher on the milestone branch). Copilot: one review at Lite; one comment posted, thread resolved, body note rejected. New row: "Settle a hotfix gate head after a push" (normal). Hygiene: graduated "Note the pushed head after a merge push"; M335 row pruned; `used M338` on nine lessons; the 2026-11-05 (M336) lesson trimmed of its `gh pr view` sentence, which step 8 and hotfix step 6 now own; no lesson captured.
