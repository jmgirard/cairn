# M230: The pane's PR reads stop holding up opens

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships in the plugin to every operator
- **Branch/PR:** m230-pane-reads-detached

## Goal

The cairn pane fills its pull request lines without holding up an open, fills them again after an in-process `/clear`, draws each pull request once, and keeps remote credentials out of its `gh` calls.

## Scope

**In:** four items from the "Pane edges (M222–M226 reviews)" candidate row. The three opens stop waiting for the `gh` reads, and the hotfix list read stops delaying the blocked rows' reads. A `/clear` that stays in the process reads the PR states again. A PR that is both a blocked row's and a hotfix PR draws once. The `gh pr list` call drops the userinfo of an http(s) remote URL. Comments, README, DESIGN, and CHANGELOG follow.

**Out:** the "Pane edges (M222–M226 reviews)" candidate row keeps the rest. That is the empty Hotfixes heading with a Refresh, the counts anchor rule, ssh host aliases, and non-github.com counts. It is also the reopen mark's edges, the type and URL-pattern copies, and the untested races.

## Acceptance criteria

- [x] AC1: `/cairn-pane`, the band's open Button, and the session-start reopen finish before the pull request reads settle. A `claude plugin test` case for each of the three holds every `gh` call pending. Each case shows the open finished before any `gh` call settles: the command's `cairn pane opened` line, the press handler's return, or the `session.start` handler's return. Each case then settles the calls and shows the blocked line's word drawn.
- [x] AC2: The blocked rows' `gh pr view` calls start before the `gh pr list` call settles. A test has one blocked PR URL and holds the `gh pr list` call pending. It records the blocked URL's `gh pr view` call before the list call settles.
- [x] AC3: When the pane is placed and shown, a `classic.SessionStart` with source `clear` reads the pull request words, counts, and hotfix list again. The hook returns before those reads settle. A test starts from empty `prs` and `hotfixes` state, raises that event with the `gh` calls held pending, and sees the hook return. It then settles the calls and shows the blocked line's word and the hotfix line drawn. Two more cases record no `gh` call from that event: one with the pane closed, one with it placed but not shown.
- [x] AC4: A hotfix pull request whose URL equals a blocked row's URL draws on the blocked line only, and the Hotfixes heading's count leaves it out. A test puts the same URL in both lists beside one other hotfix pull request. It shows that URL's word on the blocked line, no hotfix line for its number, and a heading count of 1. In a second case the shared pull request is the only hotfix, and the test shows no Hotfixes heading.
- [x] AC5: An http(s) base remote URL reaches `gh pr list` without its userinfo, and other URL forms reach it unchanged. Two tests use `https://user:token@github.com/o/r.git` and `https://token@github.com/o/r.git`. Each records the `--repo` value `https://github.com/o/r.git`, and no argv element they record contains `token`. A test with `git@github.com:o/r.git` records the `--repo` value `git@github.com:o/r.git`.
- [x] AC6: The five commands of the verify slot pass on the review head. `CHANGELOG.md` has an entry naming the changes of AC1 to AC5.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T5
- AC5 → T6
- AC6 → T7

## Tasks

- [x] T1: Extend the `gh(...)` test helper in `hooks/status/pane.test.tsx` so the `answer` and `list` callbacks can return a promise that the test settles. The `graph` callback already can (near L1892–1924). First, probe what `claude plugin test` does with detached `$` work still running at a test's end, and log the answer. Then move the existing `gh(...)` tests that assert right after an `await` to wait for the settled reads.
- [x] T2: In `hooks/status/register.tsx`, start `readPrs` without awaiting it in three places: the `/cairn-pane` command (near L238), `openPane` (near L634), and `reopen` (near L937). Rewrite the M224 and M222 comments that say the line comes once the reads finish. Add the AC1 tests.
- [x] T3: In `readPrs` (near L666), start the blocked URLs' reads without waiting for `readHotfixes`. Once the list settles, read the hotfix URLs that the blocked rows lack. Keep the newest-read check before each write, and keep the hotfix list written with the words. Rewrite the "Before them" comment. Add the AC2 test.
- [x] T4: In the `classic.SessionStart` hook (near L227), start `readPrs` after `refresh` without awaiting it. It starts only when `$.ui.panes()` shows the pane placed and shown. Rewrite the `readPrs` comment that says it runs only at an open and a Refresh press. Add the AC3 tests.
- [x] T5: In `paneLines` in `hooks/status/pane.ts` (near L421), drop each hotfix entry whose URL equals a blocked row's URL. Drop it before the heading count and the lines. Add the AC4 tests.
- [x] T6: In `baseRemoteUrl` (near L761), remove the userinfo from an `http://` or `https://` URL, and pass every other form unchanged. Add the AC5 tests.
- [x] T7: Update the README and the `cairn/DESIGN.md` paragraphs on when the pane reads pull requests (DESIGN near L288–355 and L397). Add the CHANGELOG entry, and run the verify slot.

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: collision check found no planned or in-progress milestone and no open GitHub issue or PR. D-143 (the mod gates this repo) is the only D-entry on the mod. The plan absorbs the five pane edge rows of the M222–M226 reviews. Records-hygiene §7 covers that group, and the user's request is its disposition.
- 2026-10-10: question set: how to combine the pane leftovers — fix four shared items in M230 and merge the rest into one candidate row.
- 2026-10-10: question set: which rows merge — the five pane edge rows, with the upstream, content, and band rows kept apart.
- 2026-10-10: question set: an empty Hotfixes heading with a Refresh — left out, and kept in the merged row.
- 2026-10-10: question set: a live look before the merge — declined, tests only.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 14 findings, all taken by narrowing. AC2 covers one direction. AC3 gained the hook-returns clause, the placed-and-shown predicate, and a not-shown case. AC4 matches an equal URL and states the heading count. AC5 covers http(s) userinfo, with `token@` and scp-form cases. The CHANGELOG clause names the AC list. The comment conflicts with M222, M224, and M226 went to T2–T4, and the test-helper cost went to T1.
- 2026-10-10: plan gate chose detached reads (`void readPrs($)`) over keeping the awaits with the list read beside the views, because the awaited form still holds an open for up to 30 s. Falsified by a probe showing that `claude plugin test` or the desktop app drops detached `$` work after a hook returns.
- 2026-10-10: plan gate kept the shared pull request on the blocked line, because only that line carries Finish, Revise, and Check. Falsified by a session where the operator looks for it under Hotfixes.
- 2026-10-10: AC5 stays a task in M230, not a `/hotfix`, because the token shows only in local process listings and the change is one function.
- 2026-10-10: the question set cut the empty-heading criterion, which also drops its state-shape change. The merged row holds it.
- 2026-10-10: implement started on branch `m230-pane-reads-detached`. The untracked `cairn-probe.log` and `tsconfig.json` in the working tree are not this milestone's and stay unstaged.
- 2026-10-10: T1 probe: detached `$` work runs on after a hook returns under `claude plugin test`, as the M221 detached runs already showed, and the 12 new cases end with their held calls released. The `gh(...)` helper takes held `answer` and `list` promises and gives `settled()`, which waits until no `git` or `gh` call is in flight for 20 ms. The drawing helpers `blockedView` and `linesAt` wait on it, and 14 cases that assert calls right after an open wait on it too.
- 2026-10-10: T2–T6 done in one checkpoint, because the six tasks share two files and one test block. `readPrs` moved its per-URL body to `readPr`, and `isShown` gives the placed-and-shown check. The Refresh press still waits for its read, since AC1 names only the three opens.
- 2026-10-10: plant check in scratch copies: each of 8 reversals turned its own M230 test red. The reversals are an await in each of the three opens, the serial list read, no read at a clear, a read at any pane, no hotfix filter, and kept userinfo. Mod tests: 1777 pass. The verify slot's five commands pass.
- 2026-10-10: T7 done: README, DESIGN, and four CHANGELOG Fixes entries describe the four changes. The CHANGELOG states the old wait as calls in turn with a 15 s timeout each, not a total, under the derived-figures rule. The verify slot's five commands pass, with 1777 mod tests.
- 2026-10-10: claim audit: 38 claims read, 8 corrected — CHANGELOG.md, README.md, hooks/status/pane.ts, hooks/status/pane.test.tsx. The main fix: words and counts appear together when the last read settles, not one at a time. The same reader re-read the 8 once and found none still wrong, and its optional "or times out" wording went into the README.
- 2026-10-10: implement done. All 7 tasks are checked, and the verify slot's five commands pass with 1777 mod tests. Status set to review.

## Decisions

## Review

Review head a8ca27e, 2026-10-10. Main had not moved since the branch was cut. `claude plugin test .` gave 1777 pass and 0 fail.

- AC1 evidence: the three "an open finishes before the pull request reads settle (M230 AC1)" cases pass: `/cairn-pane`, the band's open Button press, and the session-start reopen. Each holds every `gh` answer behind one gate and finishes within its 300 ms race. Each then releases the gate and reads `M111  Handed to the maintainers  #1250  in review`. At implement, an `await readPrs` planted in each open turned only that open's case red.
- AC2 evidence: "the blocked URL's gh pr view runs while gh pr list is held" passes. With the list call recorded and not settled, the recorded view calls equal `gh pr view https://github.com/upstream/repo/pull/1250 --json state,reviewDecision`. After release, the hotfix URL 1265 is read second. At implement, the serial order planted back turned it red.
- AC3 evidence: the three "a /clear in the same process reads the states again while the pane shows (M230 AC3)" cases pass. Each starts with the pane listed and no word or hotfix line drawn. The shown pane's `classic.SessionStart` with source `clear` finishes within 300 ms with every `gh` answer held. After release, it draws `M111 … #1250  in review` and `#1265  Fix 1265  in review`. The closed pane and the pane behind another tab record no view, list, or graphql call. At implement, three plants turned these cases red: no read, a read at any pane, and an awaited read.
- AC4 evidence: both "a hotfix whose URL is a blocked row's draws on the blocked line only (M230 AC4)" cases pass. With the shared PR 1250 beside 1265, the blocked line reads `… #1250  in review`. The hotfix keys are `hotfixes-head-gap`, `hotfixes-head`, and `hotfix-1265`, with no `hotfix-1250`. The heading reads `▎ HOTFIXES 1`, and URL 1250 is viewed once. With 1250 the only hotfix, no hotfix key draws. Removing the filter turned both red.
- AC5 evidence: the three "the gh pr list call names an http(s) remote without its userinfo (M230 AC5)" cases pass. `https://user:token@github.com/o/r.git` and `https://token@github.com/o/r.git` each record the list call with `--repo https://github.com/o/r.git`, and no recorded argv element contains `token`. `git@github.com:o/r.git` records `--repo git@github.com:o/r.git`. With the userinfo kept, the two credential cases turned red.
- AC6 evidence: on a8ca27e the five verify commands exit 0. Those are the `scripts/tests` and `hooks/tests` unittest suites, the two `claude plugin validate` calls, and `claude plugin test .` with 1777 pass. `CHANGELOG.md` Unreleased › Fixes has four entries, one per change of AC1 to AC5. They cover the opens and the read order (AC1, AC2), the refill after a Button's `/clear` (AC3), the shared PR shown once (AC4), and no remote credentials (AC5).
- Consistency gate: `cairn_validate` exits 0, with every check PASS or OK, `coverage complete` among them. No principle changed, so `cairn_impact` was skipped. The profile's checks: verify passes on a8ca27e. The marketplace validate output has no `plugins[N].version` warning. The CHANGELOG has entries for the user-visible changes, and its added lines carry no milestone id.
