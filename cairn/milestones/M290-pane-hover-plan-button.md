<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M290: The desktop cairn pane shows a candidate row's ✎ only under the pointer

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane is part of the plugin that users install
- **Branch/PR:** m290-pane-hover-plan-button   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

On the desktop, the cairn pane draws a candidate row's ✎ only while the
pointer is over that row, and the terminal draws ✎ where it does today.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** the Box that holds a candidate line's `plan` Button in
`hooks/status/register.tsx`. Off the terminal, that Box has no key,
`display: 'none'`, and `hover: { display: 'flex' }`. It stays in the row's
flow at the right end, inside the line's keyed Box, which is the hover
scope that the M286 hover card uses. Off the terminal, a candidate line
with a `full` also draws an info icon, a gray `ⓘ` glyph, before ✎ in the
same hidden way. The glyph's `Text` names a hover group, and only that
group opens the line's card. `pane.ts` marks such a line with an `info`
field. On the terminal, the keyed `candidate-<i>-plan` Box
stays as it is. Tests, the comments beside the code, README,
`cairn/DESIGN.md`, and CHANGELOG change too.

**Out:** the other Buttons of the pane (⌂, ↻, Finish, Revise, Check, the
Next action, Status) stay drawn at rest, since the request names only ✎.
A ✎ drawn over the title's end is not built (the user's choice at the
question set). On the desktop, a hidden ✎ can be out of reach of the Tab
key. The user accepted that at the question set, so no row is filed. A
first click on an unfocused pane only focuses it. That gap stays with item
(1) of the parked row "Gaps only the app or mod API can close". Every
line that is not a candidate line keeps opening its card from anywhere on
the line (the user's choice after the first live look). AC5 guards that
by the drawn props alone.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: On the `desktop` surface, a mod test loops over each candidate
      line that `paneLines` gives the `plan` Button in the `candidates` and
      `candidates-order` fixtures. For each such line, the parent Box of the
      Button has no key, `display: 'none'`, `hover: { display: 'flex' }`,
      and no `position` prop. That Box is a child of the keyed
      `candidate-<i>` Box of the line.
- [ ] AC2: On the `terminal` surface, the same loop runs over the same
      lines. For each such line, the parent Box of the Button is the keyed
      `candidate-<i>-plan` Box, with `flexShrink: 0` and no `display` prop.
      No Box under the line has a `hover` field in the drawn tree, read
      beside `props` as M286 found, and no `Svg` sits under the line.
- [ ] AC3: On each surface, a press of `cairn-pane-plan-<i>` for rows 2
      and 3 of `candidates-order` runs `/clear`, then `cairn:milestone-plan`
      with the short title of that row. A mod test shows this.
- [ ] AC4: A mod test reads the parent Box of each Button in the mounted
      pane for `pane-full` and `candidates` on both surfaces, and of the
      Finish Button that a `MERGED` read draws on a `blocked-prs` line. No
      such parent Box, other than that of a candidate line's ✎, has a
      `display` prop.
- [ ] AC5: On the `desktop` surface, a mod test loops over each candidate
      line that carries the `plan` Button in the `candidates` and
      `candidates-order` fixtures. In each such line, the child just before
      the parent Box of the Button is an unkeyed Box with `display: 'none'`
      and `hover: { display: 'flex' }`. Its only child is a `Text` that
      reads `ⓘ`, with `hover: { scope: s, bold: true }`. The line's child
      Box with `position: 'absolute'` has `hover: { display: 'flex',
      scope: s }`. The string `s` is the same on the `Text` and the Box and
      differs between lines. The same test over
      `pane-full` and `candidates` shows that each `position: 'absolute'`
      child of a line that is not a candidate line keeps
      `hover: { display: 'flex' }` with no `scope`, and that set is not
      empty in each fixture.
- [ ] AC6: The operator opens a new Code session in a cairn repo with
      candidate rows and no active milestone (circumplex), with the docked
      desktop pane focused. At rest, no candidate row shows the info icon
      or ✎. While the pointer is over a row whose short title is not
      empty, that row shows its info icon and its ✎, and no card. While the
      pointer is over the info icon, the row's card shows. A click on ✎
      runs `/clear`, then `/milestone-plan` with the short title of that
      row.
- [ ] AC7: README.md near lines 325-328 and 397-402 and `cairn/DESIGN.md`
      near lines 320-326 and 490-500 each say three things: the desktop
      pane shows a candidate row's info icon and ✎ only while the pointer
      is over the row, the row's card opens from the info icon, and the
      terminal shows ✎ as before. The comments near `register.tsx` lines
      386-397, 451-457, and 466-467 and near `pane.ts` lines 66-77 each say
      the part that their code draws. None of these sites says that a hidden Box cannot carry
      a hover `scope`. The Unreleased section of CHANGELOG has an entry for
      the change.
- [ ] AC8: The `verify` slot of `cairn/PROFILE.md` is clean.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2, T3
- AC2 → T2, T3, T5
- AC3 → T1, T2, T3
- AC4 → T2, T3
- AC5 → T5
- AC6 → T6
- AC7 → T4, T5
- AC8 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Spike. The type docs do not say whether the test harness finds
      and presses a Button inside a `display: 'none'` Box. Mount a hidden
      ✎ on the desktop and check `ui.findAll({ type: 'Button' })` and
      `ui.press`. If either fails, stop for an amendment of AC1 and AC3.
- [x] T2: Tests first in `hooks/status/pane.test.tsx` for AC1 to AC4.
      Restrict the test near lines 2016-2036, which wants a keyed
      `candidate-<i>-plan` Box on both surfaces, to the terminal, and add
      the desktop form. On the desktop, tell the ✎ Box from the hover card
      by `position: 'absolute'`. The new AC1 and AC4 parts fail.
- [x] T3: In `register.tsx`, draw the parent Box of the `plan` Button per
      AC1 off the terminal and per AC2 on it. The tests pass.
- [x] T4: Update the sites that AC7 names (AC6 before the amendment), and
      add the CHANGELOG entry.
- [x] T5: Add the `info` icon, the `info` field, the hidden info Box, and
      the scoped card. Write the tests for the new AC2 clause and AC5
      first. Update the AC7 sites. The harness cannot hover, so AC6 is the
      only proof of the hover behavior. If AC6 shows the card opening with
      the row, or the icon not opening it, stop for an amendment.
- [ ] T6: Live look (AC6) with the operator in circumplex. Tell the
      operator first that the card can close when the pointer moves from
      the icon onto the card.
- [ ] T7: Run the `verify` slot (AC8).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-19: created by /milestone-plan, from the operator's request after a look at the pane's column of ✎ boxes.
- 2026-10-19: tier check: milestone — a change to the pane's running code with a design choice (hover reveal), not a bug.
- 2026-10-19: collision check: no candidate row, archived milestone, or D-entry covers hiding ✎. M242 added ✎ and M286 added the hover card that this reuses. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-19: criteria audit (full mode, fresh Opus reader): 10 items. Fixed: T1 spike for press and find on a hidden Button; T2 restricts the M242 keyed-Box test; AC3 wording on surfaces; AC4 narrowed to parent Boxes and a Finish line after a read; AC5 recording clause dropped and pane focus added; Goal and AC6 no longer say "every row" and AC6 names the sites instead of a grep. No finding on AC2 or AC7.
- 2026-10-19: plan gate chose ✎ in the row's flow over ✎ drawn on the title's end because it is the smaller change and a short title does not move; falsified by a live look where the re-cut of a long title under the pointer reads poorly.
- 2026-10-19: question set: ✎ placement on hover — in the row (a cut title is cut about 4 columns earlier while hovered).
- 2026-10-19: question set: a hidden ✎ out of reach of Tab on the desktop — accepted, pointer only.
- 2026-10-19: question set: a live look by the operator before the merge question — granted.
- 2026-10-19: implement started on m290-pane-hover-plan-button. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-19: T1 spike run as the T3 change itself: with the ✎ Box hidden on the desktop, the existing M219 AC1 Button list and the M261/M242 desktop press tests pass, so the harness finds and presses a hidden Button. Only M242 AC4's desktop keyed-Box test failed, as T2 expected.
- 2026-10-19: T2 and T3: the code change came before the tests because of the spike. The drawn tree keeps `hover` beside `props`, as M286 found. Discrimination shown by two planted probes: the main-branch register.tsx fails AC1's two desktop tests and M242 AC4's two; every pane Button hidden off the terminal fails all three AC4 tests. The suite has 2299 pass, 0 fail.
- 2026-10-19: implementation choice: the hide sits in register.tsx's shared Button loop, keyed on `kind === 'plan'` and the surface, rather than a separate branch for candidate lines, so pane.ts and its `PaneLine` shape do not change.
- 2026-10-19: T4 in progress (checkpoint): README, DESIGN (two sites), the register.tsx and pane.ts comments, and a CHANGELOG entry written. The verify run and the claim audit are running. The DESIGN history line 82 lists no M289 either, so M290 is not added there.
- 2026-10-19: claim audit: 19 claims read, 2 corrected — hooks/status/register.tsx (the hidden-scope reason now follows the type docs), CHANGELOG.md (✎ was never on every row). Both held on the one re-read. The reader also named M286's older "engine refuses" wording at register.tsx near line 475 and DESIGN.md near line 498, which this branch does not add, so it stays.
- 2026-10-19: T4 done. The verify slot is clean: scripts/tests, hooks/tests, both validates, and the mod test (2299 pass, 0 fail). T5 waits on the operator's live look.
- 2026-10-19: live look 1 asked for this repo, where M290 is active and the pane draws no candidates; moved to circumplex (no active milestone, 40 rows).
- 2026-10-19: live look 1 (circumplex): the operator saw the full-text card and ✎ open together on row hover and clash. The operator chose an info icon that opens the card, shown with ✎ only on row hover, on candidate rows only.
- 2026-10-19: substantive amendment: AC2 gains a no-hover, no-Svg clause on the terminal; new AC5 (the info icon and its scoped card); AC5-AC7 renumbered to AC6-AC8, with AC6 moved to circumplex and AC7's sites widened for the info icon; new T5; T5-T6 renumbered to T6-T7. A widening at the user's selection: AC5 added, AC2 and AC7 widened.
- 2026-10-19: re-audit: AC2 (full) — vacuous terminal check and no info-glyph clause; AC5 (full) — card/summary-card name clash, vague placement, a fixture set that never drew a non-candidate card beside candidates, harness cannot hover, hard-coded scope name; AC6 (full) — pointer onto the card closes it, "short title" ambiguity; AC7 (full) — three missed sites, the "engine refuses" sentence.
- 2026-10-19: re-audit: AC2 (full) — `hover` must be read beside `props`; AC5 (full) — empty-set guard, lines without ✎ unbound; AC6 (full) — nothing; AC7 (full) — three claims asked of every site. All four applied as narrowings. That second line per criterion is the stop: these last narrowings go to the operator at the next live-look chip.
- 2026-10-19: the amendment put the plan-owned body at 155 lines; the template comment in Acceptance criteria was cut to one line (criteria text unchanged). The 8-criteria split tripwire WARN is accepted, since splitting mid-run would leave AC5 and AC6 apart from the code they check.
- 2026-10-19: AC5's non-candidate clause said "more than one Box in each fixture", but `candidates` draws one such card (its workable line); narrowed to "not empty". This joins the narrowings for the operator at the next chip.
- 2026-10-19: T5 done. Tests first: the two AC5 info tests and the non-candidate test failed before the code. Then `icons.ts` gained `info`, `pane.ts` sets `info` on candidate lines with a title, and `register.tsx` draws the hidden info Box and scopes the card by `infoScope(line.key)`. The M286 card test now expects a scope on candidate lines' cards (`blocked-prs` draws candidates). Docs: README (two sites), DESIGN (two sites, the "engine refuses" sentence replaced), CHANGELOG. Mod test 2303 pass, 0 fail.
- 2026-10-19: live look 2 (circumplex): the info icon showed, but hovering it opened no card. T5's stop: the operator chose a probe of variants over dropping the card.
- 2026-10-19: probe (commit 8756dd60, reverted in 0f66a55b): five rows each opened the card a different way. Only the row whose trigger was a `Text` glyph with `hover: { scope, bold }` worked. A Box with `hover: { scope }` around an image or a glyph failed, hidden or shown, and so did a keyed icon Box that held its own card. A desktop fact for LESSONS at review.
- 2026-10-19: substantive amendment: the info icon is a gray `Text` `ⓘ` (`INFO_LABEL` in pane.ts) with `hover: { scope, bold: true }`, not an `Svg` in a scoped Box. AC5 now names the `Text`, AC7 drops the `icons.ts` clause, and `icons.ts` is back to main. This follows the operator's probe result, so it rides to the operator at the next chip with no further reader (the criteria spent their re-entry).

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
