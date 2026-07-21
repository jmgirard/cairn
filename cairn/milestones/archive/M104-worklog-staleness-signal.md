# M104: Work-log staleness signal — bookkeeping entries no longer reset the idle clock

**Status:** done (2026-07-20, PR #102 https://github.com/jmgirard/cairn/pull/102)

**Goal:** The `/milestone` audit's `in-progress` staleness signal measures the recency of genuine work, so a milestone whose recent work-log lines are only bookkeeping is flagged stale, not read as active.

**Outcome:** The `/milestone` §2 Staleness bullet runs the 14-day `in-progress` clock from the last work-log line recording actual work; bookkeeping (a Depends-on amendment, a status/mirror catch-up, a git-reconciliation catch-up line) is clock-neutral (M88 T3, generalizing M88-D1). Release-shaped milestones are exempt — their idleness owned by the `release window` advisory whether or not it fired (broadened from "already flagged"). Guarded by `test_staleness_signal_discounts_bookkeeping_entries` (three anchors: measurement basis, the enumerated set bound to its disposition on one line, the release exemption) + a second ownership-guard anchor; five mutation registrations. Stayed LLM-owned (`cairn_validate.py:6`); no script change.

**Decisions:** none (the release-shaped exemption is conduct, no D-entry).

**Review:** 4/4 ACs fresh, all PASS. Fan-out (diff-bug [O], blame [S], prior-review [S], scorer [S]): F-A (92) guard missed the enumerated set — fixed, a member swap now reddens; F-C (80) the "every in-progress" bullet collided with the release advisory's deliberate leniency — fixed (ownership broadened, bullet exempts release-shaped). F-B (70) sub-threshold, resolved incidentally by the rewrite. No lesson retired; two captured.
