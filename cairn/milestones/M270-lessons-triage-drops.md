<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M270: Let /cairn-triage lessons drop false, obsolete, and low-value lessons

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, GP1
- **Resolves:** —
- **Surface tier:** user-facing. Adopting repos run `/cairn-triage lessons`, a shipped plugin skill.
- **Branch/PR:** m270-lessons-triage-drops

## Goal

`/cairn-triage lessons` can free room in a full `cairn/LESSONS.md` by dropping or correcting false, obsolete, and low-value lessons and by shortening long lessons near the caps.

## Scope

**In:** the lessons pass of `skills/cairn-triage/SKILL.md` (lines 88 to 188 at plan time). It gains two evidence exits (`refuted`, `obsolete`) and a judgment exit (`planner test`). It also gains a sixth disposition (`correct`), a near-cap rule for long lessons, and a gate warning. One decision entry records the change. The rulebook bullet, the README row, and the CHANGELOG entry follow it. The prose guards in `skills/tests/test_triage_lessons.py` change with the text.

**Out:** the scoped retirement check at `/milestone-review` post-merge hygiene stays as it is. Nobody asked for it, so it gets no candidate row. Re-running the pass in the intraclass repo is the user's act after merge. The default candidate-row pass does not change.

## Acceptance criteria

- [ ] AC1: In the lessons pass of `skills/cairn-triage/SKILL.md`, a `drop` names one of five exits: enforcement, ownership, `refuted`, `obsolete`, and `planner test`. Enforcement and ownership stay as they are. A `refuted` drop quotes the evidence that shows the lesson's premise false: a file and line, or a command and its output, read in this pass. An `obsolete` drop names the path, tool, or command that the lesson is about. It also quotes an `ls`, `git grep`, or `git log` result, read in this pass, that shows the repo no longer has it. Or it names the commit that removed that path, tool, or command. In guest mode these reads run at `<base>/<default-branch>`. The skill states that a lesson without such evidence is not dropped as `refuted` or `obsolete`. The skill no longer says that a lesson about a path or tool the repo lacks stays `keep`.
- [ ] AC2: The lessons pass has a sixth disposition, `correct`. It is for a lesson found false that still holds a part a planner needs. A lesson found false with no such part is proposed `drop` with the `refuted` exit. The gate table shows the corrected line verbatim. An accepted `correct` rewrites the line in place and adds `corrected YYYY-MM-DD`, the pass date, to the line's parenthesized provenance. A line with no provenance gets one after its date. The stamp and the commit message name each accepted `correct` by its date and provenance. The skill no longer says that a false lesson stays `keep` until a milestone corrects it.
- [ ] AC3: The skill states the planner test. Some `keep` reasons are already fixed: a pin file, a live milestone, or `survivor of <subject>`. Each other `keep` reason names what a planner loses without the line. Sometimes the pass can name no such loss, and no tracking file holds the lesson, so ownership does not apply. Then the pass proposes `drop` with the exit `planner test`. The reason says why nothing is lost, for example a one-off incident or general practice.
- [ ] AC4: The skill states a near-cap rule. The rule applies when `wc -l` or `wc -c` on `cairn/LESSONS.md` reports 45 lines or more, or 18,000 bytes or more, at session start. Then each lesson whose step-1 byte length is over 400 gets one of two proposals. One is `compress`, with its shortened line shown verbatim in the gate table. The other is `keep`, with a reason that names why each clause stays. The rule skips a lesson proposed `drop`, `merge`, `correct`, or `promote`, a merge survivor, and a lesson kept for a pin or a live milestone. Below both figures, length alone never fires a `compress`.
- [ ] AC5: The skill states a gate warning. Each time the chip is posed, Amend rounds included, the pass counts the lines and bytes that the proposals then standing leave, all accepted. If the count is 45 lines or more, or 18,000 bytes or more, the chip's question text says so in one sentence. That sentence names the line and byte counts.
- [ ] AC6: `cairn/DECISIONS.md` gains one entry. It supersedes the D-169 clause that keeps a found-false lesson `keep` for a later milestone, and the D-169 consequence that D-051's exits alone stand. It annotates D-045 and D-051. It states that the `refuted`, `obsolete`, and `planner test` exits, the `correct` disposition, and the near-cap rule apply only in `/cairn-triage lessons`. It states that the scoped check at `/milestone-review` hygiene does not change. It names the shipped-behavior trigger that passes the D-108 door: the pass kept lessons it found false in a file at its caps.
- [ ] AC7: Three texts name the pass's new exits and its correction. In the "Retiring a lesson" bullet of `skills/shared/tracking-rules.md`, the sentences on the three exits and "corrected, not deleted" are scoped to review hygiene. The bullet then names the `refuted`, `obsolete`, and `planner test` exits and the in-pass correction. The `/cairn-triage` row of README.md says the lessons pass can drop false or obsolete lessons and correct one. The CHANGELOG.md Unreleased entry for `/cairn-triage lessons` names the new exits and the correction. It no longer says that a false lesson stays.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T2, T3
- AC5 → T2, T3
- AC6 → T1
- AC7 → T4

## Tasks

- [x] T1: Append the decision entry in the shape of `skills/shared/templates/decision.md` (AC6). Read D-045, D-051, D-055, D-108, and D-169 whole first.
- [x] T2: Edit the lessons pass in `skills/cairn-triage/SKILL.md` (AC1 to AC5). Change the step-2 table and the rules after it: the five exits, `correct`, the planner test, and the near-cap rule. Change step 3 for the `correct` text and the warning. Change step 4 so `correct` edits the file and counts against the caps. Change steps 5 to 7 so the stamp, the commit message, and the close block name corrections and the new exits. Remove the flag-only run of steps 4 to 6 for a false lesson. Update the skill's description line if its wording no longer fits.
- [x] T3: Update the prose guards in `skills/tests/test_triage_lessons.py`. Replace `test_five_dispositions_only`, `test_a_false_lesson_is_keep`, and `test_drop_names_an_exit`, and add one guard per new rule. Hand-run `python3 -m unittest discover -s skills/tests` from the repo root and check its exit code.
- [x] T4: Edit the rulebook bullet, the README row, and the CHANGELOG Unreleased entry (AC7). Then run `git grep -n -i -E "found false|stays .keep|two exits|length alone" -- skills README.md CHANGELOG.md` and fix each stale hit outside `skills/tests`.
- [ ] T5: Run steps 1 to 3 of the new pass read-only over this repo's `cairn/LESSONS.md` (47 lines and 18,996 bytes by `wc` at plan time). Pose no chip and apply nothing. Log one work-log line with the counts of each exit, each `correct`, and each near-cap `compress` that fire.

## Work log

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: milestone. The request changes a shipped skill and needs a decision that supersedes part of D-169.
- 2026-10-17: collision: absorbs the candidate row "Lessons triage drops too little" (user request via the intraclass session). D-051 and D-169 are superseded in part by the user's direction and at the question set. D-108's door is passed on a shipped-behavior defect. No open issues or PRs in the inbox.
- 2026-10-17: lessons harvested: M112 (sweep the old wording over README and CHANGELOG, T4), M152 (changing a decision's operative text owes a D-entry, T1), M148 and M171 (hand-run `skills/tests` after edits near pinned text, T3).
- 2026-10-17: criteria audit (full mode, fresh Opus reader): 14 findings, all fixed. AC1 and AC3 had four exits against five. AC6 now annotates D-045 and D-051 and names the D-108 trigger. AC2 now covers missing provenance and the stamp. AC3 now leaves out fixed keep reasons and is set apart from ownership. AC4 now uses `wc`, step-1 byte length, and leaves out `promote` and merge survivors. AC5 now recounts after Amend. AC7 now scopes the rulebook's exit sentences and keeps the README row short.
- 2026-10-17: question set: a judgment drop by the planner test — yes, the user decides each drop at the gate.
- 2026-10-17: question set: a found-false lesson — correct it in the pass when part is still useful, otherwise drop it as refuted.
- 2026-10-17: question set: long lessons near the caps — propose shortening each lesson over 400 bytes.
- 2026-10-17: plan gate chose correct-or-drop over always-drop because a partly true lesson keeps its true part; falsified by an accepted `correct` line that a later pass finds false again.
- 2026-10-17: plan gate chose the planner-test drop over a reason-only test because the reason-only test leaves a full file full; falsified by a planner-test drop whose trap then recurs.
- 2026-10-17: thresholds 45 lines and 18,000 bytes are 90 percent of the caps, and 400 bytes is the byte budget divided by the line cap. Decided by the agent.
- 2026-10-17: implement started on m270-lessons-triage-drops. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-17: T1 done: D-177 appended. It supersedes two D-169 clauses, annotates D-045 and D-051, and names the D-108 trigger.
- 2026-10-17: T2 done: the lessons pass has six dispositions, five drop exits, the planner test, the near-cap rule, and the gate warning. The skill description now says "correct". Its review-hygiene pointer cites D-177. The new sentences pass the simple-english sentence checks, and the file's older hits stay as they were.
- 2026-10-17: T3 done: the guards in `test_triage_lessons.py` now pin each new rule (25 tests). All 10 new or changed guards fail on the main-branch skill text. The mutation-harness registry was updated for the renamed tests and new blocks, which T3 did not name (minor amendment). Verify: scripts, hooks, and skills suites green, both plugin validates pass, `claude plugin test` 2018 pass.
- 2026-10-17: T4 done: the rulebook bullet scopes its three exits and "corrected, not deleted" to review hygiene and names the pass's three added exits, the correction, and the near-cap rule (D-177). README row and CHANGELOG Unreleased entry updated. The rulebook grew to 719 lines / 69,612 bytes, so the three rulebook-size sites were re-seeded (`skills/milestone/SKILL.md`, `test_cost_audit_line.py`, `test_mutation_harness.py`), and the rulebook registry block was rewrapped (minor amendment). The old-wording `git grep` found two hits outside `skills/tests`, both current text: the near-cap sentence and an unrelated `retitle` keep. Suites green, validate green.

## Decisions

## Review
