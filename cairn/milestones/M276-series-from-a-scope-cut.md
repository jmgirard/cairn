<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M276: A feature cut short at implement or review still ships as one change

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what implement, plan, and the release walk tell every adopting repo to do when a milestone's scope is cut   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: The tracking-rules "Feature series" paragraph states that a
      series also forms when a substantive amendment of a user-facing
      milestone, at implement or executing a review descope, moves work
      that milestone's Goal or Scope `In:` promised to later work: the cut
      milestone and the milestone later planned for that work are the
      series. It also states that rules (a) and (b) do not bind the cut
      milestone, that the cut milestone's changelog entry, where it has one,
      is the series' one entry under rule (c), and that only the later
      milestone carries the `feature series:` line.
- [ ] AC2: `/milestone-implement` step 6 states that such an amendment
      records the moved work as a candidate row whose text carries
      `split from M<NNN>`, naming the amended milestone, also when the
      work's home is a split milestone, and that neither a follow-up row
      for a narrowed criterion's finding nor a remainder row of an
      internal-tier milestone carries the marker.
- [ ] AC3: `/milestone-plan` step 4's Feature series bullet states that a
      milestone the plan creates from a candidate row carrying
      `split from M<NNN>` gets the work-log line
      `feature series: M<NNN> -> M<new>`.
- [ ] AC4: `/cairn-release` step 1's "Half-merged feature series" paragraph
      states that the version-decision question also names each row of
      `cairn/ROADMAP.md`'s Candidates section whose text carries
      `split from M<NNN>` where M<NNN>'s status, read by that paragraph's
      status rule, is `done`, as an unplanned part of M<NNN>'s feature.
- [ ] AC5: README's feature-series tip names the cut-scope case. The
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

- [ ] T1: Guards first. In `skills/tests/test_feature_series.py`, add one
      test per sentence AC1–AC4 name, each with its own entry in
      `skills/tests/test_mutation_harness.py`; see each red before its prose
      lands. Update the existing `TestRulebookParagraph` pins and their
      mutation entries where T2 rewords pinned text.
- [ ] T2: tracking-rules "Feature series" (`skills/shared/tracking-rules.md:192-204`):
      the cut-scope sentences (AC1), including the exception to "The plan
      writes … in each milestone of the series". Re-seed the rulebook-mass
      baseline in its three places
      (`skills/milestone/SKILL.md:120`,
      `skills/tests/test_cost_audit_line.py:69`,
      `skills/tests/test_mutation_harness.py:121`).
- [ ] T3: `/milestone-implement` step 6, beside the return-adjacent
      direction rule (`skills/milestone-implement/SKILL.md:214-226`): the
      `split from M<NNN>` marker sentence (AC2).
- [ ] T4: `/milestone-plan` step 4's Feature series bullet
      (`skills/milestone-plan/SKILL.md:490-497`): the series line for a
      marked row (AC3).
- [ ] T5: `/cairn-release` step 1, "Half-merged feature series"
      (`skills/cairn-release/SKILL.md:58-68`): marked rows (AC4).
- [ ] T6: README tip (`README.md:763-768`) and the CHANGELOG's Unreleased
      feature-series entry, edited in place (AC5).
- [ ] T7: Run the `verify` slot (both gating suites, `claude plugin
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
