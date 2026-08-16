# Records hygiene (candidates and decisions)

Read this whenever you are at a milestone hygiene or plan gate — pruning or
graduating a ROADMAP candidate, or superseding a decision. It is a module of
`tracking-rules.md`, conditionally read at the moment the craft applies, so it
costs nothing to a session not at such a gate.

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

<!-- Remainder ledger (M146 trim; git holds the full text at f50136e^):
     §3 (placing a new records rule; running it over the milestone's own
     output) dropped with the rule-placement doctrine — no surviving consumer.
     §4 (amend the AC through the gate rather than drift) already lives in its
     consumer, /milestone-implement step 6. §5 retired with its subject at
     M145. §6 (compressing a capped file) dropped; the surviving remedy lives
     in tracking-rules "Weight caps". Section numbers stay stable. -->
