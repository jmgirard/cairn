# M166: GitHub issues are linked at plan time and closed at merge

**Status:** done (2026-09-02, PR #169 https://github.com/jmgirard/cairn/pull/169; resolves #168 closes)

**Goal:** A milestone that resolves a GitHub issue names the issue at plan time, carries a closing keyword into its PR so GitHub closes the issue at merge, and confirms the close afterward.

**Outcome:** plan-owned `Resolves:` slot on the milestone template (`#N closes` /
`#N partial`; unparsed by validate — `TestResolvesSlot`), echoed on the archive
status line; `/milestone-plan` fills it, rows a `partial` remainder, offers a
`Queued as M<NNN>` comment at the gate; `/milestone-review` ends the PR body with
`Closes`/`Refs` lines, names post-merge issue writes in the merge chip, reads each
`closes` issue after the merge; `/hotfix` reads a `Fixes #N` issue likewise;
`/milestone` §2 orphan bullet (retained done rows) + §3 `close` disposition; README
bullet; guard `test_issue_linkage.py`; rulebook-mass baseline re-seeded (467/43,454).

**Decisions:** milestone-local — M74's audit "never write to GitHub" narrowed to
its reads; the triage-chip `close` is the one gated audit-path write.

**Review:** three-lens fan-out; blame clean; [O] 12 findings — 8 fixed at the
gate (README derived claims, hotfix chip names its close, AC1 read widened, §3
scope, ack timing, review-path scoping), 4 rejected; prior-review 2 — baseline
re-seed fixed, 1 rejected. Live proof: #168 read CLOSED one second after the
merge; no post-merge write needed. Nothing graduated or retired.
