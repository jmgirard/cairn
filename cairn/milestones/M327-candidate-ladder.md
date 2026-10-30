# M327: Let triage move a row to any rung

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP3, GP1
- **Resolves:** —
- **Surface tier:** user-facing — it changes what `/cairn-triage` proposes and how skills write candidate rows in every adopting repo
- **Branch/PR:** m327-candidate-ladder, https://github.com/jmgirard/cairn/pull/340

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

- [x] AC1: The "Candidate priority token" paragraph of `skills/shared/tracking-rules.md` states the ladder in order and says that a move can cross any number of rungs. It says that whoever writes or updates a row places it on a rung with a reason, that only parked needs a condition, and that a skill can propose a Known issues entry or no row at its own gate. Its writer sentence names the parked rung alone, and it no longer says that every finding row states a condition.
- [x] AC2: In `skills/milestone-review/SKILL.md`, step 5's `follow-up` places each row on a rung, with the parked default above, and lets review propose a Known issues entry. The snapshot follow-up and the PR-conversation follow-up no longer say "with step 5's promotion condition". Step 7's merge question lists each Known issues proposal. Step 9's limitations bullet says that approving the merge with the proposal listed is the acceptance. `skills/copilot-review/SKILL.md` no longer says "The row states its promotion condition" and points to the rulebook paragraph.
- [x] AC3: Step 2 of `skills/cairn-triage/SKILL.md` lets the pass propose any rung for any row not held at `keep`, up or down by any number of rungs, with a reason. A move to parked drafts a condition. A move off parked needs no held condition. These seven sentences are present in the plan commit's file and absent at the head, each searched with `tr '\n' ' ' | tr -s ' '` and `grep -c -F`: "A `[high]` row is never proposed `→ parked`", "only the No condition class below proposes it", "The class never leaves such a row `keep` with no change", "The trigger has fired and the work is wanted now", "A candidate with no promotion condition that describes a limitation the repo lives with", "a Known issues entry that is really deferred work moves to a candidate row with a stated trigger", and "and it comes before the grounds above". Step 2's finding-absorbing options and records-hygiene §7 also allow a rung change.
- [x] AC4: The `drop` row of step 2 lists four reasons: refuted premise, already shipped, rejected on principle, and not worth keeping. *Not worth keeping* applies to any row not held at `keep`. Its reason quotes what the row would do or fix and says why that is not worth the work. Step 5 still writes the pass's decision entry for it.
- [x] AC5: Step 3 writes ` — kept YYYY-MM-DD` at Accept on a candidate row that the user set to `keep` at Amend after the pass proposed a move. The mark goes where step 4 puts a merge survivor's lineage clause, so the short title stays the same. A newer mark replaces an older one. The kept mark is a sixth carve-out from the untouched rule. The skip test, the size count, the stamp, and the status line each name it. Step 2 proposes no move for a kept row unless its reason names a record, change, or report dated after the mark, and the `keep` reason names the mark's date. `compress`, `merge`, and `split` keep the mark.
- [x] AC6: A fresh subagent runs steps 1 to 3 read-only, under both the plan commit's skill and the head's skill. It uses copies of this repo's `cairn/ROADMAP.md` and `cairn/DESIGN.md` at the plan commit, with six planted rows. P1 is `[high]` with a condition far from holding. P2 is `[parked]` with an unheld condition and a dated user report in its text. P3 is `[low]` with a kept mark dated before an archived milestone that bears on it. P4 is untagged with a kept mark dated today. P5 is untagged wanted work with no condition, on a subject no other row covers. P6 is untagged and names a cosmetic flaw. The open-PR read is taken as empty, and each run stops at the table. After the table, the reader reports for each skill whether it allows the pass to propose five things: P1 moved to parked, P2 moved up while its condition has not held, P3 moved despite its kept mark, P5 left at its rung with no condition, and P6 dropped as not worth keeping. The reader also reports whether the skill requires the pass to propose a condition and parked for P5. The head's skill allows all five and does not require the P5 proposal. The plan commit's skill does not allow P1 moved to parked or P5 left with no condition, and it requires the P5 proposal. Under the head's skill, P4 has no move. The reports are recorded in the Review section.
- [x] AC7: A D-entry supersedes D-227's forced-condition clauses for finding rows and for triage rows, its *not worth keeping* limits, and its `[high]` exclusion. It narrows D-184's writer rule to the parked rung. It annotates D-027 and D-134 and states how each part passes D-108's door. `README.md` and `CHANGELOG.md` describe the ladder and the kept mark. The guards that pin the removed sentences pin the new ones instead. The `verify` slot, `skills/tests`, and `scripts/cairn_validate.py` pass.

## Coverage

- AC1 → T1
- AC2 → T1, T6
- AC3 → T2, T6
- AC4 → T2
- AC5 → T3, T6
- AC6 → T5
- AC7 → T1, T4, T5

## Tasks

- [x] T1: Write the D-entry. Rewrite the rulebook paragraph. Edit review steps 5, 7, and 9 and the two follow-up sentences, `skills/copilot-review/SKILL.md:88-90`, and records-hygiene §7.
- [x] T2: In triage step 2, state the ladder, remove the seven gate sentences, open every move, widen *not worth keeping*, and let the finding-absorbing options take a rung change.
- [x] T3: Wire the kept mark through steps 2 to 7.
- [x] T4: Update README and CHANGELOG. Re-pin the guards on the removed sentences, and re-seed the `/milestone` rulebook mass at its three sites.
- [x] T5: Run AC3's grep and AC6's two dry runs, then `verify`, `skills/tests`, and `cairn_validate`.
- [x] T6: Fix review return 1 (triage step 4's route, review's Known issues record, guest acceptance) and the diff-bug fix-now findings logged in the Review section.

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
- 2026-10-30: claim audit: 58 claims read, 2 corrected — CHANGELOG.md and README.md ("Review can also propose a Known issues entry" now names `/milestone-review` alone). Also from its note, the rulebook's parked sentence now says the token goes when a re-rate moves a row off parked. The rulebook-mass seed was re-seeded to 853 / 84,443.
- 2026-10-30: T5 dry runs (fresh Opus, plan-commit ROADMAP and DESIGN with six planted rows). Under the head skill: P1 high → parked, P2 promoted, P3 promoted (its kept mark yielded to M326, dated after it), P4 no move (retitle only), P5 kept as a merge survivor, P6 dropped (refuted premise, since the planted misspelling is not in the file). Under the plan-commit skill: P1 keep, P5 kept as a survivor too, because the planted P5 overlapped the real row "State the close count in guest text". P5 was re-planted on a subject with no overlap and re-run under both skills. Ambiguities fixed: a fired trigger whose work is undone goes to Readiness, not a drop; a same-day record is not after a kept mark; `compress` and `retitle` are not moves.
- 2026-10-30: re-audit: AC6 (full) — first reader: the P1 contrast had no clear referent; P1, P2, P3, and P6 bound judgments the head skill allows but does not require; the answers come after the table; a Known issues probe was missing. Fixed by allows/requires reports. The P7 probe was declined toward the narrower promise, since AC3's grep covers that removed sentence.
- 2026-10-30: re-audit: AC6 (full) — second reader: claims match both skill texts. Findings answered with no wording change: P5 is planted as a feature, so the plan commit's drop test cannot take it; recording P4's table row and quoting the deciding sentences are review's procedure; the P2 contrast and a P7 probe would widen the promise, so they are declined. This is the criterion's one re-entry.
- 2026-10-30: substantive amendment: AC6 now checks what each skill version allows or requires for the planted rows, not which judgment a reader makes. The old wording "P5 is not moved to parked and gets no condition" bound a judgment that the ladder leaves free; the head-skill reader parked P5 by judgment, which D-228 allows. The deliverable the user sees is unchanged, so no stop.
- 2026-10-30: verify green on T4 head ae5d72db: scripts/tests 0, hooks/tests 0, both plugin validates 0, plugin test 0 (2466 pass).
- 2026-10-30: T6 done (review return 1): triage step 4's route up writes the named rung's token and a condition only for parked; review step 5 records a Known issues proposal as a `known issue` Review line with its text, step 7 lists it verbatim, and step 9 writes it from that line on the owner merge or the guest handoff approval. Also fixed: the kept mark filters §7 options and merge absorption, the chip and Accept name kept marks, a survivor takes the newest absorbed mark, the rulebook defines the mark and tells every writer to keep it, the Rung class heading and retitle wording, "a rung by step 5's rule", the hold list in README, CHANGELOG, and D-228, the CHANGELOG route sentence, and the test comment. Rulebook-mass re-seeded to 855 / 84,618. verify, `skills/tests`, and `cairn_validate` green.

## Decisions

## Review

- 2026-10-30: Copilot arm: PR #340 opened at review start (feature cap read 0), header recorded and pushed. The request exited 0, but the state query still read `none`: "Copilot request on PR #340 may not be recorded by GitHub (used-up Copilot credits are one cause)". No second request.
- AC1: tracking-rules 252-266 read whitespace-joined: the ladder in order, "a move can go up or down any number of rungs", "places it on a rung and states the reason", "A row on the parked rung states that condition … a row with no condition is valid at high, normal, or low", and "A skill that files a row can instead propose a Known issues entry, or no row, at its own gate". The old writer sentence and the "every finding row states" sentence are gone. Met.
- AC2: review 414-420 places each row on a rung with the parked default and lets review propose a Known issues entry; 562 and 617 read "on step 5's rung"; 511 lists Known issues proposals at the merge question; 955 takes merge approval as acceptance; copilot-review 89-90 points to the ladder. `git grep` for "step 5's promotion condition" and "The row states its promotion condition" over `skills` finds 0. Met.
- AC3: the seven gate sentences, searched in whitespace-joined text with `grep -c -F`, read 1 each at a455c2d6 and 0 each at the head. Step 2's Rung class proposes any rung, up or down by any number of rungs, with a reason; a move to parked drafts a condition and a move off parked needs none held. The §7 options (triage 481) and records-hygiene 47 add a rung change. Met.
- AC4: whitespace-joined greps find "Its reason is one of four classes", the *not worth keeping* text ("the pass judges that what the item would do or fix is not worth the work; the reason quotes that text from the item and says why, and it applies to any item not held at `keep`"), and step 5's "is *rejected on principle* or *not worth keeping*" trigger for the decision entry. Met.
- AC5: whitespace-joined greps find each kept-mark site once: the Amend write at Accept, the sixth carve-out, the skip test, the lineage-clause placement with replacement of an older mark, `compress`/`merge`/`split` keeping it, the size count, the stamp, the status line, and step 2's "unless its reason names a record, a change, or a report dated after the mark. Its `keep` reason names the mark's date". Met.
- AC6: fresh Opus run on the head at c2ceaf3d and on the plan commit's skill, over the plan-commit ROADMAP and DESIGN with six planted rows (P5 on a subject no other row covers), open-PR read empty, stopped at the tables. Reports, each quoting its deciding sentence: head allows P1 → parked ("the pass can propose any rung it judges right, up or down by any number of rungs"), P2 up with its condition unheld ("A move off parked needs no condition that has held"), P5 left with no condition ("A row with no condition can stay at high, normal, or low"), and P6 dropped as not worth keeping; head does not require the P5 condition and parked. For P3 the reader answered "no, unless dated evidence exists" and weighed only M259 and M284. The skill's rule allows the move when "a record, a change, or a report dated after the mark" bears on the row, and one exists: M326's merge 4ce186e7 (2026-10-30, after the 2026-10-01 mark) added the `condition: +` reason-cell form to the triage table, the format P3's condition names (`git show 4ce186e7 -- skills/cairn-triage/SKILL.md`). The T5 run moved P3 on that record. So the head allows P3's move. Plan commit: does not allow P1 → parked ("A `[high]` row is never proposed `→ parked`"), does not allow P5 left with no condition ("The class never leaves such a row `keep` with no change"), and requires the P5 condition and parked. Under the head, P4 has no move (its shipping record ee268c3b predates the mark) and takes only a retitle. Met.
- spawned: diff-bug, blame-history, prior-review, ripple
- prior-review #1: *not worth keeping* is widened past M326's effect test — reject, planned change (AC4, D-228, the user's ladder answer)
- prior-review #2: a `[high]` row can be re-parked, reversing M284's fix — reject, planned change (AC3, D-228)
- prior-review #3: the "unless it already opens with `[parked]`" clause from M326 is gone, so a parked row could be proposed `→ parked` — fix now, the Rung class says a row already on the judged rung takes no priority change, fixed b796a2e1
- prior-review #4: the Rung class lost M326's live-milestone skip — fix now, restated in the class, fixed b796a2e1
- prior-review #5: a move off parked no longer needs a held condition, loosening M284's unpark rule — reject, planned change (AC3, D-228)
- prior-review #6: copilot-review no longer states the parked default — reject, false: it points to the rulebook paragraph, which states it
- blame-history #1: dropping "A `[high]` row is never proposed `→ parked`" undoes M284's fix, and D-228 did not name it; a parked move could reuse a condition that held — fix now, D-228 names the M284 rule, and the drafted or kept condition must not have held
- blame-history #2: *not worth keeping* can drop a wrong-result row, against D-205's principle — fix now in part: D-228 says D-205 still governs review rejects and a triage drop of such a row is the user's call at the gate; the drop itself is a planned change
- blame-history #3: *not worth keeping* now reaches Known issues entries, and step 5's decision-entry text said "the effect its row named" — fix now, the text reads "what it would do or fix" in step 5 and the guest stamp; the reach is a planned change (dropped is the rung below Known issue)
- blame-history #4: declining a proposed move to parked writes no kept mark, so it returns next pass — fix now, that decline writes the mark; *Apply nothing* writing none is a planned change, since it changes no file
- blame-history #5: D-149 rejected filing unfixed findings as Known issues, and D-228 did not name it — fix now, D-228 narrows D-149; the "or no row" option is a reject, which review already logs (IP3)
- blame-history #6: merge approval now accepts listed Known issues entries — reject, planned change (AC2, D-228)
- blame-history #7: promote no longer needs a fired trigger — reject, planned change (AC3)
- blame-history #8: any later dated change ends a kept hold — reject, planned change (AC5)
- blame-history #9: route can move a Known issues entry back up — reject, planned change (AC3)
- blame-history #10: copilot-review states no default — reject, false, as prior-review #6
- ripple #1: the Unreleased CHANGELOG entry from M284 still said whoever adds a row writes `[parked]` when its condition does not hold — fix now, it points to the ladder entry
- ripple #2, #3: step 5 and the guest stamp said "the effect its row named" — fixed in cbbd30a7 (blame-history #3)
- ripple #4: step 3 said a *not worth keeping* reason "quotes the effect the row names" — fix now, it quotes what the item would do or fix and why
- ripple #5: step 2's §7 vocabulary defined `route` as one-way to Known issues — fix now, it names the way back
- ripple #6: step 3 named only trigger nearness as the ground for a priority change — fix now, any reason the cell states can serve
- ripple #7: `/milestone`'s untouched-rows chip offered only promote, keep, drop — fix now, it adds a move to another rung
- ripple #8: records-hygiene §7 and review step 9 still say "accepted" limitations — reject, false: review step 9's next sentence makes the merge approval that acceptance
- ripple #9: `compress` said the trigger always survives, though a row can now have none — fix now, "where the row states one"
- ripple #10: step 5's no-entry list omitted kept marks — fix now
- ripple #11: `/milestone-plan` uses "kept row" for a row a trivial edit leaves in place, which collides with the kept mark — reject, style: a term in another context, no rule conflict
- diff-bug #1: triage step 4's `route` of a Known issues entry still writes a stated trigger and no rung token, against step 2's route row — fix now, floor return (load-bearing)
- diff-bug #2: review's Known issues proposal is recorded nowhere a resumed or guest step 9 can read — fix now, floor return (load-bearing)
- diff-bug #3: in guest mode no merge approval exists to accept a proposed Known issues entry — fix now, floor return (load-bearing)
- diff-bug #4: §7's options bypass the kept mark — fix now
- diff-bug #5: the chip and *Accept as proposed* do not name kept marks — fix now
- diff-bug #6: the rulebook does not define the kept mark, so other row writers can lose it — fix now
- diff-bug #7: `/milestone`'s stale-row chip — fixed in 1677d118 (ripple #7)
- diff-bug #8: step 3's "quotes the effect the row names" — fixed in 1677d118 (ripple #4)
- diff-bug #9: a proposed Known issues entry is not shown verbatim before approval — fix now
- diff-bug #10: README, CHANGELOG, and D-228 overstate and leave out what holds a row — fix now
- diff-bug #11: a kept row can be merged away, and an absorbed row's mark is not carried — fix now
- diff-bug #12: no-entry list omits kept marks — fixed in 1677d118 (ripple #10)
- diff-bug #13: the kept mark sits in the class list though it filters every class — fix now
- diff-bug #14: the Rung class says "classes above" propose `retitle`, which comes from Title below — fix now
- diff-bug #15: the Rung class heading leaves out `route` — fix now
- diff-bug #16: "on step 5's rung" reads as one fixed rung — fix now
- diff-bug #17: `/copilot-review` has no gate for a Known issues proposal — reject, false: the rulebook says a skill "can" propose one at its own gate, so a skill with none files a row
- diff-bug #18: search-first still asks an alternative-approach row for a condition — reject, false: such a row waits on evidence, so it sits on the parked rung, consistent with the ladder
- diff-bug #19: the CHANGELOG's "before" sentence misstates what changed for routes — fix now
- diff-bug #20: D-228's door calls M326 shipped while its CHANGELOG entry is unreleased — reject, false: the default branch is the distribution channel (tracking-rules git model), and M326 merged there
- diff-bug #21: the AC6 amendment weakened the criterion with no stop — reject, planned: logged as a substantive amendment with two re-audits; the deliverable is unchanged, so no stop is owed, and the merge question shows it
- diff-bug #22: records-hygiene line 47 runs past the wrap — reject, style
- diff-bug (c): the "# M327: …" test comment is narrative history — fix now; the CHANGELOG claims lacking prose guards — reject, false: the profile's test-doctrine makes skill-prose guards owed by nothing (M323)
- review return 1: diff-bug #1 (triage step 4 route forces a trigger and no rung token), #2 (review's Known issues proposal not recorded for step 9), and #3 (guest mode has no acceptance event for a proposed Known issues entry)
- housekeeping: the ripple reader left `/private/tmp/claude-501/ct_m327.md`, outside the repo; a safety check blocked its delete, and it is left for the user, not deleted on the reader's request
- pass 2 (head d8a74471, after review return 1): Copilot re-requested on PR #340, state still `none`, not recorded.
- pass 2 AC1-AC5: the same whitespace-joined greps re-run on d8a74471 each read 1 for the rulebook ladder sentences, review's rung, default, `known issue` disposition, Known issues listing, and guest/owner acceptance, and for triage's four-class drop row, the any-item *not worth keeping*, the step 5 entry trigger, and every kept-mark site. The removed review phrases read 0, and the seven gate sentences read 0 (1 each at a455c2d6, unchanged). Boxes stay ticked on this fresh evidence.
- pass 2 AC6: the deciding sentences that the pass-1 report quoted are re-found on d8a74471, each reading 1: "the pass can propose any rung it judges right, up or down by any number of rungs", "A move off parked needs no condition that has held", "A row with no condition can stay at high, normal, or low", the kept-mark "dated after the mark" rule, and "A record dated the same day as the mark is not after it". The plan commit's skill is unchanged. The T6 edits do not touch the allow or require answers, so the report stands.
- pass 2 AC7 and gate: T6 head d8a74471 ran verify green (scripts 0, hooks 0, both validates 0, plugin test 0), `skills/tests` 0, and `cairn_validate` all checks passed. D-228 supersedes and narrows as AC7 states. README and CHANGELOG describe the ladder and the kept mark. The guards pin the new sentences. No `plugins[N].version` warning.
