<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M271: A triage promote gives its candidate row the high-priority token

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters run `/cairn-triage` and read its edits in their ROADMAP and the pane   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m271-triage-promote-marks-high   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

An accepted `/cairn-triage` `promote` on a candidate row gives the row the `[high]` token, so a promoted row stays first in the ROADMAP order and shows the pane's ↑ after the pass ends.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/cairn-triage/SKILL.md`'s default pass: the `promote` row of
step 2's table and its Readiness class, step 3's reason cell, chip text, amend
loop, and byte-for-byte rule, step 4's skip condition and apply rule, step 6's
stamp, and step 7's status line and fence order. A prose guard for the new
sentence in `skills/tests/test_candidate_priority_token.py`. README and
CHANGELOG. A D-entry annotating the priority-token decision.

**Out:** The rulebook's "Candidate priority token" paragraph, whose
"`/cairn-triage` reads and re-rates it" already covers a promote's re-rating,
so the rulebook-mass pins stay as they are. `/milestone`'s stale-row chip
(`skills/milestone/SKILL.md:138`) and records-hygiene §7's chip, which hand
the row to `/milestone-plan` at once, whose plan absorbs it. The lessons
pass's `promote`, which is about lesson families. Pane code, which already
draws ↑ for `[high]`. Naming the first `[high]` row in the next-step
recommendation → M272. Back-filling earlier promotions: the one found, the
2026-10-10 reasoning-effort row, was taken by M239 and M240 and later
rewritten with a new trigger.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `skills/cairn-triage/SKILL.md` makes every `promote` that stands
      at Accept for a candidate row whose opening token is not `[high]`,
      whether proposed or set at an Amend, carry a priority change to `high`,
      stated in the `promote` row of step 2's disposition table and in step
      3's reason-cell rule; the chip names that change once, with the
      promote; Amend cannot decline that change alone; a `promote` of a Known
      issues entry carries none.
- [ ] AC2: The same file's step 4 applies that change as it applies any
      accepted priority change: `[high] ` is added to an untagged row or
      replaces its `[low] ` token, and the row moves into the high level of
      the order; step 3's byte-for-byte rule names this edit among its
      carve-outs.
- [ ] AC3: The same file's step 4 skip condition and step 7's `nothing
      applied` condition count an accepted `promote` as changing no file
      only when it carries no priority change and no token change.
- [ ] AC4: The same file's step 7 orders the `/milestone-plan` fences of the
      accepted promotes as candidate rows in table order, then Known issues
      entries in table order.
- [ ] AC5: `git grep -n -F 'change nothing of their own' -- skills README.md`
      and ``git grep -n -F '`promote` (with no token' -- skills README.md``
      each return no line, and README.md's candidate-pane paragraph and a
      `CHANGELOG.md` `## Unreleased` entry each say that a `/cairn-triage`
      promote gives the row `[high]`.
- [ ] AC6: The `verify` slot of `cairn/PROFILE.md` passes on the branch
      head, and the hand-run `python3 -m unittest discover -s skills/tests`
      shows no failing test that does not also fail on the default branch at
      the branch point.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T2
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T1, T3
- AC6 → T2, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Edit `skills/cairn-triage/SKILL.md`: the `promote` table row
      (~:281) and Readiness class (~:322); a new sentence after the pinned
      "a `keep`, `compress`, or `retitle` row may also carry a priority
      change" (~:385) making a promote carry `high`; the chip text (~:398) so
      the promote's change is named once; the amend loop (~:409); a carve-out
      sentence after the pinned one at ~:433; the skip condition (~:434) and
      the "change nothing of their own" clause (~:459); step 7's status and
      fence order (~:541, ~:553). Keep both pinned sentences verbatim.
- [x] T2: Add a guard class in `skills/tests/test_candidate_priority_token.py`
      pinning the promote-carries-`high` sentence; show it red with the
      sentence removed and green restored; hand-run `skills/tests`.
- [x] T3: README candidate-pane paragraph (~`README.md:317`) and a CHANGELOG
      `## Unreleased` entry.
- [x] T4: Append the D-entry (annotates the priority-token decision; passes
      the conduct-rule door on its shipped-behavior trigger); run `verify`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: milestone — changes what `/cairn-triage` writes and needs a decision entry.
- 2026-10-17: collision check: D-134 (token is a row fact re-rated beside the disposition) stands, since the promote carries a priority change rather than becoming one; D-108's door is passed on its retained trigger: a promoted row left no mark, so triages the user ran reported promotions the ROADMAP and pane did not show (reported 2026-10-17); D-027's eight-word vocabulary is unchanged.
- 2026-10-17: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-17: question set: may Amend decline a promote's `[high]` alone — no, a promote always writes it; amend to `keep` to avoid it.
- 2026-10-17: question set: name the first `[high]` row in the next-step recommendation — include it, planned as M272.
- 2026-10-17: plan gate chose writing `[high]` on promote over a separate "ready" marker because the token, its ordering, and the pane's ↑ already exist; falsified by an operator who needs to tell a ready row from an important waiting row and cannot.
- 2026-10-17: criteria audit (full mode, fresh Opus reader): no criterion unreachable; four gaps fixed — AC1 covers a promote set at Amend and the chip's single naming, AC4 added for fence order, other promote paths named Out; the readiness-implies-high tension goes in the D-entry.
- 2026-10-17: rulebook left unchanged so the three rulebook-mass pins (LESSONS, M149) need no re-seed.
- 2026-10-17: implement started on m271-triage-promote-marks-high; untracked cairn-probe.log and tsconfig.json predate the branch and stay unstaged. Baseline hand-run skills/tests at the branch point: 829 tests, OK.
- 2026-10-17: T1 done: promote table row, Readiness class, reason-cell rule (proposed or set at Amend), chip names the change once, Amend cannot decline it alone, fourth byte-for-byte carve-out, skip and `nothing applied` conditions, apply rule, stamp, and fence order (candidates then Known issues, each in table order); both pinned sentences kept verbatim; verify green (scripts 409, hooks 179, plugin validate x2, plugin test 2018), skills/tests 829 OK.
- 2026-10-17: T2 done: `TestPromoteCarriesHigh` (7 tests, whitespace-collapsed steps) in `skills/tests/test_candidate_priority_token.py`; three planted removals (carries-high sentence, apply clause, fence order) each turned their own test red, file restored byte-identical; skills/tests 836 OK.
- 2026-10-17: T3 done: README candidate-pane paragraph and a CHANGELOG Unreleased entry; skills/tests 836 OK, scripts 409 OK.
- 2026-10-17: T4 done: D-179 appended (annotates D-134, passes D-108's door on its retained trigger); validate green; verify green (scripts, hooks, plugin validate x2, plugin test 2018 pass); skills/tests 836 OK.
- 2026-10-17: claim audit: 30 claims read, 4 corrected — skills/cairn-triage/SKILL.md, CHANGELOG.md (row "sits with the `[high]` rows", not "stays first"; promote changes nothing of its own beyond the carried change; "before" claims limited to normal and low rows; the guard's apply sentence updated to match); the same reader re-read all four as true.
- 2026-10-17: implement complete; verify green after the claim fixes; status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
