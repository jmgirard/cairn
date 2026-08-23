# M153: The effort-audit baselines are re-measured

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m153-baseline-remeasurement

## Goal

Re-measure the three 2026-08-08-era baselines — record-defect share of
actioned review findings, governance share of milestones, and per-milestone
cost — against the M137–M152 window, and record a three-way verdict on
whether the record-rule changes (M134/M136/M137 family; RR13 reduction
M144–M147, D-116 narrowing) are helping, dead weight, or generating their
own thrash. Internal tier: the deliverable is a measurement note over this
repo's own tracking records, with no external consumer relying on it.
Lineage: promotes the "Re-measure the record-defect share" candidate row
(added 2026-08-08, M137 close-out + RR13 rec 9).

## Scope

**In:** the per-finding record-defect classification for cairn M137–M152;
the RR13 Q2 governance-share classification for M144–M152; a
`cairn_cost` run for M137–M152; one new synthesis note under
`cairn/references/` holding all three beside their baselines plus the
verdict; its INDEX line.

**Out:** acting on the verdict — superseding or amending D-099/D-116 (or
any entry) is a separate, user-gated follow-up the note may motivate, never
part of this milestone (gate decision 2026-08-22). Other repos' reviews —
the baseline classification was cairn-only, so the re-measurement stays
cairn-only for comparability; a cross-repo pass would be a new candidate.
Extending `references/effort-experiment-notes.md` — that page keeps the
effort-experiment subject; the new note cross-references it for method.

## Acceptance criteria

- [ ] AC1: A committed synthesis note under `cairn/references/` carries a
      per-finding classification ledger whose domain is enumerated by this
      procedure: for each milestone ID M137 through M152, recover the full
      milestone file's `## Review` section from git history (the file
      `cairn/milestones/M<NN>-<slug>.md` at the last commit where it existed
      before archiving) and take every finding that section records as
      actioned (fixed at the gate) — restricted to those scored ≥80 for
      milestones whose reviews carry numeric scores, and all actioned
      findings for milestones after scoring was retired, with the seam
      between the two populations stated in the note. Each ledger entry
      classifies its finding record-defect or not; the note states the
      resulting share beside the M113–M136 baseline share recorded in the
      ROADMAP candidate row at commit `08bbb07`, a sub-share for M144–M152,
      and names each milestone whose recovered section records no actioned
      findings while its archive summary reports some (the recovered
      sections' coverage gap).
- [ ] AC2: The note states the governance share of milestones M144–M152,
      each classified (a)/(b)/(c)/(d) from its archive title and summary per
      the four-class rule quoted from RR13 Q2
      (`cairn/reviews/archive/RR13-philosophy-and-viability.md`), beside
      RR13 Q2's M100–M143 baseline, with the per-milestone class list
      included.
- [ ] AC3: The note states per-milestone turns and output-token medians for
      milestones M137–M152, produced by `scripts/cairn_cost.py` (the M94
      attribution method), beside the medium-cohort medians in
      `cairn/references/effort-experiment-notes.md`, pinned as a dated
      observation naming the command and the date measured.
- [ ] AC4: The note states a three-way verdict — the rule changes are
      helping, dead weight, or generating their own thrash — as a dated
      observation citing the specific ledger lines and shares it rests on,
      and names which standing decision entry (D-099 or D-116) a dead-weight
      verdict would put in question, without itself superseding or amending
      any decision entry.
- [ ] AC5: The note carries a `**Provenance.**` block per the
      tracking-rules references-pages rule and a one-line entry in
      `cairn/references/INDEX.md`.

## Coverage

- AC1 → T1, T4
- AC2 → T2, T4
- AC3 → T3, T4
- AC4 → T4
- AC5 → T4

## Tasks

- [x] T1: Recover the 16 pre-archive `## Review` sections per AC1's git
      procedure; build the per-finding ledger (milestone, finding id, class
      record-defect / not, one-clause reason); record the score seam and the
      zero-entry milestones (the audit's re-run found M143 and M152 record
      no per-finding entries).
- [x] T2: Classify M144–M152 per the RR13 Q2 rule (quote the rule text into
      the note); compute the (b)+(c) share.
- [x] T3: Run `scripts/cairn_cost.py` for M137–M152; extract per-milestone
      turns/output and window medians.
- [x] T4: Author the synthesis note from the synthesis-note template —
      three comparisons beside their baselines, verdict, Provenance block,
      INDEX line — and run `python3 scripts/cairn_validate.py` clean (the
      references check reads the INDEX pairing).

## Work log

- 2026-08-22: created by /milestone-plan (promotes the 2026-08-08
  re-measurement candidate row).
- 2026-08-22: reduced criteria audit ran ([O] fresh reader, internal tier):
  AC1's first-draft enumeration procedure was unsatisfiable (archive
  summaries carry counts, not per-finding records) — repaired to the
  git-recovery procedure; AC5's validator-green clause bound an instrument —
  moved to T4; the M145 score-retirement seam routed to the gate; revised
  AC1/AC5 re-audited clean, and the re-run surfaced the M143/M152 zero-entry
  coverage gap AC1 now names.
- 2026-08-22: plan gate chose the full M137–M152 window with the seam stated
  over stopping at M144 because the post-reduction era is the question's
  point and n=8 is too thin; falsified by the pooled share proving
  uninterpretable across the seam.
- 2026-08-22: plan gate chose measure-and-record over acting on a dead-weight
  verdict in-milestone because a rule change should not be bundled behind an
  unseen measurement; falsified by the verdict landing so unambiguous that
  the split costs a wasted gate.
- 2026-08-22: plan gate chose a new synthesis note over extending
  effort-experiment-notes because the subject differs (rule efficacy vs the
  effort switch); falsified by the two pages drifting on shared method text.
- 2026-08-22: plan chose inline classification with a committed ledger over
  spawning fresh-context classifier readers (the 2026-08-08 method) because
  the committed per-finding ledger is itself auditable and the tier is
  internal; falsified by review finding classification bias the ledger's
  reasons don't survive.

- 2026-08-22: T1–T4 landed together in one artifact (`references/record-rule-remeasurement.md` + INDEX line) — one checkpoint commit rather than four, logged as the deviation; all 16 blobs recovered, 106-row ledger built, shares/medians computed by script over the table and reproduced exactly (41%/57%/51%/60%; medians 137/175,620 and 135/179,878).
- 2026-08-22: T1 finding — M143 is a legitimate zero, not a gap (archive: "17 findings, 0 scored ≥80"; its two gate fixes scored 60); M152 is the sole coverage gap (10 gate-fixed findings unrecoverable per-finding); the cost store holds no M137/M138 sessions (axis 3 reported over the 14 it holds).
- 2026-08-22: verdict recorded as helping — record-defect share unchanged (~half) but record-caused returns fell to zero post-reduction and correction cascades collapsed to single batched entries; neither D-099's nor D-116's exit condition met; dead-weight exit path named per AC4.
- 2026-08-22: the shipped-page state ledger (`scripts/tests/test_scripts.py` `TestShippedPageStateLedger`) redded on the new page — registered `record-rule-remeasurement.md: ok` (classifier-confirmed); the first suite run had been piped (`| tail`) and hid the red, caught by the unpiped re-run the M56+M65 lesson mandates; both suites then green with explicit exits (scripts 308 / hooks 103, exit 0 each).

## Decisions

## Review
