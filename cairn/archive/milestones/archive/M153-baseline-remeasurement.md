# M153: The effort-audit baselines are re-measured

**Status:** done (2026-08-22, PR #154 https://github.com/jmgirard/cairn/pull/154)

**Goal:** Re-measure the three 2026-08-08-era baselines (record-defect share,
governance share, cost) over M137–M152, with a verdict on the record rules.

**Outcome:** `references/record-rule-remeasurement.md` + INDEX line: a 106-row
ledger classifying every actioned review finding recovered from the 16
pre-archive `## Review` blobs (record defects 41% scored era / 57% unscored /
51% pooled vs the `08bbb07` "roughly half" baseline; M143 a population zero,
M152 the named unrecoverable gap); governance share 78–89% vs Q2's 73–77%;
cost medians 137 turns / 175,620 output vs 165/169k. Verdict: helping —
record-caused returns zero post-reduction, corrections batch to one entry
per milestone, neither D-099/D-116 exit fires. Page registered in
`TestShippedPageStateLedger` (`ok`).

**Decisions:** none milestone-local. Work log records a records-hygiene §1
violation: the promoted candidate row was pruned at plan (`41affe6`), not at
completion — hygiene had nothing to graduate.

**Review:** three-lens fan-out (diff touched `scripts/tests/`): 18+1 ranked
findings, 15 fixed at the gate (M152 gap cause, batching claim, RR13 quote,
record-prose numbers among them), 3 rejected with logged reasons; shares and
medians reproduced twice, exact; 0 returns. One lesson added; none retired.
