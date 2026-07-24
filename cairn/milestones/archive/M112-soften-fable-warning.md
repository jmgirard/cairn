# M112: Soften the Fable warning — neutral token-cost framing, lower recommend bar, gate retained

**Status:** done (2026-07-24, PR #112 https://github.com/jmgirard/cairn/pull/112)

**Goal:** Rewrite cairn's anti-Fable framing from a billing-hazard warning into neutral token-cost guidance — Fable is no longer pay-on-demand — while keeping the per-instance RB/RR approval gate and lowering the bar for recommending it.

**Outcome:** Billing-hazard phrasing ("token-billed", "pay-per-use", "no standing authorization", "never a silent cost", "costs real money", "paid escalation") removed from tracking-rules.md, milestone-brief, milestone-implement, and README, replaced by "no longer pay-on-demand but typically uses more tokens than Opus". The RB-tripwire rule + milestone-implement now offer escalation on a tripwire hit OR a genuinely hard question (three tripwires stay must-offer). New guard `test_fable_gate_retained.py` pins the retained per-instance approval gate + RB/RR-only path; 6 blocks registered in the mutation harness.

**Decisions:** D-062 (promoted) — supersedes D-004's per-call-billing premise; gate retained on token-cost grounds, recommend bar lowered; D-004 left unedited (IP4).

**Review:** Three-lens fan-out, zero defects. Blame-history lens flagged README L201/L259 still on old framing → folded in via gated scope amendment (T6, AC1). No findings scored; no lesson retired (guard is new coverage).
