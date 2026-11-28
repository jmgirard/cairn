# M114: Review-loop escape hatches — thrash counted per milestone, falsifying promotion conditions, detector-precision guard doctrine

**Status:** done (2026-07-27, PR #114 https://github.com/jmgirard/cairn/pull/114)

**Goal:** Close the three gaps the intraclass M93 post-mortem exposed — a thrash
rule that resets on re-cuts and counts trips, promotion conditions written as
failure counts, and guard doctrine silent on detector visibility.

**Outcome:** `/milestone-review`'s thrash rule counts returns per milestone in
the work log and fires on a repeated failure shape, triggers (a)/(b) composing;
tracking-rules gains the falsifying-promotion-condition rule (an evidence
class, never a count); guard-doctrine §3 in-test rendering controls, §7
per-cell count plus across-sweep positive with the silent-cell rule, §8's
description-layer certification — all guarded: 19 thrash asserts, 14
lesson-graduation harness entries, 0 blanking survivors, suites 654/280/91.

**Decisions:** D-064 (the three rules), D-065/D-068 (supersede D-064's false
descriptions), D-066 (derived scope; RR criteria carried by reference), D-069/
D-070 (a certification's report is outside its own certified scope — route c).

**Review:** Eight passes, three Fable reviews (RR05–RR07); the doctrine was
byte-stable from pass 1 and every return was description-layer. Pass 8 clean:
two lenses zero findings, F1 (84) fixed by supersession, F2/F3 logged. At
hygiene: captured the work-log style lesson (facts, not characterizations).
