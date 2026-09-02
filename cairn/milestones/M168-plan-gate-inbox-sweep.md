# M168: Open GitHub inboxes are swept at the plan gate

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3
- **Resolves:** —
- **Branch/PR:** m168-plan-gate-inbox-sweep

## Goal

`/milestone-plan`'s collision check reads the repo's open GitHub issues and pull requests and, for an item overlapping the goal being planned, offers a `Resolves:` entry or a candidate row at the question gate; everything else stays the health audit's to triage.

## Scope

**Surface tier:** user-facing — the deliverable is plan-skill conduct every adopting repo runs.

**In:**
- `skills/milestone-plan/SKILL.md` step 2's collision check gains the open inboxes as a sweep target: the two read commands, the own-work PR filter, a per-hit rule (issue → `Resolves:` entry or candidate row; PR → candidate row naming `/hotfix` as its door), a count of non-overlapping items reported in the gate's chat, the no-writes rule, and the unreachable-`gh` rule in the audit's form.
- Step 4's `Resolves:` bullet names a gate-accepted inbox hit as a third source that fills the slot.
- README's "Contributions come in through you" bullet gains one sentence stating the plan-gate read.
- Lineage: absorbs the "Inbox read at plan time" candidate row (added 2026-09-02, M167 implement); the row is pruned at post-merge hygiene, never here.

**Out:** dispositions for non-overlapping items → `/milestone` §3 stays the triage surface (M74); a prose guard for the new text → none, by gate choice (the suite gates nothing, D-109); `/milestone` §2's own PR read lacking the `headRefName` field its filter reads → left as shipped, outside this scope; the env-prefix guard alignment weighed at this gate → its standing candidate row; any change to tracking-rules' Intake paragraph → none (M166 filled the slot without one).

## Acceptance criteria

- [ ] AC1: `skills/milestone-plan/SKILL.md` step 2's collision check names the open GitHub inboxes as a sweep target: it carries verbatim the two read commands `gh issue list --state open --json number,title,url` and `gh pr list --state open --json number,title,url,author,headRefName`, the own-work filter (a PR the operator authored, or whose head branch is `m<nnn>-*` or `hotfix-*`, is dropped), and the sentence that the sweep writes nothing to GitHub — verified by reading the shipped text.
- [ ] AC2: The same text states the per-hit rule: an open issue overlapping the goal being planned is posed at the step-3 gate as a `Resolves:` entry (`closes` or `partial`) or as a candidate row; an open PR overlapping it is posed as a candidate row naming `/hotfix` as its door; items with no overlap take no disposition at the plan gate — the text reports their count in the gate's chat and names `/milestone` §3 as where they are triaged — verified by reading the shipped text.
- [ ] AC3: The same text states the unreachable-inbox rule: when `gh` is missing, unauthenticated, or the repo has no remote, the plan names which of the three it was, skips the sweep, and continues planning — verified by reading the shipped text.
- [ ] AC4: Step 4's `Resolves:` bullet lists a gate-accepted step-2 inbox hit among the sources that fill the slot, appended after the existing sources; README's "Contributions come in through you" bullet states in one sentence that the plan gate reads the open inboxes for items overlapping the scope being planned — both verified by reading the shipped text.
- [ ] AC5: The `verify` slot's two suites (`python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`) exit 0 on the branch.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2, T3
- AC5 → T4

## Tasks

- [x] T1: Add an **Inbox sweep** paragraph to step 2's collision check in `skills/milestone-plan/SKILL.md` (after the collision-shape list, before **Checker-regress shape**), mirroring the audit's form at `skills/milestone/SKILL.md:125-147`: both commands verbatim, the own-work filter, the per-hit rule, the non-hit count reported in the gate's chat with `/milestone` §3 named as their triage, the no-writes sentence, and the unreachable-`gh` rule (name which of the three, skip, continue).
- [x] T2: Append the third source to step 4's `Resolves:` bullet after "or an issue the user names" — appended, never rewritten, so `skills/tests/test_issue_linkage.py:76-83` keeps matching.
- [x] T3: Add one sentence to README's "Contributions come in through you" bullet (`README.md:282-290`), written against the shipped T1 text (derived-claims rule).
- [x] T4: Run both gating suites from the repo root with explicit exit codes; hand-run `skills/tests` and confirm `test_issue_linkage.py` stays green; work-log line; status → review.

## Work log

- 2026-09-02: created by /milestone-plan. Criteria audit ran in full mode (fresh [O] reader over two drafts): AC5's hand-run `skills/tests` clause removed (it re-gated a suite D-109 un-gated; moved to T4); AC2's "only triage surface" contradiction reworded to non-hits left for the audit with a reported count; the PR read keeps `headRefName` so the own-work filter is checkable from the same read; the D-108 door read as not applying — the deliverable is intake conduct (how scope is discovered), not a rule about how records are authored, measured, or audited, and M166 shipped the same family after D-108 without superseding it; the absorbed row's promotion condition (an observed missed or duplicated issue) has not fired — planning ahead of it is the user's gate choice.
- 2026-09-02: plan gate chose planning the inbox sweep alone over planning the env-prefix guard alignment beside it because that row's own condition (a live env-prefixed guarded spelling) is unfired and the two share no code; falsified by such a spelling being observed in a live session.
- 2026-09-02: plan gate chose placing the sweep in step 2's collision check over step 1 (the candidate row's proposed home) because overlap with the described goal is judged there; falsified by a plan whose goal settles only after the collision check, so the sweep runs against a stale goal.
- 2026-09-02: plan gate chose no prose guard over a guard file because the suite gates nothing (D-109) and M167 shipped guard-free; falsified by the sweep text drifting unnoticed until an adopter's plan misses an issue the text once caught.
- 2026-09-02: plan gate chose reporting the non-hit count over silence or plan-time triage because a seen item then leaves a trace without duplicating the audit's triage surface; falsified by an adopter's non-hit staying unrowed across repeated plans with no audit run between them.
- 2026-09-02: /milestone-implement started; branch m168-plan-gate-inbox-sweep cut from pushed main. Question gate skipped — the plan fixed placement, both commands, the filter, and both rules. T1: Inbox sweep paragraph inserted between the collision-shape list and Checker-regress shape in skills/milestone-plan/SKILL.md; scripts 329 / hooks 121, both exit 0.
- 2026-09-02: T2: step 4's Resolves bullet gains "or a step-2 inbox hit the gate accepted" after the two existing sources; test_issue_linkage hand-run green; scripts 329 / hooks 121, both exit 0.
- 2026-09-02: T3: README's "Contributions come in through you" bullet gains one sentence naming the plan-time read, written against the T1 paragraph as committed; scripts 329 / hooks 121, both exit 0.
- 2026-09-02: T4: on the final branch content, from the repo root: scripts 329 exit 0, hooks 121 exit 0; skills/tests hand-run 566 OK exit 0 (test_issue_linkage among them). No deviations from plan. Status → review.

## Decisions

## Review
