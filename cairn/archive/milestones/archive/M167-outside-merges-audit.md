# M167: Outside merges reach the health audit

**Status:** done (2026-09-02, PR #170 https://github.com/jmgirard/cairn/pull/170)

**Goal:** The `/milestone` health audit lists pull requests merged since the last hygiene stamp by anyone but the operator, shows which archived milestone summaries mention the files each one touched, and carries each to the triage chip for a disposition.

**Outcome:** `/milestone` §2 **Outside merges** bullet — `gh pr list --state
merged --limit 100 --json …` filtered client-side by `mergedAt` on/after the
ROADMAP stamp date (a dateless stamp keeps all) and `mergedBy` ≠ `gh api user`
login; `--limit` raised while the oldest return is newer than the stamp or the
count hits the limit; per kept PR `gh pr diff <N> --name-only` and a
`grep -lF` literal-path hint over `milestones/archive/` (over- and
under-matching both stated); writes nothing; unreachable-`gh` or a failed read
is a reported gap. §3 resolves each item with candidate row / `/hotfix` /
`/milestone-plan` / leave (`close` stays issue-only), the `/hotfix` bullet
now naming a bug an outside merge introduced or undid. README contributions
bullet states the read. nestedtune proof: PR #30 (topepo) kept at 2026-08-01,
none at 2026-09-01; its 13 paths match seven summaries, M17 among them. No
script reads GitHub (D-043); no prose guard (gate choice).

**Decisions:** none.

**Review:** three-lens fan-out; [O] 16 findings, [S] blame 4 (two overlapping),
prior-review none; 7 fixed at the gate (limit-raise soundness, dateless stamp,
per-PR read failure, §3 route list, four/five miscount, hint under-matching, `/hotfix` fit), 13 rejected. Nothing graduated or retired; no lesson added.
