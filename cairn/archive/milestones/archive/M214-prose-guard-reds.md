# M214: Clear the prose-guard reds

**Status:** done (2026-10-04, PR #221 https://github.com/jmgirard/cairn/pull/221)

**Goal:** The hand-run `skills/tests` suite passes again, with each stale guard repointed to the current prose or deleted.

**Outcome:** `test_default_branch_parameterized.py` asserts the `<base>`
spellings of the default-branch recipe (`git ls-remote --symref <base>
HEAD`, `refs/remotes/<base>/HEAD`) that M185 wrote. The matching
Mutation block in `test_mutation_harness.py` follows. The hotfix two-way
guard in `test_resume_routing.py` asserts the passages before and after the
guest-arm sync clause, which it no longer pins.
`test_partial_coverage_was_trimmed_not_deleted` is deleted from
`test_lesson_graduation.py`, because the LESSONS lines it pinned were pruned
or corrected. The suite went from 4 failures and 1 error to 665 tests, OK.

**Decisions:** none. Repairs and a deletion sit outside the D-090/D-108
door, and no red was a firing of D-109's falsifier.

**Review:** three-lens fan-out, 13 findings: 1 fixed (a Review line corrects
the Scope's account of the pruned lessons), 12 rejected (8 planned changes,
4 false), none to follow-up. Nothing retired.
