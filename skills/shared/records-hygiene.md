# Records hygiene (candidates, decisions, compression, gate discipline)

Read this whenever you are at a milestone hygiene or plan gate — pruning or
graduating a ROADMAP candidate, superseding a decision, compressing a capped
tracking file, placing a new records rule, amending a plan mid-implementation,
or reading a review scorer's output. It is a module of `tracking-rules.md`
(D-031: doctrine gets a module, not a rulebook section; D-055: a matured lesson
family graduates whole into one), conditionally read at the moment the craft
applies, so it costs nothing to a session not at such a gate.

It exists because these are the records operations that fail quietly — a
candidate row advertising shipped work as pending, a compression pass that
saved no lines, an acceptance criterion that drifted from what shipped. Each
line here was learned by shipping the mistake, and both review lenses usually
caught it, not the author.

## 1. Candidate rows graduate at completion, never at plan

**A ROADMAP candidate whose scope a milestone absorbs is NOT pruned when that
milestone is planned.** Candidates graduate at *completion* — the row stays
through planning and implementation and is removed in the post-merge hygiene
pass. Prune it at plan time and the ROADMAP advertises shipped work as still
pending for the whole life of the branch; leave it and the graduation is a
single deliberate step where the work actually lands. Both review lenses flag
a row a milestone already fulfilled but left standing.

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

## 3. Placing a new records rule, and applying it to your own output

**A new rule's home is decided by "would a repo with NO numeric work need
this?"** A universal rule — one every adopting repo needs regardless of domain
— belongs in the core rulebook, not in a conditionally-read domain module like
`validation-doctrine.md`; filing it in the domain module makes it invisible to
exactly the non-numeric sessions the rule governs. D-031's
universal-vs-domain-conditional boundary is the test; apply it before choosing
where the sentence lands.

**A milestone that ships a records rule runs that rule over the artifacts the
milestone ITSELF authors.** The new rule's first test case is the milestone's
own output — the pages it backfills, the tracking lines it writes — and the
classic failure is a compliance fix that commits the very category its own new
rule forbids. Check the milestone's own diff against the rule before shipping
it.

## 4. Amending the plan without letting it drift from what shipped

**When implementation improves on a planned output token or format, amend the
acceptance criterion through the implement gate in that same task** — do not
let the plan text drift from the string actually delivered. Review checks the
criteria as written and correctly fails a milestone that shipped something
better than, but different from, what the AC promised; "better" is still drift.
The amendment gate (`/milestone-implement` step 6) exists for exactly this, and
using it keeps plan and delivery in one voice.

## 5. Reading a review scorer's output

**A sub-threshold confidence score gates the ACTIONED list, not the operator's
judgment.** Read every sub-80 finding's substance rather than trusting the cut,
and treat any finding that authorizes an outward-facing irreversible action as
worth fixing regardless of score — the scorer once dropped "the fallback closes
a contributor's PR with no approval gate" at 48 on a false equivalence between
opening your own PR (reversible) and closing someone else's (not).

**The scorer's *reasoning* can be wrong while its number is defensible.** It
refuted a real finding by crediting a token that did match, when the case
actually failed on a different missing piece — so verify a refutation against
the implementation before accepting it, never against the scorer's own account
of the implementation.

## 6. Compressing a capped tracking file

**Only removing a whole *wrapped* physical line lowers a line count.** A shorter
sentence that still wraps to the same number of physical lines saves nothing,
so when a file is over its cap, cut content — drop a clause, a redundant
example, a whole item — rather than rephrase. Rephrasing to "tighten" a capped
file is the commonest wasted pass.

**Compress what your phase OWNS, and cross-reference a durable record instead of
restating it.** When a cap breakdown ranks a section your phase may not touch
as the heaviest, the growth to cut is almost always your own — review evidence
you added, not the plan-owned Scope the breakdown named. Cut there, and replace
any restated durable content (a `DECISIONS.md` entry, an archived summary) with
a one-line cross-reference to it; a milestone restating a record it could cite
is the classic overrun.
