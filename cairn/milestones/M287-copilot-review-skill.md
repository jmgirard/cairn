<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M287: A /copilot-review skill handles Copilot's notes on a PR and replies to its summary

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — a new user-invoked skill, and a change to what `/hotfix` and `/milestone-review` post on a PR   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m287-copilot-review-skill   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A user can run `/copilot-review` on any PR to have Copilot's notes read, settled, replied to, resolved, and its summary answered, and the Copilot round in `/hotfix` and `/milestone-review` answers the summary the same way.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a new skill `skills/copilot-review/SKILL.md` that runs outside a
milestone run on a PR the operator can push to, built on the procedures of
`skills/shared/copilot-review.md` (state query, wait, thread read, reply,
resolve). A summary reply added to that module, so `/hotfix` and
`/milestone-review` post it too. The rule that a note the agent cannot
settle alone is put to the user in chat, never on GitHub. The skill's
listing in the status mod, `cairn_cost`, the README, and the changelog.

**Out:** requesting a Copilot review from `/copilot-review` (the request
stays with `/hotfix` and `/milestone-review`, module §2). The arm edges in
the parked `Copilot arm edges (M285 review)` candidate row stay there.
A PR whose head the operator cannot push to: the skill stops with a close
block instead.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `skills/copilot-review/SKILL.md` exists, and `/copilot-review`,
      given a PR number or URL, or nothing (the current branch's PR), works
      in this order: it reads every unresolved Copilot thread (paged
      `reviewThreads` query) and every Copilot review with a non-empty body
      (paged `reviews` query); it gives each thread a disposition (fix now,
      reject with a reason, or follow-up); it commits and pushes each fix to
      the PR's head; it replies on and resolves each thread; and last it
      posts one reply to each such review it has not yet answered. Shown by
      one run of the skill on this milestone's PR, or, if Copilot does not
      review it, on another PR that carries at least one unresolved Copilot
      thread, named in the Review section, with the replies, resolves, and
      summary reply read back from GitHub.
- [ ] AC2: When the agent cannot settle a thread's disposition without the
      user, `/copilot-review` asks the user with a chip in chat before it
      replies on that thread, and posts no question to GitHub. Shown by the
      skill's text and hand-run guards in `skills/tests`.
- [ ] AC3: A case-insensitive search for `thank` in
      `skills/copilot-review/SKILL.md` and `skills/shared/copilot-review.md`
      finds only text that forbids thanking Copilot.
- [ ] AC4: With the Copilot round on, `/hotfix` and `/milestone-review`
      post one reply to each Copilot review summary after that review's
      threads are resolved, through `skills/shared/copilot-review.md`. The
      reply links the review, and a later read skips a review whose link a
      comment by the operator already carries. Shown by the module's text and
      hand-run guards in `skills/tests`, and, where Copilot reviews this
      milestone's PR, by that PR's summary answered once.
- [ ] AC5: With the Copilot round on, a thread the agent cannot settle
      without the user takes the follow-up disposition in `/hotfix` and
      `/milestone-review`, unless it takes `/milestone-review` step 5's
      return floor, and the approval chip or merge question names it. Shown
      by the module's text and hand-run guards in `skills/tests`.
- [ ] AC6: The new skill is listed in these four places: `CAIRN_SKILLS` in
      `hooks/status/band.ts`, the generated `hooks/status/fixtures.gen.ts`,
      `PHASES` in `scripts/cairn_cost.py`, and the README's skill table. The
      `CHANGELOG.md` Unreleased section has an entry for the skill and the
      summary reply.
- [ ] AC7: The profile's `verify` slot is green (both unittest suites, the
      two `claude plugin validate` runs, and `claude plugin test .`).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1, T4
- AC3 → T1, T2, T4
- AC4 → T2, T4
- AC5 → T2, T4
- AC6 → T3
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Write `skills/copilot-review/SKILL.md`: frontmatter, phase
      header, PR resolution (argument, else `gh pr view` on the current
      branch), checkout of the PR's head on a clean tree, the module's state
      query and wait (§3, §4), the thread and review read, dispositions, the
      chat chip for notes the agent cannot settle, fix commits with the
      `verify` slot green and a push by the open-PR head rule, replies and
      resolves (§5), the summary reply, and a close block. On an `m<nnn>-`
      branch a fix commit also carries a work-log line. Guest mode: no cairn
      vocabulary in replies or commits.
- [x] T2: Edit `skills/shared/copilot-review.md` §5 and §6: the summary
      reply (after the review's threads are resolved, linking the review,
      skipped when an operator comment already carries the link, no thanks),
      the follow-up route for a note the agent cannot settle, and the rule
      that questions go to chat, never to GitHub. Compress so the module
      stays under its 140-line and 8,000-byte budget. Touch `/hotfix` step 6
      and `/milestone-review` step 7 only where their text contradicts it.
- [x] T3: List the skill in `hooks/status/band.ts`, regenerate
      `hooks/status/fixtures.gen.ts` with `hooks/status/gen_fixtures.py`,
      add it to `scripts/cairn_cost.py` `PHASES`, add a README skill-table
      row, and write the `CHANGELOG.md` Unreleased entry. Also add it to the
      other skill lists: the outside-the-run list in
      `skills/shared/tracking-rules.md` (Question gates), the list in
      `skills/tests/test_phase_header_levels.py`, and the skill count in
      `cairn/DESIGN.md`.
- [x] T4: Add hand-run guards to `skills/tests/test_copilot_review_round.py`
      for AC2 to AC5. Probe each clause separately and see each guard red
      with its clause removed: AC2's chip-before-reply and no-GitHub-question
      clauses; AC4's after-resolve, link, and skip-when-linked clauses; AC5's
      follow-up route and chip naming.
- [x] T5: Append a D-entry to `cairn/DECISIONS.md` for the summary reply,
      the chat-only questions, and the skill making no request (annotates
      D-153).
- [x] T6: Run the `verify` slot and the hand-run `skills/tests` suite.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — a new skill and a change to what two skills post on GitHub.
- 2026-10-19: question set: none posed — the user said in chat on 2026-10-19 that the agent decides, and asks only what it cannot decide without the user.
- 2026-10-19: question set: home of the skill — the user chose a cairn plugin skill over a personal skill.
- 2026-10-19: plan gate chose the follow-up disposition for an unsettled note inside `/hotfix` and `/milestone-review` over an extra question at their chip because an answer that needs a fix would land after approval, which D-152 rejected; falsified by a run where a follow-up row was the wrong home for a note the user wanted fixed before merge.
- 2026-10-19: plan gate chose a review link in an operator comment as the summary-reply record over any stored record because D-153 rejected any record that the round ran; falsified by a summary answered twice on one PR.
- 2026-10-19: plan gate chose no Copilot request from `/copilot-review` because a request spends credits and the two run skills already make it; falsified by users running the skill on PRs with no Copilot review.
- 2026-10-19: collision check: M231, M282, M285 shipped the round; D-152, D-153, D-183, D-185 read whole, none rejects a summary reply or a standalone skill; parked `Copilot arm edges (M285 review)` row left as is.
- 2026-10-19: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: criteria audit (full, fresh Opus reader): 8 findings, all taken narrower — AC1 bounds summaries to non-empty review bodies from paged queries; AC1/AC4 evidence falls back to a named PR since Copilot may not review this one (D-183, D-185); per-clause guard probes moved from AC2/AC4/AC5 to T4 (instrument property); AC5 excepts the review step-5 return floor; AC6 names its four places, and three other skill lists join T3. AC3, AC7: none.
- 2026-10-19: T1 done: `skills/copilot-review/SKILL.md` written in plain English to pass the simple-english lint hook; it fences the request command on `none` rather than making the request.
- 2026-10-19: T2 done: module §5 gains the summary reply and the unsettled-note follow-up route; §1 to §6 compressed to 137 lines and 7,999 bytes (under budget); the §2 reason line now reads "not seen by GitHub" to drop a banned modal; the wait guard follows the reworded "It prints only a result that differs from the last"; `/hotfix` and `/milestone-review` text needed no change, since both cite §5.
- 2026-10-19: T3 done: skill listed in band.ts, fixtures.gen.ts (regenerated), cairn_cost PHASES, the README table and Copilot bullet, the rulebook's outside-the-run list, test_phase_header_levels, and DESIGN.md (× 11); the band test's count and test_design_interview's "× 11" follow; CHANGELOG has a changes entry and a New entry.
- 2026-10-19: T4 done: 12 per-clause guards in test_copilot_review_round.py, each registered in the mutation harness and red when its block is blanked; the every-thanks-line guard was seen red by hand with a planted "Thanks for the review!" line, then the line was removed.
- 2026-10-19: T5 done: D-187 appended (annotates D-153).
- 2026-10-19: T6 done: verify green (scripts 428 OK, hooks OK, both validates pass, claude plugin test 2281 pass 0 fail); skills/tests 910 OK; cairn_validate all checks passed.
- 2026-10-19: claim audit: 58 claims read, 7 corrected — README.md, CHANGELOG.md, skills/shared/copilot-review.md, skills/hotfix/SKILL.md, skills/milestone-review/SKILL.md, skills/tests/test_copilot_review_round.py; the same reader re-read all 7 and found them correct; verify green again after the fixes (claude plugin test 2281 pass).
- 2026-10-19: the simple-english lint hook flags older text in tracking-rules.md, README.md, and CHANGELOG.md on every edit; only this milestone's new text was brought under it.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
