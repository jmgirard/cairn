# M245: The audit reports new activity on the issues and pull requests that candidate rows link to

**Status:** done (2026-10-11, PR #255 https://github.com/jmgirard/cairn/pull/255)

**Goal:** `/milestone`'s health audit reads each issue or pull request that a candidate row links to in one of three named forms, in owner and guest mode, and reports each close, merge, comment, and review that someone else made after the row's cut-off.

**Outcome:** `/milestone` §2 gains a "Linked items" bullet with one bash/zsh
block. It finds links in the Candidates rows (a GitHub URL, `owner/repo#N`,
or a bare `#N` read as `<base-repo>`), dedupes them, and gives each row a
cut-off: its latest date, a later `checked <UTC time>` mark, or the stamp
date. One `gh api repos/…/issues/<N>` read per item reports a close or merge
unless `closed_by` is the operator. Paginated lists report comments, reviews,
and review-thread comments by others, filtered on creation time. A failed
`gh api user` skips the read. §3 adds "update the row", which writes the
`checked` mark. README and CHANGELOG describe it. Trigger: a performance
guest audit missed the easystats/insight#1263 merge and new comments.

**Decisions:** none promoted. The question set added bare `#N` and PR
reviews; the plan chose a prose bullet (after M167) and a per-row cut-off;
the operator's merge-question decline added the own-merge filter (AC3).

**Review:** two passes after a step-7 decline. Pass 1: 35 findings, 16
fixed, 6 to "Linked-item read edges (M245 review)", 12 rejected. Pass 2:
30 findings, 8 fixed, 4 to that row, 18 rejected. Claim audits read 31 and
6 claims. Copilot did not review (quota limit). Nothing retired.
