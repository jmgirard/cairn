# M208: A fuller look for the cairn pane

- **Status:** review
- **Priority:** normal
- **Depends on:** M207
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane draws in every adopter's session
- **Branch/PR:** m208-pane-look

## Goal

Give the cairn pane a fuller look, picked by the operator from browser prototypes, on the desktop and in the terminal.

## Scope

**In:** Three additions to the pane's look. Each active milestone's head line ends with the band's percent for that row, in a tail part the title's cut never reaches (the operator dropped the track bar at T1). The `Tasks` and `Criteria` headings gain a short meter beside their counts. Section headings are set off from their items by a rule or a mark, and the `Next` line is set off from the queue. The operator picks the form of each from 2 or 3 browser prototypes in a dark and a light block. The pane keeps one line per item, with the goal wrapping (M205). The line Box gains `minWidth: 0`, from "Pane follow-ons (M205 review)". README, DESIGN, CHANGELOG, and the header comments of `pane.ts` and `register.tsx` follow.

**Out:** The fixed phase colors in light, colorblind, and ANSI themes stay in "Band label colors in other themes". The other "Pane follow-ons (M205 review)" items stay there. Clickable actions stay in "Status mod follow-ons". Pane widths under 44 columns are not swept.

## Acceptance criteria

- [x] AC1: The head line of each active milestone whose milestone file can be read ends with the percent that the band computes for the same row (`flowOf` in `band.ts`), and draws no flow track. A milestone with no readable file draws no percent on its head line and keeps its `no milestone file` line. `pane.test.tsx` cases assert this on both surfaces for an `in-progress` row, for a `review` row whose `## Acceptance criteria` holds an open box inside an HTML comment and at least one checked box outside it, so that the band's percent differs from the percent over the pane's items, and for a row with no file. A case at `bodyColumns` 44 with a title longer than the pane asserts that the percent sits in a `<id>-head-tail` Box with `flexShrink: 0` after the `<id>-head-text` Box. The AC7 live look shows that the percent stays whole when the title is cut.
- [x] AC2: The `Tasks` and `Criteria` headings each draw a meter beside their `checked/total` count, in the form the operator picked at T1. `pane.test.tsx` cases assert the meter for a partly checked, an all-checked, and an all-open section on both surfaces. If the operator picks no meter at T1, the headings draw none, and a case asserts that.
- [x] AC3: Each section heading (`Goal`, `Tasks`, `Criteria`, `Work log`, `Workable`, `Waiting`, `Candidates`) and the `Next` line draw in the set-off form the operator picked at T1. `pane.test.tsx` cases assert the form for each of these headings and the `Next` line on both surfaces. If the operator picks no set-off form at T1, they draw as before, and a case asserts that.
- [x] AC4: Over the `pane-full` fixture and an idle fixture with candidate rows, at `bodyColumns` 44, each line's indent plus lead width plus tail width, each counted by `width()` in `band.ts` summed over its spans, is at most 44, where a line with no tail counts 0. The Box keyed with each line's key carries `minWidth: 0`. A `pane.test.tsx` case asserts both on both surfaces.
- [x] AC5: README's "The cairn pane" section, the pane paragraph of `cairn/DESIGN.md`, and the header comments of `pane.ts` and `register.tsx` describe the new look. CHANGELOG's Unreleased section has an entry for it.
- [x] AC6: The four commands of the verify slot in `cairn/PROFILE.md` each exit 0.
- [ ] AC7: At a live look the operator accepts the desktop pane docked at 44 columns and at a wider dock, and the terminal pane.

## Coverage

- AC1 → T2
- AC2 → T1, T3
- AC3 → T1, T3
- AC4 → T4
- AC5 → T5
- AC6 → T2, T3, T4, T5
- AC7 → T1, T6, T7

## Tasks

- [x] T1: Build 2 or 3 browser-pane prototypes of the pane with all three additions, each in a dark and a light block, served with `python3 -m http.server` from the scratchpad (LESSONS M201, M204). The operator picks the meter and the set-off form. A work-log line records the picks.
- [x] T2: Give `PaneLine` a tail part and draw it in register.tsx as a `<key>-tail` Box with `flexShrink: 0`. Pass each active row's band counts to the pane, and end each head line with `flowOf`'s percent. Add the AC1 cases, with an in-memory review row whose criteria hold a comment box and a checked box.
- [x] T3: Draw the meters and the set-off headings and `Next` line in the picked forms. Add the AC2 and AC3 cases.
- [x] T4: Give the line Box `minWidth: 0`. Add the AC4 case.
- [x] T5: Update README, the DESIGN pane paragraph, the CHANGELOG, and the header comments of `pane.ts` and `register.tsx`.
- [ ] T6: Do the live look in a new Code session (LESSONS M195), docked at 44 columns, at a wider dock, and in the terminal, at the merge question as M205 did.
- [x] T7: Make the look changes the operator names after the declined live look, then hand back to review.

## Work log

- 2026-10-04: created by /milestone-plan.
- 2026-10-04: collision sweep: the `minWidth: 0` item of "Pane follow-ons (M205 review)" is absorbed, and hygiene trims it from the row. Its other items stay. No D-entry conflicts (D-143 read). Inbox: 0 open issues, 0 open PRs.
- 2026-10-04: criteria audit (full mode, user-facing tier, fresh Opus reader) returned 12 findings over M207 to M209, all taken. Here: AC1 draws the band's own track and percent, with a review-row case whose comment box makes the two counts differ. AC4's sweep starts at the 44-column dock, since a head line with a track needs about 32 columns before its title. AC4 binds lead widths and `minWidth: 0` and leaves the drawing to AC7. AC2 and AC3 cover a pick of none.
- 2026-10-04: question set: additions. The operator chose all three: the flow track on each milestone, meters by the counts, and set-off headings with the `Next` line. Falsified if the live look shows the pane too busy to read.
- 2026-10-04: question set: look pick. The run stops once at T1 for the operator to pick from browser prototypes (recommended), over the agent picking and showing the look only at the merge. The T1 pick and the T6 live look are stops for the operator's eyes on the closed list.
- 2026-10-04: implement started on branch `m208-pane-look`. The untracked `tsconfig.json` stays unstaged.
- 2026-10-04: T1 prototypes served from the scratchpad on port 8765: three variants (square meters with solid rules; thin bars with accent marks; braille meters with dotted leaders), each in desktop dark and light at 44 columns, terminal dark, and an idle pane with candidates. The real `trackSvg` and `brailleSpans` output is drawn there. At 44 columns the track on the head line left the title no room, so the page also compares the track on its own line under the head line. Stopping for the operator's pick.
- 2026-10-04: T1 pick: the percent alone at the end of the head line, with no track bar (the operator's own answer, over the track on its own line and over the planned track on the head line). Meter: variant 1's eight squares. Headings: variant 2's blank row, orange `▎` accent, and gray uppercase label, with the Next command in an orange pill.
- 2026-10-04: re-audit: AC1 (full) — of the percent-only wording: no fixture row makes the band's percent differ from the pane's in the phase that sets it, and a long title at 44 columns could cut the percent; Scope, T2, and the AC4 work-log reason still name the track.
- 2026-10-04: re-audit: AC1 (full) — of the fixed wording: the review-row probe passes vacuously with no checked box outside the comment, the "outside the truncate-end element" case names no single element, the "left whole" claim is the live look's to show, and AC4 measures the lead and not the tail. This is the second re-audit line on AC1, so the wording goes to the operator.
- 2026-10-04: substantive amendment: AC1 now reads "The head line of each active milestone whose milestone file can be read ends with the percent that the band computes for the same row (`flowOf` in `band.ts`), and draws no flow track. A milestone with no readable file draws no percent on its head line and keeps its `no milestone file` line. `pane.test.tsx` cases assert this on both surfaces for an `in-progress` row, for a `review` row whose `## Acceptance criteria` holds an open box inside an HTML comment and at least one checked box outside it, so that the band's percent differs from the percent over the pane's items, and for a row with no file. A case at `bodyColumns` 44 with a title longer than the pane asserts that the percent sits in a `<id>-head-tail` Box with `flexShrink: 0` after the `<id>-head-text` Box. The AC7 live look shows that the percent stays whole when the title is cut." The operator chose it at the stop. Scope's In line and T2 now name the percent and the tail in place of the track. AC4's 44-column floor stands as the docked width, not for a track.
- 2026-10-04: re-audit: AC4 (full) — of the tail-width wording over widths 44 to 120: with no track, no pane line varies with `bodyColumns`, so the sweep cannot fail; tail width was undefined, and "line Box" was ambiguous among the lead, text, and tail Boxes.
- 2026-10-04: re-audit: AC4 (full) — of the 44-column wording: reachable and sound, with two naming points: name the `candidates` fixture, and say the `minWidth` holds on each line of both fixtures. This is the second re-audit line on AC4. The agent wrote the audited wording unchanged rather than churn it again, and the AC4 case meets the narrower reading: it runs over `pane-full` and `candidates` and checks every line.
- 2026-10-04: substantive amendment: AC4 now reads "Over the `pane-full` fixture and an idle fixture with candidate rows, at `bodyColumns` 44, each line's indent plus lead width plus tail width, each counted by `width()` in `band.ts` summed over its spans, is at most 44, where a line with no tail counts 0. The Box keyed with each line's key carries `minWidth: 0`. A `pane.test.tsx` case asserts both on both surfaces." It follows from the AC1 amendment the operator chose, and the deliverable is unchanged.
- 2026-10-04: T2, T3, T4 done. `PaneLine` gained `tail`, drawn as a `<key>-tail` Box with `flexShrink: 0`, and the line Box carries `minWidth: 0`. `paneLines` takes the band rows and ends each head line with `flowOf`'s percent. Headings are a gap line, an orange `▎`, and a gray bold uppercase label, with the count and eight `■`/`□` squares for Tasks and Criteria in the phase color. Next shows ` <command> ` in an orange pill with white text. Mod tests: 986 pass. A plant with no `minWidth: 0` and a shrinking tail failed the AC1 44-column case and all four AC4 cases, and was restored.
- 2026-10-04: implement chose to pass the band rows to `paneLines` at render over storing a percent in the pane state, so the fixtures and the Python mirror stay unchanged. Falsified if the band and pane values drift apart in use, since `refresh` writes them in two updates.
- 2026-10-04: T5 done: README's pane section, the DESIGN pane paragraph, a CHANGELOG entry, and the `pane.ts` and `register.tsx` header comments describe the look, and the M207 entries now name the `CANDIDATES` heading. Minor amendment: T6's live look moves to the merge question, as M205's did, so the run asks for the operator's eyes once.
- 2026-10-04: claim audit: 44 claims read, 6 corrected — CHANGELOG.md, README.md, hooks/status/pane.ts, hooks/status/register.tsx, hooks/status/pane.test.tsx
- 2026-10-04: implement done, status `review`, with T6 open: its live look runs at the merge question, and review ticks it there. The corrections say the percent shows only when the file reads, and the empty squares are gray. The agent also renamed the AC4 describe, since the test checks layout props, not the drawn fit. Verify: 397, 174, and 986 tests pass, and validate exits 0.
- 2026-10-04: step-7 decline: the operator declined the merge after the live look and asked to change the look; the changes were not yet named. Status back to `in-progress`, and T7 below holds the change until the operator names it.
- 2026-10-04: T7 change named: the operator said everything looks good except that the colors should be phase-matched.
- 2026-10-04: implement chose the phase-color mapping from the band's `FLOW_COLORS`. A milestone's `▎` marks take its phase's color, as its meters already did. The `▎` marks of Workable, Waiting, and Candidates take plan's blue, since their rows are planned or not yet planned. The Next pill takes the color of the phase its command runs: plan blue, implement orange, review green. The head line's percent stays gray, as the band's is. Falsified if the operator reads the queue's blue as a milestone state at the live look.
- 2026-10-04: T7 done. The AC3 cases now assert the accent color per heading, with two M081 review headings added, and the pill color for a review, an implement, and a plan command; the 14 non-orange cases failed on the old colors before the change. README, the DESIGN pane paragraph, the CHANGELOG entry, and the `pane.ts` header comment name the phase colors. Verify: 397, 174, and 994 tests pass, and validate exits 0.
- 2026-10-04: claim audit: 16 claims read, 0 corrected — CHANGELOG.md, README.md, hooks/status/pane.ts, hooks/status/pane.test.tsx (the lines T7 added; the earlier lines are under the first claim-audit line)
- 2026-10-04: implement done again, status `review`, with T6 open: the live look of the phase colors runs at the merge question.

## Decisions

## Review

Review pass 1, 2026-10-04, on `f4efffd`. Main had not moved since the branch was cut, and no PR existed.

- AC1 evidence: `claude plugin test .` passes 986 of 986. "an in-progress row, a review row, and a row with no file" asserts M080's tail `  44%`, no M082 tail with its `no milestone file` line kept, no `Svg`, and no braille on the three head lines. "a review row takes the band's count, not the pane's items" asserts `review M002  Add the export command  77%` while the pane holds 2 criteria (83% over its items). "at 44 columns a long title leaves the percent in its own unshrinking Box" asserts the lead, text, and tail Box order and the tail's `flexShrink: 0`. All pass on terminal and desktop. The live look under AC7 is the drawing check.
- AC2 evidence: "partly checked and all checked" asserts `▎ TASKS 1/3 ■■■□□□□□` with orange filled squares and `subtle` empty ones, and `▎ TASKS 1/1 ■■■■■■■■` in green. "all open" asserts `▎ CRITERIA 0/1 □□□□□□□□` in `subtle` with no filled square. Both pass on both surfaces. The operator picked the squares at T1.
- AC3 evidence: seven heading cases (`GOAL`, `TASKS`, `CRITERIA`, `WORK LOG`, `WORKABLE`, `WAITING`, `CANDIDATES`) assert the gap row before each, the orange `▎`, and the gray bold uppercase label. "the Next command sits in an orange pill" asserts ` /milestone-review M081 ` on orange in bold white. All pass on both surfaces. The operator picked the accent form at T1.
- AC4 evidence: the AC4 cases over `pane-full` and `candidates` at `bodyColumns` 44 assert, for every line, indent plus lead plus tail width at most 44 and `minWidth: 0` on the line Box, on both surfaces. A plant without `minWidth: 0` and with a shrinking tail failed these and the AC1 44-column case at implement.
- AC5 evidence: README.md:208-220 describes the look in "The cairn pane", `cairn/DESIGN.md` describes it in the pane paragraph and the `hooks/status/` bullet, the `pane.ts` and `register.tsx` header comments describe it, and CHANGELOG.md:7 is the Unreleased entry.
- AC6 evidence: on `f4efffd` the scripts suite ran 397 OK (21 skipped), the hooks suite 174 OK, `claude plugin validate` exited 0 with the CLAUDE.md warning main has, and `claude plugin test .` exited 0 with 986 passing.
- Consistency gate: `cairn_validate.py` passes. No principle changed. The `generic` profile names no toolchain checks.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: the Next pill's white on orange is about 3.4:1 and not bold, where the band's pill is bold — fix now, fixed f4efffd.
- diff-bug #2: `refresh` writes band and pane apart, so a redraw between them can drop a head line's percent for one frame — follow-up, row "Pane look follow-ons (M208 review)", beside the same item in "Pane follow-ons (M205 review)".
- diff-bug #3: the no-track check looked only for an `Svg`, which the terminal never draws — fix now, fixed f4efffd (no braille on the head lines either).
- diff-bug #4: duplicate ids share the first band row's percent — follow-up, row "Pane look follow-ons (M208 review)", beside the duplicate-id item in "Pane follow-ons (M205 review)".
- diff-bug #5: `minWidth: 0` on the line Box may do nothing in a column parent, so DESIGN credited the cut to it — fix now, fixed f4efffd (DESIGN names the tail's `flexShrink: 0` and the text Box's `minWidth: 0`, and the live look as the drawing check).
- diff-bug #6: the AC1 44-column case and the AC4 cases cannot fail on width, since the render ignores `bodyColumns` — reject, planned change (AC4's amended wording, its re-audit lines, and the renamed describe record this).
- diff-bug #7: the M205 AC2 test matched band rows by id alone — fix now, fixed f4efffd.
- diff-bug #8: the all-open meter case checked no colors — fix now, fixed f4efffd.
- diff-bug #9: a cut command loses its trailing pad, so `…` draws on orange — follow-up, row "Pane look follow-ons (M208 review)".
- diff-bug #10: the percent counts a commented box and the meter does not, so one row can read `77%` over `1/2` — fix now for the docs, fixed f4efffd (README says so); the split itself is AC1's.
- diff-bug #11: the pill is orange for a review command too — reject, planned change (the operator's pick).
- diff-bug #12: the DESIGN `hooks/status/` history stopped at M206 — fix now, fixed f4efffd (M207 and M208 added).
- blame-history #1: two progress numbers on one row — fix now for the docs, as diff-bug #10.
- blame-history #2: more fixed orange and green, wider than M198's use — follow-up, row "Pane look follow-ons (M208 review)", beside "Band label colors in other themes".
- blame-history #3: empty squares used `inactive` where the band's marks use `subtle` — fix now, fixed f4efffd.
- blame-history #4: a blank row before every heading costs rows at the dock — reject, planned change (the operator's pick).
- blame-history #5: the live look is not done — reject, planned change (T6 runs it at this merge question).
- blame-history #6: the "Pane follow-ons (M205 review)" row still lists the `minWidth: 0` item — follow-up, trimmed at post-merge hygiene.
- blame-history #7: the percent depends on two writes, and an empty band draws no percent — follow-up, as diff-bug #2.
- blame-history #8: the pill's padding sits inside the cut text — follow-up, as diff-bug #9.
- blame-history #9: README and CHANGELOG now say `CANDIDATES` where the M207 archive says `Candidates` — reject, false (the archive is history, and the CHANGELOG section is unreleased).
- prior-review #1: the percent and the counts disagree on screen — fix now for the docs, as diff-bug #10.
- prior-review #2: the stale `minWidth: 0` item — follow-up, as blame-history #6.
- prior-review #3: fixed colors and the ambiguous-width `▎`, `■`, `□` — follow-up, row "Pane look follow-ons (M208 review)".
- prior-review #4: the M207 heading literal changed — reject, false, as blame-history #9.

Review pass 2, 2026-10-04, on `44c2fa5`, after the T7 phase colors. Main had not moved (`ea647c6`), and no PR existed.

- AC1 evidence: `claude plugin test .` passes 994 of 994, with the three AC1 cases and the 44-column tail case passing on both surfaces. T7 left the head line and its gray percent unchanged.
- AC2 evidence: "partly checked and all checked" and "all open" pass on both surfaces: `■` in orange on M080 (implement) and in green on M081 (review), `□` in `subtle`.
- AC3 evidence: the nine heading cases pass on both surfaces, each asserting the gap row, the `▎` in its phase color (orange for M080's four headings, green for M081's Goal and Tasks, plan blue `rgb(110,140,190)` for Workable, Waiting, and Candidates), and the gray bold label. The pill cases assert ` /milestone-review M081 ` on green, ` /milestone-implement M002 ` on orange, and ` /milestone-plan ` on blue, each bold white. The 14 non-orange cases failed on the old colors before T7.
- AC4 evidence: the AC4 cases over `pane-full` and `candidates` pass on both surfaces. T7 changed no width.
- AC5 evidence: README.md:213-219 and CHANGELOG.md:9-15 name the phase colors, as do the DESIGN pane paragraph and the `pane.ts` header comment (lines 20-26). The T7 claim audit read 16 claims there with none false.
- AC6 evidence: on `44c2fa5` the scripts suite ran 397 OK (21 skipped), the hooks suite 174 OK, `claude plugin validate` exited 0, and `claude plugin test .` exited 0 with 994 passing.
- Consistency gate: `cairn_validate.py` passes, its `release window` check OK. No principle changed. The `generic` profile names no toolchain checks.
