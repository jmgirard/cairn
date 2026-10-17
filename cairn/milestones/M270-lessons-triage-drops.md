<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M270: Let /cairn-triage lessons drop false, obsolete, and low-value lessons

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, GP1
- **Resolves:** —
- **Surface tier:** user-facing. Adopting repos run `/cairn-triage lessons`, a shipped plugin skill.
- **Branch/PR:** m270-lessons-triage-drops https://github.com/jmgirard/cairn/pull/282

## Goal

`/cairn-triage lessons` can free room in a full `cairn/LESSONS.md` by dropping or correcting false, obsolete, and low-value lessons and by shortening long lessons near the caps.

## Scope

**In:** the lessons pass of `skills/cairn-triage/SKILL.md` (lines 88 to 188 at plan time). It gains two evidence exits (`refuted`, `obsolete`) and a judgment exit (`planner test`). It also gains a sixth disposition (`correct`), a near-cap rule for long lessons, and a gate warning. One decision entry records the change. The rulebook bullet, the README row, and the CHANGELOG entry follow it. The prose guards in `skills/tests/test_triage_lessons.py` change with the text.

**Out:** the scoped retirement check at `/milestone-review` post-merge hygiene stays as it is. Nobody asked for it, so it gets no candidate row. Re-running the pass in the intraclass repo is the user's act after merge. The default candidate-row pass does not change.

## Acceptance criteria

- [x] AC1: In the lessons pass of `skills/cairn-triage/SKILL.md`, a `drop` names one of five exits: enforcement, ownership, `refuted`, `obsolete`, and `planner test`. Enforcement and ownership stay as they are. A `refuted` drop quotes the evidence that shows the lesson's premise false: a file and line, or a command and its output, read in this pass. An `obsolete` drop names the path, tool, or command that the lesson is about. It also quotes an `ls`, `git grep`, or `git log` result, read in this pass, that shows the repo no longer has it. Or it names the commit that removed that path, tool, or command. In guest mode these reads run at `<base>/<default-branch>`. The skill states that a lesson without such evidence is not dropped as `refuted` or `obsolete`. The skill no longer says that a lesson about a path or tool the repo lacks stays `keep`.
- [x] AC2: The lessons pass has a sixth disposition, `correct`. It is for a lesson found false that still holds a part a planner needs. A lesson found false with no such part is proposed `drop` with the `refuted` exit. The gate table shows the corrected line verbatim. An accepted `correct` rewrites the line in place and adds `corrected YYYY-MM-DD`, the pass date, to the line's parenthesized provenance. A line with no provenance gets one after its date. The stamp and the commit message name each accepted `correct` by its date and provenance. The skill no longer says that a false lesson stays `keep` until a milestone corrects it.
- [x] AC3: The skill states the planner test. Some `keep` reasons are already fixed: a pin file, a live milestone, or `survivor of <subject>`. Each other `keep` reason names what a planner loses without the line. Sometimes the pass can name no such loss, and no tracking file holds the lesson, so ownership does not apply. Then the pass proposes `drop` with the exit `planner test`. The reason says why nothing is lost, for example a one-off incident or general practice.
- [x] AC4: The skill states a near-cap rule. The rule applies when `wc -l` or `wc -c` on `cairn/LESSONS.md` reports 45 lines or more, or 18,000 bytes or more, at session start. Then each lesson whose step-1 byte length is over 400 gets one of two proposals. One is `compress`, with its shortened line shown verbatim in the gate table. The other is `keep`, with a reason that names why each clause stays. The rule skips a lesson proposed `drop`, `merge`, `correct`, or `promote`, a merge survivor, and a lesson kept for a pin or a live milestone. Below both figures, length alone never fires a `compress`.
- [x] AC5: The skill states a gate warning. Each time the chip is posed, Amend rounds included, the pass counts the lines and bytes that the proposals then standing leave, all accepted. If the count is 45 lines or more, or 18,000 bytes or more, the chip's question text says so in one sentence. That sentence names the line and byte counts.
- [x] AC6: `cairn/DECISIONS.md` gains one entry. It supersedes the D-169 clause that keeps a found-false lesson `keep` for a later milestone, and the D-169 consequence that D-051's exits alone stand. It annotates D-045 and D-051. It states that the `refuted`, `obsolete`, and `planner test` exits, the `correct` disposition, and the near-cap rule apply only in `/cairn-triage lessons`. It states that the scoped check at `/milestone-review` hygiene does not change. It names the shipped-behavior trigger that passes the D-108 door: the pass kept lessons it found false in a file at its caps.
- [x] AC7: Three texts name the pass's new exits and its correction. In the "Retiring a lesson" bullet of `skills/shared/tracking-rules.md`, the sentences on the three exits and "corrected, not deleted" are scoped to review hygiene. The bullet then names the `refuted`, `obsolete`, and `planner test` exits and the in-pass correction. The `/cairn-triage` row of README.md says the lessons pass can drop false or obsolete lessons and correct one. The CHANGELOG.md Unreleased entry for `/cairn-triage lessons` names the new exits and the correction. It no longer says that a false lesson stays.

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
- [x] T5: Run steps 1 to 3 of the new pass read-only over this repo's `cairn/LESSONS.md` (47 lines and 19,892 bytes by `wc`). Pose no chip and apply nothing. Log one work-log line with the counts of each exit, each `correct`, and each near-cap `compress` that fire.

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
- 2026-10-17: T5 task text corrected to 19,892 bytes (minor amendment). The plan's 18,996 was the intraclass file, read from the wrong directory.
- 2026-10-17: T5 done (read-only, nothing applied): the file is near its caps. `correct` 1: the 2026-08-17 (M149) lesson cites `test_cost_audit_line.py:68`, and the pin now sits at line 70. `refuted` 0. `obsolete` 0: `git grep` finds `check_dangling_ids`, `TestHeadingNormalizationContract`, `CMD_POS`, and `is_guarded_merge`. `planner test` 1 candidate: 2026-08-16 (M146), a one-off count. Ownership 1 candidate: 2026-07-27 (M114), held by the rulebook's record-prose rule. Near-cap: 19 lessons are over 400 bytes, and `compress` fits at least the four over 1,000 bytes (2026-07-16, 2026-08-29, 2026-10-01, 2026-10-03).
- 2026-10-17: claim audit: 75 claims read, 4 corrected — CHANGELOG.md (the warning counts proposals, not accepted changes; near-cap lessons are shortened or kept with a reason), tracking-rules.md (same near-cap overstatement), skills/cairn-triage/SKILL.md (the `keep` row now names the fixed pin, milestone, and survivor reasons). The CHANGELOG list of dispositions also gained "correct it". The rulebook re-seeded to 719 lines / 69,651 bytes at the three sites. Verify slot green: three unittest suites, both plugin validates, `claude plugin test` 2018 pass, `cairn_validate` green.
- 2026-10-17: implement done; status set to `review`.
- 2026-10-17: step-7 approval: m270-lessons-triage-drops approved for merge

## Decisions

## Review

Evidence, gathered 2026-10-17 on the review head by whitespace-normalized phrase counts over `skills/cairn-triage/SKILL.md` (each count below is 1 unless stated 0) and by the suites.

- AC1: "The reason names one of five exits." 1; the `refuted` cell (file and line, or command and output, read in this pass) 1; the `obsolete` cell 1, with its `ls`/`git grep`/`git log` quote and "Or it names the commit that removed it." 1; guest reads "run at that ref too" 1; "is not dropped as `refuted` or `obsolete`" 1; the old "A lesson about a path or tool the repo no longer has is `keep`" 0. Guards `test_drop_names_one_of_five_exits` and `test_evidence_exits_need_evidence` pass.
- AC2: "A lesson takes one of six dispositions" 1; the `correct` row's "The table shows the corrected line verbatim." 1; "adds `corrected YYYY-MM-DD`, the pass date" 1; "A line with no provenance gets one after its date." 1; "A false lesson with no such part is `drop` with the `refuted` exit." 1; step 5's "each corrected lesson by its date and provenance" (stamp and commit message) 1; the old "A lesson the pass finds false is `keep`" 0 and "corrected in place (D-045) at a milestone, not in this pass" 0. Guard `test_a_false_lesson_is_corrected_or_dropped` passes.
- AC3: the `keep` row "or else what a planner loses without the line" 1; "A `keep` whose reason is already fixed needs no answer" (pin file, live milestone, `survivor of <subject>`) 1; the no-loss, no-tracking-file case "Then the pass proposes `drop` with the `planner test` exit." 1; the `planner test` cell gives "a one-off incident or general practice" as examples. Guard `test_planner_test` passes.
- AC4: session start "run `wc -l -c cairn/LESSONS.md`. A file at 45 lines or more, or 18,000 bytes or more, is near its caps" 1; "Each lesson whose step-1 byte length is over 400 gets one of two proposals." 1, followed by `compress` with its shortened line verbatim in the table or `keep` with a reason for each clause; the skips ("`drop`, `merge`, `correct`, or `promote`" and "a merge survivor and a lesson kept for a pin or a live milestone") 1; "Below the near-cap figures, length alone never fires a `compress`." 1. Guard `test_near_cap_rule` passes.
- AC5: step 3 "Each time the chip is posed, Amend rounds included, count the lines and bytes that `cairn/LESSONS.md` has with the proposals then standing all applied." 1; the 45-line / 18,000-byte condition with "the chip's question text says so. One sentence names both counts." 1. Guard `test_gate_warning` passes.
- AC6: `cairn/DECISIONS.md:6407` holds `### D-177`, the one new entry on the branch (`git diff main...HEAD -- cairn/DECISIONS.md` adds one heading). Its heading supersedes D-169's false-lesson clause and its clause that D-051's exits stand, and annotates D-045 and D-051. Its Decision opens "In `/cairn-triage lessons` only" and covers the three exits, `correct`, and the near-cap rule; it states "The `/milestone-review` hygiene check stays as D-051 scopes it"; its Context names the D-108 trigger (the shipped pass kept lessons it found false in a file at its caps).
- AC7: `skills/shared/tracking-rules.md:126` opens "At review hygiene, three exits", and :134 reads "At review hygiene, retirement removes the redundant, never the merely disputed (a disputed lesson is corrected, not deleted)"; :137-139 name `refuted`, `obsolete`, `planner test`, and "corrects a false lesson in place". `README.md:627` reads "can drop a false or obsolete lesson or correct one". The CHANGELOG.md Unreleased entry for `/cairn-triage lessons` names the false, obsolete, and planner exits and the in-place correction; `grep -n 'flagged for correction\|finds false' CHANGELOG.md` returns nothing. Guards `test_rulebook_names_the_on_demand_pass` and `test_readme_names_the_pass` pass.
- Consistency gate: `cairn_validate.py` all checks passed. Verify on the review head: scripts, hooks, and skills suites exit 0; plugin validate passes; marketplace validate passes with no `plugins[N].version` warning; `claude plugin test` 2018 pass, 0 fail. CHANGELOG has an Unreleased entry with no milestone number (`grep -c M270 CHANGELOG.md` is 0). No DESIGN.md principle changed, so `cairn_impact` is skipped.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: a second Amend shows no table, so a `correct` or `compress` named there has no shown line — fix now, fixed 7c79b987 (every Amend round re-shows new lines).
- diff-bug #2: `correct` needs no evidence, so a disputed lesson can be rewritten — fix now, fixed 7c79b987 (its reason quotes evidence; D-178).
- diff-bug #3: guest reads use `ls` on a ref, and `cairn/` is untracked there — fix now, fixed 7c79b987 (`git cat-file -e` at the ref, `cairn/` on disk, reachable commit).
- diff-bug #4: D-177 Context carries a derived count — fix now by D-178 clause (1), fixed 7c79b987 (D-177 not edited, D-175 precedent).
- diff-bug #5: the new `corrected YYYY-MM-DD` mark differs from `corrected M75` and leaves an existing mark unstated — fix now in the skill, fixed 7c79b987; the rulebook example is rejected for change (false: it is an example, not the only form).
- diff-bug #6: "refuted premise" listed as not applying while `refuted` is an exit — fix now, fixed 7c79b987 (the five exits replace the default classes).
- diff-bug #7: owner-mode commit message names exits without evidence — fix now, fixed 7c79b987.
- diff-bug #8: D-177 says evidence always makes a lesson leave or be corrected, but pins and live milestones keep it — fix now by D-178 clause (5), fixed 7c79b987.
- diff-bug #9: D-177 heading says annotates D-051 though it narrows it — fix now by D-178 clause (3), fixed 7c79b987.
- diff-bug #10: D-177 falsifier misses the plan-gate one — fix now by D-178 clause (6), fixed 7c79b987.
- diff-bug #11: order of `correct` against a live-milestone `keep` unstated — fix now, fixed 7c79b987 (a pin or live milestone keeps first; the stamp names a false one).
- diff-bug #12: an `obsolete` commit has no guest reachability rule — fix now, fixed 7c79b987.
- diff-bug #13: an Amend `keep` has no reason — fix now, fixed 7c79b987 (`kept at the gate`).
- diff-bug #14: the rulebook reads as six exits — fix now, fixed 7c79b987 ("three drop exits"); rulebook re-seeded to 719 lines / 69,644 bytes at the three sites.
- diff-bug #15: this repo's LESSONS.md header lists only the review-hygiene exits — reject (false: the header does not say "only", and the file is 108 bytes under its budget).
- diff-bug #16: CHANGELOG reasons read as facts — fix now, fixed 7c79b987 (one list of five reasons).
- diff-bug #17: rulebook, README, and some skill sentences unpinned — fix now, fixed 7c79b987 (guards and registry entries added, `assertNotIn` for the removed `keep` sentence).
- diff-bug #18: D-177 Context fragment — fix now by D-178 clause (2), fixed 7c79b987.
- blame-history #1: a `refuted` drop deletes a false lesson, which D-177 calls D-045's correction — fix now by D-178 clause (4), fixed 7c79b987; the drop itself is a planned change (question set).
- blame-history #2: the stamp for a flagged false lesson was removed — fix now, fixed 7c79b987 (restored for a lesson kept by a pin or live milestone).
- blame-history #3: D-051's two-criteria sentence not marked narrowed — fix now by D-178 clause (3), fixed 7c79b987.
- blame-history #4: "only" dropped from the compress rule — fix now, fixed 7c79b987.
- blame-history #5: two mark forms — same as diff-bug #5, fixed 7c79b987.
- blame-history #6: near-cap figures not derived in D-177, and this repo's file trips the warning — reject (planned change: the derivation is in this file's work log, and D-entries carry no derived measurements).
- blame-history #7: `planner test` beyond D-108's trigger — reject (planned change: the user asked for it as part of the fix for a file at its caps, and D-177 names the trigger).
- blame-history #8: seed note lost the M267 and M268 history — reject (style: the note names the prior seed, and git holds the rest).
- blame-history #9: CHANGELOG fragments; README omits the planner and near-cap parts — CHANGELOG fixed 7c79b987 with diff-bug #16; README part rejected (planned change: the criteria audit kept the README cell short).
- prior-review #1: CHANGELOG wording unpinned, as on PR #275 — reject (style: release prose stays unpinned, the PR #275 disposition under D-109).
- prior-review #2: the pass now reverses M263's keep-false and ownership dispositions — reject (planned change: D-177 at the user's choice).
- prior-review #3: Copilot's header thread may be stale — handled by the Copilot line below.
- prior-review #4: the work log states two rulebook sizes — reject (false as a defect: the work log is append-only, and the later line supersedes).
- copilot: cairn/milestones/M270-lessons-triage-drops.md:14 (record the PR URL in the header) — fix now, fixed 9cc062e7; replied and resolved.
- copilot: review body — noted (its one item is the thread above).
- Copilot level: unknown, since the review body has no effort line (set by GitHub's settings).
- Verify after the fixes (head 7c79b987): scripts, hooks, and skills suites exit 0; both plugin validates pass with no version warning; `claude plugin test` 2018 pass; `cairn_validate` all checks passed. Defect-return count 0, amendment-return count 0.
