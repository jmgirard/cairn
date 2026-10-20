<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M292: Candidate row titles are one short sentence that fits the cairn pane

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — adopting repos' sessions write and retitle candidate rows by the rulebook and `/cairn-triage`
- **Branch/PR:** m292-candidate-title-format, https://github.com/jmgirard/cairn/pull/304

## Goal

A candidate row's short title says what the work would do in one sentence of at least 5 words that fits the desktop cairn pane's line, ending with its GitHub issue number when it has one.

## Scope

**In:** the rule in tracking-rules "Candidate short title"; `/cairn-triage`'s
`retitle` trigger and new-title bounds; the README passage and the
`/cairn-init` ROADMAP skeleton comment that restate them; a CHANGELOG entry;
a D-entry recording the user's decision past D-108's door.

The cap derives from the pane's layout (`hooks/status/pane.ts:806`,
`hooks/status/register.tsx:228` and `:477`, M205's 44-column docked desktop
pane). A candidate line sits outside the bordered card: 44 columns, less 2
for its indent and 2 for its mark and space, leaves 40 at rest. Under the
pointer the info glyph (2) and ✎'s slot (`PLAN_SLOT` 4) leave 34, and the
line's hover card then shows the whole title. The terminal's width varies.

**Out:** retitling this repo's existing rows → the user's next
`/cairn-triage` run (question set). A `cairn_validate` check on titles →
none (D-163 declined one at the user's choice). Wrapping or widening the
pane's candidate line → not planned; the line's hover card already shows
the whole title.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md` "Candidate short title" tells whoever writes a candidate row to open it with a short title that says what the work would do in one sentence with no ending period, of at least 5 words and at most 40 characters, a wide character such as a CJK character counting as 2, so that the desktop cairn pane's docked candidate line shows it whole while the pointer is elsewhere. Words are whitespace-separated runs, not counting a trailing issue reference; the 40 characters include it. It says that a row written for one or more of the repo's GitHub issues ends its title with an issue number in parentheses, `(#N)`, or `(#N, #M)` when that fits, and that an issue absorbed into an existing row later goes in the row's detail and leaves its title as it is. It keeps the rules that each title differs from every other row's title and is followed by `: `, and each title the paragraph offers as one to write meets these bounds. Verified by reading the paragraph, and `grep -n 'few words' skills/shared/tracking-rules.md` returns no match.
- [ ] AC2: `/cairn-triage` proposes `retitle` for a candidate row whose short title has fewer than 5 words or more than 40 characters, counted as AC1 counts them, in place of the over-60-code-points trigger; the empty, shared, and icon triggers stay. Each new title it proposes meets AC1's bounds, holds no `: `, ` — `, or icon, and ends with AC1's issue reference, as AC1 allows it, when the row's text names a GitHub issue of the repo, by an `/issues/N` URL or as `#N` that the row calls an issue (a ` — started #<n>` token is not one). The `retitle` table row no longer says "a few words". Verified by reading the `retitle` table row and the Title class in `skills/cairn-triage/SKILL.md`, and `grep -n -E '60 code points|a few words that name' skills/cairn-triage/SKILL.md` returns no match.
- [ ] AC3: README.md's candidate-title passage and the ROADMAP skeleton comment in `skills/cairn-init/SKILL.md` state AC1's format and AC2's trigger, and each title they offer as one to write, placeholders such as `short title` aside, meets AC1's bounds. Verified by reading both, and `grep -rn -E 'few words that name|longer than 60|60 code points' README.md skills --include='*.md'` returns no match.
- [ ] AC4: CHANGELOG.md's `## Unreleased` heading carries one entry that describes the new title format and the new retitle trigger, and says that existing rows keep their titles until a `/cairn-triage` pass retitles them.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks

- [x] T1: Rewrite tracking-rules "Candidate short title" (`skills/shared/tracking-rules.md:259-270`) to AC1, with example titles inside the bounds in place of `ordinal REML: …` and `Home Button edges`; re-seed the rulebook-mass baseline in `skills/milestone/SKILL.md:120` and its two hand-run pins (`skills/tests/test_cost_audit_line.py`, `skills/tests/test_mutation_harness.py`).
- [x] T2: Rewrite the `retitle` table row and the "Title → `retitle`" class in `skills/cairn-triage/SKILL.md` (~lines 283 and 325-340) to AC2.
- [x] T3: Rewrite README.md's passage (~lines 399-410) and the skeleton comment in `skills/cairn-init/SKILL.md` (~lines 188-197) to AC3.
- [x] T4: Add the CHANGELOG entry under `## Unreleased`, and append a D-entry that annotates D-108, D-163, and D-164 (IP4: no edit to them), naming the user's decision at the M292 question set and the pane-width basis of the cap.
- [x] T5: Run both gating suites, `claude plugin validate`, the hand-run `skills/tests`, and `cairn_validate`; grep the repo for the old phrasing ("few words", "60 code points", "60 characters") outside history records and fix any live hit.

## Work log

- 2026-10-19: created by /milestone-plan.
- 2026-10-19: tier check: milestone — a rule change to the rulebook and `/cairn-triage` with a design decision (the length bound).
- 2026-10-19: collision check: D-163 and D-164 set the current title rule (extended here, not superseded); D-108 bars new rules on how records are written without a shipped defect, so the question set asked; no candidate, planned, or archived milestone overlaps. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: question set: proceed past D-108's door — go ahead, recorded as the user's decision in a new D-entry.
- 2026-10-19: question set: length check — the user wants a title that fits a standard pane width without an ellipsis, avoiding 3-word titles but not a paragraph; the plan took a 5-word floor and a 40-character cap from the pane's layout (Scope). The user's first ask of up to 15 words, and their 52-character example, exceed that cap; the answer put pane fit first.
- 2026-10-19: question set: existing rows — left for the user's next `/cairn-triage` run.
- 2026-10-19: criteria audit (full mode), round 1: 10 findings, all taken — titles offered as examples meet the bounds, uniqueness and `: ` kept, a later issue leaves the title alone, words defined, no ending period, issue forms listed, the table row's "a few words" named, `## Unreleased` named; the cap's trade-off goes to the D-entry.
- 2026-10-19: criteria audit (full mode), round 2 over the answers: 6 findings, all taken — the cap is 40 at rest, not 36 (candidate lines sit outside the card), counted in columns with wide characters as 2, scoped to the desktop's docked pane; offered titles only; AC2 takes AC1's reference form; the dropped 15-word range stated in the log above and in the handoff.
- 2026-10-19: plan gate chose a 40-character cap, the docked desktop pane's room at rest, over 34 (room under the pointer) because the hover card shows the whole title under the pointer; falsified by a title of 40 or fewer characters cut with an ellipsis at rest in a docked desktop pane in a real session.
- 2026-10-19: plan gate chose the pane-width cap over the user's first 5-15 word range because the user's answer put pane fit first; falsified by the user finding titles at the cap too terse.
- 2026-10-19: plan gate chose to leave an issue absorbed later in the row's detail over changing its title, so double-quoted mentions, `/hotfix` matching, and live milestone quotes keep matching; falsified by a user asking for every issue number in the title.
- 2026-10-19: T1 done: tracking-rules "Candidate short title" states the one-sentence, 5-word, 40-character format with `(#N)` and new example titles; rulebook baseline re-seeded to 760 lines / 73,320 bytes at its three sites; verify green (5/5).
- 2026-10-19: T2 done: `/cairn-triage`'s Title class flags fewer than 5 words or more than 40 characters, new titles take the sentence bounds and the issue reference, and the `retitle` table row says one sentence; AC2's grep finds nothing; verify green (5/5).
- 2026-10-19: T3 done: README's passage states the format, the issue reference, and the triage trigger, its two `Pane refresh lag` examples became `Fix the pane's slow refresh`; the `/cairn-init` skeleton comment states the bounds with the skewness example; AC3's grep finds nothing; verify green (5/5).
- 2026-10-19: T4 done: CHANGELOG `## Unreleased` entry "Candidate short titles are one short sentence"; D-189 appended, annotating D-163 and D-164 and passing D-108's door by the user's decision.
- 2026-10-19: T5 done: verify green (5/5), hand-run `skills/tests` green (914 tests), `cairn_validate` green; the old-phrasing sweep outside history records hits only CHANGELOG.md:320, the released 2.1.0 entry, left as history.
- 2026-10-19: claim audit: 44 claims read, 3 corrected — skills/shared/tracking-rules.md, README.md, CHANGELOG.md, skills/cairn-init/SKILL.md (fit stated as what the cap is sized to; skeleton names triage's real trigger; README gains the later-issue sentence); 2 declined (wide-character count is a writer's convention; a retitle may add every named issue since it rewrites mentions); re-read holds; rulebook baseline re-seeded to 760 lines / 73,350 bytes; verify green, `skills/tests` green.
- 2026-10-19: status review; handed to /milestone-review.
