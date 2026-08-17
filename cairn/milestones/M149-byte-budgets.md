<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M149: The line caps gain byte budgets

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** m149-byte-budgets

## Goal

The rulebook's ROADMAP and LESSONS line caps gain fixed byte budgets, stated as
prose and checked by judgment at hygiene passes, so an item file can no longer
defeat its cap by line width — the adopter-measured defect: circumplex ROADMAP
62,482 B at 58 green lines, circumplex LESSONS 63,662 B and intraclass LESSONS
34,554 B at 49 green lines, hygiene passes of 2026-08-15/17 stamping green over
all three. Surface tier: user-facing — the deliverable is the shipped rulebook
and skills every adopting repo reads.

## Scope

**In:** byte budgets `ROADMAP.md < 24,000 bytes` and `LESSONS.md < 20,000
bytes` (fixed: line cap × 400, the healthy line width surveyed 2026-07-19 for
D-052) in the rulebook's Weight caps; propagation to every shipped surface
stating those line caps; a `wc -c` instruction at the two hygiene-pass sites;
a D-entry recording the decision and evidence; a dated annotation on the
instrument-adoption candidate row.

**Out:** a validator byte check — declined at the 2026-08-17 plan gate
(checker-regress rule, simplify-first); the D-entry's falsifier names the
re-open path. A DECISIONS.md cap — illegal under IP4 (D-053); it stays bounded
by reading less (D-054). Trimming the three over-budget adopter files — their
own next audits (the D-052 rollout shape). Item-line length caps — M84's kept
reasoning stands: item lines are never length-policed.

## Acceptance criteria

- [ ] AC1: The rulebook's Weight caps bullet states, beside the existing line
      caps, `ROADMAP.md` < 24,000 bytes and `LESSONS.md` < 20,000 bytes, marks
      them judgment-checked at hygiene passes (no validator check), and leaves
      the existing cap substrings intact (the mutation harness pins
      `` `LESSONS.md` < 50 lines `` — skills/tests/test_mutation_harness.py:343);
      the remedies bullet covers a byte-budget overrun, adding a LESSONS remedy
      (retire or prune entries, imported from the cairn/LESSONS.md:9 header)
      covering both its line cap and its byte budget.
- [ ] AC2: Every hit of the sweep
      `grep -rnE "\b(60|50)[- ]lines?\b" --exclude-dir=tests skills/ cairn/ROADMAP.md cairn/LESSONS.md`
      on the merged tree that states a ROADMAP or LESSONS line cap also states
      that file's byte budget beside it; every other hit is named out-of-scope
      in the review evidence. Append-only history (DECISIONS.md, archives) is
      outside the domain and untouched.
- [ ] AC3: The `/milestone` health-audit step and `/milestone-review`'s
      post-merge hygiene step (skills/milestone-review/SKILL.md:336-337) each
      name the two byte budgets as a `wc -c` check in their cap checks.
- [ ] AC4: An appended D-entry records: the two budgets and their fixed basis;
      that D-058's falsifier fired, identifying the adopter evidence, which
      this milestone's Goal holds; that the prose form was chosen at the
      checker-regress gate with machinery declined — its heading reading
      "annotates D-058", not claiming supersession, and the entry stating why
      annotation is the correct disposition though D-058's Consequences
      pointed at supersession (no removed machinery is rebuilt); and the prose
      form's own falsifier — a file found over its byte budget at two
      consecutive hygiene passes without a trim, excluding the three files
      this milestone's Goal names on their first hygiene pass after this rule
      ships — whose firing takes a fresh plan-gate remedy (the D-117 shape).
      No prior entry is edited (`git diff main...HEAD -- cairn/DECISIONS.md`
      shows additions only). A work-log line records the falsifier tightening
      relative to the plan-gate line (two consecutive passes; first-pass-only
      carve-out) and why.
- [ ] AC5: The instrument-adoption-discipline candidate row carries a dated
      annotation that a standing instrument was weighed at this milestone's
      checker-regress gate and declined in favour of prose — condition not
      fired; the row remains a candidate.
- [ ] AC6: cairn's own ROADMAP.md and LESSONS.md measure under their byte
      budgets (`wc -c`) on the merged tree.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T4
- AC6 → T5

## Tasks

- [x] T1: Amend the Weight caps bullet (skills/shared/tracking-rules.md:62) and
      the remedies bullet (:71-76): byte budgets beside the line caps, marked
      judgment-checked; LESSONS remedy imported; pinned substrings intact.
- [x] T2: Run the AC2 sweep; add the byte budget beside every ROADMAP/LESSONS
      line-cap statement it finds (known sites: skills/cairn-init/SKILL.md:95
      and :103, skills/milestone-review/SKILL.md:355 "50-line",
      cairn/LESSONS.md:9); record each remaining hit's disposition.
- [x] T3: Add the `wc -c` byte-budget line to the `/milestone` health audit and
      the `/milestone-review` post-merge hygiene checklist.
- [x] T4: Append the D-entry (AC4's content); annotate the instrument-adoption
      candidate row (AC5's wording).
- [ ] T5: Run both gating suites with explicit exit codes; hand-run
      skills/tests and disposition reds (intentional re-wording per D-109 is
      noted, not a firing); `wc -c` both tracking files.

## Work log

- 2026-08-17: created by /milestone-plan, from the cross-repo assessment of circumplex/intraclass/quarto-index (this session) finding line-cap gaming by line width.
- 2026-08-17: criteria audit ran in full mode (user-facing tier), twice, each with a fresh [O] reader: pre-gate machinery draft — 25 findings, gate re-shaped the milestone to prose-only; post-gate prose draft — 5 findings (sweep pattern missed hyphenated "50-line" and over-matched the 150-line cap and test fixtures; spurious falsifier; row-annotation wording), all repaired into AC1/AC2/AC4/AC5 above.
- 2026-08-17: plan gate chose prose budgets over a validator byte check because the checker-regress rule poses simplify-first and the user took it; falsified by an over-budget file surviving a hygiene pass untrimmed (the D-entry's recorded falsifier).
- 2026-08-17: plan gate chose fixed budgets (line cap × 400) over mean-derived thresholds because derivation is the measured failure mode of M84/D-049 (misfire or inertness plus a per-pass re-measurement tax); falsified by the budgets proving wrong-sized in the field — a healthy file red, or bloat sitting comfortably under cap.
- 2026-08-17: plan gate chose adopter-side trims at each repo's own next audit over trim passes planned now because the D-052 rollout shape lets the rule prove itself in the field; falsified by an adopter red persisting across consecutive audits untrimmed.

- 2026-08-17: T1 done — Weight caps bullet gains the byte-budget sentence (pinned `` `LESSONS.md` < 50 lines `` substring untouched); remedies bullet gains the ROADMAP byte remedy and imports the LESSONS retire-or-prune remedy; both gating suites green, exit codes checked.
- 2026-08-17: T2 done — sweep found 6 hits: 5 gained budgets (cairn-init:95/:103, migration-protocol:87 — a site the plan's known list missed, the sweep caught it — milestone-review:355, LESSONS.md:9); tracking-rules:62's budgets sit on the same bullet's continuation lines (T1). Suites green.
- 2026-08-17: T3 done — `wc -c` byte-budget check added to the `/milestone` health audit (after the validate read) and `/milestone-review` post-merge hygiene (beside "verify weight caps"). Suites green.
- 2026-08-17: substantive amendment of AC4 at the mini gate — the original wording forced the D-entry to restate measured figures (D-116 part 2 conflict) and carried a falsifier that self-fired on the licensed rollout; narrowed, never widened; two fresh [O] readers (mini-gate draft, re-entry pass), final wording user-accepted.
- 2026-08-17: falsifier tightening vs the plan-gate line above — one-pass-untrimmed became two consecutive passes with a first-pass carve-out for the three files the Goal names, so the rule survives the rollout the Scope licenses (adopters trim at their own next audits) while staying falsifiable on those files from their second pass on.
- 2026-08-17: T4 done — D-119 appended at file end (an initial mis-placement above D-118 was corrected before commit; branch diff on DECISIONS.md is 32 insertions, 0 deletions); instrument-adoption row annotated (weighed, not fired).

## Decisions

## Review
