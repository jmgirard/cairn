import { describe, expect, test } from 'claude-code/testing'

import { COUNTS_QUERY, countPr, countsArgv, prCounts, prNodes } from './counts'
import { PR_245_STDOUT } from './fixtures/pr-245-threads'
import { countsText } from './pane'

// The count is the review threads with `isResolved` false (M225, M236).

// The reply shape `gh api graphql` prints.
function reply(pr: unknown) {
  return { data: { repository: { pullRequest: pr } } }
}
const threads = (...resolved: boolean[]) => ({ reviewThreads: { nodes: resolved.map(isResolved => ({ isResolved })) } })
const ok = (value: unknown) => ({ exitCode: 0, stdout: `${JSON.stringify(value)}\n` })

describe('the count is the unresolved threads (M236 AC1)', () => {
  const CASES: [string, boolean[], number][] = [
    ['no threads', [], 0],
    ['one unresolved thread', [false], 1],
    ['two unresolved threads and one resolved thread', [false, true, false], 2],
  ]
  for (const [name, resolved, unresolved] of CASES) {
    test(name, () => {
      expect(prCounts(ok(reply(threads(...resolved))))).toEqual({ unresolved })
      expect(countPr({ threads: resolved.map(isResolved => ({ isResolved })) })).toEqual({ unresolved })
    })
  }

  // PR #245's reply as `gh api graphql` printed it: one Copilot summary
  // review and no threads, so the count is 0.
  test('the PR #245 reply counts nothing', () => {
    const counts = prCounts({ exitCode: 0, stdout: PR_245_STDOUT })
    expect(counts).toEqual({ unresolved: 0 })
    // and no count line is drawn for it.
    expect(countsText(counts as { unresolved: number })).toBe(null)
  })

  test('the query asks for threads only', () => {
    for (const field of ['reviews', 'comments', 'commits', 'author']) expect(COUNTS_QUERY).not.toContain(field)
    expect(COUNTS_QUERY).toContain('reviewThreads(last: 100) { nodes { isResolved } }')
  })
})

describe('prCounts reads only the reply shape it names (M225 AC4)', () => {
  const BAD: [string, unknown][] = [
    ['a null pullRequest', reply(null)],
    ['a null repository', { data: { repository: null } }],
    ['no data', { errors: [{ message: 'Could not resolve' }] }],
    ['threads that are not a list', reply({ reviewThreads: { nodes: null } })],
    ['no reviewThreads', reply({})],
    ['a thread with a string isResolved', reply({ reviewThreads: { nodes: [{ isResolved: 'false' }] } })],
    ['a null node', reply({ reviewThreads: { nodes: [null] } })],
  ]
  for (const [name, value] of BAD) {
    test(`${name} fails the read`, () => {
      expect(prNodes(value)).toBe(null)
      expect(prCounts(ok(value))).toBe(null)
    })
  }

  test('a rejected call, a non-zero exit, and text that is not JSON fail the read', () => {
    expect(prCounts(null)).toBe(null)
    expect(prCounts({ exitCode: 1, stdout: JSON.stringify(reply(threads(false))) })).toBe(null)
    expect(prCounts({ exitCode: 0, stdout: 'not json\n' })).toBe(null)
  })
})

describe('countsArgv names the owner, repo, and number of the URL (M225 AC1)', () => {
  const arg = (argv: string[] | null, name: string) => argv?.find(a => a.startsWith(`${name}=`))
  test('two URLs with different owners, repos, and numbers', () => {
    const a = countsArgv('https://github.com/alpha/one/pull/12')
    const b = countsArgv('https://github.com/beta/two/pull/9001')
    expect(a?.slice(0, 3)).toEqual(['gh', 'api', 'graphql'])
    expect([arg(a, 'owner'), arg(a, 'repo'), arg(a, 'number')]).toEqual(['owner=alpha', 'repo=one', 'number=12'])
    expect([arg(b, 'owner'), arg(b, 'repo'), arg(b, 'number')]).toEqual(['owner=beta', 'repo=two', 'number=9001'])
    // The number goes as an Int, the owner and repo as strings.
    expect(a?.[a.indexOf('number=12') - 1]).toBe('-F')
    expect(a?.[a.indexOf('owner=alpha') - 1]).toBe('-f')
    expect(a?.[a.indexOf('repo=one') - 1]).toBe('-f')
  })

  test('a URL of another form gives no argv', () => {
    expect(countsArgv('https://github.com/alpha/one/pull/12/files')).toBe(null)
    expect(countsArgv('https://example.com/alpha/one/pull/12')).toBe(null)
  })
})
