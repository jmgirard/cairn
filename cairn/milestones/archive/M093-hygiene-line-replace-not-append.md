# M93 — Hygiene-line accretion — the ROADMAP stamp is replaced, not appended

**Status:** done · approved 2026-07-19 · PR #92

## Goal
Make `Last hygiene check` a replaced one-line stamp, not a growing chain, and give the density advisory a per-line axis.

## Outcome
The rule now sits in `tracking-rules.md` and at all four surfaces that write the stamp — the July
prune (`dbf1068`) changed one ROADMAP and no skill, scaffold, or guard, which is why it neither
propagated nor held. `record density` gained `NON_ITEM_LINE_CAP = 400` over non-item lines,
item lines excluded by SHAPE. Live-fire WARNs on intraclass (1,870) and circumplex (2,568).

## Decisions
- D-052 narrows M84's per-line rejection to ITEM lines (rationale quoted and kept) and adds
  `ROADMAP.md` to D-045's current-knowledge class, which D-045 had left unenumerated.
- AC6 amended mid-milestone: circumplex's own `review M42` pass (`d396e94a`) rewrote that stamp
  and still left 2,568 chars — the defect demonstrating itself in the field, unprompted.

## Review
One trip, gate green. 3 lenses + scorer: blame-history clean; prior-PR a clean no-op (0 comments
across every merged PR #1–#91, quantifying that standing row); diff-bug 3, all ≥80, all fixed.
F1/85 and F2/92 were vacuous guards proven by live mutation — F2 being M84's own crash-reads-
as-pass defect reproduced in the milestone whose AC5 forbids it. F3/88: D-052 stated one defect
at two ratios, its "all four sites corrected" claim having missed a fifth. No lessons retired.
