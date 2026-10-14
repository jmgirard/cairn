<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M250: The plan checks that the work needs a milestone before it plans one

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP1, IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — it changes what `/milestone-plan` does in every adopting repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m250-plan-tier-check   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Before `/milestone-plan` investigates, it checks whether the request needs a milestone, and when a hotfix or a direct edit fits instead, it offers that route.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A tier check in `skills/milestone-plan/SKILL.md` step 1, its chip
and the effect of each option, and the work-log line step 4 writes. One
sentence in tracking-rules "Question gates and phase closes" and a D-entry
annotating D-144. README.md's `/milestone-plan` row and a CHANGELOG entry.
A hand-run prose guard in `skills/tests/`.

**Out:** The tier definitions do not change: a one-sitting change to
running code that is not a bug stays a milestone (question set). `/hotfix`
step 1's opposite check does not change. The CLAUDE.md router template
does not change: it already routes before a skill fires. The guest-mode
trivial tier for files outside `cairn/` stays undefined, as it is today;
such a request is a milestone here.

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

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 1 holds a tier check that
      runs before step 2. It cites tracking-rules "Sizing and the work
      tiers" and puts the request as a whole in exactly one tier: `hotfix`
      when it is a user-visible bug whose fix restores documented behavior
      in one sitting with no design decision; `trivial` when it has no
      runtime surface, fits one sitting with no design decision, and, in
      guest mode, touches only files under `cairn/`; `milestone` otherwise.
      A request whose parts fall in more than one tier, or any of whose
      parts is `milestone`, is a milestone. The check may read the code and
      docs the request names. It runs neither step 2's sweeps nor its
      subagents.
- [ ] AC2: The skill says that an invocation from `/milestone` §4's
      `milestone` verdict, or for a request that `/hotfix` step 1 routed
      to `/milestone-plan` in this session, is classified `milestone`
      without re-judging, and that the work-log reason names the router.
      A request that names no work skips the check until step 3 names the
      work, and the check then runs before step 4.
- [ ] AC3: When the check finds `hotfix` or `trivial`, the skill poses one
      chip before step 2. Its question text names the tier found and the
      reason. Its options are the tier's route (marked recommended),
      planning a milestone anyway, and stop. The trivial option's
      description says the edit is committed and pushed to the default
      branch (owner mode) or left uncommitted on disk (guest mode).
      tracking-rules "Question gates and phase closes" states that a run
      begins at the plan question set, and that `/milestone-plan`'s tier
      chip, posed only on a `hotfix` or `trivial` finding, comes before it.
- [ ] AC4: `skills/milestone-plan/SKILL.md` says what each option of AC3's
      chip does. The hotfix route invokes `/hotfix` through the Skill tool
      with the request as its argument, and the plan skill writes no file.
      The trivial route in owner mode runs `git status`, then edits and
      commits only the files the edit touches and pushes at once. If the
      checkout is not on the default branch, or one of those files already
      has uncommitted changes, it makes no edit and ends with a close block
      naming why. On success it ends with a close block naming the commit.
      In guest mode it writes the edit on disk with no commit and ends with
      a close block. Stop ends with the close block and writes nothing.
      Planning anyway goes on to step 2.
- [ ] AC5: The skill says that step 4 writes one work-log line in the
      first milestone file it writes: `tier check: milestone — <reason>`
      when the check found `milestone` and posed no chip, or `tier check:
      <tier> — planned as a milestone at the user's choice` after the
      plan-anyway option. When step 4 writes no milestone file, the line
      goes into the close block's recap.
- [ ] AC6: README.md's `/milestone-plan` row in the commands table says
      that the plan first checks whether the work needs a milestone and
      offers `/hotfix` or a direct edit when it does not. CHANGELOG.md's
      Unreleased section has an entry for the check. No hit of
      `git grep -n -i "milestone-plan" -- README.md CLAUDE.md skills/
      ':!skills/tests'` states that `/milestone-plan` always produces a
      milestone.
- [ ] AC7: The `verify` slot's five commands (`cairn/PROFILE.md`) each
      exit 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T1, T6
- AC3 → T2, T4, T6
- AC4 → T2, T6
- AC5 → T3, T6
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Step 1 (`skills/milestone-plan/SKILL.md:37-41`): add the tier
      check paragraph after the in-progress check, without renumbering
      steps (lesson M148). Trace each entry path to it (lesson M172):
      `/milestone` §4's Do it now (`skills/milestone/SKILL.md`), `/hotfix`
      step 1's over-the-bar route (`skills/hotfix/SKILL.md:33-45`), the
      pane's ✎ press (README.md:320), and a request naming no work.
- [x] T2: Add the chip and each option's effect, with the owner and
      guest arms of the trivial route.
- [x] T3: Add the `tier check:` work-log line to step 4's rules.
- [x] T4: Add the sentence to tracking-rules "Question gates and phase
      closes" (`:378-390`). Append a D-entry annotating D-144 on the chip's
      place before the run. Re-seed the rulebook baseline at its three
      sites (lesson M149): `skills/milestone/SKILL.md:117`,
      `skills/tests/test_cost_audit_line.py:68`,
      `skills/tests/test_mutation_harness.py:120`.
- [x] T5: Edit README.md's `/milestone-plan` row (`:545`) and add the
      CHANGELOG entry. Run AC6's sweep and fix each hit (lesson M112).
- [ ] T6: Add a hand-run prose guard in `skills/tests/` pinning the
      clauses of T1-T4, and show each pin red by deleting its clause. Run
      `skills/tests` once and note red or green in the work log (D-109).
      Run the five verify commands and `cairn_validate`.

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

- 2026-10-14: created by /milestone-plan from the user's request that cairn check a milestone is needed before planning one.
- 2026-10-14: collision sweep: no candidate, planned, or in-progress overlap; M008 (the CLAUDE.md router) and `/hotfix` step 1's over-the-bar check are distinct; no D-entry rejects this; D-144 (one plan gate) is annotated, not contradicted; checker-regress shape not hit.
- 2026-10-14: inbox sweep: 0 open issues and 0 open PRs on jmgirard/cairn.
- 2026-10-14: lessons harvested: M112 (sweep the doc surface), M148 (prose-guard markers, no step renumbering), M149 (rulebook baseline at three sites), M172 (trace each entry path).
- 2026-10-14: criteria audit (full mode, fresh Opus reader): 9 findings, all fixed: routed requests are not re-judged; a request naming no work is checked after step 3; mixed-tier requests and long docs work are milestones; the check reads only named code and docs; the rulebook gate section names the chip; the trivial option says it pushes; the trivial route refuses off the default branch or over dirty files; the guest rule moved into AC1; the work-log line names its file; the sweep became a no-hit claim over README, CLAUDE.md and skills; the hand-run suite moved to a task (D-109).
- 2026-10-14: question set: on a smaller-tier finding — ask, route recommended; small non-bug runtime changes — stay milestones; trivial route — the plan skill makes the edit.
- 2026-10-14: plan gate chose a chip on a smaller-tier finding over an automatic route because a wrong call would cost a rerun and the user keeps the plan-anyway option; falsified by tier chips the user always answers with the recommended route.
- 2026-10-14: plan gate chose the tier check in step 1 over a question in step 3's set because step 2's sweeps and the criteria audit would run first on work that needs no milestone; falsified by tier chips that cannot be answered without step 2's investigation.
- 2026-10-14: plan gate kept the rulebook's tier definitions over widening `/hotfix` to small non-bug changes, at the user's choice; falsified by small refactors that the check keeps sending through a full milestone run.
- 2026-10-14: implement started on m250-plan-tier-check; untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-14: T1-T3: tier check, tier chip, and the `tier check:` line added to step 1 of `skills/milestone-plan/SKILL.md`, with a pointer bullet in step 4; no steps renumbered; entry paths traced: `/milestone` §4 passes the issue (exempt), `/hotfix` step 1 routes by a close block (exempt in-session), the ✎ press passes a row title (checked).
- 2026-10-14: T4: tracking-rules "Question gates and phase closes" names the tier chip as before the run, not a run gate; D-162 appended (annotates D-144); rulebook baseline re-seeded to 655 lines / 62,812 bytes at its three sites.
- 2026-10-14: T5: README `/milestone-plan` row and CHANGELOG Unreleased entry added; AC6 sweep read 52 hits, none says the plan always produces a milestone; the router's "One question set follows" (CLAUDE.md, template) left as is per Scope Out.

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
