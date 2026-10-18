<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M276: A feature cut short at implement or review still ships as one change

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what implement, plan, and the release walk tell every adopting repo to do when a milestone's scope is cut   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m276-series-from-a-scope-cut, https://github.com/jmgirard/cairn/pull/288   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When an amendment at implement or a descope at review moves part of a user-facing milestone to later work, the cut milestone and the milestone that finishes it form a feature series, so the feature keeps one changelog entry and the release walk sees it as unfinished.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** tracking-rules "Feature series" gains a second way a series forms:
a scope cut (a substantive amendment at `/milestone-implement` step 6,
including one that executes a `/milestone-review` descope) that moves work
a user-facing milestone's Goal or Scope `In:` promised to later work. The
cut records that work as a candidate row carrying `split from M<NNN>`,
also when its home is a split milestone, which is then planned from the
row. The cut milestone's changelog entry is the series' one entry. The
plan that turns the row into a milestone writes the `feature series:` line
in the new milestone only, since the cut milestone is archived by then.
`/cairn-release` step 1 lists a marked row whose cut milestone is `done` as
an unplanned part. README tip and the CHANGELOG's series entry.

**Out:** the readers that already key on the `feature series:` line (the
four profiles' changelog gates, `/hotfix` step 5, `/milestone-review` step
8's guest sentence, the archive-summary template, `/milestone` §1, which
cites the release rule) → unchanged, because the milestone planned from the
row carries the line. A validator check on the marker → not planned; the
rule stays prose, as M274's plan gate chose. Marking remainder rows that
cuts wrote before this lands → not needed: no row on the 2026-10-18
ROADMAP is the remainder of a user-facing cut. An internal-tier cut, and
a follow-up row for a narrowed criterion's finding (the return-adjacent
direction rule) → unchanged: such a row takes no marker. What a later part
does once a release shipped the series' entry → unchanged rule (c); the
four profiles' gates read "existing entry", and narrowing both → the
candidate row "Series entry after a release (M276 plan)".

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

- [x] AC1: The tracking-rules "Feature series" paragraph states that a
      series also forms when a substantive amendment of a user-facing
      milestone, at implement or executing a review descope, moves work
      that milestone's Goal or Scope `In:` promised to later work: the cut
      milestone and the milestone later planned for that work are the
      series. It also states that rules (a) and (b) do not bind the cut
      milestone, that the cut milestone's changelog entry, where it has one,
      is the series' one entry under rule (c), and that only the later
      milestone carries the `feature series:` line.
- [x] AC2: `/milestone-implement` step 6 states that such an amendment
      records the moved work as a candidate row whose text carries
      `split from M<NNN>`, naming the amended milestone, also when the
      work's home is a split milestone, and that neither a follow-up row
      for a narrowed criterion's finding nor a remainder row of an
      internal-tier milestone carries the marker.
- [x] AC3: `/milestone-plan` step 4's Feature series bullet states that a
      milestone the plan creates from a candidate row carrying
      `split from M<NNN>` gets the work-log line
      `feature series: M<NNN> -> M<new>`.
- [x] AC4: `/cairn-release` step 1's "Half-merged feature series" paragraph
      states that the version-decision question also names each row of
      `cairn/ROADMAP.md`'s Candidates section whose text carries
      `split from M<NNN>`, where M<NNN>'s status, read by that paragraph's
      status rule, is `done`, as an unplanned part of M<NNN>'s feature, and
      that it leaves out such a row whose ` — started M<x>` token names a
      milestone whose status, read by the same rule, is `planned`,
      `in-progress`, `blocked`, or `review`.
- [x] AC5: README's feature-series tip names the cut-scope case. The
      CHANGELOG's Unreleased feature-series entry is edited to describe it,
      and `git diff <default-branch>...HEAD -- CHANGELOG.md` adds no new
      top-level `- **` entry.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T1, T5
- AC5 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Guards first. In `skills/tests/test_feature_series.py`, add one
      test per sentence AC1–AC4 name, each with its own entry in
      `skills/tests/test_mutation_harness.py`; see each red before its prose
      lands. Update the existing `TestRulebookParagraph` pins and their
      mutation entries where T2 rewords pinned text.
- [x] T2: tracking-rules "Feature series" (`skills/shared/tracking-rules.md:192-204`):
      the cut-scope sentences (AC1), including the exception to "The plan
      writes … in each milestone of the series". Re-seed the rulebook-mass
      baseline in its three places
      (`skills/milestone/SKILL.md:120`,
      `skills/tests/test_cost_audit_line.py:69`,
      `skills/tests/test_mutation_harness.py:121`).
- [x] T3: `/milestone-implement` step 6, beside the return-adjacent
      direction rule (`skills/milestone-implement/SKILL.md:214-226`): the
      `split from M<NNN>` marker sentence (AC2).
- [x] T4: `/milestone-plan` step 4's Feature series bullet
      (`skills/milestone-plan/SKILL.md:490-497`): the series line for a
      marked row (AC3).
- [x] T5: `/cairn-release` step 1, "Half-merged feature series"
      (`skills/cairn-release/SKILL.md:58-68`): marked rows (AC4).
- [x] T6: README tip (`README.md:763-768`) and the CHANGELOG's Unreleased
      feature-series entry, edited in place (AC5).
- [x] T7: Run the `verify` slot (both gating suites, `claude plugin
      validate` on both manifests, `claude plugin test`), hand-run
      `skills/tests`, and `cairn_validate`.

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
- 2026-10-18: question set: what to work on — the candidate row "Feature series from a review-time split (M274 plan)"; how wide — the main failure and its edges (both parts of the row: no `feature series:` line, and a second changelog entry).
- 2026-10-18: collision check: absorbs the candidate row "Feature series from a review-time split (M274 plan)" in full; M274 and M275 (done) shipped the planned-series rule this extends; D-103 is the review-time split precedent (M139 → candidate row → M140), no rejection; inbox sweep found 0 open issues and 0 open PRs.
- 2026-10-18: plan gate chose a `split from M<NNN>` marker on the remainder row, with the later plan writing the `feature series:` line, over the cut writing that line itself, because the line's readers parse `M<a> -> M<b>` and the moved part has no milestone id at the cut; falsified by a cut whose remainder is later planned with the marker unread (a request that names the work but not the row).
- 2026-10-18: plan gate chose the release walk listing marked rows over making the cut plan the remainder as a milestone at once, because a review descope ends at a merge question and planning there adds a stop; falsified by a marked row whose half-shipped feature reaches a release that the walk did not flag.
- 2026-10-18: criteria audit (full, fresh Opus reader): 5 findings, all fixed toward the narrower promise. (1) a cut to a split milestone formed no series: AC2 now records that work as a marked row too. (2) the marker's domain was unclear: AC1/AC2 limit it to work the Goal or Scope `In:` promised, with no marker on a narrowed criterion's follow-up row. (3) appending the line to the cut milestone could never run, since the row reaches main only at that milestone's merge and archive: arm dropped, AC1 says only the later milestone carries the line. (4, 5) the released-entry clause contradicted the four profiles' gates and changed every series: removed, sent to the candidate row "Series entry after a release (M276 plan)". The release-walk and docs criteria passed (then AC5, AC6); criteria renumbered AC1–AC5.
- 2026-10-18: remainder ledger: the absorbed row's two parts (no series line; a second changelog entry) are in M276; the released-entry gap the plan found becomes the candidate row "Series entry after a release (M276 plan)".
- 2026-10-18: implement started on branch `m276-series-from-a-scope-cut`; untracked `cairn-probe.log` and `tsconfig.json` (not this milestone's) left unstaged.
- 2026-10-18: T1: `TestCutSeries` (6 tests) in `skills/tests/test_feature_series.py`, reading whitespace-collapsed text so wrapped prose matches whole (docstring says so); all 6 red by AssertionError before the prose; 18 mutation entries, one per asserted sentence.
- 2026-10-18: T2: tracking-rules gains the "A cut series" paragraph after "Feature series", short sentences per the simple-english hook (its whole-file counts are mostly old text, left alone); rulebook-mass baseline re-seeded to 742 lines / 71,576 bytes at its three sites.
- 2026-10-18: T3–T5: implement step 6 "A cut series" paragraph; plan step 4 bullet also says the new milestone's changelog task edits the cut milestone's entry under (c); release step 1 names marked rows and "No such series or row".
- 2026-10-18: substantive amendment: AC4 adds that the walk leaves out a marked row whose ` — started M<x>` token names a `planned`, `in-progress`, `blocked`, or `review` milestone, since that milestone's `feature series:` line already lists the series; found while writing the CHANGELOG claim; wording only, the user-visible plan unchanged.
- 2026-10-18: re-audit: AC4 (full) — 1 finding: "no ` — started` token" also hid a row whose token names a dropped milestone; fixed to the four live statuses.
- 2026-10-18: re-audit: AC4 (full) — nothing; passes (re-entry read of the fixed wording).
- 2026-10-18: T6: README tip and the CHANGELOG's Unreleased series entry edited in place, no new entry.
- 2026-10-18: claim audit: 45 claims read, 2 corrected — skills/tests/test_mutation_harness.py (three asserted sentences lacked their own entry; added), skills/cairn-release/SKILL.md and skills/milestone-implement/SKILL.md (cite tracking-rules "A cut series"); same reader re-read both, now hold; skills/tests 883 OK.
- 2026-10-18: T7: verify green (scripts 418 OK, hooks 179 OK, plugin and marketplace validate exit 0, plugin test 0 fail), skills/tests 883 OK, cairn_validate all checks passed.
- 2026-10-18: review started; PR https://github.com/jmgirard/cairn/pull/288 opened at review start (Copilot round on); Copilot state `none`, requested.
- 2026-10-18: step-7 approval: m276-series-from-a-scope-cut approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

Pass 1, 2026-10-18, branch head 8d1620e6 (main 3fcceb41, not moved).

- AC1: `skills/shared/tracking-rules.md:206-213` "A cut series" paragraph read: scope cut defined (substantive amendment moving work the Goal or Scope `In:` promised, at implement or carrying out a review descope); cut milestone plus later milestone are the series; (a) and (b) do not bind the cut milestone; its entry, where it has one, is the one entry under (c); only the later milestone carries the line. `TestCutSeries` rulebook tests OK; mutation harness OK (each sentence's blanking reds its guard).
- AC2: `skills/milestone-implement/SKILL.md:227-235` read: such an amendment records the moved work as a candidate row whose lineage carries ` — split from M<NNN>` naming the milestone, the same row when the home is a split milestone; no marker on a narrowed criterion's follow-up row or an internal-tier remainder row. `test_implement_marks_the_row` OK.
- AC3: `skills/milestone-plan/SKILL.md:498-502`, inside step 4's Feature series bullet, read: a milestone created from a row carrying `split from M<NNN>` gets `feature series: M<NNN> -> M<new>`. `test_plan_writes_the_line_for_a_marked_row` OK.
- AC4: `skills/cairn-release/SKILL.md:68-71`, inside step 1's "Half-merged feature series" paragraph, read: the question names each Candidates row of `cairn/ROADMAP.md` carrying `split from M<NNN>` with M<NNN> `done` by the paragraph's status rule as an unplanned part of M<NNN>'s feature, and leaves out a row whose ` — started M<x>` token names a `planned`, `in-progress`, `blocked`, or `review` milestone by that rule. `test_release_names_marked_rows` OK.
- AC5: `README.md:768-771` names the cut-scope case; `git diff main...HEAD -- CHANGELOG.md` adds 8 lines at the end of the existing Unreleased "A feature split across milestones reaches users as one change" entry, and `grep -cE '^\+- \*\*'` over that diff gives 0 new top-level entries.

Consistency gate: `cairn_validate` exit 0, all checks passed. `cairn_impact` skipped (Principles touched `—`, no principle changed). Profile slot: verify on the review head green (scripts 418 OK and hooks 179 OK after the claim-audit fixes; plugin and marketplace validate exit 0; plugin test 2076 tests, 0 fail); marketplace validate has no `plugins[N].version` warning; changelog: M276 is not a series member, and its user-visible change is described by the edit to the existing Unreleased series entry (the M275 precedent), no milestone number in it (`M<NNN>` is a placeholder). No CI on this repo.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: the implement exclusion for "a narrowed criterion's finding" can read as covering a review descope's remainder (a D-118-shaped case), so no marker is written — fix now: added "A review descope's remainder is work the Goal or Scope `In:` promised, so its row takes the marker.", fixed 93512655
- diff-bug #2: a guest cut milestone's PR gets no series sentence, since only the later milestone carries the line — follow-up, row "Cut series edges (M276 review)".
- diff-bug #3: a cut inside a planned series forks it into two lines with two last parts; a second cut drops the first part — follow-up, same row.
- diff-bug #4: a `/hotfix` before the later part is planned finds no series and adds a second entry — follow-up, same row.
- diff-bug #5: a milestone that absorbs a marked row only in part carries no line, and its started token hides the row from the release walk — follow-up, same row.
- diff-bug #6: the plan bullet still says no part is a candidate row — fix now: "(never a candidate row, except a cut series' unplanned part, below)", fixed 93512655
- diff-bug #7: `/milestone` §1 does not say it reads marked rows — follow-up, same row.
- diff-bug #8: the marker's place in the row was not pinned, so it could land in the short title — fix now: "The marker goes after the row's first `: `, so it stays out of the short title.", fixed 93512655
- diff-bug #9: a plain "split from M<n>" anywhere in a row reads as the marker — follow-up, same row.
- diff-bug #10: review step 4(a) names no marker, and a reviewer could create the split milestone directly — reject (false): the descope runs through `/milestone-implement` step 6, which states the marker, and only `/milestone-plan` writes milestone files; the frozen thrash fixture stays untouched.
- diff-bug #11: the CHANGELOG release sentence left out that the cut milestone must be done — fix now: "Once the cut milestone is done, …", fixed 93512655
- diff-bug #12: the "`/milestone-plan` then plans that milestone from it" clause had no guard — fix now: assertion extended, mutation entry added, fixed 93512655
- diff-bug #13: the test-file docstring still claims the one-line convention, and the new blocks are wrap-dependent — fix now for the docstring; reject (style) for the blocks, which follow the harness's physical-line convention used by every entry; docstring fixed 93512655
- blame-history #1: a row whose token names a done or dropped milestone is named as unplanned — reject (false): a dropped later part leaves the work unplanned, which is what the walk says; a done one's row leaves at that milestone's hygiene.
- blame-history #2: the plan bullet's "never a candidate row" — same as diff-bug #6, fixed.
- blame-history #3: the descope remainder and the follow-up exclusion collide — same as diff-bug #1, fixed.
- blame-history #4: planning a split milestone "from the row" duplicates a file that exists — reject (false): no milestone file exists at a cut, because only `/milestone-plan` writes one.
- blame-history #5: D-108's door on new conduct rules about records; no door check logged — reject (judgment, shown at the merge question): the deliverable is what a cut feature does to the changelog and the release walk, the same shipped-behavior trigger M274 and M275 passed under; the plan's collision check did not surface D-108.
- blame-history #6: the absorbed row's promotion trigger had not fired — reject (planned change): the user chose this row at the question set, told that its trigger had not fired.
- blame-history #7: a cut milestone's entry may already be released — follow-up, already the row "Series entry after a release (M276 plan)".
- prior-review #1: the cut milestone's guest PR gets no series sentence (M274 blame-history #3 pattern) — follow-up, row "Cut series edges (M276 review)".
- prior-review #2: the release leave-out ignores ` — started #<n>` tokens — reject (false): that token is written only in guest mode, where `/cairn-release` stops.
- prior-review #3: the leave-out relies on the later milestone's line; a plan writing the token without the line hides the series — follow-up, same row as diff-bug #5.

Return floor: no finding shows an acceptance criterion failing; diff-bug #1 was judged a wording gap that the added sentence closes, not a load-bearing defect (the paragraph already said "A review descope is one such amendment"), so no return. After the fixes: skills/tests 884 OK, scripts 418 OK, hooks 179 OK, plugin and marketplace validate exit 0, plugin test 0 fail.

PR-conversation read (PR #288, before the merge question): no issue comments; one Copilot review (COMMENTED, Bot, on 8d1620e6); one unresolved thread.
- copilot: cairn/milestones/M276-series-from-a-scope-cut.md:160 (work log says 18 mutation entries, the block has 21) — reject (false): the T1 line was accurate at its commit 706a7d3f; the claim-audit line records the three added later, and the work log is append-only. Replied and resolved.
- copilot: review body — noted (its one anchored finding is the thread above).
- Copilot level: unknown (the review body has no "Review effort" line; set by GitHub's settings).
