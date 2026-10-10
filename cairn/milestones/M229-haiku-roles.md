<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M229: The edit-work Sonnet roles move to Haiku 5.5

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M228   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP1, IP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes which model every adopter's skills spawn   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m229-haiku-roles   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The skills spawn Haiku 5.5 for the edit-work role group, under a decision that supersedes the "Never Haiku" rule. M228's note marks that group `move`, and the user chose it at T1.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A `DECISIONS.md` entry supersedes D-016's "Never Haiku" blanket and
the D-110 clause that leaves it standing. The tracking-rules "Model and
agent strategy" section, each skill line that names Sonnet for a moved
group, and the prose-guard pins on those lines change to match. One
`CHANGELOG.md` entry records the change.

**Out:** Opus and Fable roles stay unchanged, because the request named only
the Sonnet roles. The search group (`stay`) keeps Sonnet. The
history-review group (`move`) also keeps Sonnet, by the user's T1 choice
on 2026-10-10. A re-test of either group uses the re-measurement procedure
in M228's note.

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

- [x] AC1: A new `cairn/DECISIONS.md` entry supersedes D-016's "Never
      Haiku" blanket and D-110's clause that the blanket stands, and its
      `### D-` heading names both. It cites
      `cairn/references/haiku-sonnet-roles.md`. It names the edit-work
      group as moving to Haiku, and boilerplate as following that group's
      verdict. It names the search and history-review groups as staying on
      Sonnet. It gives each group's verdict from that note. It records
      that history review stays by the user's T1 choice of 2026-10-10.
- [x] AC2: In `skills/shared/tracking-rules.md` "Model and agent strategy",
      Haiku is assigned to mechanical migrations and to test writing
      against a spec (the edit-work group), and to boilerplate, which
      follows the edit-work verdict. Sonnet is assigned to the search role
      (Explore fan-outs) and to the history-review roles (the blame-history
      and prior-PR-comments reviewers). The "Set the model" bullet's list
      of models includes Haiku. No bullet forbids Haiku for a role that
      this criterion assigns to Haiku.
- [x] AC3: Each line that `git grep -n -i -E "sonnet|haiku" -- skills
      README.md ':!skills/tests'` lists and that assigns a model to a role
      that AC2 names assigns the model that AC2 gives that role. Each
      listed line that bars a model bars it only from roles that AC2 does
      not give it.
- [x] AC4: `CHANGELOG.md`'s unreleased section carries one entry naming the
      roles that now run on Haiku 5.5.
- [x] AC5: The active profile's `verify` slot passes (`cairn/PROFILE.md`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5, T6
- AC5 → T4, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Read the verdicts in `cairn/references/haiku-sonnet-roles.md`.
      If all are `move`, log the groups and go on. If all are `stay` or the
      verdicts are mixed, stop at the goal-wrong stop with the verdicts,
      because a move of fewer than all roles drops part of the request.
- [x] T2: Append the D-entry that supersedes D-016's blanket. It cites the
      note and names the moved and kept groups. Under IP2 it quotes D-016's
      "can silently drop a real bug" reason and answers it with the
      choice to keep every review role on Sonnet.
- [x] T3: Rewrite the "Set the model", "Sonnet subagents", review fan-out,
      and "Never Haiku" bullets of "Model and agent strategy" in
      `skills/shared/tracking-rules.md` to match AC2.
- [x] T4: Edit each skill line that the AC3 grep lists. At plan time these
      are `skills/cairn-triage/SKILL.md:142`,
      `skills/design-interview/SKILL.md:46`,
      `skills/milestone-implement/SKILL.md:119-120`,
      `skills/milestone-plan/SKILL.md:42`, and
      `skills/milestone-review/SKILL.md:259,264`. Line 119's "well-specified
      mechanical work" is the edit-work group and moves to Haiku. The
      reviewer pins in `skills/tests/test_review_fanout.py` stay Sonnet.
      Hand-run `skills/tests` and both gating suites.
- [x] T5: Add the `CHANGELOG.md` entry and run the full `verify` slot.
- [x] T6: Remove the milestone and decision numbers from the new
      `CHANGELOG.md` entry (review return 1) and re-run `verify`.

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
- 2026-10-10: started; branch m229-haiku-roles cut from main at 42c0ec5 (in sync with origin). Untracked `cairn-probe.log` and `tsconfig.json` predate the run and stay unstaged.
- 2026-10-10: T1: M228's verdicts are mixed (search `stay`, edit work `move`, history review `move` on a 4-to-4 single-run tie whose cost gap about 870 unrecorded output tokens per call reverses), so T1 stopped for the user. The user chose "Edit work only" at the chip: edit work and boilerplate move to Haiku, search and history review stay on Sonnet.
- 2026-10-10: substantive amendment: at the user's T1 choice, the title, Goal, Scope Out, AC1, AC2, and AC3 narrow from "each group M228 marks `move`" to the edit-work group. The goal is narrowed in place rather than re-cut through `/milestone-plan`, because the plan's Scope named this per-group choice as the user's to make at T1. T2, T3, and T4 reworded to match (minor).
- 2026-10-10: re-audit: AC1 (full) — no reason recorded for history review staying despite `move`; fixed by requiring the entry to record the user's T1 choice.
- 2026-10-10: re-audit: AC2 (full) — boilerplate listed as edit work though M228 never measured it; fixed by restoring "follows the edit-work verdict". Also flagged the stale title, T1, T2, and T4 reviewer-pin step; all fixed.
- 2026-10-10: re-audit: AC3 (full) — lines that assign Opus can never match a model AC2 does not give; fixed by binding only roles that AC2 names. Also: the ROADMAP candidate "Haiku for Sonnet subagent work" covers roles that do not move, so post-merge hygiene narrows it to search and history review instead of graduating it whole.
- 2026-10-10: re-audit: AC1 (full) — nothing on the criterion; T2's "history-review verdict" answer reworded to the choice to keep review on Sonnet.
- 2026-10-10: re-audit: AC2 (full) — nothing.
- 2026-10-10: re-audit: AC3 (full) — `milestone-implement` line 119's "well-specified mechanical work" is not a role AC2 names verbatim, so AC3 could pass with it still on Sonnet. Answered, not refixed (a third wording pass is the repeated-re-audit stop): that phrase is the mechanical-migration role AC2 names, and T4 now says it moves to Haiku. Also answered: Scope In's "pins on those lines change" binds nothing here, because no prose-guard pin covers a line that changes.
- 2026-10-10: T2: appended D-151; it supersedes D-016's blanket and D-110's "blanket stands" clause, names each group's verdict, and quotes D-016's "silently drop a real bug" reason, answered by keeping every review role on Opus or Sonnet.
- 2026-10-10: T3: "Set the model" lists Haiku; the "Sonnet subagents" bullet splits into "Haiku subagents" (D-151: migrations, test writing, boilerplate, with verify before commit) and "Sonnet subagents" (Explore, the two history-review lenses); "Never Haiku" removed; the review fan-out bullet already said Sonnet and is unchanged. Suites: scripts 401 OK (21 skipped), hooks 174 OK, skills 669 OK.
- 2026-10-10: T4: of the AC3 grep lines, only `skills/milestone-implement/SKILL.md:119-120` assigned or barred a model against AC2; it now reads Haiku for mechanical work and test writing, Sonnet for Explore searches, with "never Haiku" removed. The Explore lines (cairn-triage 142, design-interview 46, milestone-plan 42) and the reviewer lines (milestone-review 259, 264) already say Sonnet and stay. No prose-guard pin covers a changed line. `cairn/references/anthropic-code-review.md:53` quotes the old rule as history and stays. Suites: skills 669 OK, hooks 174 OK, scripts 401 OK (21 skipped).
- 2026-10-10: T5: CHANGELOG Unreleased gains a "Changes that affect existing repos" entry naming the edit-work roles now on Haiku 5.5; the ROADMAP candidate "Haiku for Sonnet subagent work" narrowed in place to search and history review rather than graduating at hygiene. verify: scripts 401 OK (21 skipped), hooks 174 OK, plugin validate passed with warnings, marketplace validate passed, plugin test 1765 pass 0 fail.
- 2026-10-10: claim audit: 24 claims read, 1 corrected — CHANGELOG.md (the edit-work entry said M228 measured the whole move; it now says boilerplate follows the measured result untested; the same reader re-read it and it checks out).
- 2026-10-10: all tasks checked, verify green; status review.
- 2026-10-10: review return 1: consistency gate failed — the profile's changelog check bars milestone numbers in user-facing text, and the new CHANGELOG entry names `D-151` and `M228` (CHANGELOG.md lines 75 and 78). AC1-AC4 evidence, `cairn_validate`, and both manifest validates were clean at this point.
- 2026-10-10: T6 (review return 1): T6 added and mapped to AC4 (minor amendment). The CHANGELOG entry drops `(D-151)` and reads "A side-by-side test measured" in place of "M228 measured"; the Unreleased section now holds no `M<NNN>` or `D-<NNN>` token. The claim audit's pass stands: the change swaps an id for a plain name and adds no claim. verify: scripts 401 OK (21 skipped), hooks 174 OK, plugin validate passed with warnings, marketplace validate passed, plugin test 1765 pass 0 fail; status review.

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

### Pass 2 (2026-10-10, after review return 1)

Evidence, read fresh at 69ed436:
- AC1: D-151's heading reads "supersedes D-016's "Never Haiku" blanket and D-110's clause that the blanket stands"; its body cites `cairn/references/haiku-sonnet-roles.md`, gives search `stay`, edit work `move`, history review `move`, moves edit work with boilerplate following it, keeps search and history review on Sonnet, and records "History review stays on Sonnet by the user's T1 choice of 2026-10-10" (one grep hit each). Pass.
- AC2: "Model and agent strategy" lists "(Haiku, Sonnet, Opus, or Fable" in "Set the model"; "Haiku subagents" holds mechanical migrations, test writing against a spec, boilerplate; "Sonnet subagents" holds Explore and the blame-history and prior-PR-comments lenses; no "Never Haiku" bullet (0 hits). Pass.
- AC3: the grep lists 11 lines; the Explore lines (cairn-triage 142, design-interview 46, milestone-plan 42, tracking-rules 530) and reviewer lines (milestone-review 259, 264, tracking-rules 535) say Sonnet, milestone-implement 119-120 and tracking-rules 527 give mechanical work and test writing to Haiku, tracking-rules 509 lists models; no listed line bars a model (0 hits for never/no Haiku). Pass.
- AC4: the Unreleased section holds one "Edit-work subagents run on Haiku 5.5" entry naming migrations, test writing, and boilerplate. Pass.
- AC5: verify — scripts 401 OK (21 skipped), hooks 174 OK, plugin validate passed with warnings, marketplace validate passed, plugin test 1765 pass 0 fail. Pass.

Consistency gate: `cairn_validate` exit 0; no principle changed, so no `cairn_impact`; profile slot: verify green on the review head, marketplace validate shows no `plugins[N].version` warning, the Unreleased changelog has an entry and 0 `M<NNN>`/`D-<NNN>` tokens. Pass.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: D-151 says a Haiku edit-work miss "shows as a failed check", but a weak test passes verify, and the note's edit tasks sat at the ceiling — fix now
- diff-bug #2: D-151's falsifier needs a paired Haiku and Sonnet run on one spec, which normal use never makes — fix now
- diff-bug #3: the ROADMAP candidate row gives the user a reason the record does not show — fix now
- diff-bug #4: `/milestone-implement` step 5 drops "against a spec" and boilerplate, wider and narrower than AC2 — fix now
- diff-bug #5: "Changes that affect existing repos" sits after "New" in Unreleased, unlike released sections — fix now
- diff-bug #6: the CHANGELOG's `cairn/references/…` path reads as the adopter's own folder — fix now
- diff-bug #7: the Sonnet bullet's "one work-log line" fits Explore, not the review lenses — fix now
- diff-bug #8: `cairn/references/INDEX.md:5` still says the reference "challenges cairn's never-Haiku rule" — fix now
- diff-bug #9: the DECISIONS annotation near line 2557 says the scorer stays "never Haiku" — reject, false as a defect: DECISIONS is append-only history and that scorer was retired by D-110
- blame-history #1: step 5 drops boilerplate and never says to run verify — fix now (with diff-bug #4)
- blame-history #2: INDEX.md and `competitive-landscape.md:99` describe a live never-Haiku rule — fix now for INDEX (with diff-bug #8); reject for competitive-landscape, false as a defect: a dated reference note whose "revisit" is the observation D-151 acted on
- blame-history #3: D-016 and D-110 carry no inline "superseded by D-151" marker — reject, false as a defect: entries are append-only and supersession lives in the superseding heading by convention
- blame-history #4: the split Sonnet bullet dropped "Give complete specs" and "verify" — reject, false: the reviewer found nothing lost, since Explore and the lenses make no diffs
- blame-history #5: the CHANGELOG cites a plugin-repo path — fix now (with diff-bug #6)
- blame-history #6: no D-entry depends on Sonnet edit work — reject, false: reports no defect
- prior-review #1: step 5 does not say to run verify on a Haiku diff — fix now (with diff-bug #4)
- prior-review #2: CHANGELOG section order — fix now (with diff-bug #5)
- prior-review #3: the CHANGELOG figures are accurate — reject, false: reports no defect

