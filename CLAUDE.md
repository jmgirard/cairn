# cairn (plugin repo)

This repo IS the cairn plugin (skills/, templates, rulebook) and dogfoods
its own tracking format by hand under `cairn/`. Its toolchain profile is
`claude-plugin` (declared in `cairn/PROFILE.md`, since M215). `verify` is this
repo's two gating `python3 -m unittest` suites (`scripts/tests`,
`hooks/tests`) plus `claude plugin validate` on the plugin manifest and
`claude plugin test` for the status mod (D-143), and `claude plugin validate`
on the marketplace manifest (M215). The `skills/tests`
prose-guards are hand-run only (M144, D-109).

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
