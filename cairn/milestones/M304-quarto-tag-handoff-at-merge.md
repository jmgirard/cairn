# M304: Hand over the tag commands when a merge raises the version

- **Status:** review
- **Priority:** normal
- **Depends on:** M303
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — operators of quarto-extension repos read the close after each merge
- **Branch/PR:** m304-quarto-tag-handoff-at-merge — https://github.com/jmgirard/cairn/pull/318

## Goal

In a quarto-extension repo, the close after a merge that raised the version hands the user the commands that tag and release it.

## Scope

**In:** `/milestone-review` step 10 and the `/hotfix` close after a merge it made, in owner mode, for a repo whose profile is quarto-extension. After the default branch is fast-forwarded, the close runs `scripts/cairn_versions.py --changed-by <merge sha>` (M303). When a version comes back with no tag, the close fences the tag, push, and release commands, which cairn provides and never runs. A D-entry annotates D-050 and supersedes D-048's three-skill wiring to add the `/hotfix` close. README and CHANGELOG.

**Out:** guest mode, where cairn never merges and the maintainers tag; resume route (a) and the guest hygiene run, which reach step 10 without a merge this run made; running the commands (the user's choice at the question set: hand them over). Other profiles get no merge-time handoff; a repo that raises its version at merge under another profile would need a new candidate row.

## Acceptance criteria

- [x] AC1: In owner mode, in `skills/milestone-review/SKILL.md` step 10 and the `skills/hotfix/SKILL.md` close after a merge that run made, for a repo whose profile is quarto-extension, the skill fast-forwards the default branch and runs `scripts/cairn_versions.py --changed-by <merge sha>`. When it prints a version and no `v<version>` tag exists, the close block fences `git tag -a v<version> <merge sha> -m "v<version>"`, `git push origin v<version>`, and, where `origin` is GitHub and `gh` is available, `gh release create v<version> --title "v<version>" --notes-file <file> --verify-tag`. The notes file holds the changelog section for that version, or with changelog "none" the commit subjects on the default branch since the previous `v*` tag. The skills provide these commands and never run them.
- [x] AC2: When the script prints nothing, the tag exists, the profile is another one, the run is in guest mode, or the run made no merge, the close fences no tag command.
- [x] AC3: A D-entry in `cairn/DECISIONS.md` annotates D-050: in a repo that raises its version at merge, the merge is the release the user approved at the merge question, and the close records it with commands it provides and never runs, so cairn proposes no release. The same entry supersedes D-048's wiring to add the `/hotfix` close as a handoff site.
- [x] AC4: Run read-only in `/Users/jmgirard/github/embedpdf`, `scripts/cairn_versions.py --changed-by a68951d` (the merge that raised 1.2.9) prints `1.2.9`, and `--changed-by cf71a53` (a merge that changed only `cairn/` files) prints nothing.
- [x] AC5: README.md and a CHANGELOG.md Unreleased entry describe the handoff, and the five `verify` commands in `cairn/PROFILE.md` each exit 0.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T4
- AC5 → T5

## Tasks

- [x] T1: `/milestone-review` step 10: the quarto-extension arm per AC1 and AC2, placed after the hygiene commit and before the next-action commands, with the notes file built per the profile's changelog slot.
- [x] T2: The `/hotfix` close after its own merge: the same arm.
- [x] T3: Write the D-entry (annotates D-050, supersedes D-048's wiring) and show it in chat.
- [x] T4: Run the AC4 checks read-only on embedpdf and record them in the work log.
- [x] T5: README (the quarto-extension profile's part) and a CHANGELOG Unreleased entry. Hand-run `skills/tests`.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — new close-block behavior in two skills and a D-entry.
- 2026-10-20: criteria audit (full mode, Opus reader, shared with M303): for M304, the handoff runs only in owner mode after a merge the run made, after fast-forwarding the default branch; the notes file's content is named; D-048 limits copy-run wiring to three skills, so the entry also supersedes it for `/hotfix`; AC4's commits were checked in embedpdf (a68951d raised 1.2.9, cf71a53 touched only `cairn/`); the new prose owes no new guard (D-109).
- 2026-10-20: question set: what happens when a merge raises a Quarto extension's version — the close hands over the tag, push, and release commands, and cairn never runs them.
- 2026-10-20: plan gate chose handing over the commands over tagging at merge approval and over leaving it to `/cairn-release`, because the user picked it and cairn never self-publishes; falsified by versions still going untagged in a repo whose closes show the commands.
- 2026-10-20: implement start: branch m304-quarto-tag-handoff-at-merge cut from main at a831d529; the untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-20: T1 done: `/milestone-review` step 10 ends with a self-contained "Tag handoff" paragraph that `/hotfix` cites. Choices: the merge sha comes from `gh pr view --json mergeCommit`, since the hygiene commit sits on top; the notes file goes to the system temp directory as `cairn-notes-<owner>-<repo>-v<version>.md`, like `/milestone` §4's reply draft; a declared changelog with no section for the version falls back to the commit subjects and the recap names the gap, so all three commands still come. Verify: 5/5 green.
- 2026-10-20: T2 done: `/hotfix` step 7 runs review step 10's tag handoff after a merge the run made (authored, adopted, re-landed, or the re-entry's follow-up PR; not the re-entry's already-merged PR), after any ROADMAP commit, with its own `git pull --ff-only` in place of review's step 9. Verify: 5/5 green.
- 2026-10-20: T3 done: D-202 appended (annotates D-050; supersedes D-048's wiring clause (2) for the `/hotfix` close; D-108's door does not apply). `cairn_validate` green; tracking-only, so the five verify commands run once at T5.
- 2026-10-20: T4 done (read-only in embedpdf, marker `_extensions/embedpdf/_extension.yml`): `--changed-by a68951d` printed `1.2.9`, exit 0; `--changed-by cf71a53` printed nothing, exit 0 (that commit touches only `cairn/`). `v1.2.9` is tagged there now, so the handoff for a68951d would fence nothing (AC2's tag-exists case). Open concern: the "none" notes command lists plan and review tracking commits too (12 lines since v1.2.8, one of them the fix); M303's release-walk notes do the same, so M304 keeps the shared rule.
- 2026-10-20: T5 done: README's "Prepare a release" row and a new CHANGELOG Unreleased "New" entry describe the handoff. Verify: 5/5 green; `skills/tests` hand-run green (930 tests).
- 2026-10-20: claim audit: 28 claims read, 0 corrected — skills/milestone-review/SKILL.md, skills/hotfix/SKILL.md, README.md, CHANGELOG.md. Reader notes, not defects: README and CHANGELOG leave out the tag-exists and missing-section conditions the skill states; a `/hotfix` follow-up PR rarely changes `version:`, so a version raised by the re-entry's already-merged PR gets no handoff (Out by AC1).
- 2026-10-20: implement complete; status → review.

## Decisions

## Review

- AC1 evidence (2026-10-20, head c75d64bb): `skills/milestone-review/SKILL.md` step 10's "Tag handoff" paragraph (owner mode, quarto-extension) states, each found once by `grep -cF`: step 9's fast-forward, `gh pr view <N> --json mergeCommit`, `cairn_versions.py <marker file> --changed-by <merge sha>`, the `git rev-parse -q --verify refs/tags/v<version>` tag check, the three commands verbatim (`git tag -a v<version> <merge sha> -m "v<version>"`, `git push origin v<version>`, `gh release create v<version> --title "v<version>" --notes-file <file> --verify-tag`, the last only where `origin` names github.com and `gh` is available), the notes (changelog section for the version, or with "none" `git log --first-parent --format='- %s' <previous tag>..<merge sha>` since the previous `v*` tag), and "provides these commands and never runs them". `skills/hotfix/SKILL.md:540-551` runs that arm on its own PR's merge commit after a merge the run made, with its own `git pull --ff-only origin <default-branch>`. Pass.
- AC2 evidence (2026-10-20, head c75d64bb): `skills/milestone-review/SKILL.md:944-948` fences no tag command when the script prints nothing, the tag exists, the profile is another one, the run is in guest mode, or the close follows no merge this run made (resume route (a), the guest hygiene run), and none on a script error. `skills/hotfix/SKILL.md:543-551` excludes the merged-PR re-entry's already-merged PR and says the guest arm fences none. Pass.
- AC3 evidence (2026-10-20): `cairn/DECISIONS.md:7348` D-202's heading reads "annotates D-050; supersedes D-048's wiring clause to add the `/hotfix` close". Its Decision says that in a repo that raises its version at merge, the merge is the release the user approved at the merge question, and the close records it with commands it provides and never runs, so cairn proposes no release; it supersedes D-048's wiring clause (2) to add the `/hotfix` close as a handoff site. Pass.
- AC4 evidence (2026-10-20, run read-only in `/Users/jmgirard/github/embedpdf`): `cairn_versions.py _extensions/embedpdf/_extension.yml --changed-by a68951d` printed `1.2.9`, exit 0; `--changed-by cf71a53` printed nothing, exit 0; `git diff --name-only cf71a53^ cf71a53` lists no file outside `cairn/`; embedpdf's `git status --short` is empty after the runs. Pass.
- AC5 evidence (2026-10-20, head c75d64bb): README.md's "Prepare a release" row says that after a merge that raised the version, the `/milestone-review` or `/hotfix` close gives the tag, push, and `gh release create` commands and cairn does not run them; CHANGELOG.md's Unreleased "New" section carries "A merge that raises a Quarto extension's version ends with the tag commands". The five `verify` commands exit 0: scripts/tests, hooks/tests, plugin validate, marketplace validate (no version warning), `claude plugin test .`. Pass.
- Consistency gate (2026-10-20): `cairn_validate` exit 0, all checks PASS; no DESIGN principle changed, so `cairn_impact` skipped; profile gate: verify 5/5 green on c75d64bb, marketplace validate shows no `plugins[N].version` warning, CHANGELOG Unreleased has this milestone's entry. Pass.
