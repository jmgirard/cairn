<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M73: External-PR intake — /hotfix adopts a PR it did not author

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M72   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m73-external-pr-intake` · https://github.com/jmgirard/cairn/pull/71   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1 — `skills/hotfix/SKILL.md` carries an incoming-PR path: given a PR
      reference, step 2 checks the PR out instead of branching, and the step
      states that the contributor's branch name is exempt from the
      `hotfix-<slug>` contract. Evidence: the steps quoted.
- [x] AC2 — the regression-test step states the adopted-PR form honestly: the
      test is *added* and must fail against the default branch and pass on the
      PR head (the author-side "fails before the fix" sequence is unreachable
      when the fix already exists).
- [x] AC3 — the changelog step covers "contributor already added one" and
      "none present", and names the fallback when the fork's head branch
      cannot be pushed to.
- [x] AC4 — the merge step notes the `--delete-branch` caveat for a fork PR
      and otherwise reuses M72's PR-bound marker + the existing approval chip
      unchanged. Evidence: the step quoted; no second approval mechanism added.
- [x] AC5 — `/hotfix`'s `description:` frontmatter names incoming PRs as a
      trigger, and `tracking-rules.md`'s Intake paragraph names `/hotfix` as
      the door for the hotfix-bar disposition.
- [x] AC6 — guard tests lock AC1's incoming-PR path and AC5's Intake wording;
      the new guard file is registered in
      `skills/tests/test_mutation_harness.py` and the completeness meta-test
      is green. `test_search_first_candidates.py` still passes (its asserted
      Intake substrings must survive the rewording).
- [x] AC7 — the `verify` slot is clean: all three `unittest discover` suites
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
- [x] T2 — Rewrite step 3 (`:32-33`) to carry both forms: author-side
      (fail→fix→pass) and adopted-side (add test; fail on default branch, pass
      on PR head).
- [x] T3 — Extend step 5 (`:39-45`) for the adopted case, incl. the
      no-push-to-fork fallback.
- [x] T4 — Extend step 6 (`:47-60`) with the fork `--delete-branch` caveat;
      confirm the marker line matches M72's bound form (no divergence).
- [x] T5 — Update the frontmatter `description:` (`:3`) and the Intake
      paragraph (`tracking-rules.md:199-203`).
- [x] T6 — Write the guard tests; register in the mutation harness; re-run
      `test_search_first_candidates.py` and `test_idea_intake_gate.py`, both of
      which assert Intake-adjacent substrings.
- [x] T7 — Run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan.
- 2026-07-18: implement gate — inline both forms in steps 1–6; fork fallback
  is ask-then-re-land-locally; commit_guard nudge mirror dropped (T1
  amendment: the hook returns early off the default branch, so the exemption
  text is unreachable there). All three user-selected.
- 2026-07-18: T1 — /hotfix steps 1–2 carry the adopt-a-PR form; branch-name
  exemption stated in tracking-rules git model. verify clean.
- 2026-07-18: T2 — step 3 states both sequences; adopted form is add-the-test
  + prove fail-on-default / pass-on-head via a scratch worktree. verify clean.
- 2026-07-18: T3 — step 5 covers entry-already-present / none-present and the
  no-push-to-fork fallback (ask, then re-land locally). verify clean.
- 2026-07-18: T4 — step 6 drops --delete-branch on a fork PR; marker line
  already matches M72's PR-bound form, left unchanged. verify clean.
- 2026-07-18: T5 — /hotfix description names incoming PRs; Intake paragraph
  names /hotfix as the door. verify clean.
- 2026-07-18: T6 — test_external_pr_intake.py (17 tests) + 9 mutation-registry
  entries; completeness meta-test green; the two Intake-adjacent guards
  (search-first, idea-intake) still pass. skills suite 246 → 263.
- 2026-07-18: T7 — verify slot clean (263/96/72 across the three suites);
  cairn_validate all checks passed. Status → review.

## Decisions
<!-- owner: implement / review · append-only -->

## Review
<!-- owner: review · exclusive -->

**PR:** https://github.com/jmgirard/cairn/pull/71 · reviewed 2026-07-18

### Acceptance-criteria evidence

- AC1 — `SKILL.md:19-42` quoted: step 1 tier-checks the PR's own diff via
  `gh pr view/diff <N>`; step 2's *Adopting a PR* branch runs
  `gh pr checkout <N>` ("never cut a fresh branch, which would orphan work
  that already exists") and states the name is "**exempt** from the
  `hotfix-<slug>` contract". Mirrored at `tracking-rules.md:255-259`.
- AC2 — `SKILL.md:43-54` quoted: the adopted form states the author-side
  sequence "is unreachable", the test is "**added**", and it must fail
  against the default branch and pass on the PR head, with a scratch-worktree
  recipe for proving the first direction.
- AC3 — `SKILL.md:68-80` quoted: contributor-entry-present (check + edit in
  place, no duplicate) and none-present (add one); the no-push fallback asks
  the contributor first, then re-lands locally with `Co-authored-by:` credit,
  and never merges a fix missing its regression test.
- AC4 — `SKILL.md:82-100` quoted: `--delete-branch` dropped for fork PRs;
  the marker line and approval chip are M72's, unchanged. Guard
  `test_no_second_approval_mechanism` asserts exactly one
  `cairn/.merge-approved` mention — no second approval mechanism.
- AC5 — `SKILL.md:3` frontmatter names incoming PRs ("or adopt an incoming
  external PR that fixes one" + the `"adopt PR #12"` trigger phrases);
  `tracking-rules.md:199-205` Intake names "**`/hotfix` is the door**" and
  keeps the larger-PR route to `/milestone-plan`.
- AC6 — `test_external_pr_intake.py`: 17 tests, all pass. 9 blocks registered
  in the mutation harness; `test_each_registered_guard_fails_when_its_block_is_blanked`
  and `test_every_prose_guard_is_registered_or_exempt` both green.
  False-coverage check by script: all 18 asserted phrases occur exactly once
  in their target file (0 non-unique). `test_search_first_candidates.py` (4)
  and `test_idea_intake_gate.py` (5) still pass.
- AC7 — verify slot clean from the repo root: skills 263, scripts 96,
  hooks 72 — all OK.

### Consistency gate

- `cairn_validate.py` exit 0 — all 17 checks passed.
- `consistency-gate` slot (`generic`) names no toolchain checks — clean no-op.
- No DESIGN principle changed (Principles touched: —) → `cairn_impact` skipped.
- No `.github/` in the repo: there is no CI, so the green-CI wait is a no-op.

### Independent review (three lenses + scorer)

- **[O] diff-bug (Opus):** independently re-derived AC1–AC7 as met; confirmed
  guard soundness (all asserted substrings unique) and that all 9 registry
  blocks are exact. 5 findings raised.
- **[S] blame-history (Sonnet):** zero findings — every pre-M73 clause
  survives verbatim in the *Authoring a fix* halves; M72's marker text is
  character-identical; independently confirmed T1's dropped `commit_guard.py`
  mirror was correct (the hook returns early off the default branch).
- **[S] prior-PR-comments (Sonnet):** no prior-PR evidence — this repo's PRs
  carry no GitHub-side review comments (review happens locally). Clean no-op.

**Scorer ([S], fresh context): all 5 findings scored below 80 → none
actioned; logged here per IP3.**

1. (63) `SKILL.md:68` vs `:78` — "never open a second one" reads as
   contradicting the fallback's "open a PR that credits them"; a qualifier
   would remove the ambiguity, but the bolded no-push sub-case resolves it
   on a full read.
2. (48) `SKILL.md:74-79` — the fork fallback's comment/close/re-land sequence
   is ungated. Scorer: the authoring path's PR-opening is equally ungated,
   IP1 scopes approval to the default branch, and M73's Scope frames this as
   "a documented fallback, not new machinery".
3. (25) `test_mutation_harness.py:810-813` — registry comment claims one
   entry per block; 8 of 17 asserts unregistered. Scorer: M71's cited
   precedent also leaves asserts unregistered, completeness is per guard
   *module*, and no live false-coverage bug exists.
4. (68) `SKILL.md:50-52` — the scratch-worktree recipe names no path and no
   `git worktree remove`; a stray untracked dir could trip step 2's own
   dirty-tree check.
5. (35) `DESIGN.md:68` / `README.md:118,194` still describe the pre-M73
   trigger. Scorer: neither file is in M73's Scope In; the DESIGN line is
   incomplete rather than false — candidate-row-worthy, not an in-scope
   defect.
