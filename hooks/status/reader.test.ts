import { describe, expect, test } from 'claude-code/testing'

import { FIXTURES } from './fixtures.gen'
import {
  canonId,
  dirname,
  findRoot,
  loadBand,
  memorySource,
  parseDepends,
  parseRoadmapRows,
  sectionFields,
  workableRows,
} from './reader'

describe('reader over every fixture (M193 AC5, M199 AC2)', () => {
  test('the fixture domain is not empty', () => {
    expect(Object.keys(FIXTURES).length).toBeGreaterThan(8)
  })

  for (const [name, fixture] of Object.entries(FIXTURES)) {
    test(`${name}: rows, counts and next items match expected.json`, async () => {
      const { rows } = await loadBand(memorySource(fixture.files, fixture.cwd))
      expect(rows).toEqual(fixture.rows)
    })

    test(`${name}: the workable list matches expected.json`, async () => {
      const { workable } = await loadBand(memorySource(fixture.files, fixture.cwd))
      expect(workable.map(row => row.id)).toEqual(fixture.workable)
    })
  }

  test('no-roadmap expects an empty result', async () => {
    const fixture = FIXTURES['no-roadmap']
    expect(fixture.rows).toEqual([])
    expect(await loadBand(memorySource(fixture.files, fixture.cwd))).toEqual({ rows: [], workable: [] })
  })

  test('missing-file expects no counts and no next items', async () => {
    const fixture = FIXTURES['missing-file']
    const [row] = (await loadBand(memorySource(fixture.files, fixture.cwd))).rows
    expect([row.tasksChecked, row.tasksTotal, row.criteriaChecked, row.criteriaTotal]).toEqual([null, null, null, null])
    expect([row.nextTask, row.nextCriterion]).toEqual([null, null])
  })

  test('nested-first names the nested task, less its box and spaces', async () => {
    const fixture = FIXTURES['nested-first']
    const [row] = (await loadBand(memorySource(fixture.files, fixture.cwd))).rows
    expect(row.nextTask).toBe('T1a: Nested task, open, with extra spaces after the box.')
  })

  test('the workable list is computed while a row is active', async () => {
    const fixture = FIXTURES['six-active']
    const band = await loadBand(memorySource(fixture.files, fixture.cwd))
    expect(band.rows.length).toBe(6)
    expect(band.workable).toEqual([{ id: 'M073', title: 'A planned row between them' }])
  })

  test('idle-deps: an archive file marks its id done only directly under the archive directory', async () => {
    const fixture = FIXTURES['idle-deps']
    expect(Object.keys(fixture.files)).toContain('/cairn/milestones/archive/sub/M077-nested.md')
    const ids = (await loadBand(memorySource(fixture.files, fixture.cwd))).workable.map(row => row.id)
    // M040 needs M57, which only the archive file M0057-pruned.md marks done.
    expect(ids).toContain('M040')
    // M051 needs M077, whose only file sits one directory deeper.
    expect(ids).not.toContain('M051')
  })
})

describe('the workable list (M199 AC1)', () => {
  const roadmap = (lines: string[]) =>
    parseRoadmapRows(['| ID | Title | Status | Depends on | Priority | File/Archive |', '|---|---|---|---|---|---|', ...lines].join('\n'))

  test('Depends-on cells in their comma, space, dash, and malformed forms', () => {
    expect(parseDepends('M001, M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('M001 M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('M001,M002')).toEqual(['M001', 'M002'])
    expect(parseDepends('—')).toEqual([])
    expect(parseDepends('')).toEqual([])
    expect(parseDepends('m001 M M1a')).toEqual([])
  })

  test('ids compare at three-digit padding', () => {
    expect(canonId('M57')).toBe('M057')
    expect(canonId('M0057')).toBe('M057')
    expect(canonId('M1000')).toBe('M1000')
    expect(canonId('Mfoo')).toBe('Mfoo')
  })

  test('a done row meets a dependency spelled at another padding', () => {
    const rows = roadmap(['| M57 | Shipped | done | — | normal | m |', '| M060 | Next | planned | M057 | normal | m |'])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M060'])
  })

  test('only an archive file ending in .md marks its id done', async () => {
    const text = [
      '| ID | Title | Status | Depends on | Priority | File/Archive |',
      '|---|---|---|---|---|---|',
      '| M091 | On a text file | planned | M090 | high | m |',
      '| M093 | On a markdown file | planned | M092 | normal | m |',
    ].join('\n')
    const files = {
      '/cairn/ROADMAP.md': text,
      '/cairn/milestones/archive/M090-notes.txt': '',
      '/cairn/milestones/archive/M092-shipped.md': '',
    }
    expect((await loadBand(memorySource(files, '/'))).workable.map(r => r.id)).toEqual(['M093'])
  })

  test('a priority word that names an object property reads as normal', () => {
    const rows = roadmap([
      '| M002 | Low | planned | — | low | m |',
      '| M003 | Odd | planned | — | constructor | m |',
      '| M004 | Normal | planned | — | normal | m |',
    ])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M003', 'M004', 'M002'])
  })

  test('a dependency on a planned, blocked, or unknown milestone holds a row back', () => {
    const rows = roadmap([
      '| M001 | Base | planned | — | low | m |',
      '| M002 | Held | blocked | — | low | m |',
      '| M010 | On planned | planned | M001 | high | m |',
      '| M011 | On blocked | planned | M002 | high | m |',
      '| M012 | On unknown | planned | M099 | high | m |',
      '| M013 | On archive | planned | M99 | high | m |',
    ])
    expect(workableRows(rows, ['M099']).map(r => r.id)).toEqual(['M012', 'M013', 'M001'])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M001'])
  })

  test('only planned rows are workable', () => {
    const rows = roadmap([
      '| M001 | A | in-progress | — | high | m |',
      '| M002 | B | review | — | high | m |',
      '| M003 | C | blocked | — | high | m |',
      '| M004 | D | done | — | high | m |',
      '| M005 | E | candidate | — | high | m |',
      '| M006 | F | Planned | — | low | m |',
    ])
    expect(workableRows(rows, []).map(r => r.id)).toEqual(['M006'])
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
      list: async () => null,
    }
    const { rows } = await loadBand(source)
    expect(rows.map(r => [r.id, r.tasksChecked, r.tasksTotal, r.nextTask])).toEqual([['M002', null, null, null]])
    expect(reads).toEqual(['/cairn/ROADMAP.md'])
  })

  test('a found ROADMAP that cannot be read gives null, and no ROADMAP found gives an empty band (M200)', async () => {
    const fixture = FIXTURES['single-in-progress']
    const source = { ...memorySource(fixture.files, fixture.cwd), read: async () => null }
    expect(await loadBand(source)).toBeNull()
    const none = FIXTURES['no-roadmap']
    expect(await loadBand({ ...memorySource(none.files, none.cwd), read: async () => null })).toEqual({ rows: [], workable: [] })
  })

  test('an archive directory that cannot be listed marks nothing done', async () => {
    const fixture = FIXTURES['idle-deps']
    const source = { ...memorySource(fixture.files, fixture.cwd), list: async () => null }
    const ids = (await loadBand(source)).workable.map(row => row.id)
    expect(ids).not.toContain('M040')
    expect(ids).toContain('M041')
  })

  test('dirname stops at the root', () => {
    expect(dirname('/a/b')).toBe('/a')
    expect(dirname('/a')).toBe('/')
    expect(dirname('/')).toBe('/')
    expect(dirname('C:\\a')).toBe('C:\\')
  })
})
