# M300: A trivial edit keeps owed issues open

**Status:** done (2026-10-20, PR #313 https://github.com/jmgirard/cairn/pull/313)

**Goal:** In owner mode, the trivial route closes no issue whose number a kept candidate row holds as `#N` or an open milestone's `Resolves:` slot holds, and none after an open-PR read it could not finish or a failed check.

**Outcome:** `/milestone-plan` step 1's **Issue read (trivial route, owner mode)** paragraph now runs only after the five trivial-route checks pass; on a failed check the plan reads no issue and the option names no issue number. A text holds a number when it holds `#N` with no digit right after it. The route closes a number only when it reads `OPEN`, its URL path holds `/issues/`, no kept row's text holds it (title or detail, where M297 checked only the title), and no `Resolves:` slot of a milestone whose ROADMAP status is `planned`, `in-progress`, `blocked`, or `review` holds it; each other number is left alone with its reason. When the open-PR read failed, `gh` could not run for it, or it returned 100 PRs, the route closes no issue. The trivial option's naming sentences now apply only when no owner-mode check failed. `skills/tests/test_plan_tier_check.py` pins each new sentence; README's trivial-edit row and M297's Unreleased CHANGELOG entry state the new cases.

**Decisions:** D-200 (narrows D-195's kept-row clause and its Consequence on a number named only in a row's detail; protecting only issue-shaped references rejected, since finding numbers such as `diff-bug #4` share the spelling; D-108's door does not apply). Plan gate: a small fix over parking the row; edit M297's unreleased CHANGELOG entry over a new one.

**Review:** Criteria audit at plan (full, 5 findings, all fixed). Claim audit 21 claims, 2 corrected. One pass of four lenses: 20 findings, 6 fixed, 4 follow-up (new parked row "Close the last trivial-route issue gaps"), 10 rejected. Copilot (Lite, 1 body item rejected; summary reply posted). No returns, no amendments. Hygiene: row "Keep owed issues open on a trivial edit" graduated; M297 row pruned to the 3-row terminal cap. No lessons added or retired, nothing unparked.
