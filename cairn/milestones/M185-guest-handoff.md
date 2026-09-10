# M185: Guest collaboration mode — fork-aware remotes and review handoff

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M184   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP1, GP2   <!-- owner: plan · create/amend-via-gate; IP1 worked under, unchanged -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate -->
- **Surface tier:** user-facing — the PR flow adopters run from a fork   <!-- owner: plan -->
- **Branch/PR:** m185-guest-handoff   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create -->

In guest mode the branch is cut from and the PR targets the upstream repo, and review ends by handing the PR to the maintainers, the milestone reaching `done` once they merge.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a base remote — in guest mode `upstream` when that remote exists, else `origin`; owner mode always `origin` — read by `cairn_common.default_branch`, by the rulebook's detection recipe, and by every skill site that restates it. Skills spell `--repo <base>` on `gh pr create`, `view`, `checks`, and `ready` in guest mode; cairn never merges in guest mode (the one-repo approval binding stands; an operator with rights merges in the GitHub UI). `/milestone-implement` cuts from `<base>/<default>` and syncs by rebase. `/milestone-review` step 7 in guest mode is an approval gate in the merge gate's shape: hand the PR to the maintainers (recommended), decline present; step 8 runs `gh pr ready` only on selection, sets status `blocked` with a work-log line naming the maintainers as the blocker, and closes with the CI line; step 9 hygiene runs on disk with no commit or push. `/milestone` §2 routes a `blocked` milestone by its PR state: MERGED → hygiene via `/milestone-review`; CLOSED unmerged → a chip (dropped or back to `in-progress`); OPEN with `CHANGES_REQUESTED` → `/milestone-implement`; OPEN otherwise → report the fresh state, stay `blocked`. `/hotfix`'s merge step takes the same handoff. The r-package profile states that in guest mode the `check()` NOTE for the non-standard `cairn` directory is justified by the mode.

**Out:** a new status value for the handed-off state → not needed, `blocked` covers it (plan gate 2026-09-10). Merging via cairn in guest mode → rejected at the plan gate; revisit only with a guard extension binding the marker to the base repo. `gh repo set-default` → rejected (routes a bare merge past the one-repo binding). Adopting a third party's PR into a guest repo → M184 Scope Out. A fork's own push-triggered workflows → left as the fork has them; the maintainers' CI on the PR is the check that counts. Running `check()` in a throwaway worktree → rejected at the plan gate in favour of the justified NOTE.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: On a guest-mode fixture with both an `upstream` and an `origin` remote whose HEAD branches differ, `cairn_common.default_branch(root)` returns upstream's HEAD branch name and `cairn_common.base_remote(root)` returns `"upstream"`; on a guest fixture with `origin` alone, and on an owner fixture that has an `upstream` remote, `base_remote(root)` returns `"origin"` and `default_branch(root)` returns origin's HEAD branch name; every existing `default_branch` test stays green.
- [ ] AC2: T2's site list is read line by line and each site either names the base remote, describes a push of the operator's own branch to the fork, or is recorded in the work log as owner-mode-only naming the skill that stops in guest mode; `grep -rni "origin" skills/*/SKILL.md skills/shared/` is then run and every hit outside that list takes the same three-way disposition; the rulebook's detection recipe names the base remote and states the guest rule (`upstream` when present).
- [ ] AC3: `skills/milestone-review/SKILL.md` states the guest arm: step 1 fetches the default branch from `<base>` and never pushes it; step 2 pushes the branch to `origin` (the fork) and opens the PR with `gh pr create --repo <base> --head <fork-owner>:<branch> --draft`; step 7's chip is an approval gate with handoff recommended and decline present and no merge option; step 8 runs `gh pr ready --repo <base>` only on selection, sets `blocked`, writes the work-log line, and closes with the CI line; step 9 hygiene writes to disk and commits nothing. `skills/shared/tracking-rules.md`'s transition line adds `blocked → done` as legal for a guest-mode handoff whose PR the maintainers merged. Verified by reading each passage.
- [ ] AC4: `skills/milestone/SKILL.md` §2 states the four routes for a `blocked` milestone whose header names a PR, keyed on `gh pr view <N> --repo <base> --json state,reviewDecision`: MERGED, CLOSED, OPEN with `CHANGES_REQUESTED`, OPEN otherwise; verified by reading the passage.
- [ ] AC5: `skills/milestone-implement/SKILL.md` step 2 in guest mode fetches the default branch from `<base>` and never pushes it, cuts the branch from `<base>/<default-branch>`, and syncs a moved default branch by `git rebase <base>/<default-branch>`; `skills/hotfix/SKILL.md`'s merge step names the guest handoff; `skills/shared/profiles/r-package.md`'s consistency-gate names the justified NOTE; verified by reading each passage.
- [ ] AC6: `CHANGELOG.md` carries an entry under the dev heading naming the base remote and the handoff; the `verify` slot's two suites exit 0 from the repo root, each exit code checked, with no new test skipped.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2
- AC3 → T3, T4
- AC4 → T5
- AC5 → T6
- AC6 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: `hooks/cairn_common.py`: `base_remote(cwd)` — `upstream` when `collaboration_mode(root) == "guest"` and `git remote` lists it, else `origin`; `default_branch` (`:277-292`) resolves `refs/remotes/<base>/HEAD`, falling back to `git ls-remote --symref <base> HEAD`; tests beside `test_default_branch_resolved_via_remote_head` (hooks/tests/test_hooks.py:1749, :1510).
- [x] T2: rulebook recipe (`tracking-rules.md:220-223`) and the sites `cairn-init:83-86`, `milestone-implement:41-44`, `milestone-review:70,426`, `cairn-release:32,103-104`, `cairn-triage:30`, `profiles/generic.md:46` → base remote, or a work-log owner-mode-only disposition (release and triage stop in guest mode); then AC2's repo-wide grep for hits outside the list.
- [x] T3: `/milestone-review` guest arm, steps 1–2 (fetch-only sync; fork push + cross-repo `gh pr create`), steps 7–8: the handoff gate chip (`:384-388`) and the handoff sequence in place of the marker + merge (`:395-423`). (RB tripwire: ip-touching — IP1 is worked under unchanged: the handoff merges nothing, and the chip is an approval gate in the merge gate's shape.)
- [x] T4: `/milestone-review` guest arm, steps 9–10: on-disk hygiene (`:425-503`) and the close block (`:505-526`); `--repo <base>` on the `gh pr checks`/`view` reads; the transition line's `blocked → done` guest clause (`tracking-rules.md:171-172`).
- [ ] T5: `/milestone` §2 blocked-with-PR routes (`skills/milestone/SKILL.md:133-141`).
- [ ] T6: `/milestone-implement` step 2 base-remote cut and rebase sync (`:38-49`); `/hotfix` merge step handoff (`:179-204`); `r-package.md` consistency-gate NOTE clause (`:31-32`).
- [ ] T7: CHANGELOG entry; run both suites from the repo root, exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-09-10: created by /milestone-plan; criteria audit ran in full mode via a fresh [O] reader (shared with M184: 24 findings, 20 fixed, 4 gated; a second fresh [O] read returned 14, all fixed before the commit).
- 2026-09-10: plan gate chose reusing `blocked` for the handed-off state over a new `awaiting-upstream` status because the definition already fits and the vocabulary is pinned in five places; falsified by a ROADMAP where blocked-on-maintainers and blocked-on-something-else rows cannot be told apart from their work-log lines.
- 2026-09-10: plan gate chose never merging via cairn in guest mode (skills spell `--repo <base>`) over a guard extension because `gh repo set-default` would route a bare `gh pr merge` past the one-repo approval binding; falsified by an operator with write rights who needs cairn's post-merge hygiene to run in the same session as the merge.
- 2026-09-10: plan gate chose justifying the `check()` NOTE for the `cairn` directory over a throwaway-worktree check because the maintainers' CI on the PR branch is the check that counts; falsified by an upstream whose contribution checklist requires a zero-NOTE local check.
- 2026-09-10: /milestone-implement started on branch `m185-guest-handoff`; question gate: T3's handoff chip built as planned (escalation offered on the ip-touching tag, declined); `<base>` resolves to an `OWNER/REPO` slug via `gh repo view "$(git remote get-url <base>)" --json nameWithOwner -q .nameWithOwner` (fork owner from `origin` the same way, `--json owner -q .owner.login`), the recipe stated once in the rulebook; the CHANGELOG's guest-mode entry is extended rather than a second entry added.
- 2026-09-10: T1 done — `base_remote(cwd)` added and `default_branch` reads `refs/remotes/<base>/HEAD` with the `ls-remote` fallback on `<base>`; five tests in `TestBaseRemote` (both-remotes guest, ls-remote fallback, origin-alone guest, owner-with-upstream, no remote), shown red before the change (1 failure, 4 errors) and green after; hooks 146 green, scripts green.
- 2026-09-10: T2 done — site dispositions: `tracking-rules.md` recipe → names `<base>` and the guest rule plus the `<base-repo>`/`<fork-owner>` slug recipe; `cairn-init` default-branch bullet → `<base>`; `milestone-implement` step 2 → `<base>` cut, guest arm (fetch-only sync, `<slug>` from `<base>/<default-branch>`, rebase + `--force-with-lease` push of the operator's own fork branch) written here rather than in T6; `milestone-review:70` → T3, `:426` → T4; `cairn-release:37,108-109` owner-mode-only (`/cairn-release` stops in guest mode); `cairn-triage:36` owner-mode-only (`/cairn-triage` stops); `profiles/generic.md:46` owner-mode-only (release-walk slot, `/cairn-release` stops). Repo-wide grep hits outside the list: `cairn-triage:93-95,209-216`, `milestone-plan:324`, `records-hygiene:34` — the word "origin"/"original" as provenance, not a remote; no edit.
- 2026-09-10: T3 done — `/milestone-review` session start accepts `blocked` with a header PR in guest mode and puts `--repo <base-repo>` on every `gh pr` read; step 1 fetches from `<base>` and rebases, never pushes the default branch; step 2 pushes to the fork and opens the PR with `gh pr create --repo <base-repo> --head <fork-owner>:<slug> --draft`; step 7's guest chip hands off or declines, no merge option, approval line `step-7 approval: PR #<N> approved for handoff` (resume route's prefix kept); step 8's guest sequence runs `gh pr ready` on selection only, sets `blocked` with the line `blocked: PR #<N> awaits the maintainers of <base-repo>`, commits nothing, closes with the CI line and `/milestone` as the next command.
- 2026-09-10: T4 done — step 9 guest arm: fetch `<base>`, ff-only merge of `<base>/<default-branch>`, every write on disk, no docs-only commit or push, close-if-open skipped (the `Closes` keyword closes at the maintainers' merge), `partial` comments posted with `--repo`; step 10 reads "after its on-disk pass"; `--repo <base-repo>` on every `gh pr` read is stated once at session start (step 8's owner-mode `gh pr checks` wait is replaced whole by the guest sequence); rulebook transition line gains `blocked → done` for a merged guest handoff; the "Collaboration mode" bullet that pointed at M185 is replaced by two bullets stating the base remote and the never-merge handoff.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->
