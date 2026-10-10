# M230: The pane's PR reads stop holding up opens

- **Status:** in-progress
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

- [ ] AC1: `/cairn-pane`, the band's open Button, and the session-start reopen finish before the pull request reads settle. A `claude plugin test` case for each of the three holds every `gh` call pending. Each case shows the open finished before any `gh` call settles: the command's `cairn pane opened` line, the press handler's return, or the `session.start` handler's return. Each case then settles the calls and shows the blocked line's word drawn.
- [ ] AC2: The blocked rows' `gh pr view` calls start before the `gh pr list` call settles. A test has one blocked PR URL and holds the `gh pr list` call pending. It records the blocked URL's `gh pr view` call before the list call settles.
- [ ] AC3: When the pane is placed and shown, a `classic.SessionStart` with source `clear` reads the pull request words, counts, and hotfix list again. The hook returns before those reads settle. A test starts from empty `prs` and `hotfixes` state, raises that event with the `gh` calls held pending, and sees the hook return. It then settles the calls and shows the blocked line's word and the hotfix line drawn. Two more cases record no `gh` call from that event: one with the pane closed, one with it placed but not shown.
- [ ] AC4: A hotfix pull request whose URL equals a blocked row's URL draws on the blocked line only, and the Hotfixes heading's count leaves it out. A test puts the same URL in both lists beside one other hotfix pull request. It shows that URL's word on the blocked line, no hotfix line for its number, and a heading count of 1. In a second case the shared pull request is the only hotfix, and the test shows no Hotfixes heading.
- [ ] AC5: An http(s) base remote URL reaches `gh pr list` without its userinfo, and other URL forms reach it unchanged. Two tests use `https://user:token@github.com/o/r.git` and `https://token@github.com/o/r.git`. Each records the `--repo` value `https://github.com/o/r.git`, and no argv element they record contains `token`. A test with `git@github.com:o/r.git` records the `--repo` value `git@github.com:o/r.git`.
- [ ] AC6: The five commands of the verify slot pass on the review head. `CHANGELOG.md` has an entry naming the changes of AC1 to AC5.

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

## Decisions

## Review
