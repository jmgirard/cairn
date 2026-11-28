# M244: Turn on the Copilot round in the easystats checkouts, and name the line when Copilot reviews a PR with the round off

**Status:** done (2026-10-11, PR #254 https://github.com/jmgirard/cairn/pull/254)

**Goal:** The six easystats guest checkouts run the Copilot round, and four named `/hotfix` and `/milestone-review` closes name the opt-in line when Copilot is on a PR that the round covers but the round is off.

**Outcome:** `/hotfix` skipped Copilot in easystats because only this repo
carried `# Copilot review: on`. The line now sits in the local, uncommitted
`cairn/PROFILE.md` of correlation, insight, modelbased, parameters,
performance, and see. `copilot-review.md` §1 gains "Off but present": with
the round off, `/hotfix` step 7 and its step 6 guest close, and
`/milestone-review` step 10 and its step 8 guest close, run §3's query once
on a covered PR. On `pending` or `reviewed` the recap ends with one line
naming the PR and the line to set. A later request goes unreported. README,
CHANGELOG, and DESIGN describe it.

**Decisions:** none promoted. The question set chose the line plus a note
over handling threads with the round off, and the six easystats checkouts.
The plan chose the rule in §1 with four pointers over four copies.

**Review:** claim audit, 18 claims, 5 corrected. Three lenses, 26 findings:
11 fixed (note wording, the timing caveat, DESIGN), 14 rejected, 1 to "Late
Copilot requests with the round off (M244 review)". Copilot did not review
(quota limit). Nothing retired.
