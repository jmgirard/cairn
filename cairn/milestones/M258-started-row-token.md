# M258: Started token on candidate rows

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the pane's drawn mark and the ROADMAP text that skills write for the operator
- **Branch/PR:** m258-started-row-token

## Goal

A candidate row that a planned or handed-off milestone absorbs, or that an open guest hotfix PR fixes, draws the started mark `◐` in the cairn pane through a ` — started <ref>` token on the row itself.

## Scope

**In:** a ` — started M<NNN>` token that `/milestone-plan` appends, in both
modes, to each candidate row a plan absorbs in full or in part; a
` — started #<n>` token that `/hotfix`'s guest arm appends on disk after it
opens the PR; the pane reading both tokens, counting an M token while the
ROADMAP table holds that id as `planned` or `blocked` and a #n token while
the pane's open hotfix list holds n; the narrowing rule that drops a token;
the docs and one D-entry.

**Out:** owner-mode `/hotfix` and `/milestone-review` keep their PR-body
`Candidate row:` lines unchanged, and no token is written at PR open in owner
mode, because that would need a commit to the default branch. The other
"Started mark edges (M252 review)" items (a cut `gh pr list`, the fence forms)
stay on that row. A guest base remote with no `upstream` lists no hotfix PR,
so its #n token counts nothing; that stays a documented limit, not a fix.

## Acceptance criteria

- [ ] AC1: In the cairn pane, a candidate row's ` — started M<NNN>` token
      counts while the ROADMAP table holds a row with that id whose status is
      `planned` or `blocked`. A row with a counted M token and no other mark
      source (AC3) draws `◐` in the review color, the lowest counted id at its
      right end, and no ✎. A row whose M tokens all fail to count (the table
      row absent, `done`, or `dropped`), with no other source, draws its
      priority mark and no id, and ✎ when its short title is not empty and no
      cairn skill's step is set. `hooks/status/pane.test.tsx` cases cover a
      planned id, a blocked id, a done id, a dropped id, an absent id, and a
      row with two M tokens of which one counts.
- [ ] AC2: A candidate row's ` — started #<n>` token counts while the open
      hotfix list that the pane holds for its root (the last successful
      read's) holds PR number n. A row with a counted #n token draws `◐`, the
      lowest counted number at its right end, and no ✎. A row whose #n tokens
      all fail to count, with no other source, draws its priority mark and no
      number. `pane.test.tsx` cases cover n listed, n not listed, and a row
      with two #n tokens of which one is listed.
- [ ] AC3: When more than one source marks a row (an open PR's
      `Candidate row:` line, a counted #n token, a counted M token), the
      row's right end shows the lowest PR number among the first two sources,
      and the lowest counted milestone id only when neither gives a number.
      `pane.test.tsx` cases cover a body line with a counted M token, a
      counted #n token with a counted M token, and a body line naming #a with
      a counted #b token where b < a, which shows #b. The M252 and M257
      started-mark cases pass unchanged.
- [ ] AC4: For a candidate row with `: ` in it, one with ` — ` and no `: `,
      and one with neither, `candidateRows` in `hooks/status/reader.ts` gives
      the same short title with ` — started M258`, ` — started #301`, or both
      appended as without them, shown by `reader.test.ts` cases.
- [ ] AC5: `skills/shared/tracking-rules.md` defines the two token forms
      beside "Candidate priority token". `/milestone-plan` step 6 appends
      ` — started M<NNN>` to each candidate row the plan absorbs, in both
      modes. `/hotfix`'s guest arm appends ` — started #<n>` on disk to each
      row step 1 matched, after the PR create, and the two sentences in
      steps 6 and 7 saying the guest handoff leaves a matched row unchanged
      say so no longer. `skills/shared/records-hygiene.md` §1 says a narrowed
      row loses the token of the milestone or hotfix that narrows it.
      Evidence: a read of those five sites.
- [ ] AC6: README's started-mark section says which skill writes each token
      and in which mode, that guest mode gets the mark only through the
      tokens, and when each token's mark shows and goes. `cairn/DESIGN.md`
      and the unreleased `CHANGELOG.md` entry state the token rule. A D-entry
      records that the token rule passes D-108's door on its retained
      trigger, and that a token names another record's id and is not the
      row's own id (D-035). Evidence: a read of the four files.
- [ ] AC7: The `verify` slot of `cairn/PROFILE.md` is clean.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T2
- AC4 → T1
- AC5 → T3
- AC6 → T4
- AC7 → T5

## Tasks

- [x] T1: `reader.ts` and `types/`: `candidateRows` reads each
      ` — started M<NNN>` and ` — started #<n>` token of a row into the row,
      the short title cut as now; `loadAt` gives the pane the set of table
      ids whose status is `planned` or `blocked`. `reader.test.ts` cases for
      AC4. If the shared fixtures gain token rows, regenerate them and keep
      `scripts/tests/test_status_fixtures.py` in agreement.
- [x] T2: `pane.ts` `paneLines`: count tokens as AC1 and AC2 state, pick the
      right-end text as AC3 states, and hide ✎ on a marked row;
      `register.tsx` `pressCandidate` refuses a stale ✎ press on a row a
      counted token marks. `pane.test.tsx` cases for AC1 to AC3.
- [ ] T3: skill text: tracking-rules token paragraph; `/milestone-plan`
      step 6 (both modes, rows absorbed in full or in part); `/hotfix` guest
      arm write after the PR create, and the steps 6 and 7 "unchanged"
      sentences; records-hygiene §1 narrowing drops the token.
- [ ] T4: README started-mark section, DESIGN, the unreleased CHANGELOG
      entry, and the D-entry AC6 names.
- [ ] T5: run the `verify` slot and fix what it reports.

## Work log

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — a pane change and new skill conduct across several files, with a design choice.
- 2026-10-15: collision: extends M252 and M257 (done); absorbs in part the "Started mark edges (M252 review)" row's first clause, which takes a ` — started M258` token at plan; D-163 and D-164 keep the short title, since the token sits after the first ` — `; D-108's door is passed on its retained trigger (a guest pane never shows the mark M252 shipped), recorded by AC6's D-entry; inbox sweep found no open issue or PR.
- 2026-10-15: plan gate chose a ` — started <ref>` token on the candidate row over M252's PR-body line for guest mode, because guest PR bodies carry no cairn text and a guest ROADMAP edit needs no commit; this narrows M252's plan-gate choice, whose two reasons (a default-branch commit at PR open, a removal on an unmerged close) the plan-time token in the plan commit and the pane's live-status and open-list checks answer; falsified by a token left counting after its milestone or PR ended.
- 2026-10-15: plan gate chose the token on the row over a `Candidate row:` line in the milestone file for milestones, because the pane already reads the ROADMAP and not planned milestone files, and one token form serves both milestones and hotfixes; falsified by a plan that absorbs a row but writes no token.
- 2026-10-15: plan gate chose the token on the row over a hotfix file or a tracker file for guest hotfixes, because no new file type, format, or cleanup step is needed and step 7 already removes or narrows the row; falsified by a guest hotfix whose token outlives the row edit.
- 2026-10-15: question set: token text — ` — started M<NNN>` and ` — started #<n>`; plan token in both modes; hide ✎ on a marked row; no live look, pane tests only.
- 2026-10-15: criteria audit (full, fresh Opus reader): 9 findings, all fixed: AC1 and AC2 second clauses scoped to rows no other source marks; several tokens of one form, counted or not, with a case each; ✎ only for a non-empty title; "the list the pane holds" for "the last read"; the no-read pane case dropped as the same input as not-listed; a body-line-and-#n precedence case; AC4 covers #n and both tokens; AC5 evidence is a read of the five sites, including the two "unchanged" hotfix sentences; AC6 gains the D-108 door and D-035 note.
- 2026-10-15: implement: branch m258-started-row-token cut from main at 2ccf609f; the untracked `cairn-probe.log` and `tsconfig.json` stay unstaged.
- 2026-10-15: T1, T2 done: the tokens ride in a new `PaneState.taken` list ({title, ref}) built by `takenRows` from `startedTokens`, not in `CandidateRow`, so the fixtures, `fixtures.gen.ts`, and the Python mirror keep their candidate shape; pane shape tag to `pane-6`; `startedRefs` in pane.ts picks the marks for `paneLines` and `pressCandidate`; an id token is `M` plus digits compared through `canonId`, a number token `#` plus 1-15 digits, each ended by the row end or ` — `; mod tests 1757 pass, scripts 408 OK.

## Decisions

## Review
