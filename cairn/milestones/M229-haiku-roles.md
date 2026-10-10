<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M229: Sonnet roles move to Haiku 5.5 where M228 found it cheaper and noninferior

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M228   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1, IP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which model every adopter's skills spawn   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The skills spawn Haiku 5.5 for each Sonnet role group that M228's note marks `move`, under a decision that supersedes the "Never Haiku" rule.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A `DECISIONS.md` entry supersedes D-016's "Never Haiku" blanket and
the D-110 clause that leaves it standing. The tracking-rules "Model and
agent strategy" section, each skill line that names Sonnet for a moved
group, and the prose-guard pins on those lines change to match. One
`CHANGELOG.md` entry records the change.

**Out:** Opus and Fable roles → unchanged, because the request named only
the Sonnet roles. A group that M228 marks `stay` keeps Sonnet, and its
re-test → the re-measurement procedure in M228's note. If every group is
`stay`, or the verdicts are mixed, T1 stops for the user, because the
request was for all roles. The user then decides whether to drop M229 or to
move only some groups.

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

- [ ] AC1: A new `cairn/DECISIONS.md` entry supersedes D-016's "Never
      Haiku" blanket and D-110's clause that the blanket stands, and its
      `### D-` heading names both. It cites
      `cairn/references/haiku-sonnet-roles.md` and names each role group
      that moves to Haiku and each that stays on Sonnet, matching that
      note's verdicts.
- [ ] AC2: In `skills/shared/tracking-rules.md` "Model and agent strategy",
      each role group that the note marks `move` is assigned Haiku, and each
      marked `stay` is assigned Sonnet. Boilerplate follows the edit-work
      verdict. The "Set the model" bullet's list of models includes Haiku.
      No bullet forbids Haiku for a moved group.
- [ ] AC3: Each line that `git grep -n -i -E "sonnet|haiku" -- skills
      README.md ':!skills/tests'` lists and that assigns a model to a role
      assigns the model that AC2 gives that role. Each listed line that bars
      a model bars it only from roles that AC2 does not give it.
- [ ] AC4: `CHANGELOG.md`'s unreleased section carries one entry naming the
      roles that now run on Haiku 5.5.
- [ ] AC5: The active profile's `verify` slot passes (`cairn/PROFILE.md`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [ ] T1: Read the verdicts in `cairn/references/haiku-sonnet-roles.md`.
      If all are `move`, log the groups and go on. If all are `stay` or the
      verdicts are mixed, stop at the goal-wrong stop with the verdicts,
      because a move of fewer than all roles drops part of the request.
- [ ] T2: Append the D-entry that supersedes D-016's blanket. It cites the
      note and names the moved and kept groups. Under IP2 it quotes D-016's
      "can silently drop a real bug" reason and answers it with the
      history-review verdict.
- [ ] T3: Rewrite the "Set the model", "Sonnet subagents", review fan-out,
      and "Never Haiku" bullets of "Model and agent strategy" in
      `skills/shared/tracking-rules.md` to match the verdicts.
- [ ] T4: Edit each skill line that the AC3 grep lists. At plan time these
      are `skills/cairn-triage/SKILL.md:142`,
      `skills/design-interview/SKILL.md:46`,
      `skills/milestone-implement/SKILL.md:119-120`,
      `skills/milestone-plan/SKILL.md:42`, and
      `skills/milestone-review/SKILL.md:259,264`. Update the reviewer pins
      in `skills/tests/test_review_fanout.py` and show each pin red with the
      old name planted. Hand-run `skills/tests` and both gating suites.
- [ ] T5: Add the `CHANGELOG.md` entry and run the full `verify` slot.

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

- 2026-10-09: created by /milestone-plan.
- 2026-10-09: question set: which roles move — "all, but only if some testing finds it is cheaper and noninferior"; M228 runs that test, so M229 depends on it, and a mixed or all-`stay` result stops at T1 for the user.
- 2026-10-09: collision: D-016 ("Keep the blanket rule … a weaker model can silently drop a real bug") is a standing rejection; it is superseded at T2 only after M228's verdicts exist, never at plan, because the user conditioned the move on the test. The ROADMAP candidate "Haiku for Sonnet subagent work" graduates at this milestone's post-merge hygiene.
- 2026-10-09: plan gate chose a stop at T1 on mixed verdicts over moving only the passing groups unasked, because a partial move drops part of the request; falsified by the user saying a per-group move was what they meant.
- 2026-10-09: criteria audit (full mode, fresh Opus reader) returned three findings, all fixed: AC1 left D-110's "blanket stands untouched" clause live, so the entry now supersedes it too and names both in its heading; AC2 left boilerplate (a "Sonnet subagents" role in no M228 group) and the "Set the model" model list undecided, so boilerplate follows the edit-work verdict and the list gains Haiku; AC3 failed any line that bars a model and made a reading act the promise, so it now binds assigning lines and barring lines separately. AC4 and AC5 drew no finding.

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
