# M77: Work-log cap exemption — the budget stops counting a section IP4 forbids editing

**Goal:** exempt the work log from the 150-line plan-owned cap and add an
advisory for wrapped entries, so the cap can never demand a trim to a section
D-045 makes history. PR #75, merged 2026-07-18.

**Outcome:** both cap counters share one fence-aware `_plan_owned_scan`; it
subtracts `## Work log` from the body count and drops it from the
heaviest-first breakdown, so the remedy never names an untrimmable section. New
exit-code-neutral `work-log format` advisory WARNs on a line that is not a
one-line `- ` entry. Rulebook + template name the exempt set and each reason.
M76's 15 entries: 58 lines wrapped, 21 reflowed.

**Decisions:** D-046 (annotates D-030) — exempt the work log; WARN not FAIL, an
unbudgeted wrap being untidiness; `## Decisions` stays counted, so D-030's
rejection stands. Milestone-locally supersedes M69's "work log stays counted":
its premise predates D-045, and IP4 barred adding the citation to D-046.

**Review:** trip 1 FAILED AC4 (6 asserts, 5 entries); the "computed couplings
are exempt" reading was declined as reinterpretation. Trip 2: 6/6 AC, gate
clean, blame + prior-PR no findings; diff-bug 3 + orchestrator 1, all real, all
fixed. F1: the shipped 3-line template comment tripped the new single-line
comment matcher, so every milestone from it emitted 3 spurious WARNs — this
milestone's halves contradicting each other, now paired by a test reading the
real template. F2 closing fence dropped; F3 prose falsified, 4 places; F4 M69.
