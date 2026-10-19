<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M288: Sessions read the repo's source shelf before they search the web for a paper

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the session-start hook's injected text and the source rules every adopting repo's sessions follow   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m288-shelf-first-sources   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A session in a cairn repo looks for a cited paper in `cairn/references/` before it searches the web, both inside the cairn skills and in plain conversation.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a "Source shelf" part in the session-start hook's injected
context for a repo whose `cairn/references/` holds notes or shelf files.
A shelf-first clause in the primary-sources rule
(`skills/shared/validation-doctrine.md`) and in tracking-rules
"References pages", so the rule binds non-numeric sources too. The README
sources section and a changelog entry.

**Out:** retrieving or adding sources to a shelf (the user supplies
them, as today). Deleting the datawizard memory note
`check-cairn-shelf-first.md`, which lives outside this repo and is the
user's to remove once this ships. Any check that fails a session for
searching the web. The legacy `cairn/references/pdf/` shelf of a repo
that has not taken D-047's rename: the notice reads `sources/` only, and
`cairn_validate` already reports the old name.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: When `hooks/session_context.py`'s `build_context` returns a
      context, that context holds one `## Source shelf` part exactly when
      `cairn/references/INDEX.md` has at least one line that begins with
      `- ` at column 0, or `cairn/references/sources/` has at least one
      top-level entry (file or directory, not recursed) whose name does not
      start with `.`. The part sits before the ROADMAP part. It gives the
      count of those INDEX lines and of those shelf entries, and lists the
      shelf entry names in Python `sorted` order, at most 30. When there are
      more than 30, one line names how many more, and otherwise no such
      line appears. It tells the session to read `INDEX.md`, the source's
      note, and the shelf before it searches the web for a cited source.
      Shown by the `hooks/tests` cases that T1 lists.
- [ ] AC2: The primary-sources rule in `skills/shared/validation-doctrine.md`
      and the "References pages" section of `skills/shared/tracking-rules.md`
      each say to read `cairn/references/INDEX.md`, the source's note, and
      `cairn/references/sources/` before a web search for a source, and to
      search the web only for a source not found there. The tracking-rules
      sentence covers any source a session needs, not only scoring or
      algorithmic ones. Shown by the two files' text and hand-run guards in
      `skills/tests`.
- [ ] AC3: The README section "Keeping track of sources" and a `CHANGELOG.md`
      Unreleased entry each describe the session-start shelf notice and the
      shelf-first rule as text the plugin gives sessions, with no claim that
      sessions always follow it.
- [ ] AC4: The profile's `verify` slot is green (both unittest suites, the
      two `claude plugin validate` runs, and `claude plugin test .`).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3, T4
- AC3 → T5
- AC4 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Add `hooks/tests` cases in `TestSessionContext`, seen failing
      first: a shelf with files; notes with no shelf; an absent
      `references/` folder; an `INDEX.md` with no `- ` line and no shelf; a
      shelf of only dot-files; a mix of dot and other entries (dot entries
      left out of the count and list); a subdirectory entry; exactly 30
      entries (no "more" line); 31 entries (the "more" line names 1); and
      the part placed before the ROADMAP part. Assert the heading, counts,
      names, the "more" line, the shelf-first sentence, and absence.
- [x] T2: Implement the part in `hooks/session_context.py`, placed before
      the ROADMAP part so the existing shedding never drops it, with the
      30-name cap as a named constant. Update the module docstring.
- [x] T3: Add the shelf-first clause to the primary-sources rule in
      `skills/shared/validation-doctrine.md` and one sentence to
      tracking-rules "References pages". Keep the doctrine module inside
      the budget its header states.
- [x] T4: Add hand-run guards for both clauses to the `skills/tests` file
      that covers the references rules, registered in the mutation
      harness, each seen red with its clause removed.
- [x] T5: Add the README sentence and the CHANGELOG Unreleased entry.
- [x] T6: Run the `verify` slot and the hand-run `skills/tests` suite.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — a change to the session-start hook's output, a runtime surface.
- 2026-10-19: question set: none posed — the user said in chat on 2026-10-19 that the agent decides and asks only what it cannot decide without the user; nothing here needs the user.
- 2026-10-19: plan gate chose a hook notice plus a doctrine clause over a doctrine clause alone because the datawizard miss came in plain conversation, where no rulebook text loads; falsified by a session that misses the shelf with the notice in its context.
- 2026-10-19: plan gate chose listing shelf entry names capped at 30 over listing every INDEX line because shelves reach 51 files (circumplex) and INDEX lines carry long descriptions, and the hook's text competes with the active milestones for its 30,000-character budget; falsified by a session that cannot match a cited paper to a capped or unlisted name.
- 2026-10-19: collision check: D-047 (the shelf's name) and D-063 (the hook's read-bound) read whole, neither conflicts; no ROADMAP row covers this; archived M078 to M103 built the references pages and set no shelf-first rule.
- 2026-10-19: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: criteria audit (full, fresh Opus reader): 9 findings, all taken narrower — AC1 scoped to a returned context, top-level entries, column-0 `- ` lines, Python `sorted`, a "more" line only past 30, and placement before the ROADMAP part; its fixtures moved to T1 and widened to 10 cases (instrument property); the legacy `pdf/` shelf went to Out; AC2 says the rulebook sentence covers any source; AC3 describes the notice and rule text, not session compliance. AC4: none.
- 2026-10-19: origin: the datawizard session web-searched Brincks et al. (2017) while `cairn/references/brincks2017.md` and `sources/brincks2017.pdf` were on its shelf, then saved a per-repo memory note in place of a plugin fix (GP4).
- 2026-10-19: T1 done: `TestSessionShelf`, 10 cases; 7 failed first on the missing heading, the 3 absence cases passed as silent controls.
- 2026-10-19: T2 done: `shelf_section` and `SHELF_MAX_NAMES = 30` in `hooks/session_context.py`, appended before the ROADMAP part; the 10 cases pass and hooks/tests is OK; rendered for datawizard (2 pages, 2 entries) and circumplex (36 pages, 51 entries, "and 21 more").
- 2026-10-19: catch-up: status set to in-progress and the branch recorded with T3's commit; step 1 skipped it before the T1-T2 commit.
- 2026-10-19: T3 done: shelf-first clause in the primary-sources rule (`validation-doctrine.md`, now 101 lines and 6,638 bytes, under its 115 and 8,000 budget) and a "Shelf first." paragraph in tracking-rules "References pages".
- 2026-10-19: T4 done: `TestShelfFirst` in `test_references_pages.py`, 4 one-line anchors, each registered in the mutation harness and red when blanked; skills/tests OK.
- 2026-10-19: T5 done: README "Keeping track of sources" bullet and CHANGELOG Unreleased entry, written in plain English to pass the lint hook.
- 2026-10-19: T6 done: verify green (scripts 0, hooks 0, both validates 0, plugin test 0 fail); skills/tests OK; cairn_validate all checks passed.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
