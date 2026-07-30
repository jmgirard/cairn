# Guard doctrine (prose-guards, fixtures, matchers, validators)

Read this whenever authoring or editing a test that locks prose, a fixture
that feeds one, a matcher that classifies human-written markdown, or a
`cairn_validate` check. It is a module of `tracking-rules.md` (D-031: domain
doctrine gets a module, not a rulebook section), conditionally read at
guard-authoring time, so it costs nothing to sessions that never write a
guard.

It exists because the universal floor in "What gets a test" states the
*obligation* — a guard must fail when the rule it locks is deleted — while
the craft of making an assertion actually falsifiable is judgment the harness
cannot make for you. Everything here was learned by shipping a guard that
passed over the defect it claimed to cover.

## 1. What an assert must pin

**A substring anchor gives false coverage, and prose you add elsewhere can
create one.** Shipping a name that contains an asserted name (`merge_guard` →
`merge_guard_post`) unfalsifies every bare `assertIn` on the shorter name and
blocks its mutation registration. Use word-bounded `assertRegex` (`\bname\b`;
`_` is a word character). The reverse direction bites too: new header prose
adding a second occurrence of an anchored word degrades a bare `assertIn` in
another file — **after adding prose, grep every word an existing guard
anchors on.** Anchor a template field on its own line (`startswith`, column
0), since the field name also occurs in the file's comment header.

**When guarded prose maps a LABEL to a RULE or to a SET, pin the label
together with its members on one physical line.** Pinning only the clause
survives swapping the label elsewhere; pinning only the mechanism sentence
leaves the sets swappable *and* deletable with every assert green. The
harness does not catch this — blanking is not swapping — and registration is
per file, so sound entries elsewhere mask it. A wrapped sentence is the usual
cause: the anchor stops at the line break, before the predicate carrying the
meaning. The clause likeliest to go unpinned is one a mid-implementation gate
amendment added, because every anchor was authored before it existed — re-read
the guard against the acceptance criteria after any amendment.

**Verify by inversion.** Relabel, negate, or transpose the rule in place, run
the suite, require red, restore, and diff. Blanking proves only that the text
is present; inversion is what proves the guard pins the *rule*.

**Fix the wrap, never the assert.** When an anchor breaks because prose
reflowed, re-wrap the prose. Loosening the assert is how a label→rule guard
stops pinning its rule. Author anchors on their own physical line and re-run
the suite after any rewording near one. The one-line demand is scoped to
mutation blocks and label→rule pairings; a plain presence check over prose
that legitimately re-wraps may normalize whitespace instead.

## 2. What the mutation harness does and does not catch

The harness blanks each registered block and asserts its guard fails; a
completeness meta-test reddens on an unregistered guard *file*. So the
mechanics are self-reporting — a registered block that reflowed, duplicated,
or lost its trailing punctuation "found 0"-errors.

What it cannot see:

- **Registration is per file (≥1 exemplar block), never per assertion.** A
  new `assertIn` in an already-registered file still needs its own entry, or
  the by-hand check: would this assertion pass against the pre-milestone
  content? Sound entries elsewhere in the same file mask its absence.
- **Only a positive assertion can be mutation-proven.** An `assertNotIn` is
  satisfied by blanking, so pair every negative guard with a positive framing
  assert and register *that* phrase.
- **It runs a guard as a single method, which skips `setUpClass`.** A guard
  caching its source text at class level reads the unmutated file and reports
  false coverage on itself. Read the target per test (a property or
  `setUp`), never a class-level cache.
- **Blanking is not swapping.** Deletion-resistance says nothing about
  transposition; see the inversion protocol above.

The harness proves a guard reacts to its block; it never judges whether that
block was worth pinning. That judgment is yours before you register it.

## 3. Absence assertions

**A guard whose only assertion is an `assertNotIn` is vacuous against a
crash.** Empty stdout satisfies every absence-assert, so a test stays green
while the command under test exits 1 on every run. Three corollaries, each
learned separately:

- **Pair the absence-assert with a positive signal that the path ran**, and
  assert what the exit code *should* be.
- **The positive signal must prove the work happened**, not merely that
  output appeared — exceptions swallowed to `[]` keep `OK` printing while
  nothing is measured.
- **An absence-assert routed through a filtered channel is unfalsifiable.**
  Assert against the classifier, not the report it feeds.

**Where a report renders one token in several sections, a whole-string
`assertIn` is unfalsifiable** — stripping a row's labels leaves the guard
green. Anchor on the row, then re-verify by stripping exactly what the test
claims to check.

**A detector's matcher must be exercised at every rendering its target can
take.** The positive signal above proves the detector RAN; it never proves the
detector would SEE the thing. A leak detector comparing six characters of
`format(abs(v), digits = 6)` matched about four significant figures, so a real
violation rendered `round(v, 3)` — the codebase's own house style for a number
in a message — passed at zero failures, while the full-precision mutation its
author reached for reddened it. Carry the renderings INTO the test as positive
controls: append the real value at full precision, rounded, and `signif`-ed,
and require the detector to see each one. That is strictly stronger than
external mutation-verification, which proves only that the guard catches the
mutation its author thought of — and the author of a detector is exactly who
cannot enumerate the renderings it misses.

**The renderings vary by site as well as by format.** A number has several
spellings; a message has several *sites* — the branches, message literals, and
code paths at which one target can appear. Exercising every number format of
one literal is not coverage of a surface that has several, and a detector that
survives the format axis fails the site axis next: a leak placed in a one-way
singular lead no control had exercised passed at zero failures over 720 cells,
while that lead shipped in about 4% of real cases.

**A count of enumerated entries is not coverage of renderings.** A detector
asserting `checked == N` over a hand-listed set measures the list, not the
surface, and it passes at exactly the moment a site is missing from the list.
§7's positive-count rule does not reach this: the guard that failed here
counted two, and two was a complete count of the author's list. So **derive the
renderings from the producer rather than listing them** — sweep the producer's
own outputs over a grid of inputs and assert the invariant over what comes back
(a rendered bullet contains no number), which covers renderings not yet
written, with one end-to-end case retained to prove those outputs reach the
real surface unchanged.

## 4. Fixtures

**Vary every axis the prose is free in, and vary it where the value under
test lives.** Decoration is only one axis; fixtures varying it alone pass
vacuously on phrasing and layout. A 36-cell product bought nothing when every
cell wrapped at a split point that left the value before the cut — no cell
wrapped where it changes the answer. A page fixture that always places the
block last makes trailing-paragraph absorption untestable.

**Build the fixture in the shape an author writes, not the shape that makes
the assertion convenient.** Running each member of a taught vocabulary as
`{member} <verb>` hands every member an independent verb, passing on
`spot-checked verified against the source` while the phrasing the templates
actually teach (`spot-checked against the source`, where the qualifier
*overlaps* the verb) classifies wrongly. Where a vocabulary member can
textually collide with the pattern it modifies, one clause shape is not a
test: run several, and assert the failure direction, not only the success
case.

**A fixture helper that defaults an input never tests it.** A two-signal
detector is only as strong as its weaker signal; grep the helper for defaults
before believing a discrimination claim, and give every false-positive
fixture a realistic value on the axis it defends.

**When one task authors content and another authors its checker, add a test
running the real checker over the real artifact.** The fixture copy is not
the artifact. A template is such an artifact, and its pairing test must
*instantiate* it — placeholders satisfy no guard regex.

## 5. Matchers and parsers over human-written markdown

**Tolerate cosmetic decoration on the semantic token.** A hard CHECK parsing
authored markdown must accept backticks, links, and emphasis around the token
it reads; the no-false-positive doctrine binds CHECK parsers, not only scan
heuristics. But widening a capture class admits non-targets too — widen
deliberately, and test both directions.

**Negation is a property of a clause, not a phrase list.** Matching
affirmative verbs against a fixed set of negative *phrases* breaks in both
directions the moment the verb set grows: a false positive on the very prose
that motivated the check, and a clean bill for a record saying in plain words
that it was never verified. When a matcher gains verbs, its negation handling
gains them too, and the negator search is scoped to the verb's own clause.

**A containment-based command guard fails in both directions.** It over-fires
on any command that merely *quotes* the guarded string — a heredoc, an
evidence grep, a debug probe — so author that content with Write/Edit or
assemble the string inside a script file; and it is direction-blind, denying
a legitimate inbound merge. It under-fires by parsing only the first
occurrence: `re.search` on a chained command clears the leading match and
lets the rest through. **When a detection regex graduates from "is this
guarded?" to "is this authorized?", switch to `finditer` and require every
occurrence to clear.**

**A gate and an advisory need opposite protections against one parser.**
Parameterize; never share a widening rule. "A more generous read means
nothing that passed can now fail" is the wrong invariant when the consumer
asks an existence question — a wider read *erases* failures rather than
creating them. More generally: **when a change makes a check fire less, ask
what it was for** — a fix that quiets a detector can destroy its job as a
reminder.

**When a figure is reported under a filter, ask whether it is a
whole-population property.** Filtering the input can make a "share not keyed
to X" 0.0% by construction, so the report announces its own blind spot as
absent. Compute such a share over the unfiltered set and say so; a mode that
cannot honour the filter refuses it rather than ignoring it.

**Two defects in one heuristic can each be safe to fix only because the other
suppresses them.** Before fixing one finding in a shared matcher, check what
closing it *activates* in the others. When they interact, the honest
disposition is a redesign banked with the interaction written down, not a
patch that passes today.

## 6. Restatement, and numbers

**A rule inherited from a prior finding is unverified until read out of the
implementation.** Restating a matcher's behavior into a reference page ships
it wrong; restating a parser into doc prose taught a verb set the parser does
not implement. **Run each member of a documented set through the
implementation, never the set as a whole.** This binds temporal claims (a
`find` hit is not evidence a path moved — one `git log --follow` settles it)
and relocation alike: moving a fact into its owner is a restatement too, so
re-verify each member *after* the move, not before.

**A number fails two ways — derived wrong, and restated stale.**

- **Derive it through the gate's own comparison.** A check failing at
  `n >= cap` means a `<50` cap permits 49, and capacity is `(cap-1) -
  overhead`. Read the operator; never assume the cap is attainable.
- **Restating it is an encoding, so a stated↔enforced coupling test is only
  as wide as the encodings it pairs.** Count every site — including a test's
  own docstring. Cheaper still: let the owning file keep the number and have
  the others name the members instead.
- **An amendment fixing a stale number is itself a restatement.** Re-derive
  from a fresh measurement rather than editing each site from the old value,
  or an "all four sites corrected" claim misses the fifth.

During a review pass that fixes several findings, a number you corrected
early can be re-staled by a later fix in the same pass — settle numeric
records last, after the content has stopped moving.

Name a validate finding by its emitted label in backticks (`coverage
complete`), and write evidence counts from command output, never memory.

## 7. Scoping a sweep or a grep-shaped criterion

**A repo-wide sweep and a grep-shaped acceptance criterion both hit ground
you did not mean.** An exclusion list may name only history files
(`DECISIONS.md`, changelogs, `legacy/`, `reviews/archive/`) — never a live
directory, or the sweep silently skips records that are still read to act on.

**A sweep whose cells may legitimately be silent passes for free on silence.**
Assert per cell that it checked a positive number of things, and assert across
the sweep that the positive case fired somewhere, so universal silence cannot
satisfy it. Stronger still, assert the CONVERSE beside the claim — `named ==
usable` rather than `named ⇒ usable` — which turns a silent cell into an
assertion that nothing admissible would have worked, rather than an assertion
about nothing. A bare `assertGreaterEqual(checked, 0)` is the tautology this
rule exists to name.

**A criterion whose evidence is a grep will hit the milestone's own
artifacts**: the guard's `assertNotIn` (an absence-assert is a hit for the
token it locks), the milestone file's Scope and Tasks, and the ROADMAP
lineage row. Scope the evidence command to the prose surface being fixed, and
exempt the tracking lines in the criterion at plan time — otherwise it needs
a gated amendment at implement.

## 8. The author never certifies its own guard's coverage

**Running a guard and certifying that it covers what you claim are different
jobs, and only the first one survives being done by its author.** Operation
self-corrects: suites, the mutation harness, and the sweeps all report against
the artifact, so an author who runs them finds its own mistakes. Certification
does not, because the author checks the description against its generative
model of the artifact rather than against the artifact — the docstring says
what the file was meant to do, the work-log line says what the fix was meant
to close, and both read as true to the person who formed the intent. A
milestone whose deliverable was a guard once returned from review seven times,
and its seventh return — every suite green, every numeric projection met
exactly, the validator clean — was still two records describing that
milestone's own artifact wrongly.

**So before `status -> review`, a guard-authoring milestone hands the
description layer to a fresh-context [O] reader that authored no part of it.**
The reader checks three things and reports discrepancies verbatim:

- **AC-clause-to-assert coverage** — every clause of every acceptance
  criterion maps to an assert that actually pins it, and no criterion is
  covered only by an assert the author believes covers it.
- **Claim-vs-file accuracy** — every docstring, comment, work-log line, and
  record claim about the guard is true of the file it describes, read out of
  that file rather than out of the milestone's narrative.
- **Anchor-vs-shipped-bytes fidelity** — every multi-word anchor matches the
  bytes actually shipped, including under the target's hard wrap.

The gate is entered at zero unresolved: every discrepancy is fixed, never
argued down as imprecision. Which confirmation that fix then takes depends on
the finding's class, and the classes are set out below — each carries exactly
one. The author still runs everything —
this moves certification, not operation.

**The certified scope is the work and the records describing the work; a record
whose subject is a certification round itself — the final round's own report
included — sits outside it** (D-069). Without this the gate cannot converge
rather than merely being hard to reach: §8 obliges every round to record a
verdict, that record is append-only under IP4, and so each round manufactures
uncertified surface for the next one to audit. M114 pass 8 ran four rounds on
that treadmill — round 4 finding defects only in certification narrative — at
15, 14, 17 and 38 minutes. Zero unresolved stays the bar; what this excludes is
a scope that regresses.

**Two lines govern a round, and they are drawn on different axes.** Collapsing
them into one is what made this section's first attempt at a bound unusable, so
they are stated apart. **What the reader checks and the author fixes** is drawn
by *subject matter*: the work and every record about the work are inside,
narrative about the certifying process is outside (D-069, as narrowed by
D-070). **What a finding reopens** is drawn by *provenance*: a finding is
grounds for a further round unless its only subject is a **fix-authored
record**.

A fix-authored record is a docstring, a comment, a work-log line, or a record
claim that a previous round's own fix wrote in this same certification. That
name is the only one this section gives the class, and where it means anything
wider it says so — the earlier formulation alternated "text" and "record" as if
they were synonyms, and the two readings that licensed were opposite rules. A
fix's code, its asserts and its fixtures are not records and stay ordinary
round-opening surface; so does every record that existed before round 1, since
a false claim in an original docstring is the defect this section was built on
and it reopens a round no matter who wrote it.

The two axes compose rather than compete. A fix-authored record is still read
and still corrected — it never leaves the certified scope, and nothing here
narrows that scope. What it loses is only the power to force another round.
D-070 rules on the first axis and says nothing about the second, which is why
this is compatible with it rather than a partial supersession of it.

**A round reopens only on a finding within the three named checks above.**
Those three are the whole of this step's mandate. A robustness observation that
no acceptance-criterion clause pins — a surviving mutation, a one-directional
pin, a near-miss control's uncovered signature, a fixture weak on an axis no
criterion names — is real work, and it is recorded and fixed as ordinary
milestone work under §§1–7 and the mutation harness. It does not reopen
certification. Such findings are those sections' job being done by hand at the
wrong gate: the reader that catches them is reading the description layer, and
what it has actually found is a guard that needs hardening, which the harness
and the by-hand mutation protocol already oblige.

**A finding reopens a round only if it clears both lines** — it falls within
the three checks, and its only subject is not a fix-authored record. Failing
either, it is fixed under the obligation named below and the round still closes.
The two lines can look like they overlap, and the definition settles it without
a tie-break: a one-directional pin that leaves an acceptance-criterion clause
unpinned is a check-1 finding and reopens, while one that merely hardens an
assert no criterion names is out of mandate. What decides is whether a criterion
clause is at stake, never how the finding is phrased.

**Each class carries exactly one confirmation obligation, and no class carries
two.** A **reopening finding** obliges a further fresh-context round, and that
round is what confirms its fix. A **fix-authored record** is fixed in place and
confirmed by the next round's reader where a further round occurs, and otherwise
by `/milestone-review`'s three-lens fan-out at the merge gate; no confirmation
obligation falls on the author, because D-067 rejected instructing an author's
own re-check — it asks for the judgment this section exists because authors fail
at — and `tracking-rules.md`'s delegation warrant says the same of a check
already happening unprompted. An **out-of-mandate robustness observation** is
confirmed by operation: the harness, the sweeps and the suite, which is what
§§1–7 already prescribe for the work it becomes.

The gate is therefore reachable with fix-authored records corrected but not yet
independently confirmed. That is a deliberate narrowing of the zero-unresolved
bar rather than an oversight, and the cost it creates is exactly what the
falsifier's second clause below counts.

**What grounds the provenance rule is record churn, not M119's round count.**
Three measured cases, each read out of the revision named beside it. M114 pass
8's round 4 found discrepancies only in the narrative its own earlier rounds had
written — four false claims in a round-3 entry, plus a neighbour re-recording
two observations logged three entries earlier (`a25e6dd^`). M119's rounds 5–9
returned eleven record errors, none of them sitting in text that existed before
round 1 (`016a210`). M121's round 2 returned twelve findings, five of which had
round 1's own fix prose as their only subject (`8763368^`).

On M119's record the provenance rule alone changes the round count by **zero**,
and the paragraph says so rather than claiming a saving it does not produce:
each of rounds 5–9 also returned coverage gaps — three, four, two, two and one
(`016a210`) — and a coverage gap is a finding about executable surface, which
the rule never shields. The mandate boundary is the rule that reaches that
count. Replayed under it, M119 stops after round 6, saving three rounds;
round 6's `kind`-label gap is the one classification that could go either way,
since those two labels are AC1's own pasted-output-or-fenced-block distinction,
and reading it as in-mandate stops the replay after round 7 instead. Tolerance:
±1 round, on that gap.

**This step carries its own falsifier**, stated up front rather than left for a
later argument about whether it is pulling its weight. It counts yield and not
rounds, because the round count is precisely what the two rules above change,
and a measure its own subject can satisfy by construction measures nothing.
Measured over the next three guard-authoring milestones that run §8, the window
closing when the third completes:

- **(i)** If the rounds after each milestone's first return, totalled across the
  window, zero shipped-behaviour defects and zero findings whose subject is
  pre-round-1 surface, then the rounds after the first have stopped earning
  their cost — retire them and run §8 as a single certification pass. A finding
  counts where it was **found**, never where it was fixed, so routing one to
  §§1–7 does not remove it from the count. Tolerance: exact zero on both counts,
  and the window counts only if at least one of its three milestones convened a
  round after its first — a window that never ran a later round has not measured
  one.
- **(ii)** If any fix-authored record corrected in place is later found false —
  by the three-lens review, or by a subsequent milestone — then the in-place
  route has failed, and that class returns to round-opening. Tolerance: one
  occurrence.

Clause (i) counts whether the later rounds still find anything the two rules
above have not already disposed of. Clause (ii) counts the cost those rules
create, which is records corrected without an independent read — a cost the
round-count falsifier this replaces could not see. Both are countable from work
logs as milestones already write them. Replacing that falsifier rather than
retiring the step is a supersession argued in D-083, not a quiet loosening:
D-059's retire-don't-tune rule bites on tuning a measure that works, and the
claim there is that a measure of the wrong quantity is replaced instead.
