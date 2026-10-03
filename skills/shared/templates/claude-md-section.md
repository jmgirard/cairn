<!-- Appended to the repo's CLAUDE.md by /cairn-init. Keep the section body under ~25 lines. -->

## Project tracking (cairn)

This repo uses the cairn plugin. **Before acting on any request, classify it
and route** — the tracking rulebook only loads once a cairn skill fires, so
starting work in plain conversation silently bypasses the work tiers and the
git model. Classify first:

- **Trivial** (no runtime surface — typo, comment, tracking edit): commit
  directly to the default branch.
- **User-visible bug**: invoke `/hotfix`.
- **New work, a design decision, or more than one sitting**: invoke
  `/milestone-plan`. One question set follows, then the run goes on through
  implement and review to the merge question; typed `/milestone-implement`
  or `/milestone-review` resumes a stopped run.
- **Status, "what's next", or unsure which tier**: invoke `/milestone`.
- **Never implement code on the default branch** outside a milestone/hotfix
  branch; nothing reaches it without the user's explicit approval at the
  merge question, or up front in the plan question set if the plan's promise
  merges unchanged. Back to the merge question on: a goal, scope, or criteria
  change, a declined merge question, missing evidence, an unfixed finding, a
  top-ranked finding rejected as false (any, if user-facing), no spawned
  reviewers, an IP or D-entry change, a review asking for changes, a Fable
  shortfall, guest mode, a companion repo, an issue write, red CI, or a push
  after the PR opens.

Whenever the request is anything but trivial, invoke the skill *first* so the
full rulebook (the plugin's `skills/shared/tracking-rules.md`) and its conduct
load — do not reconstruct the rules here from memory. All project state lives under
`cairn/` (**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone
files · Decisions → DECISIONS · Lessons → LESSONS · History → archive +
git**); never record
status or TODOs in this file. Claude's persistent memory never holds project
state; `cairn/` files win any conflict.
