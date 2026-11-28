# Roadmap

- Detect drift in scaffold file content: When the `CLAUDE.md` section template changes, a repo that is already set up keeps the old text, since `setup` writes only the pieces that are missing. One repo's section was corrected by hand on 2026-11-27 after a session misread it.
- Add a skill for reviewing others' PRs: `review` reads and tests someone else's PR and reports the findings to the user, and nothing covers posting them as one GitHub review with inline notes.
- Check maintainer roles seen by outsiders: `start` checks that a maintainer agreed to a change before a road in a guest repo, and whether GitHub shows an org member with private membership as a maintainer to a viewer outside the org is unconfirmed.
- [blocked] Support a protected default branch: A trivial edit, the triage commit, a source note, and `setup` commit straight to the default branch, which a repo that requires a PR for every change cannot take. Waits for a repo that uses cairn to turn that requirement on.
- [blocked] Have a second person drive an adoption: Every run of `setup`, and of the work that follows it, has been driven by the plugin's author, which cannot show what someone else would trip on. Waits for a second person to be available to drive one.
