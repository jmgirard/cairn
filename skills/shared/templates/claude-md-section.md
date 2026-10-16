<!-- Appended to the repo's CLAUDE.md by /cairn-init. Keep the section, heading included, under 30 lines. -->

## Project tracking (cairn)

This repo uses the cairn plugin. **Before acting on any request, classify it
and route** — the tracking rulebook only loads once a cairn skill fires, so
starting work in plain conversation silently bypasses the work tiers and the
git model. Classify first:

- **Trivial** (no runtime surface — typo, comment, tracking edit): in owner
  mode, commit to the default branch. In guest mode, leave the edit on disk.
- **Look into a GitHub issue**: invoke `/milestone` with the issue number
  or URL.
- **User-visible bug**: invoke `/hotfix`.
- **New work, a design decision, or more than one sitting**: invoke
  `/milestone-plan`. Where a hotfix or trivial route fits, it offers that
  first. Then one question set comes, and the run goes on to the merge
  question. Typed `/milestone-implement` or `/milestone-review` resumes it.
- **Status, "what's next", or unsure which tier**: invoke `/milestone`.
- **Never implement code on the default branch** outside a milestone/hotfix
  branch. Nothing reaches it without the user's explicit approval at the
  merge question, or at the tier chip for a trivial edit.

Whenever the request is anything but trivial, invoke the skill *first* so the
full rulebook (the plugin's `skills/shared/tracking-rules.md`) and its conduct
load — do not reconstruct the rules here from memory. All project state lives under
`cairn/` (**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone
files · Decisions → DECISIONS · Lessons → LESSONS · History → archive +
git**); never record
status or TODOs in this file. Claude's persistent memory never holds project
state; `cairn/` files win any conflict.
