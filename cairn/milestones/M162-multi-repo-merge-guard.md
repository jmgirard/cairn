<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M162: Multi-repo sessions: the merge guard's cross-repo contract

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP1, IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m162-multi-repo-merge-guard   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

One-session-multi-repo merges stop mis-gating: the guard denies the
cross-repo `gh pr merge` forms its tokenization can see, and the per-repo
approval contract is documented.

## Scope
<!-- owner: plan · create/amend-via-gate -->

Tier: user-facing — the merge guard's deny/allow behavior ships to every
adopting repo.

**In:** deny repo-targeting flag tokens and `GH_REPO=` env prefixes on
`gh pr merge`; remove the URL-positional acceptance; see through leading
env-assignment prefixes in the shared command-position pattern; document
the per-repo contract and the remaining redirections. Enforces the shipped
promise "an approval authorizes exactly the PR it names" (D-107 Untouched
clause) — a repair, not a promise widening. Narrows two M72-review-era
allows (repo-flag values, URL positionals), surfaced and approved at the
plan gate; no D-entry stood on them.

**Out:** repo-qualified marker binding and target-repo keying (full
multi-repo support) → declined at the plan gate, the candidate row's remedy
space stands superseded by this scope; portable marker for non-cairn repos
→ declined, out of contract (docs state it); env-prefix holes in
`commit_guard.py`/`force_push_guard.py`'s own `CMD_POS` copies → new
candidate row; two-operators-one-repo → existing concurrent-cairn-operator
candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `merge_guard.py` denies — before the marker-existence check, and
      with `cairn/.merge-approved` byte-identical after the denial — every
      `gh pr merge` occurrence whose segment tokens contain a
      repo-targeting flag token. A shared `cairn_common` helper yields each
      occurrence's token list (keeping the never-raises `shlex` fallback),
      consumed by both `gh_merge_pr_numbers` and this predicate; the
      predicate walks tokens with `_first_pr_token`'s value-flag skip and
      fires on a token equal to `--repo`, beginning with `--repo=`, or
      matching `^-[A-Za-z]*R`. The denial message states that an approval
      binds the repo whose `cairn/.merge-approved` records it and that the
      merge must run from the target repo without a repo flag or `GH_REPO`
      in the environment. Behavior to test: each predicate limb; a bundled
      cluster (`-sdR`); the flag before and after the PR positional; a
      chained command whose second occurrence alone carries the flag;
      denial with the marker present and absent; negative controls — `-sd`
      and `-r` clusters allowed, a repo flag in a preceding or following
      non-merge segment not denying, a value token like
      `--subject "-Recovered null deref"` not denying (value-flag skip).
- [ ] AC2: every `gh pr merge` occurrence whose PR positional is not a
      bare digit string is denied without consuming the marker via the
      existing does-not-name-a-PR denial, whose message prescribes the
      bare-number spelling — the `/pull/<N>`-tail URL acceptance is
      removed. The value-flag allows the M72 tests lock survive as allows:
      `-m 7`, `--subject "fix issue 9" 7`, `-t 'bump to 9' 7`. Behavior to
      test: a `/pull/7` URL (previously allowed), a `/pull/7/files` URL
      (previously denied via the no-PR path), a branch-name positional,
      marker untouched, and the three surviving allows.
- [ ] AC3: `cairn_common`'s shared command-position pattern sees through
      leading environment-assignment prefixes (`VAR=value` words before
      the command word) — so `merge_guard_post.py` keys identically — and
      a `gh pr merge` occurrence whose prefix assigns `GH_REPO` is denied
      with AC1's message. Behavior to test: `GH_REPO=o/r gh pr merge 5`
      denied with the marker present and absent;
      `A=1 GH_REPO=o/r gh pr merge 5` (multi-assignment) denied;
      `echo hi; GH_REPO=o/r gh pr merge 5` (post-separator) denied;
      `FOO=1 gh pr merge 5` guarded exactly like the unprefixed spelling
      (marker consumed), and a `PostToolUseFailure` on it restores
      `cairn/.merge-approved` byte-identical; an assignment spelling in
      argument position (`echo GH_REPO=x gh pr merge 5`) still ignored.
- [ ] AC4: the multi-repo contract is stated in two places:
      `merge_guard.py`'s known-limitations docstring paragraph —
      explicitly non-exhaustive — names compound `cd … && gh pr merge`,
      subshells, alias/wrapper invocations, `GH_HOST`, and
      assignment values containing whitespace or quoting as redirections
      the detection does not see; and tracking-rules' "Git and approval
      model" section states that an approval binds one repo (the marker
      lives in the merged repo's own `cairn/`), that a secondary repo's
      merge runs from a session cwd inside that repo, and that a repo
      without cairn tracking is outside the guard entirely (an improvised
      marker there does nothing — such merges are gated by chat approval
      alone, or the repo adopts cairn). Verified by reading the two named
      files.
- [ ] AC5: both gating suites pass (`scripts/tests`, `hooks/tests`).

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T3
- AC3 → T1, T4
- AC4 → T5
- AC5 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: red tests in `hooks/tests/test_hooks.py`: AC1's predicate limbs,
      positions, chain, negative controls; AC2's positional cases and the
      three surviving allows (rework the two M72-era subTest loops at
      `test_hooks.py:957` and `:1040`, keeping their allow cases); AC3's
      env-prefix matrix including the post-hook restore case.
- [x] T2: extract the shared occurrence-tokens helper in
      `hooks/cairn_common.py` (from `gh_merge_pr_numbers`'s inline
      segmentation, `cairn_common.py:94-103`); add the repo-flag predicate
      with the value-flag skip; hoist the denial branch above the
      marker-existence check in `hooks/merge_guard.py` with the two-limb
      message.
- [x] T3: remove `_PR_URL_TAIL` and its branch in `_first_pr_token`
      (`cairn_common.py:65,121-123`); confirm URL/branch positionals fall
      to the existing no-PR denial.
- [ ] T4: extend `CMD_POS` in `cairn_common.py` with the env-assignment
      prefix run; add the `GH_REPO=` prefix denial; leave
      `commit_guard.py`/`force_push_guard.py` copies untouched.
- [ ] T5: docs — the guard docstring's non-exhaustive limitations
      paragraph; tracking-rules "Git and approval model" per-repo contract
      sentences.
- [ ] T6: run both gating suites from the repo root, each exit code
      checked explicitly; hand-run `skills/tests` (tracking-rules edit
      touches guarded prose).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-29: created by /milestone-plan from the multi-repo candidate row (added 2026-08-29, hitop/hitop-builder session); row pruned at post-merge hygiene, not at plan.
- 2026-08-29: criteria audit ran in full mode ([O] fresh reader, two passes): pass 1 returned 11 findings (unsatisfiable message ordering; hand-list token enumeration defeated by short-option bundling; URL-predicate ambiguity; instrument-bound clauses; the GH_REPO no-fire hole; the M72-allow reversal), pass 2 over the gate-changed wording returned 10 (subTest-loop coverage destruction; missing negative controls on the R-cluster and segment boundary; unshared segmentation; post-hook pending-strand risk; message/mechanism mismatch; CMD_POS triplication; new undocumented boundaries; value-token false denial) — all repaired into the AC wording above or routed to Out.
- 2026-08-29: plan gate chose minimal repair + docs over docs-only because the false-authorization vector (local marker #N authorizes `-R other N`) was live and observed, and over full multi-repo support because repo-qualified binding widens the guard's promise (D-107 regress shape); falsified by a cross-repo mis-gating this scope's denials do not reach.
- 2026-08-29: plan gate chose fixing CMD_POS env-prefix detection over documenting it as accepted because `GH_REPO=` today makes the guard not fire at all (IP1 hole in single-repo sessions too); falsified by the extended pattern denying a legitimate spelling in practice.
- 2026-08-29: plan gate chose narrowing the M72-era allows (repo-flag values, URL positionals become denials; value-flag allows survive) over keeping URLs allowed because the URL form is a cross-repo vector the number check cannot see; falsified by a legitimate same-repo workflow that must merge by URL.
- 2026-08-29: plan gate chose out-of-contract docs for non-cairn secondary repos over a portable marker mode because a repo that never adopted cairn has no enforcement surface to key on (D-043 boundary-over-machinery); falsified by the hitop-builder pattern recurring with a real unapproved merge.
- 2026-08-29: implement started on m162-multi-repo-merge-guard; question gate skipped (plan gate settled all open choices, no tripwire tags).
- 2026-08-29: T1 done — AC1/AC2/AC3 test matrices added, two M72-era subTest loops reworked keeping their allow cases; 13 reds confirmed pre-change, each failing as the pre-change behavior the plan names (repo flags allowed, GH_REPO unseen, /pull/7 URL allowed, -sdR mis-denied via no-PR path, post hook blind to prefixes).
- 2026-08-29: T2 done — `gh_merge_occurrence_tokens` extracted (shlex fallback kept), `names_repo_target` predicate added, denial hoisted above the marker check in `merge_guard.py`; AC1 tests green, remaining reds are the T3/T4 targets only (URL positional, env prefixes).
- 2026-08-29: T3 done — `_PR_URL_TAIL` and its `_first_pr_token` branch removed; URL positionals fall to the existing no-PR denial (both URL tests green), remaining reds are T4's env-prefix targets only.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion. -->
