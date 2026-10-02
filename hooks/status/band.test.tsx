import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { bandLines, knownStep, lineText, SKILL_LABELS } from './band'
import { FIXTURES, SKILLS } from './fixtures.gen'

// Each case answers the shipped mod's `$.session.cwd`, `$.fs.stat` and
// `$.fs.read` calls from an in-memory copy of a fixture, keyed by absolute
// path. A plain answer goes back as `{ value }`; a path the copy lacks goes
// on to the bottom of the chain, which rejects, as a missing file does in a
// session. The copy is mutable: an edit case edits a file between two turn
// ends, and the second turn end reads the edit.

const SURFACES = ['terminal', 'desktop'] as const
const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
} as const
let turnCount = 0
function turn() {
  turnCount += 1
  return { answer: '', durationMs: 1, isAborted: false, turnId: `t${turnCount}`, reason: 'answer' as const }
}

function at(bodyColumns: number) {
  return { ...BAND, props: { ...BAND.props, bodyColumns } }
}

type Copy = { cwd: string; files: Record<string, string> }

function copyOf(name: string): Copy {
  const fixture = FIXTURES[name]
  return { cwd: fixture.cwd, files: { ...fixture.files } }
}

// How the chapter tool beneath the mod answers a call: it marks the
// chapter, refuses the call, or marks nothing and errs.
type ChapterAnswer = 'mark' | 'deny' | 'error'

// The world beneath the mod: the fixture copy as the session's directory and
// files, a turn end that answers nothing, a skill prompt passed through, the
// chapter tool, and a session end.
function seat(on: On, copy: Copy, chapter: ChapterAnswer = 'mark') {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) => (has(e.path) ? { value: copy.files[e.path] } : next(e)))
  on('turn.complete', async () => ({ text: '' }))
  on('skill.prompt', async ($, e) => ({ text: e.text }))
  on('tool.call', { tool: CHAPTER_TOOL }, async () =>
    chapter === 'deny'
      ? { deny: 'refused beneath' }
      : chapter === 'error'
        ? { result: 'failed beneath', isError: true }
        : { result: 'Chapter marked' },
  )
  on('session.end', async ($, e) => ({ sessionId: e.sessionId }))
  // The engine's own drawing of the band slot, which the mod draws its rows
  // above, or passes to when it has nothing to show.
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: [ENGINE] }))
}

const ENGINE = 'engine slot'
const CHAPTER_TOOL = 'mcp__ccd_session__mark_chapter'

// A skill prompt, as the engine expands one.
async function prompt($, skill: string) {
  await $.skill.prompt({ skill, text: `the ${skill} prompt` })
}

// A chapter the main loop marks.
async function chapter($, title: string) {
  await $.tool.call({ tool: CHAPTER_TOOL, title })
}

// A plugin beneath the mod that draws its own band row and never calls
// `next`. Its register closes over nothing here, so its row text is
// written inside it and restated as BENEATH_ROW.
const BENEATH = {
  name: 'band-beneath',
  tier: 'append' as const,
  register: on => {
    on('ui.render', { component: 'AbovePrompt' }, async ($, e) => {
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box key="beneath-band">
          <Text>another plugin's band row</Text>
        </Box>
      )
    })
  },
}
const BENEATH_ROW = "another plugin's band row"

// An element as `findAll` returns it, or as it sits in a found element's
// `children`, where its key is in its props.
type Element = { type: string; key?: string; text?: string; props: Record<string, unknown>; children: unknown[] }
type Ui = {
  findAll: (q: { type?: string; key?: string }) => Promise<Element[]>
  press: (q: { key: string }) => Promise<unknown>
  unmount: () => Promise<void>
}

// The text an element shows, its nested Text children included. The close
// Button's label is left out, so a row reads the same on every surface.
function textOf(node: unknown): string {
  if (typeof node === 'string') return node
  if (node === null || typeof node !== 'object') return ''
  if ((node as Element).type === 'Button') return ''
  return ((node as Element).children ?? []).map(textOf).join('')
}

function keyOf(node: Element): string | undefined {
  return node.key ?? (node.props?.key as string | undefined)
}

// The element children of a node, strings left out.
function kids(node: Element): Element[] {
  return (node.children ?? []).filter((c): c is Element => c !== null && typeof c === 'object')
}

// Every element below `node` of the given type, at any depth.
function below(node: unknown, type: string): Element[] {
  if (node === null || typeof node !== 'object') return []
  const el = node as Element
  const rest = (el.children ?? []).flatMap(child => below(child, type))
  return el.type === type ? [el, ...rest] : rest
}

const ROW_KEY = /^(M\d+|skill)-row$/

// A row's text with its two groups joined by the right group's left margin,
// the least gap a row draws (a wide row spreads them further), with the
// close button's label and the spaces before it left out.
function rowText(row: Element): string {
  const groups = kids(row)
  if (row.props.justifyContent !== 'space-between' || groups.length !== 2) return textOf(row)
  const [left, right] = groups
  return `${textOf(left)}${' '.repeat(Number(right.props.marginLeft ?? 0))}${textOf(right)}`.trimEnd()
}

// The rows as drawn, top to bottom: each of cairn's rows (a keyed Box), then
// the rows the hooks beneath drew (ENGINE, BENEATH_ROW).
async function lines(ui: Ui): Promise<string[]> {
  const all = await ui.findAll({})
  return all
    .filter(el => (el.type === 'Box' && ROW_KEY.test(el.key ?? '')) || (el.type === 'Text' && [ENGINE, BENEATH_ROW].includes(textOf(el))))
    .map(el => (el.type === 'Box' ? rowText(el) : textOf(el)))
}

// The `cairn-band` Box as found.
async function bandBox(ui: Ui): Promise<Element> {
  const [box] = await ui.findAll({ key: 'cairn-band' })
  expect(box?.type).toBe('Box')
  return box
}

// The Texts inside the `cairn-band` Box.
async function bandTexts(ui: Ui): Promise<Element[]> {
  return below(await bandBox(ui), 'Text')
}

// The keys of the row Boxes inside the `cairn-band` Box.
async function rowKeys(ui: Ui): Promise<string[]> {
  return below(await bandBox(ui), 'Box')
    .map(keyOf)
    .filter((k): k is string => ROW_KEY.test(k ?? ''))
}

// Whether the drawing holds any of cairn's elements.
async function hasCairn(ui: Ui): Promise<boolean> {
  const all = await ui.findAll({})
  return all.some(el => ROW_KEY.test(el.key ?? '') || /^cairn-/.test(el.key ?? ''))
}

async function mountEach(name: string, view: typeof BAND, check: (ui: Ui, surface: string) => Promise<void>, $) {
  for (const surface of SURFACES) {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...view })) as Ui
    await check(ui, surface)
    await ui.unmount()
  }
}

// Each active row at 120 columns, drawn as the only active row, written out
// by hand, never derived from band.ts. The two spaces before a bar, a
// count, or a state label are the right group's left margin. A row's text
// shows every bar cell as `█`; the dim empty cells are asserted on the
// drawn Texts.
const DRAWN: Record<string, string[]> = {
  'single-in-progress': ['implement M002 → T2: Write the command.  ██████████  1/3 tasks'],
  mixed: [
    'review M010 → AC3: Third criterion.  ██████████  2/3 criteria',
    'implement M012 A Tasks section with no boxes  no tasks',
    'review M013 Capitalized status, file gone  no milestone file',
    'implement M014 No Tasks section at all  no tasks',
  ],
  'nested-first': ['implement M030 → T1a: Nested task, open, with extra spaces after the box.  ██████████  1/3 tasks'],
  'states-implement': [
    'implement M040 Its file was never written  no milestone file',
    'implement M041 No Tasks section  no tasks',
    'implement M042 A Tasks section with no boxes  no tasks',
    'implement M043 Every task checked  all 3 tasks checked',
  ],
  'states-review': [
    'review M050 Its file was never written  no milestone file',
    'review M051 No criteria section  no criteria',
    'review M052 A criteria section with no boxes  no criteria',
    'review M053 Every criterion checked  all 2 criteria checked',
  ],
  'missing-file': ['review M004 Its file was never written  no milestone file'],
  subdirectory: ['implement M007 Started from a subdirectory  all 2 tasks checked'],
  'unlabeled-item': ['implement M062 → Write the docs, with no label.  ██████████  1/3 tasks'],
}

// Each skill's label, written out by hand, never read from band.ts.
const LABELS: Record<string, string> = {
  'cairn-init': 'init',
  'cairn-release': 'release',
  'cairn-triage': 'triage',
  'design-interview': 'design',
  hotfix: 'hotfix',
  milestone: 'status',
  'milestone-brief': 'brief',
  'milestone-implement': 'implement',
  'milestone-plan': 'plan',
  'milestone-review': 'review',
}

// A skill row's text at 120 columns: the label and one space, then the
// slash command, then the chapter when one is set.
const skillRow = (skill: string, title?: string) => `${LABELS[skill]} /${skill}${title === undefined ? '' : ` → ${title}`}`

// The one row each fixture draws at 120 columns with no skill running,
// written out by hand: its first `in-progress` row, else its first
// `review` row.
const SHOWN: Record<string, string> = {
  'single-in-progress': DRAWN['single-in-progress'][0],
  mixed: 'implement M012 A Tasks section with no boxes  no tasks',
  'nested-first': DRAWN['nested-first'][0],
  'states-implement': 'implement M040 Its file was never written  no milestone file',
  'states-review': 'review M050 Its file was never written  no milestone file',
  'missing-file': DRAWN['missing-file'][0],
  subdirectory: DRAWN.subdirectory[0],
  'unlabeled-item': DRAWN['unlabeled-item'][0],
}

// The id of the row the band shows on a fixture, read from the fixture's
// rows by AC5's rule: the first `review` row while /milestone-review runs
// and one exists, else the first `in-progress` row, else the first
// `review` row; null when no row is active.
function shownId(name: string, skill: string | null = null): string | null {
  const rows = FIXTURES[name].rows
  const first = (status: string) => rows.find(row => row.status === status)?.id
  return (skill === 'milestone-review' ? first('review') : undefined) ?? first('in-progress') ?? first('review') ?? null
}

// A copy of a fixture in which `id` is the only active row: every other
// `in-progress` or `review` row in its ROADMAP is set to `done`.
function alone(name: string, id: string): Copy {
  const copy = copyOf(name)
  for (const path of Object.keys(copy.files)) {
    if (!path.endsWith('cairn/ROADMAP.md')) continue
    copy.files[path] = copy.files[path]
      .split('\n')
      .map(line => {
        const cells = line.split('|')
        if (cells.length < 8 || !cells[1].trim().startsWith('M') || cells[1].trim() === id) return line
        if (!['in-progress', 'review'].includes(cells[3].trim().toLowerCase())) return line
        cells[3] = ' done '
        return cells.join('|')
      })
      .join('\n')
  }
  return copy
}

// The row's right group ends in the close button, the band's only Button.
async function closesFirst(ui: Ui) {
  const [first] = await ui.findAll({ key: (await rowKeys(ui))[0] })
  const right = kids(first)[1]
  const last = kids(right)[kids(right).length - 1]
  expect(last.type).toBe('Button')
  expect(keyOf(last)).toBe('cairn-close')
  expect((await ui.findAll({ type: 'Button' })).length).toBe(1)
}

// The text of a row's first head Text: its phase or skill label.
function labelOf(row: Element): string {
  return textOf(kids(layout(row).head)[0])
}

describe('one row while the band shows (M197 AC5)', () => {
  const names = Object.keys(FIXTURES)
  test('the fixture list holds the fixtures the row tests need', () => {
    expect(names.length).toBeGreaterThan(10)
    for (const name of ['mixed', 'no-active', 'no-roadmap', 'single-in-progress', 'states-review', 'six-active']) {
      expect(names).toContain(name)
    }
  })

  test('shownId follows the rule on the hand-checked fixtures', () => {
    expect(shownId('mixed')).toBe('M012')
    expect(shownId('mixed', 'milestone-review')).toBe('M010')
    expect(shownId('states-review', 'milestone-implement')).toBe('M050')
    expect(shownId('six-active')).toBe('M070')
    expect(shownId('six-active', 'milestone-review')).toBe('M071')
    expect(shownId('no-active')).toBeNull()
  })

  for (const name of names) {
    test(`${name}: with no skill running, one row on a fixture with an active row, else none`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const id = shownId(name)
      await mountEach(
        name,
        BAND,
        async ui => {
          if (id === null) {
            expect(await hasCairn(ui)).toBe(false)
            return
          }
          expect(await rowKeys(ui)).toEqual([`${id}-row`])
          await closesFirst(ui)
        },
        $,
      )
    })

    for (const skill of SKILLS) {
      test(`${name}: with ${skill} running, one row under its label`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        await prompt($, skill)
        const id = shownId(name, skill)
        await mountEach(
          name,
          BAND,
          async ui => {
            expect(await rowKeys(ui)).toEqual([id === null ? 'skill-row' : `${id}-row`])
            const [row] = await ui.findAll({ key: (await rowKeys(ui))[0] })
            expect(labelOf(row)).toBe(LABELS[skill])
            await closesFirst(ui)
          },
          $,
        )
      })
    }
  }

  // Rows and label colors written out by hand.
  for (const [name, skill, key, label, color] of [
    ['mixed', null, 'M012-row', 'implement', 'claude'],
    ['mixed', 'milestone-review', 'M010-row', 'review', 'success'],
    ['states-review', 'milestone-implement', 'M050-row', 'implement', 'claude'],
    ['states-review', 'milestone', 'M050-row', 'status', 'claude'],
    ['single-in-progress', 'milestone-review', 'M002-row', 'review', 'success'],
  ] as const) {
    test(`${name} with ${skill ?? 'no skill'}: ${key} under ${label} in ${color}`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      if (skill !== null) await prompt($, skill)
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await rowKeys(ui)).toEqual([key])
          const [row] = await ui.findAll({ key })
          expect(labelOf(row)).toBe(label)
          expect(kids(layout(row).head)[0].props.color).toBe(color)
        },
        $,
      )
    })
  }

  for (const name of ['single-in-progress', 'mixed', 'nested-first']) {
    test(`${name}: the row above the engine's drawing`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([SHOWN[name], ENGINE])
          expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
        },
        $,
      )
    })
  }

  test('the hand-written rows match what band.ts builds', () => {
    for (const [name, drawn] of Object.entries(DRAWN)) {
      expect(FIXTURES[name].rows.flatMap(row => bandLines(row, 120)).map(lineText)).toEqual(drawn)
    }
  })

  test('the band yields to a survey', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND, props: { ...BAND.props, hasSurvey: true } })) as Ui
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

const ROW = (name: string, id: string) => FIXTURES[name].rows.find(row => row.id === id)!

describe("a row's one text: the chapter, else the next open item, else the title (M196 AC2)", () => {
  test('implement: the chapter on the carrying row', () => {
    expect(bandLines(ROW('single-in-progress', 'M002'), 120, 'T3: Write the docs.').map(lineText)).toEqual([
      'implement M002 → T3: Write the docs.  ██████████  1/3 tasks',
    ])
  })

  test('review: the chapter on the carrying row', () => {
    expect(bandLines(ROW('mixed', 'M010'), 120, 'AC1: First criterion.').map(lineText)).toEqual([
      'review M010 → AC1: First criterion.  ██████████  2/3 criteria',
    ])
  })

  test('implement: the next open task with no chapter', () => {
    expect(bandLines(ROW('single-in-progress', 'M002'), 120).map(lineText)).toEqual([DRAWN['single-in-progress'][0]])
  })

  test('review: the next open criterion with no chapter', () => {
    expect(bandLines(ROW('mixed', 'M010'), 120).map(lineText)).toEqual([DRAWN.mixed[0]])
  })

  test('implement: the title with no chapter and no open task', () => {
    expect(bandLines(ROW('states-implement', 'M043'), 120).map(lineText)).toEqual(['implement M043 Every task checked  all 3 tasks checked'])
  })

  test('review: the title with no chapter and no open criterion', () => {
    expect(bandLines(ROW('states-review', 'M053'), 120).map(lineText)).toEqual(['review M053 Every criterion checked  all 2 criteria checked'])
  })

  for (const surface of SURFACES) {
    test(`a skill row with no chapter, then with one (${surface})`, async ($, on) => {
      seat(on, copyOf('no-active'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-plan')
      expect(await lines(ui)).toEqual(['plan /milestone-plan', ENGINE])
      await chapter($, 'Question gate')
      expect(await lines(ui)).toEqual(['plan /milestone-plan → Question gate', ENGINE])
      await ui.unmount()
    })
  }
})

describe('the right group shows the bar only in the task or criterion loop (M196 AC3)', () => {
  const m002 = ROW('single-in-progress', 'M002')
  test('a labeled chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, 'T3: Write the docs.').map(lineText)).toEqual(['implement M002 → T3: Write the docs.  ██████████  1/3 tasks'])
  })

  test('a nested labeled chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, 'T2a: A sub-task.').map(lineText)).toEqual(['implement M002 → T2a: A sub-task.  ██████████  1/3 tasks'])
  })

  test('an unlabeled chapter shows the counts alone', () => {
    expect(bandLines(m002, 120, 'Question gate').map(lineText)).toEqual(['implement M002 → Question gate  1/3 tasks'])
  })

  test('no chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, null).map(lineText)).toEqual([DRAWN['single-in-progress'][0]])
  })

  test('a chapter on a state-label row keeps the label', () => {
    expect(bandLines(ROW('mixed', 'M013'), 120, 'AC1: A criterion.').map(lineText)).toEqual(['review M013 → AC1: A criterion.  no milestone file'])
    expect(bandLines(ROW('mixed', 'M012'), 120, 'Question gate').map(lineText)).toEqual(['implement M012 → Question gate  no tasks'])
    expect(bandLines(ROW('states-review', 'M053'), 120, 'Consistency gate').map(lineText)).toEqual([
      'review M053 → Consistency gate  all 2 criteria checked',
    ])
  })
})

describe('three states draw the title and the label (M193 AC2)', () => {
  for (const name of ['states-implement', 'states-review', 'missing-file', 'subdirectory']) {
    for (const [i, fixtureRow] of FIXTURES[name].rows.entries()) {
      test(`${name}: ${fixtureRow.id} alone, with no bar`, async ($, on) => {
        seat(on, alone(name, fixtureRow.id))
        await $.turn.complete(turn())
        await mountEach(
          name,
          BAND,
          async ui => {
            expect(await lines(ui)).toEqual([DRAWN[name][i], ENGINE])
            expect(await rowKeys(ui)).toEqual([`${fixtureRow.id}-row`])
            expect((await bandTexts(ui)).filter(t => /█/.test(textOf(t)))).toEqual([])
            expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
          },
          $,
        )
      })
    }
  }
})

// A Text that holds only strings: one span of a row.
function leafIn(texts: Element[], text: string): Element | undefined {
  return texts.find(t => t.children.every(c => typeof c === 'string') && textOf(t) === text)
}

describe('the rows carry style props (M193 AC3)', () => {
  for (const [id, label, color] of [
    ['M012', 'implement', 'claude'],
    ['M013', 'no milestone file', 'warning'],
  ] as const) {
    test(`mixed: ${id} alone draws ${label} in ${color}`, async ($, on) => {
      seat(on, alone('mixed', id))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        BAND,
        async ui => {
          const inBand = await bandTexts(ui)
          expect(leafIn(inBand, label)?.props.color).toBe(color)
          expect(leafIn(inBand, id)?.props.bold).toBe(true)
        },
        $,
      )
    })
  }

  // M010's head `review M010 → AC3:` is 18 columns, its text gets 10, the
  // margin 2, the bar form 24, and the close gap and label 3: 57 columns
  // keep its bar, and 56 drop it.
  for (const columns of [56, 57, 120]) {
    test(`mixed: M010 alone at ${columns} columns`, async ($, on) => {
      seat(on, alone('mixed', 'M010'))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        at(columns),
        async ui => {
          const inBand = await bandTexts(ui)
          const leaf = (text: string) => leafIn(inBand, text)
          expect(leaf('review')?.props.color).toBe('success')
          expect(leaf('M010')?.props.bold).toBe(true)
          expect(inBand.length).toBeGreaterThan(5)
          expect(inBand.filter(t => t.props.wrap !== 'truncate-end')).toEqual([])

          const [row] = await ui.findAll({ key: 'M010-row' })
          expect(rowText(row).endsWith('  2/3 criteria')).toBe(true)
          const filled = leaf('██████')
          if (columns < 57) {
            expect(filled).toBeUndefined()
            expect(rowText(row)).toBe('review M010 → AC3: Third criterion.  2/3 criteria')
          } else {
            expect(filled?.props.color).toBe('success')
            expect(filled?.props.dimColor).toBeUndefined()
            expect(leaf('████')?.props.dimColor).toBe(true)
            expect(rowText(row)).toBe(DRAWN.mixed[0])
          }
        },
        $,
      )
    })
  }
})

// One row's layout: the row, its two groups, the head Box that keeps its
// width, and the text Box that gives way, with its Text.
function layout(row: Element) {
  const groups = kids(row)
  const [left, right] = groups
  const [head, textBox] = kids(left)
  return { groups, left, right, head, textBox, text: textBox ? kids(textBox)[0] : undefined }
}

// What gives way in a row: the left group and the text's Box shrink to any
// width, and the head (phase, id, arrow, and label) keeps its width. The
// desktop app drew a long text whose Box lacked `minWidth: 0` past the edge,
// and shrank the short Texts beside it to nothing.
function shrinks(row: Element) {
  const { left, head, textBox } = layout(row)
  expect(left.props.flexShrink).toBe(1)
  expect(left.props.minWidth).toBe(0)
  expect(head.type).toBe('Box')
  expect(head.props.flexShrink).toBe(0)
  expect(textBox.type).toBe('Box')
  expect(textBox.props.flexShrink).toBe(1)
  expect(textBox.props.minWidth).toBe(0)
}

const CLOSE = { terminal: '×', desktop: '×' } as const
// The terminal draws the close button plain, its label alone. The desktop
// draws its own close control.
const PLAIN = { terminal: true, desktop: undefined } as const

// The left group of each mixed row, written out by hand.
const MIXED_LEFT: Record<string, string> = {
  M010: 'review M010 → AC3: Third criterion.',
  M012: 'implement M012 A Tasks section with no boxes',
  M013: 'review M013 Capitalized status, file gone',
  M014: 'implement M014 No Tasks section at all',
}

describe('each row is a left and a right group (M194 AC1)', () => {
  for (const columns of [56, 57, 120]) {
    for (const row of FIXTURES.mixed.rows) {
      test(`mixed: ${row.id} alone at ${columns} columns`, async ($, on) => {
        seat(on, alone('mixed', row.id))
        await $.turn.complete(turn())
        await mountEach(
          'mixed',
          at(columns),
          async ui => {
            const [drawn] = await ui.findAll({ key: `${row.id}-row` })
            expect(drawn.props.justifyContent).toBe('space-between')
            const { groups, left, right } = layout(drawn)
            expect(groups.map(g => g.type)).toEqual(['Box', 'Box'])
            expect(drawn.children.length).toBe(2)
            expect(right.props.flexShrink).toBe(0)
            expect(right.props.marginLeft).toBe(2)
            expect(textOf(left)).toBe(MIXED_LEFT[row.id])
            shrinks(drawn)
            // The right group: the bar at 57 columns or more, and the counts
            // or the state label, then the close button.
            const hasBar = below(right, 'Text').some(t => /█/.test(textOf(t)))
            expect(hasBar).toBe(row.id === 'M010' && columns >= 57)
            const last = kids(right)[kids(right).length - 1]
            expect(last.type).toBe('Button')
            expect(keyOf(last)).toBe('cairn-close')
            if (row.id === 'M013') expect(textOf(right).trim()).toBe('no milestone file')
          },
          $,
        )
      })
    }
  }

  // A long chapter, labeled on long-title and unlabeled on wide-title,
  // reaches the text's Text whole after its label; the engine cuts it. At
  // 40 columns neither row has room for the counts' noun.
  const LONG: [string, string, string, string, string][] = [
    ['long-title', 'milestone-implement', 'T2: ', '1/2', 'T2:'],
    ['wide-title', 'milestone-review', '', '1/2', ''],
  ]
  for (const [name, skill, prefix, counts, label] of LONG) {
    test(`${name} at 40 columns: the text's Text holds the long chapter's whole text after its label`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const [row] = FIXTURES[name].rows
      await prompt($, skill)
      await chapter($, `${prefix}${row.title}`)
      await mountEach(
        name,
        at(40),
        async ui => {
          const [drawn] = await ui.findAll({ key: `${row.id}-row` })
          expect(drawn.props.justifyContent).toBe('space-between')
          const { right, head, text } = layout(drawn)
          expect(right.props.flexShrink).toBe(0)
          expect(right.props.marginLeft).toBe(2)
          expect(textOf(head).endsWith(`→ ${label}`)).toBe(true)
          expect(text?.children).toEqual([label === '' ? row.title : ` ${row.title}`])
          expect(text?.props.wrap).toBe('truncate-end')
          shrinks(drawn)
          expect(below(right, 'Text').some(t => /█/.test(textOf(t)))).toBe(false)
          expect(textOf(right).trim()).toBe(counts)
          expect(keyOf(kids(right)[kids(right).length - 1])).toBe('cairn-close')
        },
        $,
      )
    })
  }

  test("the wide-title fixture's title holds wide characters and an emoji", () => {
    const [row] = FIXTURES['wide-title'].rows
    expect(row.title).toContain('🚀')
    expect(row.title).toContain('宽字符')
  })
})

// A press hides the band until the active list changes, and that state
// lasts the session, so each surface gets a session of its own.
describe('the close button (M194 AC2)', () => {
  for (const name of ['mixed', 'single-in-progress']) {
    for (const surface of SURFACES) {
      test(`${name}: one dismiss Button, and a press passes to the engine (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await lines(ui)).toEqual([SHOWN[name], ENGINE])
        const buttons = await ui.findAll({ type: 'Button' })
        expect(buttons.map(keyOf)).toEqual(['cairn-close'])
        const [button] = buttons
        expect(button.props.role).toBe('dismiss')
        expect(button.props.plain).toBe(PLAIN[surface])
        expect(button.props.label).toBe(CLOSE[surface])
        // The Button is the last child of the row's right group.
        const [first] = await ui.findAll({ key: `${shownId(name)}-row` })
        const { right } = layout(first)
        expect(keyOf(kids(right)[kids(right).length - 1])).toBe('cairn-close')
        expect(kids(right)[kids(right).length - 1].type).toBe('Button')
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        expect(await hasCairn(ui)).toBe(false)
        expect(await ui.findAll({ type: 'Button' })).toEqual([])
        await ui.unmount()
      })
    }
  }

  for (const surface of SURFACES) {
    test(`mixed over a plugin beneath: a press leaves the row the plugin beneath draws (${surface})`, { plugins: [BENEATH] }, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await lines(ui)).toEqual([SHOWN.mixed, BENEATH_ROW])
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([BENEATH_ROW])
      expect(await hasCairn(ui)).toBe(false)
      await ui.unmount()
    })
  }
})

// A row's Texts, each with the Texts that enclose it.
function textsIn(node: unknown, outer: Element[] = []): { text: Element; outer: Element[] }[] {
  if (node === null || typeof node !== 'object') return []
  const el = node as Element
  const inner = el.type === 'Text' ? [...outer, el] : outer
  const rest = (el.children ?? []).flatMap(child => textsIn(child, inner))
  return el.type === 'Text' ? [{ text: el, outer }, ...rest] : rest
}

const LABELED: [string, string, string][] = [
  ['mixed', 'M010-row', 'AC3:'],
  ['single-in-progress', 'M002-row', 'T2:'],
  ['nested-first', 'M030-row', 'T1a:'],
]

describe("the step's label draws bold, and its arrow dim (M196 AC2)", () => {
  for (const [name, key, label] of LABELED) {
    test(`${name}: ${label} is bold and undimmed, and the rest is plain`, async ($, on) => {
      seat(on, alone(name, key.replace(/-row$/, '')))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          const [row] = await ui.findAll({ key })
          const { head, text } = layout(row)
          const texts = textsIn(head)
          const found = texts.filter(t => t.text.children.length === 1 && t.text.children[0] === label)
          expect(found.length).toBe(1)
          const [{ text: labelText, outer }] = found
          expect(labelText.props.bold).toBe(true)
          expect([labelText, ...outer].filter(t => t.props.dimColor)).toEqual([])
          const arrows = texts.filter(t => textOf(t.text) === '→ ')
          expect(arrows.length).toBe(1)
          expect(arrows[0].text.props.dimColor).toBe(true)
          expect(textOf(head).endsWith(`→ ${label}`)).toBe(true)
          expect(text?.props.dimColor).toBeUndefined()
          expect(text?.props.bold).toBeUndefined()
          shrinks(row)
        },
        $,
      )
    })
  }

  test('unlabeled-item: no bold Text after the id', async ($, on) => {
    seat(on, copyOf('unlabeled-item'))
    await $.turn.complete(turn())
    await mountEach(
      'unlabeled-item',
      BAND,
      async ui => {
        expect(await lines(ui)).toEqual([...DRAWN['unlabeled-item'], ENGINE])
        const [row] = await ui.findAll({ key: 'M062-row' })
        const { head, text } = layout(row)
        expect(textsIn(head).filter(t => t.text.props.bold).map(t => textOf(t.text))).toEqual(['M062'])
        expect(textOf(head).endsWith('→ ')).toBe(true)
        expect(text?.children).toEqual(['Write the docs, with no label.'])
        expect(text?.props.bold).toBeUndefined()
        shrinks(row)
      },
      $,
    )
  })
})

// Each edit case asserts the band at a first turn end, edits the copy, ends
// a second turn, and asserts again.
type Edit = { name: string; fixture: string; edit: (files: Record<string, string>) => void; before: string[]; after: string[] }

const ROADMAP = '/cairn/ROADMAP.md'
const M002 = '/cairn/milestones/M002-export.md'
const M030 = '/cairn/milestones/M030-nested.md'
const EDITS: Edit[] = [
  {
    name: 'a task gets checked',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: ['implement M002 → T3: Write the docs.  ██████████  2/3 tasks', ENGINE],
  },
  {
    name: 'a row moves from planned to in-progress',
    fixture: 'no-active',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
    },
    before: [ENGINE],
    after: ['implement M021 → T1: Not started.  ██████████  0/1 tasks', ENGINE],
  },
  {
    name: 'a row moves from in-progress to review, and switches to criteria',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: ['review M002 → AC1: The export command writes one file per table.  ██████████  0/1 criteria', ENGINE],
  },
  {
    name: 'a row leaves both statuses from review',
    fixture: 'missing-file',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Its file was never written | review |', '| Its file was never written | done |')
    },
    before: ['review M004 Its file was never written  no milestone file', ENGINE],
    after: [ENGINE],
  },
  {
    name: 'a row leaves both statuses',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | done |')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: [ENGINE],
  },
  {
    name: 'a check on the nested task grows the bar and names the next task',
    fixture: 'nested-first',
    edit: files => {
      files[M030] = files[M030].replace('- [ ]   T1a:', '- [x]   T1a:')
    },
    before: [DRAWN['nested-first'][0], ENGINE],
    after: ['implement M030 → T2: Second top-level task.  ██████████  2/3 tasks', ENGINE],
  },
]

describe('the band follows edits at the next turn end (M193 AC4)', () => {
  for (const { name, fixture, edit, before, after } of EDITS) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(fixture)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await lines(ui)).toEqual(before)
        edit(copy.files)
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual(after)
        await ui.unmount()
      })
    }
  }
})

// Each close case presses the close button, ends a turn with nothing
// changed, edits the copy, ends another turn, and asserts whether the band
// shows, by the keys of the rows it draws.
type Close = { name: string; fixture: string; edit: (files: Record<string, string>) => void; shown: string[] | null }

const ADDED = (status: string) => `| M005 | Added later | ${status} | — | normal | milestones/M005-added.md |\n`
const CLOSES: Close[] = [
  {
    name: 'a checked task box keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    shown: null,
  },
  {
    name: 'an added planned row keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| M001 | First release |', `${ADDED('planned')}| M001 | First release |`)
    },
    shown: null,
  },
  {
    name: 'an edited title keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command |', '| Add the export commands |')
    },
    shown: null,
  },
  {
    name: 'a row moved from in-progress to review shows it',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    shown: ['M002-row'],
  },
  {
    name: 'an added active row shows it',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| M001 | First release |', `${ADDED('in-progress')}| M001 | First release |`)
    },
    shown: ['M002-row'],
  },
  {
    name: 'a removed active row shows it',
    fixture: 'mixed',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| A Tasks section with no boxes | in-progress |', '| A Tasks section with no boxes | done |')
    },
    shown: ['M014-row'],
  },
  {
    name: 'two active rows that swap ROADMAP order show it',
    fixture: 'mixed',
    edit: files => {
      const lines = files[ROADMAP].split('\n')
      const a = lines.findIndex(l => l.startsWith('| M010 |'))
      const b = lines.findIndex(l => l.startsWith('| M012 |'))
      ;[lines[a], lines[b]] = [lines[b], lines[a]]
      files[ROADMAP] = lines.join('\n')
    },
    shown: ['M012-row'],
  },
]

describe('a press hides the band until the active ids, statuses, or order change (M194 AC3)', () => {
  for (const { name, fixture, edit, shown } of CLOSES) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(fixture)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        // A turn end with nothing changed keeps it hidden.
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual([ENGINE])
        const unedited = JSON.stringify(copy.files)
        edit(copy.files)
        expect(JSON.stringify(copy.files)).not.toBe(unedited)
        await $.turn.complete(turn())
        if (shown === null) {
          expect(await lines(ui)).toEqual([ENGINE])
          expect(await hasCairn(ui)).toBe(false)
        } else {
          expect(await rowKeys(ui)).toEqual(shown)
        }
        await ui.unmount()
      })
    }
  }

  for (const surface of SURFACES) {
    test(`a move to review shows it, and a move back keeps it shown (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      const original = copy.files[ROADMAP]
      copy.files[ROADMAP] = original.replace('| Add the export command | in-progress |', '| Add the export command | review |')
      await $.turn.complete(turn())
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      copy.files[ROADMAP] = original
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      // The band stays shown until the next press.
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await ui.unmount()
    })
  }
})

// A plugin above the mod that draws how the mod's render hook settled, read
// from `next.trace`: `returned` when it settled on a result, here the
// engine's drawing it handed on to, and `skipped` when it threw. A thrown
// hook is skipped and the engine draws, so the drawing alone cannot tell
// the two apart.
const PROBE = {
  name: 'band-probe',
  tier: 'prepend' as const,
  register: on => {
    on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
      const drawn = await next(e)
      const link = next.trace.find(t => t.plugin === 'cairn')
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box key="band-probe" flexDirection="column">
          <Text>{`cairn hook: ${link ? link.outcome : 'absent'}`}</Text>
          {drawn}
        </Box>
      )
    })
  },
}

describe('the band draws nothing', () => {
  for (const name of ['no-roadmap', 'no-active']) {
    test(`${name}: the mod draws nothing, passes to the engine, and does not throw`, { plugins: [PROBE] }, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      for (const surface of SURFACES) {
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        const shown = (await ui.findAll({ type: 'Text' })).map(textOf)
        expect(shown).toEqual(['cairn hook: returned', ENGINE])
        await ui.unmount()
      }
    })
  }

  test('a cairn repo with a ROADMAP below the working directory only draws nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    // The ROADMAP sits one level below the working directory, where the
    // upward walk never looks.
    seat(on, { cwd: '/', files: Object.fromEntries(Object.entries(copy.files).map(([k, v]) => [`/below${k}`, v])) })
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

describe("cairn's rows sit above the band beneath (M193 AC6)", () => {
  test('single-in-progress over a plugin beneath', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    await mountEach(
      'single-in-progress',
      BAND,
      async ui => {
        expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], BENEATH_ROW])
        expect((await bandTexts(ui)).map(textOf)).not.toContain(BENEATH_ROW)
      },
      $,
    )
  })

  test('with nothing active, the band beneath shows alone', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('no-active'))
    await $.turn.complete(turn())
    await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([BENEATH_ROW]), $)
  })
})

// M195: the running cairn skill and the session's chapters.

const M010 = '/cairn/milestones/M010-nested.md'
// The row mixed draws while /milestone-review runs with no chapter.
const MIXED_REVIEW = DRAWN.mixed[0]
// single-in-progress's row under the label `plan`, with no chapter.
const PLAN_M002 = 'plan M002 → T2: Write the command.  ██████████  1/3 tasks'

// Mounts the band on each surface, runs `act` against it, and checks it.
async function eachSurface(name: string, chapterAnswer: ChapterAnswer, act: (ui: Ui, $, copy: Copy) => Promise<void>, $, on) {
  const copy = copyOf(name)
  seat(on, copy, chapterAnswer)
  await $.turn.complete(turn())
  for (const surface of SURFACES) {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
    await act(ui, $, copy)
    await ui.unmount()
  }
}

describe('the label map covers the skill directories (M195 AC1)', () => {
  test('the skill list is not empty, and the map has a label for each skill and no other', () => {
    expect(SKILLS.length).toBe(10)
    expect(Object.keys(SKILL_LABELS).sort()).toEqual([...SKILLS].sort())
    expect(Object.keys(LABELS).sort()).toEqual([...SKILLS].sort())
  })
})

describe('the row that carries a running cairn skill shows its label (M195 AC1)', () => {
  for (const skill of SKILLS) {
    for (const spelling of [skill, `cairn:${skill}`]) {
      test(`${spelling} over no-active`, async ($, on) => {
        const copy = copyOf('no-active')
        seat(on, copy)
        await $.turn.complete(turn())
        await prompt($, spelling)
        await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([skillRow(skill), ENGINE]), $)
      })
    }
  }

  for (const other of ['commit', 'other:hotfix', 'cairn:nope']) {
    test(`${other} leaves the band as it was`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      await prompt($, 'milestone-plan')
      const drawn = [PLAN_M002, ENGINE]
      await mountEach('single-in-progress', BAND, async ui => expect(await lines(ui)).toEqual(drawn), $)
      await prompt($, other)
      await mountEach('single-in-progress', BAND, async ui => expect(await lines(ui)).toEqual(drawn), $)
    })
  }
})

describe('a running skill puts its label on the row, or gets a skill row with no active milestone (M197 AC5)', () => {
  const CASES: { skill: string; fixture: string; drawn: string[] }[] = [
    { skill: 'milestone-plan', fixture: 'no-active', drawn: [skillRow('milestone-plan')] },
    { skill: 'milestone-plan', fixture: 'mixed', drawn: ['plan M012 A Tasks section with no boxes  no tasks'] },
    { skill: 'hotfix', fixture: 'mixed', drawn: ['hotfix M012 A Tasks section with no boxes  no tasks'] },
    {
      skill: 'milestone-review',
      fixture: 'single-in-progress',
      drawn: ['review M002 → T2: Write the command.  ██████████  1/3 tasks'],
    },
    // Outside a cairn repo, a running cairn skill draws its row alone.
    { skill: 'cairn-init', fixture: 'no-roadmap', drawn: [skillRow('cairn-init')] },
    { skill: 'milestone-implement', fixture: 'mixed', drawn: [SHOWN.mixed] },
    { skill: 'milestone-review', fixture: 'mixed', drawn: [MIXED_REVIEW] },
  ]
  for (const { skill, fixture, drawn } of CASES) {
    test(`${skill} over ${fixture}`, async ($, on) => {
      seat(on, copyOf(fixture))
      await $.turn.complete(turn())
      await prompt($, skill)
      await mountEach(
        fixture,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([...drawn, ENGINE])
          const [row] = await ui.findAll({ key: 'skill-row' })
          if (drawn[0] === skillRow(skill)) {
            // Nothing on the right side but the close button.
            const [, right] = kids(row)
            expect(textOf(right).trim()).toBe('')
            expect(below(right, 'Button').length).toBe(1)
          } else {
            expect(row).toBeUndefined()
          }
        },
        $,
      )
    })
  }
})

describe('the carrying row follows the session chapters (M195 AC3)', () => {
  test('a review prompt and an unlabeled chapter put the chapter on M010, with the counts alone', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-review')
        await chapter($, 'Post-merge hygiene')
        expect(await lines(ui)).toEqual(['review M010 → Post-merge hygiene  2/3 criteria', ENGINE])
      },
      $,
      on,
    )
  })

  test('an implement prompt and a chapter put the chapter on M012, beside its label', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-implement')
        await chapter($, 'T1: Write it.')
        expect(await lines(ui)).toEqual(['implement M012 → T1: Write it.  no tasks', ENGINE])
      },
      $,
      on,
    )
  })

  for (const surface of SURFACES) {
    test(`a file edited between two chapters draws the new counts with no turn end (${surface})`, async ($, on) => {
      const copy = copyOf('mixed')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-review')
      await chapter($, 'AC3: Third criterion.')
      expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      copy.files[M010] = copy.files[M010].replace('- [ ] AC3:', '- [x] AC3:')
      await chapter($, 'Consistency gate')
      expect(await lines(ui)).toEqual(['review M010 → Consistency gate  all 3 criteria checked', ENGINE])
      await ui.unmount()
    })

    test(`the chapter moves to the next review row, then to the in-progress row under review (${surface})`, async ($, on) => {
      const copy = copyOf('mixed')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-review')
      copy.files[ROADMAP] = copy.files[ROADMAP].replace('| Nested tasks and a capital X | review |', '| Nested tasks and a capital X | done |')
      await chapter($, 'Approval gate')
      expect(await lines(ui)).toEqual(['review M013 → Approval gate  no milestone file', ENGINE])
      copy.files[ROADMAP] = copy.files[ROADMAP].replace('| Capitalized status, file gone | Review |', '| Capitalized status, file gone | done |')
      await chapter($, 'Post-merge hygiene')
      expect(await lines(ui)).toEqual(['review M012 → Post-merge hygiene  no tasks', ENGINE])
      await ui.unmount()
    })
  }

  for (const answer of ['deny', 'error'] as const) {
    test(`a chapter call that ends in a ${answer} beneath leaves the row as it was`, async ($, on) => {
      await eachSurface(
        'mixed',
        answer,
        async (ui, $) => {
          await prompt($, 'milestone-review')
          try {
            await chapter($, 'Post-merge hygiene')
          } catch {
            // A refused call may reject; the drawing is what counts.
          }
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
        },
        $,
        on,
      )
    })
  }

  test("a subagent's chapter call leaves the row as it was", async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-review')
        await $.tool.call({ tool: CHAPTER_TOOL, title: 'Subagent chapter', agentId: 'a1' })
        expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      },
      $,
      on,
    )
  })

  test('an empty chapter title leaves the row as it was', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-review')
        await chapter($, 'Consistency gate')
        await chapter($, '')
        expect(await lines(ui)).toEqual(['review M010 → Consistency gate  2/3 criteria', ENGINE])
      },
      $,
      on,
    )
  })

  test('a chapter with no cairn skill running starts no step', async ($, on) => {
    await eachSurface(
      'no-active',
      'mark',
      async (ui, $) => {
        await chapter($, 'Auth bug fix')
        expect(await lines(ui)).toEqual([ENGINE])
        expect(await hasCairn(ui)).toBe(false)
      },
      $,
      on,
    )
  })

  test('a stored skill with no label reads as no step', () => {
    expect(knownStep({ skill: 'milestone-gone', chapter: 'Old chapter' })).toBeNull()
    expect(knownStep({ skill: 'hotfix', chapter: null })).toEqual({ skill: 'hotfix', chapter: null })
    expect(knownStep(null)).toBeNull()
  })
})

describe('every session end clears the step (M195 AC4)', () => {
  for (const reason of ['clear', 'resume'] as const) {
    test(`a session end with reason ${reason}`, async ($, on) => {
      await eachSurface(
        'single-in-progress',
        'mark',
        async (ui, $) => {
          await prompt($, 'milestone-plan')
          await chapter($, 'Investigation')
          expect(await lines(ui)).toEqual(['plan M002 → Investigation  1/3 tasks', ENGINE])
          await $.session.end({ reason, sessionId: 's1' })
          expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
        },
        $,
        on,
      )
    })
  }

  test('a second milestone-review prompt drops the chapter', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-review')
        await chapter($, 'Post-merge hygiene')
        await prompt($, 'cairn:milestone-review')
        expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      },
      $,
      on,
    )
  })
})

describe('the close button works with skill rows (M195 AC5)', () => {
  test('the close button sits on the skill row', async ($, on) => {
    await eachSurface(
      'no-active',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-plan')
        const [row] = await ui.findAll({ key: 'skill-row' })
        expect(below(row, 'Button').map(keyOf)).toEqual(['cairn-close'])
        expect((await ui.findAll({ type: 'Button' })).length).toBe(1)
      },
      $,
      on,
    )
  })

  for (const surface of SURFACES) {
    test(`after a press, a chapter, a checked task, and the same skill keep it hidden; another skill shows it (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-plan')
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await chapter($, 'Question gate')
      expect(await lines(ui)).toEqual([ENGINE])
      copy.files[M002] = copy.files[M002].replace('- [ ] T2:', '- [x] T2:')
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'cairn:milestone-plan')
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'hotfix')
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      await ui.unmount()
    })

    test(`a session end after a press shows the band again (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-plan')
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await $.session.end({ reason: 'clear', sessionId: 's1' })
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      await ui.unmount()
    })
  }

  test('a press on a lone skill row hides it', async ($, on) => {
    await eachSurface(
      'no-active',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-plan')
        expect(await lines(ui)).toEqual([skillRow('milestone-plan'), ENGINE])
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        expect(await hasCairn(ui)).toBe(false)
        // The next surface starts shown: a new skill prompt brings it back.
        await prompt($, 'hotfix')
      },
      $,
      on,
    )
  })
})

// M197: a band that fits narrow windows and the desktop font.

// Columns at one per code point.
const cols = (s: string) => [...s].length

// The columns of a drawn row's parts that never shrink: the head Box's
// Texts, the right group's left margin and Texts, and the close button's
// label. The terminal draws a Button that is not `plain` as `[ label ]`.
function fixedWidth(row: Element): number {
  const { head, right } = layout(row)
  const close = below(right, 'Button').reduce((n, b) => n + cols(String(b.props.label)) + (b.props.plain ? 0 : 4), 0)
  return cols(textOf(head)) + Number(right.props.marginLeft ?? 0) + cols(textOf(right)) + close
}

// Every band width from 36 to 120 columns.
const WIDTHS = Array.from({ length: 85 }, (_, i) => 36 + i)

// Mounts the terminal band at each width and collects each named row whose
// parts that never shrink are wider than the width. Returns the overruns
// and how many rows it measured.
async function sweep($, keys: string[]): Promise<{ overruns: string[]; measured: number }> {
  const overruns: string[] = []
  let measured = 0
  for (const columns of WIDTHS) {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...at(columns) })) as Ui
    for (const key of keys) {
      const [row] = await ui.findAll({ key })
      expect(row?.type).toBe('Box')
      measured += 1
      const width = fixedWidth(row)
      if (width > columns) overruns.push(`${key} at ${columns}: ${width}`)
    }
    await ui.unmount()
  }
  return { overruns, measured }
}

// The two skills that a milestone row carries, the status of that row, the
// field that holds its open item, and a long chapter.
const LONG_STEPS = [
  { skill: 'milestone-implement', status: 'in-progress', next: 'nextTask', chapter: 'T10a: Long step' },
  { skill: 'milestone-review', status: 'review', next: 'nextCriterion', chapter: 'AC10a: Long step' },
] as const

// The row that carries the skill on a fixture when it shows counts: the
// first row of the skill's status, with an open item.
function countsCarrier(name: string, status: string, next: 'nextTask' | 'nextCriterion') {
  const carrier = FIXTURES[name].rows.find(row => row.status === status)
  return carrier !== undefined && carrier[next] !== null ? carrier : undefined
}

describe('each sampled row fits the band from 36 to 120 columns in the terminal (M197 AC1)', () => {
  test('the sweep covers 36 to 120 columns, and the widest fixture reaches the bounds', () => {
    expect(WIDTHS.length).toBe(85)
    expect(WIDTHS[0]).toBe(36)
    expect(WIDTHS[84]).toBe(120)
    const rows = FIXTURES.widest.rows
    expect(rows.map(row => row.id)).toEqual(['M1000', 'M1001', 'M1002', 'M1003'])
    expect(rows.map(row => row.status)).toEqual(['in-progress', 'in-progress', 'review', 'review'])
    expect(rows[0].nextTask?.startsWith('T10a:')).toBe(true)
    expect(rows[2].nextCriterion?.startsWith('AC10a:')).toBe(true)
    expect([rows[3].criteriaChecked, rows[3].criteriaTotal]).toEqual([100, 100])
    expect(rows[1].tasksTotal).toBeNull()
    // Both long chapters have a carrier showing counts on the widest fixture.
    for (const { status, next } of LONG_STEPS) expect(countsCarrier('widest', status, next)).toBeDefined()
  })

  test('the widest fixture draws the full label at 120 columns', () => {
    expect(bandLines(FIXTURES.widest.rows[3], 120).map(lineText)).toEqual([
      'review M1003 Every criterion checked at the widest counts  all 100 criteria checked',
    ])
  })

  for (const name of Object.keys(FIXTURES)) {
    for (const row of FIXTURES[name].rows) {
      test(`${name}: ${row.id} as the only active row, with no skill running`, async ($, on) => {
        seat(on, alone(name, row.id))
        await $.turn.complete(turn())
        const { overruns, measured } = await sweep($, [`${row.id}-row`])
        expect(measured).toBe(WIDTHS.length)
        expect(overruns).toEqual([])
      })
    }

    for (const { skill, status, next, chapter: title } of LONG_STEPS) {
      const carrier = countsCarrier(name, status, next)
      if (carrier === undefined) continue
      test(`${name}: the row that carries ${skill} at a long chapter`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        await prompt($, skill)
        await chapter($, title)
        const { overruns, measured } = await sweep($, [`${carrier.id}-row`])
        expect(measured).toBe(WIDTHS.length)
        expect(overruns).toEqual([])
      })
    }
  }

  for (const name of ['no-active', 'widest']) {
    for (const skill of SKILLS) {
      test(`${name}: the ${skill} row at the chapter Question gate`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        await prompt($, skill)
        await chapter($, 'Question gate')
        const id = shownId(name, skill)
        const { overruns, measured } = await sweep($, [id === null ? 'skill-row' : `${id}-row`])
        expect(measured).toBe(WIDTHS.length)
        expect(overruns).toEqual([])
      })
    }
  }
})

// Each change of form, at the narrowest width that keeps the earlier form,
// worked out by hand at one column per code point. `left` reads the row's
// left group, and `right` its right group without the close button.
type Switch = {
  name: string
  fixture: string
  // The row made the only active one, when the fixture shows another.
  alone?: string
  step?: [string, string]
  key: string
  at: number
  part: 'left' | 'right'
  before: string
  after: string
}

const SWITCHES: Switch[] = [
  // Head `implement M002 → T2:` 20, text 10, margin 2, bar form 21, close 3.
  {
    name: 'the bar and counts give way to the counts with their noun',
    fixture: 'single-in-progress',
    key: 'M002-row',
    at: 56,
    part: 'right',
    before: '██████████  1/3 tasks',
    after: '1/3 tasks',
  },
  // Head 20, text 10, margin 2, `1/3 tasks` 9, close 3.
  {
    name: 'in the loop, the counts with their noun give way to the bare counts',
    fixture: 'single-in-progress',
    key: 'M002-row',
    at: 44,
    part: 'right',
    before: '1/3 tasks',
    after: '1/3',
  },
  // Head `implement M002 → ` 17, text 10 of 13, margin 2, `1/3 tasks` 9, close 3.
  {
    name: 'out of the loop, the counts with their noun give way to the bare counts',
    fixture: 'single-in-progress',
    step: ['milestone-implement', 'Question gate'],
    key: 'M002-row',
    at: 41,
    part: 'right',
    before: '1/3 tasks',
    after: '1/3',
  },
  // A text shorter than 10 needs only its own width: head 20, text ` Go.` 4,
  // margin 2, bar form 21, close 3.
  {
    name: 'a short text keeps the bar down to its own width',
    fixture: 'single-in-progress',
    step: ['milestone-implement', 'T3: Go.'],
    key: 'M002-row',
    at: 50,
    part: 'right',
    before: '██████████  1/3 tasks',
    after: '1/3 tasks',
  },
  // M053 as the only active row: head `review M053 ` 12, text 10, margin 2,
  // label 22, close 3.
  {
    name: 'all N criteria checked gives way to N/N checked',
    fixture: 'states-review',
    alone: 'M053',
    key: 'M053-row',
    at: 49,
    part: 'right',
    before: 'all 2 criteria checked',
    after: '2/2 checked',
  },
  // Head `review M004 ` 12, text 10, margin 2, label 17, close 3.
  {
    name: 'no milestone file gives way to no file',
    fixture: 'missing-file',
    key: 'M004-row',
    at: 44,
    part: 'right',
    before: 'no milestone file',
    after: 'no file',
  },
  // Head `plan /milestone-plan → ` 23, text 10 of 13, margin 2, close 3.
  {
    name: 'a skill row drops its slash command',
    fixture: 'no-active',
    step: ['milestone-plan', 'Question gate'],
    key: 'skill-row',
    at: 38,
    part: 'left',
    before: 'plan /milestone-plan → Question gate',
    after: 'plan → Question gate',
  },
]

describe('the right group and the skill row take shorter forms (M197 AC2)', () => {
  for (const { name, fixture, alone: only, step, key, at: columns, part, before, after } of SWITCHES) {
    test(`${fixture}: ${name} below ${columns} columns`, async ($, on) => {
      seat(on, only === undefined ? copyOf(fixture) : alone(fixture, only))
      await $.turn.complete(turn())
      if (step !== undefined) {
        await prompt($, step[0])
        await chapter($, step[1])
      }
      for (const [width, form] of [
        [columns, before],
        [columns - 1, after],
      ] as const) {
        await mountEach(
          fixture,
          at(width),
          async ui => {
            const [row] = await ui.findAll({ key })
            const { left, right } = layout(row)
            expect((part === 'left' ? textOf(left) : textOf(right)).trim()).toBe(form)
          },
          $,
        )
      }
    })
  }
})

// The phase label of each status, written out by hand.
const PHASE_LABEL: Record<string, string> = { 'in-progress': 'implement', review: 'review' }

// The head's first two Texts: the label and the space after it.
function labelGap(row: Element): string[] {
  return kids(layout(row).head)
    .slice(0, 2)
    .map(t => textOf(t))
}

// The bar's Texts in a row's right group, empty runs left out.
function barTexts(row: Element): Element[] {
  return below(layout(row).right, 'Text').filter(t => /[█░▒▓]/.test(textOf(t)))
}

describe('one space after the label, and one bar glyph with dim empty cells (M197 AC3)', () => {
  for (const name of Object.keys(FIXTURES)) {
    for (const fixtureRow of FIXTURES[name].rows) {
      test(`${name}: ${fixtureRow.id} alone at 120 columns`, async ($, on) => {
        seat(on, alone(name, fixtureRow.id))
        await $.turn.complete(turn())
        await mountEach(
          name,
          BAND,
          async ui => {
            const [row] = await ui.findAll({ key: `${fixtureRow.id}-row` })
            expect(labelGap(row)).toEqual([PHASE_LABEL[fixtureRow.status], ' '])
            const bar = barTexts(row)
            if (bar.length === 0) return
            expect(bar.map(t => textOf(t)).join('')).toBe('█'.repeat(10))
            // The filled run, when there is one, then the dim empty run.
            const empty = bar[bar.length - 1]
            expect(empty.props.dimColor).toBe(true)
            for (const filled of bar.slice(0, -1)) {
              expect(filled.props.dimColor).toBeUndefined()
              expect(filled.props.color).toBe(fixtureRow.status === 'review' ? 'success' : 'claude')
            }
          },
          $,
        )
      })
    }
  }

  test('single-in-progress at 1/3 tasks draws 3 filled cells and 7 dim ones', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    await mountEach(
      'single-in-progress',
      BAND,
      async ui => {
        const [row] = await ui.findAll({ key: 'M002-row' })
        const bar = barTexts(row)
        expect(bar.map(t => [textOf(t), t.props.dimColor === true])).toEqual([
          ['███', false],
          ['███████', true],
        ])
      },
      $,
    )
  })

  for (const name of ['no-active', 'widest']) {
    for (const skill of SKILLS) {
      test(`${name}: the ${skill} row at 120 columns`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        await prompt($, skill)
        const id = shownId(name, skill)
        await mountEach(
          name,
          BAND,
          async ui => {
            const [row] = await ui.findAll({ key: id === null ? 'skill-row' : `${id}-row` })
            expect(labelGap(row)).toEqual([LABELS[skill], ' '])
            const third = kids(layout(row).head)[2]
            expect(third === undefined ? '' : textOf(third)).toBe(id === null ? `/${skill}` : id)
          },
          $,
        )
      })
    }
  }
})

describe('one row whatever maxRows is (M197 AC5)', () => {
  // Written out by hand: the row's key and label with no skill, under
  // /milestone-review, and under /milestone.
  for (const [skill, key, label] of [
    [null, 'M070-row', 'implement'],
    ['milestone-review', 'M071-row', 'review'],
    ['milestone', 'M070-row', 'status'],
  ] as const) {
    test(`six-active at a maxRows of 3 with ${skill ?? 'no skill'}`, async ($, on) => {
      seat(on, copyOf('six-active'))
      await $.turn.complete(turn())
      if (skill !== null) await prompt($, skill)
      const view = { ...BAND, props: { ...BAND.props, maxRows: 3 } }
      await mountEach(
        'six-active',
        view,
        async ui => {
          expect(await rowKeys(ui)).toEqual([key])
          const [row] = await ui.findAll({ key })
          expect(labelOf(row)).toBe(label)
          await closesFirst(ui)
        },
        $,
      )
    })
  }
})
