# M121: Verification triage — classify every self-verification instruction, and re-decide D-067's two fresh-context readers

- **Status:** review
- **Priority:** normal
- **Depends on:** M120
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** `m121-verification-triage` / https://github.com/jmgirard/cairn/pull/121

## Goal

Classify every self-verification instruction in cairn's shipped prose against
the Opus 5 guide's over-verification finding, apply a recorded disposition to
each, and re-decide D-067's two fresh-context readers on the evidence of what
they have caught since adoption.

## Scope

**In:** a committed synthesis note holding the classification ledger; applying
every `narrow` and `remove` disposition to the shipped prose; a `DECISIONS.md`
entry disposing of D-067's criteria audit and description-layer certification
individually; a rulebook rule in "Model and agent strategy" naming which class
of self-checking the delegation guidance governs and which it does not.

**Out:** evidence-gathering instructions that run a command and read its output
— they are the guide's own preferred pattern and are classified `keep` in the
ledger without further work. The three RB tripwires and the Fable gate → not
touched; they gate escalation, not self-verification. A reasoning-effort dial
and a numeric spawn cap → candidate rows opened at M120. Any change to the
review fan-out's three lenses or its scorer → out; M120 owns the one review
change in this batch, and the lenses rest on M17's diff-blindness argument,
which no finding here disturbs.

## Acceptance criteria

- [ ] AC1 — `cairn/references/self-verification-ledger.md` exists, authored
      from `skills/shared/templates/synthesis-note.md`, and records: the search
      that produced the corpus, stated so a later pass can re-run it; one ID'd
      row per search hit, carrying `file:line`, the hit line's own
      words, its mechanism classified as one of `command-evidence`,
      `fresh-context-reader`, `same-context-recheck`, or `not-an-instruction`
      (a line that names or discusses verification without instructing any),
      and a disposition of `keep`, `narrow`, or `remove` with a stated ground. Every count in the
      note is pinned to a named measurement commit and marked
      `— observed YYYY-MM-DD`. Its `INDEX.md` line, its provenance block, and
      its `TestShippedPageStateLedger` pin all land in the same milestone, with
      the work-log justification the ledger contract requires.
- [ ] AC2 — Every row dispositioned `narrow` or `remove` is applied in the
      shipped prose. For a `remove` row, a grep over the working tree for that
      row's quoted instruction returns hits only in the ledger,
      `cairn/DECISIONS.md`, milestone files, and `milestones/archive/`. For a
      `narrow` row, whose hit line may be one physical line of a multi-line
      instruction, the check is that the instruction's operative clause no
      longer reads as it did at the measurement commit, with the shipped
      replacement quoted in that row's ground. No row lacks a disposition, and
      the count of rows in the ledger equals the count of hits the AC1 search
      returns at the measurement commit.
- [ ] AC3 — A `cairn/DECISIONS.md` entry disposes of D-067's two instruments
      separately — the plan-gate criteria audit and the `guard-doctrine.md` §8
      description-layer certification — each as `keep unchanged`, `narrow`, or
      `retire`. The entry states, per instrument, what it caught across M115
      through M119, read from those milestones' Review sections and work logs
      and cited by file, against what it cost in rounds; it cites
      `prompting-opus-5` for the guide's finding. Any disposition other than
      `keep unchanged` names D-067 as superseded in the entry's heading; a
      `keep unchanged` restates D-067's own falsifier as still standing.
- [ ] AC4 — `tracking-rules.md`'s "Model and agent strategy" section states
      which class of self-checking the delegation guidance governs and which it
      does not, naming both an author re-checking its own output and an
      independent fresh-context reading of it. A prose-guard asserts a phrase
      from each of the two named classes, each phrase occurring within a single
      physical line of the shipped file, and each carries its own entry in
      `skills/tests/test_mutation_harness.py`.
- [ ] AC5 — Any instruction the ledger removes or narrows in a file carrying a
      prose-guard has that guard's asserted phrases re-checked against the
      shipped bytes, and `python3 -m unittest` over `skills/tests`,
      `scripts/tests` and `hooks/tests` is green from the repo root with each
      exit code checked separately.

## Coverage

- AC1 → T1, T2, T6
- AC2 → T3
- AC3 → T4
- AC4 → T5
- AC5 → T3, T5

## Tasks

- [x] T1 — Run the corpus search over the nine `skills/*/SKILL.md` files and
      the five `skills/shared/*.md` modules; record the exact command and its
      raw hit list. Pin the measurement commit.
- [x] T2 — Classify each hit by mechanism and author the ledger from the
      synthesis-note template, with a disposition and ground per row. A row is
      `same-context-recheck` only where the instruction has the agent re-read
      work it just produced, with the context that produced it.
- [x] T3 — Apply every `narrow` and `remove` disposition to the shipped prose.
      After each edit, grep every nearby guard's asserted substring for
      contiguity on one physical line (LESSONS 2026-07-20/M104), and re-run the
      three suites with exit codes checked.
- [x] T4 — Read M115–M119's Review sections and work logs for what each of
      D-067's instruments caught and what it cost; author the DECISIONS entry
      per AC3. Show it verbatim in chat before its commit.
- [x] T5 — Write the self-checking-class rule into "Model and agent strategy";
      guard + per-phrase mutation entries; verify each reddens when blanked.
- [x] T6 — `INDEX.md` line and `TestShippedPageStateLedger` pin for the ledger
      page, with the work-log justification line.

## Work log

- 2026-07-27: created by /milestone-plan.
- 2026-07-27: plan gate chose reopening D-067's two readers over triaging only the same-context rechecks, at the user's direction, because the guide's advice against subagent self-verification reaches them even though its stated mechanism (an author's own re-read) does not; falsified by the M115–M119 evidence showing either reader caught a defect no later gate would have.
- 2026-07-27: plan chose a committed synthesis note over an in-milestone ledger because the classification is the artifact a later re-decision re-reads, which is the owed-applied-to-time test; falsified by nothing outside this milestone citing the ledger.
- 2026-07-27: plan chose a search-scoped criterion over a list of the 19 instructions a plan-time subagent found because a criterion that lists its sites becomes the sweep and omits what it never named (LESSONS 2026-07-27/M118); falsified by the search returning a corpus a reader judges materially incomplete.
- 2026-07-27: implement started on branch `m121-verification-triage`; status → in-progress.
- 2026-07-27: implement question gate chose the 79-hit term set (verify family + `re-read`/`confirm`/`self-check`, excluding `audit`) over 65 (verify family only) and 114 (+`audit`); measured at 684e53a, `audit` adds 35 lines of which all but `/milestone-plan:86`'s criteria audit name the health-audit feature rather than instruct a check, and AC3 reaches that instrument by name regardless.
- 2026-07-27: AC1 amended at the gate — mechanism vocabulary gains a fourth value `not-an-instruction`, because AC2 pins rows to hits and the three original values all presuppose the line is an instruction, leaving a hit like `tracking-rules.md:195` with no legal classification and dropping it silently against IP3.
- 2026-07-27: task order — T4's evidence read ran before T2's ledger authoring (minor amendment), because the ledger's eleven `fresh-context-reader` rows inherit whatever disposition AC3 reaches, and authoring them twice would have been the restatement guard-doctrine §6 warns about.
- 2026-07-27: D-067 disposition gate — the criteria audit takes `narrow` (kept, plus a mandatory work-log line either way) over `keep unchanged` and `retire`, because M117 and M119 carry no audit record at all, so "did not run" and "ran and found nothing" are indistinguishable and the instrument's yield is unmeasurable; falsified by a milestone recording the line and the line proving to carry no information a reader uses.
- 2026-07-27: D-067 disposition gate — §8 takes `narrow` (a stopping bound on what a round returns) over `retire` and `keep unchanged`, because round 1 returned real defects in every milestone that ran it (M116 9, M117 8, M118 16, M119 2 code defects) while rounds 5-9 of M119 returned zero shipped-behaviour defects and re-certified the previous round's own fix comments; falsified by a bounded round 1 still averaging multiple returns.
- 2026-07-27: T3 — §8's unbounded loop narrowed at `guard-doctrine.md:284,297` and the routing bar at `milestone-implement/SKILL.md:102`; the criteria audit gains a record requirement at `milestone-plan/SKILL.md` step 3, cross-referenced from `milestone-brief/SKILL.md` (step 0, one home). Two guard asserts re-anchored, five added, five mutation entries added; three suites green, exit 0 each.
- 2026-07-27: T5 — the self-checking-class rule lands in "Model and agent strategy" naming both classes; two asserts (one per class, each a single physical line) with their own mutation entries. The guide's third delegation clause ("do not use subagents to verify or double-check your own work") reads onto D-067's readers only if the classes are unnamed, which is the misreading this rule blocks.
- 2026-07-27: T4 — D-079 appended: both D-067 instruments narrowed, not retired. §8's falsifier is recorded as FIRED (4.5-round average over M116-M119) with its prescribed remedy declined on the evidence — round 1 returned real defects in all four milestones and the waste sits in rounds re-certifying the previous round's own fix comment. Supersedes D-067's unbounded loop and the "don't tune it" half of the falsifier; annotates D-069.
- 2026-07-27: T1/T2/T6 — `references/self-verification-ledger.md` authored from the synthesis-note template: 79 rows at 684e53a, one per hit, with mechanism and disposition each. The measurement: 31 `command-evidence`, 36 `not-an-instruction`, 11 `fresh-context-reader` (D-067's two instruments), and exactly ONE `same-context-recheck` (`guard-doctrine.md:36`) — so the guide's over-verification finding lands almost entirely on D-067 and nearly nowhere else in cairn's prose. INDEX line + `TestShippedPageStateLedger` pinned `exempt`, on M118's ledger footing: the corpus is this repo at a named commit, re-derived by the page's own search rather than re-read against an external source.
- 2026-07-27: AC2 amended at a mini gate — its grep clause assumed every applied disposition would be a deletion, but both `narrow` instructions span two physical lines and in each case the sweep hit the line that did not change (V24 at `:102` while `:103` changed; V48 at `:285` while `:284` changed), so the clause was unsatisfiable by construction for a `narrow`. Now: `remove` keeps the disappearance grep, `narrow` quotes its operative clause before and after in the row's ground. Rejected at the gate: reflowing the paragraphs so the quoted lines change, which fits the work to the test.
- 2026-07-27: three cited row IDs in the ledger's Disposition section were wrong on first draft (V45/V27/V51 for V37/V24/V48) — caught by reading them out of the shipped table rather than out of the draft, which is guard-doctrine §6's restatement rule applied to this milestone's own artifact.

- 2026-07-27: §8 description-layer certification, round 1 (fresh-context [O], authored none of this): 1 shipped-behaviour defect + 10 description-layer defects, all resolved.
- 2026-07-27: round 1's shipped-behaviour defect — AC4's rule was invertible with both guards green. Each assert pinned its class phrase but not the verb assigning it, and the two verbs sat on different physical lines because the phrases had been put on their own lines to satisfy AC4's single-line clause; swapping the phrases made the delegation warrant govern the fresh-context reader and exempt the author's own re-read, with the suite green. Fixed by pinning `it governs` / `it does not govern` WITH their phrases on one line; the phrase-swap now reds both asserts (verified by hand, restored, diffed).
- 2026-07-27: round 1 also refuted the §8 disposition itself, and the maintainer re-decided it at a gate. The shipped bound ("stops at the first round returning no shipped-behaviour defect and no regression") reads two ways and fails both: M119's rounds 5-9 EACH returned a real guard-coverage gap, so if gaps are not shipped-behaviour defects the bound fires at round 5 and discards nine later gaps including round 9's forever-WARNing `--- a/|+++ b/` widening, and if gaps count it never fires. Replaced by a scope exclusion on D-069's own object — text a previous round's fix authored opens no further round, while still being fixed, since leaving it unexamined ships the false records §8 exists to catch. `guard-doctrine.md` and D-079 clause (1) rewritten; `milestone-implement/SKILL.md` reverted to unchanged.
- 2026-07-27: correction (supersedes this session's implement-gate line, IP4 — appended, not edited): the `audit` term set's 35 extra lines are 22 health-audit-feature lines, 7 unrelated senses of `audit`/`auditability`, and 6 criteria-audit instruction lines across TWO surfaces (`milestone-plan:39,86,124,125` and `milestone-brief:92,100`) — not "all but `/milestone-plan:86`". The exclusion stands; its stated ground was wrong.
- 2026-07-27: correction (supersedes this session's AC1-amendment line, IP4): `tracking-rules.md:195` is not a hit in the chosen 79-hit set — it appears only under the rejected `+audit` set. The amendment's ground is unaffected and its correct exemplars are `tracking-rules.md:157` and `:297`, both genuine hits with no legal classification under the original three values.
- 2026-07-27: correction (supersedes this session's T3 line, IP4): the second §8 site is `guard-doctrine.md:298`, not `:297`, which is blank; and `milestone-implement/SKILL.md:102` is no longer edited at all after the re-decision above.
- 2026-07-27: AC1 and AC5 amended at the same gate — AC1 said "one row per instruction found" while the ledger ships one row per search HIT (36 rows are `not-an-instruction`, which AC2's row-count clause requires), and AC5 covered only what the ledger `removes` while nothing was removed and two guards were re-anchored for narrowings. Now "per search hit" / "the hit line's own words", and "removes or narrows in".
- 2026-07-27: round 1's remaining description-layer defects, all fixed: four unstamped counts in the ledger; the ledger's "M121 edited two of these files" (four edited, hit lines moved in two); "two of the five milestones after adoption" shipped in `/milestone-plan` (D-067 was adopted BY M115, so the five after are M116-M120 and three carry no record — M117, M119, M120); three D-079 citations reading as live paths when the files are archived; two stale test docstrings; and a "(step 0, one home)" reference sitting where it read as a `/milestone-brief` step number.

- 2026-07-27: §8 round 2 (second fresh-context [O], did not do round 1): 0 shipped-behaviour defects, 0 regressions, 12 description-layer defects, all fixed. It inverted every rule this milestone ships — the two class phrases, the phrase-verb pairing, `opens no further round`, `It is still fixed`, `did not run`, `records one work-log line either way` — and each reddened.
- 2026-07-27: round 2's one acceptance-criterion failure — AC3 requires a non-`keep unchanged` disposition to name D-067 as SUPERSEDED in the heading, and round 1's rewrite had left the heading naming only the falsifier clause. Heading now reads "narrowly supersedes D-067, at the \"don't tune it\" half of §8's falsifier", the D-071/D-056 form.
- 2026-07-27: round 2 corrected D-079's own evidence — M115's plan-time criteria re-read was the AUTHOR's, standing in for the instrument M115 was building, and M115's work log says so verbatim; the instrument's measured firings are two (M116, M118), not three. The disposition is unchanged: both firings were productive and the record gap is what `narrow` answers.
- 2026-07-27: correction (supersedes this session's T3 line, IP4 — appended, not edited): `guard-doctrine.md` has ONE edited site, the paragraph inserted at `:298`; `:284` ships byte-identical to main and `milestone-implement/SKILL.md` is unchanged, both after the round-1 re-decision. Zero asserts were re-anchored in the net diff, and T3's contribution is six asserts and six mutation entries, not five. This supersedes both the original T3 line and this session's earlier `:297`→`:298` correction, which itself said "the second §8 site" when there is only one.
- 2026-07-27: correction (supersedes this session's T4 line, IP4): D-079 no longer supersedes "D-067's unbounded loop" — that clause was withdrawn when the round bound was, and the shipped heading narrowly supersedes D-067 at the falsifier's "don't tune it" half while EXTENDING D-069's scope bound rather than annotating it.
- 2026-07-27: correction (supersedes this session's round-1 line, IP4): hit line numbers move in ONE corpus file, `tracking-rules.md` (+14 from `:670`), not two — `guard-doctrine.md`'s inserted paragraph sits below its last hit at `:294`. Four corpus files are edited, as stated.
- 2026-07-27: round 2's remaining fixes, all description-layer: the ledger still called §8's narrowing a "stopping bound" in three places (the locked-rules pointer and two row grounds); one count carried its measurement commit without its `— observed` stamp; `guard-doctrine.md` stated "rounds 5-9 returned zero code defects" without M119's own "apart from round 7's live false positive" carve-out, and its "eleven record errors in an earlier round's fix text" is now "eleven record errors, ten of them in an earlier round's own fix text", which is what the record supports; D-079's M119 citation `:99-124` narrowed to `:99-123` with the override at `:125`.

- 2026-07-27: §8 gate entered at zero unresolved after round 2, and the judgment is recorded because the author is applying its own new rule for the first time. Round 2 returned 0 shipped-behaviour defects and 0 regressions, and independently inverted every rule this milestone ships. Of its 12 findings, 5 had round 1's fix text as their only subject — the class D-079 (1) fixes without reopening — and the 7 in-scope ones were count and citation precision in original text, all fixed. A round 3's only new surface would be round 2's own fixes, which is exactly what the shipped exclusion covers, so it is not required; a reviewer who reads that as self-serving should say so at the gate.
- 2026-07-27: status → review. Three suites green from the repo root with exit codes checked separately (skills 697, scripts 332, hooks 98); `cairn_validate` all checks passed; plan-owned body 108/149.

- 2026-07-27: REVIEW GATE FAILURE, return 1. AC1 fails: the ledger's printed corpus search is not re-runnable as written — run literally as `git grep <rev> -- <pathspec>`, git's wildmatch lets `*` cross `/`, so `skills/shared/*.md` also matches `profiles/` and `templates/` and the command returns 119 hits, not 79; the 79 came from unquoted shell-glob expansion against the working tree, which no later pass can reproduce from the page. AC2's row-count clause fails with it (79 != 119). Also blocking: the same search returns 83 hits at HEAD with four of M121's own lines unclassified; three sentences invert with the suite green (`tracking-rules.md:676-677`, `:678-679`, `guard-doctrine.md:307-310`); the eleven-vs-ten measurement contradicts across three files; two partial-pin asserts; and D-079's exclusion does not engage D-070's work-vs-process carve-back. Status → in-progress.

- 2026-07-27: blocked on RB09 — the §8 scope exclusion's soundness escalated at the user's gate, per the rule that the implementing session never authors the durable verdict on the review constraining it. Three grounds carried: F-BH2 (80, contradicts D-070's work-vs-process carve-back), F-A2 (74, inert on its own motivating case or else it discards round 9's forever-WARN finding), F-A5 (62, composed with D-069 it is a round bound by another route and suppresses its own falsifier). The eight mechanical review findings are independent of the outcome and are fixed on the branch meanwhile.

- 2026-07-27: review fixes, the four independent of RB09's outcome. F-C1 (87) — the ledger's corpus search now writes its fourteen paths out instead of globbing: a pathspec is not a shell glob, git's wildmatch lets `*` cross `/`, and the printed command returned 119 hits when run literally while the 79 came from the shell expanding globs against the working tree. Re-verified: the page's own command now returns 79, equal to its row count. F-B1 (88) and F-B2 (86) — the discriminator sentence and the loop-bound sentence were rewrapped onto single physical lines and each gained an assert; both inversions now red. F-PR1 (80) — the two class asserts stopped at the em-dash, so each rationale clause deleted green; both clauses gained an `assertRegex` spanning the wrap. Five asserts and four mutation entries added; all four inversions verified by hand, restored, diffed. Three suites green, exit 0 each.
- 2026-07-27: four findings deliberately NOT fixed while RB09 is open, because all four sit in text the review may rewrite — F-B3 (90, §8's evidence sentence), F-A1 (88, the eleven-vs-ten measurement spanning D-079 and §8), F-PR2 (85, the assert on §8's exclusion sentence), F-C3 (85, four unclassified hits, one of them inside the §8 paragraph). Fixing them now would guarantee rework.

## Decisions

- 2026-07-27 (RR09 ingest): **Q1 — the exclusion's framing contradicts D-070, its substance is reconcilable.** RR09 finds D-079 and §8 placed the exclusion on the "certified scope", the object D-070 ruled on by subject matter, without naming D-070; but excluded findings are still checked and fixed, so they never leave D-070's scope — they lose only the power to reopen a round. The fix is a two-axis discriminator: subject matter draws what is checked and fixed, provenance draws what reopens. Travels to the banked rebuild.
- 2026-07-27 (RR09 ingest): **Q2 — objection B confirmed and sharpened; this is the finding that decided the disposition.** Every one of M119's rounds 5-9 coverage-gap findings sat in fix-authored surface. Under the description-layer reading the exclusion is exactly inert on M119 — zero rounds saved, zero findings lost, the loop still ends by override. Under the broad reading it stops at round 5, the withdrawn round bound's own stopping point, losing round 9's forever-WARN widening set. The two readings are objection B's two horns, selected by an undefined noun.
- 2026-07-27 (RR09 ingest): **Q3 — objection C is real only under the broad reading**, where it is worse than stated; under the description-layer reading rounds >=2 keep the substantive class M119 actually exercised.
- 2026-07-27 (RR09 ingest): **Q4 — the re-armed falsifier is wrong either way**, honest-but-already-failed under one reading and unfireable under the other. RR09 proposes a yield-based replacement; it travels to the rebuild, and D-067's falsifier stands unchanged meanwhile.
- 2026-07-27 (RR09 ingest): **Q5 — verdict (d), rebuild.** Revert-unchanged (b) and outright retirement (c) both rejected with reasons. M121 departs from (b)'s rejection and says so in D-080: the ground is that the rebuild's own criteria set carries ten blocking defects, not that RR09 is wrong.
- 2026-07-27 (RR09 ingest): **Q6 — the text/record switch judged real and blocking**, plus four further prose defects and a live contradiction with §8's unamended "fixed and re-certified" clause. All moot for now: the paragraph is withdrawn.
- 2026-07-27 (RR09 ingest): **Beyond the brief, B2 — M121's own §8 gate entry was not licensed by the rule it applied.** Round 2 returned seven in-scope findings in original text, which the unamended re-certification clause obliges a further round to confirm; the gate entry's ground was prospective and the shipped rule nowhere provided it. Now moot in the same way — the exclusion is withdrawn and §8 is back to its pre-M121 bytes, under which round 2's fixes were confirmed by operation (three suites, `cairn_validate`) and no round 3 was owed on the exclusion's account. Recorded rather than dropped, because the gate entry's stated ground was wrong when made.

- 2026-07-27: RR09 ingested. Criteria audit of its binding-criteria set (D-067 instrument 1, fresh-context [O] that authored none of them) returned TEN BLOCKING findings and nine judgment calls — recorded per D-079 clause 2's requirement that the audit record one work-log line either way. Verified first-hand: RR09's `- **BCn** —` bullets parse to `{}` under the shipped `_BC_HEAD`, so setting `Driving RR: RR09` would FAIL the gate; the BC section is 59 lines against 41 of headroom (D-066(4) territory); and D-065 forbids the in-place D-079 amendment BC3 mandates.
- 2026-07-27: correction owed to the record — RB09 supplied a FALSE CONSTRAINT. It told the reviewer that "D-079 has not merged, so the authoring milestone may still amend it in place (M115's precedent)". D-065 says IP4 attaches at append time, not merge time, and was written to close exactly that M115 precedent. The reviewer took the constraint as instructed, so BC3 mandates an IP4 violation. The error is the brief's, not the review's; recorded in D-080 so a later reader does not treat BC3 as usable.
- 2026-07-27: at the ingest gate the maintainer chose to drop §8 from M121 rather than rebuild it here or re-brief. `guard-doctrine.md` is byte-identical to `main` again; the three exclusion asserts and three mutation entries went with it. D-080 supersedes D-079's clause 1 and its heading's exclusion claim; clauses 2 and 3 stand. The rebuild is banked on the ROADMAP's existing §8 row, rewritten in place (ROADMAP is current knowledge, D-045/D-052) with RR09 as its evidence — which also closes review finding F-D5 (78).
- 2026-07-27: the revert closes three deferred review findings outright — F-B3 (90), F-PR2 (85) and F-A1 (88) all sat in the withdrawn paragraph or the D-entry D-080 now supersedes; `grep eleven skills/` returns nothing. F-C3 (85) is closed by disclosing in the ledger that the search returns 82 at HEAD, three of them M121's own self-checking rule, classified `not-an-instruction` on the page's own vocabulary.
- 2026-07-27: RB09/RR09 relocated to `cairn/reviews/archive/`; status → in-progress.

- 2026-07-28: review pass 2 opened. All five AC boxes UNTICKED first: pass 1's evidence was gathered at `b4fdfe5`, before the RR09 revert removed the §8 exclusion and its guards, so those ticks stood on evidence about a branch state that no longer exists — AC fencing treats an already-ticked criterion without fresh recorded evidence as unverified. Status in-progress → review; the transition is logged here because the routing chip sent this session straight to review rather than back through `/milestone-implement`.

## Review

**Fresh evidence, 2026-07-27** (branch `m121-verification-triage` at `b4fdfe5`,
cut from `origin/main` and still containing it — no merge needed; PR #121).

**AC1 — the ledger page.** `cairn/references/self-verification-ledger.md`
exists and follows `templates/synthesis-note.md`: `**Provenance.**` block with
`Ingested`/`Pagination:`/`Extraction:` (one physical line, one alternative,
`— observed 2026-07-27`), `**Scope.**`, `**Evidence snapshot.**`, six `##`
sections ending in `## Open questions`. The corpus search is printed in the
page and re-runs: executing the page's own command returned **79 hits**, and
the `file:line` list matches the table's 79 rows exactly, in order. Every row
carries `file:line`, the hit line's own words, a mechanism from the four-value
vocabulary, a disposition, and a ground — 0 rows missing any of the four.
Mechanism counts read off the shipped table: `command-evidence` 31,
`not-an-instruction` 36, `fresh-context-reader` 11, `same-context-recheck` 1,
summing to 79. The measurement commit `684e53a` is named and nine
`— observed 2026-07-27` stamps carry the counts. `INDEX.md` line present (1
match); `TestShippedPageStateLedger` pins the page `exempt` at
`scripts/tests/test_scripts.py:1436`, with its justification in the class
comment and in the work log.

**AC2 — dispositions applied, and the counts.** 0 rows take `remove` and 0 take
`narrow`, so both applied-disposition arms are **vacuously satisfied** — recorded
plainly rather than as a pass, since nothing exercised them. What does bind is
met: 0 rows lack a disposition, and the ledger's 79 rows equal the 79 hits the
AC1 search returns at `684e53a`, re-measured above by re-running the command the
page prints. The two rows a first pass marked `narrow` (V24, V48) are `keep` at
HEAD: §8's narrowing is a scope exclusion added beside the instrument, and it
rewrites no line in the corpus.

**AC3 — D-079 disposes of both instruments.** `cairn/DECISIONS.md` D-079
disposes of the two separately, each `narrow`: instrument 1 the plan-gate
criteria audit, instrument 2 `guard-doctrine.md` §8 description-layer
certification, both named in those words. Per instrument it states what was
caught against what it cost, cited by file: M115's gated AC2/AC6 amendments
(archive, Decisions) with the entry's own correction that this re-read was the
plan author's own; M116's jointly-unsatisfiable {AC2, AC5, AC6} and four
drafting defects (`M116-…md:52`, pre-archive at `32122ab^`); M118's four
gate-bound ambiguities (`M118-…md:193`, pre-archive at `c76fa65^`); M117 and
M119 recorded as carrying no audit record. §8's cost in rounds: M116 two (9+2),
M117 four (8→6→6→2), M118 three (16→10→2), M119 nine, average 4.5. It cites
`prompting-opus-5` for the guide's finding and quotes it. Because both
dispositions are other than `keep unchanged`, the heading names D-067 as
superseded, in the D-071/D-056 form.

**AC4 — the self-checking-class rule.** `tracking-rules.md` "Model and agent
strategy" states both classes at `:669` and `:673`, each on a single physical
line: "It governs **an author re-checking work it just produced, in the context
that produced it**" and "It does not govern **an independent fresh-context
reading of that work by a reader that authored none of it**". Each is asserted
by its own test in `skills/tests/test_delegation_warrant.py`
(`TestSelfCheckingClassRule`, `:93` and `:100`) and each carries its own
`skills/tests/test_mutation_harness.py` entry (`:3346`, `:3352`). Falsifiability
verified by inversion rather than by blanking: swapping the two class phrases
between the lines, leaving the verbs in place, reds both asserts; restoring
returns the suite to green and the diff to the intended change only.

**AC5 — suites green, exit codes separate.** Run from the repo root, each exit
code captured on its own: `skills/tests` 697 tests OK exit 0; `scripts/tests`
332 tests OK exit 0; `hooks/tests` 98 tests OK exit 0. The re-check clause is
**vacuous** — no ledger row removes or narrows an instruction — recorded as
such. The re-anchoring that did happen (§8's two asserts during the withdrawn
round-bound, reverted at HEAD) is visible in the branch history, not in the net
diff.

**Consistency gate.** `cairn_validate` exit 0, all checks passed — 16 PASS, 8
advisory OK, no WARN. No `DESIGN.md` principle changed in the diff, so
`cairn_impact --changed` does not apply. The active profile is `generic`, whose
`consistency-gate` slot names **none**, so the toolchain half is a clean no-op.
Returns to `in-progress` this milestone: **zero** — the thrash rule does not
fire.

### Independent fresh-context review (three lenses + scorer), 2026-07-27

Three reviewers with distinct evidence bases, all instructed to report every
candidate finding and filter nothing; a separate `[S]` scorer that generated
none of them scored each 0-100 against the rubric. Diff-bug `[O]` 30 findings,
blame-history `[S]` 5, prior-review `[S]` 2 (its `gh api` probe found zero
inline PR comments repo-wide, so archived `## Review` sections and the open
ROADMAP candidate rows were its whole evidence base). Four claims were
re-measured first-hand before scoring; two of those refuted a reviewer.

**GATE FAILURE — the milestone returns to `in-progress`.** Two of the nine
80+ findings are acceptance-criterion failures, both verified by command rather
than accepted on report.

**Actioned (scored 80+), all returned to `/milestone-implement`:**

- **F-B3 (90)** `guard-doctrine.md:307-310` — "Every round in that stretch also
  returned a real guard-coverage gap, so a bound on *rounds* would have
  discarded work that was still finding defects" inverts to "No round..." with
  the suite green. This is the one sentence carrying D-079's scope-vs-rounds
  argument. Verified: inversion run, suite green, restored.
- **F-A1 (88)** `DECISIONS.md:2662` / `guard-doctrine.md:306` /
  `test_fresh_context_readers.py:281` — the same measurement reads "eleven ...
  in an earlier round's own fix text" in two places and "eleven ... ten of them
  in an earlier round's own fix text" in the third. The round-2 fix corrected
  one site of three; the D-entry is history under IP4 and needs a superseding
  correction rather than an edit.
- **F-B1 (88)** `tracking-rules.md:676-677` — "The discriminator is *who
  reads*, never *how often the work is read*" inverts with the suite green.
  This is the sentence telling a reader how to apply AC4's two classes;
  inverted, §8's loop sorts into the governed class. Verified.
- **F-C1 (87)** `references/self-verification-ledger.md:22-24` — **AC1
  failure.** The printed search is not re-runnable as written: run literally as
  a `git grep <rev> -- <pathspec>`, git's wildmatch lets `*` cross `/`, so
  `skills/shared/*.md` also matches `profiles/` and `templates/` and the command
  returns **119** hits. The 79 arises only from unquoted shell-glob expansion
  against the working tree. Verified first-hand; AC2's row-count clause fails
  under the literal reading (79 != 119).
- **F-B2 (86)** `tracking-rules.md:678-679` — "A fresh reader's own loop is
  bounded by its instrument, never by this rule" inverts with the suite green.
  Verified.
- **F-PR2 (85)** `test_fresh_context_readers.py:292-300` — the assert stops at
  "ship it", leaving the clause stating WHY an excluded finding does not reopen
  a round pinned by nothing.
- **F-C3 (85)** `references/self-verification-ledger.md:79-86` — the same
  search returns **83** hits at HEAD, four of them M121's own prose
  (`guard-doctrine.md:310`; `tracking-rules.md:666`, `:669`, `:672`),
  unclassified. The page's own re-run protocol yields four unexplained hits on
  the next pass. Verified first-hand.
- **F-PR1 (80)** `test_delegation_warrant.py:91-103` — both new asserts pin only
  the bolded lead clause to the em-dash, leaving each rationale clause unpinned.
  The partial-pin class an open ROADMAP candidate row (M114 pass 8, re-evaluated
  at M116's plan gate, never dropped) already tracks.
- **F-BH2 (80)** `DECISIONS.md` D-069/D-070 vs D-079 — D-070 carved D-069 back
  so that defects in *records about the work* stay inside the certified scope,
  leaving only certification narrative outside it. D-079's exclusion reclassifies
  that same category out by a different axis (who authored the text, not what it
  is about) and frames itself as extending D-069 without engaging D-070.

**Logged below threshold (24 findings, surfaced not dropped — IP3):**
F-D5 78 stale ROADMAP candidate row whose promotion condition M121 just met ·
F-C13 75 ledger says it "produced rules" when it produced none · F-A2 74 the
exclusion may be inert on its own motivating case · F-A3 74 "text" vs "record"
switch mid-sentence, undefined · F-D4 74 step-0 one-home tension with M120's
freshness sentence · F-C8 74 no stated precedence between two mechanism values ·
F-C10 72 `exempt` pin rests on a frozen-corpus precedent while this corpus is
live · F-C5 70 V30/V32 arguably misclassified `command-evidence` · F-D2 68 Scope
In-list omits three of four edited surfaces · F-D3 65 docstring gets which half
is novel backwards · F-C4 65 `profiles/` not named in Open questions · F-D1 62
no criterion binds the §8 prose change directly · F-A5 62 exclusion composes
with D-069 into a de facto round bound · F-C7 55 `fresh-context-reader` defined
by its own extension · F-A4 50 the author decides which findings are excluded
(self-disclosed) · F-C11 45 some counts unpinned to a commit · F-C6 42 seven
`fresh-context-reader` rows are arguably descriptive prose · F-C14 35 "no
vocabulary beyond four values" vs a second interpretive rule · F-C12 35 two
`— observed` stamps wrap · F-C9 30 six quotes "padded" (refuted on inspection:
CommonMark double-backtick delimiters) · F-BH5 30 AC2's check fires on nothing
(self-disclosed) · **F-A6 25 REFUTED** — "code defects" matches M119's own
vocabulary · F-A7 25 ambiguous antecedent, all citations resolve · **F-C2 15
REFUTED** — the 65/79/114 figures reproduce exactly at `684e53a`.

**Thrash count: return 1 of this milestone.** Neither trigger fires — (a) needs
a third return, and (b) needs one criterion failing twice by the same shape.
