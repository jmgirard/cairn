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

**A count recorded in a milestone record carries the procedure that produced
it, at verbatim-reproducible grade.** A work-log line, a docstring, a comment,
or a D-entry stating a count states the command as run, or the committed
artifact the count is read from — at the granularity that discriminates it
from a disagreeing record. M124 measured the failure: three records disagreed
on one suite count under a reflow, and the one discriminator — whether bullet
paragraphs are re-wrapped — was stated in none of them; the two that named a
procedure left it out, and the third named no procedure at all.

**A universal claim over a milestone's own artifacts is a count claiming zero exceptions, and carries the recorded-counts rule's procedure obligation.**
"Every criterion has a task", "no guard reads via `open()`", "all five sites
updated" each assert an exception count of zero, so the record stating one
names the procedure that enumerated the domain, at the same
verbatim-reproducible grade as any other count.
**Where no stated procedure can enumerate the domain, the universal is not written** —
state what was actually swept and how, and claim that instead (RR11 BC5; the
M118 lesson is the failure mode: a criterion listing its sites becomes the
sweep, and every site it omits ships stale).

**The first remedy weighed for a claim proven false in prose the branch in hand added is deleting the claim** —
available where a search over the repo for the claim's subject finds no
dependent; correction is the remedy where one exists, and the measured
failure mode is the repair that re-falsifies: intraclass M100's review
passes 2 and 3 each found a fresh false claim inside the previous pass's
fix, while the sentence that is not there cannot be false (M130). Merged
current knowledge stays corrected-in-place and marked (D-045); IP4 history
is superseded, never edited.

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

## 9. Presence is not consistency

**A prose-guard pins that a sentence is present. It does not pin that the
section around it still agrees with itself.** Every assert in §8 matched and
the whole suite was green while eight of ten mutations negated a shipped rule
without touching one pinned block (M123 round 3). An anchor is a claim about a
sentence; a rule is a claim the section makes. They come apart three ways.

**A contradicting sentence added elsewhere in the section.** The pinned
sentence stays where it was and stays true of itself; a later sentence asserts
the opposite, and the section now says both. Appending "A robustness
observation outside them reopens a round on the same terms" was one of eight
such mutations, which between them defeated six acceptance-criterion clauses
with every anchor still matching.

**A rename reusing no word of the term.** A guard keyed on part of a defined
term — its prefix, or its noun — is defeated by a coinage sharing neither, and
the section is left alternating two names for one class. Substituting "A
shielded entry is still read" for "A fix-authored record is still read" is the
measured case, and it survived four successive extensions of the enumeration
meant to catch it, which is why the remedy is not a fifth.

**A relocation falsifying a back-reference.** "The three named checks above" is
true of a position, not of a phrase: move the list and the sentence is
unchanged, still matched, and false.

**So derive the check from the section, never from a list of what to look
for.** Enumerating the renderings a phrase can take is the failure §3 names,
and against this class it has a measured record of losing. M124 shipped the
derived form: `section_ledger.py` extracted a section's ordered,
whitespace-normalized sentence sequence, and a guard compared it against a
committed ledger of that sequence, with no term drawn from the section
written into the extractor — so a coinage nobody anticipated was still a
difference. The instrument detected a change and never judged it: whether a
change is a contradiction, a correction or an ordinary edit is not a question
a diff can answer, and building it to answer one would rebuild the judgment
D-059 retired. Its remedy was operation the author ran, never adjudication
the guard performed — a red ledger was discharged by regenerating it, reading
the reported diff sentence by sentence, and then repairing the section or
accepting the change. The one failure mode that defeated the instrument was a
ledger updated without its diff being read, which no guard can detect — a
cost stated here rather than hidden.

The one ledger ever committed covered §8, the certification section M127
retired whole (its number stays retired, as milestone IDs and principle
numbers do). The ledger machinery — `section_ledger.py`, its guard, the
committed ledger and the extractor's contract fixture — was deleted with it,
restorable from git, because a consistency instrument whose only subject is
gone tests nothing but itself.
