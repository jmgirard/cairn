# M235: `/cairn-triage` runs in guest mode and writes its edits to disk

**Status:** done (2026-10-10, PR #244 https://github.com/jmgirard/cairn/pull/244)

**Goal:** In a guest-mode repo, `/cairn-triage` runs its whole pass over the local `cairn/` files and ends with the accepted edits on disk, never committed or pushed.

**Outcome:** The skill's guest stop became a "Guest mode runs on disk" arm. It skips the clean-tree, default-branch, and sync preconditions, and runs steps 1–4 as written and step 5 with the stamp in place of the commit message. Step 2 checks a cited code path with `git cat-file -e <base>/<default-branch>:<path>`, judges fired triggers and already-shipped drops at that ref, and needs a shipped drop's commit to be reachable from it. Step 3 names that ref above the table. Step 4's byte check counts the longer guest stamp. Step 6's guest arm validates and stamps, the stamp names each refuted-premise or already-shipped drop's evidence, and it makes no commit and no push. Step 7 reports `written to disk, not committed (guest mode)` and a matching safety line. The rulebook's guest bullet now stops `/cairn-release` alone and states the triage arm and its longer, short-lived stamp. README's guest section and table row, the CHANGELOG, and the `/milestone` rulebook-mass baseline (638 lines / 60,962 bytes) follow. New guard `test_guest_triage.py` (7 tests, 8 mutation entries).

**Decisions:** D-156: in guest mode `/cairn-triage` runs and leaves its edits on disk, uncommitted. It annotates D-137.

**Review:** Full criteria audit (5 findings, all narrowed) and claim audit (26 claims, 4 corrected). Three-lens fan-out with no return. Of 19 findings, 9 were fixed, 2 went to the new row "Guest triage drop evidence outlives one stamp", 7 were rejected, and 1 was noted. The main fix: guest path and shipped checks read the base default branch, not the operator's branch. Copilot (Lite) drew 2 threads and 2 body items: the stale rulebook-mass baseline was fixed, the PR-URL thread was rejected (already recorded), both threads were replied to and resolved. Nothing graduated or retired.
