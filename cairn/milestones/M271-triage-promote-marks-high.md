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
- **Branch/PR:** m271-triage-promote-marks-high, https://github.com/jmgirard/cairn/pull/283   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: `skills/cairn-triage/SKILL.md` makes every `promote` that stands
      at Accept for a candidate row whose opening token is not `[high]`,
      whether proposed or set at an Amend, carry a priority change to `high`,
      stated in the `promote` row of step 2's disposition table and in step
      3's reason-cell rule; the chip names that change once, with the
      promote; Amend cannot decline that change alone; a `promote` of a Known
      issues entry carries none.
- [x] AC2: The same file's step 4 applies that change as it applies any
      accepted priority change: `[high] ` is added to an untagged row or
      replaces its `[low] ` token, and the row moves into the high level of
      the order; step 3's byte-for-byte rule names this edit among its
      carve-outs.
- [x] AC3: The same file's step 4 skip condition and step 7's `nothing
      applied` condition count an accepted `promote` as changing no file
      only when it carries no priority change and no token change.
- [x] AC4: The same file's step 7 orders the `/milestone-plan` fences of the
      accepted promotes as candidate rows in table order, then Known issues
      entries in table order.
- [x] AC5: `git grep -n -F 'change nothing of their own' -- skills README.md`
      and ``git grep -n -F '`promote` (with no token' -- skills README.md``
      each return no line, and README.md's candidate-pane paragraph and a
      `CHANGELOG.md` `## Unreleased` entry each say that a `/cairn-triage`
      promote gives the row `[high]`.
- [x] AC6: The `verify` slot of `cairn/PROFILE.md` passes on the branch
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

Review head da54fc3b; PR #283 opened at review start (Copilot round on).

- AC1: `skills/cairn-triage/SKILL.md:281` (promote table row: a candidate row not `[high]` takes the change to `high`; Known issues entry takes none), `:395-400` (reason-cell rule: every promote of such a row, proposed or set at Amend, carries it; Known issues promote carries none), `:408-410` (chip names it once), `:417-419` (Amend cannot decline it alone). Pass.
- AC2: `SKILL.md:474-478` — "an accepted priority change, a promote's included, adds, replaces, or removes the row's opening token ... and moves the row to its level"; `:487` orders candidates high → normal → low; `:442-443` names the promote's change as the fourth byte-for-byte carve-out. Pass.
- AC3: `SKILL.md:445-447` skip condition reads "every item `keep` or `promote` with no priority change and no token change, or nothing enumerated"; `:556-558` `nothing applied` covers "an accept of only `keep` and `promote` items with no priority or token change". Pass.
- AC4: `SKILL.md:568-570` — "Several promotes take several blocks: the candidate rows first, in table order, then the Known issues entries, in table order." Pass.
- AC5: both `git grep -n -F` commands exit 1 with no line; `README.md:318-320` and the `CHANGELOG.md` `## Unreleased` entry (line 7-15) each say a `/cairn-triage` promote gives the row `[high]`. Pass.
- AC6: verify on da54fc3b — scripts/tests 409 OK (21 skipped), hooks/tests 179 OK, plugin validate (plugin, marketplace) exit 0, plugin test 2018 pass 0 fail; hand-run skills/tests 836 OK against 829 OK at the branch point, so no failing test. Pass.
- Consistency gate: cairn_validate all checks passed; no principle changed (cairn_impact skipped); marketplace validate shows no `plugins[N].version` warning; CHANGELOG has the entry, no milestone numbers.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: Amend-set promote vs. a proposed `→ low` on the same row is unsettled — fix now (the promote's change replaces any other proposed priority change)
- diff-bug #2: a misspelled opening token (`[HIGH]`) stays beside the written `[high]` — fix now (apply step counts a misspelled opening token as the row's token)
- diff-bug #3: D-179 changes `[high]`'s meaning but says it only annotates D-134 — fix now (D-180 records it as a narrowing)
- diff-bug #4: the new guards are not in the mutation registry — fix now (13 entries; the blanking test passes)
- diff-bug #5: several new rules have no guard — fix now (guards added for the table row, Readiness class, replaces-other-change, chip level, fourth carve-out, `nothing applied`)
- diff-bug #6: "once, in the promote's own words" may leave `high` unsaid in the chip — fix now (chip names "its new level `high`")
- diff-bug #7: an Amend-set promote on a row with a live started token writes `[high]` and a fence for taken work — follow-up (candidate row "Triage promote edges (M271 review)")
- diff-bug #8: unclear whether each row of a §7 group takes `[high]` and a fence — follow-up (same row)
- diff-bug #9: the cap overflow note omits promoted rows' stamp length — fix now
- diff-bug #10: status line and step 5's record list omit priority changes — fix now
- diff-bug #11: D-179 credits D-027 with the vocabulary — fix now (D-180)
- diff-bug #12: D-179's Rejected clause reads as if the user chose the rejected option — fix now (D-180)
- diff-bug #13: the D-108 trigger is arguable since promote worked as designed — reject, planned change: the user asked for the mark at the plan, and D-179 records the reasoning
- diff-bug #14: the Goal says "stays first"; the skill puts the row among the `[high]` rows — reject, false as a criterion failure: review checks the criteria, and AC2 states the placement and passes; the archive summary words the goal as shipped
- diff-bug #15: "the cairn pane marks it ↑" stated without conditions — fix now ("While the cairn pane lists candidates")
- diff-bug #16: the rule is written in three places — reject, style: each site is the skill's own place for it, and each is now guarded
- blame-history #1: the no-mark promote was designed (M173, M251) and other paths keep it — reject, planned change: the user chose the mark; the Out section says why the other paths hand on at once
- blame-history #2: D-134 overload not recorded — fix now (D-180 (1))
- blame-history #3: the fence-order change has no decision record — fix now (D-180 (4))
- blame-history #4: the decline-alone right from M259 is narrowed without a record — fix now (D-180 (4))
- prior-review #1: no mutation-registry entries — fix now (as diff-bug #4)
- prior-review #2: the chip may not show the new level — fix now (as diff-bug #6)
- prior-review #3: barring a decline alone runs against M259's pattern — reject, planned change: the user's answer at the question set
- prior-review #4: only one of three statement sites pinned — fix now (as diff-bug #5)
- prior-review #5: one guard pins prose, and the step-7 read runs to EOF — reject, false: prose guards pin prose by design, and step 7 is the file's last section
- prior-review #6: fence order changed from M179's fix — noted (context, no defect)
- copilot: cairn/milestones/M271-triage-promote-marks-high.md:14 (header lacks the PR URL) — fix now, fixed 363980e1
- copilot: skills/tests/test_candidate_priority_token.py:117 (new asserts not in the mutation registry) — fix now, fixed 363980e1
- copilot: review body (index of the two threads above) — noted
- Copilot level: unknown (set by GitHub's settings; the review body has no `Review effort:` line)
- conversation: no human reviews, comments, or other threads on PR #283
