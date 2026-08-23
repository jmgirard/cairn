# M153: The effort-audit baselines are re-measured

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m153-baseline-remeasurement · https://github.com/jmgirard/cairn/pull/154

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

- [x] AC1: A committed synthesis note under `cairn/references/` carries a
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
- [x] AC2: The note states the governance share of milestones M144–M152,
      each classified (a)/(b)/(c)/(d) from its archive title and summary per
      the four-class rule quoted from RR13 Q2
      (`cairn/reviews/archive/RR13-philosophy-and-viability.md`), beside
      RR13 Q2's M100–M143 baseline, with the per-milestone class list
      included.
- [x] AC3: The note states per-milestone turns and output-token medians for
      milestones M137–M152, produced by `scripts/cairn_cost.py` (the M94
      attribution method), beside the medium-cohort medians in
      `cairn/references/effort-experiment-notes.md`, pinned as a dated
      observation naming the command and the date measured.
- [x] AC4: The note states a three-way verdict — the rule changes are
      helping, dead weight, or generating their own thrash — as a dated
      observation citing the specific ledger lines and shares it rests on,
      and names which standing decision entry (D-099 or D-116) a dead-weight
      verdict would put in question, without itself superseding or amending
      any decision entry.
- [x] AC5: The note carries a `**Provenance.**` block per the
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
- 2026-08-22: review fan-out F14 — the promoted candidate row was pruned from the ROADMAP at plan time (`41affe6`, on main) against records-hygiene §1 (candidates graduate at completion, never at plan); violation logged here, the mitigation being that the M153 planned row advertised the work throughout; the post-merge hygiene pass has nothing to graduate.
- 2026-08-22: the shipped-page state ledger (`scripts/tests/test_scripts.py` `TestShippedPageStateLedger`) redded on the new page — registered `record-rule-remeasurement.md: ok` (classifier-confirmed); the first suite run had been piped (`| tail`) and hid the red, caught by the unpiped re-run the M56+M65 lesson mandates; both suites then green with explicit exits (scripts 308 / hooks 103, exit 0 each).

## Decisions

## Review

Fresh evidence, 2026-08-22, branch head at PR #154:

- AC1: the note's 106-row ledger re-counted by script over its own table at review — scored era 17/41 (41%), unscored 37/65 (57%), whole 54/106 (51%), M144+ sub-share 42/70 (60%) — each matching the stated figures exactly; the `08bbb07` baseline named 5 times; the population seam stated in Method ("Population and seam"); the coverage statements present — M143 a legitimate zero (archive: "17 findings, 0 scored ≥80"), M152 the named gap (10 gate-fixed findings unrecoverable); ledger milestones = the 14 with populated rows, M143/M152's absence explained in Coverage. VERIFIED.
- AC2: the RR13 §2 rule quoted at note line 202, the per-milestone class list at 209, "(b)+(c) = 7–8 of 9 (78–89%)" beside "RR13 Q2's 73–77% for M100–M143" at 213. VERIFIED.
- AC3: the cost table produced by `cairn_cost.py --milestone M<NN>` with the command and run date pinned; medians "137 turns / 175,620 output" beside the medium-cohort 165/169k, re-reproduced by `statistics.median` at review. The procedure ran over all 16 IDs; the store yields 0 sessions for M137–M138, and the note states that absence as a dated observation, so the medians rest on the 14 the procedure yields — the maintainer-logged reading (fan-out F6): the criterion names the procedure, the procedure ran over its full domain, its empty yield for two milestones is disclosed in the deliverable. VERIFIED on that reading.
- AC4: the verdict section opens "**Helping — neither supersede exit fires; not self-thrash** — dated observation, 2026-08-22", cites ledger ids (L24) and the shares; names D-116 (first) and D-099 as what a dead-weight verdict would put in question; `git diff origin/main...HEAD -- cairn/DECISIONS.md` is empty (0 lines) — nothing superseded or amended. VERIFIED.
- AC5: `**Provenance.**` block at note line 3 with the template's field words; exactly 1 INDEX.md line for the page. VERIFIED.

Consistency gate: `cairn_validate` exit 0 (all checks passed; the 19 work-log-wrap advisories are exit-neutral). No DESIGN.md principle changed → `cairn_impact --changed` skipped. Profile `generic`: consistency-gate slot names no toolchain checks — clean no-op. Driving RR `—` → projection-vs-outcome no-ops. Defect returns this milestone: 0; amendment returns: 0.

Fan-out 2026-08-22 (three lenses — the diff touches `scripts/tests/`, so the internal tier's single-reviewer route does not apply): [O] diff-bug 18 ranked findings; [S] blame-history 1 finding (the test-dict placement, converging with diff-bug's #18) + 6 verified-clean checks; [S] prior-PR-comments no prior-review regression (probe empty, archives M78–M91/M99/M115/M137/M146/M147/M149 checked; independently reproduced every share and median exactly). All three lenses independently reproduced the ledger shares; the [O] lens spot-checked 13 milestones' rows against the recovered blobs, all exact, and confirmed the verdict's zero-record-caused-returns-post-M144 claim.

Triage (maintainer, at the gate) — fixed now on the branch: F1 M152 gap cause corrected (the per-finding record was never written — the surviving branch carries the same two-line section; not the M105 squash shape) and open question closed as unrecoverable; F2 batching claim narrowed to history-record correction entries (D-121 only; D-117 dropped from the claim); F3 one-pass claim corrected (L106 surfaced at re-review; none escaped or forced amendment); F4 exit-silence clause added (a non-firing exit is equally consistent with dead weight); F5 M149 headline/enumeration seam noted beside M145's; F6 AC3 evidence line now records the 14-of-16 basis and the logged reading; F7 RR13 quote completed ((d)'s parenthetical + the classed-by-subject sentence); F8 code-adjacent enumeration fixed (7 ids incl. L65, "about" dropped); F9 share-reproduction procedure stated as the actual regex; F10 record-prose characterizations replaced with numbers ("flat"/"alive"/"legitimately"/INDEX "flat"/"collapsed"); F11 sub-window relabeled and marked as pooling across the seam; F15 M152 archive arithmetic noted (18 vs 10+6); F16 scoring-retirement cite corrected to D-110; F17 observed-stamps added to medians and verdict; F13+blame-1/F18 test comment gains the ok-vs-exempt distinction and the EXPECTED key moved to alphabetical position. Rejected with reasons: F12's Extraction-blend half (the template calls its status alternatives examples, and the exempting nothing-to-re-verify clause is absent) and its missing-template-sections half (Method serves the what-it-is role; open questions carry stated landings after F1's fix); F14 as a branch defect (the candidate row was pruned at plan on main, pre-branch — a records-hygiene §1 violation logged in the work log, not this diff's defect; restoring the row minutes before its legitimate post-merge graduation would re-create the step it exists to make deliberate). Return floor: no finding demonstrates an AC failing on its logged reading and none is a load-bearing defect in what the skills/hooks/scripts do → no status change.
