import { describe, expect, test } from 'claude-code/testing'

import { FIXTURES } from './fixtures.gen'
import { dirname, findRoot, loadBand, memorySource, sectionFields } from './reader'

describe('reader over every fixture (M193 AC5)', () => {
  test('the fixture domain is not empty', () => {
    expect(Object.keys(FIXTURES).length).toBeGreaterThan(8)
  })

  for (const [name, fixture] of Object.entries(FIXTURES)) {
    test(`${name}: rows, counts and next items match expected.json`, async () => {
      const rows = await loadBand(memorySource(fixture.files, fixture.cwd))
      expect(rows).toEqual(fixture.rows)
    })
  }

  test('no-roadmap expects an empty result', async () => {
    const fixture = FIXTURES['no-roadmap']
    expect(fixture.rows).toEqual([])
    expect(await loadBand(memorySource(fixture.files, fixture.cwd))).toEqual([])
  })

  test('missing-file expects no counts and no next items', async () => {
    const fixture = FIXTURES['missing-file']
    const [row] = await loadBand(memorySource(fixture.files, fixture.cwd))
    expect([row.tasksChecked, row.tasksTotal, row.criteriaChecked, row.criteriaTotal]).toEqual([null, null, null, null])
    expect([row.nextTask, row.nextCriterion]).toEqual([null, null])
  })

  test('nested-first names the nested task, less its box and spaces', async () => {
    const fixture = FIXTURES['nested-first']
    const [row] = await loadBand(memorySource(fixture.files, fixture.cwd))
    expect(row.nextTask).toBe('T1a: Nested task, open, with extra spaces after the box.')
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
    expect(sectionFields(text, 'Tasks')).toEqual({ checked: 2, total: 4, next: 'T2' })
    expect(sectionFields(text, 'Acceptance criteria')).toEqual({ checked: 1, total: 1, next: null })
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
    expect(rows.map(r => [r.id, r.tasksChecked, r.tasksTotal, r.nextTask])).toEqual([['M002', null, null, null]])
    expect(reads).toEqual(['/cairn/ROADMAP.md'])
  })

  test('dirname stops at the root', () => {
    expect(dirname('/a/b')).toBe('/a')
    expect(dirname('/a')).toBe('/')
    expect(dirname('/')).toBe('/')
    expect(dirname('C:\\a')).toBe('C:\\')
  })
})
