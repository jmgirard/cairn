<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M275: A feature series stays listed and keeps one entry until its last part ships

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what the release walk, hotfix, guest review, status snapshot, and templates tell every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A feature series stays visible to the release walk and the status snapshot until its last part ships, and a hotfix or a dropped part no longer breaks its one changelog entry or its guest PR sentence.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the four gaps of the candidate row "Feature series edges (M274 review)". (1) `/cairn-release` step 1 falls back to a part's archive summary when its ROADMAP row was pruned. (2) `/hotfix` edits a feature series' unreleased changelog entry instead of adding one, at step 5 and at the merged-PR re-entry's changelog clause. (3) `/milestone-review` step 8's last-part guest sentence names only the merged PRs of `done` earlier parts. (4) The milestone and archive-summary templates and `/milestone` §1 name the series. Guards in `skills/tests/test_feature_series.py` with mutation entries, and an edit to the existing CHANGELOG entry.

**Out:**
- A series that a review-time split creates → the candidate row "Feature series from a review-time split (M274 plan)".
- A hotfix to unreleased behavior outside a feature series → no record; the plan scoped the rule to series entries (work log).
- A scripted series listing in `cairn_status.py` or the cairn pane → no record; §1 applies the release rule in prose.
- Moving the half-merged rule into tracking-rules → no record; it stays in `/cairn-release` step 1 and `/milestone` cites it (work log).

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

- [ ] AC1: `skills/cairn-release/SKILL.md` step 1's "Half-merged feature series" rule reads each named milestone's status from its ROADMAP row, and for a milestone with no ROADMAP row from the Status line of its archive summary under `cairn/milestones/archive/`, both when it decides that a series is half-merged and when the question gives the status of each part that is not `done`; a named milestone with neither reads as unknown, and the question says so. `skills/tests/test_feature_series.py` asserts the archive-summary source and the unknown reading.
- [ ] AC2: `skills/hotfix/SKILL.md` step 5 and the merged-PR re-entry's *Changelog* clause say that when the bug is in behavior that a feature series' entry under the development version describes, the hotfix adds no new entry, and edits that entry only where the fix changes what it says. `skills/tests/test_feature_series.py` asserts the sentence at both sites.
- [ ] AC3: `skills/milestone-review/SKILL.md` step 8's sentence for a series' last milestone names by number the merged pull request of each earlier milestone that is `done`, and leaves out each `dropped` earlier milestone. `skills/tests/test_feature_series.py` asserts both clauses.
- [ ] AC4: `skills/shared/templates/milestone.md`'s work-log comment names the `feature series: M<a> -> M<b>[ -> …]` line and points at tracking-rules "Feature series"; `skills/shared/templates/archive-summary.md` tells the summary of a milestone whose work log carries that line to copy the line verbatim on its own line after the **Goal:** line; `skills/milestone/SKILL.md` §1 Snapshot, in owner mode, reports each half-merged feature series by applying the rule `/cairn-release` step 1 states, citing it by name without restating it. `skills/tests/test_feature_series.py` asserts each of the three.
- [ ] AC5: `CHANGELOG.md`'s existing Unreleased feature-series entry is edited to describe the release, hotfix, guest pull-request sentence, and status changes, and the Unreleased section still has exactly one entry that mentions `feature series`.
- [ ] AC6: The `verify` slot in `cairn/PROFILE.md` passes on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Edit `skills/cairn-release/SKILL.md` step 1 (~lines 58-64): status from the ROADMAP row, else the archive summary's Status line, else unknown, named in the question. Add the guards to `TestReleaseList` and a mutation entry in `skills/tests/test_mutation_harness.py` (~line 4828).
- [ ] T2: Edit `skills/hotfix/SKILL.md` step 5 (~line 265) and the re-entry *Changelog* clause (~lines 109-111): a series' unreleased entry is edited where the fix changes it, never duplicated. Say how the hotfix finds the series: a live milestone file or an archive summary carrying a `feature series:` line. Guards plus mutation entries.
- [ ] T3: Edit `skills/milestone-review/SKILL.md` step 8 (~lines 678-679): merged PRs of `done` earlier parts only, `dropped` parts left out. Guards in `TestReviewGuestSentence` plus a mutation entry.
- [ ] T4: Edit the milestone template's work-log comment, the archive-summary template (one optional line after **Goal:**, keeping summaries ≤ 25 lines), and `skills/milestone/SKILL.md` §1 (~line 58). Guards plus mutation entries. Template edits feed the gating suites, so run both after this task.
- [ ] T5: Edit the M274 entry in `CHANGELOG.md`'s Unreleased section; add no new entry. Check the README bullet at lines 765-767: it restates only the plan rule, which this milestone leaves alone, so log "no README edit" unless implement changes that.
- [ ] T6: Run the `verify` slot's five commands from the repo root, checking each exit code. Hand-run `python3 -m unittest discover -s skills/tests` (not a gate, D-109) and fix any red the edits caused.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: not run — work named at the question set.
- 2026-10-18: question set: what to plan — "Feature series edges" (user pick over the Haiku search re-test, the Opus effort measurement, and triage); runs per model — "na" (no measurement picked).
- 2026-10-18: collision: absorbs the candidate row "Feature series edges (M274 review)" in full (started token appended); "Feature series from a review-time split (M274 plan)" stays a separate row, named in Out; extends M274 (done); no D-entry heading names a feature series; inbox: 0 open issues, 0 open PRs.
- 2026-10-18: surface tier user-facing: skill prose and templates that adopting repos read.
- 2026-10-18: lessons applied: M112 (sweep README and CHANGELOG for restatements; CHANGELOG task present), M148/M171 (new prose near guarded slices; hand-run skills/tests), M56 line (template edits run both gating suites), M274 (no profile slot changes, so no `cairn/PROFILE.md` copy step).
- 2026-10-18: criteria audit (full, fresh Opus reader, run after the work was picked at the set): 12 findings, all fixed: AC1 gains the unknown reading; AC2 scoped to series entries, edit only where the fix changes the text, re-entry clause added; AC3 narrowed to merged PRs of `done` parts with `dropped` parts left out (removes the archive "no PR" form gap); AC4 cites the release rule without restating, owner mode only, line placed after **Goal:**; AC5 README clause dropped (grep missed line 767 and the bullet restates only the unchanged plan rule) and "one entry" made countable; AC6 hand-run clause dropped (D-109 keeps skills/tests non-gating; also an instrument property).
- 2026-10-18: plan gate chose a hotfix rule scoped to feature-series entries over a rule for every unreleased entry because the narrower promise was asked for and the audit flagged the wider one as beyond the series entry; falsified by a hotfix in a real repo adding a second entry for non-series behavior no release shipped.
- 2026-10-18: plan gate chose citing `/cairn-release` step 1's rule from `/milestone` §1 over moving it into tracking-rules "Feature series" because a rulebook edit re-seeds three mass pins (LESSONS M149) for two readers; falsified by a third skill needing the same rule.
- 2026-10-18: the four gaps share one feature and one test file, under the split tripwires (6 ACs, 6 tasks), so one milestone, no split.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->
