# M225: The pane counts each handed-off PR's unanswered comments

- **Status:** planned
- **Priority:** normal
- **Depends on:** M224
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the cairn pane ships to every plugin user
- **Branch/PR:** —

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

- [ ] AC1: For each Blocked line whose M224 state read returned OPEN, the
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
- [ ] AC2: The unresolved count is the number of returned threads with
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
- [ ] AC3: Under a Blocked line with either count above zero, the pane
      draws a line with key `blocked-<id>-counts` at indent 4, reading
      `<t> unresolved threads · <c> unanswered`. A count of 1 reads
      `1 unresolved thread`, and a zero part is left out. There is no
      such line before the first GraphQL read, when both counts are zero,
      or after a GraphQL read fails. On a `Refresh`, the earlier counts stay
      drawn until the new read returns. `pane.test.tsx` cases cover both
      counts, each alone, both zero, the singular, and 3-digit counts in
      the 44-column width check.
- [ ] AC4: A GraphQL read fails when the call rejects, exits non-zero,
      prints text that is not JSON, or prints a reply that fails the shape
      check, including a null `pullRequest`, a null PR author, and a
      malformed node. Then no count line draws for that PR, its M224 state
      word and Button stay as they were, and the hook does not throw. One
      register test covers each case.
- [ ] AC5: In the desktop app's docked pane in the guest-mode insight
      checkout (`~/github/insight`), the operator compares a PR whose
      counts are not both zero with that PR's GitHub page and accepts the
      count line at the merge question.
- [ ] AC6: README's pane section, `cairn/DESIGN.md`'s pane text, and
      CHANGELOG.md's Unreleased section describe the two counts, the
      anchor rule, that bots count, the newest-100 limit, that one review
      can show in both counts, and when the counts are read. Each claim is
      read against the code at implement time.
- [ ] AC7: Every command in `cairn/PROFILE.md`'s `verify` slot exits 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T3
- AC4 → T1, T2, T3
- AC5 → T5
- AC6 → T4
- AC7 → T3, T4

## Tasks

- [ ] T1: Tests first. Add the counting function's cases on each AC2 axis,
      the AC1 query cases over two PR URLs, the AC3 layout cases, and the
      AC4 failure cases, with `process.run` answers per case. Extend M224's
      trigger tests to record GraphQL calls. Make sure that they fail
      against the M224 code.
- [ ] T2: Add the query and the shape check beside M224's read in
      `register.tsx`, and the counting function in `reader.ts` or its own
      module, with the counts in the M224 state atom under a moved shape
      tag (LESSONS M193, M210).
- [ ] T3: Draw the count line in `pane.ts` with the Box widths of LESSONS
      M194. Run `verify`.
- [ ] T4: Describe the counts in README.md's "The cairn pane", in
      `cairn/DESIGN.md`, and in CHANGELOG.md's Unreleased section. Run
      `verify`.
- [ ] T5: Live look in a new desktop Code session in `~/github/insight`
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

## Decisions

## Review
