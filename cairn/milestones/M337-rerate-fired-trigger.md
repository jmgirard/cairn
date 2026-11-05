# M337: Re-rate a row whose trigger fired

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes what a `/cairn-triage` pass proposes to users
- **Branch/PR:** m337-rerate-fired-trigger

## Goal

When `/cairn-triage` finds that a candidate row's promotion trigger has fired, it moves the row to the rung it judges right and proposes `promote`, and so `[high]`, only when it judges the work wanted now.

## Scope

**In:** `skills/cairn-triage/SKILL.md` step 2: the Staleness class stops sending a fired trigger to Readiness; the Readiness class stops counting a fired trigger alone as the ground for `promote`; the Rung class says what a parked row whose condition has held takes. README.md's ladder paragraph and a CHANGELOG entry. One D-entry superseding D-228's Readiness clause. Prose guards for the new sentences.

**Out:** D-179's rule that a promote writes `[high]` stays as it is (the user's words). `/milestone-review`'s post-merge unpark step already moves a readied row to normal and is unchanged. The `/cairn-triage lessons` pass's `promote` is a different disposition and is unchanged.

## Acceptance criteria

- [ ] AC1: In `skills/cairn-triage/SKILL.md` step 2, the Staleness class says that it does not fire on a row whose trigger has fired and whose work is still undone, so it decides nothing for that row, which goes on to the classes below it. It no longer sends that row to Readiness. `git grep -n "goes to Readiness" -- skills README.md` returns no match.
- [ ] AC2: The Readiness class in the same step no longer holds "because its trigger has fired", and it says that a fired trigger alone does not make the work wanted now: a proposed `promote` names in its reason what the pass read that shows the work is wanted now, beyond the trigger firing. The sentence does not bind a `promote` the user sets at *Amend*.
- [ ] AC3: The Rung class in the same step says that a `[parked]` row whose promotion condition has held, that no class above proposes for a disposition other than `keep`, `compress`, or `retitle`, and that the Rung class does not propose for `route` or `drop`, is proposed for a priority change off parked to the rung the pass judges right, or for staying parked with a new condition that has not held, with a reason. It names normal as the usual rung. The new sentence leaves every hold and filter that step 2 already applies to that row in force (the started-token, PR-named, live-milestone, merge-survivor, and finding-absorbing holds, and the kept-mark filter).
- [ ] AC4: README.md's ladder paragraph says that when a parked row's condition has held, `/cairn-triage` moves it off parked to the rung it judges right, that the held condition alone does not bring `[high]`, and that a promote does. CHANGELOG.md's Unreleased section has an entry saying the same.
- [ ] AC5: `cairn/DECISIONS.md` gains one entry that supersedes D-228's clause "a fired trigger whose work is still undone now goes to Readiness instead", states that D-179's promote-to-`high` rule stands, and states how D-108's door applies.
- [ ] AC6: Read with four planted candidate rows on subjects no real row covers, each trigger planted as an in-repo fact that Staleness detects (a file or an archived milestone), the branch's step 2 decides them so: (P1) a `[parked]` row whose condition has held, with nothing read saying the work is wanted now, is not required to take `promote` and must move off parked or take a new condition, normal and low both allowed; (P2) the same with a record dated after the row asking for the work now allows `promote`; (P3) a `[parked]` row whose condition has not held is not required to move; (P4) a `[low]` row whose trigger has fired, with nothing saying the work is wanted now, is not required to take `promote`. A fresh-context reader checks this, quoting the deciding sentence for each row on main and on the branch; on main P1 and P4 route to Readiness, whose `promote` carries the change to `high`.
- [ ] AC7: The verify slot is clean on the review head: `python3 -m unittest discover -s scripts/tests`, `python3 -m unittest discover -s hooks/tests`, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test`.

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
