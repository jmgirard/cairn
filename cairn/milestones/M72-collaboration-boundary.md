<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M72: Collaboration boundary — what survives a merge outside cairn, plus PR-bound approval

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP1   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m72-collaboration-boundary`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

State plainly which parts of cairn's approval model survive a merge made
outside a cairn session, and bind the merge-approval marker to the specific PR
it authorizes.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a rulebook passage in "Git and approval model" naming what is
agent-session-scoped (merge_guard, force_push_guard) versus honor-system under
a GitHub-UI merge, a merge queue, or a contributor without the plugin; a
plain-words README subsection saying the same to a human; `merge_guard.py`
reading the marker body and refusing a `gh pr merge` for a PR the marker does
not name; the two marker-writing skills updated to the bound form. Closes RR01
§10 rec 4 (`cairn/reviews/archive/RR01-architecture-retrospective.md:395-400`),
which recorded this gap and was never actioned.

**Out:** an entry point for externally-authored PRs → M73. Issue enumeration →
M74. Concurrent-cairn-operator races (ID allocation, duplicate D-numbers,
pull-before-plan, the one-in-progress cap) → candidate rows. A CONTRIBUTING /
PR-template scaffold → candidate row. Branch-protection compatibility for the
docs-only direct pushes → candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/shared/tracking-rules.md` "Git and approval model" states
      which guarantees are enforced only inside a cairn-equipped session and
      which degrade to honor-system when the merge happens elsewhere (GitHub
      UI, merge queue, unplugged contributor), naming `merge_guard` and
      `force_push_guard` as agent-session-scoped. Evidence: the passage quoted
      + its guard test green.
- [ ] AC2 — `README.md` carries a human-facing subsection saying the same in
      plain words: what cairn will block, and what it cannot see.
- [ ] AC3 — `hooks/merge_guard.py` denies `gh pr merge <N>` when the marker
      body names a different PR, and the deny reason names both numbers.
      Evidence: a new `TestMergeGuard` case.
- [ ] AC4 — the same hook allows-and-consumes when the marker names the same
      PR, and still allows when the marker body names no PR at all
      (back-compat for `git merge` and legacy markers). Evidence: two
      `TestMergeGuard` cases.
- [ ] AC5 — `/milestone-review` and `/hotfix` write the PR-bound marker form
      at their approval gates. Evidence: grep of the two SKILL.md files
      (tracking lines in this milestone file are not evidence).
- [ ] AC6 — the new prose-guard file is registered in
      `skills/tests/test_mutation_harness.py`; the completeness meta-test is
      green.
- [ ] AC7 — the `verify` slot is clean: all three `unittest discover` suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T5
- AC2 → T2
- AC3 → T3, T4
- AC4 → T3, T4
- AC5 → T3
- AC6 → T5
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Write the boundary passage into `skills/shared/tracking-rules.md`
      "Git and approval model" (after the `.merge-approved` paragraph,
      `:265-271`). Keep it ≤10 lines; the rulebook is already long.
      *(RB tripwire: ip-touching — the passage states where IP1's mechanical
      backing stops.)*
- [ ] T2 — Add the README subsection. Plain words, no rulebook jargon; this is
      the surface a collaborator reads.
- [ ] T3 — Bind the marker: `hooks/merge_guard.py` parses a PR number from the
      marker body and compares it to the `gh pr merge <N>` target
      (`hooks/cairn_common.py:29` `GH_PR_MERGE` is the existing detection);
      mismatch → deny; no PR token in the body → today's existence check.
      Update the marker-write lines in `skills/milestone-review/SKILL.md` and
      `skills/hotfix/SKILL.md:54-57` to the bound form.
- [ ] T4 — Extend `TestMergeGuard` in `hooks/tests/test_hooks.py:186-292`:
      match allows+consumes, mismatch denies, PR-less body allows. Check
      `merge_guard_post`'s restore path still keys on the identical detection.
- [ ] T5 — New guard test for the T1 passage; register it in
      `skills/tests/test_mutation_harness.py` (per-file registration, ≥1
      exemplar block on ONE physical line — M59/M65).
- [ ] T6 — Run all three suites from the repo root; update `cairn/DESIGN.md`'s
      "Known issues" honor-system bullet to cite the new passage instead of
      restating it.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: in-progress on `m72-collaboration-boundary`.
- 2026-07-18: implement gate — marker binding requires the explicit PR number in the merge command (bare `gh pr merge` denied); marker stays prose with `for PR #<N>` appended; ip-touching tripwire on T1 not escalated (user choice).
- 2026-07-18: T1 — boundary passage + PR-binding bullet added to tracking-rules "Git and approval model"; three single-line mutation anchors verified unique.

## Decisions
<!-- owner: implement / review · append-only -->
