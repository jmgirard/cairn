# M259: Triage keeps started tokens current

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — `/cairn-triage` proposals and the ROADMAP rows it writes for the operator
- **Branch/PR:** —

## Goal

`/cairn-triage` proposes, at its one gate, adding a missing ` — started M<NNN>` token to a candidate row that a live milestone file names and removing a started token whose work has ended, and it never rewrites away a live token.

## Scope

**In:** `skills/cairn-triage/SKILL.md`: the dead, missing, and live token rules, the reads they need (live milestone files; `gh pr view` for `#<n>` tokens, `--repo <base-repo>` in both modes), the token change as a row fact beside the disposition (the priority token's precedent), the keep rule for live-token rows, the chip, apply, and stamp. tracking-rules "Candidate started token" names triage as the step that does this. README, CHANGELOG, and a DECISIONS entry annotating D-165's "no step removes it" consequence. The rulebook-mass baseline re-seed that a tracking-rules edit owes.

**Out:**
- A `/milestone` health-audit check for missing or dead tokens → dropped at the user's choice (question set); no row.
- Proposing a missing `#<n>` token: owner mode marks a hotfix through PR-body `Candidate row:` lines and writes no `#<n>` token, guest `/hotfix` writes its token in the step that opens the PR, and a guest PR body carries no row text to match → not planned (decided at plan).
- `/milestone-plan` step 6 removing a dead token when it appends a new one → triage does it; no row.
- The other clauses of "Started mark edges (M252 review)" (body lines set at PR open, a cut `gh pr list`, fences, same-title rows, a later `: `, `/hotfix` matching a taken row) → stay in that row; its "a dead one stays" and "triage compress or merge can drop one" clauses leave it at M259's post-merge hygiene.

## Acceptance criteria

- [ ] AC1: `skills/cairn-triage/SKILL.md` reads a started token as tracking-rules "Candidate started token" and the pane do (` — started ` and `M<digits>` or `#<digits>`, not followed by a letter or digit), compares ids at three-digit padding, and defines a dead token as an `M<NNN>` token whose id the ROADMAP milestone table holds as `done` or `dropped`, or does not hold, or whose milestone file sits in `cairn/milestones/archive/`, and as a `#<n>` token for which `gh pr view <n> --repo <base-repo> --json state` reports `MERGED` or `CLOSED`. Step 3's table proposes removing each dead token on a row proposed `keep`, `compress`, `retitle`, or `promote`. A `#<n>` read that fails proposes no token change for that token, and the table names the failed read.
- [ ] AC2: The skill defines a missing token as ` — started M<NNN>` absent from a candidate row while the ROADMAP table holds `M<NNN>` as `planned`, `in-progress`, `blocked`, or `review` and that milestone's file directly under `cairn/milestones/` quotes the row's non-empty short title in double quotes outside its Scope `**Out:**` list. Step 3's table proposes appending that token to the end of each such row and names the file, and the user can decline it at the gate. The skill proposes adding no `#<n>` token.
- [ ] AC3: The skill makes a token change a row fact beside the row's disposition, as a priority change is, never a ninth disposition, riding on a `keep`, `compress`, `retitle`, or `promote` row (a merge survivor is a `keep`, its lineage clause written before the row's tokens); a `drop`, `merge`, `split`, or `route` writes no dead token into any row it writes. The chip's question text names each proposed token change. Step 4 writes a token change only when the user's answer accepts it; the change adds or removes the token text (` — started <ref>`) and leaves the rest of the row as it is. Step 4's skip rule and cap count, step 3's untouched-items carve-outs, and step 6's stamp each count token changes.
- [ ] AC4: The skill proposes `keep`, with the token named in the reason, for a row that carries a started token that is not dead under AC1, a `#<n>` token whose read failed included, as it does for a row a live milestone absorbs, and this rule comes before records-hygiene §7's options for a finding-absorbing row.
- [ ] AC5: tracking-rules "Candidate started token" names `/cairn-triage` as the step that proposes a missing `M<NNN>` token and the removal of a dead token; README's started-token paragraph says so in place of its sentence that such a token "stays on the row and marks nothing"; `CHANGELOG.md`'s `## Unreleased` has an entry; a new `cairn/DECISIONS.md` entry annotates D-165's "no step removes it" consequence and records the ground on which it passes D-108's door. No sentence in README, `skills/`, or `cairn/DESIGN.md` says a dead token stays with no step to remove it, checked by `grep -rn -e "marks nothing" -e "no step removes" -e "stays on the row" README.md skills/ cairn/DESIGN.md`.
- [ ] AC6: The `verify` slot of `cairn/PROFILE.md` is clean: both gating suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T4

## Tasks

- [ ] T1: Triage session start and step 2: read the files directly under `cairn/milestones/` of each live milestone, read each `#<n>` token's PR state with `gh pr view <n> --repo <base-repo> --json state` (guest mode reads the base repo too), and state the dead, missing, and live rules; extend the keep rule (`skills/cairn-triage/SKILL.md:56-58`, `:171-172`) to live-token rows.
- [ ] T2: Steps 3, 4, and 6: the token change in the table's reason cell and the chip's question text, the untouched-items carve-out (`:228-234`), the apply edit (`:264-267`, a token appended at the row's end, removal of the token text alone), the skip rule (`:236-240`), the cap count, the merge survivor's lineage clause before its tokens, and the stamp (`:311-315`). A row a `drop`, `merge`, `split`, or `route` takes out writes no dead token into the rows it writes. Place the live-token keep before §7's options (`:162-172`).
- [ ] T3: tracking-rules "Candidate started token" (`:215-220`), README's started-token paragraph (`README.md:476-495`), a CHANGELOG `## Unreleased` entry, the DECISIONS entry, and the rulebook-mass baseline in `skills/milestone/SKILL.md:116` plus its two hand-run pins (LESSONS M149). Sweep README and `cairn/DESIGN.md` for other triage or token sentences the change makes stale (LESSONS M112).
- [ ] T4: Apply AC1 and AC2's rules by hand to this repo's ROADMAP and milestone files and log which tokens are dead, live, and missing. Hand-run `skills/tests` for the triage guards and fix a pinned phrase the edit moved. Run the `verify` slot.

## Work log

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — changes `/cairn-triage`'s shipped behavior and settles a design choice (where token upkeep lives); routed by a request relayed from another session.
- 2026-10-15: collision check: absorbs in part the candidate row "Started mark edges (M252 review)" (its "a dead one stays" and "triage compress or merge can drop one" clauses), so it gets ` — started M259`; annotates D-165 (its consequence that no step removes a dead token); a token change rides beside a disposition as D-134's priority token does, so D-027's eight words stand and D-035's no-sub-status rule holds (D-165: a token holds no status). Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-15: D-108's door judged passed on its retained trigger: a triage `compress` or `retitle` can rewrite away a live `#<n>` token, which drops the pane's mark for an open PR, and M258's own hygiene left a dead ` — started M258` on that row in this repo; the D-entry records it. Checker-regress shape judged not hit: triage is an on-demand editing pass, not a checker; the `/milestone` audit check, the checker-shaped part, was posed as not recommended.
- 2026-10-15: lessons harvested: M112 (sweep README and DESIGN for stale wording, CHANGELOG task), M149 (rulebook-mass pins re-seed in three places), M185 (`gh` reads carry `--repo <base-repo>`), LESSONS line 1 (a SKILL.md edit runs both gating suites).
- 2026-10-15: criteria audit (full, fresh Opus reader): 10 findings, all fixed: AC1 and AC3 disagreed on dead tokens under other dispositions (now ride on keep, compress, retitle, promote; leaving rows write none); ids compared at three-digit padding; token shape tied to tracking-rules and the pane; AC2's substring match narrowed to a double-quoted title outside Scope Out, declinable at the gate; skip rule and cap count token changes; merge survivor's lineage clause goes before its tokens; live-token keep comes before §7's options and a failed read proposes no token change; AC5's grep widened and made the check for a stated property; D-108's door ground goes in the D-entry; Out names the row clauses that leave at hygiene.
- 2026-10-15: plan gate chose a token change beside the disposition over a ninth disposition because D-027 fixes the vocabulary and D-134 set the precedent; falsified by a pass where a token change must happen on a row that leaves the list.
- 2026-10-15: plan gate chose a double-quoted short-title match outside Scope Out over any literal substring because generic titles and Out lists over-match; falsified by a live milestone that absorbs a row without quoting its title, which triage then misses.
- 2026-10-15: plan gate chose not to propose missing `#<n>` tokens: owner mode marks hotfixes through PR-body lines and guest `/hotfix` writes its token as it opens the PR; falsified by a guest hotfix PR open with no token on its row.
- 2026-10-15: question set: a `/milestone` health-audit check for tokens — dropped, triage only, idea not recorded.
- 2026-10-15: question set: the stale ` — started M258` on "Started mark edges (M252 review)" — left in place; T4's hand run must report it dead, and M259's hygiene removes it.
- 2026-10-15: ROADMAP: M258's done row pruned to keep the table under the 60-line cap (terminal-row retention).
