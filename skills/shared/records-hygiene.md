# Records hygiene (candidates and decisions)

Read this whenever you are at a milestone hygiene or plan gate — pruning or
graduating a ROADMAP candidate, or superseding a decision. It is a module of
`tracking-rules.md`, conditionally read at the moment the craft applies, so it
costs nothing to a session not at such a gate.

Budget, per the maturation exit's module-budget rule (retrofitted 2026-08-22,
M154): **under 55 lines and under 4,000 bytes**, set from the retrofitted
size (44 lines / 2,575 bytes) plus roughly one section of headroom, hand-read
with `wc -l -c` at the repo's hygiene passes and covered by no validator.
Over either figure, compress or retire content here — never "let it grow".

## 1. Candidate rows graduate at completion, never at plan

**A ROADMAP candidate whose scope a milestone absorbs is NOT pruned when that
milestone is planned.** Candidates graduate at *completion* — the row stays
through planning and implementation and is removed in the post-merge hygiene
pass. Prune it at plan time and the ROADMAP advertises shipped work as still
pending for the whole life of the branch; leave it and the graduation is a
single deliberate step where the work actually lands.

## 2. Superseding a decision, and sweeping the archive for one

**The plan-time collision sweep greps `milestones/archive/` for *decisions*,
not only `DECISIONS.md` and the candidate rows.** A milestone-local decision
recorded in an archived milestone file (with no `DECISIONS.md` entry) is
invisible to a sweep that reads only the two obvious homes, and a later
milestone reverses it without ever citing it.

**A milestone-local decision is superseded in the same milestone-local form.**
`DECISIONS.md` is history IP4 forbids editing, so a choice first recorded
inside a milestone file is overturned by a new milestone-local entry that names
and supersedes it — not by editing the original, and not by a `DECISIONS.md`
entry that silently outranks a record it never mentions.

## 7. A finding-absorbing candidate row is dispositioned, not silently extended

**A candidate row already carrying deferred review findings filed from two or
more distinct milestones (named in its provenance or weighed notes) is not
silently extended again.** The hygiene pass about to extend it — the
`/milestone` health audit or `/milestone-review`'s post-merge pass — poses a
disposition chip: promote a bounded milestone for the items that guard shipped
behavior; route items the user accepts to `cairn/DESIGN.md` Known issues (the
review skill's accepted-limitations block); prune the rest; extend once more
as an explicit choice, never the default. "Extended" means gaining a new
provenance or weighed note without a disposition; compressing the row to meet
a byte budget never substitutes for the disposition.

<!-- Remainder ledger (M146 trim; git holds the full pre-trim text —
     `git log -- skills/shared/records-hygiene.md`): §3 dropped with the
     rule-placement doctrine; §4 lives in its consumer, /milestone-implement
     step 6; §5 retired with its subject at M145; §6's surviving remedy
     lives in tracking-rules "Weight caps". Section numbers stay stable. -->
