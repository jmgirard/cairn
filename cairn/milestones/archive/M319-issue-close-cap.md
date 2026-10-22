# M319: Let PROFILE.md set the guest close limit

**Status:** done (2026-10-22, PR #332 https://github.com/jmgirard/cairn/pull/332)

**Goal:** A guest repo's `cairn/PROFILE.md` can set or remove the daily limit on issue closes with a `# Issue close cap:` line (D-215).

**Outcome:** `ISSUE_CLOSE_CAP_LINE` and `issue_close_cap(root)` in `hooks/cairn_common.py` read the line: a `[1-9][0-9]?` value sets the limit, `off` in any case removes it, and no line or any other value gives 3, with the untaken value named as written. `host_rules(root)` in `hooks/session_context.py` builds the guest rules from `HOST_RULES_BEFORE_LIMIT` and `HOST_RULES_AFTER_LIMIT` around the close clause ("at most N such close(s)", or "have no daily limit"), plus a note for an untaken line; with no line the text equals the old `HOST_RULES`. Guest rule (3) in tracking-rules opens "By default, make at most 3", states the line, counts only with a limit, and says a full page of 100 events whose oldest event falls on the current UTC day counts as reaching the limit (D-216, corrected by D-217). The file-map row, DESIGN.md's header list (six lines), README's guest passage, and a CHANGELOG Unreleased entry describe it. Requested by the easystats session for the user.

**Decisions:** D-215 (the line; supersedes D-213's fixed daily limit), D-216 (the full-page clause; supersedes D-215's sentence), D-217 (corrects D-216's count to "100 or more").

**Review:** Criteria audit at plan (full, 9 findings, all taken). Claim audits: 23 claims, 1 corrected; then 13 claims on the return, 1 corrected (D-217). One amendment return on AC1 (the full-page clause blocked every close on a busy repo), re-audited twice. Two four-lens passes gave 37 findings: 2 the amendment, 14 fixed, 5 to the new candidate row "State the close count in guest text", 16 rejected (none as `edge`). Copilot: no review recorded on PR #332. Hygiene: no row graduated or unparked, and no lesson added (LESSONS at its byte cap). The rulebook-mass baseline in `skills/milestone/SKILL.md` stays at M317's figure, so the audit reports the growth.
