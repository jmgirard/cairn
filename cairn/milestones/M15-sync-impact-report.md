# Milestone 15: Sync Impact Report on principle changes

- **Status:** review   <!-- mirror; cairn/ROADMAP.md is the authority -->
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m15-sync-impact-report · https://github.com/jmgirard/cairn/pull/13

## Goal

When a DESIGN.md principle (IPn/GPn) is added, changed, or retired, report
every `cairn/` file that cites it so downstream references reconcile in the
same change.

## Scope

**In:** A deterministic reporter `scripts/cairn_impact.py` that, given one or
more principle ids (or `--changed`, deriving changed principles from the git
diff of `DESIGN.md`), greps the tracked `cairn/` files (milestone files,
`DECISIONS.md`, `ROADMAP.md`, `DESIGN.md`) for `IPn`/`GPn` tokens and prints
referencing `file:line`. Read-only; reuses the `cairn_scripts` parser (no
duplication); exit 2 outside a cairn repo — matching `cairn_validate` /
`cairn_status` / `cairn_next` (M10). A step in the `/milestone-review`
consistency gate names when to run it (a milestone that touches a principle).
A lock test in `scripts/tests/` with a fixture repo.

**Out:** Impact of `tracking-rules.md` *rule* changes on the plugin's own
skills — that keys on plugin-internal structure, meaningful only in this repo
(the dogfood case), not portably in adopting repos → candidate if wanted.
`--json` output → existing "Scripts --json" candidate.

## Acceptance criteria

- [ ] `scripts/cairn_impact.py IP2 GP4` prints the referencing `cairn/`
      `file:line` for each named principle; exit 0.
- [ ] `--changed` derives the changed principle ids from the working/committed
      diff of `cairn/DESIGN.md` and reports on those.
- [ ] Runs read-only, reuses `cairn_scripts`, exits 2 outside a cairn repo
      (parity with the other reporters).
- [ ] `/milestone-review` consistency gate names when to run it (principle
      touched by the milestone).
- [ ] `scripts/tests/test_scripts.py` covers it with a fixture: a principle
      cited in a milestone file + `DECISIONS.md` is reported at the right
      lines; an uncited principle reports none.
- [ ] Full `scripts/tests/` + `skills/tests/` + `cairn_validate` pass.

## Tasks

- [x] Write `scripts/cairn_impact.py` (principle-id args + `--changed`), on
      the `cairn_scripts` parser and `resolve_root`/`NotCairn` idiom.
- [x] Add fixture + cases to `scripts/tests/test_scripts.py`.
- [x] Add the invoke-when step to `skills/milestone-review/SKILL.md`
      consistency gate.
- [x] Note the reporter in `cairn/DESIGN.md` Architecture (scripts layer).
- [x] Run all test suites + `cairn_validate`.

## Work log
<!-- append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan.
- 2026-07-11: cairn_impact.py written (principle ids + --changed via git diff); 5 fixture cases added, scripts/tests 26 green.
- 2026-07-11: review consistency gate runs cairn_impact --changed on principle-touching milestones; DESIGN Architecture notes the reporter. All suites + validate green.
- 2026-07-11: review fixes — F1 --changed diffs merge-base not HEAD (committed edits now seen), F2/F3 stricter arg parsing, F4-F6 nits. scripts/tests 29 green.

## Decisions
<!-- milestone-local; promote cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- filled by /milestone-review: evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

Evidence (2026-07-11, PR #13):

- **C1 named principles:** `cairn_impact.py IP2 GP4` → exit 0, prints `cairn/…:line` per principle (e.g. IP2 at DESIGN.md:56 + M15 file:33).
- **C2 --changed:** `test_changed_derives_from_design_diff` (real git fixture — commit, edit GP4's line) reports GP4 + its DECISIONS ref, omits unchanged IP2. Also confirmed live during implement.
- **C3 read-only / exit 2:** outside a cairn repo → exit 2, "not a cairn repo"; the reporter only reads.
- **C4 review gate wiring:** `milestone-review` consistency gate runs `cairn_impact --changed` on principle-touching milestones (skip otherwise).
- **C5 fixture coverage:** `TestImpact` (4) + outside-cairn case verify cited-at-right-lines (DESIGN:3/4, milestone:1, DECISIONS:5), absent principle → "no references", usage error → exit 2.
- **C6 suites:** scripts/tests 26 · skills/tests 21 · `cairn_validate` all green.

Consistency gate: `cairn_validate` exit 0; `cairn_impact --changed` → "no changed principles" (M15 touches no principle — the gate's skip path). R gates waived (plugin repo).

Independent fresh-context review (Opus subagent): CHANGES NEEDED → resolved. Triage:
- F1 (major) `--changed` diffed HEAD, so a *committed* branch principle edit (the review-gate state) reported nothing → **fixed**: diff from the merge-base with the default branch (origin/HEAD→main→master, HEAD fallback); added `test_changed_sees_committed_branch_edit` (feature-branch, committed). Satisfies C2's "committed diff".
- F2 (minor) typo'd flag became a "principle" → false all-clear → **fixed**: unknown `-…` options raise usage error (exit 2); `test_unknown_flag_is_usage_error`.
- F3 (minor) `--root` with no value silently used cwd → **fixed**: now a usage error.
- F4 (minor) git-absent read as "no changes" → **fixed**: stderr warning distinguishes it.
- F5 (nit) docstring "Sorted" vs scan-order → **fixed**: reworded to deterministic scan order.
- F6 (nit) no test pinned the whole-word non-match → **fixed**: `test_whole_word_non_match` (IP2 ≠ IP20).
Re-verified: scripts/tests 29 · skills/tests 21 · cairn_validate green.
