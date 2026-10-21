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

- [x] AC1: In `skills/milestone-review/SKILL.md` step 5, the reject bullet names a fourth ground, `edge`. The ground
      covers a finding that the agent judges real, whose defect only an input outside both the deliverable's documented
      use and its common use reaches, and whose effect is an error, a warning, or slow running. The bullet says that a
      finding is never `edge` when its effect is a wrong result with no error or warning. The bullet also says that a
      finding is never `edge` when it demonstrates an acceptance criterion failing.
- [x] AC2: In the same step, the Review-section line format names `edge` among a reject's grounds, beside false,
      style, and planned change.
- [x] AC3: README.md's "Ship it" paragraph says that a real finding that only an unusual input reaches, with no wrong
      result, can be rejected with the reason `edge`.
- [x] AC4: `skills/milestone-review/SKILL.md` step 8's guest arm says that when it opens the PR, the body lists,
      before the `Closes`/`Refs` lines, each Review-section reject whose ground is `edge`, one short line each in plain
      words with no cairn vocabulary, then asks the maintainers whether they want those inputs handled in this PR or
      later. With no `edge` rejects it adds neither. When the PR is already open, the arm says that no body edit is
      made and the close block names any new `edge` rejects.
- [x] AC5: The `verify` slot of `cairn/PROFILE.md` is green at the branch head: its five commands, each exit code
      checked.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T5
- AC5 → T3, T5

## Tasks

- [x] T1: Edit `skills/milestone-review/SKILL.md` step 5 (the reject bullet near line 381 and the line format near
      line 402) for AC1 and AC2. Keep the text short.
- [x] T2: Edit README.md's "Ship it" paragraph (near line 725) for AC3.
- [x] T3: Append a D-entry: the `edge` ground, its trigger, and its falsifier. It passes D-108's door on the
      narrowing carve-out, because it narrows the fix-now rule. Run the five `verify` commands.
- [x] T4: Add a CHANGELOG.md entry under "Changes that affect existing repos" for the `edge` ground (review return 1).
- [x] T5: Add the guest PR-body list of `edge` rejects to step 8's guest arm, a CHANGELOG sentence, and a D-206 clause; rerun the five `verify` commands.

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
- 2026-10-21: review return 1: consistency gate — CHANGELOG.md has no entry for the edge ground (the plan listed no changelog task).
- 2026-10-21: minor amendment: added T4 for review return 1; CHANGELOG.md entry written.
- 2026-10-21: user request at review: in guest mode, keep edge findings out of the PR's code but note them briefly in the PR body with a question to the maintainers; a new criterion goes to a fresh re-audit before it is written.
- 2026-10-21: re-audit: AC4 (full) — five findings: the open-PR path, the source of "each", the empty case, placement before the Closes/Refs lines, and a D-entry owed; wording narrowed to the reader's proposal, which re-enters once.
- 2026-10-21: re-audit: AC4 (full) — three findings (Copilot-round edge rejects after the body, ground-less copilot and conversation lines, the baseline for "new"); the criterion stays as audited, and the skill text answers all three: reviewer lines only, the close block names any edge reject the body leaves out, "new" means after the newest earlier step-7 approval line.
- 2026-10-21: substantive amendment: AC4 added at the user's request (guest PR body notes edge rejects and asks the maintainers); verify criterion renumbered AC5; T5 added and done.

- 2026-10-21: step-7 approval: m307-edge-findings approved for merge
## Decisions

## Review

Evidence, 2026-10-21, branch head 68d555ae on origin/main cb214128 (not moved since the cut):

- AC1: step 5's reject bullet reads "A fourth ground is `edge`: a real defect the diff adds that only an input outside both the deliverable's documented use and its common use reaches, whose effect is an error, a warning, or slow running", and "A finding is never `edge` when its effect is a wrong result with no error or warning, when it shows an acceptance criterion failing or wrong, or when it authorizes an outward-facing irreversible action."
- AC2: step 5's line format reads "its ground — false, style, planned change, or edge — included".
- AC3: README's "Ship it" paragraph reads "One exception: a real finding that only input outside both documented and common use reaches is rejected as `edge` when its effect is an error, a warning, or slow running. A wrong result or a failed acceptance criterion is never `edge`."
- AC4: step 8's guest arm reads "When it opens the PR, the body lists, before any `Closes`/`Refs` lines, each Review-section reject whose ground is `edge` … with no cairn vocabulary", then asks the maintainers, adds neither with no `edge` rejects, and on an open PR makes no body edit while the close block names them.
- AC5: at 68d555ae, scripts/tests 445 tests OK, hooks/tests 193 tests OK, plugin validate exit 0, marketplace validate exit 0 with no `plugins[N].version` warning, `claude plugin test .` exit 0.

Consistency gate (68d555ae): `cairn_validate.py` all checks passed (one advisory sizing warning on M308); no principle changed, so no `cairn_impact`; CHANGELOG Unreleased has the `edge` entry with no milestone number; skills/tests prose guards OK.

spawned: diff-bug, blame-history, prior-review, ripple (first pass, head b58349f1)
- diff-bug #1 / blame-history #1 / ripple #1: an `edge` reject skipped the return floor's load-bearing arm — fix now, fixed a9913e03 (an `edge` defect is not load-bearing).
- diff-bug #2: `edge` could absorb amendment returns — fix now, fixed a9913e03 (never `edge` when a criterion fails or is wrong).
- diff-bug #3: the PR-conversation read could reject a human's request as `edge` — fix now, fixed a9913e03.
- diff-bug #4 / blame-history #2: D-205 did not name D-144 — fix now, fixed a9913e03 (D-206 annotates D-144).
- diff-bug #5: D-205's hotfix reason was partly false — fix now, fixed a9913e03 (D-206).
- diff-bug #6: `edge` had no evidence standard — fix now, fixed a9913e03 (the reason names the input and the use).
- diff-bug #7: `edge` rejects were not shown verbatim at the merge question — fix now, fixed fb71d9dd.
- diff-bug #8 / blame-history #4 / prior-review #1 / ripple #2: no exception for outward irreversible actions — fix now, fixed a9913e03.
- diff-bug #9: `edge` could leak onto a guest PR — reject, false: the Copilot module's replies already carry no cairn vocabulary.
- diff-bug #10: no new failure path in guest, fork, dirty-tree, first-run, or moved-remote cases — noted.
- blame-history #3 / prior-review #3: the D-108 door claim — reject, false: the change narrows the fix-now rule, the carve-out D-108 names; D-206 adds the shipped-behavior trigger.
- prior-review #2: D-205 misstates the mechanism — reject, false: "at the user's choice" refers to the mode choice.
- ripple #3: README's "rejects a false one" names one ground — reject, style: README summarizes.
spawned: diff-bug, blame-history, ripple (second pass, on b58349f1..7853a975 after the user's AC4 amendment; prior-review not re-run, since the first pass found no prior-review evidence on these files)
- diff-bug #1, #2, #3: the open-PR baseline could not be computed, and maintainers never saw rejects on an open PR — fix now, fixed 68d555ae (one PR comment for this review pass's `edge` rejects).
- diff-bug #4: no `Closes`/`Refs` lines on some PRs — fix now, fixed 68d555ae ("before any").
- diff-bug #5 / ripple #3: Copilot rejects carry no ground — fix now, fixed 68d555ae (the Copilot example was dropped; Copilot rejects get their own GitHub reply).
- diff-bug #6: an earlier pass's `edge` rejects may be stale at the pushed head — reject, edge: only a floor return followed by a fresh PR reaches it, and the effect is an extra line in the PR body.
- diff-bug #7, #8: D-206's heading and falsifier — fix now, fixed 68d555ae.
- diff-bug #9, #10 / ripple #1, #2: CHANGELOG and README wording — fix now, fixed 68d555ae.
- diff-bug #11 / ripple #2: README lacks the new exclusions — reject, style: README summarizes; the guest note was added.
- diff-bug #12: "one short line" versus host style — reject, false: the host-text rule governs all host text.
- diff-bug #13: lens name and rank could leak — fix now, fixed 68d555ae.
- diff-bug #14: no new failure path in the five cases — noted.
- blame-history #1: D-144 has no superseded line — reject, false: DECISIONS is append-only, and D-206's annotation is how a later entry changes it.
- blame-history: M308 will shorten the same PR body — noted for M308.
- ripple #4: "nothing cairn writes reaches the repo's maintainers" — reject, false: it means the `cairn/` records.
- ripple #5: the close block's listed contents — fix now, fixed 68d555ae (the arm names them).
- claim audit (implement): 7 claims read, 2 corrected (README).
- copilot: README.md:729 — fix now, fixed b58349f1.
- copilot: cairn/milestones/M307-edge-findings.md:69 — fix now, fixed b58349f1.
- copilot: cairn/DECISIONS.md:7457 — fix now, fixed 1ec7f046.
- copilot: review body — noted (summary reply posted).
- Copilot level: Lite (set by GitHub's settings).
