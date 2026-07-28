# M121: Verification triage — classify every self-verification instruction, and re-decide D-067's two fresh-context readers

- **Status:** review
- **Priority:** normal
- **Depends on:** M120
- **Driving RR:** —
- **Principles touched:** IP3
- **Branch/PR:** `m121-verification-triage`

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

## Decisions

## Review
