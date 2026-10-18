<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M282: A later Copilot request is a retry, and a late-recorded request is not reported as missing

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters with `# Copilot review: on` get the round's requests and read its report   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The Copilot round states that a later request on a PR where the state
query finds no Copilot request or review is an intended retry, and its
report at the read gives the not-recorded line as the reason for a missing
review only when the read still finds none.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The candidate row "Copilot not-recorded edges (M281 review)" holds
three gaps in `skills/shared/copilot-review.md` and its callers. (1) §2's
"Make no second request" binds only within §2, so a later review pass or a
`/hotfix` resume that reads `none` requests again. M281's pass 2 did so on
PR #293. The PR timelines of #291, #292, and #293 show no
`review_requested` event, while #290, which Copilot reviewed, shows one
(read 2026-10-18). So a request GitHub never recorded leaves nothing for a
second request to duplicate. At the question set the user chose
to allow the retry and to state it, not to block it. A D-entry narrows
D-153's falsifier "requests Copilot twice on one PR" to a request made
while GitHub holds an earlier Copilot request or review. (2) §2's re-query
runs at once, so a request GitHub records a few seconds late gets a false
"may not be recorded" line. §6 then reports that line as the reason no
review exists only when the read's own state query still prints `none`.
§2's own chat line at request time stays. Only the owner `/milestone-review`
path runs steps 3 to 6 between §2 and the read. On the hotfix owner arm and
both guest handoffs the read's query runs seconds after §2's, so there the
fix catches only a record that lands in those seconds. (3) `/milestone-review`
step 7's presentation, `/hotfix` step 6's chip, and the two guest handoff
closes list the `copilot:` lines and the level or pending line but not
§6's reason line. Each then names it too. README and CHANGELOG text follow.
Other module text is compressed to hold the module's budget.

**Out:** a delayed re-query or a poll at §2 (M281's plan gate chose an
immediate re-query, and the read's own query covers the late case here,
so it has no home). Any cairn record that a request was made (D-153's
rejection stands; the user declined it at this question set). Late bot
comments stay with the row "`/milestone` reads bot threads on open PRs",
and a request with the round off stays with the row "Late Copilot
requests with the round off (M244 review)". New prose guards and mutation
registrations for the hand-run `skills/tests` are not owed (D-109) and are
not added.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: `skills/shared/copilot-review.md` §2 states that a later run of
      §2 on the same PR (a later review pass, or a `/hotfix` resume) whose
      state query prints `none` requests Copilot again. It gives the
      reason: `none` means the query found no Copilot request or review on
      the PR, and a request GitHub never recorded leaves none (PR #291 to
      #293). §2 still requests nothing on `pending` or `reviewed`, and
      still makes no second request after its own re-query prints `none`.
- [ ] AC2: `skills/shared/copilot-review.md` §6 states that §2's
      not-recorded line is given as the reason no review exists only when
      the read's own state query still prints `none`. When that query
      prints `pending` or `reviewed`, the report gives the pending or level
      line and not the not-recorded line.
- [ ] AC3: Four sentences that say what a Copilot report shows name §6's
      reason line for a missing review beside the `copilot:` lines and the
      level or pending line: `skills/milestone-review/SKILL.md` step 7's
      presentation sentence and its guest handoff close (step 8), and
      `skills/hotfix/SKILL.md` step 6's Copilot round arm and its guest close.
- [ ] AC4: `README.md`'s Copilot paragraph and a new entry under
      `CHANGELOG.md`'s `## Unreleased` state that a later pass that finds
      no Copilot request or review on the PR asks again, and that the
      report at the read gives the not-recorded line as the reason for a
      missing review only when the PR still shows no Copilot request or
      review when the read runs.
- [ ] AC5: `wc -l -c skills/shared/copilot-review.md` shows under 140
      lines and under 8,000 bytes, the figures the module's budget line
      states, and the budget line's figures are unchanged.
- [ ] AC6: `cairn/DECISIONS.md` gains a D-entry that narrows D-153's
      falsifier "requests Copilot twice on one PR" to a request made while
      GitHub holds an earlier Copilot request or review on the PR, and
      names a cairn record of the request as the rejected alternative.
- [ ] AC7: The profile's `verify` slot is clean: both gating
      `python3 -m unittest` suites (`scripts/tests`, `hooks/tests`),
      `claude plugin validate` on the plugin and marketplace manifests, and
      `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1
- AC6 → T4
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: In `skills/shared/copilot-review.md`, add the retry sentence to
      §2 (lines 37-49) and the late-record rule to §6 (lines 133-135).
      Compress other module text to stay under 140 lines and 8,000 bytes
      (139 lines, 7,993 bytes at plan). Leave §4's wait sentences and the
      §5 text that `skills/tests/test_guest_fork_remote.py:74` pins as they
      are, since `skills/tests/test_copilot_review_round.py` pins §4.
- [ ] T2: Name §6's reason line in `skills/milestone-review/SKILL.md`
      step 7 (lines 479-481) and its guest handoff close (line 695), and in
      `skills/hotfix/SKILL.md` step 6's Copilot round arm (lines 333-335)
      and its guest handoff close (lines 468-469).
- [ ] T3: Update `README.md`'s Copilot paragraph (lines 849-853) and add a
      `### Fixes` entry under `CHANGELOG.md`'s `## Unreleased`. Grep the
      repo for "second request" and "not recorded" to find any other site
      that states the old rule (the M112 lesson).
- [ ] T4: Append a D-entry to `cairn/DECISIONS.md` that narrows D-153's
      falsifier "requests Copilot twice on one PR" to a request made while
      GitHub holds an earlier Copilot request or review on the PR. It
      states the timeline facts from Scope (1), and records the rejected
      alternative: a cairn record of the request, which D-153 rejected.
- [ ] T5: Run the `verify` slot, and hand-run `skills/tests` after the
      module and skill edits (the M148 and M279 lessons).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: not run — work named at the question set.
- 2026-10-18: question set: which candidate row to plan — "Copilot not-recorded edges (M281 review)", the one row whose promote condition fired (PR #293).
- 2026-10-18: question set: how much of the row — all three gaps.
- 2026-10-18: question set (second chip, posed after investigation showed the first chip's "never ask again" description needed a cairn record D-153 rejected): a later request on `none` — allowed as a stated retry, not blocked by a record.
- 2026-10-18: plan gate chose allowing the retry over blocking it with a Review-section record because GitHub's `none` holds no request to duplicate (no `review_requested` event on PR #291-#293) and D-153 rejected round records; falsified by a PR where a request on `none` starts a second Copilot review.
- 2026-10-18: plan gate chose correcting the report at the read over a delayed or polled §2 re-query because the read already runs the state query and M281 chose no §2 wait; falsified by a late-recorded request on the owner `/milestone-review` path whose not-recorded line still reaches the Review section.
- 2026-10-18: criteria audit (full mode, fresh Opus reader): 7 findings, all fixed. (1) T4's D-entry had no criterion: AC6 added. (2) The Goal and AC4 promised more than §6 does, since §2's chat line stays: both narrowed to the report at the read. (3) AC1's reason claimed GitHub behavior from four PRs: reworded as what the query found. (4) The late-record fix covers little on the hotfix and guest paths: stated in Scope, falsifier narrowed to the owner milestone path. (5) The hotfix chip and both guest closes also omit the reason line: AC3 and T2 extended. (6) No other site states the old rule: no change. (7) AC5 is tight and §5 text is pinned by `test_guest_fork_remote.py:74`: noted in T1.
- 2026-10-18: collision check: M281 (done) shipped the not-recorded line, extended here. D-153's falsifier collides with the retry, superseded in part by T4's D-entry at the user's choice. Candidate row "Copilot not-recorded edges (M281 review)" absorbed in full. Rows "`/milestone` reads bot threads on open PRs" and "Late Copilot requests with the round off (M244 review)" stay distinct (Out).
- 2026-10-18: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-18: lessons harvested: M112/M249 (grep old wording, CHANGELOG task, T3), M148/M279 (hand-run `skills/tests` after edits near guarded text, T5).
- 2026-10-18: changelog: a new Unreleased Fixes entry, not an edit of M281's entry, since the profile gate asks for an entry for this milestone's changes.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
