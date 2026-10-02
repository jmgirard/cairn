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

// The rows at 120 columns, written out by hand, never derived from band.ts.
// The two spaces before a bar, a count, or a state label are the right
// group's left margin.
const DRAWN: Record<string, string[]> = {
  'single-in-progress': ['implement M002 → T2: Write the command.  ███░░░░░░░  1/3 tasks'],
  mixed: [
    'review    M010 → AC3: Third criterion.  ██████░░░░  2/3 criteria',
    'implement M012 A Tasks section with no boxes  no tasks',
    'review    M013 Capitalized status, file gone  no milestone file',
    'implement M014 No Tasks section at all  no tasks',
  ],
  'nested-first': ['implement M030 → T1a: Nested task, open, with extra spaces after the box.  ███░░░░░░░  1/3 tasks'],
  'states-implement': [
    'implement M040 Its file was never written  no milestone file',
    'implement M041 No Tasks section  no tasks',
    'implement M042 A Tasks section with no boxes  no tasks',
    'implement M043 Every task checked  all 3 tasks checked',
  ],
  'states-review': [
    'review    M050 Its file was never written  no milestone file',
    'review    M051 No criteria section  no criteria',
    'review    M052 A criteria section with no boxes  no criteria',
    'review    M053 Every criterion checked  all 2 criteria checked',
  ],
  'missing-file': ['review    M004 Its file was never written  no milestone file'],
  subdirectory: ['implement M007 Started from a subdirectory  all 2 tasks checked'],
  'unlabeled-item': ['implement M062 → Write the docs, with no label.  ███░░░░░░░  1/3 tasks'],
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

// A skill row's text: the label, padded as the phase label is, then the
// slash command, then the chapter when one is set.
const skillRow = (skill: string, title?: string) => `${LABELS[skill].padEnd(9)} /${skill}${title === undefined ? '' : ` → ${title}`}`

// The ROADMAP status of the row each phase skill runs on.
const CARRIED: Record<string, string> = { 'milestone-implement': 'in-progress', 'milestone-review': 'review' }

// The first row's right group ends in the close button.
async function closesFirst(ui: Ui) {
  const [first] = await ui.findAll({ key: (await rowKeys(ui))[0] })
  const right = kids(first)[1]
  const last = kids(right)[kids(right).length - 1]
  expect(last.type).toBe('Button')
  expect(keyOf(last)).toBe('cairn-close')
  expect((await ui.findAll({ type: 'Button' })).length).toBe(1)
}

describe('one row per active milestone, and one per skill row (M196 AC1)', () => {
  const names = Object.keys(FIXTURES)
  test('the fixture list holds the fixtures the row tests need', () => {
    expect(names.length).toBeGreaterThan(10)
    for (const name of ['mixed', 'no-active', 'no-roadmap', 'single-in-progress', 'states-review']) expect(names).toContain(name)
  })

  for (const name of names) {
    test(`${name}: with no skill running, one row per active row`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const rows = FIXTURES[name].rows
      await mountEach(
        name,
        BAND,
        async ui => {
          if (rows.length === 0) {
            expect(await hasCairn(ui)).toBe(false)
            return
          }
          expect(await rowKeys(ui)).toEqual(rows.map(row => `${row.id}-row`))
          await closesFirst(ui)
        },
        $,
      )
    })

    for (const [skill, title] of [
      ['milestone-implement', 'T1: Write it.'],
      ['milestone-review', 'Consistency gate'],
    ]) {
      test(`${name}: with ${skill} running and a chapter, one row per active row, plus a skill row when none carries it`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        await prompt($, skill)
        await chapter($, title)
        const rows = FIXTURES[name].rows
        const carried = rows.some(row => row.status === CARRIED[skill])
        await mountEach(
          name,
          BAND,
          async ui => {
            const keys = await rowKeys(ui)
            expect(keys.length).toBe(rows.length + (carried ? 0 : 1))
            expect(keys).toEqual([...(carried ? [] : ['skill-row']), ...rows.map(row => `${row.id}-row`)])
            await closesFirst(ui)
          },
          $,
        )
      })
    }
  }

  for (const name of ['single-in-progress', 'mixed', 'nested-first']) {
    test(`${name}: the rows in ROADMAP order, above the engine's drawing`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
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
      'implement M002 → T3: Write the docs.  ███░░░░░░░  1/3 tasks',
    ])
  })

  test('review: the chapter on the carrying row', () => {
    expect(bandLines(ROW('mixed', 'M010'), 120, 'AC1: First criterion.').map(lineText)).toEqual([
      'review    M010 → AC1: First criterion.  ██████░░░░  2/3 criteria',
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
    expect(bandLines(ROW('states-review', 'M053'), 120).map(lineText)).toEqual(['review    M053 Every criterion checked  all 2 criteria checked'])
  })

  for (const surface of SURFACES) {
    test(`a skill row with no chapter, then with one (${surface})`, async ($, on) => {
      seat(on, copyOf('no-active'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-plan')
      expect(await lines(ui)).toEqual(['plan      /milestone-plan', ENGINE])
      await chapter($, 'Question gate')
      expect(await lines(ui)).toEqual(['plan      /milestone-plan → Question gate', ENGINE])
      await ui.unmount()
    })
  }
})

describe('the right group shows the bar only in the task or criterion loop (M196 AC3)', () => {
  const m002 = ROW('single-in-progress', 'M002')
  test('a labeled chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, 'T2: Write the command.').map(lineText)).toEqual([DRAWN['single-in-progress'][0]])
  })

  test('a nested labeled chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, 'T2a: A sub-task.').map(lineText)).toEqual(['implement M002 → T2a: A sub-task.  ███░░░░░░░  1/3 tasks'])
  })

  test('an unlabeled chapter shows the counts alone', () => {
    expect(bandLines(m002, 120, 'Question gate').map(lineText)).toEqual(['implement M002 → Question gate  1/3 tasks'])
  })

  test('no chapter keeps the bar and the counts', () => {
    expect(bandLines(m002, 120, null).map(lineText)).toEqual([DRAWN['single-in-progress'][0]])
  })

  test('below 60 columns a labeled chapter shows the counts alone', () => {
    expect(bandLines(m002, 59, 'T2: Write the command.').map(lineText)).toEqual(['implement M002 → T2: Write the command.  1/3 tasks'])
  })

  test('a chapter on a state-label row keeps the label', () => {
    expect(bandLines(ROW('mixed', 'M013'), 120, 'AC1: A criterion.').map(lineText)).toEqual(['review    M013 → AC1: A criterion.  no milestone file'])
    expect(bandLines(ROW('mixed', 'M012'), 120, 'Question gate').map(lineText)).toEqual(['implement M012 → Question gate  no tasks'])
    expect(bandLines(ROW('states-review', 'M053'), 120, 'Consistency gate').map(lineText)).toEqual([
      'review    M053 → Consistency gate  all 2 criteria checked',
    ])
  })
})

describe('three states draw the title and the label (M193 AC2)', () => {
  for (const name of ['states-implement', 'states-review', 'missing-file', 'subdirectory']) {
    test(`${name}: one row each, with no bar`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
          expect(await rowKeys(ui)).toEqual(FIXTURES[name].rows.map(row => `${row.id}-row`))
          expect((await bandTexts(ui)).filter(t => /[█░]/.test(textOf(t)))).toEqual([])
          expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
        },
        $,
      )
    })
  }
})

describe('the rows carry style props (M193 AC3)', () => {
  for (const columns of [59, 60, 120]) {
    test(`mixed at ${columns} columns`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        at(columns),
        async ui => {
          const inBand = await bandTexts(ui)
          // A Text that holds only strings: one span of a row.
          const leaf = (text: string) => inBand.find(t => t.children.every(c => typeof c === 'string') && textOf(t) === text)
          expect(leaf('review   ')?.props.color).toBe('success')
          expect(leaf('implement')?.props.color).toBe('claude')
          expect(leaf('M010')?.props.bold).toBe(true)
          expect(leaf('no milestone file')?.props.color).toBe('warning')
          expect(inBand.length).toBeGreaterThan(10)
          expect(inBand.filter(t => t.props.wrap !== 'truncate-end')).toEqual([])

          const [row] = await ui.findAll({ key: 'M010-row' })
          expect(rowText(row).endsWith('  2/3 criteria')).toBe(true)
          const filled = leaf('██████')
          if (columns < 60) {
            expect(filled).toBeUndefined()
            expect(rowText(row)).toBe('review    M010 → AC3: Third criterion.  2/3 criteria')
          } else {
            expect(filled?.props.color).toBe('success')
            expect(leaf('░░░░')?.props.dimColor).toBe(true)
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

// The left group of each mixed row, written out by hand.
const MIXED_LEFT: Record<string, string> = {
  M010: 'review    M010 → AC3: Third criterion.',
  M012: 'implement M012 A Tasks section with no boxes',
  M013: 'review    M013 Capitalized status, file gone',
  M014: 'implement M014 No Tasks section at all',
}

describe('each row is a left and a right group (M194 AC1)', () => {
  for (const columns of [59, 60, 120]) {
    test(`mixed at ${columns} columns`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        at(columns),
        async ui => {
          const rows = FIXTURES.mixed.rows
          for (const [i, row] of rows.entries()) {
            const [drawn] = await ui.findAll({ key: `${row.id}-row` })
            expect(drawn.props.justifyContent).toBe('space-between')
            const { groups, left, right } = layout(drawn)
            expect(groups.map(g => g.type)).toEqual(['Box', 'Box'])
            expect(drawn.children.length).toBe(2)
            expect(right.props.flexShrink).toBe(0)
            expect(right.props.marginLeft).toBe(2)
            expect(textOf(left)).toBe(MIXED_LEFT[row.id])
            shrinks(drawn)
            // The right group: the bar at 60 columns or more, and the counts
            // or the state label; the close button last on the first row.
            const hasBar = below(right, 'Text').some(t => /[█░]/.test(textOf(t)))
            expect(hasBar).toBe(row.id === 'M010' && columns >= 60)
            const last = kids(right)[kids(right).length - 1]
            expect(last.type === 'Button').toBe(i === 0)
            if (i === 0) expect(keyOf(last)).toBe('cairn-close')
          }
          const [m013] = await ui.findAll({ key: 'M013-row' })
          expect(textOf(layout(m013).right).trim()).toBe('no milestone file')
        },
        $,
      )
    })
  }

  // A long chapter, labeled on long-title and unlabeled on wide-title,
  // reaches the text's Text whole; the engine cuts it.
  const LONG: [string, string, string, string, string][] = [
    ['long-title', 'milestone-implement', 'T2: ', '1/2 tasks', 'T2:'],
    ['wide-title', 'milestone-review', '', '1/2 criteria', ''],
  ]
  for (const [name, skill, prefix, counts, label] of LONG) {
    test(`${name} at 40 columns: the text's Text holds the whole long chapter`, async ($, on) => {
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
          expect(below(right, 'Text').some(t => /[█░]/.test(textOf(t)))).toBe(false)
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
        expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
        const buttons = await ui.findAll({ type: 'Button' })
        expect(buttons.map(keyOf)).toEqual(['cairn-close'])
        const [button] = buttons
        expect(button.props.role).toBe('dismiss')
        expect(button.props.plain).toBe(true)
        expect(button.props.label).toBe(CLOSE[surface])
        // The Button is the last child of the first row's right group.
        const [first] = await ui.findAll({ key: `${FIXTURES[name].rows[0].id}-row` })
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
      expect(await lines(ui)).toEqual([...DRAWN.mixed, BENEATH_ROW])
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
    test(`${name}: ${label} is bold and undimmed, and so is the rest`, async ($, on) => {
      seat(on, copyOf(name))
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
    after: ['implement M002 → T3: Write the docs.  ██████░░░░  2/3 tasks', ENGINE],
  },
  {
    name: 'a row moves from planned to in-progress',
    fixture: 'no-active',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
    },
    before: [ENGINE],
    after: ['implement M021 → T1: Not started.  ░░░░░░░░░░  0/1 tasks', ENGINE],
  },
  {
    name: 'a row moves from in-progress to review, and switches to criteria',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: ['review    M002 → AC1: The export command writes one file per table.  ░░░░░░░░░░  0/1 criteria', ENGINE],
  },
  {
    name: 'a row leaves both statuses from review',
    fixture: 'missing-file',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Its file was never written | review |', '| Its file was never written | done |')
    },
    before: ['review    M004 Its file was never written  no milestone file', ENGINE],
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
    after: ['implement M030 → T2: Second top-level task.  ██████░░░░  2/3 tasks', ENGINE],
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
    shown: ['M002-row', 'M005-row'],
  },
  {
    name: 'a removed active row shows it',
    fixture: 'mixed',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| A Tasks section with no boxes | in-progress |', '| A Tasks section with no boxes | done |')
    },
    shown: ['M010-row', 'M013-row', 'M014-row'],
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
    shown: ['M012-row', 'M010-row', 'M013-row', 'M014-row'],
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
const MIXED_REST = DRAWN.mixed.slice(1)

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
      const drawn = [skillRow('milestone-plan'), ...DRAWN['single-in-progress'], ENGINE]
      await mountEach('single-in-progress', BAND, async ui => expect(await lines(ui)).toEqual(drawn), $)
      await prompt($, other)
      await mountEach('single-in-progress', BAND, async ui => expect(await lines(ui)).toEqual(drawn), $)
    })
  }
})

describe('a running skill with no active row of its phase gets a skill row (M195 AC2)', () => {
  const CASES: { skill: string; fixture: string; drawn: string[] }[] = [
    { skill: 'milestone-plan', fixture: 'no-active', drawn: [skillRow('milestone-plan')] },
    { skill: 'milestone-plan', fixture: 'mixed', drawn: [skillRow('milestone-plan'), ...DRAWN.mixed] },
    { skill: 'hotfix', fixture: 'mixed', drawn: [skillRow('hotfix'), ...DRAWN.mixed] },
    {
      skill: 'milestone-review',
      fixture: 'single-in-progress',
      drawn: [skillRow('milestone-review'), ...DRAWN['single-in-progress']],
    },
    // Outside a cairn repo, a running cairn skill draws its row alone.
    { skill: 'cairn-init', fixture: 'no-roadmap', drawn: [skillRow('cairn-init')] },
    { skill: 'milestone-implement', fixture: 'mixed', drawn: DRAWN.mixed },
    { skill: 'milestone-review', fixture: 'mixed', drawn: DRAWN.mixed },
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
  test('a review prompt and an unlabeled chapter put the title on M010, with the counts alone', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-review')
        await chapter($, 'Post-merge hygiene')
        expect(await lines(ui)).toEqual(['review    M010 → Post-merge hygiene  2/3 criteria', ...MIXED_REST, ENGINE])
      },
      $,
      on,
    )
  })

  test('an implement prompt and a chapter put the title on M012, beside its label', async ($, on) => {
    await eachSurface(
      'mixed',
      'mark',
      async (ui, $) => {
        await prompt($, 'milestone-implement')
        await chapter($, 'T1: Write it.')
        const drawn = [DRAWN.mixed[0], 'implement M012 → T1: Write it.  no tasks', ...DRAWN.mixed.slice(2)]
        expect(await lines(ui)).toEqual([...drawn, ENGINE])
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
      expect(await lines(ui)).toEqual([...DRAWN.mixed, ENGINE])
      copy.files[M010] = copy.files[M010].replace('- [ ] AC3:', '- [x] AC3:')
      await chapter($, 'Consistency gate')
      expect(await lines(ui)).toEqual(['review    M010 → Consistency gate  all 3 criteria checked', ...MIXED_REST, ENGINE])
      await ui.unmount()
    })

    test(`the chapter moves to the next review row, then to a skill row (${surface})`, async ($, on) => {
      const copy = copyOf('mixed')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-review')
      copy.files[ROADMAP] = copy.files[ROADMAP].replace('| Nested tasks and a capital X | review |', '| Nested tasks and a capital X | done |')
      await chapter($, 'Approval gate')
      expect(await lines(ui)).toEqual([
        'implement M012 A Tasks section with no boxes  no tasks',
        'review    M013 → Approval gate  no milestone file',
        'implement M014 No Tasks section at all  no tasks',
        ENGINE,
      ])
      copy.files[ROADMAP] = copy.files[ROADMAP].replace('| Capitalized status, file gone | Review |', '| Capitalized status, file gone | done |')
      await chapter($, 'Post-merge hygiene')
      expect(await lines(ui)).toEqual([
        skillRow('milestone-review', 'Post-merge hygiene'),
        'implement M012 A Tasks section with no boxes  no tasks',
        'implement M014 No Tasks section at all  no tasks',
        ENGINE,
      ])
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
          expect(await lines(ui)).toEqual([...DRAWN.mixed, ENGINE])
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
        expect(await lines(ui)).toEqual([...DRAWN.mixed, ENGINE])
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
        expect(await lines(ui)).toEqual(['review    M010 → Consistency gate  2/3 criteria', ...MIXED_REST, ENGINE])
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
          expect(await lines(ui)).toEqual([skillRow('milestone-plan', 'Investigation'), ...DRAWN['single-in-progress'], ENGINE])
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
        expect(await lines(ui)).toEqual([...DRAWN.mixed, ENGINE])
      },
      $,
      on,
    )
  })
})

describe('the close button works with skill rows (M195 AC5)', () => {
  test('the close button sits on the skill row when it comes first', async ($, on) => {
    await eachSurface(
      'single-in-progress',
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
      expect(await rowKeys(ui)).toEqual(['skill-row', 'M002-row'])
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
