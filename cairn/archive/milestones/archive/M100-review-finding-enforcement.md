# M100: Review-finding enforcement — findings travel verbatim, outcomes meet projections

**Status:** done (2026-07-20, PR #98 https://github.com/jmgirard/cairn/pull/98)

**Goal:** An RR's binding findings reach the merge gate unsoftened — verbatim
criteria, shown deviations, projections beside outcomes (RR04 rec 8).

**Outcome:** RRs emit numbered `BC<n>` Binding criteria (brief template);
the constrained milestone names its `Driving RR:` (new header slot) and
carries each criterion verbatim in its AC block or in a shown "Deviations
from RR<NN>" table — enforced by the new hard `binding criteria` check,
which strips HTML comments, word-bounds the table marker, and fails loud on
unparseable sections or slots. Review and the merge chip must juxtapose
measured-vs-projected with an explicit accept-shortfall option; the
rulebook gains the adjudication-asymmetry and script-measurable-AC rules.

**Decisions:** implement-gate: header slot over an AC marker; deviations
table inside the AC section; whitespace-normalized matching; strict default
tolerance. Merge-gate: rulebook delta read as net +4 vs ≤4 (gross +5/−1 shown).

**Review:** diff-bug lens found 4 fail-open paths — F1 92 comment-hidden
deviations, F2 92 unparseable-section no-op, F3 85 RR5/RR50 marker, F4 78
malformed slot (sub-threshold, fixed with the cluster) — all fixed, 6
regression tests, 5 proven red pre-fix. Blame-history and prior-PR lenses
clean (the latter's 16th recorded no-op). No lessons retired.
