# M226: The pane lists open hotfix PRs

**Status:** done (2026-10-09, PR #234 https://github.com/jmgirard/cairn/pull/234)

**Goal:** The cairn pane lists each open pull request that the operator opened from a `hotfix-*` branch, with its state word and counts.

**Outcome:** `readHotfixes` in `register.tsx` runs inside `readPrs` at
each pane open and Refresh press. It picks the base remote as
`cairn_common.base_remote` does (`collaborationMode` in `reader.ts`).
Then one `gh pr list --repo <url> --state open --author @me --limit 100`
call runs in the band's root. `hotfixPrs` in `pane.ts` keeps `hotfix-` entries
with a URL and an integer number, once each. A failed call keeps the last
list for the same root. The `hotfixes` atom (`hotfixes-1`) holds
`{ root, prs }`, and the hotfix URLs get words and counts with the blocked
ones. `paneLines` draws `HOTFIXES` before the candidates, with no Button,
and the heading's Refresh key is `cairn-pane-refresh-hotfixes`.

**Decisions:** none promoted. The plan chose a live `gh pr list` read over
a record that `/hotfix` writes. The status report change split to M227.

**Review:** one return, for a missing CHANGELOG entry. Claim audit: 60
claims, 6 corrected. Three lenses, 33 findings: 10 fixed (per-write
newest-read check, repeated entries, parity tests), 14 to "Pane hotfix
edges (M226 review)", 6 rejected, 3 no finding. The look in parameters
showed its 5 hotfix PRs. Mod tests went to 1765. Nothing retired.
