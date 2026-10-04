# Records hygiene (candidates and decisions)

Read this whenever you are at a milestone hygiene or plan gate — pruning or
graduating a ROADMAP candidate, or superseding a decision. It is a module of
`tracking-rules.md`, conditionally read at the moment the craft applies, so it
costs nothing to a session not at such a gate.

Budget (maturation exit's module-budget rule, retrofitted 2026-08-22, M154,
from 44 lines / 2,575 bytes plus about one section of headroom): **under 55
lines and under 4,000 bytes**, hand-read with `wc -l -c` at hygiene passes,
covered by no validator. Over either figure, compress or retire content
here — never "let it grow".

## 1. Candidate rows graduate at completion, never at plan

**A ROADMAP candidate whose scope a milestone absorbs is NOT pruned when that
milestone is planned.** Candidates graduate at *completion*: the row stays
through planning and implementation and goes in the post-merge hygiene pass.
Pruned at plan time, the ROADMAP shows shipped work as pending for the life of
the branch. Kept, the graduation is one step where the work actually lands.

## 2. Superseding a decision, and sweeping the archive for one

**The plan-time collision sweep greps `milestones/archive/` for *decisions*,
not only `DECISIONS.md` and the candidate rows.** A milestone-local decision in
an archived file, with no `DECISIONS.md` entry, is otherwise invisible, and a
later milestone reverses it without citing it.

**A milestone-local decision is superseded in the same milestone-local form.**
IP4 forbids editing history, so a new milestone-local entry names and
supersedes it. Never edit the original, and never let a `DECISIONS.md` entry
silently outrank a record it does not mention.

## 7. A finding-absorbing group of candidate rows is dispositioned, not silently extended

**Rows that name each other count as one group.** A candidate row's title is
its text after the `- ` and any `[high]`/`[low]` token, up to the first `: `.
The row and each row that names its exact title in double quotes form its
group, direct references only. A group whose rows together carry deferred
review findings filed from two or more distinct milestones (named in
provenance or weighed notes) is finding-absorbing, and none of its rows is
silently extended again. The `/milestone` audit poses a disposition chip for
the group. `/milestone-review`'s post-merge pass files new findings as a new
row that names the older row's exact title in double quotes after its own
`: `. The chip's options: promote a bounded milestone for the items that guard
shipped behavior, route accepted items to `cairn/DESIGN.md` Known issues (the
review skill's accepted-limitations block), prune the rest, or extend once
more as an explicit choice, never the default. "Extended" means gaining a new
provenance or weighed note without a disposition. Compressing a row for a
byte budget never substitutes for the disposition (M161, M211).

<!-- Remainder ledger (M146 trim, full text in git log): §3 dropped with
     rule-placement, §4 is in /milestone-implement step 6, §5 retired at M145,
     §6's remedy is in tracking-rules "Weight caps". Numbers stay stable. -->
