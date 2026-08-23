# M64: Durable-record preview — verbatim in-chat preview before docs-only commits

- **Status:** done (2026-07-16) · PR: https://github.com/jmgirard/cairn/pull/62
- **Priority:** high · **Principles touched:** GP4

**Goal:** every newly authored durable record (D-entry, plan-owned milestone
sections, LESSONS line, archive summary, ROADMAP candidate/graduation row)
is shown verbatim in chat before the docs-only commit that lands it.

**Outcome:** "Durable-record preview" rule in tracking-rules Output &
interaction discipline + carve-out in "Deltas, not dumps"; one-line
directives at the four gap skills' commit steps (plan step 6, review
post-merge hygiene, implement decisions/amendments, brief RR ingestion);
guard file (8 tests) + 10 mutation-registry entries. Origin: D-035's
rationale reached main sight-unseen (user-flagged, 2026-07-16); design in
D-036 (show-then-commit, four skills, per-skill wired).

**Review:** all 5 ACs on fresh command evidence; fan-out F1 (93, test-count
error in evidence) fixed; F2 (70, exemption scoping vs D-036) fixed at user
direction at the gate; M59 reflow trap hit live (review directive wrapped
mid-name) and fixed on branch.
