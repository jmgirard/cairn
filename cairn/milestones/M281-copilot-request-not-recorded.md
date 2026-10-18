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
- **Branch/PR:** m281-copilot-request-not-recorded   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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
- [ ] AC2: `skills/shared/copilot-review.md` §6's report, where it says why
      no review exists, names the not-recorded case from AC1 when §2 ran in
      the same pass.
- [ ] AC3: `README.md`'s Copilot paragraph and a new entry under
      `CHANGELOG.md`'s `## Unreleased` state that when the state query just
      after a request that exited 0 prints `none`, the run says so in one
      line and goes on without Copilot.
- [ ] AC4: `wc -l -c skills/shared/copilot-review.md` shows under 140 lines
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
- [ ] T3: Run the `verify` slot (AC5) and `wc -l -c` on the module (AC4).
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
