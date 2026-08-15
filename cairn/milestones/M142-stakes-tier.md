# M142: The plan gate scales criteria rigor to the deliverable's stakes

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** m142-stakes-tier · https://github.com/jmgirard/cairn/pull/143

## Goal

`/milestone-plan` classifies every scope's deliverable surface and holds
internal-tier criteria to a domain-bounded standard, so verification effort
tracks user-facing stakes instead of growing without limit on internal
tooling — the measured failure in intraclass M120 and circumplex M72–M86.

## Scope

**In:** the step-2 surface-tier rule and internal-tier criteria standard; the
step-3 criteria audit's proportionality question; the step-2 collision check's
checker-regress clause — all in `skills/milestone-plan/SKILL.md` — plus their
prose-guards, mutation-registry entries, and one D-entry.

**Out:** any change to D-090's own clauses — its cairn-scoped door and
Untouched clause stand, annotated only. Out: the review-side thrash remedy →
M143. Out: triage of intraclass M120 and circumplex's norms-audit arc → those
repos' own sessions. Out: adoption piloting for standing instruments → the
existing standing-instrument candidate row (ROADMAP), cross-referenced.

## Acceptance criteria

- [x] AC1 `/milestone-plan` step 2 states the surface-tier rule: every plan
      classifies the milestone's deliverable as user-facing or internal, where
      internal means no external consumer of the repo relies on it — dev
      tooling, data-generation scripts, in-repo checkers over internal
      artifacts, tracking records — and user-facing is everything else,
      including any deliverable whose tier is unclear or that spans both; the
      tier and a one-clause reason are recorded in the milestone file's Goal
      or Scope prose. A registered prose-guard reds when the rule is deleted
      from the skill.
- [x] AC2 The same step states the internal-tier criteria standard: an
      internal-tier acceptance criterion's promise quantifies over a domain
      its named procedure enumerates directly — never an exemption registry, a
      per-rendering enumeration, or a demonstration family spanning process or
      environment boundaries — and a draft needing those is repaired at the
      plan gate by narrowing the promise (step 4's bounded-promise rule) or by
      descoping, never by widening the specification. The standard governs a
      criterion's promise, never a guard's construction — a detector's
      per-rendering positive controls stay mandated by their own doctrine. A
      registered prose-guard reds when the standard is deleted.
- [x] AC3 The step-3 criteria audit asks a proportionality question of each
      criterion — is the promise's domain proportionate to the declared
      tier — and an internal-tier criterion outside AC2's standard is a
      finding disposed at the gate like the audit's other findings. A
      registered prose-guard reds when the question is deleted from the
      audit's question list.
- [x] AC4 The step-2 collision check names the checker-regress shape — a scope
      extending or hardening a checker that the ROADMAP or archive records an
      earlier milestone of the same repo shipping, where that checker verifies
      repo-internal artifacts — and directs that on such a hit the gate poses
      simplifying or deleting the checker as the recommended option and
      hardening it as a present, non-recommended alternative. A repair that
      leaves the checker's promise unchanged stays outside the shape (D-090's
      Untouched clause); one that widens the checker's promise is the regress
      shape however it is framed. A registered prose-guard reds when the
      regress clause is deleted.
- [ ] AC5 The three suites pass from the repo root with per-suite exit codes
      checked; every prose-guard this milestone adds or edits is registered in
      the mutation harness per protected block, and each new rule sentence
      survives relabel, negation, subject-transposition, and relocation probes
      red. A D-entry records the stakes-tier adoption and the regress question
      as a new rule beside D-090's cairn-scoped door — annotating D-090 with
      its Untouched clause intact, hosted per D-098 — and names the
      shipped-behavior defect clearing D-090's trigger: the plan gate as
      shipped accepts internal-tier scopes whose criteria demand unbounded
      specification, measured in the downstream repos.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4, T5

## Tasks

- [x] T1 Author the step-2 surface-tier rule and internal-tier criteria
      standard in `skills/milestone-plan/SKILL.md` (anchors copied from
      shipped bytes; adjacent-guard reflow check per the M104 lesson).
- [x] T2 Add the proportionality question to the step-3 criteria-audit
      paragraph, beside the existing one-exemplar probe it must not oppose.
- [x] T3 Add the checker-regress clause, with its repair discriminator, to the
      step-2 collision check.
- [x] T4 Write prose-guards for the four new rules; register per protected
      block in the mutation harness; run relabel, negation,
      subject-transposition, and relocation probes red (commit fixes before
      any probe that restores — M140 lesson).
- [x] T5 Append the D-entry (next free id); run `cairn_validate` and the three
      suites from the repo root with per-suite exit codes checked.

## Work log

- 2026-08-15: created by /milestone-plan, from the maintainer's churn/thrash report over intraclass and circumplex (measured: intraclass M120's four returns in one day; circumplex M72–M86's fifteen-milestone checker arc).
- 2026-08-15: criteria audit ran (fresh [O] reader, two rounds) — round 1 returned nine findings, all disposed at the gate; round 2 on the amended wording returned five residual scoping findings, fixed in place (AC4 repair discriminator, AC2 promise-scope clause, AC5 D-090-trigger naming, plus two on M143).
- 2026-08-15: plan gate chose a regress gate-question with deletion recommended over a D-090-style hard door because a hard door narrows D-090's Untouched clause and adds supersede ceremony to legitimate hardenings; falsified by a tracked repo accepting the recommended deletion where the checker's absence then admits a user-facing defect it would have caught.
- 2026-08-15: plan gate chose a domain-bounded lite standard over a numeric probe-count cap because the cap contradicted the shipped one-exemplar probe (audit round-1 finding 1); falsified by an internal-tier criterion within the standard still consuming three defect returns.
- 2026-08-15: T1 — surface-tier rule and internal-tier criteria standard authored into /milestone-plan step 2 (two paragraphs after the criteria-drafted rule); question gate skipped, nothing genuinely open — both approach choices were settled at the plan gate; three suites green (786/345/103, per-suite exit codes checked).
- 2026-08-15: T2 — proportionality question added to the step-3 criteria audit, directly after the one-exemplar probe sentence, with an explicit never-relaxes boundary toward it; three suites green, per-suite exit codes checked.
- 2026-08-15: T3 — checker-regress clause with its repair discriminator appended to the step-2 collision check, after the status-disposition bullets; three suites green, per-suite exit codes checked.
- 2026-08-15: T4 — test_stakes_tier.py authored (marker-bounded slice per rule, marker-uniqueness asserted), 18 blocks registered in the mutation harness (contained phrases, never slice bounds); probe run per probe_m142.py at commit 51882de: 17 probes (relabel/negation/subject-transposition/relocation, at least one per rule) all genuinely red (failures>0, errors=0, ran=19), restore verified byte-identical; a subject-pin gap the transposition probe design surfaced was fixed and committed before probing (M131, M140); three suites re-run green after restore, per-suite exit codes checked.
- 2026-08-15: T4 note — probe_m142.py is session scratch, not committed; the T4 line itself states the full procedure (probe families, red criteria failures>0/errors=0/ran>0, byte-identical restore check), so the record stands without the script.
- 2026-08-15: T5 — D-107 appended (previewed verbatim in chat): stakes-tier adoption + regress question beside D-090's door, D-090 annotated with its Untouched clause intact, hosted per D-098, trigger-clearing defect named; cairn_validate all checks passed; three suites green from repo root, per-suite exit codes checked.
- 2026-08-15: defect return #1 (review floor): AC5's probe clause failed as written — new-rule sentences do not survive the four probe families red (upward relocation D4, subject transpositions D5/D6, obligation negations D7/D8, tail deletion P1); repair is guard hardening (positional slice binding, subject/obligation pins, tail coverage, D9's registry block), criteria unchanged; status review → in-progress.
- 2026-08-15: return #1 repaired (T4 reworked): rule slices now resolve inside their owning step's slice so upward relocation reds (D4); subject pins added for the proportionality finding and the regress provenance (D5, D6); obligation pins for "Every plan classifies…records" and "the gate poses" (D7, D8); the "or by descoping" tail pinned (P1); the proportionality slice re-anchored so its registered block is contained, not a bound (D9); 5 new registry blocks; probe run re-executed with the six previously-green mutations plus three upward relocations added — 26 probes all genuinely red (failures>0, errors=0, ran=21), restore byte-identical; three suites green (807/345/103) and cairn_validate clean, per-suite exit codes checked.
- 2026-08-15: defect return #2 (review floor, pass 2): AC5's probe clause failed again by new mechanisms of the same shape (R1-R3: definitional subject, repair verb, shape-intro obligation — each verified green by mutation); thrash trigger (b) fired — pin-enumeration reconsidered in favor of whole-slice equality fixtures per rule slice (D-103's instrument), which settle the in-slice mutation domain by procedure; status review → in-progress.
- 2026-08-15: return #2 repaired: four whole-slice equality fixtures added (verbatim from shipped bytes, normalize = lowercase + whitespace collapse; declared blind spot per RR12: whitespace-only mutations), each registered in the harness anchored on a phrase R1-R3 proved unpinned; step-slice bounds moved to bold labels alone (pass-2 R4, renumbering no longer false-reds); dead assertIn removed (R6); probe run extended with R1-R3 — 29 probes all genuinely red (failures>0, errors=0, ran=25), R1-R3 each red on the fixture alone, restore byte-identical; three suites green (811/345/103) and cairn_validate clean, per-suite exit codes checked; status → review.

## Decisions

## Review

- 2026-08-15 AC1: shipped SKILL.md step 2 lines 42–48 carry the surface-tier rule — classification into user-facing/internal, internal defined by no-external-consumer with the example enumeration, unclear-or-spanning defaulting to user-facing, tier + one-clause reason recorded in Goal/Scope (grep, this session). Guard: 5 TestSurfaceTierRule tests in test_stakes_tier.py, 5 blocks registered in the mutation harness; TestRegisteredGuardsFailWhenBlanked green in the fresh suite run (blanking each block reds its guard), and the fresh probe run's relabel/surface probe reds the whole rule's deletion path (19 ran, 6 failures, 0 errors).
- 2026-08-15 AC2: lines 50–58 carry the internal-tier criteria standard — domain-enumerated-directly bound, the three prohibited forms, narrow-or-descope repair with never-widen, and the promise-not-guard boundary with the positive-controls carve-out (grep, this session). Guard: 4 TestInternalTierStandard tests, 4 registered blocks, harness green; relabel/standard probe reds deletion (10 failures, 0 errors).
- 2026-08-15 AC3: lines 132–137, inside the step-3 criteria-audit paragraph, ask the proportionality question of each criterion against the declared tier, and dispose an out-of-standard internal-tier criterion as a gate finding like the audit's others (grep, this session). Guard: 4 TestProportionalityQuestion tests, 4 registered blocks, harness green; relabel/proportionality probe reds deletion of the question from the audit list (5 failures, 0 errors).
- 2026-08-15 AC4: lines 88–96, inside the step-2 collision check, name the checker-regress shape (extending/hardening a ROADMAP-or-archive-recorded checker over repo-internal artifacts), pose deletion as recommended with hardening present but non-recommended, and carry the repair discriminator both ways — promise-unchanged outside the shape (D-090's Untouched clause), promise-widening inside it however framed (grep, this session). Guard: 5 TestCheckerRegressClause tests, 5 registered blocks, harness green; relabel/regress probe reds deletion (6 failures, 0 errors).
- 2026-08-15 AC5: three suites re-run fresh from the repo root this session — skills 805, scripts 345, hooks 103 tests (corrected 2026-08-15 same review pass, scorer finding D17: the scripts/hooks labels were swapped as first written), exit 0 each, per-suite exit codes checked without pipes. All 18 registered stakes-tier blocks pass the harness's blanking check inside that run; the full probe run re-executed fresh (17 probes across relabel/negation/subject-transposition/relocation, at least one per rule sentence, all RED with failures>0/errors=0/ran=19, restore byte-identical). D-107 present at its heading (grep) — records the adoption and the regress question beside D-090's door, annotates D-090 naming the Untouched clause intact, states the D-098 hosting, and names the trigger-clearing defect measured in the downstream repos.
- 2026-08-15 AC5 tick withdrawn (same pass): the fan-out demonstrated the probe clause failing inside its named families — upward relocation, two subject transpositions, two obligation negations, and a deletable sentence tail all leave the suite green (findings D4-D8, P1 below). The suites-pass and registration halves of AC5 stand; the probe clause is the failing half.
- 2026-08-15 fan-out record: three fresh-context lenses ([O] diff-bug: 20 findings; [S] blame-history: 0 defects, 1 note; [S] prior-PR-comments: 1 finding, PR-thread probe empty) → [S] scorer over all 22.
- 2026-08-15 actioned (≥80): D4 90 (slice_between binds first occurrence from position 0 — upward relocation of any rule out of its step stays green; the T4 red-probe claim holds only for downward relocation); D5 88 (same-repo provenance clause of the regress shape unpinned — "any repo at any time" stays green); D6 88 (proportionality-finding subject unpinned — internal-tier→user-facing inversion stays green); D7 88 (surface-tier obligation unpinned — "Every plan classifies"→"may classify" and "records"→"need not record" stay green); D8 85 (regress recommendation obligation unpinned — "the gate poses"→"may pose" stays green); P1 85 (the repair sentence's "or by descoping" tail deletes green — the M131/M132 prefix-without-tail class); D17 88 (AC5 evidence line's scripts/hooks labels swapped — corrected in place above). Disposition: D17 fixed in this pass; D4-D8+P1 are one guard-hardening defect cluster → defect return #1 to in-progress; D9 (78, sub-threshold) rides the same fix: the "asks a proportionality question of each criterion" registry block overlaps PROPORTION_START, contradicting the registry comment's contained-phrases claim.
- 2026-08-15 logged below threshold (15, surfaced never dropped): D9 78 registry block doubles as slice bound; D2 55 step-4 re-audit routes through "three questions" so amended criteria skip proportionality; D10 55 STANDARD_START doubles as surface-slice end bound (cross-rule red, right direction); D16 55 D-090-door vs regress-recommendation precedence unstated for cairn-internal checkers; D18 55 M142's own file declares no tier (rule ships this milestone); D19 52 step 4/template carry no tier-recording cross-reference; D3 35 audit question-count forks across the three reader surfaces (other skills out of scope); D11 30 "declared" tier precedes the file that records it; D12 30 "this gate" referent in step 2; D13 28 "probe question above" referent; D15 28 "cairn-scoped" gloss on D-090; D14 25 Untouched-clause gloss (Scope sanctioned annotation); D1 22 "three mechanical questions" count reads fine with "also asks"; D20 12 wrap width; B1 10 test-name wording.
- 2026-08-15 AC5 (pass 2): three suites fresh from repo root — skills 807, scripts 345, hooks 103, exit 0 each, per-suite exit codes checked without pipes; all 23 registered stakes-tier blocks pass the harness blanking check inside that run; probe run re-executed hardened — 26 probes (the original 17, the six return mutations D4-D8/P1, three upward relocations) all RED with failures>0/errors=0/ran=21, restore byte-identical; D-107 unchanged since pass 1 (its evidence stands as recorded).
- 2026-08-15 AC5 (pass 2) tick withdrawn: the delta reviewer ([O], repair diff only; findings scored by a fresh [S] scorer) confirmed all six return-#1 repairs hold — 24 relocation probes red in both directions, all named mutations red — then demonstrated three same-class survivors, each verified green by mutation: R1 93 (definitional subject unpinned — "Internal means"→"User-facing means" green), R2 92 (repair obligation verb unpinned — "is repaired"→"is optionally repaired" green), R3 90 (shape-intro obligation/subject unpinned — "The sweep also names this shape: a scope"→"may also name…a review" green). Logged below threshold: R4 65 step-slice markers embed workflow ordinals (renumbering false-reds; fix to bold labels rides the repair), R5 40 PROPORTION_START anchors pre-M142 prose (disclosed D9 tradeoff), R6 35 dead assertIn subsumed by its regex (delete rides the repair), R7 30 regress slice open-ended toward the harvest marker (the fixture repair closes it: insertion reds equality).
- 2026-08-15 pass-2 disposition: AC5 failing twice by new mechanisms of one shape fires thrash trigger (b) — pin-enumeration is the wrong approach, each round buying the next unpinned member. Non-widening repair exists: whole-slice equality fixtures (D-103's instrument, M140/M143 precedent) — byte-equality per rule slice reds on any in-slice mutation, settling the domain by procedure. Defect return #2; the widening test does not reclassify (the repair widens no enumeration).
