// The stdout of `gh api graphql --hostname github.com` with the M237
// `COUNTS_QUERY` for jmgirard/cairn, captured unedited on 2026-10-10. PR
// #246 was merged with no review decision and no threads. PR #247 was open
// with no review decision and one unresolved Copilot thread.
export const PR_246_STDOUT =
  '{"data":{"repository":{"pullRequest":{"state":"MERGED","reviewDecision":null,"reviewThreads":{"nodes":[]}}}}}'
export const PR_247_STDOUT =
  '{"data":{"repository":{"pullRequest":{"state":"OPEN","reviewDecision":null,"reviewThreads":{"nodes":[{"isResolved":false}]}}}}}'
