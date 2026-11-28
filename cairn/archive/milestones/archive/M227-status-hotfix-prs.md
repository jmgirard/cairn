# M227: The status report lists open hotfix PRs

**Status:** done (2026-10-09, PR #235 https://github.com/jmgirard/cairn/pull/235)

**Goal:** The `/milestone` health audit reports each open pull request that the operator opened from a `hotfix-*` branch.

**Outcome:** `skills/milestone/SKILL.md` §2 has an "Open hotfix PRs"
bullet, in owner and guest mode. It runs one `gh pr list --repo
<base-repo> --state open --author @me --limit 100` call, keeps the
`hotfix-` heads, and reports each one's number, title, and review
decision (`none` when empty). It carries no §3 disposition and no next
command. A failed read names its cause and is a reported gap. The inbox
bullet no longer says hotfix PRs are "already reported two bullets up",
and the `/hotfix` guest handoff says §2 reports the open PR. CHANGELOG
entry under Unreleased.

**Decisions:** none. At the T4 stop the user dropped the live-look
criterion, because no hotfix PR was open in any repo. The "Live look at
`/milestone`'s "Open hotfix PRs" bullet" candidate row holds it.

**Review:** one return, for a missing CHANGELOG entry. Claim audits: 13
claims with 1 corrected, then 12 changelog claims with 0 corrected. Three
lenses, 11 findings: 2 fixed (the guest handoff's inbox clause), 3 to the
"Live look" row, 6 rejected. Nothing retired.
