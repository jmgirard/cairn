# M202: One question set, then the agent runs the milestone to the merge question

**Status:** done (2026-10-03, PR #209 https://github.com/jmgirard/cairn/pull/209)

**Goal:** After the one question set of the plan, the agent implements and reviews the milestone in the same run. It stops only at a named stop or at the merge question.

**Outcome:** The rulebook's "Question gates and phase closes" names two gates, the plan question set and the merge question, and a closed list of ten stops between them. Inside a run, each phase ends with a Skill-tool call to the next phase. After a merge, review calls implement for the next workable milestone of the same plan. Review finds that milestone from the newest `plan M…` commit subject, in ROADMAP order. The close block ends the run. The question set asks only what the user alone can settle, and its grants go on disk as `question set:` work-log lines. Implement has no question round, and it adds a task for each `review return` line. Review settles each finding itself (reject with a reason, fix now, or follow-up). Its merge question lists every disposition and each criterion amendment, verbatim. README, CHANGELOG, DESIGN, the routing template, and CLAUDE.md describe the run. Typed `/milestone-implement` or `/milestone-review` resumes a stopped run.

**Decisions:** D-144 records the run. It supersedes the three-gate clause, D-124's per-phase handoff, D-067's plan-gate question for an arguable audit finding, and D-110's maintainer triage. It annotates D-003, D-022, and D-050.

**Review:** There was one defect return. AC1's grep over `skills/` hit a negative assert in `test_gate_wording.py`, which repeats the M169 lesson. Pass 2 ran three lenses with 24 findings. Of those, 16 were fixed on the branch, 4 went to the "Run edge cases" candidate row, and 4 were rejected as planned changes. AC5 was amended once at implement. No lesson was retired or graduated.
