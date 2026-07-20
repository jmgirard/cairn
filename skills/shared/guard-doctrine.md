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
the suite, require red, restore, and diff. This is the behavioral test —
a rule is what changes compliant behavior when deleted or inverted — and
guard-reddening is its mechanical proof procedure, never a substitute for it.

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

Anchors are chosen partly for matchability, so a pinned block is not thereby
doctrine: reddening is *sufficient* to block a careless deletion, never
*necessary* to justify one, and never *sufficient* to keep prose that fails
the behavioral test.

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

Name a validate finding by its emitted label in backticks (`coverage
complete`), and write evidence counts from command output, never memory.

## 7. Scoping a sweep or a grep-shaped criterion

**A repo-wide sweep and a grep-shaped acceptance criterion both hit ground
you did not mean.** An exclusion list may name only history files
(`DECISIONS.md`, changelogs, `legacy/`, `reviews/archive/`) — never a live
directory, or the sweep silently skips records that are still read to act on.

**A criterion whose evidence is a grep will hit the milestone's own
artifacts**: the guard's `assertNotIn` (an absence-assert is a hit for the
token it locks), the milestone file's Scope and Tasks, and the ROADMAP
lineage row. Scope the evidence command to the prose surface being fixed, and
exempt the tracking lines in the criterion at plan time — otherwise it needs
a gated amendment at implement.
