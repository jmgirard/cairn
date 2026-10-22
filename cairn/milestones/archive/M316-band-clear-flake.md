# M316: Fix the flaky refused-clear band tests

**Status:** dropped (2026-10-22, no PR; branch `m316-band-clear-flake` kept locally, tracking commits only, never pushed)

**Goal:** The refused-clear tests of M221 AC4 in `hooks/status/band.test.tsx` stop failing at random with a doubled `/clear` fill, because the cause of the second fill is found and removed.

**Outcome:** Not shipped, no code changed. The recorded fails (CLI 2.1.287, 2026-10-22) were a refused-clear case with two `/clear` fills from one `command.run` record, and a resume case with an extra `/clear` fill before its own. Probes in a scratch copy ruled out late calls from an ended case (the kit rejects them), mod state carried across cases (each case loads a fresh copy of the module), six forced orders of press and session end, and an engine fill of its own after a refused run. 12 band-only runs and 10 full runs on the same CLI all passed. The one documented mechanism that fits the first fail is the engine re-running a hook in a fresh copy after a lost hooks worker, which reuses the first `$.command.run` result but makes a `$.prompt.fill` again; nothing confirmed it. The user demoted the milestone at the stop: dropped, with the idea kept as the parked candidate row "Fix the flaky refused-clear band tests".

**Decisions:** none promoted. The plan gate chose 20 repeat runs over 50 for AC3; it was never reached.

**Review:** none. Next try: tag each fallback toast with a per-load id and strip it in the tests' toast hook (the scratch probe's method), so a recurring fail shows whether two copies of the mod made the two fills.
