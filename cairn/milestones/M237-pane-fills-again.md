# M237: The pane fills again after a resume or a hidden-tab clear, and reads each PR with one call

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane is part of the shipped status mod
- **Branch/PR:** m237-pane-fills-again https://github.com/jmgirard/cairn/pull/247

## Goal

The cairn pane fills its lines at each session start that empties the host's state. It shows ⋯ only during a read of its own, and it reads each github.com pull request with one `gh` call.

## Scope

**In:** In `register.tsx`, the `classic.SessionStart` hook also handles source `resume`. For both sources, it starts the pull request read for a placed pane, shown or not. The ↻ Button reads ⋯ only while the stored `reading` is true and a read from this module is in flight. `readPr` gets the word and thread count of a github.com URL from one `gh api graphql` call. A URL of another form keeps its one `gh pr view` call and gets no count. Update the code comments, README, DESIGN, and CHANGELOG.

**Out:** Source `fork`, which nobody looked at. A fork can also start with empty state, and that item goes to the merged "Pane edges" row. The reopen-mark edges, the rare-setup edges, and the code copies also stay in that row. The question set dropped the test-gap items. A timer or turn-end read stays out (M224, M230).

## Acceptance criteria

- [x] AC1: A `classic.SessionStart` whose source is `resume` reads the tracking files again, as one whose source is `clear` does. This holds at a process start and in a running process. `claude plugin test .` passes tests that fire each of the two sources twice. The first start has empty band and pane state. The second has band rows from the same root that differ from the fixture. Each test asserts the band rows and the pane lines that the fixture ROADMAP gives. Tests that fire `startup` and `compact` assert that the hook reads no file.
- [x] AC2: A `classic.SessionStart` whose source is `clear` or `resume` starts the pull request read for a pane that `$.ui.panes()` lists as placed. The pane can be shown or behind another tab. It starts none for a pane that is not listed or not placed, and none after `$.ui.panes()` throws. `claude plugin test .` passes ten tests over the `blocked-active` fixture, one for each of these five pane cases under each of the two sources. Each test asserts whether a `gh` call ran. The existing tests that assert no `gh` call for a placed pane behind another tab now assert the new behavior.
- [x] AC3: A pane drawn after a read settles shows ↻. A pane drawn during a read that the running module started shows ⋯. `claude plugin test .` passes three tests. In the first, a stored `reading` of true with no read started in the module draws ↻. In the second, a read with held answers draws ⋯ until it settles and ↻ after it. In the third, the write of `reading` false fails, and the next draw after the read settles shows ↻.
- [x] AC4: A github.com pull request URL gets its state word and its unresolved-thread count from one `gh api graphql` call. A hotfix URL on another host gets its word from one `gh pr view` call and no count. These are the words for the graphql reply. MERGED reads `merged`, and CLOSED reads `closed`. OPEN reads `changes requested` for CHANGES_REQUESTED and `approved` for APPROVED. OPEN reads `in review` for REVIEW_REQUIRED, a null decision, an absent decision, or another string. These replies read `unknown` with no count: a missing or unknown `state`, a null `pullRequest`, text that is not JSON, a non-zero exit, and a rejected call. Threads that are not a list, or a thread whose `isResolved` is not a boolean, leave the word and make the count null. A word other than the three open words carries no count. `claude plugin test .` passes tests that assert the argv of every call for each of the two URL forms. The tests also assert the word and the count for each reply in this list.
- [x] AC5: README's pane section, DESIGN.md's `hooks/status/` entry, and CHANGELOG.md's `## Unreleased` section state the resume read, the read behind another tab, and the one-call read. Each line that `git grep -n -e 'behind another tab' -e 'gh pr view' -e 'When the query fails' -e 'shown' -- README.md cairn/DESIGN.md` returns agrees with the new behavior.
- [x] AC6: The five `verify` commands in `cairn/PROFILE.md` exit 0 on the branch head.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5

## Tasks

- [x] T1: Session-start read (AC1, AC2). In `register.tsx:237-244`, handle `resume` beside `clear`. Start `readPrs` for a placed pane through a placed-only test beside `isShown` (`register.tsx:671`). Write the resume tests and the ten pane-case tests. Flip the tests near `pane.test.tsx:2738` that assert no read behind another tab.
- [x] T2: Reading label (AC3). Add a module-level count of reads in flight. `readPrs` raises it at its start and lowers it in its `finally`. The render shows ⋯ only for a stored `reading` of true and a count above 0. Rewrite the test at `pane.test.tsx:2554`, whose first assertion expects ⋯ for a stale stored true. Add the held-read and failed-write tests.
- [x] T3: One call (AC4). Add `state` and `reviewDecision` to the `counts.ts` query. Parse the word and the count from one reply, so a bad thread list leaves the word. `readPr` (`register.tsx:758`) runs the graphql call for a URL that `countsArgv` takes, and `gh pr view` alone for any other URL. Update `counts.test.ts` and the pane tests' `gh` fakes.
- [x] T4: Docs (AC5). Update the comments at `register.tsx:70-81`, `208-213`, `232-236`, and `686-703`, and the `counts.ts` header. Update README's pane section (near lines 340 and 365), DESIGN.md's `hooks/status/` entry (near lines 292 and 311-333), and CHANGELOG `## Unreleased`. Run the AC5 grep.
- [x] T5: Run the five `verify` commands (AC6).

## Work log

- 2026-10-10: created by /milestone-plan from the three "Pane edges" candidate rows (M222–M226, M230, and M236 reviews) at the user's `/milestone-plan pane edges`.
- 2026-10-10: question set: which edges. Answer: the visible fixes only (resume refill, hidden-tab read, stuck ⋯, one call per PR).
- 2026-10-10: question set: leftovers. Answer: merge the three rows into one, keep the behavior edges, and drop the test-gap items, since they never show in a real session.
- 2026-10-10: question set: live look. Answer: none, and the mod tests are the evidence.
- 2026-10-10: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-10: collision: this milestone absorbs five items of the three "Pane edges" rows. They are the `/resume` item, the hidden-tab `/clear` item, and the stored-true half of the reload item. The serial `gh pr view` then `gh api graphql` item and part of the hotfix-only wait are the others. The rest merges into one row. M230 and M236 (done) shipped the reads and the `reading` atom that this milestone changes. No D-entry collides.
- 2026-10-10: plan chose one graphql call per github.com URL over folding the word into the `gh pr list` call, because blocked rows have no list call. One path then serves both. Falsified by a session where a hotfix-only line still waits visibly on its own call after the list.
- 2026-10-10: plan chose an in-flight count beside the stored `reading` over resetting the stored value at load, because the API gives no load hook. A module variable resets at a reload. Falsified by a pane drawn after a reload that still shows ⋯ with no read running.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 13 findings, and the plan took all of them. AC1 drops "in-process", since the hook cannot tell the two resumes apart. AC1 also leaves `fork` unasserted (to the row) and adds a stale-rows case. AC2 runs ten cases on a named fixture, names the `$.ui.panes()` throw, and flips the old tests. AC3 narrows to a pane drawn after a read and adds the failed-write case. AC4 names the two URL forms and lists every reply. The plan then chose that a bad thread list leaves the word, as today. AC5 adds the sweep for contrary lines, and T4 adds the stale comments. The plan answered the finding that verify belongs among the done conditions: the template puts verify in a criterion.
- 2026-10-10: implement: branch m237-pane-fills-again cut from main at 345dc0d. The untracked `cairn-probe.log` and `tsconfig.json` are not the milestone's and stay unstaged.
- 2026-10-10: T1 done. `classic.SessionStart` reads on `clear` or `resume`, and `isPlaced` (new, beside `isShown`) gates the PR read. Sixteen new tests replace the old behind-a-tab quiet case, and the test fake's `ui.panes` can throw (`panesThrow`). Planting the old hook made five of them fail. Verify: five commands exit 0, 1575 mod tests.
- 2026-10-10: T2 done. A module-level `inFlight` count gates ⋯ in the render. The stale-store test now expects ↻, and a new test covers a lost write of false. The engine skips a `state.set` hook that throws and lets the write land, so the test hook writes true in place of the mod's false. Both tests failed before the fix (they drew ⋯). The held-read case is the existing M236 test at `pane.test.tsx:2435`. Verify: five commands exit 0, 1576 mod tests.
- 2026-10-10: T3 done. `prRead` in `counts.ts` reads the word and the count from one graphql reply. `wordOf` in `pane.ts` maps a state and a decision for both `prRead` and `prWord`. `readPr` keeps `gh pr view` only for a URL that `countsArgv` refuses. `prCounts` is gone. The pane tests' `gh` fake merges its `answer` and `graph` answers into one reply and records each read's URL in `reads`. Three fake-only count-failure cases were dropped, since a failed call now reads `unknown`, and `counts.test.ts` covers each reply that AC4 lists. A new test covers a hotfix URL on another host. Planting a `gh pr view` call before the graphql call failed 12 or more pane tests. Verify: five commands exit 0, 1590 mod tests.
- 2026-10-10: T4 done. Updated the `register.tsx` comments (the file header, `GH_TIMEOUT_MS`, the `classic.SessionStart` hook, `readPrs`, `readPr`, and the `reading` atom), README's pane section, DESIGN's `hooks/status/` entry, and four CHANGELOG `## Unreleased` entries. Three entries describe the unreleased pane features and were brought up to date in place, and one is new for the resume and hidden-tab reads. The AC5 sweep returned 14 lines. The 7 new or edited lines state the new behavior, and the other 7 are about the band example, the reopen, and a review chip, which this milestone does not change. Verify: five commands exit 0, 1590 mod tests.
- 2026-10-10: claim audit: 56 claims read, 3 corrected — CHANGELOG.md, README.md, hooks/status/counts.ts. "An open pane reads" became a placed or drawn pane, and the `prRead` comment no longer says it returns null. The reader also flagged the stale catch comment in `readPrs`'s `finally` (register.tsx). The same reader re-read the 4 fixes once: 3 held, and the catch comment took its suggested wording (an older read can keep `inFlight` above 0).
- 2026-10-10: T5 done. The five verify commands exit 0 on the corrected tree (1590 mod tests). Status set to `review`.
- 2026-10-10: step-7 approval: m237-pane-fills-again approved for merge

## Decisions

## Review

- Sync: `origin/main` is 345dc0d, an ancestor of the branch head, so no merge was needed. The Copilot arm pushed the branch, opened PR #247, ran the state query (`none`), and requested Copilot (exit 0).
- AC1: `claude plugin test .` on the review head (1590 pass, 0 fail). The 6 tests of "a resume start reads the files again, as a clear start does (M237 AC1)" pass. They cover `clear` and `resume` on empty state and on stale rows from the same root, each compared with a turn-end read, plus `startup` and `compact` with no file read. At T1 a planted `clear`-only hook failed both resume tests.
- AC2: same run. The 10 tests of "a clear or resume start reads the states for a placed pane (M237 AC2)" pass on `blocked-active`: placed and shown, placed and hidden (`gh` calls run), not listed, listed and not placed, and `ui.panes` throwing (no call), under each source. The old quiet test for a placed pane behind another tab is gone, and "a closed pane runs no gh call" remains. At T1 a planted `isShown` gate failed the hidden and resume cases.
- AC3: same run. "a stored reading state with no read in this module draws ↻ and lets a press read" passes, and its first assertion is ↻. The three "a held read reads ⋯ on the first line, and ↻ after it …" tests pass. "a failed write of the reading state false still draws ↻ once the read settles" passes. Before the T2 fix, the first and the last drew ⋯.
- AC4: same run. In `counts.test.ts`, the 17 tests of "prRead gives the word and the count of one graphql reply (M237 AC4)" pass. They cover the 7 state and decision pairs, an absent decision, the 6 `unknown` replies, and the 3 bad-thread replies that keep the word. In `pane.test.tsx`, the 3 tests of the M237 AC4 thread-shape group pass. "a hotfix on another host takes one gh pr view call and draws no count" asserts the exact `gh pr view` argv and one graphql call for the github.com URL. The M224 AC1 tests assert one graphql call and no `gh pr view` for a github.com URL. In all, 25 M224 AC1, M224 AC3, and M225 AC1 tests pass. At T3 a planted `gh pr view` call before the graphql call failed 12 or more of them.
- AC5: README's pane section states the resume read, the read for a drawn pane behind another tab, and the one graphql query. DESIGN's `hooks/status/` entry states all three (`isPlaced`, `readPr`, `prRead`). CHANGELOG `## Unreleased` has the new "fills again" entry, and the state, count, and ↻ entries were updated. The AC5 `git grep` returns 14 lines on the review head. The 7 new or edited lines state the new behavior. The other 7 are the band example (README:96), the reopen (README:399, 402, DESIGN:420, 431, 436), and a review chip and band row (README:686, DESIGN:574), and none of them contradicts the new behavior.
- AC6: on the review head, `python3 -m unittest discover -s scripts/tests` exits 0, as do `-s hooks/tests`, `claude plugin validate .claude-plugin/plugin.json`, and `claude plugin validate .claude-plugin/marketplace.json`. `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` exits 0 with 1590 pass and 0 fail.
- Consistency gate: `cairn_validate.py` prints "all checks passed". No DESIGN principle changed, so `cairn_impact` is skipped. The verify checks pass on the review head (AC6). The marketplace validate prints "Validation passed" with no `plugins[N].version` warning. CHANGELOG `## Unreleased` carries the changes, with no milestone numbers.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: a failed write of `reading` false leaves ⋯ on a pane already drawn, since a change to `inFlight` causes no redraw — fix now (`$.ui.invalidate('ui.render')` in that catch), fixed 314746b. The failed-write test now denies the write. With the redraw removed, a pane mounted through the read still read ↻ in the test harness, so no test covers the redraw.
- diff-bug #2: a resumed start in a folder marked for reopen reads the PRs twice, from the reopen and from the resume hook — follow-up, new row "Pane edges (M237 review)".
- diff-bug #3: the AC1 tests never fire `session.start` before the resume hook — fix now (a test of a resumed process start), fixed 314746b.
- diff-bug #4: a failed graphql call now loses the word, and the docs do not call it a change — reject, planned change: AC4 names a rejected call and a non-zero exit as `unknown`, and the PR-state feature is still under `## Unreleased`, so no released behavior changes.
- diff-bug #5: the claim that a reload ends the old module's reads is unverified — follow-up, already in "Pane edges (M222–M236 reviews)".
- diff-bug #6: a pane listed but not placed at a clear or resume reads nothing, so once placed it shows no words until an open or ↻ — follow-up, new row "Pane edges (M237 review)".
- diff-bug #7: the test fake's failing `graph` answer models only bad threads — reject, false: the fake's comment says so, and a failed call is modeled through `answer`. The missing `reviewDecision` key is covered by the absent-decision case in `counts.test.ts`.
- diff-bug #8: the AC2 positive cases do not check that the blocked URL was read — fix now (assert its graphql call and its word), fixed 314746b.
- diff-bug #9: README's "The state word and its Button stay" can be read with the failed-query sentence — fix now (reworded), fixed 314746b.
- diff-bug #10: `COUNTS_QUERY`, `countsArgv`, and `counts.ts` keep their names, and `prRead` looks up the pull request twice — reject, style.
- blame-history #1: a failure confined to the threads, which `gh api graphql` reports with a non-zero exit, now blanks the word that M225 kept — reject, planned change (AC4).
- blame-history #2: with `GH_HOST` set to another host, the graphql call for a github.com URL can go to that host and read `unknown` — fix now (`--hostname github.com` in the argv), fixed 314746b.
- blame-history #3: no captured `gh` reply carries `state` and `reviewDecision`, so a wrong field name would pass — fix now (replies captured from PR #246 and PR #247 with the new query, read by `prRead`), fixed 314746b.
- blame-history #4: the pane-level count-failure cases were removed, a merged PR now reads its threads, and the M230 quiet hidden-tab case was inverted — reject, planned change (AC2, AC4). `counts.test.ts` and the M224 AC4 pane tests cover the failure cases.
- blame-history #5: `inFlight` is module-local while `reading` is shared, so another host of the read would show ↻ — reject, false: one module serves the session's process, and the state is per session.
- blame-history #6: the double read at a resumed start — follow-up, the diff-bug #2 row.
- blame-history #7: no test lands a resume in another root — reject: the user dropped test-gap items at the question set, and `refresh`'s root handling is the M210 path that `clear` already takes.
- blame-history #8: docs drift, and the pane-shown check now at four sites — follow-up, new row "Pane edges (M237 review)". The AC5 sweep found no contrary line.
- prior-review #1: `isPlaced` adds a fourth spelling of the pane check that M230 asked to share — follow-up, new row "Pane edges (M237 review)".
- prior-review #2: the double read now also at a resume — follow-up, the diff-bug #2 row.
- prior-review #3: stale comments at `pane.ts` (`PrWord`, `OPEN_WORDS`) and `types/index.d.ts` (`CairnPrWord`) still name `gh pr view` — fix now, fixed 314746b.
- prior-review #4: long comment and prose lines — reject, style.
- prior-review #5: an old module's detached read can still write after a reload — follow-up, already in "Pane edges (M222–M236 reviews)".
- prior-review #6: no test of `inFlight` when two reads overlap — reject: the M236 overlap tests run through the counter, and the user dropped test-gap items.
- prior-review #7: a hotfix-only PR still waits for the list — follow-up, already in "Pane edges (M222–M236 reviews)".
- prior-review #8: a PR on another host gets no counts — reject, planned change (AC4).
- prior-review (unranked): DESIGN's `hooks/status/` history list does not name M237 — fix now, fixed 314746b.
- copilot: CHANGELOG.md:132 — fix now: the M230 entry for the in-process `/clear` still said a pane behind another tab waits for the next open, fixed 2ea874c (replied and resolved).
- copilot: review body — noted (one finding, the thread above, "Approval recommended").
- Copilot level: Lite (set by GitHub's settings). The review covered an earlier head (state `reviewed earlier-head Lite`).
- conversation: copilot-pull-request-reviewer[bot] PR — noted (the COMMENTED review whose body is the index above). No issue comments.
- Fix-now verify: the five verify commands exit 0 after 314746b (1592 mod tests). With the `inFlight` guard removed, the stale-store test and the deny-based failed-write test failed.
