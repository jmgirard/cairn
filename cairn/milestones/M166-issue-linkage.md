# M166: GitHub issues are linked at plan time and closed at merge

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** #168 closes
- **Branch/PR:** m166-issue-linkage

## Goal

A milestone that resolves a GitHub issue names the issue at plan time, carries a closing keyword into its PR so GitHub closes the issue at merge, and confirms the close afterward, so a collaborator sees the issue acknowledged when the work is queued and closed when it ships.

## Scope

**Surface tier:** user-facing — the deliverable is skill conduct every adopting repo runs (nestedtune's five topepo issues are the motivating record: issue #168 states it).

**In:**
- A `Resolves:` header slot on the milestone template (owner: plan), entries `#N closes` or `#N partial`; the archive-summary template's status line carries the entries so the audit can read them after archiving.
- `/milestone-plan`: fills the slot from the issues the scope absorbs; a `partial` entry's remainder becomes a candidate row in the same plan commit; the plan gate offers to post an acknowledgement comment on the slotted issues.
- `/milestone-review`: the draft PR body ends with `Closes #N` / `Refs #N` lines from the slot; the merge chip's text enumerates the post-merge issue writes it authorizes; step 9 reads each `closes` issue's state and closes any still open, comments on partials.
- `/hotfix`: the same post-merge state read for a `Fixes #N` PR.
- `/milestone` §2/§3: an orphan bullet — an issue still open on GitHub though the milestone slotted as closing it is done — with a close disposition in the triage chip; the audit still writes nothing to GitHub.
- README "Working with collaborators": the three behaviors.
- Every GitHub write stays behind an existing user gate (plan-gate chip, merge chip, triage chip); none is a default.

**Out:** reconciling PRs merged outside cairn → candidate row (added with this plan); a contributor-facing scaffold → its standing candidate row; nestedtune issue #33's un-rowed `control` remainder → a nestedtune ROADMAP edit, not cairn's; an issue-number parser in `cairn_validate` → not planned (the slot is skill conduct; no check parses it).

## Acceptance criteria

- [ ] AC1: `skills/shared/templates/milestone.md` carries a header slot `- **Resolves:** —` with an owner comment naming the `#N closes` / `#N partial` entry forms, and `skills/shared/templates/archive-summary.md`'s status line carries a `resolves <entries>` clause; a `scripts/tests` fixture milestone runs `cairn_validate` clean with the slot filled `#12 closes, #13 partial` and with `—`, and no `cairn_validate` check parses the slot's contents.
- [ ] AC2: `/milestone-plan` step 4 states that the slot is filled from the issues the scope absorbs — a promoted candidate row citing one, or an issue the user names — and that a `partial` entry's remainder is recorded as a `candidate` row in the same plan commit and listed in step 5's remainder ledger; step 3 states that the gate poses one option offering an acknowledgement comment on all slotted issues, whose body is `Queued as M<NNN>: <title>` plus, for a partial, the remainder's candidate-row text, shown before selection, posted with `gh issue comment` only on selection.
- [ ] AC3: `/milestone-review` step 2 states that the draft PR body ends with one `Closes #N` line per `closes` entry and one `Refs #N` line per `partial` entry of the `Resolves:` slot; step 7 states that the merge chip's question text enumerates the post-merge issue writes it authorizes (close-if-open per `closes` entry; a comment naming what shipped and the remainder's candidate row per `partial` entry); step 9 states that after the merge each `closes` entry's state is read with `gh issue view <N> --json state` and one still open is closed with a one-line comment naming the merged PR, that the `partial` comments are posted, and that an unreachable `gh` (missing, unauthenticated, no remote) is named in the done recap and never fails the hygiene pass; `/hotfix` step 7 states the same post-merge state read and close-if-open for the issue a `Fixes #N` line names when the PR carries one, a no-op otherwise, with the same unreachable-`gh` reporting.
- [ ] AC4: This milestone's `Resolves:` slot names `#168 closes`, and its PR body ends with the line `Closes #168` (verified on the draft PR); step 9's post-merge state read for #168 is reported in the done recap.
- [ ] AC5: `/milestone` §2 gains an audit bullet that, for each `done` row still in the ROADMAP table (the retained terminal rows bound the reads) whose archive summary's status line carries a `resolves` entry marked `closes`, reads that issue's state with `gh issue view <N> --json state,url` and reports one still open as an orphan; §3 carries a close disposition per orphan that, only on the user's selection in the triage chip, closes the issue with a one-line comment naming the archived milestone's PR; the §2 sweep and the orphan read write nothing, and the inbox bullet's never-write sentence is narrowed to the reads with its unreachable-`gh` rule applying unchanged.
- [ ] AC6: `README.md`'s "Working with collaborators" section states the three behaviors — plan-time acknowledgement offer, PR closing keyword, post-merge check — each matching a line of the shipped skill text it describes.
- [ ] AC7: The active profile's `verify` slot is clean: `python3 -m unittest discover scripts/tests` and `python3 -m unittest discover hooks/tests` exit 0 on the branch, and the hand-run `skills/tests` suite is green.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3, T4
- AC4 → T7
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks

- [x] T1: Add the `Resolves:` slot to `skills/shared/templates/milestone.md` (after `Principles touched:`) and the `resolves` clause to `skills/shared/templates/archive-summary.md`'s status line; add a `scripts/tests` fixture test (filled and `—` forms run `cairn_validate` clean; `check_principles_slot`'s validate-if-present shape at `scripts/cairn_validate.py:726` is the precedent for leaving the slot unparsed).
- [ ] T2: `/milestone-plan` steps 3–5 (`skills/milestone-plan/SKILL.md` step 3 gate, step 4 header slots near the `Principles touched` bullet, step 5 ledger); prose guard `skills/tests/test_issue_linkage.py` with mutation entries pinning the trigger (slot filled from absorbed issues) and the gate condition (posted only on selection).
- [ ] T3: `/milestone-review` steps 2, 7, 9 (`skills/milestone-review/SKILL.md:29`, `:280-297`, `:321-390`); guard entries pinning the PR-body lines, the chip's authorization enumeration, the step-9 read-and-close, and the unreachable-`gh` clause.
- [ ] T4: `/hotfix` step 7 (`skills/hotfix/SKILL.md`, after the candidate-row sentence); guard entry.
- [ ] T5: `/milestone` §2 orphan bullet beside the untriaged-inboxes bullet (`skills/milestone/SKILL.md:125`), bounded to the ROADMAP's retained terminal rows, and the §3 close disposition (`:182-190`); narrow the §2 never-write sentence to the reads and record that narrowing of M74's shipped rule as a milestone-local decision; guard entries vary the archive fixture (no entry, `partial` only, multi-entry, unreachable `gh`).
- [ ] T6: README "Working with collaborators" bullet(s) (`README.md:282-287`), each sentence written against the shipped skill lines (derived-claims rule).
- [ ] T7: Run both gating suites and hand-run `skills/tests`; at review, the PR body carries `Closes #168` (the slot dictates it) and the post-merge read is the live proof.

## Work log

- 2026-09-02: created by /milestone-plan. Criteria audit ran in full mode (fresh [O] reader): ten findings on the first draft — AC1 reworded to a validate-clean fixture with no parser (unknown header slots are ignored by every check), AC2 to one chip option for all slotted issues and skill-text binding, AC3 to route post-merge issue writes through the merge chip's authorization text, AC4 conditional on a `Fixes #N` line, AC5 conditional on a slotted issue, the README criterion to three behaviors matching shipped lines, the test-harness criterion folded into the verify criterion; the live-proof and the gate-added orphan-check criteria re-entered the audit before writing: the live proof's `CLOSED` read moved to the post-merge done recap (evidence is gathered before the merge), the orphan check's reads bounded to the retained terminal rows (GP1) and its close made a chip-selected write, the §2 never-write sentence narrowed to the reads.
- 2026-09-02: sizing advisory (8 criteria) cleared by folding the hotfix clause into the review criterion — one conduct rule, two skill sites.
- 2026-09-02: plan gate chose the full loop (plan-time acknowledgement + PR keyword + post-merge check) over PR-keyword-and-check only because the nestedtune record's visible gap was 51 hours of silence on five issues while work was under way; falsified by an adopter declining the acknowledgement option at every plan gate.
- 2026-09-02: plan gate chose including the audit orphan check now over a candidate row because the `Answers #36` case shows the failure mode is a missed keyword, which only a later read can catch; falsified by the bullet never reporting an orphan across adopting repos.
- 2026-09-02: plan gate chose filing issue #168 in this repo as the live proof over skill-text verification alone; falsified by the dogfood run passing while an adopter's first run fails on a path the fixture never exercised.
- 2026-09-02: implement started on `m166-issue-linkage`; question gate skipped — the plan pins every open shape (slot name, entry forms, comment body, commands).
- 2026-09-02: T1 done — `Resolves:` slot on the milestone template, `resolves` clause on the archive-summary status line, `TestResolvesSlot` (filled + `—` validate clean; validate source parses neither form); suites scripts 329 / hooks 121 green.

## Decisions
