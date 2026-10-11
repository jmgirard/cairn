# M237: The pane fills again after a resume or a hidden-tab clear, and reads each PR with one call

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane is part of the shipped status mod
- **Branch/PR:** m237-pane-fills-again

## Goal

The cairn pane fills its lines at each session start that empties the host's state. It shows ⋯ only during a read of its own, and it reads each github.com pull request with one `gh` call.

## Scope

**In:** In `register.tsx`, the `classic.SessionStart` hook also handles source `resume`. For both sources, it starts the pull request read for a placed pane, shown or not. The ↻ Button reads ⋯ only while the stored `reading` is true and a read from this module is in flight. `readPr` gets the word and thread count of a github.com URL from one `gh api graphql` call. A URL of another form keeps its one `gh pr view` call and gets no count. Update the code comments, README, DESIGN, and CHANGELOG.

**Out:** Source `fork`, which nobody looked at. A fork can also start with empty state, and that item goes to the merged "Pane edges" row. The reopen-mark edges, the rare-setup edges, and the code copies also stay in that row. The question set dropped the test-gap items. A timer or turn-end read stays out (M224, M230).

## Acceptance criteria

- [ ] AC1: A `classic.SessionStart` whose source is `resume` reads the tracking files again, as one whose source is `clear` does. This holds at a process start and in a running process. `claude plugin test .` passes tests that fire each of the two sources twice. The first start has empty band and pane state. The second has band rows from the same root that differ from the fixture. Each test asserts the band rows and the pane lines that the fixture ROADMAP gives. Tests that fire `startup` and `compact` assert that the hook reads no file.
- [ ] AC2: A `classic.SessionStart` whose source is `clear` or `resume` starts the pull request read for a pane that `$.ui.panes()` lists as placed. The pane can be shown or behind another tab. It starts none for a pane that is not listed or not placed, and none after `$.ui.panes()` throws. `claude plugin test .` passes ten tests over the `blocked-active` fixture, one for each of these five pane cases under each of the two sources. Each test asserts whether a `gh` call ran. The existing tests that assert no `gh` call for a placed pane behind another tab now assert the new behavior.
- [ ] AC3: A pane drawn after a read settles shows ↻. A pane drawn during a read that the running module started shows ⋯. `claude plugin test .` passes three tests. In the first, a stored `reading` of true with no read started in the module draws ↻. In the second, a read with held answers draws ⋯ until it settles and ↻ after it. In the third, the write of `reading` false fails, and the next draw after the read settles shows ↻.
- [ ] AC4: A github.com pull request URL gets its state word and its unresolved-thread count from one `gh api graphql` call. A hotfix URL on another host gets its word from one `gh pr view` call and no count. These are the words for the graphql reply. MERGED reads `merged`, and CLOSED reads `closed`. OPEN reads `changes requested` for CHANGES_REQUESTED and `approved` for APPROVED. OPEN reads `in review` for REVIEW_REQUIRED, a null decision, an absent decision, or another string. These replies read `unknown` with no count: a missing or unknown `state`, a null `pullRequest`, text that is not JSON, a non-zero exit, and a rejected call. Threads that are not a list, or a thread whose `isResolved` is not a boolean, leave the word and make the count null. A word other than the three open words carries no count. `claude plugin test .` passes tests that assert the argv of every call for each of the two URL forms. The tests also assert the word and the count for each reply in this list.
- [ ] AC5: README's pane section, DESIGN.md's `hooks/status/` entry, and CHANGELOG.md's `## Unreleased` section state the resume read, the read behind another tab, and the one-call read. Each line that `git grep -n -e 'behind another tab' -e 'gh pr view' -e 'When the query fails' -e 'shown' -- README.md cairn/DESIGN.md` returns agrees with the new behavior.
- [ ] AC6: The five `verify` commands in `cairn/PROFILE.md` exit 0 on the branch head.

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
- [ ] T3: One call (AC4). Add `state` and `reviewDecision` to the `counts.ts` query. Parse the word and the count from one reply, so a bad thread list leaves the word. `readPr` (`register.tsx:758`) runs the graphql call for a URL that `countsArgv` takes, and `gh pr view` alone for any other URL. Update `counts.test.ts` and the pane tests' `gh` fakes.
- [ ] T4: Docs (AC5). Update the comments at `register.tsx:70-81`, `208-213`, `232-236`, and `686-703`, and the `counts.ts` header. Update README's pane section (near lines 340 and 365), DESIGN.md's `hooks/status/` entry (near lines 292 and 311-333), and CHANGELOG `## Unreleased`. Run the AC5 grep.
- [ ] T5: Run the five `verify` commands (AC6).

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

## Decisions

## Review
