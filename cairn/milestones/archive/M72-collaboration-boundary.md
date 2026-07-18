# M72: Collaboration boundary — what survives a merge outside cairn, plus PR-bound approval

**Status:** done · 2026-07-18 · PR https://github.com/jmgirard/cairn/pull/70

**Goal:** State which parts of the approval model survive a merge made outside
a cairn session, and bind the approval marker to the PR it authorizes.

**Outcome:** tracking-rules gained an enforcement-boundary passage — guards are
hooks on this session's own calls, so a GitHub-UI merge, merge queue, or
unplugged contributor bypasses `merge_guard`/`force_push_guard` and IP1 degrades
to honor-system — plus a plain-words README "Working with collaborators"
section. `merge_guard` now reads the marker body, denying a merge naming a
different PR or none, across every `gh pr merge` in a chain, without consuming
the marker. Closes RR01 §10 rec 4; first live-fire on its own merge.

**Decisions:** D-043 (one operator + outside contributions; boundary over
machinery; intake gets a door, not a tenth skill). Milestone-local: deny-on-
unnamed runs before the marker is read, so a pre-convention marker authorizes a
numbered merge but never a bare one. AC3/AC4 amended at the implement gate.

**Review:** 7/7 verified; suites 246/96/72; `cairn_validate` 15/15. F4 (82)
actioned — only the first merge in a chain was checked, so a second rode through
on the first's approval; fixed by per-occurrence parsing. F1/F2/F5 fixed at the
gate on user direction (marker regex anchored on `for PR #<N>`; `--repo`/`-R`
added, `-m` removed). F3/F6/F7 logged. Follow-ons: M73, M74.
