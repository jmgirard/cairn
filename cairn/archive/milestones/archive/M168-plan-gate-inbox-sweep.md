# M168: Open GitHub inboxes are swept at the plan gate

**Status:** done (2026-09-02, PR #171 https://github.com/jmgirard/cairn/pull/171)

**Goal:** `/milestone-plan`'s collision check reads the repo's open GitHub issues and pull requests and, for an item overlapping the goal being planned, offers a `Resolves:` entry or a candidate row at the question gate; everything else stays the health audit's to triage.

**Outcome:** `skills/milestone-plan/SKILL.md` step 2 gains an **Inbox sweep**
paragraph in the audit's read form: `gh issue list --state open --json
number,title,url`; `gh pr list --state open --json number,title,url,author,headRefName`;
own-work PRs dropped (`author.login` = `gh api user --jq .login`, or head branch
`m<nnn>-*` / `hotfix-*`); an overlapping issue posed at the step-3 gate as a
`Resolves:` entry (`closes`/`partial`) or candidate row, an overlapping PR as a
candidate row naming `/hotfix` as its door; non-hits counted in the gate's chat
and left to `/milestone` §3; writes nothing to GitHub; unreachable `gh` named,
sweep skipped, planning continues. Step 4's `Resolves:` bullet names a
gate-accepted inbox hit as a third source; README contributions bullet gains one
sentence; no prose guard (D-109); absorbed and pruned the "Inbox read at plan time" row.

**Decisions:** none.

**Review:** three-lens fan-out; [O] 10 findings, [S] blame none, prior-review
none; 2 fixed at the gate (`author.login` / operator-login clause; README
sentence moved after the outside-merges sentence), 8 rejected (AC wording,
recorded plan-gate choices, a `/milestone` §2 gap left as shipped, no `--limit`
on the verbatim commands). Nothing graduated or retired; no lesson.
