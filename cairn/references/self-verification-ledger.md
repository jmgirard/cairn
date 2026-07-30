# Self-verification instructions in cairn's shipped prose, classified (M121)

**Provenance.** Ingested 2026-07-27 by M121 from a first-hand sweep of this
repo's own shipped skill and module prose at commit `684e53a` — the nine
`skills/*/SKILL.md` files and the five `skills/shared/*.md` modules — read
against the over-verification finding in `prompting-opus-5.md`
(§ Task scope and over-verification).
Pagination: —.
Extraction: first-hand record, nothing to re-verify against — the corpus is this repo at a named commit, and the search below re-derives it exactly — observed 2026-07-27.

**Scope.** This is the classification ledger behind D-079, not a source
summary: it owns no external source and asserts nothing about any. It builds no
new machinery — no check, no advisory, no vocabulary beyond the four mechanism
values M121's AC1 fixes. It is a reference, not an authority: status lives in
`ROADMAP.md`, decisions in `DECISIONS.md`, architecture in `DESIGN.md`.

**Evidence snapshot.** One command over one commit. A later pass re-runs it and
diffs the hit list against the table below.

- The corpus search, run from the repo root — 79 hits — observed 2026-07-27.
  **The fourteen paths are written out rather than globbed**, because a
  pathspec is not a shell glob: git's wildmatch lets `*` cross `/`, so
  `skills/shared/*.md` as a pathspec also matches `skills/shared/profiles/*.md`
  and `skills/shared/templates/*.md` and returns 119. The 79 arose from the
  shell expanding those globs against the working tree, which makes the corpus
  depend on the tree a later pass happens to have rather than on the revision
  named in the command. Written out, the command reproduces under any shell
  and any quoting (M121 review F-C1):

  ```
  git grep -nEi 'verify|verifies|verified|verification|re-?check|double-?check|certif|sanity|re-?read|confirm|self-check' 684e53a -- skills/cairn-init/SKILL.md skills/cairn-release/SKILL.md skills/design-interview/SKILL.md skills/hotfix/SKILL.md skills/milestone-brief/SKILL.md skills/milestone-implement/SKILL.md skills/milestone-plan/SKILL.md skills/milestone-review/SKILL.md skills/milestone/SKILL.md skills/shared/guard-doctrine.md skills/shared/migration-protocol.md skills/shared/records-hygiene.md skills/shared/tracking-rules.md skills/shared/validation-doctrine.md
  ```

- The term set was chosen at M121's implement gate over a narrower one (65
  hits: the verify family alone) and a wider one (114 hits: `audit` added).
  Of `audit`'s 35 extra lines, measured at `684e53a`: 22 name `/milestone`'s
  health-audit feature, 7 use `audit`/`auditability` in unrelated senses
  (`tracking-rules.md:495`, `:698`; `validation-doctrine.md:47, 53, 55, 59,
  60`), and 6 are the criteria-audit instruction, across two surfaces —
  `milestone-plan/SKILL.md:39, 86, 124, 125` and
  `milestone-brief/SKILL.md:92, 100`. Those 6 are the real cost of the
  exclusion, and it is paid because D-079 reaches that instrument by name
  rather than through a row here — observed 2026-07-27.
- `skills/design-interview/SKILL.md` is in the corpus and returns zero hits —
  observed 2026-07-27.
- **The same search returns 82 hits at M121's own HEAD, not 79.** Three are
  M121's own prose — `tracking-rules.md:666`, `:669` and `:672`, the
  self-checking-class rule (D-079 clause 3), which names and discusses
  verification without instructing any and so classifies `not-an-instruction`
  on this page's own vocabulary. Those three are the whole difference: content-diffing the
  two hit lists gives three additions and no removals, the rest being
  line-number shift. A later pass re-running the command at
  `684e53a` gets the 79 this table holds; re-running it at a later commit
  should expect its own additions and diff them, not against this table
  (M121 review F-C3) — observed 2026-07-27.

## What the guide's finding says, and what it therefore reaches

The guide reports that explicit self-verification instructions "cause
over-verification on Claude Opus 5, and removing them reduces wasted tokens
with no loss in quality", on the stated mechanism that "Claude Opus 5 verifies
its own work without being told to". The mechanism is a claim about **an author
re-reading its own fresh output**. It says nothing about an instruction that
goes and reads an artifact, and nothing about a reader that authored none of
what it reads. That is what the mechanism column below separates.

## Mechanism vocabulary

- `command-evidence` — the instruction gathers evidence from outside the
  agent's own context (runs a command, reads a file or a tool's output) and
  reads the result. This is the guide's own preferred pattern; M121's Scope
  classifies the whole class `keep` without further work.
- `fresh-context-reader` — the instruction is, or is part of, an independent
  reading by an agent that authored none of what it reads. D-067's two
  instruments, and nothing else in the corpus.
- `same-context-recheck` — the instruction has the agent re-read work it just
  produced, with the context that produced it. The guide's target class.
- `not-an-instruction` — the hit uses a verification word without instructing
  any self-check: prose describing a rule, a slot or feature name, a
  status-table cell, a user-approval gate, an example of a bad claim.

Dispositions are `keep`, `narrow`, `remove`, and they are **per instruction, not
per instrument**: an instrument narrowed at one of its lines leaves its other
lines `keep`, and D-079 is where the instrument-level disposition lives.

**No row below takes `narrow` or `remove`, and that is the result rather than
an omission.** D-079 narrows the criteria audit by adding a record
requirement, which rewrites no instruction already in this corpus. It also
narrowed §8, and **that half was withdrawn at D-080** on RR09's evidence, so
`guard-doctrine.md` ships byte-identical to its pre-M121 state and every §8 row
below describes prose this milestone leaves untouched. A first
pass did reword two hit lines' neighbours and marked those rows `narrow`, and
the §8 certification found the reasoning behind it wrong — the round-bounding
rule it implemented would have stopped M119's loop two rounds before a live
false positive was found. Both rows are `keep`: their own words stand.
M121's AC2 still carries the amended `narrow` check, which now fires on
nothing — observed 2026-07-27.

Quotes are the hit line verbatim, so each is directly greppable. Where a line
contains a table pipe, the longest pipe-free run carrying the instruction is
quoted instead. `file:line` is at `684e53a`. M121 edits four of the fourteen
corpus files — `milestone-brief`, `milestone-plan`, `guard-doctrine.md`,
`tracking-rules.md`. M121 edits **three** of the fourteen corpus files at
HEAD — `milestone-brief`, `milestone-plan` and `tracking-rules.md`;
`guard-doctrine.md` was edited and then restored byte-identical when D-080
withdrew the §8 exclusion. Hit line numbers move in one file,
`tracking-rules.md`, whose insertion at `:666` shifts every hit from `:670`
onward by **+15** (670→685, 725→740, 733→748, 755→770, 811→826, 819→834). In
the other two the edit lands after the file's last hit. Measured at `baf2fbb` —
observed 2026-07-28.

## The ledger — 79 rows, one per hit at `684e53a` — observed 2026-07-27

| # | file:line | The instruction's own words | Mechanism | Disposition | Ground |
|---|---|---|---|---|---|
| V01 | `cairn-init/SKILL.md:26` | `(hooks.json) — best-effort, unverified on Windows (DESIGN Known` | `not-an-instruction` | `keep` | a DESIGN known-issue statement about Windows |
| V02 | `cairn-init/SKILL.md:58` | `language-specific commands (tracking-rules "Toolchain profiles"). Confirm the` | `not-an-instruction` | `keep` | a user-approval gate on the profile choice |
| V03 | `cairn-init/SKILL.md:135` | ``verbatim; the repo edits its slots (notably `verify`) afterward as needed.`` | `not-an-instruction` | `keep` | names the `verify` profile slot |
| V04 | `cairn-init/SKILL.md:143` | `DESIGN Purpose & Scope; and **numeric-work-needs-oracle-verification**` | `not-an-instruction` | `keep` | the name of a greenfield opener question |
| V05 | `cairn-init/SKILL.md:192` | `- **Missing §1 pieces.** Verify every §1 piece exists and is intact; create` | `command-evidence` | `keep` | reads the filesystem for §1 pieces; the subject is the repo, not the agent's output |
| V06 | `cairn-init/SKILL.md:240` | ``Close by re-running `cairn_validate.py`. **A quiet advisory confirms the entry, not the directory** — `check_gitignore_deprecations` reads `.gitignore` alone and never the filesystem,`` | `command-evidence` | `keep` | re-runs `cairn_validate`; the rest of the line bounds what the advisory proves |
| V07 | `cairn-release/SKILL.md:44` | `conventions per DESIGN.md). Confirm the target version with the user.` | `not-an-instruction` | `keep` | a user-approval gate, not a check of the agent's own work |
| V08 | `cairn-release/SKILL.md:54` | ``verification, wide checks, `cran-comments.md`, the version bump, and a`` | `not-an-instruction` | `keep` | names what the r-package release-walk contains |
| V09 | `cairn-release/SKILL.md:69` | `(r-package: the CRAN submission checklist — submit, confirm the email, then` | `not-an-instruction` | `keep` | an item on the checklist the user runs, never the agent |
| V10 | `cairn-release/SKILL.md:90` | `gh release create v<version> --title "v<version>" --notes-file <notes-file> --verify-tag` | `not-an-instruction` | `keep` | a flag inside a `gh` command |
| V11 | `hotfix/SKILL.md:45` | `*Authoring a fix:* write the test that fails because of the bug; confirm` | `command-evidence` | `keep` | runs the new test and reads that it fails |
| V12 | `hotfix/SKILL.md:46` | `it fails; then fix; confirm it passes.` | `command-evidence` | `keep` | runs it again after the fix and reads that it passes |
| V13 | `hotfix/SKILL.md:52` | ``(`git worktree add /tmp/<repo>-verify <default-branch>`) with only the`` | `not-an-instruction` | `keep` | a throwaway worktree path, not an instruction |
| V14 | `hotfix/SKILL.md:58` | `check — adopting a PR means verifying its evidence, not inheriting it.` | `command-evidence` | `keep` | re-runs a contributor's test both directions; the work checked is not the agent's |
| V15 | `hotfix/SKILL.md:60` | ``4. **Gate-lite:** run the active profile's `verify` slot (`cairn/PROFILE.md`;`` | `command-evidence` | `keep` | runs the profile's `verify` slot |
| V16 | `milestone-brief/SKILL.md:81` | ``re-check the plan-owned body with `cairn_budget`; if the added criteria`` | `command-evidence` | `keep` | runs `cairn_budget` and reads the count |
| V17 | `milestone-implement/SKILL.md:23` | `` 1. Verify status is `planned` (fresh start) or `in-progress` / `blocked` `` | `command-evidence` | `keep` | reads the status off the ROADMAP |
| V18 | `milestone-implement/SKILL.md:24` | ``with a resolved blocker (resume). Verify all `Depends on:` milestones are`` | `command-evidence` | `keep` | reads each dependency's status off the ROADMAP |
| V19 | `milestone-implement/SKILL.md:40` | ``profile's `verify` slot before continuing.`` | `command-evidence` | `keep` | re-runs the `verify` slot after a merge from the default branch |
| V20 | `milestone-implement/SKILL.md:59` | ``- Run the active profile's `verify` slot (`cairn/PROFILE.md`; absent →`` | `command-evidence` | `keep` | runs the `verify` slot per task |
| V21 | `milestone-implement/SKILL.md:73` | `` `/milestone-brief`); tier-tag the Agent description ([S]/[O]). Verify `` | `command-evidence` | `keep` | reads a subagent's diff; the work checked is the subagent's, not the session's |
| V22 | `milestone-implement/SKILL.md:86` | ``that grows a plan-owned section re-checks the body with `cairn_budget`;`` | `command-evidence` | `keep` | runs `cairn_budget` after an amendment |
| V23 | `milestone-implement/SKILL.md:99` | `` `verify` slot passes clean (for a toolchain whose profile names a fuller `` | `command-evidence` | `keep` | runs the `verify` slot at completion |
| V24 | `milestone-implement/SKILL.md:102` | ``— `skills/shared/guard-doctrine.md` §8, the author never certifies its own`` | `fresh-context-reader` | `keep` | the §8 routing bar; ships unchanged — D-079 (1)'s narrowing was withdrawn at D-080 |
| V25 | `milestone-plan/SKILL.md:27` | ``1. Confirm nothing else is `in-progress` — run`` | `command-evidence` | `keep` | runs `cairn_next.py` rather than eyeballing the ROADMAP |
| V26 | `milestone-plan/SKILL.md:40` | `audit over a rougher draft certifies text that never ships.` | `fresh-context-reader` | `keep` | the ground for the criteria audit's ordering; D-079 narrows the instrument elsewhere, not this line |
| V27 | `milestone-plan/SKILL.md:59` | `confirm the scopes are distinct and cross-reference.` | `command-evidence` | `keep` | reads the colliding milestone's scope off its file |
| V28 | `milestone-review/SKILL.md:3` | `description: Verify and ship a finished milestone in a cairn repo - fresh evidence for every acceptance criterion, consistency gate, independent code review, and merge on user approval. Use when the user wants to review, verify, finish, ship, or merge a milestone.` | `not-an-instruction` | `keep` | skill frontmatter description |
| V29 | `milestone-review/SKILL.md:34` | `` the tests and the active profile's checks (its `verify` / `consistency-gate` `` | `command-evidence` | `keep` | actually runs the tests and the profile's checks |
| V30 | `milestone-review/SKILL.md:38` | `section-ownership table — and, under AC fencing, tick each verified` | `command-evidence` | `keep` | AC fencing — the tick follows a recorded evidence line |
| V31 | `milestone-review/SKILL.md:40` | `verification mark against recorded evidence, never a change to the` | `not-an-instruction` | `keep` | defines what the tick is, and is not itself a check |
| V32 | `milestone-review/SKILL.md:58` | `evidence is a gate failure, not a pass — treat it as unverified. This` | `command-evidence` | `keep` | an evidence-gated gate rule; a tick without an evidence line fails |
| V33 | `milestone-review/SKILL.md:250` | `re-verify, re-request approval if the fix was nontrivial. When green:` | `command-evidence` | `keep` | re-runs CI after a red-CI fix |
| V34 | `milestone-review/SKILL.md:281` | ``archive any resolved RB/RR pairs; **replace** "Last hygiene check" — overwrite the previous text, never append to it and never demote it to a `Prior:` clause (D-052); verify`` | `command-evidence` | `keep` | runs the weight-cap check at post-merge hygiene |
| V35 | `milestone/SKILL.md:53` | `` remedies, never "let it grow"), then re-run to confirm green. **Exception — a `scaffold present` `` | `command-evidence` | `keep` | re-runs `cairn_validate` after a fix and reads the result |
| V36 | `milestone/SKILL.md:112` | ``- A milestone at `review` with an open unmerged PR → re-check CI now`` | `command-evidence` | `keep` | `gh pr checks`; the stateless-resume rule forbids trusting a remembered state |
| V37 | `shared/guard-doctrine.md:36` | `amendment added, because every anchor was authored before it existed — re-read` | `same-context-recheck` | `keep` | the one same-context recheck in the corpus; fires only after a mid-implementation amendment and reads the guard against the criteria, both artifacts, so it is not the blanket final-verification step the guide names |
| V38 | `shared/guard-doctrine.md:39` | `**Verify by inversion.** Relabel, negate, or transpose the rule in place, run` | `command-evidence` | `keep` | runs the suite under inversion and requires red |
| V39 | `shared/guard-doctrine.md:93` | `green. Anchor on the row, then re-verify by stripping exactly what the test` | `command-evidence` | `keep` | re-runs the test after stripping what it claims to check |
| V40 | `shared/guard-doctrine.md:105` | `external mutation-verification, which proves only that the guard catches the` | `not-an-instruction` | `keep` | states a limit of external mutation-verification |
| V41 | `shared/guard-doctrine.md:140` | `` `spot-checked verified against the source` while the phrasing the templates `` | `not-an-instruction` | `keep` | an example string in a matcher discussion |
| V42 | `shared/guard-doctrine.md:169` | `that it was never verified. When a matcher gains verbs, its negation handling` | `not-an-instruction` | `keep` | describes a matcher failure mode |
| V43 | `shared/guard-doctrine.md:204` | `**A rule inherited from a prior finding is unverified until read out of the` | `command-evidence` | `keep` | reads the rule out of the implementation |
| V44 | `shared/guard-doctrine.md:211` | `re-verify each member *after* the move, not before.` | `command-evidence` | `keep` | runs each moved member through the implementation |
| V45 | `shared/guard-doctrine.md:256` | `## 8. The author never certifies its own guard's coverage` | `fresh-context-reader` | `keep` | §8's heading; ships unchanged — D-079 (1)'s narrowing was withdrawn at D-080 |
| V46 | `shared/guard-doctrine.md:258` | `**Running a guard and certifying that it covers what you claim are different` | `fresh-context-reader` | `keep` | §8's operation/certification split, which D-079 keeps |
| V47 | `shared/guard-doctrine.md:261` | `the artifact, so an author who runs them finds its own mistakes. Certification` | `fresh-context-reader` | `keep` | §8's diagnosis, which the M116-M119 round-1 yield confirms |
| V48 | `shared/guard-doctrine.md:285` | `re-certified, never argued down as imprecision. The author still runs` | `fresh-context-reader` | `keep` | §8's zero-unresolved bar; ships unchanged, and D-079 (1)'s narrowing below it was withdrawn at D-080 |
| V49 | `shared/guard-doctrine.md:286` | `everything — this moves certification, not operation.` | `fresh-context-reader` | `keep` | operation stays with the author — unchanged by D-079 |
| V50 | `shared/guard-doctrine.md:288` | `**The certified scope is the work and the records describing the work; a record` | `fresh-context-reader` | `keep` | D-069's certified-scope bound; ships unchanged — D-079 (1) would have extended it and was withdrawn at D-080 |
| V51 | `shared/guard-doctrine.md:289` | `whose subject is a certification round itself — the final round's own report` | `fresh-context-reader` | `keep` | the same D-069 clause, continued |
| V52 | `shared/guard-doctrine.md:293` | `uncertified surface for the next one to audit. M114 pass 8 ran four rounds on` | `fresh-context-reader` | `keep` | D-069's convergence argument; ships unchanged — D-079 (1) would have extended it and was withdrawn at D-080 |
| V53 | `shared/guard-doctrine.md:294` | `that treadmill — round 4 finding defects only in certification narrative — at` | `fresh-context-reader` | `keep` | the M114 treadmill measurement D-079 cites as one step below its own |
| V54 | `shared/migration-protocol.md:36` | ``as the sole `in-progress` milestone, explicitly confirmed.`` | `not-an-instruction` | `keep` | a user confirmation on carrying work over |
| V55 | `shared/migration-protocol.md:124` | `an estimator scaffold, an oracle-verification runner) carry value this` | `not-an-instruction` | `keep` | an example of a clean domain skill |
| V56 | `shared/records-hygiene.md:79` | `actually failed on a different missing piece — so verify a refutation against` | `command-evidence` | `keep` | reads the implementation rather than the scorer's account of it |
| V57 | `shared/tracking-rules.md:55` | `create; amend-via-gate — review reads, never reinterprets; under AC fencing review check-offs a verified criterion box (a verification mark, not a text change)` | `not-an-instruction` | `keep` | a section-ownership table cell describing AC fencing |
| V58 | `shared/tracking-rules.md:65` | `verification mark; the criterion wording stays plan-owned, amended only via` | `not-an-instruction` | `keep` | defines the tick as a verification mark |
| V59 | `shared/tracking-rules.md:157` | `An **always-read file** is one this repo re-reads at the start of most` | `not-an-instruction` | `keep` | defines what an always-read file is |
| V60 | `shared/tracking-rules.md:228` | `and **maturation — a stabilized family graduates whole into a doctrine module** (D-055), where the bar is conjunctive: it teaches transferable authoring or verifying craft rather than a fact about this repo's tools, it has been extended or consolidated at least twice, and neither enforcement nor ownership offers it an exit today.` | `not-an-instruction` | `keep` | the maturation criterion's wording |
| V61 | `shared/tracking-rules.md:297` | `Tasks done, local checks clean; awaiting verification + merge approval` | `not-an-instruction` | `keep` | a status-vocabulary table cell |
| V62 | `shared/tracking-rules.md:576` | `line when they're clean. A recap the user must re-read to find out` | `not-an-instruction` | `keep` | about recaps, not about checking work |
| V63 | `shared/tracking-rules.md:600` | `a proposed disposition or action plan awaiting confirmation (D-038)` | `not-an-instruction` | `keep` | the acceptance-chip scope clause |
| V64 | `shared/tracking-rules.md:670` | `searches the right ground instead of guessing; verify their diffs before` | `command-evidence` | `keep` | reads a subagent's diff before committing it |
| V65 | `shared/tracking-rules.md:725` | ``- **verify** — the per-task test/check command(s) `/milestone-implement` and `/hotfix` run.`` | `not-an-instruction` | `keep` | names the `verify` profile slot |
| V66 | `shared/tracking-rules.md:733` | `The **domain verification doctrine (oracles) is universal, not a profile slot**:` | `not-an-instruction` | `keep` | names the oracle doctrine as universal |
| V67 | `shared/tracking-rules.md:755` | `The domain-verification doctrine — oracle priority list, the five oracle` | `not-an-instruction` | `keep` | the Validation-doctrine pointer |
| V68 | `shared/tracking-rules.md:811` | `"must be verified when X is written" — is the specific failure this rule` | `not-an-instruction` | `keep` | an example of the undated absence claim the rule forbids |
| V69 | `shared/tracking-rules.md:819` | `unpaginated), and extraction-verified status — whether the extracted values` | `not-an-instruction` | `keep` | specifies a provenance block's contents |
| V70 | `shared/tracking-rules.md:820` | `have been re-read against the source, or are an unverified first pass. The` | `not-an-instruction` | `keep` | the same specification, continued |
| V71 | `shared/tracking-rules.md:828` | `**Re-verification.** An extraction status is written once and then ages, so a page the repo still relies on is re-checked against its source as it gets old, and a page never checked against its source at all keeps saying so.` | `command-evidence` | `keep` | re-reads a page against its external source, which the agent never authored |
| V72 | `shared/tracking-rules.md:829` | `A re-check marks inline in the provenance block, on the extraction status itself — never in a new file, a new section, or a log.` | `not-an-instruction` | `keep` | says where a re-check is recorded |
| V73 | `shared/tracking-rules.md:833` | `status and WARNs on a page recording no verified re-check, and on one last` | `not-an-instruction` | `keep` | describes what the staleness advisory WARNs on |
| V74 | `shared/tracking-rules.md:834` | `verified more than 180 days ago; a status naming no date of its own ages from` | `not-an-instruction` | `keep` | the same advisory description, continued |
| V75 | `shared/tracking-rules.md:835` | `the block's ingested date, and a first-hand record with nothing to re-verify` | `not-an-instruction` | `keep` | the advisory's exemption clause |
| V76 | `shared/tracking-rules.md:868` | `guard-verification protocol, whose obligation and unguarded-case fallback the` | `not-an-instruction` | `keep` | names the guard-verification protocol and hands it off |
| V77 | `shared/tracking-rules.md:883` | `passes over a rule that is gone (the recurring M39/M40 trap). Verify by` | `command-evidence` | `keep` | runs the mutation harness rather than reading by eye |
| V78 | `shared/validation-doctrine.md:3` | `<!-- The domain-verification doctrine — a *module* of the core rulebook` | `not-an-instruction` | `keep` | the module's own HTML provenance comment |
| V79 | `shared/validation-doctrine.md:11` | `Tests verify against ground truth, not against the code. Every` | `not-an-instruction` | `keep` | a test-authoring rule about oracles, not a step the agent repeats |

## Counts, at `684e53a`

| Mechanism | Rows | Disposition |
|---|---|---|
| `command-evidence` | 31 | all `keep` |
| `not-an-instruction` | 36 | all `keep` |
| `fresh-context-reader` | 11 | all `keep` |
| `same-context-recheck` | **1** | `keep` |
| total | **79** | — |

All counts observed 2026-07-27 at `684e53a`, and re-derivable by re-running the
search above and re-reading this table's Mechanism column.

## Disposition

The single finding this ledger produces is the shape of the corpus, not any one
row: **cairn does not have the over-verification the guide describes.** Of 79
hits at `684e53a` — observed 2026-07-27 — exactly one, V37 at `guard-doctrine.md:36`, is an author re-reading work
it just produced, and it survives because it fires only after a
mid-implementation amendment and reads the guard against the acceptance
criteria, two artifacts, rather than standing as a blanket final-verification
step. The guide's finding lands almost entirely on D-067's two fresh-context
readers, which its stated mechanism does not reach and its delegation clause,
read unqualified, does.

Where every row lands:

- The 67 `command-evidence` and `not-an-instruction` rows at `684e53a` →
  folded into this milestone as `keep`, no edit — observed 2026-07-27.
- V37 (`same-context-recheck`) → `keep`, ground stated in its row.
- All eleven `fresh-context-reader` rows at `684e53a` → `keep`. D-079's
  surviving clause 2 adds the criteria audit's record requirement, which
  rewrites no line in this corpus; its clause 1 would have narrowed §8 and was
  withdrawn at D-080, leaving `guard-doctrine.md` byte-identical to its
  pre-M121 state — so every §8 row here describes prose this milestone does not
  touch — observed 2026-07-28.
- The criteria audit's own instruction block is **not in this corpus** — its
  wording carries no term in the search — so D-079 reaches it by name rather
  than through a row here. Stated so a later pass does not read the ledger as
  the complete instrument inventory.

This page produced no rule of its own; the rules its measurement fed are
D-079's, and they are locked by `skills/tests/test_fresh_context_readers.py`
(the criteria-audit record requirement, clause 2) and
`skills/tests/test_delegation_warrant.py` (`TestSelfCheckingClassRule`, clause
3), each registered in `skills/tests/test_mutation_harness.py`. D-079's clause 1
shipped no guard: it was withdrawn at D-080 before merge (M121 review F-C13).

## Open questions

- The corpus is the shipped skill and module prose only. Templates, hooks,
  scripts, and `cairn/` tracking files were not swept, so an instruction living
  there is unclassified — observed 2026-07-27.
- Three of the five milestones after D-067's adoption by M115 — M117, M119 and
  M120 — carry no criteria-audit record, and whether each ran the audit
  silently or never ran it is not recoverable; D-079's record requirement fixes
  the ambiguity forward and not backward. D-079's own evidence covers the
  M115-M119 window AC3 names, which is why it reports two rather than three —
  observed 2026-07-27.
