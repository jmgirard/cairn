<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M272: The next-step recommendation names the first unstarted high-priority candidate

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters read `cairn_next.py`'s output and press the pane's and band's Plan Button   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m272-next-step-names-high-row, https://github.com/jmgirard/cairn/pull/284   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When nothing is in review, in progress, or workable, `cairn_next.py` and the cairn pane recommend planning the first unstarted `[high]` candidate row by its short title, and the Plan press plans that row.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A candidate-row reader in `scripts/` (priority, short title, started
token) and a `title` key on `recommend` in `scripts/cairn_next.py`; its
printed `Recommended:` line and docstrings. The TypeScript mirror in
`hooks/status/reader.ts`, a fixture that reaches the case, the pane's Next
line, and the shared `pressNext` in `hooks/status/register.tsx`. README and
CHANGELOG.

**Out:** The band's drawing: it shows no command (M220), so its only change is
the shared press. Skipping to a later `[high]` row when the pane hides the
first one for an open pull request's body (M252): the pane then shows no title,
as below; a later-row search stays out until that case is seen in a real
session. `/milestone` and `/milestone-plan` text: `/milestone` leads its
close with the Recommended line as printed, and `/milestone-plan` step 1 reads
only the active and workable picture. The triage change that writes `[high]` →
M271.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: `recommend` in `scripts/cairn_next.py` returns a `title` key. In
      the planning case it holds the short title (tracking-rules "Candidate
      short title"), trimmed as JavaScript's `trim` trims, of the first
      candidate row, in ROADMAP order, that opens with `[high] `, has a
      non-empty short title, and carries in its text after `[high] ` no
      started token (` — started M<n>` or ` — started #<n>`, `<n>` one or
      more ASCII digits, followed by the row's end or a character that is
      not an ASCII letter or digit); with no such row, and in every other
      case, it is `None`. A candidate row is a line that opens with `- `
      under a `## ` heading that starts with `## candidates` in any letter
      case, up to the next `## ` line, read after each `<!--` … `-->` span
      that opens and closes within that section is removed. Tests in
      `scripts/tests` cover: a `[high]` row chosen over an earlier untagged
      row, a started `[high]` row passed over for a later `[high]` row, a
      token followed by a non-ASCII letter still counting as started, a
      `[high]` row inside an HTML comment passed over, no `[high]` row giving
      `None`, and a workable planned milestone giving `None` beside a
      `[high]` row.
- [x] AC2: In the planning case with a title, `cairn_next.py`'s printed
      `Recommended:` line reads `Recommended: plan the next milestone →
      /milestone-plan <title>`; with no title the line is unchanged.
- [x] AC3: `recommend` in `hooks/status/reader.ts` returns the same `title` as
      the Python on every fixture `scripts/tests/test_status_fixtures.py`
      compares, and at least one compared fixture gives a non-null title.
- [x] AC4: In the planning case with a title, the pane's Next line shows
      `/milestone-plan <title>`, and the next-step Plan press, from the pane
      or the band, runs `/cairn:milestone-plan` with that title as its
      argument after `/clear`; with no title, or when an open pull request's
      body names that title (the pane's M252 hide rule), both behave as
      before. Tests in `hooks/status` cover the line and the press with and
      without a title.
- [x] AC5: The README paragraph on the pane's Next line (~`README.md:290`),
      the paragraph naming `cairn_next.py`'s recommendation (~`README.md:187`),
      the `cairn_next.py` module and `recommend` docstrings, and a
      `CHANGELOG.md` `## Unreleased` entry each say that planning names the
      first unstarted `[high]` candidate.
- [x] AC6: The `verify` slot of `cairn/PROFILE.md` passes on the branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T5
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1, T4
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Python: a candidate-row reader (Candidates sections, comments
      stripped, `[high] `/`[low] ` token, short title with JS-trim, started
      token) in `scripts/cairn_scripts.py` or `cairn_next.py`; `recommend`'s
      `title`; the `Recommended:` line; both docstrings; tests in
      `scripts/tests` for the AC1 cases and the AC2 line.
- [x] T2: TypeScript: `recommend` in `hooks/status/reader.ts` takes the
      candidate texts and returns `title`; `NextStep` gains `title`; add or
      edit a fixture with no workable row and a `[high]` row; regenerate the
      expected JSON with `hooks/status/fixtures.gen.ts`; run
      `test_status_fixtures.py`.
- [x] T3: Pane: the Next line's target text (`hooks/status/pane.ts` ~:465)
      and `pressNext`'s args (`hooks/status/register.tsx` ~:1111), both
      falling back to no title when an open pull request's body names it;
      tests in `hooks/status` for the line and the press.
- [x] T4: README (~:187, ~:290) and CHANGELOG; run `verify`, including
      `claude plugin test`.
- [x] T5: AC1 amendment (review pass 1, diff-bug #8): the token-end
      wording says ASCII, the candidate-row rule is stated, and tests cover a
      non-ASCII letter after the token, a U+FEFF trim, and section bounds.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: milestone — planned at the question set of M271's plan, which the user asked to include this work in; changes script output and pane behavior.
- 2026-10-17: collision check: D-134 (priority token), D-165 (started token), and D-167 (pane hides started rows) allow it; no candidate row or archived milestone covers naming a candidate in the recommendation.
- 2026-10-17: question set: name the first `[high]` row in the next-step recommendation — include it.
- 2026-10-17: plan gate chose the first unstarted `[high]` row in ROADMAP order over the first `[high]` row the pane draws because Python cannot read open pull request bodies and the parity test needs one rule; falsified by a session where the Next line names a row the Candidates list hides.
- 2026-10-17: criteria audit (full mode, fresh Opus reader): no criterion unreachable; fixed — the started token takes its real shape, the title trim is JavaScript's, AC4 falls back for a row an open PR names, AC5 narrowed to two named README paragraphs plus both docstrings; noted — a row with a dead started token is never recommended though the pane still lists it.
- 2026-10-17: implement started on branch m272-next-step-names-high-row, cut from main at b1d03358; untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-17: T1 done: `candidate_texts`, `short_title`, and `high_title` in `scripts/cairn_next.py` (not `cairn_scripts.py`, since only `recommend` reads them); `recommend` takes an optional `roadmap` text and returns `title`; 6 tests in `TestNext`, each shown red on a planted defect. Choice: the started token takes any number of digits after `M` or `#` (AC1's `#<n>`), where the pane's `STARTED_TOKEN` caps `#` at 15 digits; a letter after the token is ASCII-only, as in that reader.
- 2026-10-17: T2 done: `highTitle` and `recommend(rows, workable, roadmap)` in `hooks/status/reader.ts`; new fixture `high-candidate` (title "Chosen row"); `"title": null` added to the other 29 fixtures' `next` by a Haiku subagent, diff checked as 29 one-line inserts; T1 and T2 commit together, since either alone fails the fixture parity tests.
- 2026-10-17: T3 done: `nextTitle` in `hooks/status/pane.ts` drops the title when an open PR body names it; the Next line and `pressNext` both read it; 6 old tests updated to the new planning shape and 6 new AC4 tests (line, pane press, band press, hide rule) added; plants of no hide rule and no title in the press turned 11 tests red, and a press plant without the hide rule turned 1 red.
- 2026-10-17: T4 done: README's idle-row paragraph (~:187) and the pane's Next-line paragraph (~:297) name the `[high]` row; the empty-row paragraph (~:226) said `Plan` runs with no arguments, now false, so it was corrected too; CHANGELOG entry under Unreleased. The simple-english lint hook reports 218 README and 360 CHANGELOG hits; the README count equals its pre-branch count, and the CHANGELOG's one added hit is the house bold lead-in. verify green: scripts 415 OK, hooks OK, both validates exit 0, plugin test 2070 pass.
- 2026-10-17: claim audit: 41 claims read, 1 corrected — scripts/tests/test_scripts.py (a test comment said a token run on into a digit is not a token; `[0-9]+` absorbs the digit, so it now says a letter); re-read by the same reader: true. Noted, not a claim error: a `[high]` row with a dead started token is skipped by the pill but still listed by the pane, as the criteria audit noted.
- 2026-10-17: implement complete; status review. verify green on the branch head: scripts 415 OK, hooks OK, both validates exit 0, plugin test 2070 pass; cairn_validate all checks passed.
- 2026-10-17: review pass 1: AC2-AC6 and the gate pass; 3 lenses ran; 5 findings fixed in 5afb3631, 9 rejected, 9 to the new candidate row "Plan target edges (M272 review)".
- 2026-10-17: amendment routed: AC1 — diff-bug #8: AC1 says a started token is followed by "a character that is not a letter or digit", but the reader, like the pane's M258 `STARTED_TOKEN`, ends the token at any character that is not an ASCII letter or digit, so `— started M12é` counts; the wording, not the code, is wrong.
- 2026-10-17: re-audit: AC1 (full) — first wording ("not an ASCII letter or digit" alone): "outside HTML comments" is wider than the per-section comment strip (an unclosed or cross-section `<!--`), "under `## Candidates`" omits the any-case prefix rule, `- [high] — started M1` carries a token the code misses, and no test holds a non-ASCII letter after the token; fixed by stating the candidate-row rule, "in its text after `[high] `", and the `é` test.
- 2026-10-17: re-audit: AC1 (full) — second wording: the code meets every clause; wording edges answered, not changed (the second line is the bound): "non-empty short title" is the title the sentence trims as JavaScript does, "opens with `[high] `" reads the row text after `- ` as tracking-rules uses it, and "line" splits as `str.splitlines` does, which `reader.ts` mirrors; test gaps closed in T5: a U+FEFF trim, a lower-case heading, a second Candidates section, and a `[high]` row under a later non-Candidates heading, each shown red on a planted defect.
- 2026-10-17: amendment return: AC1 — "carries in its text after `[high] ` no started token (` — started M<n>` or ` — started #<n>`, `<n>` one or more ASCII digits, followed by the row's end or a character that is not an ASCII letter or digit) … A candidate row is a line that opens with `- ` under a `## ` heading that starts with `## candidates` in any letter case, up to the next `## ` line, read after each `<!--` … `-->` span that opens and closes within that section is removed."
- 2026-10-17: T5 done; verify green: scripts 416 OK, hooks OK, both validates exit 0, plugin test 2071 pass; cairn_validate all checks passed. Status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Review pass 1, 2026-10-17, branch head 7e6726f9 (main b1d03358 unmoved). PR #284 opened at review start (Copilot round on).

- AC1: `python3 -m unittest -v scripts.tests.test_scripts -k TestNext` — 13 OK, among them the five cases AC1 names: `test_plan_names_the_first_high_row_over_an_earlier_untagged_row`, `test_plan_passes_over_a_started_high_row` (each token shape, then the later `[high]` row), `test_plan_passes_over_a_high_row_in_a_comment_and_an_empty_title`, `test_plan_with_no_high_row_gives_none`, `test_workable_milestone_gives_none_beside_a_high_row`; `recommend` returns `title` in all four branches (`scripts/cairn_next.py`); the trim is `strip(JS_TRIM)`. PASS.
- AC2: `python3 scripts/cairn_next.py` on a copy of fixture `high-candidate` prints `Recommended: plan the next milestone → /milestone-plan Chosen row`; on a copy of `candidates-skeleton` (no `[high]` row outside a comment) it prints the line ending at `/milestone-plan` and a newline (`od -c`), unchanged from main; the tests above assert both lines with their newline. PASS.
- AC3: `python3 -m unittest -v scripts.tests.test_status_fixtures` — 12 OK; `test_python_helpers_match_expected` holds `cairn_next.recommend` (with `title`) to every fixture's `expected.json`, and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude plugin test .` (2070 pass, 0 fail) passes "the pane's milestones and next step match expected.json" for all 31 fixtures, so `reader.ts` `recommend` gives the same `title` on each; `test_a_fixture_names_a_high_row_for_planning` asserts the only non-null title is `high-candidate`'s "Chosen row". PASS.
- AC4: same `claude plugin test .` run; the "M272 AC4" block passes: the Next line text ` /milestone-plan Chosen row `, ` /milestone-plan ` with no title, and ` /milestone-plan ` when a body names the title; the pane press on `high-candidate` runs `clear` then `cairn:milestone-plan` "Chosen row", on `candidates-skeleton` with `''`; with a `gh pr list` body naming "Chosen row" both the pane and the band press run planning with `''`, and with a body naming another row both run it with "Chosen row". The band's M213 and M221 press tests run "Chosen row" on `high-candidate`. PASS.
- AC5: read at head: `README.md:187-191` (the paragraph naming `cairn_next.py`'s recommendation) and `README.md:298-302` (the pane's Next line) each say planning names the first `[high]` candidate row with no started token; the `cairn_next.py` module docstring (:9-11) and the `recommend` docstring (:83-88) say it; `CHANGELOG.md:7-19` under `## Unreleased` has the entry. PASS.
- AC6: verify on code head 7e6726f9: `scripts/tests` 415 OK (21 skipped), `hooks/tests` 179 OK, `claude plugin validate` plugin.json exit 0 and marketplace.json exit 0, `claude plugin test .` 2070 pass 0 fail. PASS.
- Gate: `cairn_validate.py` exit 0, all checks passed; no principle touched, so no `cairn_impact`; profile gate: verify green (AC6), the marketplace validate prints no `version` warning, and `CHANGELOG.md` has an Unreleased entry with no milestone number. PASS.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the press names a row an open PR names when the pane has not read the PRs yet (pane closed, or press before the read settles), while README/CHANGELOG stated the hide rule with no condition — fix now (docs: the rule is the pane's last PR read, as AC4's "the pane's M252 hide rule" is; README :230, :300, CHANGELOG), fixed 5afb3631
- diff-bug #2: two rows with one short title, the other carrying a live started token: the pill names a title the Candidates list hides — follow-up ("Plan target edges (M272 review)")
- diff-bug #3: a dead started token, or a `#` token of 16+ digits, makes the pill pass over a row the pane still lists — follow-up (same row); AC1 as written skips any token
- diff-bug #4: `cairn/DESIGN.md:180` still says Plan runs with empty args — fix now, fixed 5afb3631
- diff-bug #5: `skills/milestone-review/SKILL.md` step 10's `→ /<skill> [M<NNN>]` tail omits a title, and `skills/milestone/SKILL.md:392` says `cairn_next` reads status and priority alone — follow-up (same row); both outside Scope In
- diff-bug #6: `NextStep` gained `title` with the `pane` atom tag left at `pane-6`, against register.tsx's "bump a tag when its type changes" — fix now (`pane-7`, DESIGN :356, :474, :706), fixed 5afb3631
- diff-bug #7: a `[high]` row under `## Candidates (dropped)` can be recommended — follow-up (same row); the reader shares the pane's and `candidate_count`'s heading rule, a DESIGN known issue
- diff-bug #8: AC1 says a token followed by "a character that is not a letter or digit", and the code treats a non-ASCII letter (`M12é`) as ending the token — amendment routed (AC1's wording, not the code: the reader follows the pane's M258 `STARTED_TOKEN`, ASCII-only)
- diff-bug #9: an unclosed `<!--` hides nothing, so a row after it can be recommended — follow-up (same row); pre-existing reader behavior
- diff-bug #10: a press after a refresh plans the new first `[high]` row, not the one the stale drawing showed — reject (planned design: the press reads state at press time, M212 review, M213)
- diff-bug #11: no test holds a live started token, only one compared fixture has a title, and the comment unit tests wrap markers in bullets — reject (no defect behind it; the fixture covers a flush-left comment)
- blame-history #1: dead started tokens block the row — follow-up (same as diff-bug #3)
- blame-history #2: `[high]` now picks the Plan target, which D-179 names as the entry to supersede if ready and important rows need telling apart — reject (planned change: the user chose naming the first `[high]` row at M271's question set; no operator has hit the case D-179 names)
- blame-history #3: `cairn_next.py` prints the title when an open PR names the row, the pane drops it — reject (planned change: the plan gate chose one rule Python can apply, falsifier recorded)
- blame-history #4: DESIGN.md:179-180 stale — fix now (same as diff-bug #4), fixed 5afb3631
- blame-history #5: `pane-6` tag not bumped — fix now (same as diff-bug #6), fixed 5afb3631
- blame-history #6: `## Candidates (dropped)` heading read — follow-up (same as diff-bug #7)
- blame-history #7: the `#` digit cap differs from the pane's — follow-up (same as diff-bug #3)
- blame-history #8: no length cap on the pill's title — reject (false: the pill's Text draws `truncate-end` and is cut first, M218)
- blame-history #9: the title argument goes unquoted — reject (planned change: the ✎ press passes titles the same way, M242)
- blame-history #10: an untokened row that a planned or blocked milestone already quotes can be named again — follow-up (same row)
- prior-review #1: a sibling row with the same title and a live token hides the row in the pane while the pill names it — follow-up (same as diff-bug #2)
- AC1 tick withdrawn: diff-bug #8 shows AC1's token-end wording failing as written; AC1 is re-verified after its amendment.

Review pass 2, 2026-10-17, branch head 7fe3604c (main b1d03358 unmoved), after the AC1 amendment and fix-now commit 5afb3631. Copilot state: reviewed earlier-head, so no new request.

- AC1 (as amended): `python3 -m unittest -v scripts.tests.test_scripts -k TestNext` — 14 OK, among them the six cases AC1 names: the `[high]` row over an earlier untagged row, the started `[high]` row passed over (each token shape, `#` of 16 digits, and `— started M12é`, a non-ASCII letter still counting as started), the `[high]` row in a comment and the empty title, no `[high]` row giving `None`, and a workable milestone giving `None`; `test_high_title_trims_as_javascript_and_reads_each_candidates_section` holds the U+FEFF trim, the any-case heading, a second Candidates section, and a later non-Candidates heading; code: `STARTED` `(M[0-9]+|#[0-9]+)(?![0-9A-Za-z])`, `COMMENT` removed per section, heading test `strip().lower().startswith("## candidates")`. PASS.
- AC2: at 7fe3604c, `cairn_next.py` on a copy of `high-candidate` prints `Recommended: plan the next milestone → /milestone-plan Chosen row`; on `candidates-skeleton` the line ends at `/milestone-plan` and a newline. PASS.
- AC3: `scripts.tests.test_status_fixtures` OK at 7fe3604c; the verify run at 7fe3604c (`claude plugin test .`, 2071 pass, 0 fail) passes the next-step comparison for all 31 fixtures. PASS.
- AC4: the same plugin test run passes the "M272 AC4" block (line, pane press, band press, both hide-rule cases) and the band's M213/M221 Plan tests on `high-candidate`; the pane state tag is now `pane-7`, and no test reads the tag. PASS.
- AC5: README now states the hide rule as the pane's last PR read (`README.md:229-233`, `:300-303`), and the paragraph at :187-191, both docstrings, and the CHANGELOG entry still say planning names the first unstarted `[high]` candidate. PASS.
- AC6: verify at 7fe3604c: scripts 416 OK (21 skipped), hooks OK, both `claude plugin validate` exit 0, plugin test 2071 pass 0 fail. PASS.
- Gate: `cairn_validate.py` all checks passed at 7fe3604c; marketplace validate prints no `version` warning; CHANGELOG entry present with no milestone number. PASS.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: README's "Otherwise `Plan` runs planning with no arguments" followed "Before the pane reads your PRs, nothing drops it", so it said a read always empties the argument — fix now, fixed 80c63869
- diff-bug #2: README said a refused planning run puts `/cairn:milestone-plan` in the prompt box, but `lineOf` adds the title — fix now, fixed 80c63869
- diff-bug #3: CHANGELOG's "With no such row, nothing changes" read as "with no PR naming it", and two lines ran past the wrap — fix now, fixed 80c63869
- diff-bug #4: `DESIGN.md:476` and the `STARTED_TOKEN` comment still said "a letter or digit" over an ASCII class — fix now, fixed 80c63869
- diff-bug #5: `JS_TRIM` and the U+FEFF test held literal invisible characters (the editor had decoded the `\u` escapes), so a stripping editor would change the set and void the test — fix now (built from `chr` code points; the bare-`strip()` plant still fails the test), fixed 80c63869
- diff-bug #6: the `candidate_texts` docstring said "under a `## Candidates` heading" and neither `high_title` nor `highTitle` said where a token is read — fix now, fixed 80c63869
- diff-bug #7: DESIGN.md misses the next step's `title` (:294) and M272 in the shape-tag correction list (:709) — fix now, fixed 80c63869; its :80 feature list — reject (false as a convention: that list already omits M258 and M268)
- diff-bug #8: a short title holding `#N` reaches `/milestone-plan` from the Plan press — reject (planned change: the ✎ press passes titles the same way, M242; pass 1 blame-history #9)
- blame-history #1: `types/index.d.ts` `CairnPaneState.next` lacks `title`, where M258 updated that file for `taken` — fix now, fixed 80c63869
- blame-history #2: DESIGN.md:476 "letter or digit" — fix now (same as diff-bug #4), fixed 80c63869
- blame-history #3: the shape-tag correction list and the `tag pane-N, M<x>` form at DESIGN.md:477 — fix now, fixed 80c63869
- blame-history #4, #6, #7, #9: repeats of pass-1 follow-ups and rejects — dispositions as in pass 1 ("Plan target edges (M272 review)", M242 pattern)
- blame-history #5: `[high]` as the Plan target meets D-179's supersede trigger, and no D-entry records the choice — reject (planned change: the user chose it at M271's question set, recorded in this file's `question set:` line; no operator has hit D-179's case)
- blame-history #8: `cairn_next.py` prints the title when an open PR names the row — reject (repeat of pass-1 blame-history #3)
- blame-history #10: `title` was added in 08e8a5da before the tag bump in 5afb3631 — reject (false as a shipped state: the PR squash-merges, so no intermediate commit ships)
- blame-history #11: `test_a_fixture_names_a_high_row_for_planning` asserts an exact set — reject (planned change: a fact stated apart from the helper, so a new titled fixture must be named there on purpose)
- blame-history #12: lines past the wrap in CHANGELOG, README, and `reader.ts:16` — fix now (rewrapped with the doc fixes), fixed 80c63869
- prior-review #1: the uncapped `#[0-9]+` reopens M259's 15-digit cap — reject (false as a regression: M259 caps `#` because triage passes the number to `gh pr view`, and this reader converts no number; AC1 as amended says one or more digits; the pane/pill split is in "Plan target edges (M272 review)")
- copilot: cairn/milestones/M272-next-step-names-high-row.md:14 (outdated) — reject (the header has named PR #284 since 7e6726f9; the branch stays beside it as the resume route's key); replied and resolved
- Copilot level: Lite (set by GitHub's settings); review body's one item is that thread.
- conversation: no human reviews or issue comments on PR #284.
