# M25: Parameterize the default branch in the operational skill steps

- **Status:** done · **Depends on:** M22 · **PR:** #23 (merged 2026-07-12)

**Goal.** Make the four operational skills issue git operations against the
repo's detected default branch instead of hardcoded `main` — finishing at the
operational layer what M22 established as doctrine.

**Outcome.** `/milestone-implement`, `/milestone-review`, `/hotfix`, and
`/cairn-release` are free of hardcoded `main`; each detects the branch at
runtime via one canonical recipe in the tracking-rules git model
(`git symbolic-ref --short refs/remotes/origin/HEAD`, remote-querying
fallback, ask only if no remote). `test_default_branch_parameterized.py`
extended (+5 tests) locking the four skills + the recipe. 8 files, +175/−65.

**Key decisions (M25-local).** Runtime detection, not a stored branch name
(plan gate). Review fixed both sub-80 diff-bug findings anyway: the fallback
now queries the remote rather than guessing local HEAD (which returns the
*feature* branch on review/hotfix/resume); "a step below" dangling ref
reworded. Date-scan false positive kept separate (candidate G-C2).

**Verification.** 6/6 acceptance criteria evidenced; consistency gate 10/10;
2-lens+scorer independent review (blame-history clean). No CI on this repo.
