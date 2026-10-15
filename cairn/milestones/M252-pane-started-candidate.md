<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M252: The cairn pane marks a candidate row that an open pull request names

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane and the /hotfix and /milestone-review skills ship to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In the cairn pane, a candidate row that the body of one of the operator's open pull requests names draws a started mark and that pull request's number.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The pane's one `gh pr list` call (`register.tsx` `listArgv`) also
asks for `body`. A new parser reads `Candidate row: <short title>` lines
from each listed body, from any head branch. The read stores the items in
the hotfix list's value, so one guarded write covers both. A candidate line
that an item names draws ◐ in the review color in place of its priority
mark, `#N` in gray in its tail, and no ✎. In owner mode, `/hotfix` and
`/milestone-review` write one such line per candidate row their merge will
remove or narrow, the title cut from the ROADMAP row when the PR opens.
README, DESIGN.md, CHANGELOG.md, and `types/index.d.ts`.

**Out:**
- Guest mode: the PR body reaches the maintainers and carries no cairn
  terms, so a guest PR carries no line and marks nothing → new candidate row
  "Started mark in guest mode".
- A PR opened before this ships carries no line and marks nothing. No
  backfill: such PRs merge or close on their own.
- A row that a planned milestone absorbs with no open PR gets no mark (the
  request names open PRs only).
- The line names rows as the ROADMAP reads when the PR opens. A row
  narrowed or retitled later can leave the line stale. Accepted at the plan.
- A live look: tests only, at the operator's choice. The first real hotfix
  that names a row shows the mark.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [ ] AC1: `startedRows` in `hooks/status/pane.ts` maps one `gh pr list --json
      number,title,url,headRefName,body` result to a list of `{ title, number }`
      items. Each entry with an integer `number` and a string `body` counts,
      whatever its head branch. Each body line that begins with exactly
      `Candidate row: ` gives one item. Its `title` is the rest of the line,
      trimmed as `candidateRows` trims a title. A line whose rest is empty or
      only whitespace gives no item. Lines split on `\n`, and a trailing `\r` is
      removed. A call that rejected, exited non-zero, or printed something other
      than a JSON array gives null. Shown by `hooks/status/pane.test.tsx` cases:
      a `hotfix-*` head, an `m<nnn>-*` head, a head with neither prefix, a body
      with two such lines, the prefix after other text, the prefix after leading
      spaces, an empty rest, a whitespace-only rest, a CRLF body, a non-string
      body, a non-integer `number`, and each null case.
- [ ] AC2: `paneLines` draws a candidate line as started when its short title is
      not empty and equals an item's `title` exactly. That line draws `◐` in the
      review phase color in place of its priority mark. Its tail draws `#N` in
      gray for the lowest matching `number`. It carries no `plan` Button,
      whether `acts` is true or false. Every other candidate line draws as
      before this milestone. Shown by `pane.test.tsx` cases: a matched high,
      normal, and low row; a matched row with `acts` true and with `acts` false;
      an unmatched row beside them; two PRs naming one row; two rows sharing a
      matched title; a title that differs only by case; and an empty-title row.
- [ ] AC3: The pane's read sends `body` in its one `gh pr list` call. It stores
      the items in the same value as the hotfix list, under the tag
      `hotfixes-2`. A failed call in the same root keeps the last good items,
      and a failed call in another root, or a root with no base-remote URL,
      empties them, as the hotfix list does. The next draw whose band root is
      that root, with no active milestone, marks the lines that AC2 names. The
      Hotfixes section still lists only `hotfix-*` heads. Shown by
      `pane.test.tsx` cases through the test kit's `process.run` stub: the argv
      holds `body`, a marked line after a read, and each of the three failure
      cases.
- [ ] AC4: Each place that `/hotfix` opens a PR, the `gh pr create` lines that
      `grep -n "gh pr create" skills/hotfix/SKILL.md` lists and step 5's re-land
      PR, tells the agent what the body carries or points to the sentence that
      does. In owner mode the body carries one `Candidate row: <short title>`
      line per matched row, the title cut from the ROADMAP row as tracking-rules
      "Candidate short title" states. The guest-mode site tells the agent to put
      no such line.
- [ ] AC5: Each owner-mode site that opens the milestone PR in
      `skills/milestone-review/SKILL.md`, among the lines that `grep -n "gh pr
      create" skills/milestone-review/SKILL.md` lists, tells the agent to put
      one such line per candidate row that the post-merge hygiene will remove or
      narrow, as known when the PR opens, the title cut from the ROADMAP row.
      The guest site and the companion-repo site tell it to put none.
- [ ] AC6: README's cairn pane section and DESIGN.md's pane description state
      the started mark, the `Candidate row:` line, and four limits: only
      owner-mode PRs carry the line; only the operator's own open PRs on the
      base remote count; marks change only at a pane open, ↻, `/clear`, or
      `/resume`; and the pane draws candidate rows only while no milestone is
      active, so a milestone PR's mark shows only in a checkout of the default
      branch. CHANGELOG.md has an entry, and `types/index.d.ts` declares the
      stored type in its `PluginState` entry.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T5
- AC5 → T5
- AC6 → T4, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Tests first in `hooks/status/pane.test.tsx`: AC1's parser
      cases, AC2's draw cases, and AC3's read cases through the
      `process.run` stub (`pane.test.tsx:1908-2000`, `:2609-2720`). Update
      the stub's expected argv (`:2617`) to hold `body`. See them red.
- [ ] T2: Add `startedRows` beside `hotfixPrs` (`pane.ts:143`).
- [ ] T3: In `paneLines` (`pane.ts:472-494`), take the items as a new
      argument, add a started mark beside `PRIORITY_MARK` (`pane.ts:228`),
      and draw the mark, the `#N` tail, and no ✎ on a matched line.
- [ ] T4: In `register.tsx`, add `body` to `listArgv` (`:899`), parse the
      items in `readHotfixes` (`:882`), store them in the hotfix value, move
      its tag to `hotfixes-2` (`:150`), and pass them to `paneLines`
      (`:328`). Extend `CairnHotfixRead` in `types/index.d.ts:97`. Run
      `verify`.
- [ ] T5: In `skills/hotfix/SKILL.md` (the create sites at `:205`, `:255`,
      `:294`, and step 5's re-land at `:195`) and
      `skills/milestone-review/SKILL.md` (`:137`, `:557`; none at `:610` and
      `:631`), write the `Candidate row:` line rule. Hand-run `skills/tests`.
- [ ] T6: README's pane section, DESIGN.md's pane description, and
      CHANGELOG.md, with AC6's four limits. Run `verify`.

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
- 2026-10-15: tier check: milestone — a new pane behavior plus skill changes, more than one sitting.
- 2026-10-15: collision check: no candidate, planned, or D-entry overlap; M207, M226, M242, and M249 shipped the pieces this builds on; inbox 0 open issues, 0 open PRs.
- 2026-10-15: plan gate chose a `Candidate row:` line in the PR body, read by the existing `gh pr list` call, over a marker on the ROADMAP row because a row marker needs a commit to the default branch at PR open and a removal when the PR closes unmerged; falsified by a PR body line that GitHub or a merge tool strips or rewrites.
- 2026-10-15: plan gate chose matching by the body line over matching PR titles or branch slugs to row titles because both are free text with no fixed link to a row; falsified by a body line that names a row the PR does not fix.
- 2026-10-15: plan gate chose to cut the title from the ROADMAP row at PR open over copying it from the plan's work log because a retitle between plan and review would leave a copied title naming no row; falsified by a row retitled after the PR opens.
- 2026-10-15: criteria audit (full mode, Opus): 11 findings. Fixed 9 (AC1, AC2 cases added; AC3 draw condition and shared value; AC4 re-land site; AC5 companion site and title source; AC6 limits and types scope). Accepted 1 (a stale line after a later narrow, in Out). 1 posed (milestone PRs show only from another checkout).
- 2026-10-15: question set: mark — ◐ in the review color; ✎ on a marked row — hidden; milestone PRs — included, limit documented; live look — none, tests only.
- 2026-10-15: guest mode left out at the plan (no cairn terms reach the host repo), to the new candidate row "Started mark in guest mode".

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
