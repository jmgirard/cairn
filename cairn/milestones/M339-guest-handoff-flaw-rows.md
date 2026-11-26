<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M339: Write hotfix flaw rows at the guest handoff

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — changes what `/hotfix` writes to the ROADMAP of an adopting guest repo   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A guest-mode `/hotfix` records each flaw its idea vet found in what the fix leaves as it was when it hands the PR to the maintainers, so the flaw is not lost while the PR waits for their merge.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `skills/hotfix/SKILL.md` step 6's guest handoff and step 1's guest change route record each such flaw on disk (a new candidate row tagged with the PR number, or an extension of a matching row). Step 7's guest arm, on the merged-PR re-entry, judges those rows against the merged diff. Step 1's idea-vet paragraph says so. The prose guard, README, CHANGELOG, and a D-entry that supersedes D-225's close-block-only rule for these two guest paths follow.

**Out:** an owner-mode `/hotfix` declined at the merge question, and a guest run that stops before its PR opens, keep naming the flaw only in the close block → parked candidate row "Keep hotfix flaws after a declined merge". The owner arm's resumed merge (step 1) is unchanged.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: In `skills/hotfix/SKILL.md`, once step 6's guest handoff `gh pr create` succeeds, and once step 1's guest change route makes its approved push to PR #<n>, the run records on disk with no commit each flaw that step 1's idea vet found in what the diff leaves as it was, sweeping first by tracking-rules' search-first rule. It records the flaw as one of three things. The first is a new Candidates row of `cairn/ROADMAP.md` that names the flaw as a design decision for later work and whose provenance reads `hotfix PR #<n> handoff`. The second is an existing row extended with `extended YYYY-MM-DD by hotfix PR #<n> handoff`, placed before any ` — started` token. The third, on a standing rejection, is a close-block line naming the flaw and the decision. The close block shows each row written or extended, verbatim. A guest handoff that opens no PR names each flaw in its close block, as on main.
- [ ] AC2: In step 7's guest arm, when the merged-PR re-entry finds that the maintainers merged PR #<N> and its post-hoc verification is accepted, each Candidates row of `cairn/ROADMAP.md` that holds `hotfix PR #<N> handoff` is judged against the merged diff, and for an extended row only the part the handoff added is judged. That part is deleted when the diff covers it in full (a new row is deleted whole), narrowed with step 7's `narrowed` note when the diff covers it in part, and kept otherwise. Each deleted or narrowed row is shown verbatim in chat. A flaw that the re-entry's idea vet finds and such a row holds adds no new row. Any other re-entry outcome leaves these rows as they are.
- [ ] AC3: On the branch, step 1's idea-vet paragraph and step 6's guest arm of `skills/hotfix/SKILL.md` each say that a guest handoff whose `gh pr create` succeeds records the flaw at the handoff, and `git grep -n -E "only by its started token|only appends its started token" -- skills/hotfix/SKILL.md` lists no line.
- [ ] AC4: README.md's `| Fix a reported bug quickly |` table row and an entry in CHANGELOG.md each say that in guest mode the flaw's candidate row is written at the handoff to the maintainers, not after their merge. The CHANGELOG entry sits under a `## Unreleased` heading above `## 2.2.0`, in its "Changes that affect existing repos" subsection.
- [ ] AC5: The `verify` slot of `cairn/PROFILE.md` passes on the branch, and so does the hand-run `python3 -m unittest discover -s skills/tests -p "test_*.py"`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T1, T3
- AC4 → T5
- AC5 → T4, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [ ] T1: Step 6's guest handoff (`skills/hotfix/SKILL.md` ~lines 628-686): after the create and the started-token append, record each flaw per AC1 and show the rows in the close block; keep the close-block naming when no PR opens. Reword "The handoff changes a matched candidate row only by its started token" (~line 682) so a matched row can also be extended.
- [ ] T2: Step 1's guest change route (~lines 289-324): on the approved push, record the flaws per AC1 with that PR's number, and show them in its close block.
- [ ] T3: Step 1's idea-vet paragraph (~lines 115-133): state the guest handoff and change-route exception to "A close block that ends the run before step 7 names the flaw instead". Step 7's guest arm (~lines 719-726): replace "the handoff only appends its started token" and add AC2's judgment of the tagged rows.
- [ ] T4: Update `skills/tests/test_hotfix_candidate_graduation.py` (the guest-arm test pins the two sentences T1 and T3 change) to pin the new sentences, including one that the tagged rows are judged at the re-entry.
- [ ] T5: README `/hotfix` row (README.md:809, "becomes a candidate row after the merge") and a CHANGELOG `## Unreleased` entry, per AC4.
- [ ] T6: Append a D-entry superseding D-225's clause "A close block that ends the run before step 7 names the flaw instead" for a guest handoff that opens its PR and for the change route's approved push, naming the parked row for the owner decline. Run the `verify` slot and the hand-run `skills/tests`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-11-25: created by /milestone-plan, from a report by the easystats session: a guest `/hotfix` handoff (easystats/insight#1317) named two flaws it left alone, and neither reached insight's ROADMAP.
- 2026-11-25: tier check: milestone — the change supersedes D-225's user-chosen rule on when a hotfix flaw gets its row, a design decision.
- 2026-11-25: idea vet: one gap — a row the maintainers' own edits fix stays until a re-entry; reading taken: the re-entry judges tagged rows against the merged diff, and a row with no re-entry is left to `/cairn-triage`. No flaw.
- 2026-11-25: lessons used: 2026-10-29 (M324), 2026-07-24 (M112), 2026-08-17 (M148), 2026-07-16 (M56).
- 2026-11-25: collision check: D-225 (the flaw's row comes from step 7, a close block names it before then) is superseded for the two guest paths at the user's choice; D-240 (step 1 stop rows commit; switching branches rejected) stands and is why owner mode is out; D-108's door passes on its retained trigger, a defect in shipped behavior (flaws lost in insight). `milestone-review` and `milestone-implement` checked: both write follow-up rows before their handoff. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-11-25: criteria audit (full mode, fresh Opus reader) returned 17 findings, all taken: AC1 gained the standing-rejection case, the extended-row form and its place before the started token, the no-PR case, and the change route; AC2 gained the file, the extended-row part rule, and the other-outcome clause (a second re-entry re-judging a narrowed row is accepted); AC3 now names the two passages and a grep that must list nothing, and leaves the owner resumed-merge arm alone; AC4 names the Unreleased heading and subsection; AC5 adds the hand-run `skills/tests`.
- 2026-11-25: question set: write rows at the guest handoff — yes, recommended; owner-mode decline — left for later as a parked row, recommended.
- 2026-11-25: plan gate chose writing at the handoff over writing at step 1's vet, because the diff can still change before the handoff (address-first fixes, the snapshot rule); falsified by a guest run that stops between the vet and the handoff and loses a flaw a user needed.
- 2026-11-25: plan gate chose a `hotfix PR #<n> handoff` provenance tag over the ` — started #<n>` token to find these rows at the re-entry, because a started token hides the row in the cairn pane while the PR is open and these rows hold work no one has taken; falsified by a re-entry that misses a row because triage rewrote its provenance.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive -->
