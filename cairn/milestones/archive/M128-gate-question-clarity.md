# M128: Gate questions lead in plain words

**Status:** done (2026-07-31, PR #128 https://github.com/jmgirard/cairn/pull/128)

**Goal:** Rewrite the accessible-language rule from adjectives into a stated
two-sentence shape with a worked example, so gate questions are readable
without cairn's internal vocabulary.

**Outcome:** The tracking-rules "Accessible language on the decision surface"
bullet now states the two-sentence test (first sentence: the decision in
plain words; second: what happens on each choice; both before any term of
art), bans D-/RR-/BC-ids, IP/GP numbers and section numbers from question
text and option labels (`M<NN>` exempt — operator's own referent), mandates
verbatim same-session capture of any prompt the user flags as unclear, and
carries a worked Bad/Good pair (Bad is a labeled reconstruction, not a
capture). Four guard tests (12 asserts), seven mutation-registry entries;
"never a gate" survives as author judgment (D-059's shape kept).

**Decisions:** none milestone-local; the plan-gate choices (M-id exemption,
reconstruction over capture) live as work-log falsifier lines.

**Review:** 34 findings, 6 actioned ≥80 and fixed on branch (record counts
O9/O12; guard-coverage gaps O6/O8/O10/O25 — object-less pins, first-line-only
blockquote pins); 24 logged sub-80, top: two-sentence predicate is
question-shaped while labels stay under the plain-words sentence (78).
