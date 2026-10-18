<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M281: A Copilot request that GitHub does not record is reported

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters with `# Copilot review: on` read the round's report   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m281-copilot-request-not-recorded, https://github.com/jmgirard/cairn/pull/293   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When the Copilot request command exits 0 but GitHub records no request, the
round says so in one line instead of reporting nothing.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** On PR #291 and PR #292, `gh pr edit <N> --add-reviewer @copilot`
exited 0 four times and the PR timelines show no `review_requested` event.
PR #290 the same day worked. The user's Copilot credits were used up.
Today `skills/shared/copilot-review.md` §2 counts only a non-zero exit as a
failure, so the run goes on and the report does not say why no review
exists. This milestone adds one re-read of the PR after the request in §2,
a one-line report on `none`, the matching §6 report clause, a README
sentence, and a CHANGELOG entry. It compresses other module text to stay
inside the module's budget. This milestone's own review requests Copilot
on its PR, so the new line runs live there while the credits are out.

**Out:** a retry through a second request command (declined at the M281
question set, so it has no home). A Copilot request made with the round
off stays with the candidate row "Late Copilot requests with the round
off (M244 review)". New prose guards and mutation registrations for the
hand-run `skills/tests` are not owed (D-109) and are not added.

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

- [ ] AC1: `skills/shared/copilot-review.md` §2 states that after the
      request command exits 0, the round runs the §3 state query once more.
      On `none` it reports in one line that GitHub may not have recorded the
      request, naming used-up Copilot credits as one possible cause, and
      makes no second request. On `pending` or `reviewed` it goes on as
      before, and on a failed query it follows §3's failure rule. §2 adds no
      wait of its own, and §4's read-time query is unchanged.
- [x] AC2: `skills/shared/copilot-review.md` §6's report, where it says why
      no review exists, names the not-recorded case from AC1 when §2 ran in
      the same pass.
- [x] AC3: `README.md`'s Copilot paragraph and a new entry under
      `CHANGELOG.md`'s `## Unreleased` state that when the state query just
      after a request that exited 0 prints `none`, the run says so in one
      line, makes no second request, and does not wait at that point.
- [x] AC4: `wc -l -c skills/shared/copilot-review.md` shows under 140 lines
      and under 8,000 bytes, the figures the module's budget line states,
      and the budget line's figures are unchanged.
- [ ] AC5: The profile's `verify` slot is clean: both gating
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
- AC4 → T1, T3
- AC5 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: In `skills/shared/copilot-review.md`, add the re-query and the
      not-recorded line to §2 after its non-zero-exit sentence, and the
      not-recorded case to §6's "says why no review was requested" clause
      (worded as why no review exists). Compress other module text by at
      least the added bytes so AC4 holds (the module was 139 lines and
      7,987 bytes at plan time). Keep the strings the existing guards in
      `skills/tests/test_copilot_review_round.py` and
      `skills/tests/test_mutation_harness.py` pin, or update those pins in
      the same commit.
- [x] T2: Add one sentence to `README.md`'s "Copilot can review each PR
      first (opt-in)" paragraph and an entry under `CHANGELOG.md`'s
      `## Unreleased` (section chosen at implement), each stating AC3.
- [x] T3: Run the `verify` slot (AC5) and `wc -l -c` on the module (AC4).
      Hand-run `python3 -m unittest discover -s skills/tests` and note its
      result in the work log (non-gating, D-109).

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
- 2026-10-18: question set: which work to plan — the user said their Copilot credits are used up; a follow-up chip asked whether to still plan the report, and the user chose to plan it.
- 2026-10-18: question set: what the round does when GitHub does not record the request — report in one line and go on.
- 2026-10-18: collision check: absorbed the candidate row "Copilot request not registered" (started token added). Its stated trigger (the next opted-in PR) had not fired; the user's credits answer named the cause. D-152 and D-153 do not conflict, since no second request is made. Related rows "Late Copilot requests with the round off (M244 review)" and "`/milestone` reads bot threads on open PRs" stay apart.
- 2026-10-18: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-18: lessons harvested: M112/M249 (README and CHANGELOG surfaces), M148/M182 (pinned guard strings near edited prose), the gating-suite lesson (run both suites after a `skills/` edit).
- 2026-10-18: plan gate chose report-and-go-on over a retry through a second request command because the user picked it and no second command was seen working here; falsified by a not-recorded request that a second command would have recorded.
- 2026-10-18: plan gate chose an immediate re-query over a delayed one because PR #290's request event landed at once (review_requested 19:44:59Z, work started 19:45:29Z); falsified by an opted-in PR whose request was recorded but whose immediate re-query printed `none`.
- 2026-10-18: criteria audit (full mode, fresh Opus reader): 6 findings, all fixed. AC1 narrowed to "adds no wait of its own" (§4's read-time wait stays) and "may not have recorded" (timing). AC2 reworded to "why no review exists" and scoped to the same pass (no stored record, D-153). AC3 narrowed to the re-query case. AC5 dropped the hand-run `skills/tests` clause (D-109; it binds an instrument), now in T3 as a noted non-gating run. Dropped the new-guard task (D-109: not owed). AC4 clean but tight.
- 2026-10-18: implement started on branch m281-copilot-request-not-recorded; untracked `cairn-probe.log` and `tsconfig.json` predate this work and stay unstaged.
- 2026-10-18: T1 done: §2 gains the re-query and the not-recorded line, §6 names it; cuts elsewhere (a redundant §1 note sentence, §4's restated wait-once clause, rewraps, shorter phrasings) bring the module to 138 lines and 7,998 bytes; no guard-pinned string changed; verify green (scripts 423 OK, hooks 179 OK, both validates 0, plugin test 2132 pass).
- 2026-10-18: T2 done: README Copilot paragraph gains two sentences; CHANGELOG entry placed under Unreleased `### Fixes`, since the round was silent where it owed a reason; both gating suites green after the edits.
- 2026-10-18: T3 done: module 138 lines / 7,998 bytes, budget line unchanged; both validates 0; `claude plugin test` first run had 2 fails, both "timed out after 5000 ms" in M212 AC4 layout tests (candidates-skeleton, high-candidate plan-row) on a branch with no TS change, and the rerun passed 2132/0; hand-run skills/tests 886 OK (non-gating, D-109).
- 2026-10-18: claim audit: 17 claims read, 3 corrected — skills/shared/copilot-review.md (§6 level-line choice restored as alternatives; §2 "whoever made the request" moved back onto the never-request rule), README.md and CHANGELOG.md ("goes on without Copilot" overstated, since a late-recorded request can still be waited for at the read).
- 2026-10-18: substantive amendment: AC3 "goes on without Copilot" → "makes no second request, and does not wait at that point", after the claim audit showed the old wording false under §4's read-time wait; the deliverable the user sees is unchanged, so no stop.
- 2026-10-18: re-audit: AC3 (full) — reachable, no IP or D-entry conflict, bounded, binds the docs' prose, proportionate; noted it does not require the old phrase to go (kept narrower; the docs drop the phrase anyway) and called "at that point" loose.
- 2026-10-18: claim audit re-read (same reader): the 3 corrected claims are correct; README wrap fixed. Implement complete: both gating suites OK after the last edits, both validates 0, `claude plugin test` 2132/0 at dcf4a52c (later edits are markdown only), skills/tests 886 OK; status → review.
- 2026-10-18: review step 2 Copilot arm: pushed, opened PR #293; state query `none`, request exited 0, re-query `none`, so the round reported "Copilot request on PR #293 not recorded by GitHub (used-up Copilot credits are one cause)" and made no second request (the new §2 rule, live).
- 2026-10-18: review return 1: AC1 — §2's reported line says "not recorded by GitHub" as a fact, where AC1 requires a line saying GitHub may not have recorded the request (diff-bug #1). The fix-now items diff-bug #5, #6, #7 and blame-history #2, #8 ride the same fix pass, since they touch the same lines and files.

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

- AC1 evidence (2026-10-18, read of `skills/shared/copilot-review.md` §2 at HEAD): after a zero exit, "run the state query once more"; on `none`, one line "`Copilot request on PR #<N> not recorded by GitHub (used-up Copilot credits are one cause)`" and "Make no second request"; on `pending` or `reviewed`, "go on"; "A failed query follows §3"; "This step adds no wait." §4 still waits only when the query prints `pending` as it reads the PR's conversation, and the §3 query block is byte-identical to main's. Live: on PR #293 the request exited 0 and the re-query printed `none`.
- AC2 evidence (same read, §6): "or says why no review exists, such as §2's not-recorded line in the same pass."
- AC3 evidence (`grep` at HEAD): README.md:849-852 "If the request command exits 0 but the PR shows no Copilot request or review just after it, Claude says so in one line, makes no second request, and does not wait there."; CHANGELOG.md:522-530, under `## Unreleased` → `### Fixes` (line 520, before `## 2.0.0` at 704), new entry naming the one line, "It makes no second request and does not wait there."
- AC4 evidence: `wc -l -c skills/shared/copilot-review.md` → 138 lines, 7,978 bytes; the line "under 140 lines and under 8,000 bytes" appears once on main and once at HEAD.
- Pass 1 consistency gate: `cairn_validate` all checks passed; CHANGELOG entry present with no milestone numbers; no principle changed, so `cairn_impact` skipped; the verify run was stopped for the return below, so AC5 waits for pass 2.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the reported line says "not recorded by GitHub" as a fact, while AC1 requires a line saying GitHub may not have recorded the request — floor return (AC1 fails as written), review return 1; AC1 unticked, its evidence above missed this.
- diff-bug #2: "Make no second request" binds only within §2, so a later review pass or a hotfix resume that reads `none` requests again — follow-up, row "Copilot not-recorded edges (M281 review)".
- diff-bug #3: §6 names the not-recorded line only as an example — reject, false: AC2 asks that §6 name the case, and it does.
- diff-bug #4: milestone-review step 2's arm does not say where §2's line goes — reject, false: §6 says `/milestone-review` writes the lines to the Review section.
- diff-bug #5: "Resolve the thread, the PR's only 'handled' mark" makes the thread the mark — fix now.
- diff-bug #6: "whoever asked" and "counts a failure" are vaguer than the text they replaced — fix now.
- diff-bug #7: README.md:853 is a 104-character line; copilot-review.md:124 is a short line — fix now for the README line; reject the module line, style.
- diff-bug #8: the work log gives 7,998 bytes and the AC4 evidence 7,978 — reject, false: each was true when written, and the work log is append-only.
- blame-history #1: the dropped "a read that follows a wait in the same pass does not wait again" — reject, planned change: T1's compression, and "A pass waits at most once" keeps the rule.
- blame-history #2: "whoever asked" weakens M231's "who made an earlier request does not matter" — fix now (with diff-bug #6).
- blame-history #3: an immediate re-query can mislabel a request that GitHub records late — follow-up, row "Copilot not-recorded edges (M281 review)" (the plan's falsifier).
- blame-history #4: the dropped "The note requests, replies, and resolves nothing." — reject, planned change: §1's first paragraph still says it.
- blame-history #5: "(the M231 question set)" shortened to "(M231)" — reject, planned change: D-152 and D-153 hold the consent record, and M231 points to it.
- blame-history #6: the dropped "so it keeps polling to its 25-minute exit" — reject, planned change: "or after 25 minutes" keeps the behavior.
- blame-history #7: §6 ties the line to "the same pass" — reject, planned change: AC2's wording after the criteria audit (no stored record, D-153).
- blame-history #8: README over-long line — fix now (with diff-bug #7).
- prior-review #1: a lagged `none` after a successful request gives a false "not recorded" line, and the next pass requests again (PR #240 thread on false `none`) — follow-up, row "Copilot not-recorded edges (M281 review)".
