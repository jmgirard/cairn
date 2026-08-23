# Record-rule re-measurement against the 2026-08-08 baselines (M153)

**Provenance.** Ingested 2026-08-22 by M153 from a first-hand read of this
repo's own git history (the 16 pre-archive milestone-file `## Review`
sections, blob-pinned below), the archive summaries, RR13
(`reviews/archive/RR13-philosophy-and-viability.md`), the ROADMAP candidate
row at commit `08bbb07`, and `scripts/cairn_cost.py` over the local session
store.
Pagination: —.
Extraction: first-hand record — the review blobs and archives were read directly from git 2026-08-22 and are immutable at their commits; the cost figures are a snapshot of a live store — observed 2026-08-22.

**Scope.** Re-measures three baselines after the record-rule changes — the
derived-claims family (M134/M136/M137), the RR13 reduction (M144–M147), and
D-116's narrowing of the family to code-adjacent artifacts — and records a
three-way verdict (helping / dead weight / self-thrash). It is a measurement,
not a rule change: it supersedes and amends nothing. Method for the effort
axes: `references/effort-experiment-notes.md`. This is a reference, not an
authority — status lives in `ROADMAP.md`, decisions in `DECISIONS.md`,
architecture in `DESIGN.md`.

**Evidence snapshot.**

- The 16 `## Review` sections, each recovered from the file
  `cairn/milestones/M<NN>-<slug>.md` at the parent of the commit that
  archived it (`git log --format=%H -n1 -- <file>`, then `<hash>^:<file>`) —
  observed 2026-08-22.
- Archive summaries for M137–M152 (`cairn/milestones/archive/`) — observed
  2026-08-22.
- Baselines: record-defect share ~half of actioned ≥80 findings, M113–M136,
  ROADMAP row at `08bbb07`; governance share (b)+(c) ≈ 73–77% of M100–M143,
  RR13 §2; cost medians (medium cohort M128–M136: 165 turns / 169k output),
  `references/effort-experiment-notes.md` — observed 2026-08-22.
- Per-milestone cost: `python3 scripts/cairn_cost.py --milestone M<NN>` for
  each of M137–M152, run 2026-08-22.

## Method

**Population and seam.** For each milestone M137–M152, every finding its
recovered `## Review` section records as actioned (fixed at the gate):
restricted to findings scored ≥80 where the review carries numeric scores
(M137–M144; scoring was retired at M145, `skills/milestone-review/SKILL.md`),
and all gate-fixed findings from M145 on. The two populations differ — the
baseline's was "actioned ≥80" — so the eras are also reported separately.
Grouped fixes are rowed as the review's own actioned enumeration groups them.

**Classification rule.** A finding is `record` when the defective thing is a
claim, count, citation, or evidence statement — in a tracking record (work
log, D-entry, ROADMAP, LESSONS, DESIGN currency, review evidence, a ledger)
or a code-adjacent claim surface (comment, docstring, changelog) — matching
the `08bbb07` classification ("stale or false counts and evidence claims,
not code"). It is `other` when the defective thing is deliverable content or
behavior: skill/doctrine prose design, README or diagram content, guard or
test coverage and machinery.

**Coverage.** M143 contributes zero rows legitimately: its archive records
"17 findings, 0 scored ≥80" (its two gate fixes scored 60, below the scored
era's population). M152 is the coverage gap: its recovered section carries AC
evidence only; the archive reports 18 findings with 10 fixed at the gate,
per-finding identities unrecoverable (the M105 push-timing shape), so its 10
are excluded from every share below and named here. M137–M138 additionally
have no sessions left in the cost store (axis 3 only) — observed 2026-08-22.

## Ledger — every actioned finding, classified

| # | M | Finding | Class | Reason |
|---|---|---|---|---|
| L01 | M137 | F19/87 | record | stale work-log assert count |
| L02 | M137 | F1/85 | record | D-099 "otherwise stands" false vs D-095 |
| L03 | M137 | F3/85 | record | D-099 misattributed the classification |
| L04 | M137 | F12/84 | other | guard assert read wrong function |
| L05 | M137 | F5/82 | other | rule-wording conjunction mismatch |
| L06 | M137 | F10/82 | other | corollary prose stated grade term |
| L07 | M137 | F13/82 | other | vacuous test assert |
| L08 | M137 | F22/80 | other | unpinned pointer, guard gap |
| L09 | M137 | F27/80 | record | AC4 evidence sweep a digit-line proxy |
| L10 | M138 | F18/85 | record | stale docstring surface count |
| L11 | M139 | F1/80 | other | return-floor limb not carved out |
| L12 | M139 | FA/95 | other | relocation defeats guards |
| L13 | M139 | FD/85 | record | D-101 misdescribes shipped surface |
| L14 | M139 | R1/96 | other | rule invertible with suite green |
| L15 | M139 | R3/93 | other | test not doing what name claims |
| L16 | M139 | B1/C2 92 | record | D-101 edited in place (IP4) |
| L17 | M139 | R2/85 | other | classification sentence negatable |
| L18 | M139 | R4/80 | other | guard slice spans six rules |
| L19 | M139 | R4-03/82 | record | free-standing counts in comments |
| L20 | M139 | R4-04/80 | record | test comment claimed false property |
| L21 | M139 | R4-09/82 | record | D-103 heading's unsubstantiated annotation |
| L22 | M140 | O-F1/88 | other | fixture crossed a rule boundary |
| L23 | M140 | O-F2/82 | other | degenerate slice pair count |
| L24 | M141 | F2/95 | record | reader-ledger arithmetic, one id undispositioned |
| L25 | M141 | F1/82 | other | README meaning inversion |
| L26 | M141 | F4/87 | other | README guarantees deleted |
| L27 | M142 | D4/90 | other | guard blind to upward relocation |
| L28 | M142 | D5/88 | other | provenance clause unpinned |
| L29 | M142 | D6/88 | other | finding subject unpinned |
| L30 | M142 | D7/88 | other | obligation verbs unpinned |
| L31 | M142 | D8/85 | other | recommendation obligation unpinned |
| L32 | M142 | P1/85 | other | repair-sentence tail deletable green |
| L33 | M142 | D17/88 | record | AC5 evidence labels swapped |
| L34 | M142 | R1/93 | other | definitional subject unpinned |
| L35 | M142 | R2/92 | other | repair obligation verb unpinned |
| L36 | M142 | R3/90 | other | shape-intro obligation unpinned |
| L37 | M144 | O1/85 | record | D-108 false claim on D-090's clause |
| L38 | M144 | B1/84 | record | same D-108 defect, blame lens |
| L39 | M144 | O9/80 | record | DESIGN bullet asserted stale state |
| L40 | M144 | O11/85 | record | LESSONS line misplaced template edits |
| L41 | M144 | B2/80 | record | D-109 misattributed §8-apparatus figures |
| L42 | M145 | F1 | other | triage-ordering coherence, step 5 |
| L43 | M145 | F2 | other | triage-ordering coherence, step 6/7 |
| L44 | M145 | F3 | other | amendment-audit mode wording |
| L45 | M145 | F4 | other | §5 heuristics folded into step 5 |
| L46 | M145 | F5 | record | routing decision lacked its D-entry |
| L47 | M145 | F8 | other | carve-out wording |
| L48 | M145 | F9 | other | single-reviewer wording |
| L49 | M145 | F10 | other | probe-clause wording |
| L50 | M145 | F11 | other | ingest-mode wording |
| L51 | M145 | F12 | other | brief template comment placement |
| L52 | M145 | F13 | other | Binding-criteria header slot |
| L53 | M145 | F19 | record | twin citation left stale |
| L54 | M145 | F16 | record | D-111 claim corrected (D-113) |
| L55 | M145 | F17 | record | D-111 claim corrected (D-113) |
| L56 | M145 | F18 | record | D-110 spawn count wrong in D-112 |
| L57 | M146 | O1 | record | stale rulebook-mass baseline figure |
| L58 | M146 | O3 | record | false kept-count in Decisions |
| L59 | M146 | O4 | record | branch-only SHA pointer dangles on main |
| L60 | M146 | O6+B4 | other | review step lacked hand-run instruction |
| L61 | M146 | O7 | record | self-verification ledger claims false |
| L62 | M146 | O9 | other | failure-identity clause dropped |
| L63 | M146 | O11 | other | retirement discriminator dropped |
| L64 | M146 | O13 | other | exemption did not name members |
| L65 | M146 | O15 | record | stale D-052 id in template |
| L66 | M146 | O10/O12/B1+S1-4 | other | empty registry blocks, guard hygiene |
| L67 | M146 | B2 | record | AC5 evidence-line overclaim |
| L68 | M147 | F1 | record | over-trimmed lesson lost operative clause |
| L69 | M147 | F2 | record | trimmed lesson claimed false ownership |
| L70 | M147 | F3 | record | row lost its baseline locator |
| L71 | M147 | F4 | record | ledger label wrong |
| L72 | M147 | F5 | record | never-on-felt-cost clauses dropped |
| L73 | M147 | F6 | record | per-input redness clause dropped |
| L74 | M147 | F7 | record | lesson ground unannotated |
| L75 | M147 | F8 | record | lesson ground miscredited |
| L76 | M147 | F9 | record | parked-clauses missing from rows |
| L77 | M147 | F11 | record | four operative row/lesson clauses dropped |
| L78 | M147 | F12 | record | row claimed "pinned" for hand-run |
| L79 | M147 | F13 | record | work-log baseline count wrong |
| L80 | M148 | F1 | other | instrument-vs-probe tiebreak missing |
| L81 | M148 | F9 | record | ROADMAP row tense/date stale |
| L82 | M148 | F10 | other | chip recommendation ambiguity |
| L83 | M149 | blame-1/2 | record | D-119 missing two-doors context |
| L84 | M149 | blame-5+diff-1/8/9 | record | D-119 basis/figures misstated |
| L85 | M149 | blame-4+diff-5 | record | D-119 grounded on wrong analogy |
| L86 | M149 | diff-12 | other | rulebook trailing clause |
| L87 | M149 | diff-3 | other | remedy ordering |
| L88 | M149 | diff-4/6 | other | budget check de-numbering |
| L89 | M149 | diff-2 | other | surfaced-never-auto-trim marking |
| L90 | M149 | diff-7 | record | wrong D-id citation in skill |
| L91 | M149 | diff-10 | record | LESSONS header stated one cap of two |
| L92 | M149 | diff-13 | record | AC6 evidence figure delta |
| L93 | M149 | diff-14 | record | stale pinned baseline figures |
| L94 | M150 | F1 | other | gates drawn on wrong edges |
| L95 | M150 | F2 | other | edge contradicted worked example |
| L96 | M150 | F3 | record | changelog claim false for two gates |
| L97 | M150 | F4 | record | changelog overcounted phases |
| L98 | M150 | F5 | other | return label broader than floor |
| L99 | M151 | F1 | other | question and disposal rule disagreed |
| L100 | M151 | F2 | other | disjunct contradicted genus reading |
| L101 | M151 | F6 | other | strained antecedent |
| L102 | M151 | F3 | record | D-120 misstated M101 return 1 |
| L103 | M151 | F8 | record | D-120 misquoted G7/G8 |
| L104 | M151 | F11 | record | D-120 left a D-118 clause unnamed |
| L105 | M151 | R1 | other | genus head wording |
| L106 | M151 | R3 | record | first-pass evidence lines unmarked stale |

M145's review headline says "14" while its enumeration names the 15 ids
rowed above (F18 folded into one grouped sentence); the ledger follows the
ids.

## Axis 1 — record-defect share

Computed from the ledger table above (`python3` count of `record` vs total
rows, by era; rerun it on this file to reproduce):

- Scored era M137–M144 (actioned ≥80): **17 of 41 record (41%)**.
- Unscored era M145–M151 (all gate-fixed; M152's 10 excluded, gap above):
  **37 of 65 record (57%)**.
- Whole window: **54 of 106 (51%)**, against the `08bbb07` baseline's
  "roughly half" for M113–M136 — unchanged.
- Sub-window M144–M152 (post-reduction): **42 of 70 (60%)**. M147 is a
  special case — its deliverable *was* the record diet, so all 12 of its
  findings are record-class by construction; without M147 the sub-window is
  30 of 58 (52%) and the whole window 42 of 94 (45%).

Within the family's post-D-116 domain (code-adjacent surfaces —
comments, docstrings, changelog, user-facing docs), the window holds about
6 of the 106 rows (L10, L19, L20, L90, L96, L97; L57 and L93, stale pinned
baseline figures in skill prose, are the borderline); the rest of the
record class sits in tracking records, where D-116 deliberately withdrew
the family and left ordinary care and the review lenses to govern.

## Axis 2 — governance share, M144–M152

RR13 §2's rule, quoted: a milestone is "**(a)** if its deliverable changes
what an operator of an adopting repo gets from the skills, hooks, or scripts
in ordinary work on their own code; **(b)** if it changes how cairn's
tracking records are authored or governed; **(c)** if it changes how cairn
verifies its own prose, guards, criteria, or review loops (verification of
verification); **(d)** other". Classified from archive title and summary:

M144 (c) · M145 (c) · M146 (b) · M147 (b) · M148 (c) · M149 (b) · M150 (a)
· M151 (c) · M152 (a)-or-(b) (its plain-style rule spans operator-facing
chat conduct — the M106 precedent for (a) — and record prose).

**(b)+(c) = 7–8 of 9 (78–89%)**, against RR13 Q2's 73–77% for M100–M143.
Flat-to-adverse — with the stated caveat that four of the nine (M144–M147)
are RR13's own prescribed surgery, and a fifth (M148) and sixth (M151)
execute falsifiers that surgery pre-registered.

## Axis 3 — per-milestone cost

`python3 scripts/cairn_cost.py --milestone M<NN>` (M94 attribution), run
2026-08-22. The store no longer holds sessions for M137–M138 (0 sessions
filtered — observed 2026-08-22); figures are the 14 milestones it holds.

| M | turns | output |
|---|---|---|
| M139 | 480 | 706,204 |
| M140 | 99 | 171,362 |
| M141 | 91 | 160,748 |
| M142 | 241 | 251,724 |
| M143 | 143 | 169,246 |
| M144 | 133 | 179,878 |
| M145 | 152 | 196,712 |
| M146 | 534 | 1,529,214 |
| M147 | 119 | 316,552 |
| M148 | 129 | 123,078 |
| M149 | 135 | 147,045 |
| M150 | 139 | 81,969 |
| M151 | 165 | 191,687 |
| M152 | 116 | 116,922 |

Medians (n=14): **137 turns / 175,620 output**, against the medium-cohort
baseline's 165 / 169k (`effort-experiment-notes.md`). Post-reduction
sub-window M144–M152 (n=9): 135 turns / 179,878 output. Per-milestone cost
is flat; the two outliers are M139 (the guard-thrash milestone, 3 defect
returns) and M146 (the rulebook reduction itself).

## Verdict

**Helping — neither supersede exit fires; not self-thrash** — dated
observation, 2026-08-22, resting on the ledger and shares above:

- The headline share did not drop: record defects are still roughly half of
  gate findings (51% whole-window vs the `08bbb07` baseline's "roughly
  half"). The generator — hand-written claims in records — is alive.
- What the rules targeted was the generator's *cost*, and that fell. Defect
  returns caused by a record defect: one in the window (M141 F2, L24,
  2026-08-15, pre-reduction) and zero in M144–M152, versus the baseline
  era's record-caused returns and gated amendments (M135's two, M130's top
  finding). Correction-entry cascades collapsed: post-M146 the window shows
  at most one batched superseding entry per milestone (D-117 at M147; D-121
  at M151), the D-116 part-3 shape, versus the D-083–D-093 chain.
- Not self-thrash: the M137 F19/F27 shape (a rule milestone red on its own
  record) recurs only as single batched corrections, the designed path.
- Neither exit's condition is met. D-116's falsifier — a tracking-record
  defect class the narrowed family would have caught and ordinary review
  does not — has not fired: every record defect above was caught at the
  gate in one pass. D-099's — a case the widened rule leaves ungoverned
  where old §6 governed it — likewise not observed.
- A **dead-weight** verdict, had the cost evidence gone the other way, would
  put **D-116** in question first (its bet that ordinary care suffices for
  tracking records — the share shows records still generate half the
  findings) and D-099 behind it. That is the exit path; this note does not
  take it.

## Open questions

- The unscored era's population ("all gate-fixed") is broader than the
  baseline's ("actioned ≥80"), which inflates the 57%/60% figures by
  including sub-threshold discretionary fixes the baseline excluded; the
  seam is stated in Method and the eras reported separately — observed
  2026-08-22.
- Whether M147-style record-diet milestones should be excluded from future
  share measurements by rule (their findings are record-class by
  construction) — left to the next re-measurement — observed 2026-08-22.
- M152's 10 gate-fixed findings remain unclassifiable unless its review
  bookkeeping is recovered from a source this note did not reach — observed
  2026-08-22.
