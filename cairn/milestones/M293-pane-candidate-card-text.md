<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M293: The cairn pane's ⓘ card shows a candidate row's whole text

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane is the mod that adopters see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m293-pane-candidate-card-text, https://github.com/jmgirard/cairn/pull/306   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

On the desktop, the card that a candidate row's ⓘ opens in the cairn pane shows the row's whole ROADMAP text, not only its short title.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `candidateRows` in `hooks/status/reader.ts` gives each row its text after the priority token, as `candidateTexts` reads it, trimmed as the short title is (`text`). `pane.ts` sets a candidate line's `full` to that text, and its `info` when the text is not empty. The pane atom's shape tag moves past `pane-7`. `types/index.d.ts` names `text`. The Python twin `python_candidates` in `scripts/tests/test_status_fixtures.py` and the fixtures carry `text`. README, DESIGN, CHANGELOG, and the code comments say what the card holds.

**Out:** the line itself, which keeps the short title (M292). The terminal, which draws no card. A card that opens upward past the pane's top, and one that closes when the pointer moves onto it: the parked rows "Fix cut and odd names on the pane card" (item 1) and "Gaps only the app or mod API can close" (item 5) hold these, and the live look adds to them what it sees.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: In `paneLines`, each candidate line's `full` is its row's text as `candidateTexts` reads it (HTML comments removed), after the `- ` and any exact `[high] `, `[low] `, or `[parked] ` token, trimmed at both ends as the short title is, and the line's drawn text stays the short title. A `pane.test.tsx` test asserts each line's `full` and text against values written out by hand, over rows that carry a detail after `: `, a ` — added` tail, neither, an empty short title, each of the three tokens, one inexact token (`[High] `), and leading and trailing whitespace including U+FEFF.
- [ ] AC2: A `pane.test.tsx` test asserts `info` and `full` on a candidate line whose short title is empty and whose text is not, and asserts neither on a `- ` row and a `- [parked] ` row.
- [ ] AC3: For each fixture that `reader.test.ts` and `test_status_fixtures.py` read, `candidateRows` (through `loadCairn`) gives each row the `text` that the fixture's expected `candidates` writes out by hand, and `python_candidates` gives the same. `test_python_candidates_cut_and_trim_edges` and its `reader.test.ts` twin assert `text` for the same rows.
- [ ] AC4: The pane atom's `shape` tag in `register.tsx` is not `pane-7`, and the `candidates` entry type in `types/index.d.ts` names `text: string`. Neither `cairn/DESIGN.md` nor `types/index.d.ts` names `pane-7` as the current tag or calls a candidate entry only its priority and short title.
- [ ] AC5: README.md's pane paragraph (~line 336), the `cairn/DESIGN.md` hover-card entry (~lines 505-520), the M290 entry's card sentence in `CHANGELOG.md`'s Unreleased section, and the comments at `pane.ts:76-81` and `register.tsx:403-409` say that a candidate row's card holds the row's whole text, and none of them says it holds only the title.
- [ ] AC6: The profile's five `verify` checks pass on the review head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T1, T3
- AC4 → T1, T4
- AC5 → T4
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: `reader.ts`: add `text` to `CandidateRow` from `candidateTexts`, trimmed with the trim `shortTitle` uses (`String.prototype.trim`, reader.ts:636). Bump the pane atom's shape tag in `register.tsx:145`. Add `text` to `types/index.d.ts:80` and its comment. Update the tests that compare whole `CandidateRow` objects (reader.test.ts M251 table ~264, M258 ~297).
- [x] T2: `pane.ts` (~line 813): write the AC1 and AC2 tests first in `pane.test.tsx` (the M286 AC9 block, ~6126), show them red against `full = row.title`, then set `full` to `row.text` and `info` when it is not empty, and show them green. Update the M286 AC9 block's hand-written candidate values.
- [x] T3: add `text` to `python_candidates` and to each fixture's expected `candidates`; regenerate `fixtures.gen.ts` with `gen_fixtures.py`; add `text` to `test_python_candidates_cut_and_trim_edges` and its `reader.test.ts` twin.
- [x] T4: README, DESIGN (the hover-card entry, and the `pane-7` mentions near lines 390, 556, 799), and the code comments that AC5 names. Edit the unreleased M290 CHANGELOG entry's card sentence rather than adding an entry.
- [x] T5: run the five `verify` checks. Ask the operator for the live look: the desktop pane in circumplex, the pointer over the ⓘ of a long row and of the first row. Record what they see, and add a cut or closing card to the parked rows that Out names.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — the change alters what the pane's candidate card shows, which M290 documents as the short title, so no documented behavior is restored.
- 2026-10-19: collision check: no candidate, planned, or dropped record overlaps; M286 (hover cards) and M290 (the ⓘ on candidate rows) shipped the card this extends; the parked rows "Fix cut and odd names on the pane card" and "Gaps only the app or mod API can close" hold the card's upward-cut and close-on-move edges and stay as they are.
- 2026-10-19: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: lessons surfaced: M193/M284 (a state value layout change needs a new `shape` tag, and `types/index.d.ts` follows by hand), M286 (an absolute card opens upward), M290 (hover needs a live look), M201/M213 (look in a real cairn repo, never a scratch folder).
- 2026-10-19: criteria audit (full mode, fresh Opus reader): 7 findings, all taken toward the narrower promise. AC1's test cases now vary trim edges, all three tokens, an inexact token, and an empty title, and AC1 reads the text as `candidateTexts` does (comments removed). AC2 asserts `info` and `full`, not drawing. AC3 binds `candidateRows`, and the trim twins assert `text`. AC4 gains the stale `pane-7` and type-comment mentions. AC5 is narrowed from a grep over 22 mostly unrelated lines to the named sites that state the card's content.
- 2026-10-19: question set: card text — the whole row after its priority token (over the row without its ` — added` tail).
- 2026-10-19: question set: live look at implement — granted, in circumplex, pointer over a long row's ⓘ.
- 2026-10-19: plan chose the whole row text over the row cut before its ` — added` tail because the operator asked for the entire row; falsified by a live look where long cards are cut or unreadable in the docked pane.
- 2026-10-19: changelog: edit the unreleased M290 entry's card sentence, since no release shipped that card.
- 2026-10-19: implement started on branch m293-pane-candidate-card-text; untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-19: T1 done: `CandidateRow.text` is `text.trim()` after the token; shape tag `pane-8`; `types/index.d.ts` names `text`. The M251 table gained `text` and a leading-BOM row; the M258 started-token test now compares titles, since a token is part of the text.
- 2026-10-19: T2 done: the M293 tests in `pane.test.tsx` failed against `full = row.title` (full was the title; the empty-title row had no card) and pass with `full = row.text`, `info` when text is not empty. The M286 AC9 idle rows gained `text`. Other test literals without `text` stay as written, since no test reads their card.
- 2026-10-19: T3 done: 60 expected candidate entries in 8 fixtures gained `text` through a scratch script that read each fixture ROADMAP on its own and checked every title against the one written; a script, not Edit, because of the count (a departure from the rulebook's Write/Edit rule). `python_candidates` gives `text`; its trim-edge test gained the leading-BOM row, built from code points.
- 2026-10-19: T4 done: README, DESIGN (card entry, `info`, three `pane-7` mentions), the M290 CHANGELOG sentence, and the pane.ts and register.tsx comments say the card holds the whole row. A `git grep` for card-with-title phrasing and `pane-7` over those files finds nothing stale.
- 2026-10-19: verify green: scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2336 pass 0 fail; `gen_fixtures.py --check` clean.
- 2026-10-19: T5 done: live look by the operator in circumplex's docked pane (the plugin links to this checkout): the card holds the whole row text, and a tall card's top runs past the pane's top. Recorded as item (3) of the parked row "Fix cut and odd names on the pane card", as Out names; the row stays parked for review hygiene to judge.
- 2026-10-19: claim audit: 25 claims read, 3 corrected — reader.test.ts (the glmmTMB rows are now second and third), CHANGELOG.md and README.md (the card's text has HTML comments removed and is plain text, not the row "as written").
- 2026-10-19: implement done; status review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
