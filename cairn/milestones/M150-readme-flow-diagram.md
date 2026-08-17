# M150: The core loop becomes a rendered diagram

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** `m150-readme-flow-diagram` · https://github.com/jmgirard/cairn/pull/151

## Goal

README.md's "The core loop" ASCII block becomes a Mermaid flowchart that GitHub
renders, showing the three gates and the review→implement return the one-line
chain cannot.

## Scope

Surface tier: **user-facing** — the README is what an adopter reads before
installing, so the criteria audit ran in full mode.

**In:** replacing the fenced block at `README.md:77-80` with a mermaid-fenced
flowchart carrying the four phase nodes, the three gates, and the edge back
from review to implement (the rulebook's `review → in-progress` transition on
a review failure); one `## Unreleased` CHANGELOG entry.

**Out:** the trivial-commit and `/hotfix` side doors → they keep their rows in
the "Which skill, when" table, unillustrated. Diagrams anywhere else in the
README (the directory tree, the skills table) → not proposed; a later docs
pass if wanted. Any image file, CDN asset, or build step → refused outright;
the fence is the whole mechanism. A local Mermaid parser → none exists on this
machine, so GitHub's rendering is the sole oracle (AC2).

## Acceptance criteria

- [x] AC1: README.md's `## The core loop` section contains a fenced block whose
      opening fence line is three backticks followed by `mermaid`, and within
      that block's line range the source carries the four node labels
      `/milestone-plan`, `/milestone-implement`, `/milestone-review`, `merged`,
      the three gate labels `scope gate`, `choices gate`, `approval gate`, and
      an edge directed from the review node back to the implement node — the
      return `tracking-rules.md` defines ("review failures return to
      `in-progress`"). Verified by grepping README.md for lines beginning with
      three backticks to fix the block's start and end lines, then reading
      exactly that range.
- [x] AC2: the added block renders as a diagram, not as literal source text,
      when GitHub displays README.md on the milestone branch — observed on the
      branch's README page in a browser.
- [x] AC3: the README properties its guards own are unchanged — the
      first-paragraph positioning framing, the sources/currency section, the
      boundary-rule homes, and the tree block's lessons line — verified by the
      hand-run `python3 -m unittest discover skills/tests` guards that own them
      (`test_readme_currency.py`, `test_positioning_guard.py`,
      `test_collaboration_boundary.py`), whose result is the D-109 hygiene-pass
      observation with any red classified, never an exit-0 merge bar.
- [x] AC4: CHANGELOG.md's `## Unreleased` section gains exactly one entry
      describing the diagram, verified by reading `git diff origin/main --
      CHANGELOG.md`: one added entry, every claim in it visible in the shipped
      README block.
- [x] AC5: the profile's `verify` slot is clean — `python3 -m unittest discover
      scripts/tests` and `python3 -m unittest discover hooks/tests` each exit 0.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T4

## Tasks

- [x] T1: draft the flowchart source — nodes, gate labels, the return edge —
      and check it against `README.md:71-84`'s prose so the drawing and the
      paragraph beneath it agree.
- [x] T2: replace `README.md:77-80` with the mermaid-fenced block; touch no other
      fenced block (the tree block, now `README.md:144-155`, is guarded).
- [x] T3: push the branch, open its README page on GitHub in a browser, and
      confirm the block renders as a figure; record the URL and date.
- [x] T4: run both gating suites and the hand-run `skills/tests`; record counts
      and classify any red per D-109.
- [x] T5: add the `## Unreleased` CHANGELOG entry, claiming only what the
      shipped block shows.

## Work log

- 2026-08-17: created by /milestone-plan; absorbs the "README flow diagram" candidate row (added 2026-08-14).
- 2026-08-17: plan-gate criteria audit ran in FULL mode (user-facing tier), fresh [O] reader; 7 findings returned, all fixed here — greppable terminal label, block-range co-location, back edge cited to the rulebook not recalled, AC2's record clause moved to the review procedure, AC3 re-pointed from the gating suites (which assert nothing about README) to the guards owning those properties, D-109's no-exit-0-bar reading restored, AC4 given a procedure.
- 2026-08-17: plan gate chose replacing the ASCII block over keeping both because two blocks stating one flow drift apart; falsified by a reader report that the Mermaid source is unreadable where the file is read unrendered.
- 2026-08-17: branch m150-readme-flow-diagram cut from main at 62ba630; status in-progress.
- 2026-08-17: plan gate chose phases+gates+return over also drawing the trivial and hotfix side doors because the section is the core loop and those carry their own table rows; falsified by a reader taking the loop as the only entry point into cairn.
- 2026-08-17: T1 refined — the draft is shown in chat and this line records it, rather than pasted into the work log where a multi-line block would trip the one-line entry rule.
- 2026-08-17: T1+T2 done — README.md:77-84 is now a mermaid flowchart (idea → plan → implement → review → merged, gates on the edges, review→implement return); diff is 7 insertions / 3 deletions confined to that block, the other three fenced blocks untouched (tree block shifted 140-151 → 144-155, content identical).
- 2026-08-17: T4 done — scripts/tests 308 tests exit 0, hooks/tests 103 exit 0, hand-run skills/tests 513 exit 0 (exit codes read directly, not through a pipe); no reds, so D-109's red-classification clause has nothing to classify.
- 2026-08-17: T3 done — on https://github.com/jmgirard/cairn/blob/m150-readme-flow-diagram/README.md the mermaid source pre sits under `render-plaintext-hidden` and GitHub mounts a live `viewscreen.githubusercontent.com/markdown/mermaid` viewer (861x180) in its place; screenshot at 1280px shows the drawn nodes, edge labels, and GitHub's diagram zoom/pan controls — it renders as a figure, not source text.
- 2026-08-17: T5 done — one CHANGELOG `## Unreleased` entry added; `git diff origin/main -- CHANGELOG.md` shows a single added entry and every claim in it (four phases, gates on the steps, review→implement return, GitHub renders in place) is visible in the shipped README block.
- 2026-08-17: all five tasks done; verify slot clean on the finished branch (scripts/tests 308 exit 0, hooks/tests 103 exit 0), cairn_validate green; status review.

## Decisions

## Review

**Evidence (fresh, 2026-08-17, branch at 1951d24 · PR #151)**

- AC1 — `grep -n '^```' README.md` puts the block at 77-84, opening at line 77 with
  its fence line (three backticks followed by `mermaid`). An awk scan restricted to lines 77-84 finds each required
  label exactly once: `/milestone-plan`, `/milestone-implement`,
  `/milestone-review`, `merged`, `scope gate`, `choices gate`, `approval gate`.
  The return edge is present in range: `review -->|findings to fix| implement`.
- AC2 — on https://github.com/jmgirard/cairn/blob/m150-readme-flow-diagram/README.md
  the mermaid source `pre` sits under `render-plaintext-hidden` and GitHub
  mounts a live `viewscreen.githubusercontent.com/markdown/mermaid` viewer
  (861x180) in its place; a screenshot taken earlier this session at 1280px
  width shows the drawn nodes, the edge labels, and GitHub's diagram zoom/pan
  controls. It renders as a figure, not as source text.
- AC3 — the three guards owning the README properties pass fresh:
  `test_readme_currency`, `test_positioning_guard`, `test_collaboration_boundary`
  = 30 tests, exit 0; the whole hand-run suite is 513 tests, exit 0. No reds, so
  D-109's red-classification clause has nothing to classify.
- AC4 — `git diff origin/main -- CHANGELOG.md` shows exactly one added entry
  under `## Unreleased`. Its four claims — four phases drawn, each gate on the
  step it opens, an arrow back from review to implement, GitHub renders it in
  place — are each visible in the shipped block (AC1 evidence) or observed
  (AC2 evidence).
- AC5 — `scripts/tests` 308 tests exit 0; `hooks/tests` 103 tests exit 0.

**Consistency gate** — `cairn_validate` exit 0, 16 PASS and no FAIL. No
principle changed, so `cairn_impact` is skipped. The `generic` profile's
consistency-gate slot names no toolchain checks, so that half is a clean no-op.

**Defect returns this milestone: 0. Amendment returns: 0.**

