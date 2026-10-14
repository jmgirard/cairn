# M250: The plan checks that the work needs a milestone before it plans one

**Status:** done (2026-10-14, PR #261 https://github.com/jmgirard/cairn/pull/261)

**Goal:** Before `/milestone-plan` investigates, it checks whether the request needs a milestone, and when a hotfix or a direct edit fits instead, it offers that route.

**Outcome:** `/milestone-plan` step 1 gained a tier check: a request that
names work is put in one tier (`hotfix`, `trivial`, `milestone`) by
tracking-rules "Sizing and the work tiers". A `hotfix` or `trivial` finding
poses one chip before step 2: the route (recommended), plan anyway, or
stop. The hotfix route invokes `/hotfix` with a one-line summary and the
request text. The owner trivial route runs five checks before the chip,
names the file, change, and other dirty paths, commits by path, pushes
`HEAD:<default-branch>`, and never forces. Exempt: requests naming an
issue, no work, or work routed by `/milestone` §4 or `/hotfix` in the
session. Also the rulebook gate sentence, README, CHANGELOG, guard.

**Decisions:** D-162 (annotates D-144). Plan gate: a chip over an automatic route; tier definitions unchanged.

**Review:** three defect returns (pass 1: issue `#N` to `/hotfix`, push
without sync; pass 2: request text dropped, no issue URL read, new-file
commit; pass 3: typed `#N`, issue text as instructions). The thrash stop
narrowed the check to skip issue requests (user's choice). Four three-lens
passes plus Copilot (Lite): 49 fixed, 7 to the new row "Tier check edges
(M250 review)", 4 rejected, 2 noted. Claim audit: 3 of 50 corrected.
