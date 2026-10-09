import { describe, expect, test } from 'claude-code/testing'

import { countPr, countsArgv, prCounts, prNodes } from './counts'
import type { PrNodes } from './counts'

// The counting rule (M225 AC2). Each case adds one item to a pull request
// whose anchor is set by the author's comment, the author's review, or the
// newest commit, and the count it expects comes from a short restatement
// of the rule in the test loop: another
// person's COMMENTED or CHANGES_REQUESTED review, or another person's
// conversation comment, strictly after the anchor.

const AUTHOR = 'ana'
const T2 = '2026-10-02T09:00:00Z'
const T3 = '2026-10-03T09:00:00Z'
const ANCHOR = '2026-10-05T09:00:00Z'
const TIMES = { before: '2026-10-04T23:59:59Z', equal: ANCHOR, after: '2026-10-05T09:00:01Z' } as const
const STATES = ['COMMENTED', 'CHANGES_REQUESTED', 'APPROVED', 'DISMISSED', 'PENDING'] as const
// The PR author, a person, a bot as Copilot's reviewer logs in, and a
// deleted account.
const AUTHORS = { 'PR author': { login: AUTHOR }, human: { login: 'bo' }, bot: { login: 'copilot-pull-request-reviewer' }, null: null } as const

// A pull request whose anchor is ANCHOR, set by the named item. The other
// two of the author's items sit earlier.
function base(anchor: 'review' | 'comment' | 'commit'): PrNodes {
  const at = (kind: string) => (kind === anchor ? ANCHOR : kind === 'commit' ? T2 : T3)
  return {
    author: AUTHOR,
    threads: [],
    reviews: [{ author: { login: AUTHOR }, state: 'COMMENTED', submittedAt: at('review') }],
    comments: [{ author: { login: AUTHOR }, createdAt: at('comment') }],
    commit: at('commit'),
  }
}

describe('the unanswered count over each axis (M225 AC2)', () => {
  for (const anchor of ['review', 'comment', 'commit'] as const) {
    test(`the base with the ${anchor} latest counts nothing`, () => {
      expect(countPr(base(anchor))).toEqual({ unresolved: 0, unanswered: 0 })
    })
    for (const [who, author] of Object.entries(AUTHORS)) {
      for (const [when, time] of Object.entries(TIMES)) {
        const counts = who !== 'PR author' && when === 'after'
        test(`${anchor} anchor: a comment by the ${who}, ${when}`, () => {
          const pr = base(anchor)
          pr.comments.push({ author, createdAt: time })
          expect(countPr(pr).unanswered).toBe(counts ? 1 : 0)
        })
        for (const state of STATES) {
          const reviewCounts = counts && (state === 'COMMENTED' || state === 'CHANGES_REQUESTED')
          test(`${anchor} anchor: a ${state} review by the ${who}, ${when}`, () => {
            const pr = base(anchor)
            pr.reviews.push({ author, state, submittedAt: time })
            expect(countPr(pr).unanswered).toBe(reviewCounts ? 1 : 0)
          })
        }
      }
    }
  }

  test('a review with no submittedAt never counts', () => {
    const pr = base('commit')
    pr.reviews.push({ author: { login: 'bo' }, state: 'COMMENTED', submittedAt: null })
    pr.reviews.push({ author: { login: 'bo' }, state: 'CHANGES_REQUESTED', submittedAt: null })
    expect(countPr(pr).unanswered).toBe(0)
  })

  // The author's APPROVED, DISMISSED, and PENDING reviews leave the anchor
  // where it was, so another person's comment between stays counted.
  for (const state of ['APPROVED', 'DISMISSED', 'PENDING'] as const) {
    test(`the author's later ${state} review does not set the anchor`, () => {
      const pr = base('commit')
      pr.comments.push({ author: { login: 'bo' }, createdAt: TIMES.after })
      pr.reviews.push({ author: { login: AUTHOR }, state, submittedAt: '2026-10-07T09:00:00Z' })
      expect(countPr(pr).unanswered).toBe(1)
    })
  }

  // Each anchor moves the line: an item counted against an older anchor
  // stops counting once the author comments, reviews, or pushes after it.
  for (const later of ['review', 'comment', 'commit'] as const) {
    test(`an author ${later} after another's comment clears it`, () => {
      const pr = base('commit')
      pr.comments.push({ author: { login: 'bo' }, createdAt: TIMES.after })
      expect(countPr(pr).unanswered).toBe(1)
      const newer = '2026-10-06T09:00:00Z'
      if (later === 'review') pr.reviews.push({ author: { login: AUTHOR }, state: 'COMMENTED', submittedAt: newer })
      if (later === 'comment') pr.comments.push({ author: { login: AUTHOR }, createdAt: newer })
      if (later === 'commit') pr.commit = newer
      expect(countPr(pr).unanswered).toBe(0)
    })
  }

  // A mixed pull request, its counts worked out by hand: the anchor is the
  // author's comment at 10-05; after it come a bot's COMMENTED review, a
  // person's CHANGES_REQUESTED review, a deleted account's comment, and an
  // APPROVED review, which does not count. Two of four threads are open.
  test('a mixed pull request', () => {
    const pr: PrNodes = {
      author: AUTHOR,
      threads: [{ isResolved: true }, { isResolved: false }, { isResolved: false }, { isResolved: true }],
      reviews: [
        { author: { login: 'bo' }, state: 'CHANGES_REQUESTED', submittedAt: '2026-10-01T00:00:00Z' },
        { author: { login: 'copilot-pull-request-reviewer' }, state: 'COMMENTED', submittedAt: '2026-10-06T00:00:00Z' },
        { author: { login: 'bo' }, state: 'CHANGES_REQUESTED', submittedAt: '2026-10-07T00:00:00Z' },
        { author: { login: 'cy' }, state: 'APPROVED', submittedAt: '2026-10-08T00:00:00Z' },
      ],
      comments: [
        { author: { login: 'bo' }, createdAt: '2026-10-02T00:00:00Z' },
        { author: { login: AUTHOR }, createdAt: ANCHOR },
        { author: null, createdAt: '2026-10-09T00:00:00Z' },
      ],
      commit: '2026-10-03T00:00:00Z',
    }
    expect(countPr(pr)).toEqual({ unresolved: 2, unanswered: 3 })
  })

  test('the unresolved count is the threads with isResolved false', () => {
    const pr = base('commit')
    pr.threads = [{ isResolved: false }, { isResolved: true }, { isResolved: false }, { isResolved: false }]
    expect(countPr(pr)).toEqual({ unresolved: 3, unanswered: 0 })
  })
})

// The reply shape `gh api graphql` prints, as GitHub returned it for a real
// pull request on 2026-10-09, with nodes filled in.
function reply(pr: unknown) {
  return { data: { repository: { pullRequest: pr } } }
}
const GOOD = {
  author: { login: AUTHOR },
  reviewThreads: { nodes: [{ isResolved: false }] },
  reviews: { nodes: [{ author: { login: 'bo' }, state: 'COMMENTED', submittedAt: TIMES.after }] },
  comments: { nodes: [{ author: null, createdAt: TIMES.after }] },
  commits: { nodes: [{ commit: { committedDate: ANCHOR } }] },
}
const ok = (value: unknown) => ({ exitCode: 0, stdout: `${JSON.stringify(value)}\n` })

describe('prCounts reads only the reply shape it names (M225 AC4)', () => {
  test('a good reply gives both counts', () => {
    expect(prCounts(ok(reply(GOOD)))).toEqual({ unresolved: 1, unanswered: 2 })
  })

  // With no commit time, the author's comment alone sets the anchor: the
  // other person's comment before it stops counting, and the review after
  // it still counts.
  test('a pull request with no commits anchors on the author alone', () => {
    const pr = {
      ...GOOD,
      comments: { nodes: [{ author: { login: 'bo' }, createdAt: T2 }, { author: { login: AUTHOR }, createdAt: T3 }] },
      commits: { nodes: [] },
    }
    expect(prNodes(reply(pr))?.commit).toBe(null)
    expect(prCounts(ok(reply(pr)))).toEqual({ unresolved: 1, unanswered: 1 })
  })

  const BAD: [string, unknown][] = [
    ['a null pullRequest', reply(null)],
    ['a null repository', { data: { repository: null } }],
    ['no data', { errors: [{ message: 'Could not resolve' }] }],
    ['a null PR author', reply({ ...GOOD, author: null })],
    ['a PR author with no login', reply({ ...GOOD, author: {} })],
    ['threads that are not a list', reply({ ...GOOD, reviewThreads: { nodes: null } })],
    ['a thread with a string isResolved', reply({ ...GOOD, reviewThreads: { nodes: [{ isResolved: 'false' }] } })],
    ['a review with a number state', reply({ ...GOOD, reviews: { nodes: [{ author: null, state: 1, submittedAt: null }] } })],
    ['a review with no submittedAt key', reply({ ...GOOD, reviews: { nodes: [{ author: null, state: 'COMMENTED' }] } })],
    ['a comment with a number login', reply({ ...GOOD, comments: { nodes: [{ author: { login: 7 }, createdAt: ANCHOR }] } })],
    ['a comment with no createdAt', reply({ ...GOOD, comments: { nodes: [{ author: null }] } })],
    ['a commit node with no commit', reply({ ...GOOD, commits: { nodes: [{}] } })],
    ['a null node', reply({ ...GOOD, comments: { nodes: [null] } })],
  ]
  for (const [name, value] of BAD) {
    test(`${name} fails the read`, () => {
      expect(prNodes(value)).toBe(null)
      expect(prCounts(ok(value))).toBe(null)
    })
  }

  test('a rejected call, a non-zero exit, and text that is not JSON fail the read', () => {
    expect(prCounts(null)).toBe(null)
    expect(prCounts({ exitCode: 1, stdout: JSON.stringify(reply(GOOD)) })).toBe(null)
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
