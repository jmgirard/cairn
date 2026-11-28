# M84 — Record-density advisory — the item caps gain a weight axis

**Status:** done · approved 2026-07-18 · PR #82

## Goal
Give `ROADMAP.md` and `LESSONS.md` a character-mass advisory beside their item caps,
so prose weight accumulating inside single lines stops being invisible to the audit.

## Outcome
`cairn_validate` gained `record density` (WARN, exit-code neutral): character mass
against per-file thresholds `<9,000` / `<17,000`. Both files are parsed one item per line,
so the line cap counts ITEMS and is blind to prose growing inside a line — `LESSONS.md` held
49 lines, one under cap, across M78–M83 while its mass grew 13%. tracking-rules states both
axes, their opposite remedies (count → graduate/prune; weight → compress) and each severity.
`LESSONS.md` pruned by compression: 18,607 → 16,272 chars, 36 lessons into 28, all tags kept.

## Decisions
- M84-D1: thresholds from a two-repo survey — ROADMAP's 60 × 150 sits astride the real
  prune (9,691 pre / 8,001 post); LESSONS takes a 340 mean. Characters, not bytes.

## Review
3 lenses: blame and prior-PR clean; diff-bug found 7. Fixed F2/90 (a vacuous absent-file
test that stayed green while the advisory crashed, proven live by two agents), F4/82
("weight" naming both the failing CHECK and the non-failing advisory), F7/80, and
sub-threshold F5/62, F6/58, F3/50. F1/78 met by recording AC3's table as evidence.
