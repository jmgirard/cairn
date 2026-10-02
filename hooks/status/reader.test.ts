import { describe, expect, test } from 'claude-code/testing'

import { FIXTURES } from './fixtures.gen'
import { dirname, findRoot, loadBand, memorySource, taskCounts } from './reader'

describe('reader over every fixture (AC4)', () => {
  test('the fixture domain is not empty', () => {
    expect(Object.keys(FIXTURES).length).toBeGreaterThan(5)
  })

  for (const [name, fixture] of Object.entries(FIXTURES)) {
    test(`${name}: rows, statuses and task counts match expected.json`, async () => {
      const rows = await loadBand(memorySource(fixture.files, fixture.cwd))
      expect(rows).toEqual(fixture.rows)
    })
  }

  test('no-roadmap expects an empty result', async () => {
    const fixture = FIXTURES['no-roadmap']
    expect(fixture.rows).toEqual([])
    expect(await loadBand(memorySource(fixture.files, fixture.cwd))).toEqual([])
  })

  test('missing-file expects no counts', async () => {
    const fixture = FIXTURES['missing-file']
    const rows = await loadBand(memorySource(fixture.files, fixture.cwd))
    expect(rows.map(r => [r.checked, r.total])).toEqual([[null, null]])
  })
})

describe('reader details', () => {
  test('the walk goes up two levels from a subdirectory', async () => {
    const fixture = FIXTURES['subdirectory']
    expect(fixture.cwd).toBe('/pkg/src')
    expect(await findRoot(memorySource(fixture.files, fixture.cwd), fixture.cwd)).toBe('/')
  })

  test('counts only the first ## Tasks section, any indent, x or X', () => {
    const text = [
      '## Acceptance criteria',
      '- [x] AC1',
      '## Tasks',
      '- [x] T1',
      '    - [X] T1a',
      '- [ ] T2',
      '### Inside',
      '- [ ] T3',
      '## Work log',
      '- [x] not a task',
      '## Tasks',
      '- [x] a second Tasks section, not read',
    ].join('\n')
    expect(taskCounts(text)).toEqual({ checked: 2, total: 4 })
  })

  test('a milestone path that is not a regular file is never read', async () => {
    const fixture = FIXTURES['single-in-progress']
    const files = fixture.files
    const reads: string[] = []
    const source = {
      cwd: async () => '/',
      // The ROADMAP is a file; the milestone path exists but is a pipe.
      isFile: async (path: string) => path === '/cairn/ROADMAP.md',
      read: async (path: string) => {
        reads.push(path)
        return files[path] ?? null
      },
    }
    const rows = await loadBand(source)
    expect(rows.map(r => [r.id, r.checked, r.total])).toEqual([['M002', null, null]])
    expect(reads).toEqual(['/cairn/ROADMAP.md'])
  })

  test('dirname stops at the root', () => {
    expect(dirname('/a/b')).toBe('/a')
    expect(dirname('/a')).toBe('/')
    expect(dirname('/')).toBe('/')
    expect(dirname('C:\\a')).toBe('C:\\')
  })
})
