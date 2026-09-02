# M166: GitHub issues are linked at plan time and closed at merge

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** #168 closes
- **Branch/PR:** m166-issue-linkage · PR #169 https://github.com/jmgirard/cairn/pull/169

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

- [x] AC1: `skills/shared/templates/milestone.md` carries a header slot `- **Resolves:** —` with an owner comment naming the `#N closes` / `#N partial` entry forms, and `skills/shared/templates/archive-summary.md`'s status line carries a `resolves <entries>` clause; a `scripts/tests` fixture milestone runs `cairn_validate` clean with the slot filled `#12 closes, #13 partial` and with `—`, and no `cairn_validate` check parses the slot's contents.
- [x] AC2: `/milestone-plan` step 4 states that the slot is filled from the issues the scope absorbs — a promoted candidate row citing one, or an issue the user names — and that a `partial` entry's remainder is recorded as a `candidate` row in the same plan commit and listed in step 5's remainder ledger; step 3 states that the gate poses one option offering an acknowledgement comment on all slotted issues, whose body is `Queued as M<NNN>: <title>` plus, for a partial, the remainder's candidate-row text, shown before selection, posted with `gh issue comment` only on selection.
- [x] AC3: `/milestone-review` step 2 states that the draft PR body ends with one `Closes #N` line per `closes` entry and one `Refs #N` line per `partial` entry of the `Resolves:` slot; step 7 states that the merge chip's question text enumerates the post-merge issue writes it authorizes (close-if-open per `closes` entry; a comment naming what shipped and the remainder's candidate row per `partial` entry); step 9 states that after the merge each `closes` entry's state is read with `gh issue view <N> --json state` and one still open is closed with a one-line comment naming the merged PR, that the `partial` comments are posted, and that an unreachable `gh` (missing, unauthenticated, no remote) is named in the done recap and never fails the hygiene pass; `/hotfix` step 7 states the same post-merge state read and close-if-open for the issue a `Fixes #N` line names when the PR carries one, a no-op otherwise, with the same unreachable-`gh` reporting.
- [ ] AC4: This milestone's `Resolves:` slot names `#168 closes`, and its PR body ends with the line `Closes #168` (verified on the draft PR); step 9's post-merge state read for #168 is reported in the done recap.
- [x] AC5: `/milestone` §2 gains an audit bullet that, for each `done` row still in the ROADMAP table (the retained terminal rows bound the reads) whose archive summary's status line carries a `resolves` entry marked `closes`, reads that issue's state with `gh issue view <N> --json state,url` and reports one still open as an orphan; §3 carries a close disposition per orphan that, only on the user's selection in the triage chip, closes the issue with a one-line comment naming the archived milestone's PR; the §2 sweep and the orphan read write nothing, and the inbox bullet's never-write sentence is narrowed to the reads with its unreachable-`gh` rule applying unchanged.
- [x] AC6: `README.md`'s "Working with collaborators" section states the three behaviors — plan-time acknowledgement offer, PR closing keyword, post-merge check — each matching a line of the shipped skill text it describes.
- [x] AC7: The active profile's `verify` slot is clean: `python3 -m unittest discover scripts/tests` and `python3 -m unittest discover hooks/tests` exit 0 on the branch, and the hand-run `skills/tests` suite is green.

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
- [x] T2: `/milestone-plan` steps 3–5 (`skills/milestone-plan/SKILL.md` step 3 gate, step 4 header slots near the `Principles touched` bullet, step 5 ledger); prose guard `skills/tests/test_issue_linkage.py` with mutation entries pinning the trigger (slot filled from absorbed issues) and the gate condition (posted only on selection).
- [x] T3: `/milestone-review` steps 2, 7, 9 (`skills/milestone-review/SKILL.md:29`, `:280-297`, `:321-390`); guard entries pinning the PR-body lines, the chip's authorization enumeration, the step-9 read-and-close, and the unreachable-`gh` clause.
- [x] T4: `/hotfix` step 7 (`skills/hotfix/SKILL.md`, after the candidate-row sentence); guard entry.
- [x] T5: `/milestone` §2 orphan bullet beside the untriaged-inboxes bullet (`skills/milestone/SKILL.md:125`), bounded to the ROADMAP's retained terminal rows, and the §3 close disposition (`:182-190`); narrow the §2 never-write sentence to the reads and record that narrowing of M74's shipped rule as a milestone-local decision; guard entries vary the archive fixture (no entry, `partial` only, multi-entry, unreachable `gh`).
- [x] T6: README "Working with collaborators" bullet(s) (`README.md:282-287`), each sentence written against the shipped skill lines (derived-claims rule).
- [x] T7: Run both gating suites and hand-run `skills/tests`; at review, the PR body carries `Closes #168` (the slot dictates it) and the post-merge read is the live proof.

## Work log

- 2026-09-02: created by /milestone-plan. Criteria audit ran in full mode (fresh [O] reader): ten findings on the first draft — AC1 reworded to a validate-clean fixture with no parser (unknown header slots are ignored by every check), AC2 to one chip option for all slotted issues and skill-text binding, AC3 to route post-merge issue writes through the merge chip's authorization text, AC4 conditional on a `Fixes #N` line, AC5 conditional on a slotted issue, the README criterion to three behaviors matching shipped lines, the test-harness criterion folded into the verify criterion; the live-proof and the gate-added orphan-check criteria re-entered the audit before writing: the live proof's `CLOSED` read moved to the post-merge done recap (evidence is gathered before the merge), the orphan check's reads bounded to the retained terminal rows (GP1) and its close made a chip-selected write, the §2 never-write sentence narrowed to the reads.
- 2026-09-02: sizing advisory (8 criteria) cleared by folding the hotfix clause into the review criterion — one conduct rule, two skill sites.
- 2026-09-02: plan gate chose the full loop (plan-time acknowledgement + PR keyword + post-merge check) over PR-keyword-and-check only because the nestedtune record's visible gap was 51 hours of silence on five issues while work was under way; falsified by an adopter declining the acknowledgement option at every plan gate.
- 2026-09-02: plan gate chose including the audit orphan check now over a candidate row because the `Answers #36` case shows the failure mode is a missed keyword, which only a later read can catch; falsified by the bullet never reporting an orphan across adopting repos.
- 2026-09-02: plan gate chose filing issue #168 in this repo as the live proof over skill-text verification alone; falsified by the dogfood run passing while an adopter's first run fails on a path the fixture never exercised.
- 2026-09-02: implement started on `m166-issue-linkage`; question gate skipped — the plan pins every open shape (slot name, entry forms, comment body, commands).
- 2026-09-02: T1 done — `Resolves:` slot on the milestone template, `resolves` clause on the archive-summary status line, `TestResolvesSlot` (filled + `—` validate clean; validate source parses neither form); suites scripts 329 / hooks 121 green.
- 2026-09-02: T2 done — plan step 3 acknowledgement option, step 4 `Resolves` slot bullet, step 5 ledger sentence; `test_issue_linkage.py` (9 asserts) + 9 mutation entries; tracking-rules ownership table lists `Resolves` under the plan-owned header row (the allow-list parity guard required it); skills 543 hand-run green.
- 2026-09-02: T3 done — review step 2 `Closes`/`Refs` lines from the slot, step 7 chip enumerates the post-merge issue writes, step 9 reads each `closes` entry, closes if open, posts partial comments, names an unreachable `gh` in the done recap; 9 guard asserts + 9 mutation entries.
- 2026-09-02: T4 done — hotfix step 7 post-merge read and close-if-open for a `Fixes #N` line, no-op without one, same unreachable-`gh` reporting; 3 asserts + 3 entries.
- 2026-09-02: T5 done — audit §2 orphan bullet (bounded to retained terminal rows; no-clause/partial-only rows read nothing, multi-entry rows read each; writes nothing; unreachable-`gh` rule unchanged), §2 never-write sentence narrowed to the reads, §3 `close` disposition at the triage chip; milestone-local decision below; 8 asserts + 10 entries; skills 563 hand-run green.
- 2026-09-02: T6 done — README collaborators bullet states the three behaviors, each sentence written against the shipped skill lines of T2/T3/T5; 3 guard asserts + 5 mutation entries.
- 2026-09-02: T7 implement half done — on the branch: scripts 329, hooks 121, skills 566 hand-run, all green; the `Closes #168` PR-body check and the post-merge #168 state read are review's live proof. Status → review.
- 2026-09-02: review started; branch even with origin/main (no merge needed); draft PR #169 opened; suites, validate, and AC evidence recorded below; three-lens fan-out spawned.
- 2026-09-02: fan-out reported 14 findings (O 12, blame 0, prior-review 2); 9 applied at the gate as fix-now (README derived-claims tightening, hotfix chip names its post-merge close, AC1 source read widened, §3 scope sentence, ack-comment timing, review-path scoping, rulebook-mass baseline re-seeded), 5 rejected with reason — recorded in Review; suites re-run green.

## Decisions

- 2026-09-02: M74's §2 rule "never write to GitHub" is narrowed to the audit's reads — the inbox sweep and the new orphan read — and the §3 `close` disposition becomes the one GitHub write on the audit path, made only at the user's selection in the triage chip. Rationale: the orphan check exists because a missed closing keyword is caught only by a later read, and reporting an orphan with no way to close it hands the user a chore the audit can finish behind the same kind of gate every other issue write in this milestone uses (plan-gate chip, merge chip). The read side of M74's rule and its unreachable-`gh` degradation are untouched. Milestone-local: it narrows one skill's shipped sentence, not a cross-cutting rule.

## Review

- Sync: branch cut from and even with `origin/main` at the v1.10.1 release commit; no merge needed. Draft PR #169 (https://github.com/jmgirard/cairn/pull/169).
- AC1 PASS: `git diff main...HEAD` shows `- **Resolves:** —` on `skills/shared/templates/milestone.md` with an owner comment naming the `#N closes` / `#N partial` forms, and a `resolves <entries>` clause on the archive-summary status line; `TestResolvesSlot` (3 tests — slot `#12 closes, #13 partial`, slot `—`, and a source read showing `cairn_validate.py` contains neither `resolves:` nor `#N closes`) passes on the branch.
- AC2 PASS: plan step 4 carries the `Resolves` bullet (filled from the issues the scope absorbs — a promoted candidate row citing one, or an issue the user names; a `partial` remainder rowed in the same plan commit and listed in step 5's ledger); step 3 carries the one-option acknowledgement (body `Queued as M<NNN>: <title>` plus the remainder's candidate-row text for a partial, shown before selection, `gh issue comment` only on selection); step 5's ledger sentence present. All read in the diff; pinned by `skills/tests/test_issue_linkage.py`.
- AC3 PASS: review step 2 (`Closes #N` per `closes`, `Refs #N` per `partial`, `—` adds none), step 7 (chip text enumerates the post-merge writes it authorizes; no other issue write), step 9 (`gh issue view <N> --json state`, close-if-open with a one-line comment naming the merged PR, partial comments posted, unreachable `gh` named in the done recap and never a hygiene failure); hotfix step 7 (same read for a `Fixes #N` line, no-op without one, same unreachable-`gh` reporting). All read in the diff; pinned by the guard file.
- AC4 (pre-merge halves): header slot reads `#168 closes`; the draft PR body's last non-empty line is `Closes #168` (read via `gh pr view --json body`); #168 is OPEN before the merge. The done-recap clause is verified at step 9, where the box is ticked.
- AC5 PASS: `/milestone` §2 orphan bullet reads each `done` row's archive status line for a `closes` entry (bounded to the retained terminal rows; `gh issue view <N> --json state,url`; no clause or partial-only reads nothing, several `closes` entries each read; the read writes nothing; unreachable-`gh` rule unchanged); §2 never-write sentence narrowed to the sweep and the orphan read; §3 `close` disposition fires only on the user's selection with a one-line comment naming the archived milestone's PR. Read in the diff; pinned by the guard file.
- AC6 PASS: README collaborators bullet — acknowledgement offer ↔ plan step 3; `Closes #N`/`Refs #N` ↔ review step 2; post-merge read-and-close ↔ review step 9; audit orphan + close offer ↔ milestone §2/§3; "without `gh` names the gap" ↔ the three unreachable-`gh` clauses. Each sentence traced to its shipped line in the diff; pinned by `TestReadmeStatesTheThreeBehaviors`.
- AC7 PASS: at a192843 — scripts 329 tests OK (exit 0), hooks 121 OK (exit 0), skills 566 OK hand-run (exit 0).
- Consistency gate: `cairn_validate` all checks passed, exit 0 (`release window` advisory OK); `cairn/DESIGN.md` untouched → `cairn_impact` skipped; `generic` profile's consistency-gate slot names no toolchain checks.
- Review routing: declared tier user-facing and the diff touches `scripts/tests` + `skills/tests` → full three-lens fan-out ([O] diff-bug, [S] blame-history, [S] prior-review-record), fresh-context, ref-based git.
- Findings (ranked as reported; disposition applied on the branch before the gate, the merge chip carrying each for the maintainer's acceptance or reversal):
  - [O] F1 fix-now: `/hotfix` step 7 closes an issue behind no gate text — step 6's chip now names the post-merge close-if-open a `Fixes #N` PR authorizes.
  - [O] F2 fix-now: README "Without `gh`, each of these names the gap" over-claimed — narrowed to the post-merge check and the audit, the two shipped clauses.
  - [O] F3 fix-now: README dropped the orphan bullet's bound — now "(among the roadmap's retained done rows)".
  - [O] F4 fix-now: README "reads each issue's state" over-claimed — now "each issue slotted `closes`"; guard regex and mutation block updated with it.
  - [O] F5 fix-now: AC1's no-parser source read covered `cairn_validate.py` only — `cairn_scripts.py` added to the read (neither spells the slot).
  - [O] F6 reject: the tracking-rules Intake sentence enumerates dispositions for inbox items; an orphan is a done milestone's issue, not intake, so `close` widens no intake enumeration.
  - [O] F7 fix-now: §3's "inbox sweep resolves here" sentence now names the orphan bullet too.
  - [O] F8 fix-now: the acknowledgement comment is "composed against the plan as the gate's other answers settle it".
  - [O] F9 fix-now: "no other issue write is made" scoped "on the review path".
  - [O] F10 reject: "never fails the hygiene pass" states the step's outcome (the pass completes without `gh`); its position after the commit changes nothing.
  - [O] F11 reject: step 9 authors the archive from the template, whose status line carries the `resolves` placeholder — the template is the instruction by design.
  - [O] F12 reject: style nit (owner-comment length).
  - [S-prior] F1 fix-now: rulebook-mass baseline stale at its three sites after a deliberate rulebook edit (M149/M159 lesson) — re-seeded to 467 lines / 43,454 chars (M166); drift predates the branch (M162, M165 edited without re-seeding).
  - [S-prior] F2 reject: GitHub comments are not durable records under `cairn/`; the plan gate already shows the comment body verbatim before selection.
  - [S-blame]: no findings.
- Post-fix evidence: scripts 329 OK, hooks 121 OK, skills 566 OK hand-run, validate all checks passed.
