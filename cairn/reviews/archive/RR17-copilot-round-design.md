# RR17: The Copilot review round's design (M231)

- **Date:** 2026-10-10
- **Brief:** `cairn/reviews/RB17-copilot-round-design.md`
- **Branch read:** `m231-copilot-review-round` (working tree, ref-based git only)
- **Status:** advisory, no binding criteria

## Summary

The round fails at its edges because it tries to know whether "the round
ran". The PR cannot tell it that. The PR can tell it three other things,
each tested below on live PRs. One: whether a Copilot review is pending.
Two: which head each Copilot review covered. Three: whether each thread is
resolved. Those three signals answer request, wait, and read per item, with
no record of a round anywhere.

Put the request at the start of `/milestone-review`, so Copilot works while
cairn runs its own checks. Handle Copilot's threads inside the step-7
PR-conversation read, which already exists. Add reply and resolve as the
two actions that read takes on a Copilot thread. The separate round step,
its three-word state machine, and the 20-minute background loop go away.
Hotfix and guest keep a short serial wait, because their PR cannot open
earlier.

## Evidence

Read-only `gh api` queries on easystats/insight PRs 1252 to 1259 and on
jmgirard/cairn PR 239.

E1. `PullRequestReview.commit{oid}` is the head the review covered. Every
Copilot review on the seven insight PRs carries it. So does every
empty-body reply review by the operator. Example, PR 1253: the Copilot
review is on `f726b87`, the operator's two replies are on `b36b64f`, and
`headRefOid` is `6e9b5c8`.

E2. `PullRequest.reviewRequests` lists pending requests. It is empty once
Copilot's review is submitted, and the timeline shows no
`ReviewRequestRemovedEvent`. PR 1259: `ReviewRequestedEvent` at 14:49:47,
Copilot review at 14:52:44, `reviewRequests` now `[]`, no removal event.

E3. Copilot's review body states its level. All seven bodies carry
`🧠 **Review effort:** Lite` or `Balanced`. The module's report line "set
by GitHub's settings (asked for …)" (`skills/shared/copilot-review.md:28`)
can state the real level instead.

E4. Every body finding on the seven PRs links to a thread by
`#discussion_r<fullDatabaseId>`. PRs 1253 and 1254 use an anchor, PRs 1255
to 1257 a full URL. The ids match the review's `comments` connection. A "0
open findings" body has no finding lines (PRs 1252, 1258, 1259). No
body-only finding was observed. The body is an index of the threads, not a
second list.

E5. Latency from request to review: 2, 3, 4, 8, 8, 17, and 20 minutes. PR
1256 was requested at 03:52:09 and reviewed at 04:11:45. Lite is not faster
than Balanced in this sample. PRs 1256 and 1257, both Lite, took 20 and 17
minutes. The module's 20-minute bound misses PR 1256 by 24 seconds.

E6. A failing state query exits 1 and prints the raw error JSON to stdout.
Tested with a nonexistent PR number. The `--jq` filter never runs, so none
of `none`, `waiting`, or `arrived` appears. The module's three-way branch at
`copilot-review.md:52–60` has no arm for that. Pass 3's diff-bug #3 said
the same.

E7. `gh pr edit --help` (gh 2.102.0, line 41) documents `--add-reviewer` as
"Add or re-request reviewers". A second request on a reviewed PR starts a
second review and spends credits. A guard against a second request is
needed. The module's guard (`copilot-review.md:30–34`) has the right intent
and the wrong signal.

E8. A replacement state query ran on five PRs. It prints one of `pending`,
`reviewed head <level>`, `reviewed earlier-head <level>`, or `none`, with
exit 0. On a bad PR it exits 1. Results: PR 1259 `reviewed head Lite`, PRs
1258 and 1253 `reviewed earlier-head`, PR 1252 `reviewed head Balanced`,
cairn PR 239 `none`. The query is under question 1.

## Answers

### 1. Detection without state

The PR carries three signals. Each is stable across manual requests,
automatic reviews on open or on push, declines, and returns.

- **S1 pending**: `reviewRequests` contains `copilot-pull-request-reviewer`
  (E2). It is true from the request until the review is submitted. An
  automatic review's own request sets it too.
- **S2 reviewed**: a review by that login exists. Its `commit.oid` says
  which head it covered (E1). Who requested it (cairn, the user, or a
  repository setting) does not matter. It also cannot be told apart
  reliably, so the design must not depend on that.
- **S3 handled, per thread**: `isResolved`. A resolved thread was handled
  by whoever resolved it. An unresolved thread whose first comment is
  Copilot's is an open item. That holds whether nobody read it or a prior
  pass replied without a resolve. The existing step-7 read already filters
  on this field (`skills/milestone-review/SKILL.md:462–466`).

The PR cannot tell whether a given round ran. The module's current signal
is the newest `ReviewRequestedEvent` timestamp against each review's
`submittedAt` (`copilot-review.md:49`). That is a proxy for "our request",
and each pass broke the proxy. An automatic review's request is not ours
(pass 3 #1). A prior pass's request looks like ours (pass 2 #2). A failed
query looks like nothing (E6). The fix is to stop asking the question.
Nothing in the flow needs to know that a round ran. The flow needs three
answers. When S1 and S2 are both false, request. When S1 is true, wait.
S3 lists the open items. "This round already handled these items" and
"nobody has read them yet" are the same per-item fact, S3, and the resolve
is what writes it. That is why the resolve carries the design and stays
(question 7).

One residue has no key: a body finding with no thread. None was observed
(E4). If one appears, a later pass re-disposes it, at the cost of one chat
line. Accept that cost rather than add a record.

The decision procedure, one query, exit code first:

```
exit != 0            -> state the error in one line, request nothing, run the read
pending              -> wait (question 3), then read
reviewed (any head)  -> read, and never request again (one round per PR, E7)
none                 -> request, then pending
```

The query, tested (E8). It uses `-f` for the strings, so an all-digit repo
name is not coerced (pass 3 #12):

```
gh api graphql -f owner=<owner> -f name=<name> -F n=<N> -f query='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){headRefOid reviewRequests(first:20){nodes{requestedReviewer{... on Bot{login}}}} reviews(last:100){nodes{author{login} commit{oid} body}}}}}' --jq '.data.repository.pullRequest as $p | ([$p.reviewRequests.nodes[].requestedReviewer.login] | index("copilot-pull-request-reviewer") != null) as $pending | [$p.reviews.nodes[] | select(.author.login=="copilot-pull-request-reviewer")] as $cr | if $pending then "pending" elif ($cr|length)>0 then "reviewed \(if any($cr[]; .commit.oid==$p.headRefOid) then "head" else "earlier-head" end) \($cr[-1].body | capture("Review effort:\\*\\* (?<e>[A-Za-z]+)")?.e // "unknown")" else "none" end'
```

`head` versus `earlier-head` is information for the presentation. It tells
the user whether Copilot saw the fix pushes. The branch rule does not use
it. The query filters `reviews(last:100)` by author. Operator reply
reviews, one per reply (E1), only crowd it past 100 reviews on one PR, and
the thread read does not depend on it.

### 2. Placement

Yes. The round holds up better folded into the existing structure than as a
separate step, and the change is mostly deletion.

**Owner `/milestone-review`.** Step 2 today says nothing is pushed
(`SKILL.md:103–110`). With the opt-in on, step 2 instead does five things.
Push the branch. Run `gh pr create`, ready for review, with the
`Closes`/`Refs` lines. Record the URL in the header, in a commit on the
branch. Run the state query. Request Copilot on `none`. Then steps 3 to 6
run as today. Step 7's PR-conversation read runs, because the header names
an open PR (`SKILL.md:451–454` already lists the round arm as a trigger).
The read gains one rule, for an unresolved thread whose first comment's
author is Copilot. After the disposition and any fix-now commit, reply on
the first comment and resolve the thread. The module's two commands do that
(`copilot-review.md:92–103`). The chip's Copilot counts (`SKILL.md:447–449`)
stay. Four parts go. Step 6's arm. The module's §2 and §3 state machine.
The round's own step-4 gate re-run. The §6 rules for the read skipping the
round's items. The read is the round.

**Edge by edge against the Background list.** The left column is the
separate round as it stands. The right column is the fold.

| Edge | Separate round | Folded into the read |
|---|---|---|
| Endless wait, 20-minute loop | A background loop (`copilot-review.md:52–55`). It outlives a turn (pass 3 #13). | No wait in the common case. Copilot's 2 to 20 minutes (E5) run under steps 3 to 6. A bounded wait at step 7 runs only on S1. |
| Resume keyed on a log line | Removed at return 2. A mid-round death has no route (pass 3 prior-review #3). | Nothing to resume. A re-run reaches step 7 and reads S3. |
| Stale "waiting" record | Removed at return 2. | No record exists. |
| Second pass re-requests | Guarded by the request-event proxy (`copilot-review.md:30–34`). | Guarded by S2. Any Copilot review on the PR means never request. |
| Automatic review on open | Reads as an earlier pass and skips (pass 3 #1). | S1 and S2 do not care who requested. The read handles its threads. |
| Failing state query | No arm (pass 3 #3). | Exit code first. The read still runs. |
| Hotfix decline leaves an open PR | Open PR, no next command (pass 3 #4). | Question 4. |
| Round fixes land after the fan-out, gated by the `verify` slot alone (pass 1 #13) | Partly fixed by a step-4 gate re-run. | Step 7's fix-now already lands per step 6, before the chip, with the `verify` slot re-run (`SKILL.md:335–339`, `480`). Same as a human reviewer's item. |
| A Copilot finding shows a criterion failing (pass 3 #5) | Forced to follow-up (`copilot-review.md:80–83`). | Step 5's rule includes the return floor. The thread stays unresolved and the next pass's read sees it (question 6). |

The read's rule that it runs once and is not re-run after fix-now commits
(`SKILL.md:457`) stays true. It stops mattering. A Copilot review that
arrives after the read is the next pass's item or the user's. That is
already the rule for a human review that lands after the read.

What this reinstates: the pre-M186 early open, for opted-in repos only.
D-138 rejected the early open because each pre-approval push re-ran CI.
D-152 already prices that cost for opted-in repos ("CI runs on the early
push and again on each fix push"). The step-2 open adds the step-6
checkpoint push and step 5's fix-now pushes to that count. The branch is
pushed at step 2 and again before step 7, with the checkpoint and the
records. Nothing else changes in step 8. One window grows. A ready PR can
be merged from the web UI before the chip (pass 3 #11). That window was
"after the round" and becomes "during the review". The enforcement boundary
(`tracking-rules.md:270–273`) already calls that honor-system, and route (c)
returns have had the same exposure since M177. D-152's text says "after
cairn's own review and before the merge question". Amend it to "before
cairn's own review". The decision's reasons and rejections are unchanged.

The fold keeps two things the separate step did. The report says review
asked for Balanced and hotfix asked for Lite (no API field, AC2). The
presentation names which Copilot items were fixed and in which commits.

**Guest and hotfix cannot open early.** The guest PR opens at the handoff,
after the user's yes (`tracking-rules.md:323–326`). The hotfix fix is the
last thing written before its chip. Both keep a serial request, wait, and
read. They use the same signals, the same bounded wait, and the same
PR-conversation read with the reply-and-resolve rule. For them the module
shrinks to the request, the query, the bound, and the two commands.

### 3. The wait

When S1 is still pending at the read, and only then, a blocking wait is
needed. Its only purpose is the user's intent that Copilot's items are
seen before approval. With the step-2 request, review takes longer than Copilot in
nearly every case (E5), so in `/milestone-review` the wait is usually
zero. In hotfix and guest it is real.

**Bound:** one watcher, at most 10 minutes. That is the Bash tool's
600-second ceiling (`cairn/references/wait-mechanisms.md:29`). The form is
a Monitor on an until-loop over the state query, with `timeout_ms` set.
That is the tracking-rules shape for a wait on a condition, and it is gone
at its timeout (`tracking-rules.md:291–293`). The current module's
`run_in_background` loop (`copilot-review.md:53`) is the shape the wait
rule warns about. Its `timeout` does not end it (`wait-mechanisms.md:63`),
and it outlives a turn end (pass 3 #13). Poll every 30 seconds. Why 10
minutes and not 20: the serial 20 minutes was the round's whole budget. The
fold gives review 20 or more minutes of overlap for free. A hotfix at 10
serial minutes catches four of the seven observed cases outright. The rest
arrive while the user reads the chip.

**At the bound:** the read runs on what exists. The presentation states
`Copilot review pending since <time> on PR #<N>`. The chip is posed.
Nothing stops.

**A review that arrives after:** its threads are unresolved on the PR.
Before the merge, the chip is in front of the user. The user can decline,
and the return's next pass reads them (routes (c) and (d) re-run step 7's
read). After the merge, they stay on the merged PR, unread by this run. The
catch is `/milestone`'s bot-thread audit, the candidate row at
`cairn/ROADMAP.md:44`. Its promotion trigger, "a bot comment that arrives
after a round is missed", is exactly this case. The README's "you see every
Copilot thread before you approve" (`README.md:660`) is false under any
bounded wait. Change it to "every Copilot thread that arrived before the
merge question".

### 4. `/hotfix`

Run it in owner mode, with the PR opened before the chip as D-152 chose,
and define the decline. The four options:

- *Not at all in owner mode.* This contradicts the user's workflow and
  D-152's rejection of "guest repos only". Reject.
- *Guest only.* The same. Reject.
- *PR opened only after approval, round after.* This keeps D-138 for
  hotfix and removes the decline problem at the first chip. But a round
  that fixed anything must re-pose the chip, because the user approved a
  different diff. A decline at that second chip leaves the same open PR.
  D-152 rejected fixes that land after approval. The user also waits the
  same 10 minutes, after the yes instead of before it. Reject.
- *Before the chip, with a defined decline.* The smallest. A decline at
  the chip closes the PR the session opened (`gh pr close <N>`, the
  operator's own PR, reversible with reopen). The branch stays. The close
  block names the branch and the closed PR. Step 2 gains one clause: a
  `hotfix-<slug>` branch that already exists is checked out and
  fast-forwarded, not re-cut. A rerun of `/hotfix` for the same bug then
  resumes the branch and opens a fresh PR on it. GitHub allows a new PR on
  a head whose earlier PR is closed. No open-PR re-entry is needed, so the
  candidate row at `cairn/ROADMAP.md:34` stays where return 2 put it.

The alternative leaves the PR open and names it. That is what the arm says
now (`skills/hotfix/SKILL.md:194–196`), and pass 3 #4 found it incomplete.
Every rerun path then needs an open-PR arm: step 1's adopt walk and step
6's `gh pr create`. The close removes the state instead of routing it.

**The four-option rule.** Hotfix's per-item user choice sits at
`SKILL.md:208–211`. It exists because M177 gave the hotfix user the say
over a contributor's items on an adopted PR. The opt-in line is the user's standing choice for
Copilot's items (`copilot-review.md:16–19`, the M231 question set). So a
Copilot thread takes the agent's disposition, reply, and resolve. The chip
presents it with its disposition as information. Every other item on the
PR keeps the four options. The split is by the thread's first author plus
the opt-in line, not by which path opened the PR. A Copilot item over the
hotfix bar is a follow-up with `Left for a follow-up.`
(`copilot-review.md:80–83`), unchanged. A Copilot item that shows the fix
itself wrong is fix-now inside the hotfix. A repair over the bar takes the
step-1 over-the-bar exit, with the PR closed as on a decline.

**Lite's latency** is 17 and 20 minutes on two of four Lite reviews (E5).
The hotfix round will hit the 10-minute bound often. The report line then
says the review is pending, and the user decides with the PR link in front
of them. That is the honest cost of a serial round on a short fix. Nothing
in the design can shorten Copilot.

### 5. Guest mode

Same session, right after the handoff, bounded as in question 3, then the
close block. Three reasons.

- The user's workflow is guest-mode babysitting. The easystats PRs are
  where the evidence came from. The replies are the operator's own GitHub
  writes on their own PR, as the PR itself is. Pass 2 blame-history #7's
  rejection stands. No cairn file is committed, and no vocabulary leaves
  (the module's reply forms, `copilot-review.md:96–99`).
- A separate later step needs a route from `/milestone` §2's `OPEN` branch
  (`skills/milestone/SKILL.md:162–165`) into a skill that replies and
  resolves. Today that branch reports an unresolved-thread count and
  leaves the milestone `blocked`. That route is the candidate row at
  `ROADMAP.md:44`. It is the right home for the late-review case, not for
  the first round.
- Leaving it to the operator discards the half of the feature the user
  uses most.

The wait's cost here: the session already stops with the close block after
the handoff. The bounded wait sits inside that same turn, and its timeout
leaves nothing armed. A review that arrives after the bound shows up as
`/milestone` §2's unresolved-thread count on the `blocked` row. The
maintainers' `CHANGES_REQUESTED` route is unchanged. A guest hotfix's next
command is `/hotfix <PR ref>`, which has no `OPEN` route. There a late
review is the operator's by hand, and the close block must say so.

One guest-specific point. A fix push after the handoff moves the head
under the maintainers' CI. That is ordinary contributor behavior. The fork
push uses `--force-with-lease` only after a rebase, as the module says
(`copilot-review.md:85–87`).

### 6. Failure modes under the folded design

- **Request fails** (non-zero `gh pr edit`): one chat line with the error.
  No wait. The read runs as usual and finds no Copilot items. The flow
  continues. Same as `copilot-review.md:37–41`.
- **State query errors**: the exit code is non-zero (E6). One line names
  the error. No request, because a double request is the costlier mistake
  (E7). No wait. The read runs, and its own failures are already stated in
  one line (`SKILL.md:478`). Never a stop.
- **Copilot never reviews**: S1 stays pending. The bounded wait ends. The
  read runs on what exists. The presentation names the pending request and
  the PR. After the merge the request stays pending on a merged PR, which
  is harmless. `/milestone`'s bot-thread audit (the ROADMAP row) is the
  later catch.
- **Body findings linking to threads**: the thread is the item. The body's
  `discussion_r` anchors are matched to thread ids and skipped (E4). A
  finding line with no anchor is a body item: a disposition, no reply,
  reported as `copilot: review body — <disposition>`. The level line is
  read from the newest Copilot review's body (E3).
- **Several Copilot reviews** (automatic on open plus a request, or a
  re-review on push): threads are the unit. Every unresolved Copilot
  thread from any review is read. Only the newest review's body is read,
  for anchorless items and the level. Two reviews on the same head cost
  one extra review once. That happens only where a cairn request races an
  automatic request. S1 and S2 make it rare, not impossible, and a rare
  double review is cheaper than a record.
- **A Copilot finding shows an acceptance criterion failing**: it is a
  step-7 read item under step 5's rule, so it takes the return floor
  (`SKILL.md:341–353`). Status goes to `in-progress`, with a return to
  implement. The thread gets no reply and stays unresolved, because its
  fix has not happened. The next pass's read finds it unresolved (S3),
  disposes it `fixed <sha>`, replies, and resolves. This is the stateless
  per-item rule doing the work the "never takes the return floor"
  exception (`copilot-review.md:80–81`) was written to avoid. The exception
  is no longer needed. In a hotfix there is no floor. The item is fix-now
  inside the bar, or the over-the-bar exit with the PR closed.
- **Head force-pushed after a rebase** (guest, or a return): the Copilot
  review's `commit` is no longer an ancestor. S2 is still true, so no
  second request. S3 is unchanged. `isOutdated` and `originalLine` carry
  the position (`copilot-review.md:68–69`).

### 7. Scope and criteria

Which criteria change:

- **AC1**: the "20-minute limit" clause becomes a bounded wait of at most
  10 minutes at the read, after which the skill continues. The module no
  longer "states the wait" as its own step. The Copilot-thread definition,
  the three dispositions, the reply forms, and the resolve stay. "Both
  skills name the module at their round step" becomes "`/milestone-review`
  names it at step 2 and step 7". If the hotfix and guest arms ship, add
  them to that clause.
- **AC2**: replace "the round's chat report says that GitHub's settings
  chose the level" with "the report names the level from the review body's
  `Review effort:` line, or `pending` with no review" (E3). The ask-for
  Lite and Balanced wording stays as the stated intent.
- **AC3**: "pushes the branch and opens the PR after step 6 and before
  step 7" becomes "at step 2". "It then runs the round" becomes "step 7's
  read replies to and resolves each Copilot thread". The hotfix sentence
  gains the decline rule. The off-arm sentence stays.
- **AC4**: unchanged in substance. "The round runs after the handoff opens
  the PR" stays.
- **AC5** (the live round on M231's own PR): keep it, reworded to the
  stateless signals. After step 7's read, `reviewThreads` shows zero
  unresolved threads whose first comment's author is Copilot, among the
  threads that existed at the read. It is the one criterion that
  proves the mechanism, and it has never been ticked.
- **AC6**: unchanged. The prose guard's anchors move with the arms.

**Smallest M231 worth shipping:** the opt-in line. The module reduced to
the request, the state query, the bound, and the reply and resolve
commands. The `/milestone-review` owner arm at step 2 plus the step-7 rule.
The `/milestone-review` guest arm after the handoff. AC5 run live on M231's
own PR. That is one skill, both modes, and the mechanism proven once.

**Move to later work:**

- The `/hotfix` arms, both modes, as a follow-on milestone after the
  milestone round has run live twice (M231's own PR and M232's). Hotfix is
  where the decline edge and most of the serial wait live. M231 reached
  three returns by shipping it on the same pass that was still proving the
  mechanism. If the user wants it in M231, the whole cost is the
  close-on-decline rule and the step-2 existing-branch clause.
- `/milestone`'s bot-thread read of open PRs (`ROADMAP.md:44`). It is the
  catch for every late review in questions 3, 5, and 6.
- A per-request level, once the API grows the field (T1).
- Any handling of Copilot's re-review on push beyond "its threads are the
  next read's items".

**Keep the automated reply and resolve.** The resolve is the only per-item
"handled" mark on the PR (S3). Without it every later pass re-disposes
every Copilot thread, and the design needs a record again. The reply is
one REST call that puts the disposition on the PR. For a hotfix that is
its only record. Neither is where the complexity was. The wait and the
round's self-detection were.

## Beyond the brief

- B1. The level is in the review body (E3). `copilot-review.md:27–28` and
  `README.md:665–667` say the report cannot know it.
- B2. The current query's `timelineItems(last:50, itemTypes:[REVIEW_REQUESTED_EVENT])`
  is safe from commit crowding because of the type filter. The read's
  REST call (`SKILL.md:460`) has no author filter and pages past operator
  reply reviews, one per reply (E1). `--paginate` is already there, so it
  only costs calls.
- B3. `-F owner=<owner> -F name=<name>` type-infers an all-digit value
  (pass 3 #12). `-f` is correct for `String!` variables and worked on every
  test (E8).
- B4. `README.md:660` ("you see every Copilot thread before you approve")
  overpromises under any bounded wait. `README.md:668–669` says "the run
  does not read a review that arrives later". That conflicts with the
  step-7 read, which does read one that lands before it (pass 3
  prior-review #1). Both
  resolve to "every Copilot thread that arrived before the merge question".
- B5. D-138's consequence says the header's PR-URL record "is committed on
  the branch and never pushed". That is false on the opted-in path, where
  the record commit is pushed with the checkpoint (pass 3 blame #4, #5).
  D-152 needs one sentence that names that narrowing.
- B6. `tracking-rules.md:245–246` ("never before") and `README.md:646–648`
  carry the D-138 absolute with the D-152 exception appended. Under the
  step-2 placement the exception's wording changes in both, from "before
  the merge question" to "at the start of review".
- B7. The hotfix guest arm's next command, `/hotfix <PR ref>`, has no
  `OPEN` route (`ROADMAP.md:34`). After a guest hotfix handoff the only
  re-entry is `MERGED`. That is pre-existing and not M231's. The guest
  hotfix close block must still say a late Copilot review is the
  operator's by hand.
- B8. The module's budget header (`copilot-review.md:7–10`) is set for the
  current 124 lines. The folded module is about 40 to 60 lines. Re-seed
  the budget down rather than leave 100 lines of headroom.

## Recommendations

1. **apply**. Replace the module's request-event state machine (§2 and §3)
   with the exit-code-first query of question 1: `pending`, `reviewed`, or
   `none`. Request only on `none`. Never request a second time on a PR
   with any Copilot review.
2. **apply**. Move the owner `/milestone-review` open and request to
   step 2. Delete step 6's round arm. Add one rule to step 7's read: an
   unresolved thread whose first comment is Copilot's gets a reply on the
   first comment and a resolve, after its disposition. Amend D-152's
   placement sentence to match.
3. **apply**. Bound every remaining wait at 10 minutes, as a Monitor with
   `timeout_ms` on an until-loop over the query. It runs only on a
   `pending` result at the read. At the bound, read what exists and say
   the review is pending. Drop the `run_in_background` loop.
4. **apply**. Dedupe body findings against threads by the `discussion_r`
   anchor. Read the level from the body. Treat an anchorless finding as a
   body item with no reply.
5. **apply**. Drop the module's "a Copilot item never takes step 5's return
   floor" exception. A Copilot thread whose disposition is a return stays
   unresolved and unreplied until the next pass fixes it.
6. **apply**. Reword AC1, AC2, and AC3 as question 7 states. Keep AC5,
   reworded to the stateless signals, and run it live before the merge.
7. **apply**. Fix the README and rulebook sentences in B1, B4, and B6. Add
   D-152's one-sentence narrowing of D-138's unpushed-URL clause (B5).
8. **consider**. Defer the `/hotfix` arms to a follow-on milestone after
   two live milestone rounds. If they stay in M231: a decline at the chip
   closes the PR and keeps the branch. Step 2 checks out an existing
   `hotfix-<slug>` branch instead of re-cutting it. Copilot threads take
   the agent's disposition under the opt-in line, and every other item
   keeps the four options.
9. **consider**. Have the guest close block in both skills state in one
   line that a Copilot review arriving after the bound is the operator's by
   hand, until the `/milestone` bot-thread row (`ROADMAP.md:44`) ships.
10. **consider**. Re-seed the module's budget to the folded size (B8).
11. **reject, with reason**. Running the owner hotfix round after approval
    with a re-posed chip. It moves the decline problem to a second chip
    instead of removing it, and D-152 rejected post-approval fixes.
12. **reject, with reason**. Removing the automated reply and resolve. The
    resolve is the per-item state the whole stateless design rests on, and
    the reply is its record on the PR.
13. **reject, with reason**. Any record of "the round ran" in the milestone
    file, the work log, or a marker. Three passes showed each such record
    going stale against the PR, and the PR's own signals (S1 to S3) make it
    unnecessary.
