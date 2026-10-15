<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M251: One short-title rule for candidate rows

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters see the cairn pane, and their agents follow the rulebook when they write rows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m251-candidate-short-title, https://github.com/jmgirard/cairn/pull/262   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A candidate row's short title, which the pane shows and the skills quote, has one written rule that tells row writers how to form it.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The rule. A row's short title is its text after `- ` and any
`[high] ` or `[low] ` token, up to the first `: `. A row with no `: ` is cut
at its first ` — ` (space, em dash, space). A row with neither is all of
that text. Outer spaces are removed. The rule goes into the pane reader, its
Python test twin, the rulebook, and each skill that names a row by its
title. A rulebook paragraph tells writers to open each row with a few words
that name it, then `: `. `/cairn-triage` gains a disposition that rewords a
long or shared short title.

**Out:** Cutting at `. ` or guessing an area prefix (rejected at the plan
gate, see the work log). Rewording glmmTMB's rows (the glmmTMB session does
that once this merges). A `cairn_validate` check on titles (not chosen at
the plan gate). The other edges of "Amendment-return and linked-row edge
cases (M211 review)" stay in that row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets (tracking-rules section ownership) -->

- [x] AC1: `candidateRows` in `hooks/status/reader.ts` and `python_candidates`
      in `scripts/tests/test_status_fixtures.py` return the short title in the
      right column for each row text in the left column (checked by the
      `candidates` fixture and `hooks/status/reader.test.ts`). Both gating
      suites and `claude plugin test` pass.

      | Row text after `- ` | Short title |
      |---|---|
      | `ordinal: REML. The fit warns — added 2026-10-01` | `ordinal` |
      | ``loglog link for `binomial`. Needs a case — added 2026-10-15`` | ``loglog link for `binomial`. Needs a case`` |
      | `Title — detail: more — added 2026-01-01` | `Title — detail` |
      | `[low] Low row — added 2026-01-02` | `Low row` |
      | ``A `a — b` dash in backticks — added 2026-01-03`` | ``A `a`` |
      | `A row with no colon and no dash` | `A row with no colon and no dash` |
      | `: an empty short title — added 2026-01-04` | (empty) |

- [x] AC2: `skills/shared/tracking-rules.md` states the rule in one
      "Candidate short title" paragraph beside "Candidate priority token". The
      paragraph says that the pane shows the short title and that the skills
      name a row by it. It tells a writer to open each row with a few words
      that name the row and differ from every other row's title, then `: `
      and the detail. It says that an area word joins the title
      (`ordinal REML: ...`, not `ordinal: REML. ...`). A new `DECISIONS.md`
      entry whose heading names D-149 narrows D-149's title sentence to this
      rule.
- [x] AC3: records-hygiene §7, `/hotfix` step 1, `/cairn-triage` step 1's
      subject, the `/milestone` health audit's §7 sentence, and
      `/milestone-review` step 9's row-filing sentence cite that paragraph and
      state no title rule of their own. The branch runs one sweep:
      `git grep -n -i -e "first \`: \`" -e "first colon" -e "short title" -e "title's \`: \`" -e "exact title"`
      over `skills`, `README.md`, `cairn/DESIGN.md`, `hooks`, and `scripts`.
      Each hit agrees with the rule.
- [x] AC4: The `/cairn-init` ROADMAP skeleton comment in
      `skills/cairn-init/SKILL.md` and the row example in the "Candidate
      priority token" paragraph show the shape
      `- [high] short title: detail — added YYYY-MM-DD — links`.
- [x] AC5: `/cairn-triage` has a `retitle` disposition. It is proposed for
      each candidate row that the other evidence classes leave `keep`, other
      than a `merge` survivor, a finding-absorbing row, or a row a live
      milestone absorbs or quotes, whose short title is empty, is over 60
      code points, or is shared with another row (each such row gets its own
      proposal), whatever the row's byte length. It inserts a short title
      ending at `: ` after the row's `- ` and any priority token and leaves
      the row's text unchanged (a row whose title is empty loses only its
      leading `: `). Its accepted edit also rewrites each double-quoted
      mention of the old title, found by a search of `cairn/ROADMAP.md` and
      DESIGN.md's Known issues, in another ROADMAP row the pass does not
      remove. A mention of a shared title is listed as ambiguous and is not
      rewritten.
- [x] AC6: README's cairn pane section and DESIGN.md's `candidateRows`
      description state the rule. `CHANGELOG.md`'s Unreleased section says
      that a row with no `: ` now loses its date and links from its pane
      title, names the writing rule and `retitle`, and says that an old quote
      of such a row's whole text no longer matches its title.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T2
- AC5 → T4, T6
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first. Add AC1's rows to `hooks/status/fixtures/candidates/`
      and its `expected.json`, and restate the old "shown whole" rows, which
      now cut at their dash. Add the table to `reader.test.ts`. Update the
      `TITLES` list, `EMPTY_AT`, `SAME_AT`, and the ✎-count assertions in
      `pane.test.tsx` (~line 1395-1420) for the shifted indexes, or keep the
      empty-title row out of the shared fixture. See the new cases fail.
      Then change `candidateRows` (`reader.ts:543-566`) and
      `python_candidates`, with their comments. Regenerate `fixtures.gen.ts`
      with `hooks/status/gen_fixtures.py`. Run both gating suites and
      `claude plugin test`.
- [x] T2: Write the "Candidate short title" paragraph after "Candidate
      priority token" (`tracking-rules.md:209`) and change that paragraph's
      row example. Change the skeleton comment in
      `skills/cairn-init/SKILL.md` (~line 190). Append the D-entry that
      narrows D-149.
- [x] T3: Make records-hygiene §7 (line 36), `/hotfix` step 1 (line 51),
      `/cairn-triage` step 1 (line 63), `/milestone` (line 139), and
      `/milestone-review` step 9 (line 710) cite the paragraph. Update the pin
      in `skills/tests/test_hotfix_candidate_graduation.py:53` and hand-run
      `skills/tests`. Run AC3's sweep and fix each hit.
- [x] T4: Add `retitle` to `/cairn-triage`'s disposition table, its evidence
      classes, and its apply step, with the ROADMAP quote rewrite and the
      live-milestone exclusion.
- [x] T5: Update README's pane section (~line 314), DESIGN.md (~line 285),
      and `CHANGELOG.md`.
- [x] T6: Review return 1: `retitle` puts the new title before the row's
      text and keeps the token and provenance; apply the other fix-now
      findings the Review section lists.

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

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — `/hotfix` found the work over the hotfix bar earlier this session (the reader matches the documented rule, and changing it is a design decision).
- 2026-10-15: reported by the glmmTMB session: 8 glmmTMB rows written `ordinal: topic. detail` show only `ordinal` in the pane.
- 2026-10-15: investigation: across 25 local cairn repos, 447 of 625 candidate rows have a pane title over 60 characters under the current rule; cutting at the earliest of `: `, `. `, and the em dash leaves 381.
- 2026-10-15: collision check: D-149 defines the title as the text before the first `: ` (narrowed by AC2's D-entry); D-134 and D-035 are not affected; M207 and M242 shipped the reader and the ✎ press; no open issue or PR overlaps (gh, 0 and 0).
- 2026-10-15: absorbs the "a row with no `: ` has no title" part of the candidate row "Amendment-return and linked-row edge cases (M211 review)"; post-merge hygiene narrows that row.
- 2026-10-15: plan gate chose the first `: `, else the first em dash, over the earliest of `: `, `. `, and the em dash, because `. ` cuts at abbreviations such as "e.g." and changes 383 titles in other repos; falsified by writers who follow the rule still ending titles at `. ` in real rows.
- 2026-10-15: plan gate chose no area-prefix guess over keeping a one-word prefix, because every reader of the title would have to copy the guess; falsified by area-prefix rows that persist after the writing rule ships.
- 2026-10-15: plan gate chose a `/cairn-triage` `retitle` disposition over a `cairn_validate` advisory and over no route for old rows.
- 2026-10-15: agent chose a new `retitle` disposition over a `compress` variant, because `compress` fires on byte length and rewrites the body, while a title change must also rewrite quotes.
- 2026-10-15: agent chose no length cap in the reader, because the pane already cuts a long title to one line with an ellipsis.
- 2026-10-15: criteria audit (full mode, fresh Opus reader) ran twice. Pass 1 on the draft: 8 findings (missing probe axes, `. ` abbreviations, shared titles, compress breaking quotes, two missed citing sites and a work-log escape in AC3, no AC for the D-149 narrowing, no migration note, the `pane.test.tsx` list); all fixed or made moot by the gate's choice. Pass 2 on the revised criteria: 5 findings (who gets a shared-title retitle, live milestone files are plan-owned, T3's log escape, AC1's fixture clause, `EMPTY_AT`/`SAME_AT` index shifts); all 5 fixed by narrowing AC1, AC3, AC5, T1, T3, and T4.
- 2026-10-15: implement started on m251-candidate-short-title; untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-15: T1 done: AC1's table in `reader.test.ts` and the `candidates` fixture (6 rows; the empty-title row stays in reader.test.ts and pane.test.tsx's own extra rows), old "shown whole" rows reworded, `mixed` and `single-in-progress` expected titles lose their dash tail; 3 TS cases and the fixture checks failed before the reader change; after it, both suites, both validates, and `claude plugin test` (1714 pass) are green.
- 2026-10-15: T2 done: tracking-rules "Candidate short title" paragraph and the token example's new shape, the `/cairn-init` skeleton comment, D-163 narrowing D-149's title sentence; rulebook baseline re-seeded to 663 lines / 63,632 bytes at its three sites (`/milestone` and two hand-run pins); the skeleton pin and its mutation entry updated; verify green and `skills/tests` hand-run OK.
- 2026-10-15: T3 done: records-hygiene §7, `/hotfix` step 1, `/cairn-triage` step 1 (candidate subject only; a Known issues subject keeps its rule), `/milestone`'s §7 sentence, and review step 9 cite the paragraph; hotfix pin updated. AC3 sweep: remaining old-rule hits are README.md:314-317 and cairn/DESIGN.md:285, left to T5; the "exact title" hits in §7, triage, and review now read §7's title; README.md:140 is about milestone titles in the band and source-note.md:37 about a citation, both unrelated.
- 2026-10-15: T4 done: `/cairn-triage` gains `retitle` (table row, a Title evidence class checked last on rows the others leave `keep`, the proposal table's naming, the apply step, and the no-D-entry list); a `compress` or `split` rewrite opens each row with a short title; verify green, `skills/tests` OK.
- 2026-10-15: agent chose to check the Title class last, on rows the other classes leave `keep`, over letting it pre-empt them, because a drop or merge removes the title problem with the row.
- 2026-10-15: T5 done: README's pane section (rule, writing shape, `retitle`), DESIGN.md's `candidateRows` description, and a CHANGELOG entry under "Changes that affect existing repos"; AC3's sweep over README.md and cairn/DESIGN.md now finds only hits that agree with the rule (plus README.md:140, about milestone titles); verify green.
- 2026-10-15: claim audit: 44 claims read, 6 corrected — CHANGELOG.md (3), skills/cairn-triage/SKILL.md (1), skills/shared/tracking-rules.md (2); the same reader re-read the six and found all fixed; the rulebook baseline re-seeded to 664 lines / 63,656 bytes at its three sites.
- 2026-10-15: all tasks done; verify green (both suites, both validates, `claude plugin test` 1714 pass), `skills/tests` hand-run OK; status set to review.
- 2026-10-15: review return 1: AC5 — `/cairn-triage`'s `retitle` apply step replaced a title cut at ` — ` or a long `: ` title with the new title, deleting the row's description, so it did not rewrite only the row's opening (diff-bug #1, blame-history #1); the other fix-now findings in the Review section ride the same return.
- 2026-10-15: T6 added for review return 1 (minor amendment) and done: `retitle` now keeps the token, puts the new title and `: ` before the row's text, and rewrites listed mentions in other ROADMAP rows and Known issues entries; plus the triage subject bound, eight-word vocabulary, carve-outs, stamp, uniqueness, same-pass scope, merge-survivor exclusion, `JS_TRIM` with `test_python_candidates_cut_and_trim_edges` (red on bare `strip()`), two TS trim rows, the skeleton and its fixture, `types/index.d.ts`, D-163's D-108 and D-035 sentences, and two rewraps; verify green (`claude plugin test` 0 fail), `skills/tests` OK.
- 2026-10-15: claim audit: 38 claims read, 6 corrected — skills/cairn-triage/SKILL.md (3), CHANGELOG.md (1), cairn/DECISIONS.md (1), scripts/tests/test_status_fixtures.py (1); scope: the return's added lines (`6b2d646d..` outside milestone files); the same reader re-read the six and found all fixed.
- 2026-10-15: return work done; verify green, `skills/tests` OK; status set to review.
- 2026-10-15: amendment routed: AC5 — the skill proposes `retitle` only for rows the other classes leave `keep` (one disposition per item, since T4) and not for a `merge` survivor, while AC5 says each row with an empty, long, or shared title, with only the live-milestone exception; the criterion is wrong as written (review pass 2).
- 2026-10-15: re-audit: AC5 (full) — 3 findings on the first amended wording: a finding-absorbing row never reaches the Title class; a row the pass removes gets no mention rewrite; "rewrites only the row's opening" mismatches the skill's insert. All three fixed in the wording.
- 2026-10-15: re-audit: AC5 (full) — 3 findings on the re-entered wording: a row a live milestone absorbs but does not quote is `keep` in the skill; "after the row's opening token" has no anchor on an untagged row; no step names a search for mentions outside the enumerated items. Second re-audit line for AC5: the repeated review-failure stop, put to the user.
- 2026-10-15: question at the stop: accept the fixed AC5 text, move retitle out, or stop — the user chose to accept the fixed text, with no further re-check of AC5.
- 2026-10-15: amendment return: AC5 — "It is proposed for each candidate row that the other evidence classes leave `keep`, other than a `merge` survivor, a finding-absorbing row, or a row a live milestone absorbs or quotes, whose short title is empty, is over 60 code points, or is shared with another row (each such row gets its own proposal), whatever the row's byte length. It inserts a short title ending at `: ` after the row's `- ` and any priority token and leaves the row's text unchanged (a row whose title is empty loses only its leading `: `). Its accepted edit also rewrites each double-quoted mention of the old title, found by a search of `cairn/ROADMAP.md` and DESIGN.md's Known issues, in another ROADMAP row the pass does not remove."
- 2026-10-15: AC5 amendment applied to the skill: "after the `- ` and any priority token" at the table row and the apply step, the mention search named in the Title class, and the live-milestone-absorbed exclusion; AC5's box unticked for re-review.
- 2026-10-15: the AC5 amendment took the plan-owned body to 153 lines; compressed the heaviest section (Acceptance criteria) in one pass by cutting its template comment to one line; validate green.
- 2026-10-15: step-7 approval: m251-candidate-short-title approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

- AC1 (2026-10-15, branch head after 6b2d646d): `claude plugin test .` 1714 pass, 0 fail; the 7 tests of "the short title is cut at the first `: `, else at the first ` — ` (M251 AC1)" in `reader.test.ts` all pass, one per table row; the `candidates` fixture carries the 6 non-empty table rows with their expected titles, and `scripts/tests` (407, OK) holds `python_candidates` to it through `test_python_helpers_match_expected`; `hooks/tests` 175 OK; both `claude plugin validate` runs exit 0.
- AC2: `skills/shared/tracking-rules.md:215-221` is one "Candidate short title" paragraph right after "Candidate priority token" (209-213); it states the cut (first `: `, else first ` — `, else all), says the pane shows the title and the skills name a row by it (✎, §7, `/hotfix`), tells a writer to open each row with a few words that name it and differ from every other title, then `: ` and the detail, and gives the area-word example. `cairn/DECISIONS.md:5868` D-163, whose heading names D-149, narrows D-149's title sentence.
- AC3: the five sites cite the paragraph and state no rule of their own: `records-hygiene.md:37`, `hotfix/SKILL.md:51-52`, `cairn-triage/SKILL.md:63-64` (candidate subject), `milestone/SKILL.md:139-140`, `milestone-review/SKILL.md:714-716`. The sweep (`git grep -n -i` with the five patterns over the named paths) returned 57 hits on the branch; each agrees: the rule's own statements (tracking-rules, README 314-325, DESIGN 284-291, reader/pane/register comments, the test twin, fixtures, skeleton), §7's and its readers' "exact title" (now §7's defined title), triage:65 (a Known issues subject, not a candidate title), README:140 (milestone titles in the band) and source-note.md:37 (a citation title), which state no candidate-title rule.
- AC4: `cairn-init/SKILL.md:191-192` shows `- [high] short title: detail — added YYYY-MM-DD — links` and the untagged form; `tracking-rules.md:209-210` gives the same shape as the token example.
- AC5: `cairn-triage/SKILL.md:106` adds the `retitle` row (opening rewritten into a short title ending at `: `, rest unchanged, double-quoted mentions in other ROADMAP rows rewritten, a shared-title mention listed as ambiguous and left); `:144-151` the Title class (empty, over 60 code points, or shared, one proposal per sharing row, byte length does not matter, not for a row a live milestone file quotes); `:246` the apply step. Review fixed "another candidate row" to "another ROADMAP row" (106, 246, CHANGELOG:18) to match the criterion's wording.
- AC6: `README.md:314-325` states the rule, the writing shape, and `retitle`; `cairn/DESIGN.md:284-286` states the rule in the `candidateRows` description; `CHANGELOG.md` Unreleased, "Changes that affect existing repos", first entry, says a row with no `: ` loses the date and links after its dash, names the writing rule and `retitle`, and says an old whole-text quote of such a row no longer matches.
- consistency gate: `cairn_validate` all checks passed; no principle changed, so `cairn_impact` skipped; verify green on the review head (scripts 407 OK, hooks 175 OK, both validates exit 0, `claude plugin test` 1714 pass); the marketplace validate prints no `plugins[N].version` warning; CHANGELOG has the entry with no milestone number; `skills/tests` hand-run 752 OK.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: `retitle`'s apply step replaced a title cut at ` — ` (the whole description) or a long `: ` title with the new title, deleting the row's substance — fix now; floor return (AC5 "rewrites only the row's opening" fails as written).
- diff-bug #2: rewriting mentions in other rows breaks step 3's byte-for-byte rule for unaccepted items — fix now (carve-out for a listed mention).
- diff-bug #3: mention rewrites collide with same-pass dispositions of the quoting row; a milestone-row rewrite can drift from the milestone file heading — fix now for the ordering (rewrite applied to each quoting item's text as its own disposition leaves it, none in a dropped item); the milestone-row part rejected, planned change (AC5 names "another ROADMAP row").
- diff-bug #4: step 6's stamp omits retitled items — fix now.
- diff-bug #5: "seven words" is now eight — fix now.
- diff-bug #6: a candidate's subject can be empty or unbounded — fix now (short title only when not empty and ~80 characters at most, else the old fallback).
- diff-bug #7: no uniqueness check on new titles; ambiguous mentions can drop a §7 group — fix now for uniqueness; the ambiguous-mention part rejected, planned change (AC5 lists and leaves them, shown at the chip).
- diff-bug #8: a retitled row cannot take a priority change — fix now.
- diff-bug #9: "another row" ignores same-pass drops and merges — fix now.
- diff-bug #10: a Known issues quote of the old title stays stale — fix now (Known issues entries join the rewrite).
- diff-bug #11: the fixture's rows 2 and 12 share `Low row` and the pane test comment says otherwise — fix now (comment).
- diff-bug #12: `python_candidates` is never held to an empty title — fix now (`test_python_candidates_cut_and_trim_edges`).
- diff-bug #13: JS `trim()` and Python `strip()` differ on U+FEFF and U+001C-U+001F — fix now (`JS_TRIM`; the new test fails on bare `strip()` for both rows).
- diff-bug #14: the skeleton comment states half the rule — fix now (it now tells a writer to open with the short title and points to the paragraph).
- diff-bug #15: two overlong lines in README.md and DESIGN.md — fix now.
- blame-history #1: same defect as diff-bug #1, and the opening token's fate unstated — fix now (token kept).
- blame-history #2: D-163 does not say how it passes D-108's door — fix now (D-163, still unmerged, states the retained trigger: the pane showed `ordinal` for 8 rows).
- blame-history #3: D-163 does not say why D-035's rejected opener does not apply — fix now (one sentence in D-163).
- blame-history #4: review step 9's "after its own title's `: `" fits only colon rows — reject, planned change: rows review files follow the writer rule and open with a title and `: `.
- blame-history #5: a late `: ` wins over an earlier ` — `, so provenance can leak into a title — reject, planned change (the plan gate's colon-first choice, AC1's `Title — detail: more` row).
- blame-history #6: the `candidates-skeleton` fixture still holds the old skeleton text — fix now.
- blame-history #7: the skeleton comment and `types/index.d.ts` were stale at the branch commit — fix now (same as diff-bug #14 and prior-review #1).
- blame-history #8: the hotfix pin now asserts a citation, not the rule — reject, planned change (T3 called for the cite; reader tests hold the behavior).
- blame-history #9: CHANGELOG states the lost whole-text match only for §7 — reject, false: the entry says any old quote of such a row no longer matches.
- blame-history #10: a `merge` survivor can also take `retitle` — fix now (excluded in the same pass).
- prior-review #1: `types/index.d.ts:60` still documents the old cut (also Copilot's thread) — fix now.
- prior-review #2: the skeleton comment restates part of the rule — fix now (same as diff-bug #14).
- prior-review #3: hotfix step 1 now cites the paragraph in place of PR 259's colon-less wording — reject, false: the paragraph states the colon-less case and the reader agrees.
- prior-review #4-#6: rulebook baseline, hotfix step 1's before-any-stop text, README overclaims — reject, false: the lens found each consistent.
- pass 2: diff-bug #9 (same-pass drops and merges) re-dispositioned to reject, planned change: AC5 says "shared with another row", so the narrowing was reverted (skills/cairn-triage/SKILL.md:149).
- pass 2 evidence (head dd4855f0): verify green: `scripts/tests` 408 OK, `hooks/tests` 175 OK, both validates exit 0, `claude plugin test` 1716 pass, 0 fail (the 9 "M251 AC1" table tests pass, two of them the review trim rows); `skills/tests` 752 OK; `cairn_validate` all checks passed. AC1-AC4 and AC6 re-read on this head and unchanged in substance from pass 1 (AC6's CHANGELOG entry now describes the insert and the Known issues rewrite).
- AC5 (pass 2, amended text): `skills/cairn-triage/SKILL.md:109` the `retitle` row (new title and `: ` after the `- ` and any priority token, text unchanged, empty title loses only its leading `: `, mentions in other ROADMAP rows and Known issues rewritten, shared-title mentions listed as ambiguous); `:147-160` the Title class (rows left `keep`; empty, over 60 code points, or shared; one proposal per sharing row; byte length does not matter; the search over `cairn/ROADMAP.md` and Known issues; no `retitle` for a row a live milestone quotes or absorbs, or a `merge` survivor); `:161-164` finding-absorbing rows take §7's options before any class, so never reach the Title class; `:252-258` the apply step (mentions rewritten in each quoting item as its own disposition leaves it, none in a dropped item).
- copilot: cairn/milestones/M251-candidate-short-title.md:14 — fix now (record the PR URL in the Branch/PR header), fixed 8630d7c
- copilot: hooks/status/reader.ts:545 — fix now (`types/index.d.ts` still documented the old cut), fixed 15b0ad3
- copilot: review body — noted (an index of the two threads above)
- Copilot level: Lite (set by GitHub's settings)
- spawned: diff-bug, blame-history, prior-review (pass 2)
- pass 2 diff-bug #1: a `compress` or `split` rewrite gave a row a new short title with no mention rewrite or live-milestone check — fix now (that clause removed; only `retitle` changes a title).
- pass 2 diff-bug #2: the owner-mode cap check did not count the longer stamp — fix now (step 4 now counts the stamp in both modes), fixed c660c07.
- pass 2 diff-bug #3: rows that share a title get identical subjects at the chip, so the Amend loop cannot tell their proposals apart — follow-up (candidate row "Retitle edges (M251 review)").
- pass 2 diff-bug #4: README.md:325 still overlong — fix now, fixed c660c07.
- pass 2 diff-bug #5: an empty title that does not come from a leading `: ` (a row opening with ` — `, or spaces) has no anchor in the subject and apply rules, and an empty old title's mention search matches `""` — follow-up (same row).
- pass 2 diff-bug #6: nothing bounds a new title (empty, long, or holding `: `) — fix now (not empty, no `: ` or ` — `, 60 code points at most).
- pass 2 diff-bug #7: the Amend loop can set a new title another row already has — follow-up (same row).
- pass 2 diff-bug #8: the Known issues mention rewrite is scope AC5 does not ask for — reject, not a defect: a deliberate pass-1 fix (diff-bug #10) that AC5 does not forbid.
- pass 2 diff-bug #9: quotes of a whole no-`: ` row written before M251 stay stale after a `retitle` pass — reject, planned change: D-163 and CHANGELOG state that consequence.
- pass 2 diff-bug #10: "rewords" no longer describes the insert — fix now (tracking-rules, README, D-163); rulebook baseline re-seeded to 664 lines / 63,690 bytes at its three sites.
- pass 2 diff-bug #11: CHANGELOG says "characters" and omits the exclusions — reject, style: a plain-language summary for users.
- pass 2 diff-bug #12: literal invisible U+FEFF/U+001F in the tests (and in `JS_TRIM`) — fix now (written as escapes).
- pass 2 diff-bug #13: the `JS_TRIM` comment names characters that break lines before the trim — fix now (comment narrowed to U+FEFF and U+001F).
- pass 2 blame-history #1: README and DESIGN lines still overlong — fix now, fixed c660c07.
- pass 2 blame-history #2: no guard pins the new mention carve-out — reject, not a defect: the prose guards stay hand-run (D-109) and the carve-out text is correct.
- pass 2 blame-history #3: step 4 says `keep` and `promote` change nothing while a mention rewrite can touch them — fix now, fixed c660c07.
- pass 2 blame-history #4: owner-mode stamp not counted — same as pass 2 diff-bug #2, fixed c660c07.
- pass 2 blame-history #5: a candidate title over ~80 characters fell to the Known issues subject rule — fix now (the short title trimmed to ~80), fixed c660c07.
- pass 2 blame-history #6: `compress`/`split` titles had no uniqueness check — fix now (that clause removed, as pass 2 diff-bug #1).
- pass 2 blame-history #7: D-163's heading did not name D-108's door — fix now (heading, still unmerged), fixed c660c07.
- pass 2 prior-review #1: the stamp-length point from the M235 review (owner mode) — same as pass 2 diff-bug #2, fixed c660c07.
- pass 2 prior-review #2: overlong lines — same as pass 2 diff-bug #4, fixed c660c07.
- pass 2 prior-review #3: a title over ~80 characters falls out of the subject rule — same as pass 2 blame-history #5, fixed c660c07.
- pass 2 prior-review #4: a row a live milestone quotes or absorbs keeps a shared title, so its ✎ stays ambiguous — reject, planned change: AC5 excludes those rows.
- pass 2 return floor: no finding shows a criterion failing or a load-bearing defect; no return.
- conversation: copilot-pull-request-reviewer[bot] PR review (COMMENTED) — noted (its two threads are the `copilot:` lines above)
- conversation: jmgirard PR reviews (COMMENTED, two) — noted (GitHub's wrappers for the two thread replies)
- conversation: no issue comments; no unresolved threads after the replies.
