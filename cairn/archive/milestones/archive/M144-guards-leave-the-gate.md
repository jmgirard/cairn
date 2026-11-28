# M144: The prose-guard suites leave the merge gate

**Status:** done (2026-08-16, PR #145 https://github.com/jmgirard/cairn/pull/145)

**Goal:** The prose-guard suite (`skills/tests`) stops gating this repo's
commits, merges, and check-offs — `scripts/tests` and `hooks/tests` keep
gating; guard files retained, hand-runnable — RR13's smallest reversible probe.

**Outcome:** PROFILE.md `verify` names two gating suites, `skills/tests`
explicitly non-gating; `test-doctrine` drops the guard/registration obligation
for new rules here (shipped doctrine still governs adopters). D-108 widens
D-090's door to conduct rules about verification/records (removal carve-out on
D-095's precedent; D-109-firing exception). D-109 records the ungating + exit
falsifier (hygiene-pass cadence). LESSONS trivial-tier line, CLAUDE.md verify
sentence, and DESIGN's enforcement bullet corrected in place.

**Decisions:** none milestone-local; cross-cutting → D-108, D-109.

**Review:** 24 fan-out findings, five actioned ≥80, all fixed on branch:
D-108's precedent overstatement (O1/B1), DESIGN's stale bullet outside the
sweep's patterns (O9), LESSONS misplacing template edits off the gating side
(O11), D-109 importing §8-era figures (B2); 14 sub-80 logged, several riding
to RR13 step 2. No lessons captured or retired.
