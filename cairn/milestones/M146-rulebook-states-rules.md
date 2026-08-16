# M146: The rulebook states rules, git holds reasons

- **Status:** in-progress
- **Priority:** high
- **Depends on:** M145
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** m146-rulebook-states-rules

## Goal

The shipped tracking prose states operative rules only — `tracking-rules.md`
at ≤400 lines, `guard-doctrine.md` deleted, `records-hygiene.md` trimmed,
the density/budget/stamp machinery retired — with git and DECISIONS.md
holding the reasons (RR13 recs 3–4). User-facing tier: the rulebook and
skills ship to every adopting repo.

## Scope

**In:**
- Rewrite `skills/shared/tracking-rules.md` to ≤400 lines: justification
  prose, §8-era residue, the always-read governance frame, the prose-guard
  authoring rules, and the density/budget/stamp prose go; operative rules
  stay (AC1's list).
- The derived-claims / derived-figures / failure-identity rules narrowed to
  code-adjacent artifacts; two record de-escalation rules stated (AC5/AC6).
- Delete `skills/shared/guard-doctrine.md`; rewrite or remove every
  referencing site. Trim `skills/shared/records-hygiene.md` to its
  candidate-row-lifecycle and supersede-discipline sections (§5 already
  retired by M145).
- Retire the density/budget machinery from code and prose (AC4's sweep: the
  advisory and its registration, the density block, `cairn_budget.py` and
  its tests, the template's drafting-budget preamble, the budget-run steps
  in four skills, the stamp write-site ceremony — the stamp survives as one
  replace-with-a-short-line sentence per site).
- Prune `skills/tests` to guards whose subjects survive, mutation-harness
  registrations included (plan gate 2026-08-16: prune chosen over
  leave-red and delete-whole).
- Three superseding D-entries (AC6).

**Out:** the LESSONS/candidate-row diet, and cleanup of retired-artifact
names inside ROADMAP/LESSONS rows → M147 (M146's sweeps exclude those two
files); general skill-file shortening beyond reference fixes → not planned,
revisit on adopter evidence; the external adoption pass → the RR13 step-3
candidate row.

## Acceptance criteria

- [ ] AC1: `wc -l skills/shared/tracking-rules.md` reports ≤ 400, and the
      shipped file still states each of: the file map and boundary rule;
      section ownership and AC fencing; status vocabulary with gatekeepers;
      sizing and the work tiers; the git/approval model including
      default-branch detection and the enforcement boundary; question gates
      and routing-chip rules; the bounded DECISIONS.md read; toolchain
      profiles; validation-doctrine and references-page routing; the RB/RR
      escalation gate — and every tracking-rules rule a shipped
      `skills/*/SKILL.md` cites by name, enumerated by grepping the skills
      for tracking-rules citations, survives or has its citation updated.
- [ ] AC2: `skills/shared/guard-doctrine.md` does not exist, and
      `git grep -n 'guard-doctrine' -- ':!cairn/DECISIONS.md'
      ':!cairn/milestones/' ':!cairn/reviews/' ':!cairn/legacy/'
      ':!cairn/references/' ':!CHANGELOG.md' ':!cairn/ROADMAP.md'
      ':!cairn/LESSONS.md'` returns no hits (the two excluded tracking files
      are M147's ledger rows).
- [ ] AC3: `skills/shared/records-hygiene.md` contains exactly its
      candidate-row-lifecycle and supersede-discipline sections plus
      preamble; every hit of `git grep -n 'records-hygiene'` (AC2's
      exclusions) describes the trimmed form; each dropped section's
      operative rule is relocated into its consumer or its loss recorded in
      the remainder ledger.
- [ ] AC4: The density/budget machinery is retired:
      `git grep -n 'check_record_density\|NON_ITEM_LINE_CAP\|non_item_lines\|cairn_budget\|DENSITY_FILES\|record density'`
      (AC2's exclusions) returns no hits; a `cairn_validate` run on this
      repo lists no `record density` advisory; the milestone template's
      drafting-budget preamble is removed; and each stamp write site —
      enumerated by `git grep -n 'Last hygiene check' -- 'skills/'` — is a
      single sentence (replace the stamp with one short line, never append).
- [ ] AC5: The reduced rulebook's derived-claims, derived-figures, and
      failure-identity rules bind code-adjacent artifacts (code comments,
      docstrings, changelog entries, user-facing docs) and state that
      tracking records are exempt; and the rulebook states the two
      decision-entry rules — a D-entry carries the decision and rationale
      and no derived measurements, binding on entries authored after this
      milestone (prior entries stand under IP4); history-record corrections
      batch to at most one superseding entry per milestone, binding at
      authoring time — verified by reading the shipped sections.
- [ ] AC6: Three superseding D-entries are appended, each naming its
      superseded entry in its heading: one superseding D-057's trigger
      clause (the reduction's partial reopening, grounded in RR13 Q1–Q3);
      one superseding D-052's per-line-axis clause (the density advisory
      retired, the replace-never-append stamp rule standing); one narrowing
      the D-099 family to code-adjacent artifacts and stating the two record
      de-escalation rules of AC5 — the entry states the narrowing's D-108
      basis, takes the batching rule as an addition under the 2026-08-16
      plan gate's explicit decision (D-109's named-exception shape), quotes
      the batching row's 2026-08-15 audit verbatim and disposes it, and
      graduates that row.
- [ ] AC7: `python3 -m unittest discover -s skills/tests` is run by hand at
      the branch tip and its result recorded in the Review section with
      every red dispositioned (intentional cut vs defect); the prune's
      target — zero reds, every retained guard's subject present in the
      reduced corpus — is recorded as the run's observed outcome, not
      enforced as a gate (D-109: the suite gates no commit, merge, or
      check-off); a defect-classified red is ordinary pre-merge triage, and
      step 9's hygiene stamp still records the run per D-109.
- [ ] AC8: `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s hooks/tests` both pass.

## Coverage

- AC1 → T1
- AC2 → T2, T5
- AC3 → T3
- AC4 → T4
- AC5 → T1
- AC6 → T6
- AC7 → T5
- AC8 → T4, T5

## Tasks

- [x] T1: Rewrite `skills/shared/tracking-rules.md` to the reduced form
      (AC1's retained units + AC5's narrowed records rules), running the
      skill-citation grep first so every cited rule is placed.
- [x] T2: Delete `skills/shared/guard-doctrine.md`; fix referencing sites:
      tracking-rules (the module mapping and read instruction),
      skills/milestone-plan/SKILL.md:130–131 and :179,
      skills/milestone-brief/SKILL.md:107, cairn/DESIGN.md:37, and the code
      comments in scripts/cairn_validate.py:980,1004,
      scripts/tests/test_scripts.py, hooks/tests/test_hooks.py.
- [x] T3: Trim `records-hygiene.md` to §1+§2; relocate §3/§4/§6 operative
      content or ledger it; fix the tracking-rules mapping line.
- [x] T4: Retire the density/budget machinery:
      scripts/cairn_validate.py:111–150 + the :1844 registration,
      scripts/cairn_scripts.py:48–85 and :282–300, scripts/cairn_budget.py,
      scripts/tests/test_cairn_budget.py, TestNonItemLineAxis in
      scripts/tests/test_scripts.py; the budget-run steps
      (milestone-plan:241, milestone-review:333, milestone-brief:81,
      milestone-implement:109); the stamp write sites (milestone:143–146,
      milestone-review:337–340, cairn-init:109); the milestone template's
      budget preamble; cairn/DESIGN.md:64. Gating suites green after.
- [x] T5: Prune `skills/tests`: enumerate each file's test classes and
      disposition per class against its subject (M127 lesson) before any
      whole-file deletion; update mutation-harness registrations; hand-run
      and record per AC7.
- [x] T6: Draft, preview, and append the three superseding D-entries;
      graduate the batching candidate row.

## Work log

- 2026-08-16: created by /milestone-plan (RR13 step 2, gate round 1).
- 2026-08-16: criteria audit ran ([O] fresh reader): AC1 lost its thrash-rule item (never a rulebook rule) and gained the skill-citation clause; AC4 gained DENSITY_FILES + the advisory label + grep-derived write sites; AC7 reworded to D-109's record-and-disposition cadence; re-audit of gate-amended AC6/AC7 returned two AC6 fixes (rule 1's prospective/IP4 caveat; the addition-not-narrowing basis for the batching rule), both applied — AC7 OK.
- 2026-08-16: plan gate chose pruning skills/tests to surviving subjects over deleting the suite or leaving it red because D-109's day-old falsifier stays decidable only over a green baseline; falsified by the prune consuming more than a session or the retained suite reddening on unrelated edits.
- 2026-08-16: plan gate chose shipping the batching rule as an explicit addition (D-109's named-exception shape) over leaving the row parked because RR13 rec 3 prescribes it and practice already conforms (D-096, D-106); falsified by a milestone legitimately needing a second correcting entry at authoring time.
- 2026-08-16: pre-implementation question gate skipped — both open choices were settled at the plan gate; no tripwire tags.
- 2026-08-16: T1 done — tracking-rules.md rewritten to 400 lines (`wc -l` at this commit), operative rules + AC5's narrowed records rules only; skill-citation grep run first (71 hits) and every cited rule placed; /milestone's always-read-frame audit bullet removed with the frame (its stamp step compressed in passing); gating suites green.
- 2026-08-16: T2 done — guard-doctrine.md deleted; referencing sites fixed in milestone-plan, DESIGN.md, cairn_validate.py, test_scripts.py, test_hooks.py (plan's line numbers had drifted; sites re-derived by grep); AC2 grep clean outside skills/tests (T5's ground); gating suites green (345+103 OK).
- 2026-08-16: T3 done — records-hygiene.md trimmed to §1+§2 + preamble with an HTML-comment remainder ledger (§4's rule already lives in implement step 6; §3/§6 dropped, losses recorded); every records-hygiene reference (DESIGN.md, tracking-rules mapping line) describes the trimmed form.
- 2026-08-16: T4 done — cairn_budget.py + test_cairn_budget.py deleted; check_record_density, its registration, DENSITY_FILES, NON_ITEM_LINE_CAP, non_item_lines, TestNonItemLineAxis removed; budget-run steps in four skills replaced by cap-only drafting lines; both stamp write sites now one sentence; template budget preamble cut; DESIGN.md reporter list updated; AC4 grep clean outside skills/tests; suites 308+103 OK; validate lists no density advisory.
- 2026-08-16: T5 done — skills/tests pruned per the Decisions ledger; hand-run 506 tests zero reds; AC2+AC4 greps clean repo-wide; gating suites 308+103 OK.
- 2026-08-16: T6 done — D-114 (D-057 trigger reopened for reduction), D-115 (density axis retired, stamp rule stands), D-116 (family narrowed to code-adjacent + two de-escalation rules, batching-as-addition per the plan gate's named-exception decision) previewed verbatim in chat and appended; batching candidate row graduated.

## Decisions

- 2026-08-16 (T5 prune ledger): `skills/tests` pruned to surviving subjects; hand-run at the pruned tip: 506 tests, zero reds. Every red was dispositioned **intentional cut** — a pin on wording M146 deliberately rewrote or on machinery M146/M145 retired (the 45 pre-existing M145-rewording reds the 2026-08-16 ROADMAP stamp recorded are the M145 subset) — none a defect. Files deleted whole, subject retired: test_always_read_frame, test_amendment_budget, test_derived_figures (rule survives in the rulebook; every pin was on retired wording), test_git_safety_hooks, test_guard_doctrine_sections, test_scripted_edit_landing, test_record_density (its one green test was a stray LESSONS-header pin). The other 36 files kept their green classes/methods; class-level cuts: TestRulebookStatesTheBoundedRead; TestMilestoneTemplateBudgets + TestCounterIsAdvertisedWhereItIsDocumented; TestSelfCheckingClassRule; TestDurableRecordPreviewRule; TestRbRrOnlyPath; TestBriefTemplate + TestRulebookSentences; TestAcceptanceChipsRule + TestAccessibleLanguageRule; TestClarificationMarkerCap; TestHygieneStampRule + TestStatedCapMatchesEnforcedCap; TestModuleExists + TestRulebookPointer (lesson-graduation); TestNarrationDisciplineRule; TestRulebookPointer (records-hygiene-graduation); TestPlacementTest + TestReddeningAsymmetry + TestPlacedWhereItsConsumersRead; TestSearchFirstCandidateRule + TestFalsifyingPromotionConditions; TestMarkersUnique + TestProportionalityQuestion; TestGuardDoctrineBanking — method-level cuts are enumerated by this commit's diff. Mutation harness: 274 registry entries dropped (39 missing target, 212 block gone, 23 guard gone, measured by the prune script at this commit), 325 kept and re-verified by the harness's own blanking run; six retained guard files whose registrations all died moved to EXEMPT with a dated reason (re-registration deferred to adopter evidence).

## Review
