# cairn (plugin repo)

This repo is the cairn plugin: one skill, `skills/cairn/`, whose `SKILL.md`
is the Rulebook and whose `verbs/` hold each verb's steps; the templates
under `skills/cairn/templates/`; and the scripts and hooks under `scripts/`
and `hooks/`. It tracks its own work with cairn, under `cairn/`.

## Changing the skill text

The text stays short only if these hold. They bind a reviewer of a
skill-text change too.

- A change cites a real session where something went wrong, by the date and
  verb of its line in `~/.cairn/log.md`. A gap someone can imagine does not
  count, and a finding that a line could be misread, with no session behind
  it, is dropped.
- A failure that happened once gets a log line and no text change. The
  second occurrence gets the change. Anything that pushed, merged, posted to
  GitHub, tagged, deleted, or wrote in a guest checkout without the user's
  word is fixed the first time.
- The first response is to delete or reword the line that was misread. A new
  line goes in only if no existing line is at fault, and only if it guards
  one of those public or hard-to-undo actions or the user names it as a step
  they want every time.
- A feature goes in only if the user needs it now in a repo being worked in.
  No validator, hook, or new kind of record is added to stop a failure from
  recurring.
- Size is counted in steps and rules. Too long is fixed by removing one,
  never by rewording to fit.
- Write skill text in short declarative sentences, in American English with
  Oxford commas. Rules describe the reader and give no example.
- Shipped text and scripts name no Claude config folder. The home folder is
  `~/.cairn/<owner>/<repo>/`.
- This repo is public. Leave other people's repo names out of anything
  committed here, log lines included.

Scripts get unit tests. Verb text gets none: real work is its test.

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
