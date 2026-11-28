# M229: The edit-work Sonnet roles move to Haiku 5.5

**Status:** done (2026-10-10, PR #237 https://github.com/jmgirard/cairn/pull/237)

**Goal:** The skills spawn Haiku 5.5 for the edit-work role group, under a decision that supersedes the "Never Haiku" rule. M228's note marks that group `move`, and the user chose it at T1.

**Outcome:** D-151 supersedes D-016's "Never Haiku" blanket and D-110's
clause that it stands. Mechanical migrations, test writing against a spec,
and boilerplate now spawn Haiku 5.5, in tracking-rules "Model and agent
strategy" and `/milestone-implement` step 5, which also says to run
`verify` on a subagent diff before committing it. Explore searches and the
blame-history and prior-PR-comments reviewers stay on Sonnet. M228's
verdicts were mixed (search `stay`, edit work and history review `move`),
so T1 stopped, and the user kept history review on Sonnet. The ROADMAP
candidate narrowed to the two groups that stay. One CHANGELOG entry.

**Decisions:** D-151. One substantive amendment narrowed the title, Goal,
Scope Out, and AC1 to AC3 to the edit-work group. Two fresh readers
re-audited them, and the second AC3 finding was answered, not refixed.

**Review:** one return (the CHANGELOG entry named milestone and decision
ids, which the profile bars). Pass 2 ran three lenses: 18 findings, 13
fixed on the branch (among them D-151's claim that verify catches a weak
test, its unobservable falsifier, and step 5's wording), 5 rejected, none
sent to follow-up. Nothing retired.
