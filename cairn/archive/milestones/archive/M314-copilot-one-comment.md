# M314: Answer each Copilot review in one PR comment

**Status:** done (2026-10-22, PR #328 https://github.com/jmgirard/cairn/pull/328)

**Goal:** In every mode, the Copilot round and `/copilot-review` answer a Copilot review with one PR comment that gives each note's outcome, in place of a reply on each thread.

**Outcome:** `skills/shared/copilot-review.md` §5 posts no reply on a Copilot thread; its `/replies` command is gone. Each Copilot review that has a note (an unresolved Copilot thread, tied to its review by the first comment's `pullRequestReview{url}`, else the newest review; or a body finding with no anchor) gets one PR comment once every note has a disposition and each fix is pushed: the review's URL, then one one-sentence line per note (`fixed in <short-sha>`, why it is not a problem, or left for a later change), no thanks, no cairn vocabulary in guest mode. The threads it names are resolved after it. A review whose URL an operator comment already carries (no digit after it) gets no second comment and no dispositions, and its open threads are resolved. A return-floor item puts only its own review's comment and resolves on hold, and §6 reports a held review. `/copilot-review` (description, steps 3, 4, 6 Comment, 7 Resolve), `/hotfix`, `/milestone-review` step 7 (its query selects §4's fields), README, DESIGN, and the Unreleased CHANGELOG entries follow; the hand-run guards in `skills/tests` were updated, with three new guards. The module stays within its budget (162 lines, 9,595 bytes). Trigger: the second easystats audit (175 inline Copilot replies in two weeks).

**Decisions:** D-212 (one comment per review, no thread reply, in every mode; supersedes D-153's thread reply and D-187's order and its "before that thread gets a reply"; passes D-108's door on the audit).

**Review:** Criteria audit at plan (full, all findings taken). Claim audit: 24 claims, 2 corrected. Four fresh reviewers: 19 findings fixed, 12 rejected (none as `edge`), none to a follow-up row. Copilot (Lite): 2 notes, both fixed, answered in one comment and resolved, the first run of the new form. No lesson added (LESSONS at its cap), and no row unparked.
