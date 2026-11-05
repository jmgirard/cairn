# M337: Re-rate a row whose trigger fired

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes what a `/cairn-triage` pass proposes to users
- **Branch/PR:** m337-rerate-fired-trigger, https://github.com/jmgirard/cairn/pull/352

## Goal

When `/cairn-triage` finds that a candidate row's promotion trigger has fired, it moves the row to the rung it judges right and proposes `promote`, and so `[high]`, only when it judges the work wanted now.

## Scope

**In:** `skills/cairn-triage/SKILL.md` step 2: the Staleness class stops sending a fired trigger to Readiness; the Readiness class stops counting a fired trigger alone as the ground for `promote`; the Rung class says what a parked row whose condition has held takes. README.md's ladder paragraph and a CHANGELOG entry. One D-entry superseding D-228's Readiness clause. Prose guards for the new sentences.

**Out:** D-179's rule that a promote writes `[high]` stays as it is (the user's words). `/milestone-review`'s post-merge unpark step already moves a readied row to normal and is unchanged. The `/cairn-triage lessons` pass's `promote` is a different disposition and is unchanged.

## Acceptance criteria

- [x] AC1: In `skills/cairn-triage/SKILL.md` step 2, the Staleness class says that it does not fire on a row whose trigger has fired and whose work is still undone, so it decides nothing for that row, which goes on to the classes below it. It no longer sends that row to Readiness. `git grep -n "goes to Readiness" -- skills README.md` returns no match.
- [x] AC2: The Readiness class in the same step no longer holds "because its trigger has fired", and it says that a fired trigger alone does not make the work wanted now: a proposed `promote` names in its reason what the pass read that shows the work is wanted now, beyond the trigger firing. The sentence does not bind a `promote` the user sets at *Amend*.
- [x] AC3: The Rung class in the same step says that a `[parked]` row whose promotion condition has held, that no class above proposes for a disposition other than `keep`, `compress`, or `retitle`, and that the Rung class does not propose for `route` or `drop`, is proposed for a priority change off parked to the rung the pass judges right, or for staying parked with a new condition that has not held, with a reason. It names normal as the usual rung. The new sentence leaves every hold and filter that step 2 already applies to that row in force (the started-token, PR-named, live-milestone, merge-survivor, and finding-absorbing holds, and the kept-mark filter).
- [x] AC4: README.md's ladder paragraph says that when a parked row's condition has held, `/cairn-triage` moves it off parked to the rung it judges right, that the held condition alone does not bring `[high]`, and that a promote does. CHANGELOG.md's Unreleased section has an entry saying the same.
- [x] AC5: `cairn/DECISIONS.md` gains one entry that supersedes D-228's clause "a fired trigger whose work is still undone now goes to Readiness instead", states that D-179's promote-to-`high` rule stands, and states how D-108's door applies.
- [x] AC6: Read with four planted candidate rows on subjects no real row covers, each trigger planted as an in-repo fact that Staleness detects (a file or an archived milestone), the branch's step 2 decides them so: (P1) a `[parked]` row whose condition has held, with nothing read saying the work is wanted now, is not required to take `promote` and must move off parked or take a new condition, normal and low both allowed; (P2) the same with a record dated after the row asking for the work now allows `promote`; (P3) a `[parked]` row whose condition has not held is not required to move; (P4) a `[low]` row whose trigger has fired, with nothing saying the work is wanted now, is not required to take `promote`. A fresh-context reader checks this, quoting the deciding sentence for each row on main and on the branch; on main P1 and P4 route to Readiness, whose `promote` carries the change to `high`.
- [x] AC7: The verify slot is clean on the review head: `python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T6

## Tasks

- [x] T1: Edit `skills/cairn-triage/SKILL.md` step 2: the Staleness sentence (AC1), the Readiness class's ground (AC2), and a Rung class sentence for a parked row whose condition has held (AC3). Keep the step-3 sentence "A row whose condition has held usually moves up, as in `priority: parked → normal`" and check that step 3 and the close block say nothing that still ties a fired trigger to `promote`.
- [x] T2: Add prose guards in `skills/tests/test_candidate_priority_token.py` for the three new sentences, with entries in `skills/tests/test_mutation_harness.py`, giving the "when this applies" half of each its own entry; hand-run `python3 -m unittest discover -s skills/tests`, the existing `TestPromoteCarriesHigh.test_readiness_class_states_it` case included.
- [x] T3: Add the README.md sentence (AC4) and the CHANGELOG.md Unreleased entry; grep README and the skills for the old phrasing first.
- [x] T4: Append the D-entry (AC5).
- [x] T5: Spawn a fresh-context Opus reader with main's and the branch's `skills/cairn-triage/SKILL.md` and the four planted rows, each with the record it rests on (AC6). Also run a read-only dry run of the branch's step 2 over this repo's `cairn/ROADMAP.md`, stopping at the table with the open-PR read taken as empty, and log which rows the changed classes reach.
- [x] T6: Run the verify slot (AC7).

## Work log

- 2026-11-05: tier check: milestone — it changes what `/cairn-triage` proposes and needs a decision superseding a D-228 clause.
- 2026-11-05: idea vet: no gap or flaw. A parked row waits on a condition, and a held condition ends the wait without saying how important the work is; review hygiene's unpark step already moves such a row to normal. The change also reaches a normal or low row whose trigger fired, by the same rule.
- 2026-11-05: collision check: D-228 set "a fired trigger whose work is still undone now goes to Readiness instead" (superseded here, T4); D-179 and D-184 stand; no candidate row, live milestone, or archived milestone covers this; inbox sweep found no open issue or PR.
- 2026-11-05: lessons used: 2026-07-24 (M112), 2026-08-17 (M148), 2026-08-22 (M152), 2026-08-30 (M165), 2026-10-30 (M326), 2026-10-30 (M327), 2026-11-02 (M329).
- 2026-11-05: question set: none posed — the user chose the change ("Yes, plan it") after the diagnosis, and no open choice is the user's alone.
- 2026-11-05: approach: the fired-trigger row goes on to the Rung class; rejected: keeping it in Readiness and letting `promote` carry a rung other than `high`, because D-179 ties a promote to `high` and the user asked that it stay. Falsified if a pass leaves rows whose trigger fired on parked, or a user cannot tell a ready row from a re-rated one.
- 2026-11-05: criteria audit (full, Opus): 10 findings. Taken: AC1 says Staleness does not fire; AC2 removes the old ground and leaves Amend free; AC3 names every hold and allows a new condition; AC4 drops the false "only when it promotes"; AC6 states the branch's text with the reader as the check, plants in-repo triggers, softens main's expectation, and adds P4. AC5 had none. The hand-run guard check went to T2.
- 2026-11-05: T1 done: Staleness no longer fires on a fired-trigger row, Readiness drops the fired-trigger ground and binds only the pass's proposal, Rung names the two changes for a parked row whose condition held; step 3 and the close block needed no change. My new sentences carry no simple-english lint hit (file 221 hits, main 222).
- 2026-11-05: T2 done: `TestFiredTriggerReRated` (11 tests, two of them `assertNotIn` on the removed phrases, which main's text holds) and 9 mutation entries, one per positive sentence; hand-run `skills/tests` 1025 tests OK.
- 2026-11-05: T3 done: README ladder paragraph and a CHANGELOG Unreleased entry; old phrasing ("goes to Readiness", "because its trigger has fired") grepped in README and skills, no other site. Lint counts equal main's for both files.
- 2026-11-05: T4 done: D-243 supersedes D-228's Readiness clause; D-179 stands; outside D-108's door by its carve-out.
- 2026-11-05: T5 planted-row reader (fresh Opus): main sends P1, P2, P4 to Readiness and `high`; the branch requires P1 to leave parked or take a new condition, allows `promote` for P2 only, requires no move for P3, and requires no promote for P4. It found that "one of two changes" left no `route` or `drop` for a parked held row, and that a low row (P4) can keep a held condition's text.
- 2026-11-05: substantive amendment: AC3 adds "and that the Rung class does not propose for `route` or `drop`", so the Rung class keeps those two for a parked row whose condition held; the skill sentence now says the class can route or drop such a row, and D-244 corrects D-243's "one of two" clause. Goal unchanged.
- 2026-11-05: re-audit: AC3 (full) — 4 findings: D-243's clause contradicts (taken, D-244); use one wording for the class (taken, "the class"); AC6 P1 silent on route or drop (answered: a route or drop also leaves parked, so P1 holds as written); two guards anchor the old phrase (taken, re-anchored, plus a guard and a mutation entry for the route-or-drop clause).
- 2026-11-05: P4's held-condition gap on a normal or low row filed as the parked candidate "Drop a held condition from a row"; widening AC3 to non-parked rows was not taken.
- 2026-11-05: T5 ROADMAP dry run (fresh Opus, step 2 to the table, open-PR read empty): 35 rows, no trigger judged fired, so neither changed class is reached on this repo; proposals were one retitle, one compress, rest keep. Its five notes on unclear text (drift "bites", a trigger waiting on unplanned work, one clause with two arms, §7 and Out deferrals, split by title or row) concern unchanged wording and are left.
- 2026-11-05: T6 done: scripts/tests, hooks/tests, both plugin validates, and `claude plugin test` (2466 pass) exit 0; after the AC3 amendment the two suites, both validates, and skills/tests (1026 OK) reran green; the branch changes nothing under `hooks/`.
- 2026-11-05: claim audit: 16 claims read, 3 corrected — CHANGELOG.md, README.md, skills/cairn-triage/SKILL.md (the old behavior overstated as every fired row; README stated a proposal as an action and left out the stay-parked option; the stay-parked option had no apply text, so steps 3 and 4 now say the new condition replaces the held one in place). The re-read found all three hold and asked that the replacement keep its position, taken.
- 2026-11-05: implement done; skills/tests 1026 OK, scripts/tests and hooks/tests exit 0 after the last edits; lint counts on the three changed docs equal or below main's.
- 2026-11-05: review pass 1: Copilot arm opened PR #352 and requested Copilot (pending); four lenses spawned; 23 findings: 11 fixed in 64560f98 (with D-245), 2 to candidate rows, 10 rejected; no return.

## Review

Evidence (pass 1, head 346b2032, fixes in 64560f98):

- AC1: `git grep -n "goes to Readiness" -- skills README.md` exit 1, no match; step 2 (whitespace collapsed) holds "is not a drop. Staleness does not fire on that row, so it decides nothing for it, and the row goes on to the classes below".
- AC2: step 2 lacks "because its trigger has fired" and holds "A fired trigger alone does not make the work wanted now", "A proposed `promote` names in its reason what the pass read that shows the work is wanted now, beyond the trigger firing", and "This binds the pass's proposal, not a `promote` the user sets at *Amend*".
- AC3: step 2's Rung class holds "Among those rows, the class can route or drop a `[parked]` row whose promotion condition has held", "If it does neither, it proposes one of two changes for that row, each with a reason", "The first is a priority change off parked to the rung the pass judges right, usually normal", "The second keeps the row parked with a new condition that has not held", and the holds sentence naming all five holds and the kept-mark filter; the fix adds "A row that one of them holds takes only what that hold or filter allows".
- AC4: README.md:419-425 says triage proposes moving the row off parked to the rung it judges right, usually normal, that "The held condition alone does not bring `[high]`. A promote does."; CHANGELOG.md's first section (Unreleased) holds the entry "A row whose trigger fired is re-rated, not always promoted" saying the same.
- AC5: D-243 quotes "a fired trigger whose work is still undone now goes to Readiness instead" as superseded, states "D-179's rule that a promote writes `[high]` stands", and states the door; D-245 corrects that Door to split the removal (carve-out) from the added rules (retained trigger).
- AC6: fresh Opus reader at 346b2032, main and branch, P1 to P4: branch P1 decided by Rung, promote not allowed on the trigger alone, must leave parked (high, normal, low), take a new condition, or be routed or dropped; P2 Readiness allows promote on the M330 record; P3 `keep`, no move required; P4 promote not allowed, no change required; main sends P1, P2, P4 through Staleness to Readiness, whose promote carries `→ high`. The fix commit changes none of the sentences the reader quoted as deciding (diff 346b2032..HEAD checked).
- AC7: on 346b2032, scripts/tests (446, 21 skipped), hooks/tests (212), both `claude plugin validate`, and `claude plugin test` (2466 pass) exit 0; after 64560f98, scripts/tests, hooks/tests, and both validates exit 0 again; the branch changes nothing under `hooks/`. Hand-run skills/tests: 1031 OK.
- Gate: `cairn_validate.py` all checks passed; no DESIGN principle changed, so `cairn_impact` skipped; profile consistency-gate checks are the verify checks above.

spawned: diff-bug, blame-history, prior-review, ripple

- diff-bug #1: Staleness decides nothing for a fired row, so its other faults (refuted premise, dead citation) get no drop or compress — follow-up, parked row "Let Staleness see a fired row's other faults" (main did the same through Readiness)
- diff-bug #2: README pronoun "removes it" now reads as the promote — fix now, fixed 64560f98
- diff-bug #3: a kept parked row whose condition held is forced to a condition change every pass — fix now, fixed 64560f98 ("takes only what that hold or filter allows")
- diff-bug #4: declining a stay-parked condition writes no kept mark — fix now, fixed 64560f98
- diff-bug #5: what a held row takes is unclear (PR-named riders) — fix now, fixed 64560f98 (same sentence as #3)
- diff-bug #6: replacement anchors on `promote when` wording — fix now, fixed 64560f98 ("however the row words it"); the short-title case — reject, edge: a condition inside a short title is outside the documented row shape, and the next pass re-rates the row
- diff-bug #7: D-243's Door claims the carve-out for added rules; D-244 has no Door — fix now, fixed 64560f98 (D-245)
- diff-bug #8: the reason cell has no replace form, so guest mode loses the held text — fix now, fixed 64560f98 (`condition: <held condition> → <new condition>`)
- diff-bug #9: a split of a parked held row copies the held condition — follow-up, absorbed into parked row "Drop a held condition from a row"
- diff-bug #10: the scope clause "Among those rows," has no mutation entry — fix now, fixed 64560f98
- diff-bug #11: README and CHANGELOG leave out route or drop — fix now, fixed 64560f98
- diff-bug #12: D-243's Context overstates "came out `[high]`" — fix now, fixed 64560f98 (D-245)
- diff-bug #13: CHANGELOG wraps early — reject, style
- blame-history #1: the Rung class can drop a parked held row, against D-228's "not a drop" — reject, false: D-228 bars dropping a row because its trigger fired and keeps *not worth keeping* for any row
- blame-history #2: a normal or low fired row can now be dropped by Rung — reject, false: main's Rung class could already drop a row Readiness passed over
- blame-history #3: removing "because its trigger has fired" reverses M271's reading — reject, planned change
- blame-history #4: the step 3 and 4 replacement sentences have no guard — fix now, fixed 64560f98
- prior-review #1: the two `assertNotIn` tests have no mutation entry — reject, false: blanking text cannot fail an absence assert; both fail on main's text (T2)
- ripple #1: the Staleness ground list names a fired trigger — reject, false: the same bullet's qualifier carves it out, as on main
- ripple #2: tracking-rules "The token goes when the condition holds" — reject, false: after the replacement the row's condition is the new one, which has not held
- ripple #3: "the promote itself is the reason" against the new promote reason — reject, false: that sentence governs the `→ high` cell, not the promote's own reason
- AC6 reader note: rows spell "Promote when" with a capital — reject, style (covered by #6's fix)
