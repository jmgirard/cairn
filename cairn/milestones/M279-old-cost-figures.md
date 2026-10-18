<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M279: Old cost-script figures are re-measured or marked

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — reference notes under `cairn/references/` that no adopting repo reads   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m279-old-cost-figures, https://github.com/jmgirard/cairn/pull/291   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The reference notes re-measure their old cost-script figures where the
session store still holds the sessions, and mark the rest as made with the
old script.

## Scope
<!-- owner: plan · create/amend-via-gate -->

Background. PR #238 (2026-10-10) changed `scripts/cairn_cost.py` to count
each API call once, grouping records by `message.id`. It also made the
script read each session's `subagents/agent-*.jsonl` files. Before it, the
script summed every assistant record and skipped subagent files. The local
session store now holds sessions from 2026-08-13 on, and the earliest
milestone that `cairn_cost.py` keys is M139 (observed 2026-10-18). So the
figures for M139–M152 can be re-run. The figures for M63–M93
(session-cost-notes.md) and M113–M136 (effort-experiment-notes.md) cannot.
The plan found the stale descriptions of the old script with
`git grep -n -i -E "unrecorded|absent|sums every|Session-store reading"`
over the three notes that AC4 names.

**In:** re-run the M139–M152 table in `record-rule-remeasurement.md`; mark
the old figures in `session-cost-notes.md` and `effort-experiment-notes.md`;
add a current-script baseline for M269–M278 to `session-cost-notes.md`;
correct the named descriptions of the old script; update the three
`INDEX.md` lines.

**Out:** the dated 719:1 figure in the `cairn_cost.py` docstring stays, as
it is code and dated (no follow-on). The effort note's quality tallies
(returns, escapes) did not come from the script and stay. The record-rule
verdict rests on its ledger, not on Axis 3, so it is not re-judged.
Figures in `DECISIONS.md` and the archives are history and are never
edited. Notes that read the store directly and group by `message.id`
(`effort-roles.md`, `effort-review-medium.md`, the `haiku-*` notes) are
not old-script figures.

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

- [ ] AC1: In `cairn/references/record-rule-remeasurement.md`, the Axis 3
      table gives, for each of M139–M152, the `turns` and `output` of the
      BY MILESTONE row that `python3 scripts/cairn_cost.py --milestone
      M<NN>` printed in a run the section dates and names by commit. Its
      medians are the medians of that table. The section says that the
      medium-cohort baseline it cites (165 turns / 169k output) came from
      the script before PR #238, and it does not compare the two as like
      figures. The changed text is marked `corrected M279`.
- [ ] AC2: The `Extraction:` line of `cairn/references/session-cost-notes.md`
      names the 719:1 ratio in `## What the store is`, the 40.7% and 33.9%
      unattributed shares, and the figures in `## Baseline`. The
      `Extraction:` line of `cairn/references/effort-experiment-notes.md`
      names the cohort table in `## Cost`. Each line says that those
      figures came from the script before PR #238 and are not comparable
      with its current output. Each also says that they cannot be
      re-measured, because the session store no longer holds the sessions
      of their milestones (`observed 2026-10-18`). The `## Baseline` and
      `## Cost` sections each open with a sentence that points to that
      line. The old figures stay on the page.
- [ ] AC3: `cairn/references/session-cost-notes.md` carries a
      current-script baseline for M269–M278, one row per milestone. Each
      row equals the BY MILESTONE row that `python3 scripts/cairn_cost.py
      --milestone M<NN>` printed in a run the section dates and names by
      commit.
- [ ] AC4: Each of these sites states the script's current behavior and is
      marked `corrected M279`: in session-cost-notes.md, ledger row A4, the
      `## Disposition` bullet on A3 and A4, and the first bullet of
      `## Open questions`; in effort-experiment-notes.md, step 2 of
      `## Re-measurement procedure`; in haiku-sonnet-roles.md, the
      paragraph that opens "Two older records predate the store".
- [ ] AC5: In `cairn/references/INDEX.md`, the record-rule-remeasurement.md
      line gives the new medians from AC1 and does not compare them with
      165/169k. The session-cost-notes.md line no longer calls subagent
      cost `absent`, and it says that its figures came from the script
      before PR #238. The effort-experiment-notes.md line says that its
      cost figures came from the script before PR #238.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2, T3
- AC3 → T2
- AC4 → T2, T3, T4
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Run `cairn_cost.py --milestone` for M139–M152. In
      record-rule-remeasurement.md, rewrite the Axis 3 table, medians, and
      baseline comparison, the Evidence snapshot bullet, and the re-check in
      the `Extraction:` line. Keep the page's staleness state `ok`.
- [x] T2: Run `cairn_cost.py --milestone` for M269–M278 and add the
      baseline section to session-cost-notes.md. Add the AC2 statement and
      pointer. Correct its AC4 sites.
- [x] T3: In effort-experiment-notes.md, add the AC2 statement and pointer,
      and keep the words "nothing to re-verify against" so that its
      staleness state stays `exempt`. Correct its AC4 site.
- [x] T4: Correct the AC4 site in haiku-sonnet-roles.md. Update the three
      INDEX.md lines. Run the `verify` slot (both gating suites) and
      `cairn_validate`.

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

- 2026-10-18: created by /milestone-plan.
- 2026-10-18: tier check: not run — work named at the question set.
- 2026-10-18: question set: what to work on — "Re-measure old cost figures"; after the plan — plan, then implement in this session.
- 2026-10-18: collision: absorbs the candidate row "Re-measure the figures built with the old `cairn_cost.py`" (M228 review, narrowed by the PR #238 hotfix); no D-entry rejects it; D-057's measured-regression trigger is what a like-for-like baseline serves.
- 2026-10-18: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-18: lessons: run both gating suites, since `scripts/tests` pins each references page's staleness state (M56 line); a count is only as wide as the trees swept (M157).
- 2026-10-18: criteria audit (reduced mode, fresh Opus reader): 4 findings, all fixed: AC2, AC3, and AC5 named their figures and rows in place of "the page's figures", "matches that command's output", and "agree with those pages"; AC4 dropped "the plan ran" (an instrument clause, moved to Scope) and anchors its sites by section, not line number. AC1's note to name the BY MILESTONE row was also taken.
- 2026-10-18: plan gate chose marking the old figures in place over deleting them because the pages' conclusions (the 50% cut, the +10.8% trend) cite them; falsified by a later reader taking a marked old figure as a current-script figure.
- 2026-10-18: plan gate chose adding a current-script baseline (M269–M278) over leaving session-cost-notes.md with none because a later cost comparison needs a same-method figure; falsified by a decision that needs a window other than the latest ten milestones.
- 2026-10-18: implement started on branch m279-old-cost-figures, cut from main at 92edddd4; untracked `cairn-probe.log` and `tsconfig.json` (not this milestone's) left unstaged.
- 2026-10-18: ran `cairn_cost.py --milestone` for M139–M152 and M269–M278 at 92edddd4 (one run, both ranges).
- 2026-10-18: T1 done: record-rule-remeasurement.md Axis 3 re-run (medians 130.5 turns / 112,229.5 output, were 137 / 175,620), 165/169k comparison removed, Evidence and Extraction lines marked corrected M279; verify 5/5 green.
- 2026-10-18: T2 done: session-cost-notes.md gets the old-script statement in Extraction, a pointer opening `## Baseline`, a new `## Current-script baseline` (M269–M278) before `## Disposition`, and corrected A4 row, Disposition bullet, and first Open question; also corrected the A4 paragraph under the ledger, which still said subagent tokens go uncounted; staleness pin stays `ok`; verify 5/5 green.
- 2026-10-18: T3 done: effort-experiment-notes.md gets the old-script statement in Extraction ("nothing to re-verify against" kept, pin stays `exempt`), a pointer opening `## Cost`, and a corrected step 2 of the re-measurement procedure; verify 5/5 green.
- 2026-10-18: T4 done: haiku-sonnet-roles.md "Two older records" paragraph put in the past tense with PR #238 named; INDEX.md lines for the three notes updated; plan sweep re-run, remaining hits are the tag legend, the corrected A4 row and Open question, and unrelated lower-bound lines; cairn_validate green; verify 5/5 green.
- 2026-10-18: claim audit: not owed — internal tier.
- 2026-10-18: implement complete; status review.

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
