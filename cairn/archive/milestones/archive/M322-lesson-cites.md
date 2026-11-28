# M322: Stop citing lessons from code and docs

**Status:** done (2026-10-25, PR #335 https://github.com/jmgirard/cairn/pull/335)

**Goal:** Code, tests, skill prose, and `cairn/DESIGN.md` stop pointing readers at `cairn/LESSONS.md` lines, which rank eviction and in-place correction can remove or change.

**Outcome:** About 60 lesson cites ("the M171 lesson", "LESSONS M194", "LESSONS :49", "LESSONS: widening…", one wrapped across two lines) were removed from test comments and docstrings under `scripts/tests`, `hooks/status`, and `skills/tests`, from `scripts/cairn_validate.py` and `hooks/status/register.tsx`, from two parentheticals in the plan and review skills, from `cairn/DESIGN.md`, and from `cairn/references/prompting-opus-5.md`. Each comment states its point in its own words; no lesson cite became a milestone cite. The sweep `{ git grep -niE 'lesson' -- . ':!cairn' ':!CHANGELOG.md'; git grep -niE 'lesson' -- cairn/DESIGN.md; } | grep -E 'M[0-9]{2,3}|LESSONS ?:|LESSONS [0-9]'` went from 73 lines to 16, none a cite. The `cairn/LESSONS.md` header gains one line stating the rule (header 21 lines). DESIGN.md's `/cairn-triage` Known issues entry drops its sentence on line-number cites (`narrowed 2026-10-25 — M322`). The shipped lessons template is unchanged. No CHANGELOG entry: no behavior changed.

**Decisions:** D-222 (code, tests, skill prose, and DESIGN.md do not cite a lesson; a comment states the point or cites a milestone or D-entry whose file records it; annotates D-015 and D-218).

**Review:** Criteria audit at plan (full, 5 findings, all taken). Claim audit: 46 claims, 5 corrected. No returns. Four-lens pass: 20 findings, 14 fixed (vague reason clauses, a kept "M28:" id, the DESIGN.md `minWidth` reason, the squash-merge reason in the review skill, the header cut from two lines to one, a references-page cite), 5 rejected, 1 to the new parked row "Check bare milestone ids in tests". Copilot: one request, no review recorded. Hygiene: candidate row "Cut code cites to evicted lessons" graduated; `used M322` on the seven lessons the plan used; no lesson captured.
