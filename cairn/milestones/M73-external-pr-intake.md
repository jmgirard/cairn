<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M73: External-PR intake — /hotfix adopts a PR it did not author

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M72   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m73-external-pr-intake`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give the intake doctrine's "external PRs → review to the hotfix bar" an actual
entry point, by teaching `/hotfix` to adopt an existing PR instead of always
creating one.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** an incoming-PR branch through `/hotfix` — recognize a PR reference,
`gh pr checkout` it rather than cutting `hotfix-<slug>`, add the missing
regression test to the contributor's head, handle a missing changelog entry,
and reach the existing merge-approval chip; the branch-naming contract
(`tracking-rules.md:253`) exempting an adopted contributor branch; the skill's
`description:` frontmatter updated so an incoming PR routes here at all (today
it fires only on bug *reports*); the Intake paragraph
(`tracking-rules.md:199-203`) naming the door it currently lacks.

**Out:** GitHub issue enumeration → M74. Anything for PRs too large for the
hotfix bar — those keep today's disposition (become/join a milestone via
`/milestone-plan`), unchanged. Fork-PR push permissions are handled by a
documented fallback, not by new machinery. Concurrent-operator races and the
CONTRIBUTING scaffold → candidate rows (see M72 Out).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `skills/hotfix/SKILL.md` carries an incoming-PR path: given a PR
      reference, step 2 checks the PR out instead of branching, and the step
      states that the contributor's branch name is exempt from the
      `hotfix-<slug>` contract. Evidence: the steps quoted.
- [ ] AC2 — the regression-test step states the adopted-PR form honestly: the
      test is *added* and must fail against the default branch and pass on the
      PR head (the author-side "fails before the fix" sequence is unreachable
      when the fix already exists).
- [ ] AC3 — the changelog step covers "contributor already added one" and
      "none present", and names the fallback when the fork's head branch
      cannot be pushed to.
- [ ] AC4 — the merge step notes the `--delete-branch` caveat for a fork PR
      and otherwise reuses M72's PR-bound marker + the existing approval chip
      unchanged. Evidence: the step quoted; no second approval mechanism added.
- [ ] AC5 — `/hotfix`'s `description:` frontmatter names incoming PRs as a
      trigger, and `tracking-rules.md`'s Intake paragraph names `/hotfix` as
      the door for the hotfix-bar disposition.
- [ ] AC6 — guard tests lock AC1's incoming-PR path and AC5's Intake wording;
      the new guard file is registered in
      `skills/tests/test_mutation_harness.py` and the completeness meta-test
      is green. `test_search_first_candidates.py` still passes (its asserted
      Intake substrings must survive the rewording).
- [ ] AC7 — the `verify` slot is clean: all three `unittest discover` suites
      pass from the repo root.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Add the incoming-PR branch to `/hotfix` steps 1–2
      (`skills/hotfix/SKILL.md:19-30`): tier-check the PR's diff against the
      hotfix bar first (too large → route to `/milestone-plan`, unchanged),
      then `gh pr checkout <N>`; state the branch-name exemption and mirror it
      in `tracking-rules.md:253` and `hooks/commit_guard.py:67`'s nudge text.
- [ ] T2 — Rewrite step 3 (`:32-33`) to carry both forms: author-side
      (fail→fix→pass) and adopted-side (add test; fail on default branch, pass
      on PR head).
- [ ] T3 — Extend step 5 (`:39-45`) for the adopted case, incl. the
      no-push-to-fork fallback.
- [ ] T4 — Extend step 6 (`:47-60`) with the fork `--delete-branch` caveat;
      confirm the marker line matches M72's bound form (no divergence).
- [ ] T5 — Update the frontmatter `description:` (`:3`) and the Intake
      paragraph (`tracking-rules.md:199-203`).
- [ ] T6 — Write the guard tests; register in the mutation harness; re-run
      `test_search_first_candidates.py` and `test_idea_intake_gate.py`, both of
      which assert Intake-adjacent substrings.
- [ ] T7 — Run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: implement gate — inline both forms in steps 1–6; fork fallback
  is ask-then-re-land-locally; commit_guard nudge mirror dropped (T1
  amendment: the hook returns early off the default branch, so the exemption
  text is unreachable there). All three user-selected.
- 2026-07-18: T1 — /hotfix steps 1–2 carry the adopt-a-PR form; branch-name
  exemption stated in tracking-rules git model. verify clean.

## Decisions
<!-- owner: implement / review · append-only -->
