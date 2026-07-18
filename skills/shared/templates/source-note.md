<!-- Template for a committed cairn/references/<citekey>.md source note.
     Doctrine: skills/shared/validation-doctrine.md — "Source ingestion",
     "Standing facts vs. dated observations", "Page provenance".
     A synthesis note (a cross-source analysis no single citekey owns) uses
     the same Provenance block, naming its input pages as the source pointer.
     Every committed page also carries its one line in references/INDEX.md. -->
# <citekey> — <what this source is for, in a few words>

**Provenance.** Ingested YYYY-MM-DD by M<NN> from
`cairn/references/sources/<citekey>.pdf` (gitignored) — or, for a non-PDF source,
the URL plus how it was retrieved and by whom.
Pagination: <journal pages | preprint pages | PDF pages | —>.
Extraction: <verified YYYY-MM-DD against the source | unverified — first pass, values not yet re-read against the source> — observed YYYY-MM-DD.

The `Extraction:` status is one physical line, however long — the guard that
enforces the dated form reads the line it starts on, so a wrapped status
silently loses its `— observed` stamp.

**Citation.** Full citation as printed: authors, year, exact title, venue,
volume/issue/pages, DOI. Note anything the source prints differently from how
it is commonly cited — a missing issue number, a corrected copyright line, a
title that differs from the running head.

**Role.** What this source is here to settle, and what in the repo depends on
it. If nothing traces here yet, say so — a guidance-only source is a normal
kind of page, not an incomplete one.

## Extracted values

Every value carries its page or table anchor. Values that must be exact are
quoted verbatim, in quotation marks, rather than paraphrased:

- <value> — <source's own wording>, p. N / Table N.

## Traces to

What in the repo reads this page: tests, oracle-registry entries, vignette or
documentation claims, other `references/` pages. This is the list a corrector
walks when a value here changes, so name specific files and lines, not areas.

- `path/to/file:LINE` — what it takes from here.

## Open questions

Claims about the *repo's own state* — what is on the shelf, what has not been
read, what a later task must still check — are dated observations, not
standing facts. Each carries `— observed YYYY-MM-DD` inline, and is re-checked
before the milestone merges: the thing observed missing is often added, or
answered by a page written later in the same milestone.

- <question or absence> — observed YYYY-MM-DD.
