# M122: A differential guard holding the hook and the cap counters to one heading contract

**Status:** done (2026-07-30, PR #122 https://github.com/jmgirard/cairn/pull/122)

**Goal:** Pin the session-context hook and the cap counters to one
heading-classification contract so a normalization step dropped on either side reds.

**Outcome:** `TestHeadingNormalizationContract` (`hooks/tests/test_hooks.py`) — a
15-row table measured three ways per row: counters through
`milestone_body_line_count` over a real file, hook through `milestone_part`, and
the row's own expected verdict, which reds a drift hitting both layers alike.
Six silent divergences now fail: hook `.strip()` and `.lower()`, the `## ` prefix
test on both layers, an `lstrip()` added ahead of it, the hook's `~~~` fence
support, and the counters' boundary `.strip()`. No production code changed.

**Decisions:** none promoted. Scope amended at two gates — widened to the fence
axis mid-implement, then the prefix clause review F1 disproved was deleted at the
merge gate. Round-3 §8 certification declined as a logged deviation, not D-069 cover.

**Review:** 3 lenses + scorer; 11 findings, 4 actioned (F1 88, F3 85, F2 80, F5 80),
7 logged below 80. F1/F2 were surviving mutations of the milestone's own failure
mode. `LESSONS.md`'s M113 line trimmed to its uncovered remainder.
