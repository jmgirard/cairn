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

- [x] AC1: In `paneLines`, each candidate line's `full` is its row's text as `candidateTexts` reads it (HTML comments removed), after the `- ` and any exact `[high] `, `[low] `, or `[parked] ` token, trimmed at both ends as the short title is, and the line's drawn text stays the short title. A `pane.test.tsx` test asserts each line's `full` and text against values written out by hand, over rows that carry a detail after `: `, a ` — added` tail, neither, an empty short title, each of the three tokens, one inexact token (`[High] `), and leading and trailing whitespace including U+FEFF.
- [x] AC2: A `pane.test.tsx` test asserts `info` and `full` on a candidate line whose short title is empty and whose text is not, and asserts neither on a `- ` row and a `- [parked] ` row.
- [x] AC3: For each fixture that `reader.test.ts` and `test_status_fixtures.py` read, `candidateRows` (through `loadCairn`) gives each row the `text` that the fixture's expected `candidates` writes out by hand, and `python_candidates` gives the same. `test_python_candidates_cut_and_trim_edges` and its `reader.test.ts` twin assert `text` for the same rows.
- [x] AC4: The pane atom's `shape` tag in `register.tsx` is not `pane-7`, and the `candidates` entry type in `types/index.d.ts` names `text: string`. Neither `cairn/DESIGN.md` nor `types/index.d.ts` names `pane-7` as the current tag or calls a candidate entry only its priority and short title.
- [x] AC5: README.md's pane paragraph (~line 336), the `cairn/DESIGN.md` hover-card entry (~lines 505-520), the M290 entry's card sentence in `CHANGELOG.md`'s Unreleased section, and the comments at `pane.ts:76-81` and `register.tsx:403-409` say that a candidate row's card holds the row's whole text, and none of them says it holds only the title.
- [x] AC6: The profile's five `verify` checks pass on the review head.

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

Pass 1, 2026-10-19, head 40598619 (the PR-URL commit); main at ce40bc7b is an ancestor, so no sync was needed.

- AC1: `claude plugin test .` (exit 0, 2336 pass, 0 fail) passes "a candidate line's card holds the row's whole text (M293) > each line keeps its short title and holds its whole text". Its rows run through `candidateRows` and cover a `: ` detail, a ` — added` tail, neither, `[high]`, `[low]`, `[parked]` with an inline comment removed, `[High] ` kept in the text, a leading BOM with trailing tab and BOM trimmed, and a trailing U+001F kept. The empty-title row is checked in the AC2 test. At implement the test failed against `full = row.title` (work log T2).
- AC2: the same run passes "a row with an empty short title opens its card from ⓘ" (`info: true`, `full` the row text) and "a row with no text has no card" (`- ` and `- [parked] `: `full` and `info` both undefined).
- AC3: the same run passes "reader over every fixture … the pane's milestones and next step match expected.json" for all fixtures, including the 8 whose expected `candidates` now carry `text`, and the M251 table rows with `text`, the leading-BOM row included. `python3 -m unittest scripts.tests.test_status_fixtures` ran 12 tests OK, including the per-fixture `python_candidates` comparison and `test_python_candidates_cut_and_trim_edges`, which asserts `text` for the same four rows as its `reader.test.ts` twin.
- AC4: `register.tsx:146` holds `shape: 'pane-8'`, and `types/index.d.ts:81` holds `title: string; text: string`. `git grep -n pane-7 -- cairn/DESIGN.md types/index.d.ts` exits 1 (no match), and a grep for "its priority and its short title" over both exits 1.
- AC5: read at the head: README.md:338-339 ("That card holds the row's whole text after the priority token… The row itself shows only its short title."), DESIGN.md:508-510 and 518-519 (the hover-card entry, `full` and `info`), CHANGELOG.md:121-123 (the M290 entry's card sentences), pane.ts:79-80, and register.tsx:405-406 each say the candidate card holds the row's whole text. None of them says it holds only the title.
- AC6: from the repo root, each exit checked: `scripts/tests` 428 OK (21 skipped), `hooks/tests` 193 OK, both `claude plugin validate` runs exit 0, `claude plugin test .` exit 0 with 2336 pass and 0 fail.

Consistency gate: `cairn_validate.py` exit 0, all checks passed. No principle changed, so `cairn_impact` is skipped. Profile slot: the verify checks pass on the review head (AC6). The marketplace validate output holds no `version` warning (grep exit 1). CHANGELOG: the unreleased ⓘ-card entry now says what the card holds, and the added lines carry no milestone id. That entry is edited rather than a new one added, since no release shipped the card.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: 29 `pane.test.tsx` candidate literals lacked `text`, so they set `info` with no `full`, a state the reader cannot produce — fix now, fixed cc7cd3ae (all 30 literals gain `text`).
- diff-bug #2: a drawn row whose started token is not counted (an empty title, a closed `#n`, a done M id) shows the token in its card — reject, planned change: the operator chose the whole row, and a dead token is `/cairn-triage`'s to remove (D-166).
- diff-bug #3: the new M293 block sat between the M291 comment and its `describe` — fix now, fixed cc7cd3ae.
- diff-bug #4: no render-level test draws ⓘ on an empty-title row — reject, planned change: AC2 sets the test at `paneLines`, and `infos()` in register.tsx reads only `info` and `full`, which that test asserts.
- diff-bug #5: removing an inline HTML comment leaves its spaces (`trigger  — added`) — reject, style: `candidateTexts` has always kept them, and the card shows the row as the reader reads it.
- diff-bug #6: one reader.test.ts row lists `text` before `title` — reject, style (`toEqual` ignores key order; kept so the Edit tool leaves its `\u001F` escape text alone).
- diff-bug #7: edited DESIGN, CHANGELOG, and pane.ts lines were not rewrapped — fix now, fixed cc7cd3ae.
- ripple #1: the same `text`-less literals as diff-bug #1 — fix now, fixed cc7cd3ae.
- ripple #2: DESIGN.md's `candidateRows` sentence named only priority and short title — fix now, fixed cc7cd3ae.
- ripple #3: CHANGELOG's M286 entry lists the whole-text card lines without candidate rows — reject, false: the M290 entry moved candidate cards to ⓘ and now says what they hold.
- ripple #4: README's "beside the info icon that opens the row's card" for ✎ rows — reject, false: the reviewer found it still holds.
- prior-review #1: the `text`-less literals, also named by Copilot on PR #306 — fix now, fixed cc7cd3ae.
- prior-review #2: DESIGN.md:510 ran 98 characters (M292's wrap fix) — fix now, fixed cc7cd3ae.
- prior-review #3: the pane.ts comment split mid-sentence (PR #264's unclear-comment note) — fix now, fixed cc7cd3ae.
- prior-review #4: CHANGELOG.md:123 ran long — fix now, fixed cc7cd3ae.
- blame-history #1: the card shows a dead started token on a drawn row — reject, planned change (as diff-bug #2).
- blame-history #2: D-189's rejected alternative rests on "the line's hover card shows the whole title" — reject, false: the card still shows the whole title, as the start of the row's text.
- blame-history #3: a tall card opens past the pane's top — reject, already recorded as item (3) of "Fix cut and odd names on the pane card" at the live look.
- blame-history #4: the M258 started-token test dropped its priority check — fix now, fixed cc7cd3ae (it compares priority and title).
- blame-history #5: `info` now keys on the text, not the title (M290) — reject, planned change (AC2).
- blame-history #6: the pane.ts and register.tsx comments split M286's sentences — fix now, fixed cc7cd3ae.
- blame-history #7: the same `text`-less literals — fix now, fixed cc7cd3ae.

After the fixes: the five verify checks pass again (scripts 428 OK, hooks 193 OK, both validates exit 0, mod tests 2336 pass 0 fail), and `cairn_validate.py` passes.
