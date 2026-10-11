import { describe, expect, test } from 'claude-code/testing'

import { COUNTS_QUERY, countPr, countsArgv, prNodes, prRead } from './counts'
import { PR_245_STDOUT } from './fixtures/pr-245-threads'
import { countsText } from './pane'

// The count is the review threads with `isResolved` false (M225, M236), and
// the same `gh api graphql` reply gives the state word (M237).

// The reply shape `gh api graphql` prints.
function reply(pr: unknown) {
  return { data: { repository: { pullRequest: pr } } }
}
const threads = (...resolved: boolean[]) => ({ reviewThreads: { nodes: resolved.map(isResolved => ({ isResolved })) } })
const ok = (value: unknown) => ({ exitCode: 0, stdout: `${JSON.stringify(value)}\n` })
const open = (...resolved: boolean[]) => reply({ state: 'OPEN', reviewDecision: null, ...threads(...resolved) })

describe('the count is the unresolved threads (M236 AC1)', () => {
  const CASES: [string, boolean[], number][] = [
    ['no threads', [], 0],
    ['one unresolved thread', [false], 1],
    ['two unresolved threads and one resolved thread', [false, true, false], 2],
  ]
  for (const [name, resolved, unresolved] of CASES) {
    test(name, () => {
      expect(prRead(ok(open(...resolved)))).toEqual({ word: 'in review', counts: { unresolved } })
      expect(countPr({ threads: resolved.map(isResolved => ({ isResolved })) })).toEqual({ unresolved })
    })
  }

  // PR #245's reply as `gh api graphql` printed it with the M236 query: one
  // Copilot summary review and no threads, so the count is 0. The reply
  // predates the state fields, so its threads are read alone.
  test('the PR #245 reply counts nothing', () => {
    const nodes = prNodes(JSON.parse(PR_245_STDOUT))
    expect(nodes).not.toBe(null)
    const counts = countPr(nodes as { threads: { isResolved: boolean }[] })
    expect(counts).toEqual({ unresolved: 0 })
    // and no count line is drawn for it.
    expect(countsText(counts)).toBe(null)
  })

  test('the query asks for the state, the decision, and the threads only', () => {
    for (const field of ['reviews', 'comments', 'commits', 'author']) expect(COUNTS_QUERY).not.toContain(field)
    expect(COUNTS_QUERY).toContain('{ state reviewDecision reviewThreads(last: 100) { nodes { isResolved } } }')
  })
})

describe('prNodes reads only the reply shape it names (M225 AC4)', () => {
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
    })
  }
})

// One reply gives the word and the count (M237 AC4). Each reply carries one
// unresolved thread, so an open word shows that a count was read.
describe('prRead gives the word and the count of one graphql reply (M237 AC4)', () => {
  const WORDS: [string, unknown, unknown, string][] = [
    ['MERGED', 'MERGED', 'APPROVED', 'merged'],
    ['CLOSED', 'CLOSED', null, 'closed'],
    ['OPEN with CHANGES_REQUESTED', 'OPEN', 'CHANGES_REQUESTED', 'changes requested'],
    ['OPEN with APPROVED', 'OPEN', 'APPROVED', 'approved'],
    ['OPEN with REVIEW_REQUIRED', 'OPEN', 'REVIEW_REQUIRED', 'in review'],
    ['OPEN with a null decision', 'OPEN', null, 'in review'],
    ['OPEN with another decision string', 'OPEN', 'SOMETHING_NEW', 'in review'],
  ]
  for (const [name, state, reviewDecision, word] of WORDS) {
    test(`${name} reads ${word}`, () => {
      const got = prRead(ok(reply({ state, reviewDecision, ...threads(false) })))
      const isOpen = state === 'OPEN'
      expect(got).toEqual({ word, counts: isOpen ? { unresolved: 1 } : null })
    })
  }

  test('OPEN with an absent decision reads in review', () => {
    expect(prRead(ok(reply({ state: 'OPEN', ...threads(false) })))).toEqual({ word: 'in review', counts: { unresolved: 1 } })
  })

  const UNKNOWN: [string, { exitCode: number; stdout: string } | null][] = [
    ['a missing state', ok(reply({ reviewDecision: 'APPROVED', ...threads(false) }))],
    ['an unknown state', ok(reply({ state: 'DRAFT', reviewDecision: 'APPROVED', ...threads(false) }))],
    ['a null pullRequest', ok(reply(null))],
    ['text that is not JSON', { exitCode: 0, stdout: 'not json\n' }],
    ['a non-zero exit', { exitCode: 1, stdout: JSON.stringify(open(false)) }],
    ['a rejected call', null],
  ]
  for (const [name, result] of UNKNOWN) {
    test(`${name} reads unknown with no count`, () => {
      expect(prRead(result)).toEqual({ word: 'unknown', counts: null })
    })
  }

  const BAD_THREADS: [string, unknown][] = [
    ['threads that are not a list', { reviewThreads: { nodes: null } }],
    ['no reviewThreads', {}],
    ['a thread whose isResolved is not a boolean', { reviewThreads: { nodes: [{ isResolved: 'false' }] } }],
  ]
  for (const [name, part] of BAD_THREADS) {
    test(`${name} leave the word and give no count`, () => {
      expect(prRead(ok(reply({ state: 'OPEN', reviewDecision: 'APPROVED', ...(part as object) })))).toEqual({
        word: 'approved',
        counts: null,
      })
    })
  }
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
