# M82: Scaffold-deprecation migration — repair mode acts on the advisory it inherits

**Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/80

**Goal.** Give `/cairn-init` repair its own section plus a step that performs
the scaffold rename the `scaffold deprecations` advisory names, so an adopting
repo stops carrying that WARN until a maintainer acts by hand.

**Outcome.** `## 3. Repair` in `skills/cairn-init/SKILL.md`; §0's repair bullet
reduced to a pointer. The step is driven by the advisory's own output, so a
future `DEPRECATED_GITIGNORE` entry needs no skill edit. The gitignored shelf
stays covered throughout: the successor `.gitignore` entry is added first and
the superseded one dropped only once the old directory is gone; three exclusive
on-disk cases are evaluated before anything moves, clobber check first; the
move is gated on an explicit ask. 13 prose-guards, 9 mutation-registered.

**Decisions.** Repair lands as `§3` — inserting it earlier would renumber an
identifier cited from `migration-protocol.md` and two test docstrings. AC4/AC5
amended at the implement gate: the closing step reports the directory outcome
separately, not as a verified migration the named check cannot observe.

**Review.** Trip 2 PASSED; trip 1 failed AC4 (clobber unreachable) and AC5
(false verified-outcome claim). Fan-out: diff-bug 1, blame 0, prior-PR 0. F1
(85) — adding the successor entry silences the advisory, so a declined move is
never re-offered — became a candidate row.
