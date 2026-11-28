# setup

Sets cairn up in a repo, or converts a repo from cairn v2.

## Steps

1. Detect the case from the status script's listing: no cairn files, a v2 repo, or a v3 repo with pieces missing. For a repo with no cairn files, settle whether it is the user's own or a guest repo, and ask if its owner and history do not make that plain.
2. A new repo of the user's: write `cairn/ROADMAP.md`, `cairn/PROFILE.md` with the repo's own check command under Verify, `cairn/references/INDEX.md`, and the cairn section of `CLAUDE.md`, each from its template. Write no `AGENTS.md`.
3. The user's own repos: show what was written, and propose two GitHub rules on the default branch, no force-push and no deletion. On the user's yes, commit, push, and apply the rules: `gh api repos/<owner>/<repo>/rulesets --method POST --input <the default-branch-rules.json template>`. (stop)
4. Someone else's repo: create its home folder with `ROADMAP.md`, `PROFILE.md`, and `references/INDEX.md`, and commit `~/.cairn`. Write nothing in the checkout, and never change the host's settings. `Maintainer: yes` is the user's to add by hand.
5. A v2 repo: run the migration script with no flag, in the repo's main checkout, and show the user what it would do. On the user's yes, run it with `--apply`. Then fix what the status listing reports as a problem, and what the script lists for the session to look at, until the listing shows no problem lines. In the user's own repos, commit the staged changes to the default branch as one commit and push. In a guest repo, commit `~/.cairn`. (stop)
6. A v2 repo, then or the next time the repo is worked in: show one table for the old Known issues and the candidates. A Known issues entry becomes a proposed GitHub issue only if it has a failing input and points to ordinary use. Otherwise it is dropped. Each candidate is promoted, kept, or dropped, and a kept one that waits on something outside becomes `[blocked]`. Apply the table on the user's yes, and take the Known issues section out of `DESIGN.md`. In a guest repo, open no issue without the user's word. (stop)
7. A v3 repo with pieces missing: write only the missing pieces, and show them.
8. Propose a `Zotero collection:` line for the profile, with the repo's name as the default. The user can decline. Where the repo gains the line, add every shelf file not already in Zotero, at the user's yes. (stop)

## Done

The status listing names the repo as the user's own or a guest repo and shows no problem lines. In the user's own repos the cairn files are committed and pushed. In a guest repo nothing of cairn is in the checkout, and `~/.cairn` is committed.
