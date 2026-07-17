<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M70: Docker-image toolchain profile

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m70-docker-image-profile · https://github.com/jmgirard/cairn/pull/68   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Ship a fourth toolchain profile, `docker-image`, for repos whose sole
deliverable is a container image — its seven slots plus the init-detection,
inference, count-claim, greenfield-chip, and shipped-profile-test wiring.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- `skills/shared/profiles/docker-image.md` — all seven slots, under the 120-line
  PROFILE cap. `verify` = `hadolint` + `docker build` as the hard gate, with a
  vulnerability scan (trivy/grype) + container-structure-test named
  recommended-but-optional. `release-walk` = tag, `buildx`/`docker build`,
  `docker push` to a container registry (GHCR / Docker Hub), self-submits
  nothing. `changelog` = `CHANGELOG.md`.
- init-detection wiring in `skills/cairn-init/SKILL.md`: `Dockerfile` as the
  sole toolchain marker → `docker-image`; `Dockerfile` **plus** a language
  marker (`DESCRIPTION` / `pyproject.toml` / `setup.py` / `setup.cfg`) → a
  **disambiguation gate** asking which is the primary deliverable (cairn-init
  only, where a user is present); language marker without a Dockerfile →
  precedence unchanged. Add a fourth greenfield project-type chip option
  ("Docker image").
- Inference-fallback update in `tracking-rules.md` "Toolchain profiles": absent
  `PROFILE.md`, no user → deterministic order `DESCRIPTION` → `pyproject`/
  `setup` → `Dockerfile`-only → `generic`; when both a Dockerfile and a
  language marker are present at inference time the **language marker wins**
  (back-compat: a pre-profile repo shipping a Dockerfile beside `pyproject`
  still infers `python`). The disambiguation gate is cairn-init-only.
- Bump every "three profiles ship" count-claim to four naming `docker-image`:
  `DESIGN.md` (Purpose & Scope + Architecture) and `tracking-rules.md`
  "Toolchain profiles".

**Out:**
- Docker Compose / multi-image repos — this profile targets a single-image
  deliverable; multi-image orchestration → a new candidate row if it ever bites.
- Making trivy / container-structure-test **mandatory** — deliberately optional
  per the M70 plan gate; tightening the gate → a future milestone if adopters
  ask.
- Multi-arch platform / registry auto-selection — lives in the profile's
  `greenfield-openers` slot + DESIGN Conventions, not init-detection.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1 — `skills/shared/profiles/docker-image.md` exists and defines exactly
      the seven known slots, each non-empty (the same schema `cairn_validate`
      enforces on a repo `PROFILE.md`).
- [x] AC2 — its `verify` slot names `hadolint` and `docker build` as the hard
      gate and names a vulnerability scan (trivy/grype) + container-structure-test
      as recommended-but-optional (not mandatory).
- [x] AC3 — its `release-walk` slot targets a container registry (`docker push`,
      GHCR/Docker Hub) and self-submits nothing (parity with r-package/python).
- [x] AC4 — init-detection classifies: Dockerfile-only → `docker-image`;
      Dockerfile + a language marker → a disambiguation gate (cairn-init only);
      language marker without Dockerfile → unchanged. The inference fallback
      (`PROFILE.md` absent) deterministically keeps the language marker when
      both are present.
- [x] AC5 — the greenfield project-type chip offers a Docker-image option (≤4
      options total).
- [x] AC6 — every "three profiles ship" count-claim (`DESIGN.md`,
      `tracking-rules.md`) reads "four" and names `docker-image`, and the
      shipped-profile test enumeration includes `docker-image` so the real
      validator (`test_shipped_reference_profiles_are_valid`) exercises it.
- [x] AC7 — the `generic` profile carries no docker toolchain tokens (negative
      parity with the r/python no-bleed tests); new prose-guards are
      mutation-registered (`test_mutation_harness.py`).
- [x] AC8 — the `verify` slot is clean: all three stdlib `unittest` suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. Review reads to fence evidence. -->

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T2, T3
- AC5 → T2
- AC6 → T1, T3, T4
- AC7 → T1
- AC8 → T1, T2, T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Author `skills/shared/profiles/docker-image.md` (seven slots, per
      Scope), and ship its guards in the same commit: extend
      `test_toolchain_profiles.py`'s shipped-profile tuple + the
      `test_shipped_reference_profiles_are_valid` iteration to include
      `docker-image`; add a docker-token positive test and a generic-no-docker
      negative test; mutation-register the new prose-guards. Suite green.
- [x] T2 — Wire init-detection in `skills/cairn-init/SKILL.md` (Dockerfile-only
      → docker-image; Dockerfile + language marker → disambiguation gate) and
      add the fourth greenfield project-type chip option; ship the gate-wording
      guard in cairn-init's test file, mutation-registered. Suite green.
- [x] T3 — Update the inference fallback + "three→four" count-claim in
      `tracking-rules.md` "Toolchain profiles" (deterministic language-wins at
      inference), with its guard update. Suite green.
- [x] T4 — Bump the `DESIGN.md` count-claims (Purpose & Scope + Architecture)
      to four naming `docker-image`; update any DESIGN-count guard. Suite green.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-17: created by /milestone-plan.
- 2026-07-17: T1 — authored docker-image.md (113 lines, <120 cap); extended both shipped-profile enumeration tuples (test_toolchain_profiles + test_scripts); added TestDockerImageProfile + 2 mutation registrations. All three suites green (227/96/55).
- 2026-07-17: T2 — cairn-init init-detection: Dockerfile-only → docker-image, Dockerfile+language-marker → disambiguation gate; greenfield project-type chip gains a Docker-image option; repair backfill keeps language marker on a hybrid. Guard + mutation added; caught the M59 reflow trap (anchor phrase wrapped mid-line, reflowed). Suites green.
- 2026-07-17: T3 — tracking-rules "Toolchain profiles": three→four profiles, inference order gains a Dockerfile-sole-marker branch (language ranks first at inference). Renamed the guard class Three→Four, added order+count asserts and a "Four profiles ship" mutation. Suites green.
- 2026-07-17: T4 — DESIGN.md count-claims (Purpose & Scope + Architecture) bumped three→four naming docker-image. All tasks done; status → review. All three suites green; validate clean (only the justified 8-AC sizing advisory).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

**Reviewed 2026-07-17 · PR #68 · branch 5 ahead / 0 behind origin/main (no sync needed).**

Evidence per criterion (fresh runs):
- AC1 — `test_shipped_reference_profiles_are_valid` (real validator over docker-image.md: 7 slots present + non-empty, none unrecognized) green; `TestDockerImageProfile.test_docker_profile_defines_exactly_the_seven_slots` green; file 113 lines (<120 cap). ✓
- AC2 — `test_docker_verify_gates_lint_and_build_scan_optional` green (hadolint + `docker build` hard gate; trivy + container-structure-test recommended-but-optional). ✓
- AC3 — `test_docker_release_walk_pushes_to_registry_and_self_pushes_nothing` green (`docker push`, GHCR/Docker Hub, "cairn pushes nothing"). ✓
- AC4 — `TestInitSelection.test_init_selects_docker_and_runs_the_disambiguation_gate` green (Dockerfile-only → docker-image; hybrid → disambiguation gate) + `TestRulebookNamesFourProfiles.test_rulebook_inference_order` green (r-package < python < docker-image; language ranks first at inference). ✓
- AC5 — greenfield project-type chip "Docker image" option asserted (same init test); 4 options total (R/Python/Docker/generic). ✓
- AC6 — `TestRulebookNamesFourProfiles.test_rulebook_names_four_profiles` green; DESIGN.md carries "Four profiles ship" + docker-image (grep=3 hits); both shipped-profile enumeration tuples include docker-image (exercised by the AC1 real-validator run). ✓
- AC7 — `test_generic_profile_has_no_docker_toolchain` green; mutation harness green via `discover` (4 new docker registrations blanked→fail; completeness passes). ✓
- AC8 — all three suites green: skills 229 / scripts 96 / hooks 55. ✓

Consistency gate:
- Universal: `cairn_validate.py` exit 0 — weight caps / coverage complete / principles slot valid / profile valid all PASS; lone WARN is the sizing advisory (8 AC), justified at plan (7 substantive + mandated verify-clean; profile+wiring indivisible, mirrors M48) — advisory, not a gate failure.
- `cairn_impact` skipped: M70 works under GP3 but changes no principle *text* (Principles-touched slot is "works under", not a wording change).
- Toolchain (generic `consistency-gate` slot): "none" → clean no-op.

Fresh-context reviewer fan-out (3 lenses + scorer):
- [O] diff-bug: 1 finding. [S] blame-history: none. [S] prior-PR-comments: no prior-PR evidence (expected — LESSONS M40).
- **F1 (scored 90 → actioned, fixed):** docker-image.md `consistency-gate` blessed `--build-arg` as a secret channel ("build secrets use `--secret`/build args"), contradicting the same bullet's "No secrets baked into layers" — build-arg values persist in `docker history`. Fixed: BuildKit `--secret` mounts only, never `--build-arg` (visible in `docker history`) or committed files. A real security-doctrine error adopters would have followed.
- Post-fix: all three suites green (229/96/55); docker-image.md 114 lines (<120); `cairn_validate` exit 0.
