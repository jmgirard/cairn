# M188: Companion-repo merges from one session — the guard reads the `cd` target, and review merges the companions

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** user-facing — a shipped hook and a review-skill step every adopter runs
- **Branch/PR:** m188-companion-repo-merges

## Goal

A session sitting in one cairn repo merges a PR in a companion checkout by spelling `cd <path> && gh pr merge <N>`, the guard resolving the target from that path — stepping aside when the target has no cairn tracking and gating on the target's own marker when it does — so no turn-boundary directory move and no terminal merge is needed, and `/milestone-review` merges the companions a milestone lists before its primary.

## Scope

**In:** `hooks/cairn_common.py` gains a cd-target resolver; `hooks/merge_guard.py` and `hooks/merge_guard_post.py` key the marker lifecycle on the resolved target; the M163 denial narrows to the spellings the resolver refuses; the docstring, the tracking-rules approval bullet, and the two LESSONS lines stating the old rule (M163, M170) are corrected in place; `/milestone-implement` records companion branches in the `Branch/PR:` slot; `/milestone-review` step 7's chip names them and step 8 pushes, opens, waits on, and merges each before the primary.

**Out:** the `--repo`/`-R`/`GH_REPO=` merge spellings stay denied (a slug names no local checkout; the `cd` spelling covers every case the skills produce) — no row, by the gate. A `/hotfix` companion arm → candidate row (this plan). The desktop app's turn-boundary directory move is harness-owned (M163 F1) and untouched. A nested or stale non-cairn clone of the session repo under the `cd` target merges the session repo's PR ungated, and a session cwd outside every cairn repo still returns before the target is read — both documented limitations in the docstring, not compared or hardened. `pushd`, `cd;`, subshells, and the other redirections the M162/M163 docstring lists stay unseen.

## Acceptance criteria

- [ ] AC1: From a hook cwd inside a cairn-tracked repo, the Bash command `cd <P> && gh pr merge <N> --squash --delete-branch`, where `<P>` is an absolute path to an existing directory with no `cairn/ROADMAP.md` in it or any ancestor, is allowed by `merge_guard.py` (it emits no `permissionDecision`), and the session repo's `cairn/.merge-approved` is left byte-identical and not renamed; `cd <P> && gh pr merge <N> --repo o/r` and a `GH_REPO=o/r` prefix on the merge are still denied with the M162 text. `hooks/tests/test_hooks.py` holds the three tests.
- [ ] AC2: The same command where `<P>` holds `cairn/ROADMAP.md`: allowed, with `<P>/cairn/.merge-approved` renamed to `<P>/cairn/.merge-approved.pending`, when that marker names `PR #<N>`; denied, naming `<P>`, when that marker is absent, names another PR, or names no PR (no legacy fallback across repos); the session repo's own marker is left byte-identical and not renamed in all four cases. `hooks/tests/test_hooks.py` holds one test per case plus the session-marker assertion.
- [ ] AC3: After an AC2-allowed call, `merge_guard_post.py` resolves the pending file in `<P>`: on PostToolUseFailure `<P>/cairn/.merge-approved.pending` is renamed back to `<P>/cairn/.merge-approved`; on PostToolUse it is deleted; a stale `cairn/.merge-approved.pending` in the session repo is untouched in both events. `hooks/tests/test_hooks.py` holds both tests, each run from a session cwd whose repo holds the stale pending file.
- [ ] AC4: The guard accepts only these target forms — one command-position `cd` whose single following token is an absolute path, a `~`-prefixed path, or a path relative to the hook cwd, bare or in single or double quotes, naming an existing directory, joined to the merge by `&&` alone — and every other `cd` spelling before a merge is refused with a rewritten message naming the accepted forms: a target containing `$`, a backtick, `*`, or `?`; a bare `cd`; `cd -`; a second token before the `&&`; a joiner of `;`, `||`, or `|`; a `cd` inside a parenthesized subshell; more than one command-position `cd` before the merge; a target that is not an existing directory. `hooks/tests/test_hooks.py` holds one test per accepted form (three path kinds, plus single- and double-quoted spellings: five) and one per refused form (ten), each refusal pinning one phrase of the message.
- [ ] AC5: When `<P>` resolves to the hook cwd's own cairn root, the call takes the plain-spelling path (marker checked and consumed at that root); `test_denies_same_repo_cd_compound_with_respell_guidance` (`hooks/tests/test_hooks.py:1189`) is replaced by an allow test. The `merge_guard.py` M163 cd paragraph, the tracking-rules approval bullet's "runs from a session cwd inside that repo" sentence, and the M163 and M170 LESSONS sentences stating the old rule are replaced (not supplemented) by the cd-target rule, marked `corrected M188` where LESSONS convention applies.
- [ ] AC6: `/milestone-implement` step 3 records each companion checkout the milestone works in as a `companion: <abs-path> <branch>` entry of the `Branch/PR:` slot (grammar defined in `templates/milestone.md` and the tracking-rules ownership table); `/milestone-review` step 7's approval chip names every companion branch beside the primary, and step 8, on approval, for each companion in listed order and before the primary: pushes the branch, opens its PR from `cd <abs-path> &&`, waits on its checks per the tracking-rules wait rule, writes `<abs-path>/cairn/.merge-approved` in a separate step only when `<abs-path>` has a cairn root, and merges with `cd <abs-path> && gh pr merge <N> --squash --delete-branch`; a companion failure or CI-ceiling stop ends the step before the primary with the timeout close block, and the Session-start resume route re-reads each companion PR's state from `gh pr view` in that checkout. The arm is absent in guest mode. Verified by reading the three skill sites and the template.
- [ ] AC7: Both gating suites green from the repo root, exit codes checked individually: `python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests`.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T3
- AC4 → T1
- AC5 → T2, T4
- AC6 → T5
- AC7 → T6

## Tasks

- [x] T1: Tests first for AC4's fifteen forms, then `cairn_common.cd_target(command, cwd)`: returns the resolved absolute target for an accepted spelling, `None` otherwise (`hooks/cairn_common.py:47` is the predicate it replaces).
- [x] T2: `merge_guard.py`: on a `cd` before a merge, `cd_target` → `None` → the rewritten refusal; a target with no cairn root → return after the M162 checks; a target with one → the marker checks and consumption against that root (refactor the marker block to take a root; deny a marker naming no PR when the root is not the cwd's). Tests for AC1, AC2, AC5's allow test.
- [x] T3: `merge_guard_post.py` resolves pending in the target root via the same helper; AC3 tests.
- [x] T4: Docstring, tracking-rules approval bullet, LESSONS lines (M163 at `cairn/LESSONS.md:84`, M170 at `:87`) corrected in place.
- [x] T5: `templates/milestone.md` `Branch/PR:` comment and tracking-rules ownership row gain the `companion:` grammar; `/milestone-implement` step 3 records it; `/milestone-review` step 7 chip and step 8 companion arm (companions first; guest arm excluded; resume route reads companions).
- [x] T6: Run both gating suites from the repo root; hand-run `skills/tests` and report the pre-existing red set unchanged (D-109).

## Work log

- 2026-09-27: created by /milestone-plan. Origin: the operator's hitop/hitop-form/hitop-builder sessions need a "continue" for the directory move and a terminal merge for companion PRs (hitop M116 review, hitop LESSONS 2026-09-23). Extends M162/M163, which set the cwd-resolved denial; not the checker-regress shape (a guard on actions, not a checker over artifacts).
- 2026-09-27: criteria audit ran in full mode ([O] reader): 13 findings — 7 fixed (existing-directory and `&&`-only target, M162 checks kept on the cd form, byte-identical wording, session pending file untouched, refusal message rewritten, old rule text replaced not supplemented, /hotfix dropped from the arm), 3 settled at plan (nested/stale clone and outside-cairn cwd documented not hardened; no-PR marker denied cross-repo; hand-run prose guard dropped), 2 posed at the gate (merge order; hotfix arm's home), 1 absorbed (AC6 states order and resume).
- 2026-09-27: plan gate chose companions-merge-first over primary-first because a companion failure then stops before the primary lands, so the package never ships ahead of the page it documents; falsified by a companion whose merge must follow the primary (a page reading a just-released package version).
- 2026-09-27: plan chose resolving the `cd` target in the guard over asking the harness for a mid-turn cwd move because the move is harness-owned (M163 F1 declined); falsified by the directory-change tool applying mid-turn, which would make the target read unnecessary.
- 2026-09-27: implement started on `m188-companion-repo-merges`; question gate skipped — the plan fixes the helper name, the `companion:` grammar, and the merge order, nothing open.
- 2026-09-27: T1–T3 done in one checkpoint — `cairn_common.cd_target` (one `cd`, one merge, `&&` joiner, existing dir, no `$`/backtick/glob, no subshell), merge_guard resolves the root from it (untracked → step aside after the M162 checks; tracked → that root's marker, a no-PR marker denied cross-repo), merge_guard_post resolves pending in the target root; the same-repo denial test inverted; hooks 170 green, scripts 391 green. Deviation: four old test assertions were swapped by a `python3 -` script rather than the Edit tool (tracking-rules file-edit rule); verified by grep afterwards.
- 2026-09-27: T4–T6 done — guard docstring's cd paragraph and target-read limitations rewritten; tracking-rules approval bullet and ownership row, LESSONS M163/M170 lines corrected in place (`corrected M188`); template `Branch/PR:` comment carries the `companion:` grammar; implement step 2 records companions; review step 7 chip names them, step 8 companion arm (companions first, untracked → chip alone, tracked → own marker, stop before the primary on failure), resume route re-reads companion PRs. skills/tests hand-run: first pass added one red (`test_owner_parity`, the ownership cell's `;` cut the owner list) — cell respelled with a comma; now the same 4 reds + 1 error as M187. scripts 391, hooks 170 green; tracking-rules 576 lines / 55,110 bytes.
- 2026-09-27: claim audit: 27 claims read, 5 corrected — hooks/cairn_common.py (a quoted `~` was expanded by the guard but not by the shell: expansion now only unquoted, test `test_quoted_tilde_is_a_literal_directory_not_home` added, hooks 171), hooks/merge_guard.py (denial text), hooks/merge_guard_post.py (comment), skills/shared/tracking-rules.md (untracked target is outside the marker gate, not the guard); same-reader re-read: 6 re-read, 0 incorrect.
- 2026-09-27: all tasks done; status → review. scripts 391, hooks 171 green; skills/tests 4 reds + 1 error, the M187 set (D-109).
- 2026-09-27: plan chose the `cd <path>` spelling over a slug-to-checkout map for `--repo` because every skill-produced merge has a local checkout; falsified by a session needing to merge a repo it holds no checkout of.

## Decisions

## Review
