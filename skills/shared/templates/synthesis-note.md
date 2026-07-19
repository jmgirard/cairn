<!-- Template for a committed cairn/references/ synthesis note — a cross-source
     or first-hand analysis that no single citekey owns (a fit assessment, a
     comparative survey, a pilot ledger, a characterization).
     Doctrine: skills/shared/tracking-rules.md — "References pages", whose
     "When a page is owed" rule is the trigger: an analysis that will outlive
     its milestone earns a page; analysis serving only the milestone in hand
     stays in the milestone file.
     A page that owns ONE primary source uses templates/source-note.md.
     The field words `Ingested` and `Extraction:` are load-bearing — the
     references check and the dated-observation guard both parse them — so
     keep them even though nothing was ingested from a shelf here.
     The `Extraction:` status is one physical line, however long — the guard
     that enforces the dated form reads the line it starts on, so a wrapped
     status silently loses its `— observed` stamp.
     The status is READ, not merely stored: the `references staleness`
     advisory classifies it. Whatever wording you choose, it must
     claim a verification, or carry a date, or say there is nothing to re-verify.
     A verification claim is a verb — `verified`, `checked against`,
     `read against`, `read directly`, or `unverified` — and it counts as
     negated when a negator precedes it in that same clause, so
     `none re-read since` in a LATER clause qualifies a claim without undoing it.
     A status doing none of the three says nothing the advisory can read, and
     it is reported rather than assumed verified.
     The alternatives below are examples of that shape, not the accepted list.
     Pick ONE alternative and delete the others — the `nothing to re-verify`
     clause is searched across the WHOLE status, so leaving it beside another
     alternative exempts the page from staleness entirely.
     Every committed page also carries its one line in references/INDEX.md. -->
# <what this analyses> (M<NN>)

**Provenance.** Ingested YYYY-MM-DD by M<NN> from <the derivation, not a shelf
path: the input `references/` pages by filename | the activity performed
("running `/cairn-init` §2", "live probing in Claude Desktop") | the external
repo or artifact read read-only, with its path and commit>.
Pagination: —.
Extraction: <derived — no external source of its own, only as current as its inputs, none re-read since YYYY-MM-DD | first-hand record, nothing to re-verify against | a YYYY-MM-DD snapshot; the assessed artifact has moved on independently since> — observed YYYY-MM-DD.

**Scope.** What this page is and is not. Say plainly that it is not a source
summary, and what it deliberately builds nothing of. Then the tracking
disclaimer, which every synthesis note carries: this is a reference, not an
authority — status lives in `ROADMAP.md`, decisions in `DECISIONS.md`,
architecture in `DESIGN.md`. A synthesis note that starts asserting status is
a second tracking system.

**Evidence snapshot.** What was read, when, and at what path, commit, or PR.
Each of these is a claim about the repo's state at read time, not a standing
fact, so each carries `— observed YYYY-MM-DD` inline.

- <what was read> — <path / commit / URL> — observed YYYY-MM-DD.

## What <the assessed thing> is

Neutral characterization before any verdict. A reader who disagrees with the
judgment below should still be able to trust this section.

## <Ledger name> — mapped to <cairn's doctrine | the file map | the criteria>

State the tag vocabulary above the table and use only those tags:

- `fix-here` | `candidate` | `out` — for a gap ledger.
- `Adopt` | `Adapt` | `Already have` | `Reject` — for a fit assessment.

| # | <their element> | <ours today> | Tag |
|---|---|---|---|
| E1 | <what they do> | <what we do, or nothing> | <tag> |

Every row carries a stable ID (`E1`, `G-C2`, `G-I3`). Later pages, milestones,
and D-entries cite these IDs, so an ID is never renumbered once the page is
committed — add rows, never reflow them.

## Disposition

Where every row above lands: folded into this milestone, → a named ROADMAP
candidate row, → `D-<NNN>`, or → out with its reason stated here. Every
`Adopt` lands somewhere and every `Reject` carries its reason, so a later
sweep finds the rejection instead of re-proposing the idea (search-first,
tracking-rules). Name the test file that locks any rule this page produced.

## Open questions

Claims about the *repo's own state* — what has not been read, what a later
task must still check — are dated observations, not standing facts. Each
carries `— observed YYYY-MM-DD` inline, and is re-checked before the milestone
merges.

- <question or absence> — observed YYYY-MM-DD.
