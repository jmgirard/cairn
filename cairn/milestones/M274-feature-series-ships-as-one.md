<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M274: A feature split across milestones reaches users as one change

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what the plan, review, release walk, and profile gates tell every adopting repo to do   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m274-feature-series-ships-as-one https://github.com/jmgirard/cairn/pull/286   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When a plan splits one user-facing feature or fix across several milestones, the feature reaches users, and the changelog, as one change.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a "feature series" rule in tracking-rules "Sizing and the work
tiers": earlier parts keep new behavior out of users' reach where they can,
the last part adds the exports, user docs, and changelog entry, and an
earlier part that must change visible behavior owns the one changelog entry
that later parts edit. The plan writes a series as such. The four profiles
whose consistency gate asks for a changelog entry accept an edit to the
series' entry, or no entry for a hidden earlier part. In guest mode, each
series PR body says in one plain sentence whether it completes the series.
In owner mode, `/cairn-release` step 1 names each half-merged series at the
version decision. README and CHANGELOG.

**Out:** a series formed later by a review-time split (the D-103 shape),
which no plan writes as a series → the candidate row "Feature series from a
review-time split (M274 plan)". Guest-mode stacking of more than one open
earlier part (D-173 allows one) → unchanged. The series rule names the limit.
Owner-mode PR bodies → unchanged, because the owner reads the ROADMAP.

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

- [x] AC1: `skills/shared/tracking-rules.md` "Sizing and the work tiers"
      defines a feature series as two or more milestones that one plan
      splits from one user-facing feature or fix, and states: (a) each
      milestone of the series but the last keeps its new behavior out of
      users' reach where it can, adding no export, user doc, or changelog
      entry; (b) each milestone but the last carries an `Out:` item naming
      the last milestone as where the feature's new exports and user docs
      land, and, unless (c) applies, its changelog entry; (c) when a
      milestone before the last must change user-visible behavior, its
      changelog entry is the feature's one entry, and each later milestone
      of the series edits that entry instead of adding one; (d) in guest
      mode a later part can build on at most one open earlier part (D-173),
      so a series of three or more waits on the maintainers' merges.
- [x] AC2: A `skills/milestone-plan/SKILL.md` step 4 bullet directs a plan
      that splits one user-facing feature or fix into several milestones to
      write them as a feature series under AC1's rules, and to write a
      `feature series: M<a> -> M<b>[ -> …]` work-log line in each milestone
      of the series.
- [x] AC3: In each profile that `git grep -l "has an entry for this"
      skills/shared/profiles/` lists on main before the change
      (`python.md`, `r-package.md`, `claude-plugin.md`, `docker-image.md`),
      that consistency-gate line states that a milestone of a feature series
      meets it with an edit to the series' existing entry, and that a
      milestone before the series' last with no user-visible change needs
      no entry.
- [x] AC4: `skills/milestone-review/SKILL.md` step 8's guest arm states
      that when the milestone's work log carries a `feature series:` line,
      the PR body adds one plain sentence with no cairn vocabulary: for a
      milestone before the series' last, that the change is one part of a
      series whose user-facing part comes in a later pull request; for the
      last, that it completes the series, naming each earlier milestone's
      pull request by number, read from its live milestone file's
      `Branch/PR` header or, for an archived milestone, from its archive
      summary's Status line.
- [x] AC5: `skills/cairn-release/SKILL.md` step 1 lists each feature
      series named by a `feature series:` line in a milestone file under
      `cairn/milestones/` (not `archive/`) where the line names at least one
      milestone whose ROADMAP status is `done`, and names those series in
      the version-decision question.
- [x] AC6: `CHANGELOG.md`'s Unreleased section has an entry describing
      AC1–AC5's rules.
- [x] AC7: The profile's `verify` slot passes on the branch head: both
      gating `python3 -m unittest` suites, `claude plugin validate` on the
      plugin and marketplace manifests, and `claude plugin test .`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T2, T6
- AC3 → T3, T6
- AC4 → T4, T6
- AC5 → T5, T6
- AC6 → T7
- AC7 → T8

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: tracking-rules "Sizing and the work tiers" (~line 187): one
      paragraph after the split tripwires defining a feature series and its
      rules (a)–(d). Keep the word "chain" out (stacking uses it).
- [x] T2: `skills/milestone-plan/SKILL.md` step 4: one bullet for a split
      of one feature into a series, with the `feature series:` line.
- [x] T3: the four profiles' consistency-gate changelog line.
- [x] T4: `skills/milestone-review/SKILL.md` step 8 guest arm (~line 660):
      the series sentence and where the earlier PR numbers are read.
- [x] T5: `skills/cairn-release/SKILL.md` step 1: the half-merged series
      list and its place in the version-decision question.
- [x] T6: tests first in a new `skills/tests/test_feature_series.py`: one
      guard per AC1–AC5 clause, each with a mutation-registry entry
      (`skills/tests/test_mutation_harness.py`). Hand-run `skills/tests`.
- [x] T7: CHANGELOG Unreleased entry (AC6); grep README and `skills/` for
      text restating one changelog entry per milestone and update it. Read
      each claim against T1–T5's text.
- [x] T8: Run the `verify` slot on the code head and record each exit code.

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
- 2026-10-18: tier check: milestone — changes skill and profile conduct for every adopter and needs a design choice.
- 2026-10-18: question set: owner-mode release warning for a half-merged series — yes (AC5); firmness of hiding earlier parts — prefer, with the changelog-entry fallback (AC1 (a), (c)).
- 2026-10-18: surface tier user-facing — the plan, review, release, and profile rules are what adopting repos follow.
- 2026-10-18: collision check: extends tracking-rules "every milestone leaves the default branch shippable" (Sizing); no D-entry rejects it; works under D-040 (changelog slot), D-050 (release timing stays user-declared, AC5 only informs), D-137 and D-161 (guest PR text carries no cairn vocabulary and matches the host), D-173 (one stack base). Not the checker-regress shape. Inbox: 0 open issues, 0 open PRs.
- 2026-10-18: lessons surfaced: grep the old phrasing and own a CHANGELOG task (M112, M249); hand-run `skills/tests` near edited SKILL.md slices.
- 2026-10-18: plan gate chose an `Out:` item plus a `feature series:` work-log line to mark a series over a new milestone-file header slot, because both use existing places and no validator needs to parse them; falsified by a session where review or release misses a series whose files carry the line.
- 2026-10-18: plan gate chose prose rules and prose guards over a validator that checks series membership, at the user's ask for proportional rigor; falsified by a release that ships a half-built series a validator would have flagged.
- 2026-10-18: criteria audit (full mode, fresh Opus reader) returned 5 findings, all fixed: AC1's Out rule allows for rule (c); "chain" renamed "feature series" (stacking already uses "chain"), with the guest one-stack-base limit as rule (d); AC2 names a step 4 bullet, not a nonexistent list, and the line uses ASCII `->`; AC4 reads earlier PR numbers from archive Status lines too; AC5 claims only series named by a live milestone file. AC3 and AC6 clean.
- 2026-10-18: split: none; 7 criteria, 8 tasks. The review-time-split remainder goes to the candidate row "Feature series from a review-time split (M274 plan)".
- 2026-10-18: branch m274-feature-series-ships-as-one cut from origin/main at e4eb7db2; untracked `cairn-probe.log` and `tsconfig.json` are not milestone work and stay unstaged.
- 2026-10-18: T1–T5: prose edits in tracking-rules (Sizing, new "Feature series" paragraph), milestone-plan step 4 bullet, the four profiles' changelog gate lines, milestone-review step 8 guest arm, cairn-release step 1. Implementation choice: each rule clause sits on its own source line so the prose guards can match it whole.
- 2026-10-18: T6: `skills/tests/test_feature_series.py` (14 tests) and 23 mutation-registry entries; written after the T1–T5 text in one pass rather than before it, a deviation from tests-first; the mutation harness shows each guard fails when its line is blanked. `skills/tests` 856 green.
- 2026-10-18: T7: CHANGELOG Unreleased entry; README tips gain one sentence on feature series. Grep of README and skills for per-milestone changelog wording found only `/hotfix` lines, which a series does not cover.
- 2026-10-18: T8: verify on the code head: scripts 0 (418 tests, OK, 21 skipped), hooks 0, plugin validate 0 (passed with warnings), marketplace validate 0, plugin test 0 (2076 tests, 0 fail); cairn_validate all checks passed. Checkpoint is one commit for T1–T8, not one per task.
- 2026-10-18: claim audit: 38 claims read, 0 corrected — CHANGELOG.md, README.md, skills/shared/tracking-rules.md, skills/milestone-plan/SKILL.md, skills/shared/profiles/{python,r-package,claude-plugin,docker-image}.md, skills/milestone-review/SKILL.md, skills/cairn-release/SKILL.md, skills/tests/test_feature_series.py, skills/tests/test_mutation_harness.py
- 2026-10-18: status review; handed to /milestone-review.
- 2026-10-18: step-7 approval: m274-feature-series-ships-as-one approved for merge

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

- AC1: tracking-rules "Sizing and the work tiers" holds the "Feature series" paragraph with the definition and rules (a)–(d) (awk over the section, 5 clause lines found; `TestRulebookParagraph`, 10 guards, green). (b) reworded at review so the "unless (c)" clause plainly names where the changelog entry lands.
- AC2: milestone-plan step 4 carries the "Feature series" bullet and the `feature series: M<a> -> M<b>[ -> …]` line (grep within step 4: 2 hits; `TestPlanBullet` green).
- AC3: `git grep -l "has an entry for this" main -- skills/shared/profiles/` lists claude-plugin, docker-image, python, r-package; each carries the edit and no-entry sentences (2 hits per file; `TestProfileGates` green).
- AC4: milestone-review step 8 guest arm carries the trigger, earlier-part, last-part, and read-source sentences (grep: 3 hits; `TestReviewGuestSentence` green).
- AC5: cairn-release step 1 lists the series from live milestone files whose line names a `done` milestone, and the question names them (grep within step 1: 3 hits; `TestReleaseList` green).
- AC6: CHANGELOG `## Unreleased` opens with "A feature split across milestones reaches users as one change." (line 5).
- AC7: verify on head 181fdad6: scripts 0 (OK, 21 skipped), hooks 0 (OK), plugin validate 0 (passed with warnings), marketplace validate 0, plugin test 0 (2076 tests, 0 fail). `skills/tests` 861 green (hand-run). cairn_validate all checks passed.
- Consistency gate: cairn_validate exit 0; no principle changed, so no cairn_impact run; claude-plugin consistency-gate: changelog entry present (AC6).
- spawned: diff-bug, blame-history, prior-review.
- prior-review #1: the rulebook-mass baseline in `/milestone` (719 lines / 69,644 bytes) went stale when the rulebook grew, the M159/M166 pattern — fix now, re-seeded to 733 lines / 70,960 bytes in skills/milestone/SKILL.md, test_cost_audit_line.py, and its mutation entry, fixed 1f1315e0 and 181fdad6.
- prior-review #2: the CHANGELOG shows `M<a> -> M<b>` — reject (false: placeholders, not milestone numbers).
- blame-history #1: rule (b) reads as earlier parts carrying an entry — reject (false: the clause named where the entry lands); the wording was still clarified for Copilot's same reading, fixed 181fdad6.
- blame-history #2: the profile edit line leaves no path when no entry exists yet — fix now, "This holds where the series already has an entry", fixed 1f1315e0.
- blame-history #3: the guest earlier-part sentence is false under rule (c) — fix now, added "Under rule (c) it says the rest of the user-facing part comes later.", fixed 1f1315e0.
- blame-history #4: (d) contradicts D-173 for a linear chain — reject (false: a middle part's PR is stacked, and implement refuses a stacked stack base, so a third part waits).
- blame-history #5: the hidden-part exemption has no check — reject (planned change: prose rules over a validator, chosen at the plan gate).
- blame-history #6: the release question does not handle a dropped part — fix now, the question gives each part's ROADMAP status, fixed 1f1315e0.
- blame-history #7: reading a PR number from the header URL is unstated — reject (style: no instruction needed).
- diff-bug #1: the profile change does not reach an existing repo's `cairn/PROFILE.md` copy, which review reads — fix now: CHANGELOG tells existing repos to copy the sentences, and this repo's `cairn/PROFILE.md` carries them, fixed 1f1315e0.
- diff-bug #2: (d) misses guest mode without `# Push remote: base` — fix now, added the no-push-remote sentence, fixed 1f1315e0.
- diff-bug #3: a later part held as a candidate row breaks the series — fix now, the plan bullet says every part is a milestone file, fixed 1f1315e0.
- diff-bug #4: a pruned `done` row hides a half-merged series from the release list — follow-up, "Feature series edges (M274 review)".
- diff-bug #5: an all-`done` series with a live file would be listed — reject (false: the live file's own milestone is named by its line and is not `done` until hygiene archives it).
- diff-bug #6: two earlier visible parts give two owners for the one entry — reject (false: the second is a later milestone relative to the first, so (c) has it edit).
- diff-bug #7: same as blame-history #3 — fix now, fixed 1f1315e0.
- diff-bug #8: the plan bullet dropped "but the last" — fix now, fixed 1f1315e0.
- diff-bug #9: guards skip some clauses — fix now, guards added for (a)'s obligation, (c)'s first line, the internal-layer and no-push-remote lines, the review trigger, the release lead and status lines, and the profile membership line, each with a mutation entry, fixed 1f1315e0.
- diff-bug #10: profile and review guards read the whole file, not the section — reject (style: the repo's guards use whole-file reads where the phrase is unique).
- diff-bug #11: a hidden part is not a vertical slice — fix now, added "Such a part can be an internal layer rather than a vertical slice", fixed 1f1315e0.
- diff-bug #12: a hotfix to unreleased series behavior adds its own entry — follow-up, "Feature series edges (M274 review)".
- diff-bug #13: the profile line does not say how membership is known — fix now, names the `feature series:` line, fixed 1f1315e0.
- diff-bug #14: a dropped earlier part may have no PR number — follow-up, "Feature series edges (M274 review)".
- diff-bug #15: template, archive summary, and `/milestone` do not mention a series — follow-up, "Feature series edges (M274 review)".
- diff-bug #16: long unwrapped lines — reject (style).
- diff-bug #17: tests after prose and one checkpoint commit — noted (recorded in the work log).
- copilot: skills/cairn-release/SKILL.md:61 — reject (the live file's milestone is not done, so a listed series always has an unfinished part); replied and resolved.
- copilot: skills/shared/profiles/claude-plugin.md:56, docker-image.md:43, python.md:36, r-package.md:31 — fix now, fixed 1f1315e0; replied and resolved.
- copilot: skills/shared/tracking-rules.md:198 — fix now, fixed 181fdad6; replied and resolved.
- Copilot level: Lite (set by GitHub's settings).
- conversation: jmgirard PR #286 — noted (six reply reviews this run posted on Copilot threads); no issue comments; 0 unresolved threads.
