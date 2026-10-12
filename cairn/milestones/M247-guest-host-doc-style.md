# M247: In guest mode, text written for the host repo matches the host's own style

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP3
- **Resolves:** —
- **Surface tier:** user-facing — it changes what a guest session writes into another team's repo
- **Branch/PR:** m247-guest-host-doc-style

## Goal

In guest mode, the documentation, commit messages, PR text, and replies that a session writes for the host repo match the host's own length, tone, and level of technical detail, where no other writing-style instruction in the session settles them.

## Scope

**In:** one bullet in the rulebook's "Collaboration mode" section; the same rule in short form on the guest-mode line that `hooks/session_context.py` injects at session start, so it stands even when no cairn skill has loaded; a test for that line; a README guest-mode bullet and a CHANGELOG entry.

**Out:** owner mode, where the repo's style is the operator's own (a candidate row only if an owner asks for it). Recording the host's style as a DESIGN.md Conventions line at the guest seed: the rule reads the host's text when it writes, so no stored summary is kept (work-log line below). Records under `cairn/`, which the record-prose rule governs. Precedence over other style instructions: the user chose at the gate that those win.

## Acceptance criteria

- [ ] AC1: `skills/shared/tracking-rules.md`'s "Collaboration mode" section carries exactly one new bullet stating that, in guest mode, the text the session writes for the host repo or its maintainers (its documentation, such as README, guides and vignettes, help pages and docstrings, code comments, changelog entries, and messages users see; commit messages; the PR title and body; and replies on the host's issues and PRs) matches the host's existing text of the same kind in length, tone, and level of technical detail, read from that text before writing, or from the host's other documentation where it has none of that kind; that this matching works within the limits of the "No cairn vocabulary reaches the repo" bullet; and that where another writing-style instruction in the session (another plugin's, or the user's own) also governs that text, that instruction wins and the matching covers only what it leaves open, while the rulebook's Plain style rule (which binds chat output) and record-prose rule (which binds `cairn/` records) do not govern that text.
- [ ] AC2: In guest mode, the one line that ends the `## Collaboration mode` part of the SessionStart context built by `hooks/session_context.py` also states that text written for the host repo or its maintainers matches the host's own length, tone, and level of technical detail where no other writing-style instruction in the session settles it, and names the tracking-rules "Collaboration mode" section; the part's tail after the routing body stays one line.
- [ ] AC3: `README.md`'s "Contributing to a repo you don't own (guest mode)" list carries exactly one new bullet stating the rule, and `CHANGELOG.md`'s Unreleased "Changes that affect existing repos" subsection carries exactly one new entry describing it.
- [ ] AC4: The repo's `verify` slot (`cairn/PROFILE.md` `## verify`) passes on the branch.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4

## Tasks

- [x] T1: Add the bullet to `skills/shared/tracking-rules.md` "Collaboration mode" (after the "No cairn vocabulary reaches the repo" bullet, near line 325), cross-referencing that bullet rather than restating it. Hand-run `skills/tests` afterward, since prose guards slice this section (LESSONS M148).
- [x] T2: Append the short-form sentence to the guest-mode line in `hooks/session_context.py` `build_context` (lines 296-299), keeping it one line. Add a test in `hooks/tests/test_hooks.py` beside `test_guest_mode_injects_the_template_routing_section` that asserts the fragments "host", "length, tone, and level of technical detail", and "writing-style instruction" in the tail (the line already names the section, so a section-name fragment cannot fail); show it red with the sentence removed, then green. The existing one-line tail assertion stays.
- [ ] T3: Add the README bullet (`README.md` guest-mode list, lines 772-794) and the CHANGELOG entry, each written against a same-session read of T1 and T2's text (the derived-claims rule).
- [ ] T4: Run every `verify` command from the repo root, each exit code checked on its own (LESSONS M56).

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

## Decisions

## Review
