# M60: Git-safety hooks — force-push deny, merge-marker restore (done)

- **Merged:** 2026-07-16 · PR https://github.com/jmgirard/cairn/pull/58
- **Goal:** the two honor-system git rules with cheap mechanical teeth get
  hooks: force-push to the default branch denied at PreToolUse; a failed
  guarded merge no longer consumes the approval marker (RR01 recs 8+13).
- **Outcome:** `force_push_guard.py` denies all three force forms (flags,
  `+refspec`, HEAD forms), explicit-ref and on-default-branch shapes;
  feature-branch/plain pushes pass (D-023). `merge_guard_post.py` completes
  a rename lifecycle: merge_guard consumes `.merge-approved` by rename to
  `.pending`; post hook restores on PostToolUseFailure (Bash nonzero exit,
  contract pinned in references/claude-code-hooks.md), deletes on success —
  never mints. Ends the M33 rewrite-the-marker step. stop_guard excludes
  the pending basename; `.pending` gitignore entry joined the scaffold spec;
  DESIGN names all seven hooks; rulebook records the mechanical backing
  (test_git_safety_hooks + 9 mutation entries).
- **Key decisions (gate):** cover `+refspec` (zero-FP force form); rename
  lifecycle over stateless recreate (structurally cannot mint approval).
- **Review:** 3 lenses + scorer — F1 (90) substring-shadowed hook guard,
  F4 (85) parse edges, F5 (80) eager ls-remote: fixed; F2 (65) secondary-
  remote deny documented as accepted; F3 (55) composed-bypass logged.
- **Live-fire residue:** merge_guard's rename ran live at this very merge
  (script bodies read per invocation); full checklist incl. restore/retry
  flow still owed in a fresh conversation — see work log in git history.
