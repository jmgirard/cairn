# M225: The pane counts each handed-off PR's unanswered comments

- **Status:** review
- **Priority:** normal
- **Depends on:** M224
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** m225-pane-pr-comments

## Goal

On request, each open handed-off PR in the cairn pane also shows its unresolved review threads and the reviews and comments from others that are newer than its author's last comment, review, or commit.

## Scope

**In:** For each Blocked line whose M224 state read returned OPEN, the
mod runs one read-only `gh api graphql` query through `$.process.run`, at
the same moments as M224's reads. The query names the owner, repo, and
number from the PR URL that M224 keeps for the line. A pure function turns
the reply into two counts, and the pane draws them on a line under the PR.
Bots count as others, Copilot's reviewer and CI bots alike. One Copilot
review can show in both counts: as an unanswered review and as its
unresolved threads. README, DESIGN, and CHANGELOG describe the counts and
their rule.

**Out:** Per-item reply tracking: the rule clears every earlier item when
the PR author comments, reviews, or pushes, because GitHub gives no reply
link for a review or a conversation comment. More than 100 of each kind:
the counts cover the newest 100, and a real PR past that becomes a
candidate row. Replying from the pane, and the band, which the plan gate
kept unchanged. M224's state words and Buttons are M224's.

## Acceptance criteria

- [x] AC1: For each Blocked line whose M224 state read returned OPEN, the
      mod runs one `gh api graphql` query through `$.process.run` for the
      PR's author login, `reviewThreads(last: 100)` with `isResolved`,
      `reviews(last: 100)` with author login, state, and `submittedAt`,
      `comments(last: 100)` with author login and `createdAt`, and
      `commits(last: 1)` with `committedDate`. It runs at the same moments
      as M224's reads and at no other. Register tests over two lines with
      different owners, repos, and numbers assert each query's owner, repo,
      and number. A merged, closed, or `unknown` line gets no query. M224's
      trigger and turn-complete tests also record no `gh api graphql` call
      outside a pane open or a `Refresh` press.
- [x] AC2: The unresolved count is the number of returned threads with
      `isResolved` false. The unanswered count is the number of returned
      submitted reviews in state COMMENTED or CHANGES_REQUESTED, plus
      returned conversation comments, whose author is not the PR author
      and whose time is strictly later than the anchor. A null author is
      another person. The anchor is the latest of the PR author's newest
      submitted review, the PR author's newest conversation comment, and
      the `committedDate` of `commits(last: 1)`. Times are ISO-8601 UTC
      strings compared as text. APPROVED, DISMISSED, and PENDING reviews,
      and a review whose `submittedAt` is null, never count and never set
      the anchor. A pure function computes both counts. Its tests vary
      each axis: kind (review, comment), author (PR author, human, bot,
      null), review state (all five), and time against the anchor (before,
      equal, after), with each of the three anchors the latest once.
- [x] AC3: Under a Blocked line with either count above zero, the pane
      draws a line with key `blocked-<id>-counts` at indent 4, reading
      `<t> unresolved threads · <c> unanswered`. A count of 1 reads
      `1 unresolved thread`, and a zero part is left out. There is no
      such line before the first GraphQL read, when both counts are zero,
      or after a GraphQL read fails. On a `Refresh`, the earlier counts stay
      drawn until the new read returns. `pane.test.tsx` cases cover both
      counts, each alone, both zero, the singular, and 3-digit counts in
      the 44-column width check.
- [x] AC4: A GraphQL read fails when the call rejects, exits non-zero,
      prints text that is not JSON, or prints a reply that fails the shape
      check, including a null `pullRequest`, a null PR author, and a
      malformed node. Then no count line draws for that PR, its M224 state
      word and Button stay as they were, and the hook does not throw. One
      register test covers each case.
- [ ] AC5: In the desktop app's docked pane in the guest-mode insight
      checkout (`~/github/insight`), the operator compares a PR whose
      counts are not both zero with that PR's GitHub page and accepts the
      count line at the merge question.
- [x] AC6: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the two counts, the
      anchor rule, that bots count, the newest-100 limit, that one review
      can show in both counts, and when the counts are read. Each claim is
      read against the code at implement time.
- [x] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T3
- AC4 → T1, T2, T3
- AC5 → T5
- AC6 → T4
- AC7 → T3, T4

## Tasks

- [x] T1: Tests first. Add the counting function's cases on each AC2 axis,
      the AC1 query cases over two PR URLs, the AC3 layout cases, and the
      AC4 failure cases, with `process.run` answers per case. Extend M224's
      trigger tests to record GraphQL calls. Make sure that they fail
      against the M224 code.
- [x] T2: Add the query and the shape check beside M224's read in
      `register.tsx`, and the counting function in `reader.ts` or its own
      module, with the counts in the M224 state atom under a moved shape
      tag (LESSONS M193, M210).
- [x] T3: Draw the count line in `pane.ts` with the Box widths of LESSONS
      M194. Run `verify`.
- [x] T4: Describe the counts in README.md's "The cairn pane", in
      `cairn/DESIGN.md`, and in CHANGELOG.md's Unreleased section. Run
      `verify`.
- [x] T5: Live look in a new desktop Code session in `~/github/insight`
      (LESSONS M195, M213). Pick a PR whose counts are not both zero and
      open its GitHub page beside the pane.

## Work log

- 2026-10-08: created by /milestone-plan, split from the M223 merge question. There the operator asked whether the pane reports open comments or Copilot reviews not yet answered, and chose to add those counts after M224.
- 2026-10-08: question set: add per-PR unresolved threads and unanswered comments — yes (the M223 merge question's second chip).
- 2026-10-08: question set: live look in the desktop app in `~/github/insight` — granted at the M223 plan question set for this feature's milestones, with read-only `gh` calls.
- 2026-10-08: plan split the counts into M225 over amending M224, because M224 with them would carry 8 criteria and pass the sizing tripwire. M224 keeps the state words and Buttons. M225 depends on M224 for the `$.process.run` probe and the PR state read.
- 2026-10-08: criteria audit (full mode, fresh Opus reader): 13 findings, all taken toward the narrower promise. Only OPEN PRs are read. The Goal names the anchor rule in place of "waits on a reply". Threads are read `last: 100`, and the limit is documented. A null author is another person, and a null PR author fails the read. The newest commit is `commits(last: 1)`, times compare strictly as text, and PENDING and DISMISSED are named. The AC2 tests vary every axis, and AC1 uses two URLs. AC3 names its key, indent, refresh, and width case. AC4 is a shape check. AC5 needs a PR with counts not both zero, compared with GitHub. The docs and verify are split, the trigger clause rides M224's tests, and the double count goes in the docs. M224's Out now points here.
- 2026-10-08: plan chose the anchor rule (others' items newer than the author's last comment, review, or commit) over per-item reply tracking, because GitHub links no reply to a review or a conversation comment. Falsified by a GitHub API field that links a comment to the item it answers.
- 2026-10-08: plan chose a second line under the PR over adding the counts to its tail, because the tail does not shrink and a 44-column pane has no room for both. Falsified by a live look where the second line crowds the section.
- 2026-10-09: implement started on `m225-pane-pr-comments`, cut from the pushed main at 4e840a3. The untracked `cairn-probe.log` and `tsconfig.json` stay unstaged, not milestone work. The simple-english lint hook flags existing text across ROADMAP.md and this file on each edit; the hits sit in history and plan-owned sections, so they stay as written.
- 2026-10-09: a read-only `gh api graphql` call on PR #231 returned `data.repository.pullRequest` with `author.login`, `reviewThreads.nodes`, `reviews.nodes`, `comments.nodes`, and `commits.nodes[].commit.committedDate`, the shape the shape check reads.
- 2026-10-09: implementation choice: the counting lives in its own module `hooks/status/counts.ts` (`countsArgv`, `prNodes`, `countPr`, `prCounts`). The argv passes owner and repo with `-f` and the number with `-F`, so an owner named like a number stays a string.
- 2026-10-09: T1 done: `counts.test.ts` covers the AC2 axes, the shape check, and the argv; `pane.test.tsx` adds the AC1, AC3, and AC4 register cases and records `gh api graphql` calls in M224's trigger tests, now over an OPEN PR. `counts.ts` was written in the same sitting; against the M224 register and pane code with `countPr` and `prCounts` stubbed to zero counts, `claude plugin test .` gave 68 fail, 1666 pass, every failure in an M225 case or an extended M224 trigger case.
- 2026-10-09: T2 done. `readPrs` runs the count query after a `gh pr view` whose word is open, with the same 15 s timeout. The `prs` atom holds `{ word, counts }` under the tag `prs-2`, and `CairnPrRead` joins the state contract. Words and counts are written once, after every call settles.
- 2026-10-09: T3 done. `paneLines` adds `blocked-<id>-counts` at indent 4, gray, with the count text in the line's text part, so a narrow pane cuts it. The Refresh test reads the held state from the terminal surface, because the desktop pane holds the press. All five verify commands exit 0, and the mod tests give 1734 pass.
- 2026-10-09: T4 done. README's pane section, DESIGN's `hooks/status/` text, and a CHANGELOG Unreleased entry describe the two counts, the anchor rule, that bots count, the newest-100 limit, the double count, and when the counts are read, each written against `counts.ts`, `pane.ts`, and `readPrs` as read this session. The added sentences pass the simple-english sentence and dash checks. All five verify commands exit 0, and `cairn_validate` passes.
- 2026-10-09: claim audit: 66 claims read, 5 corrected — CHANGELOG.md, README.md, hooks/status/counts.ts, hooks/status/counts.test.ts, hooks/status/pane.ts, hooks/status/pane.test.tsx, hooks/status/register.tsx, types/index.d.ts
- 2026-10-09: claim audit corrections. The docs said the author's commit or push sets the anchor, but the code uses the committed date of the PR's newest commit, whoever made it. README, CHANGELOG, DESIGN, `counts.ts`, the state contract, and a test comment now say so. CHANGELOG names the two counted review states. The no-commit test now asserts the counts, and the argv test checks the repo's flag. The same reader's one re-read is pending at this checkpoint. All five verify commands exit 0.
- 2026-10-09: claim audit re-read: the same reader found all five corrections hold. One README line was re-wrapped.
- 2026-10-09: T5 prep. Read-only `gh api graphql` on insight's open PRs gave both counts zero for PR 1250, M006's PR, because its newest commit (2026-10-09T02:45:56Z) follows the Copilot review and the maintainer's comments. PR 880 gives 1 unresolved and 2 unanswered, and PR 1252 gives 0 and 1. Insight M007 is `blocked` with no URL. The live look stops for the operator.
- 2026-10-09: question at the T5 stop: the operator chose PR 880 for the look. Insight M007's `Branch/PR` header now ends with `https://github.com/easystats/insight/pull/880`. The file is under insight's `.git/info/exclude`, so nothing reaches that repo. The header goes back to `export-table-tt-lists` after the look. Waiting on the operator's look in a new insight desktop session.
- 2026-10-09: T5 done. The operator resumed the run with `/milestone-implement M225` after the setup and did not report what the PR 880 line showed, so the merge question asks the operator to confirm it read `1 unresolved thread · 2 unanswered`. PR 880's GraphQL reply was unchanged at resume. Insight M007's header is back to `export-table-tt-lists`. All five verify commands exit 0. Status set to `review`.

## Decisions

## Review

Evidence gathered 2026-10-09 on 619b58e, main at 4e840a3 (not moved). `claude plugin test .`: 1734 pass, 0 fail.

- AC1: 7 `(M225 AC1)` tests pass. "two lines with different owners, repos, and numbers" records exactly two `gh api graphql` calls, alpha/one/12 and beta/two/90, each query naming the five field sets, and no call for the MERGED line. Merged, closed, and two unknown cases record no query. The 7 `(M224 AC3)` trigger tests, now over an OPEN PR, record one query per `/cairn-pane`, band open, session-start reopen, and `Refresh` press, and none at a close, a refused open, or two turn ends.
- AC2: 228 `(M225 AC2)` tests in `counts.test.ts` pass. For each of the three anchors (author review, author comment, commit) as the latest, they add one comment and one review in each of five states, by the PR author, a person, a bot login, and a null author, before, equal to, and after the anchor. Further cases cover a null `submittedAt`, the author's later APPROVED, DISMISSED, and PENDING reviews, each anchor clearing an earlier comment, a mixed PR worked by hand to 2 unresolved and 3 unanswered, and a 3-of-4 unresolved count.
- AC3: 8 `(M225 AC3)` tests in `pane.test.tsx` pass. The line keyed `blocked-M111-counts`, at indent 4 right after `blocked-M111`, reads `3 unresolved threads · 2 unanswered`, `2 unresolved threads`, `4 unanswered`, and `1 unresolved thread · 1 unanswered`; both zero draws none, and so does a turn end before any read. A held `Refresh` keeps `2 unresolved threads · 1 unanswered` until the query returns `5 unanswered`, and a later failed query removes the line. At 44 columns, `100 unresolved threads · 100 unanswered` plus its indent fits, and every line's lead and tail fit.
- AC4: 6 register tests in "a failed count read draws no count line and leaves the state word (M225 AC4)" pass: a rejected call, a non-zero exit, non-JSON text, a null `pullRequest`, a null PR author, and a malformed thread node. In each, `/cairn-pane` returns `cairn pane opened`, the line reads `… #1250  changes requested` with the `cairn-pane-revise-M111` Button, and no count line draws. 16 `prCounts` unit cases also fail the read on other bad shapes.
- AC5: the look used insight PR 880 through a temporary M007 header, since PR 1250's counts are both zero (work log, T5). A read-only query at resume gave PR 880 1 unresolved thread and 2 unanswered, so its line should read `1 unresolved thread · 2 unanswered`. The operator did not report what the pane showed. Acceptance is asked at the merge question, and this box waits for it.
- AC6: the branch adds to README's "The cairn pane", DESIGN's `hooks/status/` text, and CHANGELOG's Unreleased section text naming the two counts, the anchor (author's latest comment or review, and the PR's newest commit), that bots count, the newest-100 limit, that one Copilot review can show in both counts, and that the counts are read at a pane open and a `Refresh`. Claim audit: 66 claims read, 5 corrected, and the re-read found all five fixed (work log).
- AC7: all five `verify` commands exit 0: the two unittest suites (401 tests with 21 skipped, and 174), both `claude plugin validate` runs, and `claude plugin test .` (1734 pass).
- Consistency gate: `cairn_validate.py` all checks passed. No principle changed, so no `cairn_impact` run. The marketplace validate prints no `plugins[N].version` warning. CHANGELOG's Unreleased section has this milestone's entry with no milestone number.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: `committedDate` is a GitTimestamp that GitHub's schema says is not converted to UTC, so an offset time misorders against UTC review and comment times — fix now: `counts.ts` converts an offset commit time to UTC before the text compare, with a test (11:00+02:00 against a 10:30Z comment). Nine commit times read from insight PRs 734, 880, and 1123 all ended in `Z`.
- diff-bug #2: the anchor uses the newest commit's committed date, not its push time — follow-up to "Pane count edges (M225 review)". AC2 names `committedDate`, and README states the committed date is the time used.
- diff-bug #3: a bot or a reviewer's suggestion commit clears earlier items — follow-up to "Pane count edges (M225 review)". The rule is AC2's and the docs say the commit can be anyone's.
- diff-bug #4: fractional seconds would sort wrong as text — follow-up to "Pane count edges (M225 review)". No reply seen carries them, and a commit time with them now converts to whole seconds.
- diff-bug #5: threads the PR author opened count as unresolved — reject, planned change: AC2 counts every thread with `isResolved` false, and the docs say "review threads not marked resolved".
- diff-bug #6: the `GH_TIMEOUT_MS` comment named only `gh pr view` — fix now: it names both calls, what each timeout gives, and the doubled wait.
- diff-bug #7: an open PR's two calls run in turn, so a read can wait up to 30 s — follow-up to "Pane count edges (M225 review)".
- diff-bug #8: a PR whose author account is deleted shows no counts — reject, planned change: AC4 makes a null PR author fail the read.
- diff-bug #9: no test for an offset time, fractional seconds, or a non-author commit between reviews — offset part fixed now with diff-bug #1; the rest follow-up to "Pane count edges (M225 review)".
- blame-history #1: each line's word now waits on its count query — follow-up to "Pane count edges (M225 review)", with diff-bug #7.
- blame-history #2: M224's trigger tests moved from MERGED to OPEN — reject, false: `merged` and its Button stay covered by the M224 AC1 and AC2 tests, and the Refresh test still ends on `merged`.
- blame-history #3: no test that only the newest read writes — follow-up, already in "Pane PR-state edges (M224 review)" ("an older read that settles after a newer one").
- blame-history #4: DESIGN's M224 text said `readPrs` writes only the words — fix now: it says each word with its counts.
- blame-history #5: the M225 DESIGN text sits between the M224 text and the layout text — reject, false: the layout text already followed the M224 PR-read text on main, and the M225 text extends that read.
- blame-history #6: unwrapped README lines and a ragged CHANGELOG wrap — reject, style.
- prior-review #1: the open and reopen wait grows from 15 s to up to 30 s — follow-up to "Pane count edges (M225 review)", with diff-bug #7.
- prior-review #2: no test of an older read settling after a newer one — follow-up, already in "Pane PR-state edges (M224 review)".
- prior-review #3: no positive control that the clock recorder catches a clock call — follow-up, already in "Pane PR-state edges (M224 review)".
- prior-review #4: the counts shape was declared twice, and `OPEN_WORDS` is a third list of open words — fix now: `PrCounts` is the contract type, and a register test per open word checks that each gets a query.
- prior-review #5: line presses in flight or after a word change stay untested — follow-up, already in "Pane PR-state edges (M224 review)".
- prior-review #6: an in-process `/clear` now also drops the count line — follow-up, already in "Pane PR-state edges (M224 review)".
- prior-review #7: `counts.ts` keeps its own copy of the PR URL pattern — follow-up to "Pane count edges (M225 review)".
- Fix-now re-run: all five `verify` commands exit 0, and `claude plugin test .` gives 1739 pass.
