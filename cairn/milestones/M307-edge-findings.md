# M307: Reject review findings that only unusual inputs reach

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — changes how `/milestone-review` settles findings in every repo that uses cairn
- **Branch/PR:** m307-edge-findings · https://github.com/jmgirard/cairn/pull/321

## Goal

`/milestone-review` rejects a real finding that only an unusual input reaches and that gives no wrong result.

## Scope

**In:** `skills/milestone-review/SKILL.md` step 5 gains a fourth reject ground, `edge`, in owner and guest mode. The
Review-section line format names it. README.md's "Ship it" paragraph says a real finding can be rejected as `edge`. A
D-entry records the ground. The trigger is maintainer review on easystats PRs: datawizard #730 and #726, and
bayestestR #794. On #730, about 20 fix-now items for unusual inputs added helpers and help text. The maintainer said
the code was hard to review and the help was too long.

**Out:** `/hotfix` keeps its four triage options, because the user settles each item there. The Copilot module
inherits the ground through "the skill's rule" and needs no edit. A severity vocabulary for findings stays on the
candidate row "Grade findings by the action they need".

## Acceptance criteria

- [ ] AC1: In `skills/milestone-review/SKILL.md` step 5, the reject bullet names a fourth ground, `edge`. The ground
      covers a finding that the agent judges real, whose defect only an input outside both the deliverable's documented
      use and its common use reaches, and whose effect is an error, a warning, or slow running. The bullet says that a
      finding is never `edge` when its effect is a wrong result with no error or warning. The bullet also says that a
      finding is never `edge` when it demonstrates an acceptance criterion failing.
- [ ] AC2: In the same step, the Review-section line format names `edge` among a reject's grounds, beside false,
      style, and planned change.
- [ ] AC3: README.md's "Ship it" paragraph says that a real finding that only an unusual input reaches, with no wrong
      result, can be rejected with the reason `edge`.
- [ ] AC4: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3

## Tasks

- [x] T1: Edit `skills/milestone-review/SKILL.md` step 5 (the reject bullet near line 381 and the line format near
      line 402) for AC1 and AC2. Keep the text short.
- [x] T2: Edit README.md's "Ship it" paragraph (near line 725) for AC3.
- [x] T3: Append a D-entry: the `edge` ground, its trigger, and its falsifier. It passes D-108's door on the
      narrowing carve-out, because it narrows the fix-now rule. Run the five `verify` commands.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a change to how review settles findings, with a design decision.
- 2026-10-21: idea vet: one concern, that a real bug on an unusual input stays unfixed. Answer at the question set: build it in both modes. Wrong results and failed criteria are never `edge`.
- 2026-10-21: question set: edge findings in which modes — both modes.
- 2026-10-21: plan gate chose a new reject ground over a new disposition, because a reject already logs the finding with its reason and needs no candidate row; falsified by edge rejects that later need a candidate row to be fixed.
- 2026-10-21: plan gate chose both modes over guest only, at the user's choice; falsified by a merged owner-mode defect on a documented or common input traced to an edge reject.
- 2026-10-21: criteria audit (full, fresh Opus reader): 12 findings over M307–M309. For M307: added the failed-criterion exclusion and "outside both" (AC1); replaced the grep criterion with the README site (AC3); dropped the prose-guard criterion per D-109; cited the verify slot in full (AC4); the D-108 door goes to the D-entry task.
- 2026-10-21: collision check: D-108 (narrowing carve-out), D-110 (reviewers rank, agent settles) and D-112 stand; the candidate row "Grade findings by the action they need" stays apart.
- 2026-10-21: inbox sweep: no open issues or PRs in this repo.
- 2026-10-21: implement: T1 to T3 done (step 5 ground and line format, README Ship-it sentence, D-205); verify five commands green; untracked cairn-probe.log and tsconfig.json left unstaged; the simple-english lint flags about 400 existing hits in SKILL.md and README.md outside the edits, left as is.
- 2026-10-21: claim audit: 7 claims read, 2 corrected — README.md (the edge sentence now names warnings, slow running, both use bounds, and the criterion exclusion, and is framed as the exception to the fix rule).

## Decisions

## Review
