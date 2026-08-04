# M133: Ingest the impeccable skill as a skill-architecture comparandum

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m133-impeccable-ingestion

## Goal

Ship `cairn/references/impeccable.md` — a first-hand read of the impeccable
skill's architecture, every finding dispositioned against cairn's own
mechanisms, with the actionable deltas banked as candidate rows.

## Scope

**In:** Read first-hand the architecture-bearing files of the impeccable
install at `~/.claude/skills/impeccable` (version 4.0.4): `SKILL.md`, and
under `reference/` — `routing.md`, `craft-floor.md`, `operate.md`,
`doctor.md`, `hooks.md`, `init.md`, `live-setup.md`, and the four
`degraded/` agent prompts. Write the page under the shelf's existing
comparandum frame (provenance · citation · role · findings), comparing four
mechanism classes cairn has counterparts for: how a request is routed, how the
skill decides which of its own documents to load, how it detects and repairs
drift in its own artifacts, and how it grades what its hooks report. Bank each
actionable delta as a ROADMAP candidate row.

**Out:** The ~15 pure design playbooks (`bolder`, `colorize`, `typeset`,
`critique`, `new-work`, …) and the ~100 scripts → not read; a later ingestion
may widen the corpus if a finding here points into them. Adopting any finding
into cairn's own skills → its own milestone, promoted from the candidate row
this milestone writes. A new outright rejection of a finding → not made here;
absent an existing D-entry covering it, the finding banks as a candidate row
instead. Comparing how impeccable *words* its rules (bans, absolutes, voice)
→ dropped at the plan gate as hard to act on.

## Acceptance criteria

- [ ] AC1: The page carries a `## Read corpus` section listing one path per
      line, each with the byte count observed at read time, plus the install
      path, the `version:` string read from the install's `SKILL.md`
      frontmatter, and the read date. A command stated in the page runs
      `wc -c` over every path in that list and reports any path absent from
      the install or whose byte count differs; met when it reports none.
- [ ] AC2: The page's findings sit in a `## Findings` section as a numbered
      list, one finding per numbered entry. A command stated in the page
      enumerates those numbered entries and reports (a) any entry carrying no
      citation of the form `<path>` or `<path>:<line>`, and (b) any cited path
      that is not a member of AC1's read-corpus list; met when it reports none.
- [ ] AC3: Each numbered finding entry carries a `Disposition:` line whose
      value begins with exactly one of `already-has`, `candidate`,
      `covered-by-D`, `not-applicable`, followed by its required reference —
      `already-has` by the cairn `file:line` already carrying the rule,
      `candidate` by the banked row's opening phrase, `covered-by-D` by the
      `D-0NN` that settled it. A command stated in the page enumerates the
      numbered entries and reports any entry with no `Disposition:` line, or
      whose value does not begin with one of those four tokens, or whose value
      is one of the first three tokens with no reference after it; met when it
      reports none.
- [ ] AC4: Every finding whose `Disposition:` begins `candidate` has a bullet
      in `cairn/ROADMAP.md`'s `## Candidates` section ending with the
      provenance tail `— added 2026-08-04 — M133 (references/impeccable.md)`,
      and each such bullet carries an overlap sweep sentence (`Swept <date>:`,
      D-042) and a falsifying promotion condition (`Promote when … — never on
      a count of …`, D-027/D-035). A command stated in the page enumerates the
      page's `candidate`-dispositioned findings and the ROADMAP bullets
      bearing that tail, and reports any finding whose named bullet is absent,
      any tailed bullet lacking a `Swept` sentence, and any lacking a
      `Promote when` clause; met when it reports none.
- [ ] AC5: `TestShippedPageStateLedger` (`scripts/tests/test_scripts.py:1381`)
      is extended to pin `impeccable.md`'s extraction state, with its one-line
      justification as a comment above `EXPECTED` (shipped practice, M118/
      M121/M127), in the same commit that adds the page. At that commit the
      profile's `verify` slot — `python3 -m unittest` over `skills/tests`,
      `scripts/tests` and `hooks/tests` — and `cairn_validate` both exit 0.
- [ ] AC6: `cairn/references/INDEX.md` gains exactly one line for
      `impeccable.md`, matching the file's existing grammar: `- <filename> — `
      followed by a single em-dashed gloss.

## Coverage

- AC1 → T1, T2, T5
- AC2 → T2, T5
- AC3 → T3, T5
- AC4 → T4, T5
- AC5 → T6
- AC6 → T6

## Tasks

- [x] T1: Read the twelve declared files first-hand; record each path with its
      `wc -c` byte count and the install's `version:` string.
- [x] T2: Draft `cairn/references/impeccable.md` — provenance, citation, role,
      `## Read corpus`, and `## Findings` as a numbered list, each entry cited
      to a corpus path.
- [x] T3: Disposition each finding against cairn's state — sweep `skills/`,
      `skills/shared/tracking-rules.md` and the `### D-` headings of
      `cairn/DECISIONS.md` (bounded read, D-054) for the counterpart
      mechanism; write the `Disposition:` line with its reference.
- [x] T4: Write a candidate bullet for each `candidate` disposition, each with
      its own overlap sweep and falsifying promotion condition, appended to
      `cairn/ROADMAP.md`'s `## Candidates` section with the M133 tail.
- [x] T5: Write AC1–AC4's four checking commands into the page's
      `## Verification` section; run each and record its output.
- [x] T6: Add the `INDEX.md` line; extend `TestShippedPageStateLedger` with
      the pin and its justification comment; run the three suites and
      `cairn_validate`, both to exit 0, in the page's commit.

## Work log

- 2026-08-04: created by /milestone-plan.
- 2026-08-04: plan gate chose reading the eight architecture files plus the four `degraded/` prompts over reading all ~40 reference pages, and over additionally reading the ~100 scripts, because the four mechanism classes cairn has counterparts for are documented in that prose and the design playbooks have no cairn parallel; falsified by a finding here that cannot be stated without a fact only a skipped file carries.
- 2026-08-04: plan gate chose ingest-and-bank over also planning an adoption milestone now (the two offered were phase-gated rulebook loading and severity-graded drift reporting), because every prior shelf ingestion banked before adopting and the adoption's shape depends on findings not yet written; falsified by a banked row whose promotion condition is already satisfied the day the page lands.
- 2026-08-04: plan chose comparing mechanisms alone over also comparing how impeccable words its rules, because style findings carry no promotion condition anyone could act on; falsified by a mechanism finding whose cairn-side defect turns out to be wording rather than structure.
- 2026-08-04: plan chose carrying AC4's provenance in the candidate bullet's existing `— added … —` tail over giving candidate rows a source column, because D-035 fixes a candidate row at one line with no file and no ID; falsified by a superseding entry reopening candidate-row structure.
- 2026-08-04: T1 — read all twelve declared files first-hand (84,208 bytes total); version 4.0.4 confirmed from SKILL.md frontmatter; byte counts recorded for the Read corpus. Status → in-progress, branch m133-impeccable-ingestion cut from pushed main.
- 2026-08-04: criteria audit ([O], fresh context) returned four findings, all fixed before writing: AC1 quantified over "every file read first-hand", which nothing enumerates (a 3-of-147 list passed) → the declared list is now the corpus, checked by `wc -c`; AC2's command enumerated citations while the criterion quantified over entries, so a zero-citation entry passed → the command now enumerates entries; AC3 required the disposition value to be *exactly* one of four tokens and *also* to name a reference, which no line satisfied → "begins with"; AC4 required a file column on candidate rows, which D-035 forbids and the section (a flat bullet list) does not have → provenance tail, plus the sweep and falsifying-condition clauses the rulebook already demands. AC5 and AC6 returned clean.

- 2026-08-04: T2–T5 — page drafted with 14 findings (6 already-has, 4 covered-by-D: D-063/D-067/D-037/D-064, 3 candidate, 2 not-applicable — one entry cites two mechanisms under one not-applicable); 3 candidate rows appended to ROADMAP with sweeps and falsifying promotion conditions; all four AC commands run clean. AC1's command needed one fix before it ran: a loop variable named `path` shadows zsh's tied `$PATH` and made `wc`/`tr` unresolvable — renamed to `p` in the stated command.
- 2026-08-04: T6 — INDEX.md line added; `TestShippedPageStateLedger` pinned `impeccable.md: ok` with its justification comment; skills/scripts/hooks suites all OK and `cairn_validate` exit 0.
- 2026-08-04: all tasks done, suites and validate clean — status → review.

## Decisions

## Review
