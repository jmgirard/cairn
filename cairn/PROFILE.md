# Profile

## Verify

Run from the repo root, and check each exit code:

```
python3 -m unittest discover -s scripts/tests
python3 -m unittest discover -s hooks/tests
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

The two validate checks pass with warnings and fail on an error. Do not add
`--strict`: it fails on warnings, and the root `CLAUDE.md` always draws one.
This repo has no CI, so a PR is mergeable on these passing locally.

## Changelog

`CHANGELOG.md`. An entry goes under the `## Unreleased` heading, in words a
user of the plugin would use.

## Release

- Print the words in the skill, as numbers with no threshold:
  `wc -w skills/cairn/SKILL.md skills/cairn/verbs/*.md skills/cairn/reviewer-brief.md`.
- Set `version` in `.claude-plugin/plugin.json` and in the plugin entry of
  `.claude-plugin/marketplace.json` to the new version. The marketplace
  validate must show no version warning.
- Retitle the changelog's `## Unreleased` heading to the version and date.
- The tag is `v<version>`, and the tag is the release.
- Give the user a `gh release create` command whose notes are the new
  changelog section. Never run it.
