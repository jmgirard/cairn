# M327: Let triage move a row to any rung

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3, GP1
- **Resolves:** —
- **Surface tier:** user-facing — it changes what `/cairn-triage` proposes and how skills write candidate rows in every adopting repo
- **Branch/PR:** m327-candidate-ladder

## Goal

Triage and every skill that writes or updates a candidate row can propose any place on one ladder, with a reason, and the user decides.

## Scope

**In:**
- The ladder, top to bottom: high, normal, low, parked (a condition that has not held), Known issue, dropped. A move can cross any number of rungs. A row with no condition is valid at high, normal, or low. Only parked needs a condition.
- The rulebook's "Candidate priority token" paragraph states the ladder. Whoever writes or updates a row places it on a rung with a reason. A skill can also propose a Known issues entry or no row at its own gate.
- `/milestone-review` places each follow-up row on a rung by judgment. The default for a finding that no documented or common use reaches is parked with "promote when a user reports it". Review can propose a Known issues entry. The merge question lists it, and approving the merge accepts it.
- `/cairn-triage` step 2 can propose any rung for any row not held at `keep`, from any rung. The moves are a priority change among high, normal, low, and parked, a `route` either way, a `drop`, or a `promote`. A move to parked drafts a condition. A move off parked needs no held condition. Seven gate sentences go (AC3). A finding-absorbing group also takes a rung change.
- *Not worth keeping* applies to any row not held at `keep`. Its reason quotes what the row would do or fix and says why that is not worth the work.
- A kept mark, ` — kept YYYY-MM-DD`, written at Accept when the user sets `keep` at Amend on a proposed move. A kept row gets no move unless its reason names a record, change, or report dated after the mark.
- One D-entry, README, CHANGELOG, re-pinned guards, and the `/milestone` rulebook-mass seed.

**Out:**
- Review's post-merge unpark step stays as it is. It runs with no gate, so a wider move waits for `/cairn-triage`.
- `/hotfix`, `/milestone-implement`, and `/milestone-plan` get no edits of their own. They follow the rulebook paragraph.
- A Known issues entry carries no kept mark.

## Acceptance criteria

- [ ] AC1: The "Candidate priority token" paragraph of `skills/shared/tracking-rules.md` states the ladder in order and says that a move can cross any number of rungs. It says that whoever writes or updates a row places it on a rung with a reason, that only parked needs a condition, and that a skill can propose a Known issues entry or no row at its own gate. Its writer sentence names the parked rung alone, and it no longer says that every finding row states a condition.
- [ ] AC2: In `skills/milestone-review/SKILL.md`, step 5's `follow-up` places each row on a rung, with the parked default above, and lets review propose a Known issues entry. The snapshot follow-up and the PR-conversation follow-up no longer say "with step 5's promotion condition". Step 7's merge question lists each Known issues proposal. Step 9's limitations bullet says that approving the merge with the proposal listed is the acceptance. `skills/copilot-review/SKILL.md` no longer says "The row states its promotion condition" and points to the rulebook paragraph.
- [ ] AC3: Step 2 of `skills/cairn-triage/SKILL.md` lets the pass propose any rung for any row not held at `keep`, up or down by any number of rungs, with a reason. A move to parked drafts a condition. A move off parked needs no held condition. These seven sentences are present in the plan commit's file and absent at the head, each searched with `tr '\n' ' ' | tr -s ' '` and `grep -c -F`: "A `[high]` row is never proposed `→ parked`", "only the No condition class below proposes it", "The class never leaves such a row `keep` with no change", "The trigger has fired and the work is wanted now", "A candidate with no promotion condition that describes a limitation the repo lives with", "a Known issues entry that is really deferred work moves to a candidate row with a stated trigger", and "and it comes before the grounds above". Step 2's finding-absorbing options and records-hygiene §7 also allow a rung change.
- [ ] AC4: The `drop` row of step 2 lists four reasons: refuted premise, already shipped, rejected on principle, and not worth keeping. *Not worth keeping* applies to any row not held at `keep`. Its reason quotes what the row would do or fix and says why that is not worth the work. Step 5 still writes the pass's decision entry for it.
- [ ] AC5: Step 3 writes ` — kept YYYY-MM-DD` at Accept on a candidate row that the user set to `keep` at Amend after the pass proposed a move. The mark goes where step 4 puts a merge survivor's lineage clause, so the short title stays the same. A newer mark replaces an older one. The kept mark is a sixth carve-out from the untouched rule. The skip test, the size count, the stamp, and the status line each name it. Step 2 proposes no move for a kept row unless its reason names a record, change, or report dated after the mark, and the `keep` reason names the mark's date. `compress`, `merge`, and `split` keep the mark.
- [ ] AC6: A fresh subagent runs steps 1 to 3 read-only, under both the plan commit's skill and the head's skill. It uses copies of this repo's `cairn/ROADMAP.md` and `cairn/DESIGN.md` at the plan commit, with six planted rows. P1 is `[high]` with a condition far from holding. P2 is `[parked]` with an unheld condition and a dated user report in its text. P3 is `[low]` with a kept mark dated before an archived milestone that bears on it. P4 is untagged with a kept mark dated today. P5 is untagged wanted work with no condition. P6 is untagged and names a cosmetic flaw. The open-PR read is taken as empty, and each run stops at the table. Under the head's skill, P1 is proposed down, P2 up, and P3 a move. P4 has no move. P5 is not moved to parked and gets no condition. P6 is proposed for a drop or a move down, and every non-`keep` reason is stated. Under the plan commit's skill, P1 and P5 get other results. The two tables are recorded in the Review section.
- [ ] AC7: A D-entry supersedes D-227's forced-condition clauses for finding rows and for triage rows, its *not worth keeping* limits, and its `[high]` exclusion. It narrows D-184's writer rule to the parked rung. It annotates D-027 and D-134 and states how each part passes D-108's door. `README.md` and `CHANGELOG.md` describe the ladder and the kept mark. The guards that pin the removed sentences pin the new ones instead. The `verify` slot, `skills/tests`, and `scripts/cairn_validate.py` pass.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T2
- AC5 → T3
- AC6 → T5
- AC7 → T1, T4, T5

## Tasks

- [x] T1: Write the D-entry. Rewrite the rulebook paragraph. Edit review steps 5, 7, and 9 and the two follow-up sentences, `skills/copilot-review/SKILL.md:88-90`, and records-hygiene §7.
- [x] T2: In triage step 2, state the ladder, remove the seven gate sentences, open every move, widen *not worth keeping*, and let the finding-absorbing options take a rung change.
- [x] T3: Wire the kept mark through steps 2 to 7.
- [x] T4: Update README and CHANGELOG. Re-pin the guards on the removed sentences, and re-seed the `/milestone` rulebook mass at its three sites.
- [ ] T5: Run AC3's grep and AC6's two dry runs, then `verify`, `skills/tests`, and `cairn_validate`.

## Work log

- 2026-10-30: created by /milestone-plan.
- 2026-10-30: tier check: milestone — a design change to triage, review, and the rulebook.
- 2026-10-30: idea vet: gap — which records count as new context for a kept row; reading taken: any record, change, or report the pass read, dated after the mark, with no extra GitHub or git reads. No flaw.
- 2026-10-30: collision check: follows M326 (archived). D-227's forced-condition, *not worth keeping*, and `[high]` clauses are superseded, D-184's writer rule is narrowed, and D-027 and D-134 are annotated. D-108's door: removing gates is the narrowing carve-out. The kept mark and the ladder rule pass on the retained trigger, because M326's shipped rule parked wanted work and brought kept rows back each pass.
- 2026-10-30: inbox sweep: no open issues or PRs on jmgirard/cairn.
- 2026-10-30: lessons used: 2026-10-30 (M326) triage dry run on a real repo; 2026-07-24 (M112, extended M249) doc surfaces; 2026-08-17 (M149) rulebook-mass seed; 2026-08-17 (M148, extended M182) guard pins; 2026-08-22 (M152, extended M287) decision change owes a D-entry.
- 2026-10-30: criteria audit (full mode, fresh Opus, two rounds after the user's ladder answer): round 2 returned 9 findings, all taken. The grep now runs on whitespace-joined text over seven named sentences, each shown present at the plan commit. The kept mark is the sixth carve-out, wired into skip, size, stamp, and status, and placed by the merge rule. The dry-run plants cross the removed gates and run under both skills. Review's two condition sentences and Copilot's are named, and merge approval is the Known issues acceptance. The D-entry narrows D-184 and four D-227 clauses. *Not worth keeping* quotes what the row would do. §7 takes a rung change.
- 2026-10-30: question set: the user chose that triage and every candidate write or update can propose any outcome on the ladder high, normal, low, parked on condition, Known issue, dropped, and that a row can move any number of rungs.
- 2026-10-30: plan gate chose a kept mark over re-proposing a declined move each pass, because the user named re-proposal as the M326 problem; falsified by a kept row that triage wrongly never revisits after a real change.
- 2026-10-30: plan gate chose `ready now` out and plain rungs in, because a normal row with no condition already means ready; falsified by an operator who cannot tell a ready row from one that lacks a decision.
- 2026-10-30: remainder ledger: the ladder and moves in either direction → M327; ready rows → M327, as the normal rung with no condition; kept rows not re-proposed → M327, the kept mark; drop or promote of conditioned rows on new context → M327; record sources for context → M327, reading taken in the idea vet.
- 2026-10-30: branch m327-candidate-ladder cut from main at a455c2d6; untracked `cairn-probe.log` and `tsconfig.json` stay unstaged.
- 2026-10-30: T1 done: D-228. The rulebook paragraph states the ladder and narrows the writer sentence to the parked rung. Review step 5 places rows on a rung and can propose a Known issues entry, the snapshot and PR-conversation follow-ups say "on step 5's rung", step 7 lists rung and Known issues proposals, and step 9 takes merge approval as the acceptance. Copilot's follow-up points to the ladder, and records-hygiene §7 adds a rung move.
- 2026-10-30: T2 done: step 2's No condition class becomes the Rung class (any rung, either way, any distance; parked carries a drafted condition; off parked needs no held condition). Readiness promotes on a judged reason it names, Misfiling routes either way on judgment, *not worth keeping* is a judged reason for any item not held, and §7's options add a rung change. The seven gate sentences read 0 in the whitespace-joined file. A Kept mark bullet sits in step 2; its writing is T3.
- 2026-10-30: T3 done: Amend's `keep` on a proposed move writes ` — kept <today>` at Accept. It is the sixth untouched carve-out and is counted in the skip test, size count, stamp, and status line. It is placed where a merge lineage clause goes, a newer mark replaces an older one, and `compress`, `merge`, and `split` keep it.
- 2026-10-30: T4 done: README's ladder paragraph and triage row, and the CHANGELOG Unreleased entry, which replaces M326's still-unreleased entry with the ladder. Five guards in `test_candidate_priority_token.py` and two harness blocks are re-pinned to the new sentences. The rulebook-mass seed is 852 / 84,399 at its three sites. `skills/tests` and `cairn_validate` are green.

## Decisions

## Review
