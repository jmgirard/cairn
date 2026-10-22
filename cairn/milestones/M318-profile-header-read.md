<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M318: State how PROFILE header lines are read

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the rulebook and hooks ship to every cairn repo and decide how its PROFILE.md is read   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m318-profile-header-read   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The rulebook states once how a `cairn/PROFILE.md` header line is read, and every header-line reader in cairn reads that way.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** One paragraph in tracking-rules "Toolchain profiles" that states the read. Four passages that cite it. The `# Toolchain profile:` line moves onto the shared reader. The Copilot opt-in line follows the shared read. The validator skips a byte-order mark. Tests for each claim the paragraph adds.

**Out:** The pane's `profileHeader` in `hooks/status/reader.ts` already reads this way and does not change. The validator still checks every mode line in the header region, not only the first, because it checks values and does not choose one. A hand-run prose guard in `skills/tests` is not planned.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: The "Toolchain profiles" section of `skills/shared/tracking-rules.md` holds one paragraph that states how a `cairn/PROFILE.md` header line is read. It makes five claims. (a) Only the lines before the first line that starts with `## ` are read. (b) A header line starts with `#` as its first character. Then come optional whitespace, the key as written in any letter case, `:` right after the key, optional whitespace, and the value. The value is the first run of non-whitespace characters after the colon. A line with no value is not a header line. (c) A byte-order mark at the start of the file is skipped. (d) When two header lines carry the same key, the first one is read. (e) Letter case in the value does not count, so `Guest` reads as `guest`.
- [ ] AC2: Four passages cite the AC1 paragraph for how their lines are read. They are the PROFILE.md row of the tracking-rules file map, the open-PR caps bullet of its "Git and approval model" section, the first sentence of its "Collaboration mode" section, and section 1 of `skills/shared/copilot-review.md`.
- [ ] AC3: `profile_name` in `hooks/session_context.py` reads the `# Toolchain profile:` line by the AC1 read. It returns None for a PROFILE.md text whose only `# Toolchain profile:` line comes after the first `## ` line. It returns `r-package` for the line `# toolchain PROFILE: R-Package`. It returns the name for a text that opens with a byte-order mark.
- [ ] AC4: Section 1 of `skills/shared/copilot-review.md` says that the value `on` in any letter case turns the round on. Any other value, or no line, leaves the round off.
- [ ] AC5: `_profile_header` in `hooks/cairn_common.py` reads as each AC1 claim states. A line with a space before `#`, or with a space before the colon, is not read. A line with no value is passed over for a later line with a value. A value followed by more text reads as its first word.
- [ ] AC6: The `profile valid` check of `scripts/cairn_validate.py` skips a byte-order mark at the start of PROFILE.md. So it FAILs an unknown mode on a first line that follows the mark.
- [ ] AC7: The verify slot of `cairn/PROFILE.md` runs clean.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T1
- AC3 → T3
- AC4 → T1
- AC5 → T2
- AC6 → T4
- AC7 → T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Write the AC1 paragraph near the header-line sentence of tracking-rules "Toolchain profiles" (about line 741). Point the AC2 passages at it (tracking-rules lines 15, 343, and 401, and copilot-review.md section 1). Write the AC4 sentence in copilot-review.md section 1.
- [x] T2: In `hooks/tests/test_hooks.py`, beside `TestPushRemote`, add cases for the four AC5 inputs, through `collaboration_mode` or `push_remote`.
- [x] T3: Put a case-insensitive `# Toolchain profile:` regex in `hooks/cairn_common.py` and make `profile_name` read it through `_profile_header`. Update the comment at `hooks/cairn_common.py:404` that names `_PROFILE_HEADER`. Add tests for the three AC3 inputs.
- [x] T4: Open PROFILE.md with `utf-8-sig` in the profile check of `scripts/cairn_validate.py` (about line 831). Add a `scripts/tests` case where a BOM-led unknown mode line FAILs.
- [x] T5: Write one CHANGELOG entry under Unreleased for the toolchain line read (T3) and the validator fix (T4), each claim backed by its test.
- [x] T6: Run the verify slot.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-22: created by /milestone-plan from the candidate row "State how PROFILE header lines are read" (found at M317 review).
- 2026-10-22: tier check: milestone — the change edits shipped rulebook prose and hook code, and it needed a choice about the toolchain line.
- 2026-10-22: idea vet: one concern. The toolchain line is read another way (whole file, exact key case, no mark skip), so one stated read would be false for it. Answer at the question set: align it.
- 2026-10-22: collision check: the candidate row is absorbed. M184, M267, M315, and M317 shipped the readers and did not state the read. No D-entry rejects this. Both GitHub inboxes have no open items.
- 2026-10-22: criteria audit (full mode, fresh Opus reader): 6 findings, all taken. (b) now says `:` follows the key directly. (e) now says case does not count, which holds for the cap lines that keep the value as written. AC2 names four passages in place of a grep that missed them. AC5 states reader behavior, not a test count, and gains the leading-space, space-before-colon, and valueless-line cases. AC6 is new: the validator opened PROFILE.md without skipping a mark. AC3 keeps three inputs, because each pins a separate change to `profile_name`.
- 2026-10-22: plan gate chose moving the toolchain line onto the shared reader over naming it as an exception, because one read is simpler to state and follow; falsified by a PROFILE.md that needs its toolchain line after a `## ` heading or in a case-sensitive key.
- 2026-10-22: plan gate chose the shared read for the Copilot line (any case of `on`) over keeping `on` exact, because one read covers every header line; falsified by a repo that writes `On` and expects the round off.
- 2026-10-22: changelog: one entry for the toolchain read and the validator fix. The Copilot case change is not in it, because only prose reads that line and no test can back the claim.
- 2026-10-22: implement started on m318-profile-header-read. The untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's work and stay unstaged.
- 2026-10-22: T1 done. The "Header lines" paragraph follows the validator sentence in "Toolchain profiles", and the four AC2 passages cite it. copilot-review.md was 5 bytes under its 9,600-byte budget, so one sentence in section 2 and the off clause in section 1 were tightened, with the same meaning. It is now 9,580 bytes. The simple-english lint hook flags many sentences that predate this change in both files. Only the sentences this change wrote were fixed.
- 2026-10-22: T2 done. `test_line_shape_and_first_line_rules` in `TestPushRemote` covers the four AC5 inputs and claim (d), first line wins. Three planted defects in `_profile_header` turned it red (search in place of match, no first-match return, a space allowed before the colon with the rest of the line as value), and the file was restored.
- 2026-10-22: T3 done. `TOOLCHAIN_PROFILE_LINE` sits in `hooks/cairn_common.py`, and `profile_name` returns `_profile_header` on it, so session_context's own regex is gone. `test_profile_name_is_read_as_a_header_line` failed on the old reader with all three AC3 inputs, each for its own reason, and passes now. Hooks suite: 204 tests OK.
- 2026-10-22: T4 done. The profile check opens PROFILE.md with `utf-8-sig`. `test_mode_other_after_a_byte_order_mark_fails` exited 0 on the old validator and FAILs the run now, naming the line. Scripts suite: 446 tests OK, 21 skipped.
- 2026-10-22: T5 done. One entry heads "Changes that affect existing repos" in CHANGELOG.md Unreleased. Its claims rest on `test_profile_name_is_read_as_a_header_line` and `test_mode_other_after_a_byte_order_mark_fails`.
- 2026-10-22: claim audit: 19 claims read, 4 corrected — skills/shared/tracking-rules.md, hooks/cairn_common.py. The "Header lines" paragraph and the comment above `TOOLCHAIN_PROFILE_LINE` said one function does every read. They now name the hook reader, the pane's `profileHeader`, and the skills, and say the validator checks every mode line. The two passages that cite the paragraph became true with it. The re-read found 0 false.
- 2026-10-22: T6 done. Verify slot green: scripts suite, hooks suite, both `claude plugin validate` runs, and `claude plugin test .` (2466 pass, 0 fail). cairn_validate passes. Status set to review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
