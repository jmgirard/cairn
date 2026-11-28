# M162: Multi-repo sessions: the merge guard's cross-repo contract

**Status:** done (2026-08-29, PR #163 https://github.com/jmgirard/cairn/pull/163)

**Goal:** One-session-multi-repo merges stop mis-gating: the guard denies the
cross-repo `gh pr merge` forms its tokenization can see, and the per-repo
approval contract is documented.

**Outcome:** `merge_guard.py` denies repo-targeting flag tokens (`--repo`,
`--repo=`, `-R`, bundled clusters) and leading `GH_REPO=` assignment prefixes
before the marker-existence check, never touching the marker; the PR-URL
positional acceptance is removed (URL/branch positionals fall to the no-PR
denial; the M72 value-flag allows survive); `cairn_common` gains the shared
`gh_merge_occurrence_tokens` helper and `names_repo_target` predicate, and
`CMD_POS` sees through leading `VAR=value` prefixes with a separator-safe
value run. The per-repo contract ("an approval binds one repo") is stated in
tracking-rules and the guard's non-exhaustive limitations docstring.
Env-prefix blindness in the other two guards' `CMD_POS` copies → candidate row.

**Decisions:** none.

**Review:** three-lens fan-out; blame-history and prior-PR lenses zero
findings; diff-bug lens 10 — 7 fixed at the gate (separator-safe value run,
`GH_REPO=` clear-spelling guarded normally, docstring/tracking-rules accuracy,
pending-absent assertion), 3 rejected. Unseen-redirection limitation → Known issues.
