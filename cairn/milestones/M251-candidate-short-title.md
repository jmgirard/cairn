<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M251: One short-title rule for candidate rows

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters see the cairn pane, and their agents follow the rulebook when they write rows   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m251-candidate-short-title   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [ ] AC1: `candidateRows` in `hooks/status/reader.ts` and `python_candidates`
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

- [ ] AC2: `skills/shared/tracking-rules.md` states the rule in one
      "Candidate short title" paragraph beside "Candidate priority token". The
      paragraph says that the pane shows the short title and that the skills
      name a row by it. It tells a writer to open each row with a few words
      that name the row and differ from every other row's title, then `: `
      and the detail. It says that an area word joins the title
      (`ordinal REML: ...`, not `ordinal: REML. ...`). A new `DECISIONS.md`
      entry whose heading names D-149 narrows D-149's title sentence to this
      rule.
- [ ] AC3: records-hygiene §7, `/hotfix` step 1, `/cairn-triage` step 1's
      subject, the `/milestone` health audit's §7 sentence, and
      `/milestone-review` step 9's row-filing sentence cite that paragraph and
      state no title rule of their own. The branch runs one sweep:
      `git grep -n -i -e "first \`: \`" -e "first colon" -e "short title" -e "title's \`: \`" -e "exact title"`
      over `skills`, `README.md`, `cairn/DESIGN.md`, `hooks`, and `scripts`.
      Each hit agrees with the rule.
- [ ] AC4: The `/cairn-init` ROADMAP skeleton comment in
      `skills/cairn-init/SKILL.md` and the row example in the "Candidate
      priority token" paragraph show the shape
      `- [high] short title: detail — added YYYY-MM-DD — links`.
- [ ] AC5: `/cairn-triage` has a `retitle` disposition. It is proposed for
      each candidate row whose short title is empty, is over 60 code points,
      or is shared with another row (each such row gets its own proposal),
      whatever the row's byte length. It is not proposed for a row whose
      title a live milestone file quotes. It rewrites only the row's opening
      into a short title that ends at `: `. Its accepted edit also rewrites
      each double-quoted mention of the old title in another ROADMAP row. A
      mention of a shared title is listed as ambiguous and is not rewritten.
- [ ] AC6: README's cairn pane section and DESIGN.md's `candidateRows`
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
- AC5 → T4
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
- [ ] T2: Write the "Candidate short title" paragraph after "Candidate
      priority token" (`tracking-rules.md:209`) and change that paragraph's
      row example. Change the skeleton comment in
      `skills/cairn-init/SKILL.md` (~line 190). Append the D-entry that
      narrows D-149.
- [ ] T3: Make records-hygiene §7 (line 36), `/hotfix` step 1 (line 51),
      `/cairn-triage` step 1 (line 63), `/milestone` (line 139), and
      `/milestone-review` step 9 (line 710) cite the paragraph. Update the pin
      in `skills/tests/test_hotfix_candidate_graduation.py:53` and hand-run
      `skills/tests`. Run AC3's sweep and fix each hit.
- [ ] T4: Add `retitle` to `/cairn-triage`'s disposition table, its evidence
      classes, and its apply step, with the ROADMAP quote rewrite and the
      live-milestone exclusion.
- [ ] T5: Update README's pane section (~line 314), DESIGN.md (~line 285),
      and `CHANGELOG.md`.

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
