# M247: In guest mode, text written for the host repo matches the host's own style

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing — it changes what a guest session writes into another team's repo
- **Branch/PR:** m247-guest-host-doc-style, https://github.com/jmgirard/cairn/pull/257

## Goal

In guest mode, the documentation, commit messages, PR text, and replies that a session writes for the host repo match the host's own length, tone, and level of technical detail, where no other writing-style instruction in the session settles them.

## Scope

**In:** one bullet in the rulebook's "Collaboration mode" section; the same rule in short form on the guest-mode line that `hooks/session_context.py` injects at session start, so it stands even when no cairn skill has loaded; a test for that line; a README guest-mode bullet and a CHANGELOG entry.

**Out:** owner mode, where the repo's style is the operator's own (a candidate row only if an owner asks for it). Recording the host's style as a DESIGN.md Conventions line at the guest seed: the rule reads the host's text when it writes, so no stored summary is kept (work-log line below). Records under `cairn/`, which the record-prose rule governs. Precedence over other style instructions: the user chose at the gate that those win.

## Acceptance criteria

- [x] AC1: `skills/shared/tracking-rules.md`'s "Collaboration mode" section carries exactly one new bullet stating that, in guest mode, the text the session writes for the host repo or its maintainers (its documentation, such as README, guides and vignettes, help pages and docstrings, code comments, changelog entries, and messages users see; commit messages; the PR title and body; and replies on the host's issues and PRs) matches the host's existing text of the same kind in length, tone, and level of technical detail, read from that text before writing, or from the host's other documentation where it has none of that kind; that this matching works within the limits of the "No cairn vocabulary reaches the repo" bullet; and that where another writing-style instruction in the session (another plugin's, or the user's own) also governs that text, that instruction wins and the matching covers only what it leaves open, while the rulebook's Plain style rule (which binds chat output) and record-prose rule (which binds `cairn/` records) do not govern that text.
- [x] AC2: In guest mode, the one line that ends the `## Collaboration mode` part of the SessionStart context built by `hooks/session_context.py` also states that text written for the host repo or its maintainers matches the host's own length, tone, and level of technical detail where no other writing-style instruction in the session settles it, and names the tracking-rules "Collaboration mode" section; the part's tail after the routing body stays one line.
- [x] AC3: `README.md`'s "Contributing to a repo you don't own (guest mode)" list carries exactly one new bullet stating the rule, and `CHANGELOG.md`'s Unreleased "Changes that affect existing repos" subsection carries exactly one new entry describing it.
- [x] AC4: The repo's `verify` slot (`cairn/PROFILE.md` `## verify`) passes on the branch.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks

- [x] T1: Add the bullet to `skills/shared/tracking-rules.md` "Collaboration mode" (after the "No cairn vocabulary reaches the repo" bullet, near line 325), cross-referencing that bullet rather than restating it. Hand-run `skills/tests` afterward, since prose guards slice this section (LESSONS M148).
- [x] T2: Append the short-form sentence to the guest-mode line in `hooks/session_context.py` `build_context` (lines 296-299), keeping it one line. Add a test in `hooks/tests/test_hooks.py` beside `test_guest_mode_injects_the_template_routing_section` that asserts the fragments "host", "length, tone, and level of technical detail", and "writing-style instruction" in the tail (the line already names the section, so a section-name fragment cannot fail); show it red with the sentence removed, then green. The existing one-line tail assertion stays.
- [x] T3: Add the README bullet (`README.md` guest-mode list, lines 772-794) and the CHANGELOG entry, each written against a same-session read of T1 and T2's text (the derived-claims rule).
- [x] T4: Run every `verify` command from the repo root, each exit code checked on its own (LESSONS M56).

## Work log

- 2026-10-12: created by /milestone-plan.
- 2026-10-12: collision check: no candidate, planned, or archived milestone covers documentation style; D-137 and D-139 define guest mode and the provisional Conventions model, and this rule sits beside them (D-161).
- 2026-10-12: inbox sweep: 0 open issues, 0 open PRs on jmgirard/cairn.
- 2026-10-12: lessons harvested: M112 (doctrine wording reaches README and CHANGELOG, so both are in scope), M148 (hand-run skills/tests after editing near a guarded slice), M56 (a hooks edit runs both gating suites).
- 2026-10-12: question set: which style wins when another style instruction conflicts with the host's — the other instruction wins, and host matching covers only what it leaves open.
- 2026-10-12: question set: which text the rule covers — everything the maintainers read: documentation, commit messages, PR title and body, and replies on the host's issues and PRs.
- 2026-10-12: criteria audit (full mode): 13 findings on the first draft. Fixed: an unanswered conflict with the no-cairn-vocabulary bullet, an undefined "nearest kind", "one bullet" made "exactly one new bullet", a closed text list widened to replies and user messages, the existing one-line tail test (the sentence now joins that line), the removal check moved from AC2 to T2, AC2's short form given named parts, the CHANGELOG subsection named. The precedence wording went to the question set. Re-audit after the gate (full mode): 3 findings, all fixed — AC1 now says the Plain style and record-prose rules do not govern host text, AC2 uses AC1's term "writing-style instruction", and T2's third fragment is one the current line lacks.
- 2026-10-12: plan chose to put the rule in both the rulebook and the guest session line over the rulebook alone, because the rulebook loads only when a cairn skill fires and a doc edit can happen outside one; falsified by a guest session that loads the session line and still writes off-style text with no skill loaded.
- 2026-10-12: plan chose reading the host's text at write time over storing a style summary in DESIGN.md Conventions at the guest seed, because a stored summary goes stale as the host's docs change; falsified by a guest session that skips the read and writes off-style text a stored line would have prevented.
- 2026-10-12: implement started on m247-guest-host-doc-style; untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-12: T1 done: the bullet follows the no-cairn-vocabulary bullet in tracking-rules "Collaboration mode". The rulebook-size baseline is re-seeded to 651 lines / 62,396 bytes at its three sites (LESSONS M149). The simple-english plugin's lint hook flagged the rulebook's older text (490 hits), and only the new bullet was rewritten to clear its own. verify, skills/tests, and validate are green.
- 2026-10-12: T2 done: `test_guest_mode_line_carries_the_host_style_rule` failed before the hook change with `'host' not found` in the old mode line, and passes after it. The sentence lists the kinds of text in short form and carries no milestone id, since it reaches guest sessions. verify, skills/tests, and validate are green.
- 2026-10-12: T3 done: README guest-mode bullet after the vocabulary bullet, CHANGELOG entry at the top of "Changes that affect existing repos", both written from a same-session read of T1's bullet and T2's line. Long sentences in the new text were split for the simple-english lint, and the older hits in both files stay.
- 2026-10-12: T4 done: all five verify commands, skills/tests, and validate exit 0, each checked on its own.
- 2026-10-12: claim audit: 16 claims read, 0 corrected — CHANGELOG.md, README.md, hooks/session_context.py, hooks/tests/test_hooks.py, skills/shared/tracking-rules.md, skills/milestone/SKILL.md, skills/tests/test_cost_audit_line.py, skills/tests/test_mutation_harness.py. The reader noted the README bullet left out "covers only what it leaves open", now added, and that the hook's line reaches only repos whose `cairn/ROADMAP.md` reads, as every injected part does.
- 2026-10-12: implement complete; status set to review.

## Decisions

- 2026-10-12 (review): the rulebook bullet gains two clauses from diff-bug findings #2 and #3. A style the host states in writing comes before what its existing text shows, and the derived-claims rule still binds what host text claims. Both narrow how the matching is read and leave D-161's decision as written, so no new D-entry.

## Review

- AC1: `git diff main..HEAD -- skills/shared/tracking-rules.md` adds one 9-line bullet, the "Collaboration mode" section going from 8 to 9 top-level bullets (awk over the section on main and HEAD). The bullet names each listed kind of text, the three matching axes, the read before writing, the host's other documentation as fallback, the limits of "the bullet above" (the no-cairn-vocabulary bullet directly above it), other writing-style instructions winning with matching covering only what they leave open, and the Plain style and record-prose rules not governing that text. Pass.
- AC2: a scratch script ran `session_context.build_context` on temp guest and owner repos. The guest part's tail after the routing body is 1 line, names tracking-rules "Collaboration mode", and adds that text for the host repo or its maintainers matches the host's own length, tone, and level of technical detail where no other writing-style instruction in the session settles it. The owner context has no `## Collaboration mode` part. `unittest -k guest_mode` over hooks/tests: 3 tests OK, `test_guest_mode_line_carries_the_host_style_rule` among them (red before the hook change, T2 work log). Pass.
- AC3: `git diff main..HEAD -- README.md CHANGELOG.md` adds one bullet to the README guest-mode list (6 to 7 bullets, awk between its heading and the "Because `cairn/`" paragraph) and one entry at the top of CHANGELOG's Unreleased "Changes that affect existing repos" (19 to 20 bullets). Both state the coverage, the three axes, and that another writing-style instruction wins with matching covering only what it leaves open. One overlong CHANGELOG line was rewrapped at review. Pass.
- AC4: the five `verify` commands run from the repo root on the review head, each exit 0 checked on its own (scripts/tests, hooks/tests, plugin validate, marketplace validate, plugin test). Pass.
- Gate (pass 1, before the fixes below): `cairn_validate.py` all checks passed; no principle text changed, so `cairn_impact` skipped; marketplace validate prints no `version` warning; CHANGELOG carries the entry with no milestone number; skills/tests (hand-run) OK.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: CHANGELOG.md:15 was 105 characters, left by the review rewrap (so AC3's "rewrapped" line was half true) — fix now; every line of the entry is now 80 or fewer.
- diff-bug #2: the derived-claims rule also covers host docs, and the bullet did not say which rule wins — fix now; the bullet says the derived-claims rule still binds what that text claims.
- diff-bug #3: a host's written style guide (CONTRIBUTING, a style doc) was not named, so copying old text could override it — fix now; the bullet says a style the host states in writing comes before what its existing text shows.
- diff-bug #4: "also governs" has no test, and a global user style rule could leave matching little to decide — reject, planned change: the user chose this precedence at the plan gate (D-161).
- diff-bug #5: "the bullet above" points by position — fix now; the bullet names the "No cairn vocabulary reaches the repo" bullet.
- diff-bug #6: the test checks fragments, so a reversed precedence would pass — fix now; the third fragment is "where no other writing-style instruction", which a reversal drops.
- diff-bug #7: the hook's short form leaves out the vocabulary limit and the read step, and its pointer belongs to the sentence before — reject, planned change: AC2 sets a short form that names the section, and the line names it.
- diff-bug #8: the new sentence spends about 300 characters of the context budget — reject, planned change: the part is charged to MAX_CHARS as M184 designed, and the plan put the rule there.
- diff-bug #9: README's "your own CLAUDE.md" is narrower than "the user's own" — reject, false: the README gives it as an example after "such as".
- diff-bug #10: "applies before any cairn skill loads" holds only when `cairn/ROADMAP.md` reads — reject, false: with no readable ROADMAP the hook injects nothing at all, so the condition is the hook's, not the rule's, and a cairn repo has the file.
- diff-bug #11: README and CHANGELOG leave out the read step, the fallback, and some kinds of text — reject, planned change: both are summaries, and AC3 asks each to state the rule.
- blame-history #1: the hook's "where no other writing-style instruction … settles it" reads all-or-nothing beside the rulebook's "covers only what it leaves open" — reject, planned change: the wording is AC2's, and "where" limits the matching to the points left unsettled.
- blame-history #2: the same CHANGELOG line as diff-bug #1 — fix now (same fix).
- blame-history #3: the line is longer but the tail stays one line and is charged to MAX_CHARS — reject, false as a defect: the reviewer itself found M184/M185's behavior kept.
- blame-history #4: the re-seed follows its rule at all three sites — reject, false as a defect (a confirmation); re-seeded again to 653 lines / 62,604 bytes after the fixes.
- blame-history #5: the bullet cites D-161 in plugin source — reject, false as a defect: rulebook text never reaches the host, and the hook line carries no id.
- blame-history #6: the bullet agrees with D-137, D-139, and D-155 — reject, false as a defect (a confirmation).
- blame-history #7: the hook's list is shorter than the rulebook's, and nothing pins the two together — reject, planned change: AC2 sets a short form.
- prior-review #1: Copilot's open thread on the stale ROADMAP stamp — handled as the copilot line below.
- prior-review #2: the same CHANGELOG line as diff-bug #1 — fix now (same fix).
- prior-review #3: the re-seed matches `wc` at all three sites, unlike PRs #242 and #244 — reject, false as a defect (a confirmation).
- prior-review #4: the D-161 cite sits in a guest-mode section — reject, false as a defect: rulebook text, never host-facing.
- copilot: cairn/milestones/M247-guest-host-doc-style.md:10 — the header should carry the PR URL — reject, false: d37201b already recorded it; Copilot read an earlier head.
- copilot: cairn/ROADMAP.md:12 — the hygiene stamp still says "M247 planned" — reject, false as a defect: the stamp records the last hygiene pass, and the post-merge pass replaces it.
- copilot: review body — add a prose guard and mutation-harness entry for the new rulebook bullet — reject: prose guards are hand-run only and gate nothing (D-109), and the copy that reaches sessions with no skill loaded, the hook line, has its test.
- Copilot level: Lite (set by GitHub's settings). Copilot reviewed head 4be5ae9 and not d37201b or the fixes after it.
- Re-check after the fixes: the AC1 bullet still carries every clause AC1 names, and names the vocabulary bullet by title; the AC3 README bullet and CHANGELOG entry are unchanged in substance; AC2's tail is still one line and the hooks test passes; all five `verify` commands, skills/tests, and `cairn_validate.py` exit 0; `git grep` finds no leftover 651 / 62,396 figure outside `cairn/`.
