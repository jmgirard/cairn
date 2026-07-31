# M127: Guard-doctrine §8 is retired whole

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, IP4, GP1
- **Branch/PR:** m127-retire-certification · https://github.com/jmgirard/cairn/pull/127

## Goal

The certification step is retired whole — no fresh-context reading of
guard descriptions, no rounds, no §8 — ending the loop that burned the
measured majority of this repo's session cost.

## Scope

**In:** Remove `guard-doctrine.md` §8 entirely (§9 keeps its number;
retired numbers are never reused) and every operative reference to it:
the pre-review certification step in `skills/milestone-implement/SKILL.md`
and the routing sentence in `tracking-rules.md`'s delegation-warrant
paragraph. Retire or update every test surface pinning the section,
per hit. Delete the M124 §8-ledger machinery whole
(`section_ledger.py`, `test_section_ledger.py`, both ledgers under
`skills/tests/ledgers/`), restorable from git — with §8 gone it has no
live subject and a guard instrument testing only itself is the shape
D-057/D-090 close doors on. Append the superseding D-entry; dispose the
mooted candidate rows. No replacement instrument of any kind: guard
verification remains §1 inversion, the mutation harness, the sweeps, the
three-lens review fan-out with scorer, and AC fencing.

**Out:** the review fan-out and the plan-time criteria audit — kept, by
explicit gate choice (2026-07-31, Q3; D-067 is narrowed to the
criteria-audit reader, not retired). RR11 BC5 → stays a parked candidate
row, re-cut by this milestone to BC5 only. The correction-batching
candidate row banked at the first plan commit → stands unchanged. Any
guard pinning §8's *absence* → deliberately nowhere: an absence guard
would be new apparatus (D-090), so re-adding §8 would be green — a
recorded, accepted exposure.

## Acceptance criteria

- [x] AC1: `guard-doctrine.md` ships with no §8: the section is removed
      whole and §9 keeps its number and heading. A search for "certif"
      and "§8" under `skills/` and `README.md` is run with every hit
      classified: zero hits of the operative class (a shipped sentence
      that obliges, routes to, or presupposes the certification step as
      live); surviving hits are only retrospective provenance citations
      in comments and guards, guards quoting IP4 history verbatim, §9's
      motivating measurement, and the criteria audit's own prose. The
      classification ledger is committed as review evidence (RR04
      rec 8).
- [x] AC2: Every test surface pinning the retired section — found by the
      AC1 search, never by a fixed list — is updated or retired per hit:
      the section-numbering test moves to the gapped 1–7, 9 list;
      §8-only guards retire with their mutation-registry entries; the
      M124 ledger machinery (`skills/tests/section_ledger.py`,
      `skills/tests/test_section_ledger.py`,
      `skills/tests/ledgers/guard-doctrine-8.txt`,
      `skills/tests/ledgers/extractor-contract.md` and
      `.expected.txt`) is deleted; and all three suites pass from the
      repo root with each exit code checked.
- [x] AC3: `skills/milestone-implement/SKILL.md`'s pre-review
      certification step is removed; in `tracking-rules.md`'s
      delegation-warrant paragraph exactly the "A fresh reader's own
      loop is bounded by its instrument" sentence and its
      `(guard-doctrine.md §8)` cite are removed, while the D-067
      carve-out protecting the criteria-audit reader survives and
      `test_delegation_warrant.py:146`'s discriminator pin is preserved
      through the rewrite.
- [x] AC4: A superseding D-entry records: the 2026-07-31 user mandate
      and evidence summary (rounds 2+ yielded record-accuracy
      corrections; every ≥80-scored real defect came from inversion,
      the harness, or the review fan-out); the explicit D-090 door
      check on its Untouched clause — this fires falsifier clause
      (iii)'s own named remedy, "the step retires whole", ahead of its
      measured window, a deliberate deviation under IP2 (D-091 part 4's
      precedent); the supersession — not mere override — of RR10's
      rejections recorded in D-085 (verdict (e) and part 4); the
      narrowing of D-067 to the criteria-audit reader alone; the
      superseded operative clauses of D-069, D-070, D-079 (clauses
      2–3), D-080, D-082, D-083, D-085, D-088, and D-091; and the
      candidate-row disposals, so D-090's by-name parking references
      resolve. `cairn_validate` green.
- [x] AC5: Candidate-row dispositions recorded on the ROADMAP: the
      mixed-round-precedence, falsifier-state-disclosure, and
      audit-over-falsifiers rows dropped (subjects retired; rationale in
      the D-entry); the polarity/vocabulary row dropped and the
      ledger-rollout row re-stated to name git as the deleted
      mechanism's home (both bound to the M124 ledger); the RR11 row
      re-cut to BC5 only with BC6's mooting recorded.

## Coverage

- AC1 → T1, T2
- AC2 → T2, T4
- AC3 → T3
- AC4 → T5
- AC5 → T6

## Tasks

- [x] T1: Remove §8 whole from `skills/shared/guard-doctrine.md`; §9
      keeps its number; rewrite or remove internal cross-references per
      AC1's classification (§9's motivating measurement survives as
      retrospective provenance).
- [x] T2: Run the AC1 search; commit the classification ledger; update
      or retire each test surface per hit (numbering test → gapped
      list; §8-only guards + registry entries retired; M124 ledger
      machinery deleted).
- [x] T3: Remove the implement-skill certification step; excise the two
      routing clauses from `tracking-rules.md` preserving the D-067
      carve-out and the `test_delegation_warrant.py:146` pin.
- [x] T4: Run all three suites from the repo root, each exit code
      checked; record evidence.
- [x] T5: Author the superseding D-entry; preview verbatim in chat
      before the commit that lands it.
- [x] T6: ROADMAP row disposals and re-cuts (AC5).

## Work log

- 2026-07-31: created by /milestone-plan.
- 2026-07-31: plan-gate criteria audit ([O] fresh reader, fresh context) returned 13 findings; 11 fixed into the criteria wording as the audit prescribed (D-069 disposition added to AC1; clause-(iii) carry-over replaces an undefined "zero findings" in AC2; AC3 search-scoped rather than file-listed; ledger-guard exclusion added to AC4; RR10-override and D-090-Untouched grounds named in AC5; third mooted row and the §7 grep collision folded into AC6), 2 became gate questions (cut depth; correction batching).
- 2026-07-31: plan gate chose single-pass §8 over retiring the step whole because round 1 demonstrably still yields (M126's certification found a real shipped defect; this plan's own audit found 13 findings); falsified by clause (iii)'s window returning zero findings across three §8-running milestones.
- 2026-07-31: plan gate chose single-pass over keep-multi-round-and-wait because the post-M125 evidence (M126: 460 turns, 19 agents, multi-round certification the day after the stop rule shipped) shows the loop still burns; falsified by a shipped-behavior defect traced to a finding a reconvened round would have surfaced.
- 2026-07-31: plan gate chose no-new-batching-rule over adding the sentence now because the rebuild removes the cascade's generator and D-090 counsels against preemptive doctrine; falsified by two or more correcting D-entries landing in a single milestone after M127 ships (the banked row's condition).
- 2026-07-31: plan gate chose keeping the review fan-out and criteria audit over trimming them because both are single-shot instruments and the measured burn is loop turns, not spawns; falsified by cairn_cost showing a regression attributable to spawn volume (the existing spawn-cap row's trigger).
- 2026-07-31: plan gate chose keeping RR11 BC5 parked over folding it in because a subtractive milestone should not add doctrine; falsified by a quantified-claim defect shipping in a guard-authoring milestone before BC5 lands.
- 2026-07-31: plan gate (second round) re-cut M127 from single-pass to full retirement at explicit user decision, after an evidence review of §8's actual yield: the multi-round output was record-accuracy corrections (D-084→D-086, D-088→D-089, D-091→D-092→D-093) while every ≥80-scored real defect of the era (M120's three inverting-green asserts 92/88/87; M123 A5 80; M124 F1 92, F2 85, F12 88) was found by inversion, the mutation harness, or the review fan-out — instruments this milestone keeps.
- 2026-07-31: re-cut criteria re-audited by the same [O] fresh reader before writing: the zero-hit search collided with six classes of legitimate survivor (fixed — operative-class scoping plus a committed classification ledger); the section-numbering test needed keep-and-update, not retirement (fixed — per-hit disposition); `section_ledger.py` would be left testing only itself (fixed — M124 machinery deleted, restorable from git); four supersessions were missing (fixed — D-079/D-080/D-082/D-088 added to AC4); two more mooted candidate rows surfaced (fixed — audit-over-falsifiers and polarity rows added to AC5).
- 2026-07-31: plan gate chose full retirement over the committed single-pass re-cut because §8's distinctive yield was record-accuracy-class while its cost was the measured dominant burn; falsified by a claim-accuracy defect (a false record claim about a guard) reaching main undetected by the review fan-out.
- 2026-07-31: plan gate chose deleting the M124 ledger machinery over keeping a subjectless helper because a guard instrument testing only itself is the shape D-057/D-090 close doors on; falsified by the ledger-rollout row's promotion condition firing (a consistency defeat found in another doctrine section).
- 2026-07-31: T1 done — §8 removed whole from guard-doctrine.md; §9 keeps its number and heading, its ledger-instrument paragraphs recast retrospective, and its closing paragraph records the M127 deletion with git as the machinery's home.
- 2026-07-31: T2 done — AC1 search re-run post-edit and the per-hit ledger committed as `cairn/references/m127-ac1-ledger.md` (zero operative hits; one `test_always_read_frame.py` docstring tense-shifted during the sweep); numbering test relocated to new `skills/tests/test_guard_doctrine_sections.py` with the gapped 1–7, 9 list and its own registry entry; 104 mutation-registry entries retired, counted before deletion by `grep -c 'test="TestDescriptionLayerCertification'` (101) + same for `TestImplementRoutesToCertification` (2) + `test_rule_leaves_a_fresh_readers_loop` (1); M124 machinery deleted whole (`section_ledger.py`, `test_section_ledger.py`, `skills/tests/ledgers/`).
- 2026-07-31: T3 done — implement-skill step 8 loses its certification clause; tracking-rules delegation paragraph loses exactly the fresh-reader-loop sentence and its `(guard-doctrine.md §8)` cite; the D-067 carve-out and the discriminator pin survive (delegation-warrant suite green).
- 2026-07-31: T4 done — from the repo root: `python3 -m unittest discover -s skills/tests` 690 tests OK exit 0; `-s scripts/tests` 332 tests OK exit 0; `-s hooks/tests` 103 tests OK exit 0; `python3 scripts/cairn_validate.py` all checks passed, zero warnings, exit 0.
- 2026-07-31: T5 done — D-095 appended (previewed verbatim in chat): the mandate and evidence summary, the IP2-logged deviation from D-090's Untouched clause, the supersession of RR10's rejections in D-085, D-067 narrowed to the criteria audit, per-entry supersessions for D-069/D-070/D-079(2–3 re-scoped)/D-080/D-082/D-083/D-085/D-088/D-091 with D-091 part 3 explicitly surviving, and the candidate-row disposals; `cairn_validate` green.
- 2026-07-31: T6 done — ROADMAP: mixed-round-precedence, falsifier-state-disclosure, audit-over-falsifiers, and polarity/vocabulary rows dropped (rationale in D-095 part 5); ledger-rollout row restated with git (`958c37c^`) as the deleted mechanism's home; RR11 row re-cut to BC5 alone with BC6's mooting recorded; both restated rows previewed verbatim in chat.
- 2026-07-31: review fan-out + scorer run — 10 findings ≥80 actioned (§9 guards re-homed into `test_guard_doctrine_sections.py`; D-096 batched record corrections; ROADMAP pointer repointed; F23 rejected with reason), 19 sub-80 logged with trivial in-place cleanups; details in Review.
- 2026-07-31: correction (review H2/F14, 90) — the T2 line's "104 mutation-registry entries retired" covered only its three named greps; the full removal was 121 entries (103 `guard="test_fresh_context_readers"` + 1 `test_delegation_warrant` + 17 `test_section_ledger`), counted by `git diff main..HEAD -- skills/tests/test_mutation_harness.py | grep '^-.*guard=' | sort | uniq -c`; the 17 include `TestSectionNineDoctrine`'s, whose loss finding F1 reversed by re-homing.
- 2026-07-31: correction (review F11, 87) — T6's `958c37c^` pointer is branch-local and will not survive the squash-merge; the ROADMAP row now cites main-side `ba1e6bd` (`git show ba1e6bd:skills/tests/section_ledger.py`).

## Decisions

## Review

_Evidence gathered fresh at review, 2026-07-31, on branch `m127-retire-certification` (PR #127)._

- AC1: PASS — `grep -n "^## " skills/shared/guard-doctrine.md` lists sections 1–7, 9 with no §8; §9's heading and number intact at line 265. Post-edit AC1 search returned 9 "certif" and 15 "§8" hits (overlapping files), every one classified in the committed ledger `cairn/references/m127-ac1-ledger.md` (in tree per `git ls-files`): zero operative-class; survivors are retrospective provenance, §9's motivating measurement, and criteria-audit prose only.
- AC2: PASS — `git ls-files skills/tests/` shows zero `section_ledger`/`ledgers/` paths (machinery deleted); zero registry mentions of the retired test classes; the relocated numbering test in `test_guard_doctrine_sections.py` asserts the gapped pair list ending (7, 9) and carries its own mutation-registry entry; fresh runs from the repo root: skills 690 tests OK exit 0, scripts 332 OK exit 0, hooks 103 OK exit 0.
- AC3: PASS — zero "certif" hits in `skills/milestone-implement/SKILL.md`; zero hits for the fresh-reader-loop sentence or its `§8` cite in `tracking-rules.md`; the D-067 carve-out sentence present, the discriminator sentence at `tracking-rules.md:687`, and `test_delegation_warrant.py:145` still defines the discriminator test — suite green.
- AC4: PASS — D-095 appended (one heading); element greps confirm the mandate + evidence summary, the D-090 Untouched-clause deviation firing clause (iii)'s "the step retires whole" under D-091 part 4's precedent, the supersession (not override) of RR10's verdict (e) and part-4 rejections, D-067 narrowed to the criteria audit, the nine per-entry supersessions with D-091 part 3 explicitly surviving, and the candidate-row disposals resolving D-090's parking references; `cairn_validate` exit 0, all checks passed.
- AC5: PASS — zero ROADMAP hits for the four dropped rows; the ledger-rollout row names `958c37c^` as the deleted mechanism's git home; the RR11 row carries "re-cut to BC5 by M127" and BC6's mooting clause.

Projection-vs-outcome: no Driving RR — no-op.

**Three-lens review + scorer (2026-07-31).** 30 reported findings ([O] diff-bug 28, [S] blame-history 3, [S] prior-review 1; all three lenses converged on one defect; prior-review's GitHub probe found no real threads). Scorer ([S], fresh): 10 at ≥80 actioned, 19 sub-80 logged, one duplicate pair merged. The scorer's own summary line misfiled F2 (scored 85) as below 80 — the per-finding score governs.

Actioned (≥80):
- F1/P1/H1 (92, three lenses): deleting `test_section_ledger.py` whole removed `TestSectionNineDoctrine` — §9-content guards whose subject survives — FIXED: re-homed as `TestSectionNineDoctrine` in `test_guard_doctrine_sections.py` (10 asserts anchored on the post-M127 bytes, polarity carriers carried over, per-assert registry entries); skills suite 690 → 700.
- H2/F14 (90): the T2 work-log count understated registry loss (104 of 121) — FIXED by appended correction line below (append-only history).
- F23 (90): no guard now pins any DECISIONS.md entry, D-091's included — REJECTED with reason: the surviving rule's durable, guarded home is guard-doctrine §6 (four registry entries still pin it); D-088's precedent makes the doctrine file the guarded home and the D-entry a dated record; pinning individual history entries was §8-era practice that retires with the certification, and history files are governed by IP4 conduct, not guards.
- F11 (87): the ROADMAP row's `958c37c^` git pointer was branch-local and dies at squash-merge — FIXED: repointed to main-side `ba1e6bd`; correction line below.
- F2 (85): "re-adding a §8 would ship green" is false as written (the kept numbering guard reds a numbered `## 8.` heading) — FIXED via D-096 clause 5: exposure recorded narrower; no dedicated absence guard was added, which is what the Scope clause decided.
- F5 (84), F16 (83), F3 (82), F15 (82): record-accuracy defects in D-095 (rounds-after-first attribution; instrument credit; correction-chain notation; A5's score-vs-threshold) — FIXED via D-096, one batched superseding entry (the ROADMAP correction-batching row's prescribed shape; the row stays parked).
- H3 (80): §9's rewritten closing record shipped unpinned — FIXED with F1 (closing-paragraph pin + registry entry).

Sub-80 (19, logged; those touching artifacts this milestone authored were fixed in place as trivial cleanups): F8 78 (§9 quotes §8 vocabulary as examples — kept, quoted history), F13 75 (D-080/D-082 residue asymmetry — D-096 affirms all D-095 supersessions stand), F4 72 (chain shorthand — folded into D-096 clause 1), F6 70 (ledger line numbers off by one — fixed in place, marked), F18 72 (self-certification half of D-067 undisposed — logged; §8's retirement leaves no certification to self-run, and the delegation-warrant rulebook paragraph still governs author re-checks), F20 68 (INDEX ordering — fixed), F21 68 (ledger class enumeration dropped AC1's fourth class — fixed), F22 68 (RP definition vs doctrine-prose row — fixed), F9 63 (one-vs-both ledgers self-contradiction — fixed in §9; D-096 clause 6), F24 62 (AC3 cites :146, def now at :145 — logged, substance preserved), F7 58, F27 56, F17 55, F12 55, F10 52, F28 48 (tense smoothed before pinning), F26 45, F19 15 (blank line restored), F25 12 (pre-existing plan-commit AC6 reference).

Post-triage verification: skills 700 OK exit 0 · scripts 332 OK exit 0 · hooks 103 OK exit 0 · `cairn_validate` all checks passed exit 0.
