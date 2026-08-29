<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M162: Multi-repo sessions: the merge guard's cross-repo contract

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP1, IP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m162-multi-repo-merge-guard · https://github.com/jmgirard/cairn/pull/163   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [x] AC1: `merge_guard.py` denies — before the marker-existence check, and
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
- [x] AC2: every `gh pr merge` occurrence whose PR positional is not a
      bare digit string is denied without consuming the marker via the
      existing does-not-name-a-PR denial, whose message prescribes the
      bare-number spelling — the `/pull/<N>`-tail URL acceptance is
      removed. The value-flag allows the M72 tests lock survive as allows:
      `-m 7`, `--subject "fix issue 9" 7`, `-t 'bump to 9' 7`. Behavior to
      test: a `/pull/7` URL (previously allowed), a `/pull/7/files` URL
      (previously denied via the no-PR path), a branch-name positional,
      marker untouched, and the three surviving allows.
- [x] AC3: `cairn_common`'s shared command-position pattern sees through
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
- [x] AC4: the multi-repo contract is stated in two places:
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
- [x] AC5: both gating suites pass (`scripts/tests`, `hooks/tests`).

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
- [x] T4: extend `CMD_POS` in `cairn_common.py` with the env-assignment
      prefix run; add the `GH_REPO=` prefix denial; leave
      `commit_guard.py`/`force_push_guard.py` copies untouched.
- [x] T5: docs — the guard docstring's non-exhaustive limitations
      paragraph; tracking-rules "Git and approval model" per-repo contract
      sentences.
- [x] T6: run both gating suites from the repo root, each exit code
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
- 2026-08-29: T4 done — `CMD_POS` gains the env-assignment prefix run (guard copies in commit/force-push guards untouched, candidate row stands), `gh_merge_gh_repo_prefixed` added, denial message names the GH_REPO limb; both suites green (hooks 112 OK, scripts 324 OK).
- 2026-08-29: T5 done — guard docstring gains the non-exhaustive cross-repo limitations paragraph (cd-compound, subshells, alias/wrapper, GH_HOST, whitespace/quoted assignment values); tracking-rules "Git and approval model" gains the approval-binds-one-repo bullet (secondary repo merges from its own cwd; non-cairn repos outside the guard, chat-approval-gated).
- 2026-08-29: T6 done — all three suites exit 0 (scripts 324, hooks 112, skills 528 hand-run); status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive; evidence per criterion. -->

- 2026-08-29 evidence, branch a9c712c, PR #163 (draft):
- AC1: hooks suite fresh-run green (112 tests, exit 0). Predicate limbs and positions: `test_repo_flag_is_denied_marker_present` (`--repo`, `--repo=`, `-R`, bundled `-sdR`, flag after the positional), `test_repo_flag_is_denied_before_the_marker_existence_check` (marker absent → still the cross-repo denial), `test_chained_second_occurrence_repo_flag_is_denied`; negative controls in `test_repo_predicate_negative_controls_still_allowed` (`-sd`, `-r`, repo flag in preceding/following non-merge segment, `--subject "-Recovered…"` value-flag skip). Marker byte-identity asserted in `assert_repo_denied` for every denial. Code read: shared `gh_merge_occurrence_tokens` (shlex fallback kept, cairn_common.py) feeds both `gh_merge_pr_numbers` and `names_repo_target`; denial hoisted above the marker-existence check (merge_guard.py) with the binds-the-repo / run-from-target-repo message.
- AC2: `test_pr_url_positional_is_denied` — `/pull/7` (previously allowed) and `/pull/7/files` both fall to the does-not-name-a-PR denial with the marker untouched; `test_branch_name_argument_is_treated_as_naming_no_pr` (branch positional denied, marker intact); the three M72 allows survive in `test_value_flag_allows_survive` (`-m 7`, `--subject "fix issue 9" 7`, `-t 'bump to 9' 7`, each consuming the marker). `grep -rn _PR_URL_TAIL hooks/` → no occurrences; the no-PR denial message prescribes the bare-number spelling (merge_guard.py, read).
- AC3: `CMD_POS` carries the env-assignment prefix run in `cairn_common.py` (one shared pattern; `merge_guard_post.py` keys through the same `GH_PR_MERGE` regex). Tests: `test_gh_repo_env_prefix_is_denied` (marker present — PR-5 command vs PR-7 marker proves ordering — and absent), `test_multi_assignment_and_post_separator_prefixes_are_denied` (`A=1 GH_REPO=…`, `echo hi; GH_REPO=…`), `test_benign_env_prefix_is_guarded_like_the_unprefixed_spelling` (`FOO=1` consumes by rename), `test_env_prefixed_failure_restores_consumed_marker` (PostToolUseFailure restores byte-identical, pending removed), `test_assignment_spelling_in_argument_position_is_ignored` (`echo GH_REPO=x gh pr merge 5` untouched). The GH_REPO denial reuses AC1's message (`assert_repo_denied` checks both limbs).
- AC4: both files read this session. `merge_guard.py` docstring's "Cross-repo limitations (M162; non-exhaustive)" paragraph names compound `cd … && gh pr merge`, subshells, alias/wrapper invocations, GH_HOST, and whitespace/quoted assignment values ("among others"). `skills/shared/tracking-rules.md` "Git and approval model" states an approval binds one repo (marker in the merged repo's own `cairn/`), a secondary repo's merge runs from a session cwd inside that repo, and a repo without cairn tracking is outside the guard (improvised marker inert; chat approval alone, or adopt cairn).
- AC5: fresh runs at review, both exit 0 — `python3 -m unittest discover -s scripts/tests` (324 tests, OK), `python3 -m unittest discover -s hooks/tests` (112 tests, OK; 114 after the fix-now tests below).
- Consistency gate: `cairn_validate` all checks passed; no DESIGN principle changed (impact run skipped); generic profile — toolchain half a clean no-op. No Driving RR — projection-vs-outcome no-ops.
- Fresh-context fan-out (three lenses, distinct evidence): [S] prior-PR-comments — no regression of any archived review finding (M60/M72 checked; PR-comment probe empty, walk skipped), zero findings. [S] blame-history — zero findings: M72 F1–F5 protections preserved, M60 marker lifecycle untouched, D-043/D-107 honored, the guards' un-updated CMD_POS copies confirmed routed to the existing candidate row. [O] diff-bug — all five ACs met as written; 10 ranked residual findings, triaged below.
- F1 (env/quoted/substituted assignment spellings escape the guard entirely, docstring implied only the repo check was missed; `env` unnamed): fix-now — docstring reworded to state those spellings hide the merge entirely and to name `env`-wrapper invocations.
- F2 (`export GH_REPO=o/r && gh pr merge 5` allowed, unnamed in limitations): fix-now — docstring names a prior `export GH_REPO=…` as an unseen redirection; mechanism detection left out (non-exhaustive contract, docs-over-machinery per D-043's boundary stance).
- F3 (`GH_REPO=o/r; gh pr merge 5` false-denied — `\S*` swallowed the separator, breaking CMD_POS's own command-position invariant): fix-now — value run narrowed to `[^\s;&|()]*`; red test `test_separator_terminated_assignment_is_not_a_prefix` confirmed failing before the fix, green after.
- F4 (`GH_REPO= gh pr merge 7` — clearing the variable, the spelling the denial message invites — was denied): fix-now — `_GH_REPO_ASSIGN` requires a value character; red test `test_cleared_gh_repo_prefix_is_guarded_normally` confirmed failing before, green after.
- F5 (tracking-rules bullet attributed URL/branch positionals to the cross-repo denial; they take the no-PR path and a branch positional is not cross-repo): fix-now — bullet reworded to attribute the mechanism correctly.
- F6 (docstring named "subshells" as unseen but `(` is a command separator, so parenthesized subshells ARE seen; the real blind spot is command substitution): fix-now — reworded to "command-substitution subshells (`$(…)`/backticks; parenthesized subshells ARE seen)"; AC4's named item retained and made accurate, no criterion text touched.
- F7 (`#` comments not stripped → `gh pr merge 7 # -R o/r` false-denied): rejected — rare, cosmetic, denies in the safe direction.
- F8a (assert_repo_denied never asserted the pending file absent): fix-now — assertion added to the shared helper, covering every denial case.
- F8b (`assertIn("GH_REPO", reason)` cannot discriminate the two message limbs): rejected — the message is one hard-coded string by design; nothing to discriminate.
- F9 (`gh_merge_gh_repo_prefixed` is a whole-command boolean, not per-occurrence via the shared walk): rejected — denial is whole-command; the prefix is part of `GH_PR_MERGE`'s own per-occurrence match, and AC1's shared-helper clause names the flag predicate, which does share it.
- F10 (the two token walkers order repo-check vs value-flag-skip differently; a future value flag matching `^-[A-Za-z]*R` would diverge): rejected — the ordering in `names_repo_target` is required (`-R`/`--repo` are themselves in the value-flag set; skip-first would never fire), and the divergence is speculative.
- Post-fix runs: hooks 114 OK, scripts 324 OK, skills 528 OK (hand-run; tracking-rules prose touched). Return floor: no finding demonstrates an AC failing and none is a load-bearing deliverable defect — no status return.