# M168: Open GitHub inboxes are swept at the plan gate

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3
- **Resolves:** —
- **Branch/PR:** m168-plan-gate-inbox-sweep · https://github.com/jmgirard/cairn/pull/171

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

- [x] AC1: `skills/milestone-plan/SKILL.md` step 2's collision check names the open GitHub inboxes as a sweep target: it carries verbatim the two read commands `gh issue list --state open --json number,title,url` and `gh pr list --state open --json number,title,url,author,headRefName`, the own-work filter (a PR the operator authored, or whose head branch is `m<nnn>-*` or `hotfix-*`, is dropped), and the sentence that the sweep writes nothing to GitHub — verified by reading the shipped text.
- [x] AC2: The same text states the per-hit rule: an open issue overlapping the goal being planned is posed at the step-3 gate as a `Resolves:` entry (`closes` or `partial`) or as a candidate row; an open PR overlapping it is posed as a candidate row naming `/hotfix` as its door; items with no overlap take no disposition at the plan gate — the text reports their count in the gate's chat and names `/milestone` §3 as where they are triaged — verified by reading the shipped text.
- [x] AC3: The same text states the unreachable-inbox rule: when `gh` is missing, unauthenticated, or the repo has no remote, the plan names which of the three it was, skips the sweep, and continues planning — verified by reading the shipped text.
- [x] AC4: Step 4's `Resolves:` bullet lists a gate-accepted step-2 inbox hit among the sources that fill the slot, appended after the existing sources; README's "Contributions come in through you" bullet states in one sentence that the plan gate reads the open inboxes for items overlapping the scope being planned — both verified by reading the shipped text.
- [x] AC5: The `verify` slot's two suites (`python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`) exit 0 on the branch.

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

- 2026-09-02: /milestone-review started. main unmoved since the branch was cut; branch pushed; draft PR #171 opened.

## Review

- 2026-09-02 evidence, on the branch head (`git diff main..HEAD` read this session):
  - AC1: `skills/milestone-plan/SKILL.md` step 2's new **Inbox sweep** paragraph carries both commands verbatim (`gh issue list --state open --json number,title,url`; `gh pr list --state open --json number,title,url,author,headRefName`), the own-work filter (operator-authored PR, or head branch `m<nnn>-*` / `hotfix-*`, dropped), and "The sweep writes nothing to GitHub — no labels, comments, or closes." Pass.
  - AC2: same paragraph: issue hit → `Resolves:` entry (`closes` or `partial`) or candidate row at the step-3 gate; PR hit → candidate row naming `/hotfix` as its door; non-hits take no disposition, "report their count in the gate's chat; `/milestone` §3 is where they are triaged". Pass.
  - AC3: same paragraph: "When `gh` is missing, unauthenticated, or the repo has no remote: name which of the three it was, skip the sweep, and continue planning." Pass.
  - AC4: step 4's Resolves bullet reads "...or an issue the user names, or a step-2 inbox hit the gate accepted — one entry per issue" (appended after the two existing sources); README's "Contributions come in through you" bullet gains one sentence: the plan's collision check reads both open inboxes and offers a disposition only for an item overlapping the scope being planned. Pass.
  - AC5: from the repo root, `python3 -m unittest discover -s scripts/tests` exit 0 (329 tests), `-s hooks/tests` exit 0 (121). Pass. Hand-run `skills/tests` also 566 OK, exit 0 (non-gating, D-109).
- Consistency gate: `cairn_validate.py` all checks passed (exit 0); no DESIGN.md principle changed (diff touches no `cairn/DESIGN.md`), so `cairn_impact` is skipped; `generic` profile's consistency-gate slot names no toolchain checks. Pass.
- Driving RR: none — projection-vs-outcome no-ops.
- Independent review (three lenses, fresh context). [S] blame-history: no conflicting finding; noted the D-108 door reading is a disclosed judgment call already in the work log. [S] prior-review-comments: probe found no inline PR comments; archived M074/M166 reviews are applied, not regressed; zero findings. [O] diff-bug: ten findings, ranked as reported, verbatim, each with its disposition:
  1. "`skills/milestone-plan/SKILL.md:99` — An overlapping open PR is unconditionally posed as 'a candidate row naming `/hotfix` as its door', dropping the size condition." — Rejected: AC2 fixes this wording (the plan called for it); tracking-rules Intake names `/hotfix` as the door and `/hotfix` itself routes an oversized PR onward, so the row's door is the same one the audit names.
  2. "`skills/milestone-plan/SKILL.md:93` — The own-work filter's `author` prong never says how the operator's identity is obtained, and `gh pr list --json author` returns an object (`{id, is_bot, login, name}`), not a login string." — Verified against live `gh` output. Fixed now: the parenthetical names `author.login` and `gh api user --jq .login` (the audit's outside-merges form); the AC1 filter wording is unchanged.
  3. "`skills/milestone-plan/SKILL.md:88` — The paragraph claims to run 'in the health audit's form (`/milestone` §2)' while `/milestone` §3 states 'The §2 inbox sweep resolves here, and nowhere else.'" — Rejected: "form" names the read (commands and filter); §3's sentence governs §2's own sweep, and the plan text sends its non-hits there. Unmodified line in another skill.
  4. "`skills/milestone-plan/SKILL.md:99` — 'a candidate row naming `/hotfix` as its door' fuses two dispositions that `/milestone` §3 keeps mutually exclusive." — Rejected: AC2 wording; a candidate row is the one disposition taken, its text naming the door the row is acted on through.
  5. "`skills/milestone-plan/SKILL.md:96` — The overlap test is stated against 'the goal being planned' while the surrounding collision check tests overlap against 'what the user described', and at step 2 the goal is a draft." — Rejected: the plan gate chose step-2 placement and recorded this exact falsifier in the work log; it has not fired.
  6. "`skills/milestone-plan/SKILL.md:101` — Non-hits leave only a bare count in the gate's chat, which is not a per-item trace and does not survive the session." — Rejected: the plan gate chose the count over per-item triage (work log), falsifier recorded and unfired.
  7. "`skills/milestone-plan/SKILL.md:89` — Neither enumeration command sets `--limit`, so both truncate at gh's default of 30 while the text promises to 'enumerate both' inboxes." — Verified (`gh pr list --help`: default 30). Rejected at review: AC1 quotes both commands verbatim, so a `--limit` cannot be added without an amendment, and the audit's own inbox commands (M74) share the shape; a repo with more than 30 open items is the condition that would reopen it.
  8. "`skills/milestone-plan/SKILL.md:91` — The paragraph says it is 'in the health audit's form' but its PR command adds `headRefName`, which the audit's command lacks." — Rejected: pre-existing gap in `/milestone` §2, named in Scope/Out as left as shipped.
  9. "`README.md:288` — The sentence says the plan 'reads both open inboxes' without mentioning the own-work filter, and omits the non-hit count report." — Rejected: AC4 asks for one sentence stating the read and its overlap condition; the sentence is written against the shipped paragraph and claims nothing it does not do.
  10. "`README.md:290` — Inserting the `/milestone-plan` sentence between the audit sentence and 'The audit also lists pull requests merged by others' leaves 'The audit' pointing back across an intervening subject." — Fixed now: the sentence moves to the end of the bullet, after the audit's outside-merges sentence.
- Actioned list: findings 2 and 10, both fixed on the branch before the gate; no finding demonstrates a criterion failing, so no return under the floor.

