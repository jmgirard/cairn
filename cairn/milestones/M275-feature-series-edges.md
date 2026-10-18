<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M275: A feature series stays listed and keeps one entry until its last part ships

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what the release walk, hotfix, guest review, status snapshot, and templates tell every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m275-feature-series-edges, https://github.com/jmgirard/cairn/pull/287   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: `skills/cairn-release/SKILL.md` step 1's "Half-merged feature series" rule reads each named milestone's status from its ROADMAP row, and for a milestone with no ROADMAP row from the Status line of its archive summary under `cairn/milestones/archive/`, both when it decides that a series is half-merged and when the question gives the status of each part that is not `done`; a named milestone with neither reads as unknown, and the question says so. `skills/tests/test_feature_series.py` asserts the archive-summary source and the unknown reading.
- [x] AC2: `skills/hotfix/SKILL.md` step 5 and the merged-PR re-entry's *Changelog* clause say that when the bug is in behavior that a feature series' entry under the development version describes, the hotfix adds no new entry, and edits that entry only where the fix changes what it says. `skills/tests/test_feature_series.py` asserts the sentence at both sites.
- [x] AC3: `skills/milestone-review/SKILL.md` step 8's sentence for a series' last milestone names by number the merged pull request of each earlier milestone that is `done`, and leaves out each `dropped` earlier milestone. `skills/tests/test_feature_series.py` asserts both clauses.
- [x] AC4: `skills/shared/templates/milestone.md`'s work-log comment names the `feature series: M<a> -> M<b>[ -> …]` line and points at tracking-rules "Feature series"; `skills/shared/templates/archive-summary.md` tells the summary of a milestone whose work log carries that line to copy the line verbatim on its own line after the **Goal:** line; `skills/milestone/SKILL.md` §1 Snapshot, in owner mode, reports each half-merged feature series by applying the rule `/cairn-release` step 1 states, citing it by name without restating it. `skills/tests/test_feature_series.py` asserts each of the three.
- [x] AC5: `CHANGELOG.md`'s existing Unreleased feature-series entry is edited to describe the release, hotfix, guest pull-request sentence, and status changes, and the Unreleased section still has exactly one entry that mentions `feature series`.
- [x] AC6: The `verify` slot in `cairn/PROFILE.md` passes on the review head.

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

- [x] T1: Edit `skills/cairn-release/SKILL.md` step 1 (~lines 58-64): status from the ROADMAP row, else the archive summary's Status line, else unknown, named in the question. Add the guards to `TestReleaseList` and a mutation entry in `skills/tests/test_mutation_harness.py` (~line 4828).
- [x] T2: Edit `skills/hotfix/SKILL.md` step 5 (~line 265) and the re-entry *Changelog* clause (~lines 109-111): a series' unreleased entry is edited where the fix changes it, never duplicated. Say how the hotfix finds the series: a live milestone file or an archive summary carrying a `feature series:` line. Guards plus mutation entries.
- [x] T3: Edit `skills/milestone-review/SKILL.md` step 8 (~lines 678-679): merged PRs of `done` earlier parts only, `dropped` parts left out. Guards in `TestReviewGuestSentence` plus a mutation entry.
- [x] T4: Edit the milestone template's work-log comment, the archive-summary template (one optional line after **Goal:**, keeping summaries ≤ 25 lines), and `skills/milestone/SKILL.md` §1 (~line 58). Guards plus mutation entries. Template edits feed the gating suites, so run both after this task.
- [x] T5: Edit the M274 entry in `CHANGELOG.md`'s Unreleased section; add no new entry. Check the README bullet at lines 765-767: it restates only the plan rule, which this milestone leaves alone, so log "no README edit" unless implement changes that.
- [x] T6: Run the `verify` slot's five commands from the repo root, checking each exit code. Hand-run `python3 -m unittest discover -s skills/tests` (not a gate, D-109) and fix any red the edits caused.

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
- 2026-10-18: implement started on branch m275-feature-series-edges; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-18: T1 done: release step 1 reads status from the ROADMAP row, else the archive summary's Status line, else unknown; 2 new guards, 1 updated, 3 mutation entries; verify green. The simple-english lint hook flags 67 older hits in the release skill; only the new lines were fitted to it (rewriting the file is out of scope).
- 2026-10-18: T2 done: hotfix step 5 and the re-entry Changelog clause keep a feature series' one unreleased entry, edited only where the fix changes it; step 5 says to find the series from `feature series:` lines in live files and archive summaries; 3 guards, 5 mutation entries; verify green.
- 2026-10-18: T3 done: review step 8's last-part sentence names merged PRs of `done` earlier parts and leaves out `dropped` ones; the long sentence was split, so the existing guard and its two mutation entries were updated, 1 guard and 1 entry added; verify green.
- 2026-10-18: T4 done: milestone template work-log comment names the series line; archive-summary template gains a placeholder line after **Goal:** (template now 22 lines, under the 25-line summary cap); `/milestone` §1 cites the release rule in owner mode; 3 guards, 3 mutation entries; verify green, both gating suites included.
- 2026-10-18: T5 done: the M274 Unreleased entry now covers the guest sentence, the status snapshot, the archive fallback, and the hotfix rule; a whitespace-normalized split of the Unreleased section finds 1 of 60 entries mentioning `feature series`; no README edit (lines 763-768 restate only the unchanged plan rule).
- 2026-10-18: T6 done: verify slot's five commands exit 0; hand-run skills/tests first red (1 error: T1 left a stale M274 mutation entry on the rewritten release sentence, "found 0"), entry removed since T1's entry covers the new sentence, then 870 tests OK; every new mutation entry blanks red.
- 2026-10-18: claim audit: 56 claims read, 4 corrected — skills/milestone-review/SKILL.md (dropped-part reason narrower than the rule), skills/tests/test_feature_series.py (stale docstring), skills/hotfix/SKILL.md (adopting-a-PR clause still ordered a second entry; *Nothing owed* missed the no-edit series case); same reader re-read all 4 as holding; its two slips after the re-read (docstring wording, adopting sentence lacking "under the development version") fixed by the author, 2 guards and 2 mutation entries added; verify green, skills/tests 872 OK.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review

Pass 1, 2026-10-18, head 0c845eaa (PR #287; Copilot requested at review start, state was `none`).

- AC1: `skills/cairn-release/SKILL.md:61-67` — the half-merged test reads "whose status is `done`", status defined as the ROADMAP row's, else the archive summary's Status line (63), else unknown (65), and the question gives each non-`done` part's status with unknown named (67); `TestReleaseList` OK (5 tests, archive-summary and unknown guards included).
- AC2: `skills/hotfix/SKILL.md:274-275` (step 5: no new entry, edit only where the fix changes what the entry says) and `:112-113` (re-entry *Changelog* clause: owes no new entry, an edit only where the fix changes it); also the adopting clause `:294-295` and *Nothing owed* `:127`; `TestHotfixSeriesEntry` OK (5 tests, both sites asserted).
- AC3: `skills/milestone-review/SKILL.md:678` names "the merged pull request of each earlier milestone that is `done`", `:680` "leaves out each `dropped` earlier milestone"; `TestReviewGuestSentence` OK (both clauses asserted).
- AC4: `skills/shared/templates/milestone.md:76-77` names the `feature series: M<a> -> M<b>[ -> …]` line and tracking-rules "Feature series"; `skills/shared/templates/archive-summary.md:10` says to copy the line verbatim on its own line after **Goal:**; `skills/milestone/SKILL.md:64` (§1) reports half-merged series in owner mode by citing `/cairn-release` step 1's "Half-merged feature series" rule, not restating it; `TestSeriesNamedElsewhere` OK (3 tests).
- AC5: `CHANGELOG.md` Unreleased: a whitespace-normalized split into entries finds 60 entries, 1 mentioning `feature series` (the M274 entry); that entry now contains the dropped-part, status-snapshot, archive-summary, and hotfix clauses (substring checks all true).
- AC6: verify slot on head 0c845eaa: `scripts/tests`, `hooks/tests`, both `claude plugin validate`, and `claude plugin test .` each exit 0.
- Consistency gate: `cairn_validate.py` all checks passed; no principle text changed, so no `cairn_impact` run; marketplace validate prints no `version` warning; changelog gate met by the edit to the series' entry; hand-run `skills/tests` 872 OK (not a gate, D-109).
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the last-part guest sentence leaves out a `blocked` earlier part (an open stack base, or one merged before hygiene) whose PR the old text named — fix now (it now also names each `blocked` part's PR), fixed fa38b75a.
- diff-bug #2: step 8 names no status source for "is `done`", so a pruned row hides a part — fix now (cites the release rule's ROADMAP-then-archive source), fixed fa38b75a.
- diff-bug #3: `/milestone` §1 cites the release rule but its reads cannot reach every live file and the archive — fix now (names the release skill path, every live milestone file, and the archive summaries), fixed fa38b75a.
- diff-bug #4: the re-entry route keeps a separate series entry the merged diff added — fix now (its removal is owed), fixed fa38b75a.
- diff-bug #5: "no release shipped that behavior" is wrong for a series that changes released behavior — fix now (a bug in behavior an earlier release shipped takes its own entry; CHANGELOG says so), fixed fa38b75a.
- diff-bug #6: a live file with no ROADMAP row reads as unknown — reject (false: `cairn_validate`'s roadmap-disk orphans check fails on that drift, so the state cannot stand).
- diff-bug #7: no mutation entry for "A named milestone's status is the status in its ROADMAP row." — fix now (entry added), fixed fa38b75a.
- diff-bug #8: "copy that line verbatim" would carry the work-log date and bullet — fix now (copy the `feature series: …` text, leaving out the date and bullet), fixed fa38b75a.
- diff-bug #9: "Status line" against the rulebook's Status paragraph — reject (false: the template puts the status word and `PR #<N>` on the paragraph's first line).
- diff-bug #10: the approval gate and the re-land fallback ignore the series rule — fix now (both name it), fixed fa38b75a.
- diff-bug #11: new lines run unwrapped — reject (planned change: asserted phrases sit on one source line by the M23 guard convention, as M274's lines do).
- blame-history #1: archive summaries before M275 lack the series line, so a hotfix misses an older series — reject (false: the series rule shipped in M274 today and no archive or work log names a series, which prior-review #4 checked).
- blame-history #2: same as diff-bug #1 — fix now, fixed fa38b75a.
- blame-history #3: *Nothing owed* passes a series bug whose fix changes the entry — reject (false: an entry that "already describes the fixed behavior" needs no change by definition; a fix that changes it fails the condition).
- blame-history #4: the adopted-PR path drops a contributor's entry and its credit — fix now (credit kept in the series' entry); the step-6 chip still gates the PR, fixed fa38b75a.
- blame-history #5: D-131's changelog check is relaxed with no D-entry — reject (false: D-131's check still runs; the series rule only defines what satisfies it, as M274's profile gates did with no D-entry).
- prior-review #1: the release predicate "at least one `done`" that Copilot flagged on PR #286 — reject (planned change: unchanged; the M274 premise holds because hygiene archives a `done` file, so a live carrying file is an unfinished part).
- prior-review #2: new CHANGELOG clauses have no guard, against M274 diff-bug #9 — reject (false: M274 #9 asked for skill-prose guards, and each clause's behavior has its skill-prose guard in `test_feature_series.py`).
- prior-review #3: step 8 states no status source or unknown case — fix now with diff-bug #2; an unknown part has no file and so no PR to name, fixed fa38b75a.
- prior-review #4: same as blame-history #1 — reject (same ground).
- copilot: cairn/milestones/M275-feature-series-edges.md:14 — the header named only the branch at the reviewed commit 61f570ed — fix now (already fixed: the header names PR #287 since 0c845eaa), replied and resolved, fixed 0c845eaa.
- copilot: review body — "merged-PR duplicate cleanup" and "the missing primary ROADMAP mutation guard" (no thread anchor) — fix now, the same items as diff-bug #4 and #7, fixed fa38b75a.
- copilot: review body overview and file table — noted.
- Copilot level: Lite (set by GitHub's settings); its one review covered 61f570ed, before the review fixes.
- PR conversation: no human reviews, no conversation comments, 1 Copilot thread (above); no `CHANGES_REQUESTED` review.
- Post-fix: verify slot five commands exit 0; hand-run `skills/tests` 877 OK, every new mutation entry blanks red.
