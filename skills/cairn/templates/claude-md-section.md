## Project tracking (cairn)

This repo uses the cairn plugin. Work goes through its `/cairn` skill:

- **Any request**: `/cairn start`. It handles a trivial edit itself (no
  runtime surface: a typo, a comment, a ROADMAP row), and it plans anything
  else on a branch and takes it to review.
- **Work in flight**: `/cairn resume` picks it up, and `/cairn review` ships it.
- **Status or "what's next"**: `/cairn status`.

Never build on the default branch. Nothing reaches it without the user's
approval at the merge question, or for a trivial edit their request.

Candidates are in `cairn/ROADMAP.md`, and the toolchain commands are in
`cairn/PROFILE.md`. Plans live outside the repo, in the home folder that
`/cairn status` prints. Never record status or TODOs in this file.
