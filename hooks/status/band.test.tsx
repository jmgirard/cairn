import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import type { Flow, Span } from './band'
import { actionsFit, bandLines, CAIRN_SKILLS, flowOf, idleFlow, idleLines, knownStep, lineText, mark, same, stepLines } from './band'
import { FIXTURES, SKILLS } from './fixtures.gen'
import type { BandRow } from './reader'
import { listNames, loadBand, memorySource } from './reader'
import { brailleSpans, trackSvg } from './track'

// Each case answers the shipped mod's `$.session.cwd`, `$.fs.stat`,
// `$.fs.read` and `$.fs.list` calls from an in-memory copy of a fixture,
// keyed by absolute path. A plain answer goes back as `{ value }`; a path
// the copy lacks, and the read of a path it marks unreadable, go on to the
// bottom of the chain, which rejects, as a missing file does in a session.
// The copy is mutable: an edit case edits a file between two turn ends,
// and the second turn end reads the edit.

// The row is the same on both surfaces but for the track, an `Svg` on the
// desktop and braille cells in the terminal (M206), so the row suites run
// on both.
const SURFACES = ['terminal', 'desktop'] as const
// The implement, review, and plan hues, written out by hand (M198, M204).
const ORANGE = 'rgb(194,122,92)'
const GREEN = 'rgb(106,165,122)'
const BLUE = 'rgb(110,140,190)'
// The terminal track's ground and the pill's text color, written out by
// hand (M206).
const GROUND = 'userMessageBackground'
const WHITE = 'rgb(255,255,255)'
// Each status's hue in the track.
const HUE: Record<string, string> = { 'in-progress': ORANGE, review: GREEN }
const GRAY = 'inactive'
const WARNINGS = ['no milestone file', 'no file']
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

type Copy = {
  cwd: string
  files: Record<string, string>
  // Paths that stat as files but whose read rejects, as a file the session
  // cannot open does.
  unreadable?: string[]
  // While set, each ROADMAP read sets `held` and waits for this promise.
  hold?: Promise<void>
  held?: boolean
  // While set, a Stop beneath the mod answers with this block.
  stopBlock?: string
  // While set, a prompt beneath the mod runs this before it resolves.
  beforeSubmit?: () => Promise<void>
  // The origin kind and turn id of each prompt that reached beneath the mod.
  submitted?: { kind: string; turnId: string | undefined }[]
  // While set, the session's working directory read rejects (M210).
  cwdThrows?: boolean
  // While set, each write of the band's value lands with its root removed,
  // as a value that stores no root (M210).
  dropRoot?: boolean
  // While set, the key of each value the mod writes, in order (M210).
  stateSets?: string[]
  // While set, the next read of the step runs this once before it answers
  // (M210).
  afterStepRead?: () => Promise<void>
  // While set, a prompt beneath the mod is dropped with this reason (M210).
  dropSubmit?: string
  // The command and argument of each slash command run that reached beneath
  // the mod, the text and mode of each prompt-box fill, and the text of
  // each toast (M212).
  commands?: { command: string; args: string }[]
  fills?: { text: string; mode: string }[]
  toasts?: string[]
  // While set, a slash command run beneath the mod throws this message
  // (M212).
  runThrows?: string
  // While set, a slash command run beneath the mod waits for this promise
  // before it answers (M212 review).
  runHold?: Promise<void>
}

function copyOf(name: string): Copy {
  const fixture = FIXTURES[name]
  return { cwd: fixture.cwd, files: { ...fixture.files }, unreadable: [...fixture.unreadable] }
}

// The world beneath the mod: the fixture copy as the session's directory and
// files, a turn end that answers nothing, a Stop that answers nothing or the
// copy's block, a prompt that enters as given, a skill prompt passed
// through, the chapter tool, and a session end. The mod has no hook for the
// chapter tool since M206, so a chapter call reaches this one.
function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => {
    if (copy.cwdThrows === true) throw new Error('no working directory')
    return { value: copy.cwd }
  })
  // A shaped value crosses as `{ shape, value }`.
  on('state.get', async ($, e, next) => {
    const after = copy.afterStepRead
    if (after === undefined || e.plugin !== 'cairn' || e.key !== 'step') return next(e)
    copy.afterStepRead = undefined
    const result = await next(e)
    await after()
    return result
  })
  on('state.set', async ($, e, next) => {
    if (e.plugin === 'cairn') copy.stateSets?.push(e.key)
    if (copy.dropRoot !== true || e.plugin !== 'cairn' || e.key !== 'band') return next(e)
    const shaped = e.value as { shape: string; value: object }
    return next({ ...e, value: { ...shaped, value: { ...shaped.value, root: null } } })
  })
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) => {
    if (copy.hold !== undefined && e.path.endsWith('cairn/ROADMAP.md')) {
      copy.held = true
      await copy.hold
    }
    return has(e.path) && !(copy.unreadable ?? []).includes(e.path) ? { value: copy.files[e.path] } : next(e)
  })
  on('fs.list', async ($, e, next) => {
    const names = listNames(Object.keys(copy.files), e.path)
    if (names === null) return next(e)
    return { value: names.map(name => ({ name, kind: 'other', size: 0, mtimeMs: 0, isLink: false })) }
  })
  on('turn.complete', async () => ({ text: '' }))
  on('classic.Stop', async () => (copy.stopBlock === undefined ? {} : { block: copy.stopBlock }))
  on('prompt.submit', async ($, e) => {
    copy.submitted = [...(copy.submitted ?? []), { kind: e.origin.kind, turnId: e.turnId }]
    if (copy.beforeSubmit !== undefined) await copy.beforeSubmit()
    if (copy.dropSubmit !== undefined) return { drop: copy.dropSubmit }
    return { text: e.text, origin: e.origin }
  })
  on('skill.prompt', async ($, e) => ({ text: e.text }))
  on('command.run', async ($, e) => {
    copy.commands = [...(copy.commands ?? []), { command: e.command, args: e.args }]
    if (copy.runHold !== undefined) await copy.runHold
    if (copy.runThrows !== undefined) throw new Error(copy.runThrows)
    return { text: '' }
  })
  on('prompt.fill', async ($, e) => {
    copy.fills = [...(copy.fills ?? []), { text: e.text, mode: e.mode }]
    return { isFilled: true }
  })
  on('ui.toast', async ($, e) => {
    copy.toasts = [...(copy.toasts ?? []), e.text]
    return { value: undefined }
  })
  on('tool.call', { tool: CHAPTER_TOOL }, async () => ({ result: 'Chapter marked' }))
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

// The Texts below a node that hold only strings: the leaves a row draws.
function leavesOf(node: Element): Element[] {
  return below(node, 'Text').filter(t => t.children.every(c => typeof c === 'string'))
}

// A sweep's problems, cut to the first five and a count, so a failing
// sweep reports in a few lines.
function firstFew(problems: string[]): string[] {
  return problems.length <= 5 ? problems : [...problems.slice(0, 5), `and ${problems.length - 5} more`]
}

// Columns at one per code point.
const cols = (s: string) => [...s].length

const ROW_KEY = /^(M\d+|idle|plan)-row$/
const TRACK = '[track]'

// Whether a right-group child is part of the track: the desktop's `Svg`, or
// a terminal Text with a background color (a braille cell run on the
// ground, or the pill on the phase color).
function isTrack(node: Element): boolean {
  return node.type === 'Svg' || (node.type === 'Text' && node.props.backgroundColor !== undefined)
}

// The track's parts in a row's right group.
function trackParts(right: Element): Element[] {
  return kids(right).filter(isTrack)
}

// A right group's text, its track drawn as TRACK on either surface.
function rightText(right: Element): string {
  const parts: string[] = []
  for (const child of kids(right)) {
    if (isTrack(child)) {
      if (parts[parts.length - 1] !== TRACK) parts.push(TRACK)
    } else {
      parts.push(textOf(child))
    }
  }
  return parts.join('')
}

// One row's layout: the row, its two groups, the head Box that keeps its
// width (the id and the space), and the title's Box that gives way, with
// its Text. The empty row (M213) has no head, so its left group holds the
// title's Box alone.
function layout(row: Element) {
  const groups = kids(row)
  const [left, right] = groups
  const parts = kids(left)
  const [head, textBox] = parts.length === 1 ? [undefined, parts[0]] : parts
  return { groups, left, right, head, textBox, text: textBox ? kids(textBox)[0] : undefined }
}

// A row's text with its two groups joined by the right group's left margin,
// the least gap a row draws (a wide row spreads them further), its track as
// TRACK, and the close button's label and the spaces before it left out.
function rowText(row: Element): string {
  const groups = kids(row)
  if (row.props.justifyContent !== 'space-between' || groups.length !== 2) return textOf(row)
  const [left, right] = groups
  return `${textOf(left)}${' '.repeat(Number(right.props.marginLeft ?? 0))}${rightText(right)}`.trimEnd()
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

// The first row Box drawn.
async function firstRow(ui: Ui): Promise<Element> {
  const [row] = await ui.findAll({ key: (await rowKeys(ui))[0] })
  return row
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

// Mounts the band on each surface, runs `act` against it, and checks it.
async function eachSurface(name: string, act: (ui: Ui, $, copy: Copy) => Promise<void>, $, on, copy: Copy = copyOf(name)) {
  seat(on, copy)
  await $.turn.complete(turn())
  for (const surface of SURFACES) {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
    await act(ui, $, copy)
    await ui.unmount()
  }
}

// Each row at 120 columns, drawn as the only active row, written out by
// hand, never derived from band.ts: the id, the title, the two spaces of
// the right group's left margin, then the track and its percent, or the
// warning label. The track reads as TRACK.
const DRAWN: Record<string, string[]> = {
  'single-in-progress': ['M002 Add the export command  [track] 44%'],
  mixed: [
    'M010 Nested tasks and a capital X  [track] 88%',
    'M012 A Tasks section with no boxes  [track] 33%',
    'M013 Capitalized status, file gone  no milestone file',
    'M014 No Tasks section at all  [track] 33%',
  ],
  'nested-first': ['M030 The next task is nested  [track] 44%'],
  'states-implement': [
    'M040 Its file was never written  no milestone file',
    'M041 No Tasks section  [track] 33%',
    'M042 A Tasks section with no boxes  [track] 33%',
    'M043 Every task checked  [track] 66%',
  ],
  'states-review': [
    'M050 Its file was never written  no milestone file',
    'M051 No criteria section  [track] 66%',
    'M052 A criteria section with no boxes  [track] 66%',
    'M053 Every criterion checked  [track] 100%',
  ],
  'missing-file': ['M004 Its file was never written  no milestone file'],
  subdirectory: ['M007 Started from a subdirectory  [track] 66%'],
  'unlabeled-item': ['M062 The next task has no label  [track] 44%'],
}

// The one row each fixture draws at 120 columns with no skill running,
// written out by hand: its first `in-progress` row, else its first
// `review` row.
const SHOWN: Record<string, string> = {
  'single-in-progress': DRAWN['single-in-progress'][0],
  mixed: DRAWN.mixed[1],
  'nested-first': DRAWN['nested-first'][0],
  'states-implement': DRAWN['states-implement'][0],
  'states-review': DRAWN['states-review'][0],
  'missing-file': DRAWN['missing-file'][0],
  subdirectory: DRAWN.subdirectory[0],
  'unlabeled-item': DRAWN['unlabeled-item'][0],
}
// The row mixed draws while /milestone-review runs.
const MIXED_REVIEW = DRAWN.mixed[0]

// Each idle row at 120 columns, written out by hand (M199 AC1, M206 AC4):
// the id and the title, then the track and the command.
const IDLE_DRAWN: Record<string, string> = {
  candidates: 'M031 Next up  [track] /milestone-implement M031',
  'idle-deps': 'M040 Met by a done row and an archive file at another padding  [track] /milestone-implement M040',
  'idle-order': 'M500 Priority in mixed case  [track] /milestone-implement M500',
  'no-active': 'M021 Waiting to start  [track] /milestone-implement M021',
  'repo-at-cut': 'M191 Milestone status band, a Claude Code mod inside the cairn plugin  [track] /milestone-implement M191',
}

// The id of the row the band shows on a fixture, read from the fixture's
// rows by the rule: the first `review` row while /milestone-review runs and
// one exists, else the first `in-progress` row, else the first `review`
// row; null when no row is active.
function shownId(name: string, skill: string | null = null): string | null {
  const rows = FIXTURES[name].rows
  const first = (status: string) => rows.find(row => row.status === status)?.id
  return (skill === 'milestone-review' ? first('review') : undefined) ?? first('in-progress') ?? first('review') ?? null
}

// The id the idle row names on a fixture, whatever skill runs (M206 AC4):
// the first id of the fixture's workable list when no row is active, else
// null.
function idleId(name: string): string | null {
  return shownId(name) === null ? (FIXTURES[name].workable[0] ?? null) : null
}

// The key of the row a fixture draws, or null for none: with no active or
// workable row, the empty row where a ROADMAP is found (M213).
function shownKey(name: string, skill: string | null = null): string | null {
  const id = shownId(name, skill)
  if (id !== null) return `${id}-row`
  if (idleId(name) !== null) return 'idle-row'
  return FIXTURES[name].next === null ? null : 'plan-row'
}

// The fixtures with a ROADMAP and no active or workable row, written out
// by hand: each draws the empty row (M213 AC1).
const EMPTY_FIXTURES = ['all-waiting', 'candidates-skeleton']
const EMPTY_TEXT = 'No milestone ready'

const rowOf = (name: string, id: string) => FIXTURES[name].rows.find(row => row.id === id) as BandRow

// A copy of a fixture with every planned row set to blocked, so nothing is
// workable.
function noneWorkable(name: string): Copy {
  const copy = copyOf(name)
  for (const path of Object.keys(copy.files)) {
    if (path.endsWith('cairn/ROADMAP.md')) copy.files[path] = copy.files[path].replace(/\| planned \|/g, '| blocked |')
  }
  return copy
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

// Whether a fixture has a ROADMAP the reader finds: its next step is null
// only where none is found (M205).
const hasRoadmap = (name: string) => FIXTURES[name].next !== null

// The next-step and status Buttons (M212).
const ACTION_KEYS = ['cairn-next', 'cairn-status']

// Whether a fixture's band carries the action Buttons at 120 columns with
// `skill` running: only with no cairn skill running and a next step, read
// from the fixture's `next`, which test_status_fixtures.py holds to
// scripts/cairn_next.py's `recommend` (M212 AC1, AC2). Planning is a next
// step since M213. Every skill in SKILLS is a cairn skill.
const actsAt120 = (name: string, skill: string | null = null) => skill === null && FIXTURES[name].next !== null

// The band's Buttons: the open button and then the close button on a row
// drawn from a found ROADMAP, the close button alone otherwise (M205 AC4),
// and the two action Buttons before them where `actions` is set (M212).
const buttonKeys = (name: string, actions = false) =>
  hasRoadmap(name) ? [...(actions ? ACTION_KEYS : []), 'cairn-open', 'cairn-close'] : ['cairn-close']

// The row's right group ends in the close button, and the open button sits
// two places before it where the fixture has a ROADMAP.
async function closesFirst(ui: Ui, name: string, actions = false) {
  const right = kids(await firstRow(ui))[1]
  const last = kids(right)[kids(right).length - 1]
  expect(last.type).toBe('Button')
  expect(keyOf(last)).toBe('cairn-close')
  if (hasRoadmap(name)) expect(keyOf(kids(right)[kids(right).length - 3])).toBe('cairn-open')
  expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual(buttonKeys(name, actions))
}

// The close Button.
async function closeButton(ui: Ui): Promise<Element> {
  const [button] = await ui.findAll({ key: 'cairn-close' })
  return button
}

const CLOSE = { terminal: '×', desktop: '✕' } as const
// The close button is plain, its label alone, on both surfaces, and dim at
// rest on the desktop.
const PLAIN = { terminal: true, desktop: true } as const
const DIM = { terminal: undefined, desktop: true } as const

// What gives way in a row: the left group and the title's Box shrink to any
// width, and the head (the id and the space) keeps its width. The desktop
// app drew a long text whose Box lacked `minWidth: 0` past the edge, and
// shrank the short Texts beside it to nothing (M194).
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

// The left group is the bold gray id, one space, and the gray title, and
// no other Text (M206 AC1).
function idAndTitle(row: Element, id: string, title: string) {
  const { left } = layout(row)
  const texts = below(left, 'Text')
  expect(texts.map(t => textOf(t))).toEqual([id, ' ', title])
  expect(leavesOf(left).length).toBe(3)
  expect([texts[0].props.bold, texts[0].props.color]).toEqual([true, GRAY])
  expect([texts[2].props.bold, texts[2].props.color]).toEqual([undefined, GRAY])
  expect(textOf(left)).toBe(`${id} ${title}`)
}

// The columns of a drawn row's parts that never shrink: the head Box's
// Texts, the right group's left margin and parts, and the buttons' labels.
// The desktop's track counts as the columns its image stands for, at 7
// pixels a column. The terminal draws a Button that is not `plain` as
// `[ label ]`.
function fixedWidth(row: Element): number {
  const { head, right } = layout(row)
  const parts = kids(right).reduce((n, child) => {
    if (child.type === 'Svg') return n + Math.ceil(Number(child.props.width) / 7)
    if (child.type === 'Button') return n + cols(String(child.props.label)) + (child.props.plain ? 0 : 4)
    return n + cols(textOf(child))
  }, 0)
  return (head === undefined ? 0 : cols(textOf(head))) + Number(right.props.marginLeft ?? 0) + parts
}

// The room the title keeps in a drawn row at `columns`, and the room it
// needs: its own width, or 10 columns when that is less (M206 AC2, AC3).
function titleRoom(row: Element, columns: number, title: string): { room: number; need: number } {
  return { room: columns - fixedWidth(row), need: Math.min(cols(title), 10) }
}

// A milestone row's percent, worked out here from its counts: floor of 100
// × (plan + implement + review fills) / 3.
function percentOf(status: string, checked: number, total: number): number {
  if (status === 'in-progress') return total === 0 ? 33 : Math.floor((100 * (total + checked)) / (3 * total))
  return total === 0 ? 66 : Math.floor((100 * (2 * total + checked)) / (3 * total))
}

// The counts a row's phase shows.
function countsOf(row: BandRow): { checked: number; total: number } {
  return row.status === 'in-progress'
    ? { checked: row.tasksChecked as number, total: row.tasksTotal as number }
    : { checked: row.criteriaChecked as number, total: row.criteriaTotal as number }
}

// A Text as a span.
function spanOf(text: Element): Span {
  return {
    text: textOf(text),
    color: text.props.color as string | undefined,
    backgroundColor: text.props.backgroundColor as string | undefined,
    bold: text.props.bold as boolean | undefined,
  }
}

const BLANK = 0x2800
const isBraille = (ch: string) => (ch.codePointAt(0) as number) >= BLANK && (ch.codePointAt(0) as number) <= 0x28ff

// What is wrong with a terminal track drawn as these spans, for a row of
// this status and these counts (M206 AC3): every cell outside the pill is a
// braille cell on GROUND; one pill in the phase's hue, white and bold,
// showing `checked/total`, or `no tasks`, `no criteria`, or `none`, its
// whole text only where that text and its two spaces take a third of the
// track or less (M206 review); at least one cell before the pill carries
// dots in the phase's hue; and the cells add up to `columns`.
function trackProblems(spans: Span[], status: string, checked: number, total: number, columns: number): string[] {
  const out: string[] = []
  const hue = HUE[status]
  const pills = spans.filter(s => s.backgroundColor === hue)
  if (pills.length !== 1) return [`${pills.length} pills`]
  const [pill] = pills
  const at = spans.indexOf(pill)
  for (const span of spans) {
    if (span === pill) continue
    if (span.backgroundColor !== GROUND) out.push(`ground ${span.backgroundColor}`)
    if (![...span.text].every(isBraille)) out.push(`not braille: ${span.text}`)
  }
  if (pill.color !== WHITE || pill.bold !== true) out.push(`pill style ${pill.color} ${pill.bold}`)
  const shown = pill.text.trim()
  const noun = status === 'in-progress' ? 'tasks' : 'criteria'
  const name = status === 'in-progress' ? 'Implement' : 'Review'
  const whole = total === 0 ? `no ${noun}` : `${name} ${checked}/${total}`
  const short = total === 0 ? 'none' : `${checked}/${total}`
  const expected = (cols(whole) + 2) * 3 <= columns ? whole : short
  if (shown !== expected) out.push(`pill ${shown}, not ${expected}`)
  const dotted = spans.slice(0, at).some(s => s.color === hue && [...s.text].some(ch => isBraille(ch) && ch.codePointAt(0) !== BLANK))
  if (!dotted) out.push('no dots in the hue before the pill')
  const width = spans.reduce((n, s) => n + cols(s.text), 0)
  if (width !== columns) out.push(`width ${width} of ${columns}`)
  return out
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
    for (const skill of [null, ...SKILLS]) {
      test(`${name} with ${skill ?? 'no skill'}: one row on a fixture with an active row, else the idle row or none`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        const key = shownKey(name, skill)
        await mountEach(
          name,
          BAND,
          async ui => {
            if (key === null) {
              expect(await hasCairn(ui)).toBe(false)
              expect(await lines(ui)).toEqual([ENGINE])
              return
            }
            expect(await rowKeys(ui)).toEqual([key])
            await closesFirst(ui, name, actsAt120(name, skill))
          },
          $,
        )
      })
    }
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

  test('the hand-written rows match what band.ts builds, each track at its full 52 columns', () => {
    for (const [name, drawn] of Object.entries(DRAWN)) {
      const built = FIXTURES[name].rows.flatMap(row => bandLines(row, 120))
      expect(built.map(line => lineText(line).replace(/\[track \d+\]/, TRACK))).toEqual(drawn)
      for (const line of built) if (line.track !== undefined) expect(line.track.columns).toBe(52)
    }
  })

  test('the band yields to a survey', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    await mountEach('single-in-progress', { ...BAND, props: { ...BAND.props, hasSurvey: true } }, async ui => expect(await lines(ui)).toEqual([ENGINE]), $)
  })
})

describe('each row alone draws its title and its percent or warning label (M193 AC2)', () => {
  for (const name of ['states-implement', 'states-review', 'missing-file', 'subdirectory', 'mixed']) {
    for (const [i, fixtureRow] of FIXTURES[name].rows.entries()) {
      test(`${name}: ${fixtureRow.id} alone`, async ($, on) => {
        seat(on, alone(name, fixtureRow.id))
        await $.turn.complete(turn())
        await mountEach(
          name,
          BAND,
          async ui => {
            expect(await lines(ui)).toEqual([DRAWN[name][i], ENGINE])
            expect(await rowKeys(ui)).toEqual([`${fixtureRow.id}-row`])
            expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
          },
          $,
        )
      })
    }
  }

  test('the warning label shortens to no file where the long one leaves the title less than its room', () => {
    // `M004 ` 5, the title's room 10, the margin 2, the label 17, and the
    // buttons 5 (the open glyph and its space 2, the close gap and label 3).
    const m004 = rowOf('missing-file', 'M004')
    expect(bandLines(m004, 39, 5).map(lineText)).toEqual(['M004 Its file was never written  no milestone file'])
    expect(bandLines(m004, 38, 5).map(lineText)).toEqual(['M004 Its file was never written  no file'])
  })
})

describe("a row's left group is the bold id and the title (M206 AC1)", () => {
  // An in-progress and a review row, each with an unchecked next item.
  const OPEN = [
    { name: 'single-in-progress', id: 'M002', status: 'in-progress', item: 'T2: Write the command.' },
    { name: 'mixed', id: 'M010', status: 'review', item: 'AC3: Third criterion.' },
  ]
  const STEPS = [null, 'milestone-review', 'milestone-implement'] as const
  // What the old row drew beside the id: phase and skill labels, the arrow.
  const GONE = ['implement', 'review', 'plan', 'status', 'next', '→']

  test('each row has an unchecked next item of its phase', () => {
    for (const { name, id, status, item } of OPEN) {
      const row = rowOf(name, id)
      expect(row.status).toBe(status)
      expect(status === 'in-progress' ? row.nextTask : row.nextCriterion).toBe(item)
    }
  })

  for (const { name, id, item } of OPEN) {
    for (const skill of STEPS) {
      test(`${name}: ${id} alone with ${skill ?? 'no skill'}`, async ($, on) => {
        seat(on, alone(name, id))
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        const title = rowOf(name, id).title
        await mountEach(
          name,
          BAND,
          async ui => {
            expect(await rowKeys(ui)).toEqual([`${id}-row`])
            const row = await firstRow(ui)
            idAndTitle(row, id, title)
            expect(rowText(row)).toBe(DRAWN[name][FIXTURES[name].rows.findIndex(r => r.id === id)])
            const all = textOf(row)
            expect([all, all.includes(item), all.includes(item.split(':')[0])]).toEqual([all, false, false])
            for (const word of GONE) expect([word, textOf(layout(row).left).includes(word)]).toEqual([word, false])
          },
          $,
        )
      })
    }
  }

  // A row whose counts cannot be read, in-progress and review.
  const UNREAD = [
    { name: 'states-implement', id: 'M040' },
    { name: 'missing-file', id: 'M004' },
  ]
  for (const { name, id } of UNREAD) {
    for (const skill of STEPS) {
      for (const columns of [40, 200]) {
        test(`${name}: ${id} alone with ${skill ?? 'no skill'} at ${columns} columns keeps its warning label`, async ($, on) => {
          seat(on, alone(name, id))
          await $.turn.complete(turn())
          if (skill !== null) await prompt($, skill)
          await mountEach(
            name,
            at(columns),
            async ui => {
              const row = await firstRow(ui)
              idAndTitle(row, id, rowOf(name, id).title)
              const { right } = layout(row)
              // `M040 ` 5, the title's room 10, the margin 2, the label 17,
              // and the buttons 5 come to 39, so 40 columns keep the long
              // label.
              expect(rightText(right).trim()).toBe('no milestone file')
              const label = leavesOf(right).find(t => textOf(t) === 'no milestone file') as Element
              expect(label.props.color).toBe('warning')
              expect(trackParts(right)).toEqual([])
              expect(below(row, 'Svg')).toEqual([])
            },
            $,
          )
        })
      }
    }
  }
})

describe('the band draws in gray, with the warning label and the track in their colors (M198 AC1, AC2)', () => {
  for (const name of Object.keys(FIXTURES)) {
    for (const skill of [null, 'milestone-review'] as const) {
      test(`${name} with ${skill ?? 'no skill'}: every leaf's color`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        const key = shownKey(name, skill)
        for (const columns of [200, 40]) {
          await mountEach(
            name,
            at(columns),
            async (ui, surface) => {
              if (key === null) {
                expect(await ui.findAll({ key: 'cairn-band' })).toEqual([])
                return
              }
              expect(await rowKeys(ui)).toEqual([key])
              // The row and the leaves come from one tree, so the track's
              // parts are found among the leaves by identity.
              const box = await bandBox(ui)
              const row = below(box, 'Box').find(b => keyOf(b) === key) as Element
              const { right, left } = layout(row)
              if (key === 'plan-row') {
                // The empty row: the gray text alone, not bold (M213 AC1).
                expect(below(left, 'Text').map(t => [textOf(t), t.props.color, t.props.bold])).toEqual([[EMPTY_TEXT, GRAY, undefined]])
              } else {
                const id = key === 'idle-row' ? (idleId(name) as string) : key.replace(/-row$/, '')
                const title = key === 'idle-row' ? textOf(layout(row).text) : rowOf(name, id).title
                idAndTitle(row, id, title)
              }
              const track = new Set(trackParts(right))
              for (const leaf of leavesOf(box)) {
                const text = textOf(leaf)
                expect([text, leaf.props.dimColor]).toEqual([text, undefined])
                if (track.has(leaf) || /^ *$/.test(text)) continue
                expect([text, leaf.props.color]).toEqual([text, WARNINGS.includes(text) ? 'warning' : GRAY])
              }
              const button = await closeButton(ui)
              expect(button.props.plain).toBe(PLAIN[surface])
              expect(button.props.dimColor).toBe(DIM[surface])
              expect(button.props.label).toBe(CLOSE[surface])
            },
            $,
          )
        }
      })
    }
  }
})

describe('each row is a left and a right group (M194 AC1)', () => {
  for (const columns of [40, 58, 120]) {
    for (const row of FIXTURES.mixed.rows) {
      test(`mixed: ${row.id} alone at ${columns} columns`, async ($, on) => {
        seat(on, alone('mixed', row.id))
        await $.turn.complete(turn())
        await mountEach(
          'mixed',
          at(columns),
          async (ui, surface) => {
            const [drawn] = await ui.findAll({ key: `${row.id}-row` })
            expect(drawn.props.justifyContent).toBe('space-between')
            const { groups, left, right } = layout(drawn)
            expect(groups.map(g => g.type)).toEqual(['Box', 'Box'])
            expect(drawn.children.length).toBe(2)
            expect(right.props.flexShrink).toBe(0)
            expect(right.props.marginLeft).toBe(2)
            // With the image, the row and its right group center their parts.
            const center = surface === 'desktop' ? 'center' : undefined
            expect([drawn.props.alignItems, right.props.alignItems]).toEqual([center, center])
            expect(textOf(left)).toBe(`${row.id} ${row.title}`)
            shrinks(drawn)
            // The right group: the track, but on the row whose counts
            // cannot be read, then the close button.
            const track = trackParts(right)
            expect(track.length > 0).toBe(row.id !== 'M013')
            if (track.length > 0) expect(track[0]).toBe(kids(right)[0])
            const last = kids(right)[kids(right).length - 1]
            expect(last.type).toBe('Button')
            expect(keyOf(last)).toBe('cairn-close')
            if (row.id === 'M013') expect(rightText(right).trim()).toBe('no milestone file')
          },
          $,
        )
      })
    }
  }

  // A long title reaches the title's Text whole; the engine cuts it.
  for (const [name, percent] of [
    ['long-title', '50%'],
    ['wide-title', '83%'],
  ] as const) {
    test(`${name} at 40 columns: the title's Text holds the whole title, and the track keeps its place`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const [row] = FIXTURES[name].rows
      await mountEach(
        name,
        at(40),
        async ui => {
          const [drawn] = await ui.findAll({ key: `${row.id}-row` })
          const { right, text } = layout(drawn)
          expect(text?.children).toEqual([row.title])
          expect(text?.props.wrap).toBe('truncate-end')
          shrinks(drawn)
          expect(rightText(right).trim()).toBe(`${TRACK} ${percent}`)
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

// A press hides the band until the active list, the running skill while a
// row is active, or the idle row's id changes, and that state lasts the
// session, so each surface gets a session of its own.
describe('the close button (M194 AC2)', () => {
  for (const name of ['mixed', 'single-in-progress']) {
    for (const surface of SURFACES) {
      test(`${name}: one dismiss Button, and a press passes to the engine (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await lines(ui)).toEqual([SHOWN[name], ENGINE])
        const buttons = await ui.findAll({ type: 'Button' })
        expect(buttons.map(keyOf)).toEqual(buttonKeys(name, actsAt120(name)))
        const button = await closeButton(ui)
        expect(button.props.role).toBe('dismiss')
        expect(button.props.plain).toBe(PLAIN[surface])
        expect(button.props.dimColor).toBe(DIM[surface])
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

// Each edit case asserts the band at a first turn end, edits the copy, ends
// a second turn, and asserts again.
type Edit = { name: string; fixture: string; edit: (files: Record<string, string>) => void; before: string[]; after: string[] }

const ROADMAP = '/cairn/ROADMAP.md'
const M002 = '/cairn/milestones/M002-export.md'
const M030 = '/cairn/milestones/M030-nested.md'
const M010 = '/cairn/milestones/M010-nested.md'
const EDITS: Edit[] = [
  {
    name: 'a task gets checked',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: ['M002 Add the export command  [track] 55%', ENGINE],
  },
  {
    name: 'a row moves from planned to in-progress',
    fixture: 'no-active',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
    },
    before: [IDLE_DRAWN['no-active'], ENGINE],
    after: ['M021 Waiting to start  [track] 33%', ENGINE],
  },
  {
    name: 'a row moves from in-progress to review, and counts its criteria',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: ['M002 Add the export command  [track] 66%', ENGINE],
  },
  {
    name: 'a row leaves both statuses from review',
    fixture: 'missing-file',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Its file was never written | review |', '| Its file was never written | done |')
    },
    before: [DRAWN['missing-file'][0], ENGINE],
    // Nothing is active or workable then, so the empty row shows (M213).
    after: [EMPTY_TEXT, ENGINE],
  },
  {
    name: 'a row leaves both statuses',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | done |')
    },
    before: [DRAWN['single-in-progress'][0], ENGINE],
    after: [EMPTY_TEXT, ENGINE],
  },
  {
    name: 'a check on the nested task grows the percent',
    fixture: 'nested-first',
    edit: files => {
      files[M030] = files[M030].replace('- [ ]   T1a:', '- [x]   T1a:')
    },
    before: [DRAWN['nested-first'][0], ENGINE],
    after: ['M030 The next task is nested  [track] 55%', ENGINE],
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

// Waits on a timer until a ROADMAP read is held. A microtask loop does not
// reach the read (M200 plan probe).
async function untilHeld(copy: Copy) {
  for (let i = 0; i < 200 && copy.held !== true; i++) await new Promise(resolve => setTimeout(resolve, 5))
  expect(copy.held).toBe(true)
}

// Guards, which also pass before M200: the window M200 closes lies between
// awaits inside the mod, after the read returns, where a test cannot press.
describe('a press while a turn end reads the ROADMAP (M200 AC1)', () => {
  const HELD: { name: string; edit: (files: Record<string, string>) => void; shown: string[] | null }[] = [
    { name: 'with the file unchanged, the band stays hidden', edit: () => {}, shown: null },
    {
      name: 'with M002 moved to review, the band shows again',
      edit: files => {
        files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
      },
      shown: ['M002-row'],
    },
  ]
  for (const { name, edit, shown } of HELD) {
    test(name, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      edit(copy.files)
      let release = () => {}
      copy.hold = new Promise<void>(resolve => {
        release = resolve
      })
      const ending = $.turn.complete(turn())
      await untilHeld(copy)
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      copy.hold = undefined
      release()
      await ending
      if (shown === null) {
        expect(await lines(ui)).toEqual([ENGINE])
      } else {
        expect(await rowKeys(ui)).toEqual(shown)
      }
      await ui.unmount()
    })
  }
})

describe('a session end shows a band that a press hid (M200 AC3)', () => {
  for (const surface of SURFACES) {
    for (const reason of ['clear', 'resume'] as const) {
      test(`reason ${reason}, with no skill running (${surface})`, async ($, on) => {
        seat(on, copyOf('single-in-progress'))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        await $.session.end({ reason, sessionId: 's1' })
        expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
        await ui.unmount()
      })

      test(`reason ${reason}, with a skill running (${surface})`, async ($, on) => {
        seat(on, copyOf('single-in-progress'))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        await prompt($, 'milestone-plan')
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        await $.session.end({ reason, sessionId: 's1' })
        expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
        await ui.unmount()
      })
    }
  }
})

describe("the close button's mark (M200 AC4, M206 AC4)", () => {
  test('over no-active, the mark for a stored skill no longer listed equals the mark for no step, and both name M021', async () => {
    const fixture = FIXTURES['no-active']
    const state = await loadBand(memorySource(fixture.files, fixture.cwd))
    expect(state).not.toBeNull()
    const gone = mark(state!, { skill: 'milestone-gone' })
    const none = mark(state!, null)
    expect(none).toEqual({ marks: [], skill: null, idle: 'M021' })
    expect(gone).toEqual(none)
    expect(same(gone, none)).toBe(true)
  })

  // The mark holds `milestone-review` only while it moves the band to
  // another row, and the idle id only while no row is active (M206 review).
  test('the mark holds the skill only where it moves the row, and the idle id only while no row is active', async () => {
    const state = async (name: string) => (await loadBand(memorySource(FIXTURES[name].files, FIXTURES[name].cwd)))!
    const idleState = await state('no-active')
    for (const skill of SKILLS) expect([skill, mark(idleState, { skill })]).toEqual([skill, { marks: [], skill: null, idle: 'M021' }])
    const activeState = await state('single-in-progress')
    const m002 = [{ id: 'M002', status: 'in-progress' }]
    for (const skill of SKILLS) expect([skill, mark(activeState, { skill })]).toEqual([skill, { marks: m002, skill: null, idle: null }])
    expect(mark(activeState, null)).toEqual({ marks: m002, skill: null, idle: null })
    // On mixed, /milestone-review moves the band from the in-progress row
    // to the review row, so its mark differs from the plain one.
    const mixedState = await state('mixed')
    expect(mixedState.rows.some(row => row.status === 'in-progress')).toBe(true)
    expect(mark(mixedState, { skill: 'milestone-review' }).skill).toBe('milestone-review')
    expect(mark(mixedState, { skill: 'milestone-implement' }).skill).toBeNull()
    // With review rows only, the review skill shows the same row.
    const reviewState = await state('states-review')
    expect(reviewState.rows.length > 0 && reviewState.rows.every(row => row.status === 'review')).toBe(true)
    expect(mark(reviewState, { skill: 'milestone-review' }).skill).toBeNull()
  })

  test('a stored skill not in the list reads as no step', () => {
    expect(knownStep({ skill: 'milestone-gone' })).toBeNull()
    expect(knownStep({ skill: 'hotfix' })).toEqual({ skill: 'hotfix' })
    expect(knownStep(null)).toBeNull()
  })
})

// The ROADMAP stats as a file, and its read rejects.
describe('a failed read of a found ROADMAP keeps the rows and alone does not hide or show the band (M200 AC2)', () => {
  for (const surface of SURFACES) {
    test(`after a press, the band stays hidden through a failed read and the good read after it (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      copy.unreadable = [ROADMAP]
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      copy.unreadable = []
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      expect(await hasCairn(ui)).toBe(false)
      await ui.unmount()
    })

    test(`with no press, a failed read still draws the row (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      copy.unreadable = [ROADMAP]
      await $.turn.complete(turn())
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      await ui.unmount()
    })
  }
})

// The cairn pane, as the band's tests read it beside the band.
const PANE_VIEW = {
  component: 'Pane',
  requestId: 'cairn',
  props: { title: 'cairn', isFocused: false, bodyColumns: 60, placement: 'dock', scroll: { offset: 0, bodyRows: 200 }, view: {} },
} as const

async function paneText($, surface: (typeof SURFACES)[number]): Promise<string> {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const text = root === undefined ? '' : textOf(root)
  await ui.unmount()
  return text
}

const BEFORE = 'Add the export command'
const EDITED = 'Add the import command'
const OTHER_ROADMAP = '/other/cairn/ROADMAP.md'

describe('a failed read in the same root keeps the rows drawn before it (M210 AC2)', () => {
  for (const surface of SURFACES) {
    test(`an edit made before a failed read shows only once a read succeeds (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      copy.files[ROADMAP] = copy.files[ROADMAP].replace(BEFORE, EDITED)
      copy.unreadable = [ROADMAP]
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      expect(await paneText($, surface)).toContain(BEFORE)
      copy.unreadable = []
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([`M002 ${EDITED}  [track] 44%`, ENGINE])
      const pane = await paneText($, surface)
      expect(pane).toContain(EDITED)
      expect(pane).not.toContain(BEFORE)
      await ui.unmount()
    })

    for (const [name, text] of [['empty', ''], ['whitespace-only', ' \n\t\n']] as const) {
      test(`an ${name} ROADMAP text keeps the rows (${surface})`, async ($, on) => {
        const copy = copyOf('single-in-progress')
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        copy.files[ROADMAP] = text
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
        expect(await paneText($, surface)).toContain(BEFORE)
        await ui.unmount()
      })
    }
  }
})

describe('a failed read never draws rows from another root (M210 AC3)', () => {
  for (const surface of SURFACES) {
    test(`a failed read after a move to another repo root empties the band and the pane (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      copy.cwd = '/other'
      copy.files[OTHER_ROADMAP] = copy.files[ROADMAP]
      copy.unreadable = [OTHER_ROADMAP]
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      expect(await paneText($, surface)).not.toContain(BEFORE)
      await ui.unmount()
    })

    test(`a working-directory read that throws empties the band and the pane (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      copy.cwdThrows = true
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      expect(await paneText($, surface)).not.toContain(BEFORE)
      await ui.unmount()
    })

    test(`rows stored with no root are not kept through a failed read (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      copy.dropRoot = true
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['M002-row'])
      copy.unreadable = [ROADMAP]
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      expect(await paneText($, surface)).not.toContain(BEFORE)
      await ui.unmount()
    })
  }
})

describe('the close state is written only on a change, and a session end beats a press (M210 AC4)', () => {
  for (const surface of SURFACES) {
    test(`a refresh with nothing hidden writes no close state (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      copy.stateSets = []
      await $.turn.complete(turn())
      // The record holds the refresh's own writes, so it is not empty.
      expect(copy.stateSets).toContain('band')
      expect(copy.stateSets.filter(key => key === 'dismissed')).toEqual([])
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      await ui.unmount()
    })

    test(`a session end between a press's reads and its write leaves the band shown (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      let ended = false
      copy.afterStepRead = async () => {
        await $.session.end({ reason: 'clear', sessionId: 's1' })
        ended = true
      }
      await ui.press({ key: 'cairn-close' })
      expect(ended).toBe(true)
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      // With no session end in between, the same press hides the band.
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await ui.unmount()
    })
  }
})

describe('the band draws nothing where no ROADMAP is found', () => {
  for (const name of ['no-roadmap']) {
    for (const skill of [null, 'milestone-plan'] as const) {
      test(`${name} with ${skill ?? 'no skill'}: the mod draws nothing, passes to the engine, and does not throw`, { plugins: [PROBE] }, async ($, on) => {
        seat(on, noneWorkable(name))
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        for (const surface of SURFACES) {
          const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
          const shown = (await ui.findAll({ type: 'Text' })).map(textOf)
          expect(shown).toEqual(['cairn hook: returned', ENGINE])
          await ui.unmount()
        }
      })
    }
  }

  test('a cairn repo with a ROADMAP below the working directory only draws nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    // The ROADMAP sits one level below the working directory, where the
    // upward walk never looks.
    seat(on, { cwd: '/', files: Object.fromEntries(Object.entries(copy.files).map(([k, v]) => [`/below${k}`, v])) })
    await $.turn.complete(turn())
    await mountEach('single-in-progress', BAND, async ui => expect(await lines(ui)).toEqual([ENGINE]), $)
  })
})

// The empty row's checks (M213 AC1): its left group is the gray title in a
// Box that gives way, with no head and no bold; its right group has no
// track and no tail; it ends in the open and close buttons.
async function isEmptyRow(ui: Ui, actions: boolean) {
  expect(await rowKeys(ui)).toEqual(['plan-row'])
  const row = await firstRow(ui)
  const { left, right, head, textBox } = layout(row)
  expect(head).toBeUndefined()
  expect([textBox.type, textBox.props.flexShrink, textBox.props.minWidth]).toEqual(['Box', 1, 0])
  const texts = below(left, 'Text')
  expect(texts.map(t => [textOf(t), t.props.color, t.props.bold])).toEqual([[EMPTY_TEXT, GRAY, undefined]])
  expect([left.props.flexShrink, left.props.minWidth]).toEqual([1, 0])
  expect(trackParts(right)).toEqual([])
  expect(rowText(row)).toBe(EMPTY_TEXT)
  const last = kids(right)[kids(right).length - 1]
  expect(keyOf(last)).toBe('cairn-close')
  expect(keyOf(kids(right)[kids(right).length - 3])).toBe('cairn-open')
  expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([...(actions ? ACTION_KEYS : []), 'cairn-open', 'cairn-close'])
}

describe('a found ROADMAP with nothing active or workable draws the empty row (M213 AC1)', () => {
  test('the hand-written empty fixtures are the fixtures whose next step is planning', () => {
    const domain = Object.keys(FIXTURES).filter(name => FIXTURES[name].next !== null && FIXTURES[name].next?.id === null)
    expect(domain.sort()).toEqual([...EMPTY_FIXTURES].sort())
  })

  const CASES: { name: string; copy: () => Copy }[] = [
    ...EMPTY_FIXTURES.map(name => ({ name, copy: () => copyOf(name) })),
    // Fixtures whose planned rows are set to blocked, so nothing is workable.
    ...['no-active', 'idle-deps'].map(name => ({ name: `${name} with nothing workable`, copy: () => noneWorkable(name) })),
  ]
  for (const { name, copy } of CASES) {
    for (const skill of [null, 'milestone-plan'] as const) {
      test(`${name} with ${skill ?? 'no skill'}: the empty row above the engine's drawing`, async ($, on) => {
        seat(on, copy())
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        await mountEach(
          name,
          BAND,
          async ui => {
            await isEmptyRow(ui, skill === null)
            expect(await lines(ui)).toEqual([EMPTY_TEXT, ENGINE])
          },
          $,
        )
      })
    }
  }
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

  test('with nothing active or workable, the empty row sits above the band beneath (M213)', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, noneWorkable('no-active'))
    await $.turn.complete(turn())
    await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([EMPTY_TEXT, BENEATH_ROW]), $)
  })

  test('with no ROADMAP, the band beneath shows alone', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    await mountEach('no-roadmap', BAND, async ui => expect(await lines(ui)).toEqual([BENEATH_ROW]), $)
  })

  test('the idle row sits above the band beneath (M199)', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('no-active'))
    await $.turn.complete(turn())
    await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([IDLE_DRAWN['no-active'], BENEATH_ROW]), $)
  })
})

// M195: the running cairn skill. Since M206 the only thing it changes on
// the row is which row shows: /milestone-review shows the first review row.

describe('a running /milestone-review picks the review row (M195 AC1)', () => {
  for (const spelling of ['milestone-review', 'cairn:milestone-review']) {
    test(`${spelling} over mixed`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await prompt($, spelling)
      await mountEach('mixed', BAND, async ui => expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE]), $)
    })
  }

  for (const other of ['commit', 'other:milestone-implement', 'cairn:nope']) {
    test(`${other} leaves the step as it was`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await prompt($, 'milestone-review')
      await mountEach('mixed', BAND, async ui => expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE]), $)
      await prompt($, other)
      await mountEach('mixed', BAND, async ui => expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE]), $)
    })
  }
})

describe('every session end clears the step (M195 AC4)', () => {
  for (const reason of ['clear', 'resume'] as const) {
    test(`a session end with reason ${reason}`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $) => {
          await prompt($, 'milestone-review')
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.session.end({ reason, sessionId: 's1' })
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }
})

describe('one row whatever maxRows is (M197 AC5)', () => {
  // Written out by hand: the row's key with no skill, under
  // /milestone-review, and under /milestone.
  for (const [skill, key] of [
    [null, 'M070-row'],
    ['milestone-review', 'M071-row'],
    ['milestone', 'M070-row'],
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
          await closesFirst(ui, 'six-active', actsAt120('six-active', skill))
        },
        $,
      )
    })
  }
})

describe('the idle row names the next workable milestone (M199 AC1)', () => {
  test('the hand-written idle rows cover every fixture that draws one', () => {
    const domain = Object.keys(FIXTURES).filter(name => idleId(name) !== null)
    expect(Object.keys(IDLE_DRAWN).sort()).toEqual(domain.sort())
  })

  for (const [name, text] of Object.entries(IDLE_DRAWN)) {
    test(`${name}: the idle row with its track and command at 120 columns`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([text, ENGINE])
          await closesFirst(ui, name, actsAt120(name))
        },
        $,
      )
    })

    test(`${name}: the idle row leaves its track and command out at 40 columns`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const id = idleId(name) as string
      await mountEach(
        name,
        at(40),
        async ui => {
          const [row] = await lines(ui)
          expect(row.startsWith(`${id} `)).toBe(true)
          expect(row).not.toContain('/milestone-implement')
          expect(row).not.toContain(TRACK)
          await closesFirst(ui, name)
        },
        $,
      )
    })
  }

  test('the track and the command stay while the title keeps its room, and go at one column less', () => {
    // The head `M001 ` takes 5 columns, the gap 2, the space and the command
    // 26, the least track 12, and the close gap and label 3.
    const short = { id: 'M001', title: 'Go' }
    expect(lineText(idleLines(short, 50, 3)[0])).toBe('M001 Go  [track 12] /milestone-implement M001')
    expect(lineText(idleLines(short, 49, 3)[0])).toBe('M001 Go  /milestone-implement M001')
    expect(lineText(idleLines(short, 37, 3)[0])).toBe('M001 Go  /milestone-implement M001')
    expect(lineText(idleLines(short, 36, 3)[0])).toBe('M001 Go')
    const long = { id: 'M001', title: 'A title well over ten columns' }
    expect(lineText(idleLines(long, 58, 3)[0])).toBe('M001 A title well over ten columns  [track 12] /milestone-implement M001')
    expect(lineText(idleLines(long, 57, 3)[0])).toBe('M001 A title well over ten columns  /milestone-implement M001')
    expect(lineText(idleLines(long, 45, 3)[0])).toBe('M001 A title well over ten columns  /milestone-implement M001')
    expect(lineText(idleLines(long, 44, 3)[0])).toBe('M001 A title well over ten columns')
  })

  test('with nothing active or workable, a found ROADMAP gives the empty row and none gives nothing (M213 AC1)', () => {
    expect(stepLines([], null, 120, 5, [], true).map(lineText)).toEqual(['No milestone ready'])
    expect(stepLines([], null, 120, 5, [], true).map(line => [line.key, line.id, line.track])).toEqual([['plan-row', '', undefined]])
    expect(stepLines([], null, 120, 5, [], false)).toEqual([])
    expect(stepLines([], null, 120, 5)).toEqual([])
    // A workable row still gives the idle row, found or not.
    expect(stepLines([], null, 120, 5, [{ id: 'M001', title: 'Go' }], true).map(line => line.key)).toEqual(['idle-row'])
  })

  test('the empty row keeps the action Buttons while its text keeps 10 columns, and no narrower (M213 AC2)', () => {
    // The close gap and label 3, the open button and its space 2, `[ Plan ]`
    // and a space 9, `[ Status ]` and a space 11: 25 reserved. With the gap
    // of 2, 27 columns are taken, so 37 leaves the text its 10.
    const [line] = stepLines([], null, 37, 25, [], true)
    expect(actionsFit(line, 37, 25)).toBe(true)
    expect(actionsFit(line, 36, 25)).toBe(false)
    expect(actionsFit(line, 200, 25)).toBe(true)
  })

  test('an active row draws its milestone row, though a planned row is workable', async ($, on) => {
    expect(FIXTURES['six-active'].workable).toEqual(['M073'])
    seat(on, copyOf('six-active'))
    await $.turn.complete(turn())
    await mountEach('six-active', BAND, async ui => expect(await rowKeys(ui)).toEqual(['M070-row']), $)
  })

  test('the session start draws the idle row before any turn ends', async ($, on) => {
    seat(on, copyOf('no-active'))
    on('session.start', async ($, e) => ({ cwd: e.cwd }))
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([IDLE_DRAWN['no-active'], ENGINE]), $)
  })
})

// Every band width from 40 to 200 columns (M206 AC2, AC3).
const WIDTHS = Array.from({ length: 161 }, (_, i) => 40 + i)

describe('each row fits the band from 40 to 200 columns, the title keeping its room (M197 AC1)', () => {
  test('the sweep covers 40 to 200 columns', () => {
    expect([WIDTHS.length, WIDTHS[0], WIDTHS[160]]).toEqual([161, 40, 200])
  })

  // Every fixture's row alone, the idle rows, the empty rows (M213), and the
  // warning rows among them, on both surfaces.
  const CASES: { name: string; key: string; copy: () => Copy }[] = [
    ...Object.keys(FIXTURES).flatMap(name => FIXTURES[name].rows.map(row => ({ name, key: `${row.id}-row`, copy: () => alone(name, row.id) }))),
    ...Object.keys(IDLE_DRAWN).map(name => ({ name, key: 'idle-row', copy: () => copyOf(name) })),
    ...EMPTY_FIXTURES.map(name => ({ name, key: 'plan-row', copy: () => copyOf(name) })),
  ]
  for (const { name, key, copy } of CASES) {
    test(`${name}: ${key}`, async ($, on) => {
      seat(on, copy())
      await $.turn.complete(turn())
      const problems: string[] = []
      for (const columns of WIDTHS) {
        for (const surface of SURFACES) {
          const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...at(columns) })) as Ui
          const [row] = await ui.findAll({ key })
          const title = textOf(layout(row).text)
          const { room, need } = titleRoom(row, columns, title)
          if (room < need) problems.push(`${surface} at ${columns}: ${room} < ${need}`)
          await ui.unmount()
        }
      }
      expect(firstFew(problems)).toEqual([])
    })
  }
})

// The rows AC2 and AC3 sweep, built here: titles shorter and longer than 10
// columns, ids of 4 and 5 characters, and partial, all-checked, and
// zero-item counts on an in-progress and a review row.
const TITLES = ['Go', 'A title well over ten columns']
const IDS = ['M206', 'M1000']
const COUNTS: { status: string; checked: number; total: number }[] = [
  { status: 'in-progress', checked: 1, total: 3 },
  { status: 'in-progress', checked: 3, total: 3 },
  { status: 'in-progress', checked: 0, total: 0 },
  { status: 'review', checked: 2, total: 5 },
  { status: 'review', checked: 4, total: 4 },
  { status: 'review', checked: 0, total: 0 },
]

function built(id: string, title: string, status: string, checked: number, total: number): BandRow {
  const tasks = status === 'in-progress' ? [checked, total] : [3, 3]
  const criteria = status === 'review' ? [checked, total] : [0, 2]
  return {
    id,
    title,
    status,
    tasksChecked: tasks[0],
    tasksTotal: tasks[1],
    criteriaChecked: criteria[0],
    criteriaTotal: criteria[1],
    nextTask: tasks[0] < tasks[1] ? 'T9: Open.' : null,
    nextCriterion: criteria[0] < criteria[1] ? 'AC9: Open.' : null,
  }
}

// The track's columns for a row, worked out here: the room the row leaves
// once the id and its space, the title's room, the gap, the tail, and the
// buttons are taken, held between 12 and 52.
function trackFor(id: string, title: string, percent: number, columns: number, close: number): number {
  const left = columns - (cols(id) + 1) - Math.min(cols(title), 10) - 2 - (cols(` ${percent}%`)) - close
  return Math.max(12, Math.min(52, left))
}

// The fixture rows the rendered sweeps draw alone: partial, all-checked,
// and zero-item counts on an in-progress and a review row, 4- and
// 5-character ids, and long and wide titles.
const SWEPT: [string, string][] = [
  ['single-in-progress', 'M002'],
  ['states-implement', 'M043'],
  ['states-implement', 'M042'],
  ['mixed', 'M010'],
  ['states-review', 'M053'],
  ['states-review', 'M052'],
  ['widest', 'M1000'],
  ['widest', 'M1002'],
  ['long-title', 'M060'],
  ['wide-title', 'M061'],
]

describe('the desktop draws the track at every width from 40 to 200 columns (M206 AC2)', () => {
  test('the swept rows cover both statuses and partial, all-checked, and zero-item counts', () => {
    const kinds = SWEPT.map(([name, id]) => {
      const row = rowOf(name, id)
      const { checked, total } = countsOf(row)
      return `${row.status} ${total === 0 ? 'zero' : checked === total ? 'all' : 'partial'}`
    })
    for (const status of ['in-progress', 'review']) for (const kind of ['zero', 'all', 'partial']) expect(kinds).toContain(`${status} ${kind}`)
    expect(TITLES.map(cols).map(n => n > 10)).toEqual([false, true])
  })

  for (const id of IDS) {
    for (const title of TITLES) {
      for (const { status, checked, total } of COUNTS) {
        test(`built ${id} ${status} ${checked}/${total}, title of ${cols(title)} columns`, () => {
          const row = built(id, title, status, checked, total)
          const percent = percentOf(status, checked, total)
          const step = status === 'review' ? { skill: 'milestone-review' } : null
          const problems: string[] = []
          for (const close of [3, 5]) {
            for (const columns of WIDTHS) {
              const [line] = stepLines([row], step, columns, close)
              const where = `close ${close} at ${columns}`
              if (line.track === undefined) {
                problems.push(`${where}: no track`)
                continue
              }
              const want = trackFor(id, title, percent, columns, close)
              if (line.track.columns !== want) problems.push(`${where}: ${line.track.columns} columns, not ${want}`)
              const px = Math.min(360, line.track.columns * 7)
              if ((px === 360) !== (want === 52)) problems.push(`${where}: ${px} px`)
              const room = columns - (cols(id) + 1) - 2 - line.track.columns - cols(` ${percent}%`) - close
              if (room < Math.min(cols(title), 10)) problems.push(`${where}: title room ${room}`)
              if (line.tail.map(s => s.text).join('') !== ` ${percent}%`) problems.push(`${where}: tail`)
              if (!trackSvg(line.track.flow, px).startsWith(`<svg xmlns="http://www.w3.org/2000/svg" width="${px}" `)) problems.push(`${where}: svg width`)
            }
          }
          expect(firstFew(problems)).toEqual([])
        })
      }
    }
  }

  for (const [name, id] of SWEPT) {
    test(`${name}: ${id} alone, drawn on the desktop`, async ($, on) => {
      seat(on, alone(name, id))
      await $.turn.complete(turn())
      const row = rowOf(name, id)
      const problems: string[] = []
      for (const columns of WIDTHS) {
        // Drawn while a turn works, so the row has no action Buttons and the
        // track takes the columns this rule gives it; the M212 AC4 sweep
        // covers the row with them.
        const view = { ...at(columns), props: { ...at(columns).props, isWorking: true } }
        const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...view })) as Ui
        const [drawn] = await ui.findAll({ key: `${id}-row` })
        const { right } = layout(drawn)
        const svgs = below(drawn, 'Svg')
        const picked = (bandLines(row, columns, 5)[0].track as { columns: number }).columns
        const px = Math.min(360, picked * 7)
        if (svgs.length !== 1 || kids(right)[0] !== svgs[0]) {
          problems.push(`at ${columns}: ${svgs.length} Svg`)
        } else {
          const [svg] = svgs
          if (svg.props.width !== px || svg.props.height !== 18) problems.push(`at ${columns}: ${svg.props.width}×${svg.props.height}, not ${px}`)
          if (!String(svg.props.source).includes(`width="${px}" height="18"`)) problems.push(`at ${columns}: source width`)
        }
        const { room, need } = titleRoom(drawn, columns, row.title)
        if (room < need) problems.push(`at ${columns}: title room ${room} < ${need}`)
        await ui.unmount()
      }
      expect(firstFew(problems)).toEqual([])
    })
  }
})

describe('the terminal draws the braille track at every width from 40 to 200 columns (M206 AC3)', () => {
  // Without the open button, at the unit level: `close` 3 is the close gap
  // and label alone, and 5 adds the open glyph and its space.
  for (const id of IDS) {
    for (const title of TITLES) {
      for (const { status, checked, total } of COUNTS) {
        test(`built ${id} ${status} ${checked}/${total}, title of ${cols(title)} columns`, () => {
          const row = built(id, title, status, checked, total)
          const percent = percentOf(status, checked, total)
          const problems: string[] = []
          for (const close of [3, 5]) {
            for (const columns of WIDTHS) {
              const [line] = bandLines(row, columns, close)
              const where = `close ${close} at ${columns}`
              if (line.track === undefined) {
                problems.push(`${where}: no track`)
                continue
              }
              const spans = brailleSpans(line.track.flow, line.track.columns)
              for (const p of trackProblems(spans, status, checked, total, line.track.columns)) problems.push(`${where}: ${p}`)
              if (line.tail.map(s => s.text).join('') !== ` ${percent}%`) problems.push(`${where}: tail`)
              const room = columns - (cols(id) + 1) - 2 - line.track.columns - cols(` ${percent}%`) - close
              if (room < Math.min(cols(title), 10)) problems.push(`${where}: title room ${room}`)
            }
          }
          expect(firstFew(problems)).toEqual([])
        })
      }
    }
  }

  // With the open button: each fixture has a ROADMAP.
  for (const [name, id] of SWEPT) {
    test(`${name}: ${id} alone, drawn in the terminal`, async ($, on) => {
      expect(hasRoadmap(name)).toBe(true)
      seat(on, alone(name, id))
      await $.turn.complete(turn())
      const row = rowOf(name, id)
      const { checked, total } = countsOf(row)
      const percent = percentOf(row.status, checked, total)
      const problems: string[] = []
      for (const columns of WIDTHS) {
        const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...at(columns) })) as Ui
        const [drawn] = await ui.findAll({ key: `${id}-row` })
        const { right } = layout(drawn)
        const parts = trackParts(right)
        const children = kids(right)
        if (parts.length === 0 || parts.some((p, i) => children[i] !== p)) {
          problems.push(`at ${columns}: the track does not lead the right group`)
        } else {
          const spans = parts.map(spanOf)
          const width = spans.reduce((n, s) => n + cols(s.text), 0)
          for (const p of trackProblems(spans, row.status, checked, total, width)) problems.push(`at ${columns}: ${p}`)
          if (width < 12 || width > 52) problems.push(`at ${columns}: ${width} cells`)
        }
        expect(below(drawn, 'Svg')).toEqual([])
        if (rowText(drawn) !== `${id} ${row.title}  ${TRACK} ${percent}%`) problems.push(`at ${columns}: ${rowText(drawn)}`)
        const { room, need } = titleRoom(drawn, columns, row.title)
        if (room < need) problems.push(`at ${columns}: title room ${room} < ${need}`)
        await ui.unmount()
      }
      expect(firstFew(problems)).toEqual([])
    })
  }
})

// Snapshots the drawn band: every element of the mod's stack, as JSON.
async function drawing(ui: Ui): Promise<string> {
  return JSON.stringify(await ui.findAll({ key: 'cairn-stack' }))
}

describe('no skill row, and the idle row with no next label (M206 AC4)', () => {
  test('the cairn skill list holds the skill directories', () => {
    expect(SKILLS.length).toBe(10)
    expect([...CAIRN_SKILLS].sort()).toEqual([...SKILLS].sort())
  })

  for (const skill of [null, ...SKILLS]) {
    test(`no-active with ${skill ?? 'no skill'}: the idle row at 200 columns`, async ($, on) => {
      seat(on, copyOf('no-active'))
      await $.turn.complete(turn())
      if (skill !== null) await prompt($, skill)
      await mountEach(
        'no-active',
        at(200),
        async (ui, surface) => {
          expect(await rowKeys(ui)).toEqual(['idle-row'])
          const row = await firstRow(ui)
          idAndTitle(row, 'M021', 'Waiting to start')
          expect(textOf(row).includes('next')).toBe(false)
          expect(await lines(ui)).toEqual([IDLE_DRAWN['no-active'], ENGINE])
          const { right } = layout(row)
          const parts = trackParts(right)
          if (surface === 'desktop') {
            expect(parts.map(p => p.type)).toEqual(['Svg'])
            expect(parts[0].props.width).toBe(360)
            expect(String(parts[0].props.source)).toContain('>Planned<')
          } else {
            expect(parts.every(p => p.type === 'Text')).toBe(true)
            const spans = parts.map(spanOf)
            const pill = spans.filter(s => s.backgroundColor === BLUE)
            expect(pill.map(s => s.text.trim())).toEqual(['Planned'])
            for (const span of spans) if (span !== pill[0]) expect([span.text, span.backgroundColor]).toEqual([span.text, GROUND])
            expect(spans.reduce((n, s) => n + cols(s.text), 0)).toBe(52)
          }
          expect(rightText(right).trim()).toBe(`${TRACK} /milestone-implement M021`)
        },
        $,
      )
    })
  }

  for (const skill of SKILLS) {
    test(`with nothing workable, ${skill} draws the empty row with no action Buttons (M213)`, { plugins: [PROBE] }, async ($, on) => {
      seat(on, noneWorkable('no-active'))
      await $.turn.complete(turn())
      await prompt($, skill)
      await mountEach(
        'no-active',
        at(200),
        async ui => {
          await isEmptyRow(ui, false)
          expect(textOf((await ui.findAll({ type: 'Text' }))[0])).toBe('cairn hook: returned')
        },
        $,
      )
    })

    for (const surface of SURFACES) {
      test(`a press keeps the idle row hidden through ${skill}'s start and its end (${surface})`, async ($, on) => {
        seat(on, copyOf('no-active'))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await rowKeys(ui)).toEqual(['idle-row'])
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        await prompt($, skill)
        expect(await lines(ui)).toEqual([ENGINE])
        await $.classic.Stop(stopWith('empty'))
        expect(await lines(ui)).toEqual([ENGINE])
        expect(await hasCairn(ui)).toBe(false)
        await ui.unmount()
      })
    }
  }

  // A chapter call reads no file and changes no state: an edit made before
  // it shows only at the next turn end, which the last check proves the
  // edit does change.
  const CHAPTERED: { name: string; skill: string | null; key: string; edit: (files: Record<string, string>) => void }[] = [
    { name: 'single-in-progress', skill: null, key: 'M002-row', edit: files => (files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')) },
    { name: 'single-in-progress', skill: 'milestone-implement', key: 'M002-row', edit: files => (files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')) },
    { name: 'mixed', skill: 'milestone-review', key: 'M010-row', edit: files => (files[M010] = files[M010].replace('- [ ] AC3:', '- [x] AC3:')) },
    { name: 'no-active', skill: null, key: 'idle-row', edit: files => (files[ROADMAP] = files[ROADMAP].replace('| Waiting to start |', '| Still waiting |')) },
    { name: 'no-active', skill: 'milestone-plan', key: 'idle-row', edit: files => (files[ROADMAP] = files[ROADMAP].replace('| Waiting to start |', '| Still waiting |')) },
  ]
  for (const { name, skill, key, edit } of CHAPTERED) {
    for (const surface of SURFACES) {
      test(`a chapter call leaves ${name}'s ${key} under ${skill ?? 'no skill'} unchanged (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await rowKeys(ui)).toEqual([key])
        const before = await drawing(ui)
        edit(copy.files)
        await chapter($, 'T2: Write the command')
        expect(await drawing(ui)).toBe(before)
        await $.turn.complete(turn())
        expect(await drawing(ui)).not.toBe(before)
        await ui.unmount()
      })
    }
  }
})

// A turn end with a given reason, as the engine sends one.
function turnWith(reason: 'answer' | 'aborted' | 'refusal' | 'error', agentId?: string) {
  const base = { ...turn(), reason, isAborted: reason === 'aborted' }
  const refused = reason === 'refusal' ? { refusal: { category: null, explanation: null } } : {}
  return { ...base, ...refused, ...(agentId === undefined ? {} : { agentId }) }
}

// One background subagent in flight, as a Stop lists it.
const TASK = { id: 'b1', type: 'subagent', status: 'running', description: 'a background reviewer', agent_type: 'general-purpose' }

// A Stop as the engine raises it: its in-flight list empty, left out, or
// holding TASK, an agent id when it fires inside a subagent, and the
// session's crons when given (M210).
function stopWith(tasks: 'empty' | 'absent' | 'one', agentId?: string, crons?: (typeof ONE_SHOT)[]) {
  return {
    stop_hook_active: false,
    ...(tasks === 'absent' ? {} : { background_tasks: tasks === 'one' ? [TASK] : [] }),
    ...(agentId === undefined ? {} : { agent_id: agentId }),
    ...(crons === undefined ? {} : { session_crons: crons }),
  }
}

// A one-shot wakeup, as ScheduleWakeup schedules one, and a recurring cron,
// as `/loop` schedules one, as a Stop lists them (M210).
const ONE_SHOT = { id: 'c1', schedule: '30 14 4 10 *', recurring: false, prompt: 'resume the review' }
const RECURRING = { id: 'c2', schedule: '*/5 * * * *', recurring: true, prompt: '/loop check the deploy' }

// A prompt as the engine submits one: where it came from, and the running
// turn's id when it was typed over or delivered into that turn.
function submitWith(kind: 'composer' | 'bridge' | 'peer' | 'task-notification', turnId?: string) {
  return { text: `a ${kind} prompt`, wait: false, origin: { kind }, ...(turnId === undefined ? {} : { turnId }) }
}

// The step's one effect on the drawing since M206: on mixed, the M010
// review row shows while /milestone-review runs, and the M012 in-progress
// row once its step ends.
describe("a cairn skill's step ends at a main-loop Stop with nothing in flight (M201 AC1)", () => {
  for (const tasks of ['empty', 'absent'] as const) {
    test(`the review row gives way at a Stop whose list is ${tasks}`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $) => {
          await prompt($, 'milestone-review')
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.classic.Stop(stopWith(tasks))
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }

  // Each keep case ends with an empty-list Stop that does end the step, so a
  // kept row is the rule at work and not a step the mod never ends.
  const KEEPS: { name: string; act: ($, copy: Copy) => Promise<void> }[] = [
    { name: 'a Stop that lists one background task', act: $ => $.classic.Stop(stopWith('one')) },
    {
      name: 'a Stop with an empty list whose answer from beneath blocks',
      act: async ($, copy) => {
        copy.stopBlock = 'stop guard: work is still owed'
        expect((await $.classic.Stop(stopWith('empty'))).block).toBe('stop guard: work is still owed')
        copy.stopBlock = undefined
      },
    },
    { name: 'a Stop with an empty list and an agent id', act: $ => $.classic.Stop(stopWith('empty', 'a1')) },
    ...(['answer', 'aborted', 'refusal', 'error'] as const).map(reason => ({
      name: `a main-loop turn end with reason ${reason}`,
      act: async $ => {
        await $.turn.complete(turnWith(reason))
      },
    })),
    {
      name: "a subagent's turn end with reason answer",
      act: async $ => {
        await $.turn.complete(turnWith('answer', 'a1'))
      },
    },
  ]
  for (const { name, act } of KEEPS) {
    test(`${name} keeps the step`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $, copy) => {
          await prompt($, 'milestone-review')
          await act($, copy)
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.classic.Stop(stopWith('empty'))
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }
})

describe("a one-shot cron keeps a cairn skill's step through a Stop (M210 AC5)", () => {
  const CASES: { name: string; crons: (typeof ONE_SHOT)[] | undefined; keeps: boolean }[] = [
    { name: 'a one-shot cron', crons: [ONE_SHOT], keeps: true },
    { name: 'a one-shot and a recurring cron', crons: [ONE_SHOT, RECURRING], keeps: true },
    { name: 'a recurring cron', crons: [RECURRING], keeps: false },
    { name: 'an empty cron list', crons: [], keeps: false },
    { name: 'no cron list', crons: undefined, keeps: false },
  ]
  for (const { name, crons, keeps } of CASES) {
    test(`a Stop with no task in flight and ${name} ${keeps ? 'keeps' : 'ends'} the step`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $) => {
          await prompt($, 'milestone-review')
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.classic.Stop(stopWith('empty', undefined, crons))
          expect(await lines(ui)).toEqual(keeps ? [MIXED_REVIEW, ENGINE] : [SHOWN.mixed, ENGINE])
          await $.classic.Stop(stopWith('empty'))
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }
})

// The case where the prompt enters and a skill prompt of its turn sets the
// new step is "a typed cairn slash command's own skill prompt sets the new
// step" below.
describe('an idle typed prompt that a hook drops leaves the step (M210 AC6)', () => {
  for (const kind of ['composer', 'bridge'] as const) {
    test(`a dropped ${kind} prompt keeps the step, and one that enters ends it`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $, copy) => {
          await prompt($, 'milestone-review')
          await $.classic.Stop(stopWith('one'))
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          copy.dropSubmit = 'refused by a hook'
          expect((await $.prompt.submit(submitWith(kind))).drop).toBe('refused by a hook')
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          copy.dropSubmit = undefined
          await $.prompt.submit(submitWith(kind))
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }

  // M210 review: the refresh before `next` clears a hide made while
  // /milestone-review moved the band, so the drop puts that back too.
  test('a dropped prompt keeps a band hidden while /milestone-review runs', async ($, on) => {
    await eachSurface(
      'mixed',
      async (ui, $, copy) => {
        await prompt($, 'milestone-review')
        await $.classic.Stop(stopWith('one'))
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        copy.dropSubmit = 'refused by a hook'
        await $.prompt.submit(submitWith('composer'))
        expect(await lines(ui)).toEqual([ENGINE])
        // The same prompt entering ends the step, which shows the band.
        copy.dropSubmit = undefined
        await $.prompt.submit(submitWith('composer'))
        expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
      },
      $,
      on,
    )
  })
})

describe('an idle typed prompt ends a kept step, and a notice turn keeps it (M201 AC2)', () => {
  // Each case keeps the step through a Stop with one task in flight, then
  // raises one prompt and reads the row. `ends` is whether the step ends.
  const PROMPTS: { kind: 'composer' | 'bridge' | 'peer' | 'task-notification'; turnId?: string; ends: boolean }[] = [
    { kind: 'task-notification', ends: false },
    { kind: 'composer', ends: true },
    { kind: 'bridge', ends: true },
    { kind: 'peer', ends: false },
    { kind: 'composer', turnId: 't-running', ends: false },
  ]
  for (const { kind, turnId, ends } of PROMPTS) {
    test(`a ${kind} prompt${turnId === undefined ? '' : ' over a running turn'} ${ends ? 'ends' : 'keeps'} the kept step`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $, copy) => {
          await prompt($, 'milestone-review')
          await $.classic.Stop(stopWith('one'))
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.prompt.submit(submitWith(kind, turnId))
          // The origin and turn id the test gave reached the hooks beneath.
          expect(copy.submitted?.at(-1)).toEqual({ kind, turnId })
          expect(await lines(ui)).toEqual(ends ? [SHOWN.mixed, ENGINE] : [MIXED_REVIEW, ENGINE])
          await $.classic.Stop(stopWith('empty'))
        },
        $,
        on,
      )
    })
  }

  test("a typed cairn slash command's own skill prompt sets the new step", async ($, on) => {
    await eachSurface(
      'mixed',
      async (ui, $, copy) => {
        await prompt($, 'milestone-implement')
        await $.classic.Stop(stopWith('one'))
        expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        // The slash command expands while its prompt goes down the chain.
        copy.beforeSubmit = () => prompt($, 'milestone-review')
        await $.prompt.submit(submitWith('composer'))
        copy.beforeSubmit = undefined
        expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
        await $.classic.Stop(stopWith('empty'))
      },
      $,
      on,
    )
  })

  // The engine expands a typed slash command before it raises the
  // command's prompt (M201 T4 live look), so the prompt finds the new step
  // already set and keeps it.
  test('a typed cairn slash command expanded before its prompt keeps its own step', async ($, on) => {
    await eachSurface(
      'mixed',
      async (ui, $) => {
        await prompt($, 'milestone-implement')
        await $.classic.Stop(stopWith('one'))
        await prompt($, 'milestone-review')
        await $.prompt.submit(submitWith('composer'))
        expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
        await $.classic.Stop(stopWith('empty'))
        expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
      },
      $,
      on,
    )
  })

  // A skill the model loads mid-turn is expanded too. A Stop or a turn end
  // after it means a later typed prompt did not bring it, so that prompt
  // ends the step. A skill that is not cairn's sets no mark.
  const LATER: { name: string; act: ($) => Promise<unknown> }[] = [
    {
      name: 'a cairn skill prompt and a Stop with one task in flight',
      act: async $ => {
        await prompt($, 'milestone-review')
        await $.classic.Stop(stopWith('one'))
      },
    },
    {
      name: 'a cairn skill prompt and an interrupted turn',
      act: async $ => {
        await prompt($, 'milestone-review')
        await $.turn.complete(turnWith('aborted'))
      },
    },
    { name: "a skill prompt that is not cairn's", act: $ => $.skill.prompt({ skill: 'simplify', text: 'the simplify prompt' }) },
  ]
  for (const { name, act } of LATER) {
    test(`an idle typed prompt after ${name} ends a kept step`, async ($, on) => {
      await eachSurface(
        'mixed',
        async (ui, $) => {
          await prompt($, 'milestone-review')
          await $.classic.Stop(stopWith('one'))
          await act($)
          expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
          await $.prompt.submit(submitWith('composer'))
          expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
        },
        $,
        on,
      )
    })
  }
})

// The mixed fixture cut to one review row (M010) and one in-progress row
// (M012).
function reviewAndImplement(): Copy {
  const copy = copyOf('mixed')
  for (const path of Object.keys(copy.files)) {
    if (path.endsWith('cairn/ROADMAP.md')) {
      copy.files[path] = copy.files[path]
        .split('\n')
        .filter(line => !line.startsWith('| M013 ') && !line.startsWith('| M014 '))
        .join('\n')
    }
  }
  return copy
}

describe('a review row stays shown through a background wait (M201 AC3)', () => {
  for (const surface of SURFACES) {
    test(`the review row stays through the wait and the notice turn (${surface})`, async ($, on) => {
      seat(on, reviewAndImplement())
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
      await prompt($, 'milestone-review')
      expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      await $.classic.Stop(stopWith('one'))
      expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      await $.prompt.submit(submitWith('task-notification'))
      expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      await $.turn.complete(turnWith('answer'))
      expect(await lines(ui)).toEqual([MIXED_REVIEW, ENGINE])
      // The closing Stop with nothing in flight hands the band back to the
      // in-progress row.
      await $.classic.Stop(stopWith('empty'))
      expect(await lines(ui)).toEqual([SHOWN.mixed, ENGINE])
      await ui.unmount()
    })
  }
})

const M021 = '/cairn/milestones/M021-wait.md'
// Each case presses the close button on no-active's idle row, ends a turn
// with nothing changed, makes its change, and asserts whether the band
// shows, by the keys of the rows it draws.
type IdleClose = { name: string; change: ($, files: Record<string, string>) => Promise<void>; shown: string[] | null }

const IDLE_CLOSES: IdleClose[] = [
  {
    name: 'a checked box keeps it hidden',
    change: async ($, files) => {
      files[M021] = files[M021].replace('- [ ] T1:', '- [x] T1:')
      await $.turn.complete(turn())
    },
    shown: null,
  },
  {
    name: 'an edited title keeps it hidden',
    change: async ($, files) => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start |', '| Still waiting to start |')
      await $.turn.complete(turn())
    },
    shown: null,
  },
  {
    name: 'a new next workable milestone shows it',
    change: async ($, files) => {
      files[ROADMAP] = files[ROADMAP].replace('| M020 | Shipped |', '| M022 | Jumps the queue | planned | — | high | milestones/M022-jump.md |\n| M020 | Shipped |')
      await $.turn.complete(turn())
    },
    shown: ['idle-row'],
  },
  {
    name: 'a row that becomes in-progress shows it',
    change: async ($, files) => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
      await $.turn.complete(turn())
    },
    shown: ['M021-row'],
  },
  {
    name: 'a cairn skill that starts keeps it hidden (M206)',
    change: async $ => {
      await prompt($, 'milestone')
    },
    shown: null,
  },
]

describe("a press stores the idle row's id (M199 AC4)", () => {
  for (const { name, change, shown } of IDLE_CLOSES) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf('no-active')
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await rowKeys(ui)).toEqual(['idle-row'])
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual([ENGINE])
        await change($, copy.files)
        if (shown === null) {
          expect(await lines(ui)).toEqual([ENGINE])
        } else {
          expect(await rowKeys(ui)).toEqual(shown)
        }
        await ui.unmount()
      })
    }
  }

  // A skill draws nothing, so over a milestone row its start and its end
  // keep a hidden band hidden, but for /milestone-review moving the band to
  // another row (M206 review).
  for (const surface of SURFACES) {
    test(`over a milestone row, a skill's start and its end keep the band hidden (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-plan')
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'hotfix')
      expect(await lines(ui)).toEqual([ENGINE])
      await $.classic.Stop(stopWith('empty'))
      expect(await lines(ui)).toEqual([ENGINE])
      await ui.unmount()
    })

    test(`over mixed, /milestone-review moving the band to the review row shows it again (${surface})`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      const plain = await rowKeys(ui)
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'milestone-implement')
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'milestone-review')
      const reviewed = await rowKeys(ui)
      expect(reviewed).toEqual(['M010-row'])
      expect(reviewed).not.toEqual(plain)
      await ui.unmount()
    })
  }

  // A write under a `cairn/` directory reads the files again inside a turn,
  // as a chapter did before M206 (M206 review). The tools answer beneath
  // the mod, so nothing is written.
  const WRITES: { name: string; tool: string; path: string; answer: object; reads: boolean }[] = [
    { name: 'an Edit of the milestone file', tool: 'Edit', path: M002, answer: { result: 'ok' }, reads: true },
    { name: 'a Write of the milestone file', tool: 'Write', path: M002, answer: { result: 'ok' }, reads: true },
    { name: 'a MultiEdit of the milestone file', tool: 'MultiEdit', path: M002, answer: { result: 'ok' }, reads: true },
    { name: 'an Edit outside cairn/', tool: 'Edit', path: '/src/main.ts', answer: { result: 'ok' }, reads: false },
    { name: 'a refused Edit of the milestone file', tool: 'Edit', path: M002, answer: { deny: 'refused beneath' }, reads: false },
    { name: 'a failed Edit of the milestone file', tool: 'Edit', path: M002, answer: { result: 'failed', isError: true }, reads: false },
  ]
  for (const { name, tool, path, answer, reads } of WRITES) {
    test(`${name} ${reads ? 'reads' : 'does not read'} the files again`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      on('tool.call', { tool }, async () => answer)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
      const before = await lines(ui)
      expect(before[0].endsWith(' 44%')).toBe(true)
      copy.files[M002] = copy.files[M002].replace('- [ ] T2:', '- [x] T2:')
      await $.tool.call({ tool, file_path: path })
      const after = await lines(ui)
      if (reads) {
        expect(after[0].endsWith(' 55%')).toBe(true)
      } else {
        expect(after).toEqual(before)
      }
      await ui.unmount()
    })
  }

  test('the new next milestone is the one the band then names', async ($, on) => {
    const copy = copyOf('no-active')
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
    await ui.press({ key: 'cairn-close' })
    await IDLE_CLOSES[2].change($, copy.files)
    expect(await lines(ui)).toEqual(['M022 Jumps the queue  [track] /milestone-implement M022', ENGINE])
    await ui.unmount()
  })
})

// M204: the flow track, one flow of plan, implement, and review.

// The flow of each fixture whose row drawn with no skill is a milestone row
// with readable counts, written out by hand: the three fills as
// checked/total, the pill, its short text, and the percent (M204 AC1, M206).
const FLOWS: Record<string, { fills: [string, string, string]; pill: string; short: string; percent: number }> = {
  'long-title': { fills: ['1/1', '1/2', '0/1'], pill: 'Implement 1/2', short: '1/2', percent: 50 },
  mixed: { fills: ['1/1', '0/1', '0/1'], pill: 'no tasks', short: 'none', percent: 33 },
  'nested-first': { fills: ['1/1', '1/3', '0/1'], pill: 'Implement 1/3', short: '1/3', percent: 44 },
  'pane-full': { fills: ['1/1', '1/3', '0/1'], pill: 'Implement 1/3', short: '1/3', percent: 44 },
  'single-in-progress': { fills: ['1/1', '1/3', '0/1'], pill: 'Implement 1/3', short: '1/3', percent: 44 },
  'six-active': { fills: ['1/1', '1/2', '0/1'], pill: 'Implement 1/2', short: '1/2', percent: 50 },
  subdirectory: { fills: ['1/1', '2/2', '0/1'], pill: 'Implement 2/2', short: '2/2', percent: 66 },
  'unlabeled-item': { fills: ['1/1', '1/3', '0/1'], pill: 'Implement 1/3', short: '1/3', percent: 44 },
  'wide-title': { fills: ['1/1', '1/1', '1/2'], pill: 'Review 1/2', short: '1/2', percent: 83 },
  widest: { fills: ['1/1', '99/100', '0/1'], pill: 'Implement 99/100', short: '99/100', percent: 66 },
}

const fillText = (flow: Flow) => flow.fills.map(f => `${f.num}/${f.den}`)

describe('the flow model gives three fills, a pill, and a percent (M204 AC1)', () => {
  test('the table holds every fixture whose drawn row has readable counts', () => {
    const domain = Object.keys(FIXTURES).filter(name => {
      const id = shownId(name)
      return id !== null && rowOf(name, id).tasksTotal !== null
    })
    expect(domain.length).toBeGreaterThan(0)
    expect([...domain].sort()).toEqual(Object.keys(FLOWS).sort())
  })

  for (const [name, want] of Object.entries(FLOWS)) {
    test(`${name}: the drawn row's flow`, () => {
      const flow = flowOf(rowOf(name, shownId(name) as string)) as Flow
      expect([fillText(flow), flow.pill, flow.short, flow.percent]).toEqual([want.fills, want.pill, want.short, want.percent])
    })
  }

  test('a section of zero items is empty, its pill names it, and its short text is none', () => {
    const tasks = flowOf(rowOf('states-implement', 'M042')) as Flow
    expect([fillText(tasks), tasks.pill, tasks.short, tasks.percent]).toEqual([['1/1', '0/1', '0/1'], 'no tasks', 'none', 33])
    const criteria = flowOf(rowOf('states-review', 'M052')) as Flow
    expect([fillText(criteria), criteria.pill, criteria.short, criteria.percent]).toEqual([['1/1', '1/1', '0/1'], 'no criteria', 'none', 66])
  })

  test('an all-checked review row reads 100%, and an all-checked implement row does not', () => {
    const review = flowOf(rowOf('states-review', 'M053')) as Flow
    expect([fillText(review), review.pill, review.percent]).toEqual([['1/1', '1/1', '2/2'], 'Review 2/2', 100])
    const implement = flowOf(rowOf('states-implement', 'M043')) as Flow
    expect([implement.pill, implement.percent]).toEqual(['Implement 3/3', 66])
  })

  test('a row whose file cannot be read has no flow', () => {
    expect(flowOf(rowOf('missing-file', 'M004'))).toBeNull()
  })

  test('the idle row: plan full, no percent', () => {
    const flow = idleFlow()
    expect([fillText(flow), flow.pill, flow.short, flow.percent]).toEqual([['1/1', '0/1', '0/1'], 'Planned', 'Planned', null])
  })
})

// The speck gray, written out by hand.
const SPECK_GRAY = 'rgb(160,160,160)'
const STEPS = [null, 'milestone-review', 'milestone-implement', 'hotfix'] as const

// What a track draws, by the share of the flow: `index` is the active
// segment (0 plan, 1 implement, 2 review), `fill` its fill, `items` and
// `checked` its item counts for the ticks, and `pill` and `short` its pill
// texts. Pixels follow from a width.
type Expected = {
  pill: string
  short: string
  index: number
  fill: number
  items: number
  checked: number
  color: string
  alt: string[]
  right: string
}

const headAt = (want: Expected, width: number) => (width * (want.index + want.fill)) / 3

// The active segment's inner item edges k with checked < k < n, when the
// items are 6 pixels apart or more.
function ticksAt(want: Expected, width: number): number[] {
  const third = width / 3
  const step = third / want.items
  if (want.items < 2 || step < 6) return []
  return Array.from({ length: want.items - 1 }, (_, i) => i + 1)
    .filter(k => k > want.checked)
    .map(k => third * want.index + step * k)
}

// What a row in the flow draws, from the fixture's counts, or null for a
// row outside the flow. Derived here, never from band.ts or track.ts. The
// idle row draws whatever skill runs (M206).
function expectedFlow(name: string, skill: string | null): Expected | null {
  const id = shownId(name, skill)
  if (id === null) {
    const idle = idleId(name)
    if (idle === null) return null
    return { pill: 'Planned', short: 'Planned', index: 0, fill: 1, items: 0, checked: 0, color: BLUE, alt: ['plan'], right: `/milestone-implement ${idle}` }
  }
  const row = rowOf(name, id)
  if (row.tasksTotal === null || row.criteriaTotal === null) return null
  const { checked, total } = countsOf(row)
  const percent = percentOf(row.status, checked, total)
  const isTasks = row.status === 'in-progress'
  const noun = isTasks ? 'tasks' : 'criteria'
  const counts = total === 0 ? `no ${noun}` : `${checked}/${total}`
  return {
    pill: total === 0 ? `no ${noun}` : `${isTasks ? 'Implement' : 'Review'} ${checked}/${total}`,
    short: total === 0 ? 'none' : `${checked}/${total}`,
    index: isTasks ? 1 : 2,
    fill: total === 0 ? 0 : checked / total,
    items: total,
    checked,
    color: isTasks ? ORANGE : GREEN,
    alt: [isTasks ? 'implement' : 'review', counts, `${percent}%`],
    right: `${percent}%`,
  }
}

// Every speck cell's left edge and width, with the color it draws in.
function specksOf(source: string): { x: number; w: number; fill: string; kind: string }[] {
  return [...source.matchAll(/<path class="specks" data-color="(\w+)" d="([^"]*)" fill="([^"]+)"/g)].flatMap(m =>
    [...m[2].matchAll(/M([\d.]+) [\d.]+h([\d.]+)/g)].map(cell => ({
      x: Number(cell[1]),
      w: Number(cell[2]),
      fill: m[3],
      kind: m[1],
    })),
  )
}

// Checks an SVG track `width` pixels wide against what it should draw, its
// pill showing `pill`.
function checkSource(source: string, want: Expected, width: number, pill: string) {
  const head = headAt(want, width)
  // Specks only between the left edge and the head, in gray or the active
  // phase's hue, at least one in the hue.
  const specks = specksOf(source)
  expect(specks.some(speck => speck.fill === want.color)).toBe(true)
  for (const speck of specks) {
    expect([speck.x, speck.x >= 0 && speck.x + speck.w <= head + 0.005]).toEqual([speck.x, true])
    expect([speck.kind, speck.fill]).toEqual([speck.kind, speck.kind === 'gray' ? SPECK_GRAY : want.color])
  }
  // The item ticks, at the active segment's item edges past the head.
  const ticks = [...source.matchAll(/<rect class="tick" x="([\d.-]+)"/g)].map(m => Number(m[1]) + 0.5)
  const wantTicks = ticksAt(want, width)
  expect(ticks.length).toBe(wantTicks.length)
  ticks.forEach((x, i) => expect(Math.abs(x - wantTicks[i])).toBeLessThan(0.01))
  // The two phase-edge marks, 1 unit wide, centered on the thirds.
  const edges = [...source.matchAll(/<rect class="edge" x="([\d.]+)"/g)].map(m => Number(m[1]) + 0.5)
  expect(edges.length).toBe(2)
  edges.forEach((x, i) => expect(Math.abs(x - (width * (i + 1)) / 3)).toBeLessThan(0.01))
  // The pill: in the active phase's hue, inside the track, with its text.
  const box = /<rect class="pill" x="([\d.]+)"[^>]*width="([\d.]+)"[^>]*fill="([^"]+)"/.exec(source) as RegExpExecArray
  const [left, w] = [Number(box[1]), Number(box[2])]
  expect(left).toBeGreaterThanOrEqual(0)
  expect(left + w).toBeLessThanOrEqual(width + 0.005)
  // Its right edge at the head plus 6, clamped to 1 inside either end.
  const right = Math.min(Math.max(head + 6, w + 1), width - 1)
  expect(Math.abs(left + w - right)).toBeLessThan(0.02)
  expect(box[3]).toBe(want.color)
  const text = /<text class="pill-text"[^>]*>(.*?)<\/text>/.exec(source)?.[1] ?? ''
  const parts = [...text.matchAll(/<tspan[^>]*>([^<]*)<\/tspan>/g)].map(m => m[1])
  expect(parts.join(' ')).toBe(pill)
}

describe('the desktop draws the track as an Svg, and the terminal as braille (M204 AC2, M206)', () => {
  for (const name of Object.keys(FIXTURES)) {
    for (const skill of STEPS) {
      test(`${name} under ${skill ?? 'no skill'}`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        if (skill !== null) await prompt($, skill)
        const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...at(200) })) as Ui
        const terminal = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...at(200) })) as Ui
        const want = expectedFlow(name, skill)
        const svgs = await ui.findAll({ type: 'Svg' })
        expect(await terminal.findAll({ type: 'Svg' })).toEqual([])
        // The rows read the same on both surfaces, the track as TRACK.
        expect(await lines(ui)).toEqual(await lines(terminal))
        if (want === null) {
          expect(svgs).toEqual([])
          if (await hasCairn(terminal)) expect(trackParts(layout(await firstRow(terminal)).right)).toEqual([])
          await terminal.unmount()
          await ui.unmount()
          return
        }
        expect(svgs.length).toBe(1)
        const [svg] = svgs
        expect([svg.props.width, svg.props.height]).toEqual([360, 18])
        checkSource(svg.props.source as string, want, 360, want.pill)
        const alt = svg.props.alt as string
        // The alt begins with the phase, then names the counts and percent.
        expect(alt.startsWith(`${want.alt[0]} `) || alt === want.alt[0]).toBe(true)
        for (const part of want.alt.slice(1)) expect([part, alt.includes(part)]).toEqual([part, true])
        // The right group: the track, then the percent or the idle command,
        // then the dim close button.
        const right = kids(await firstRow(ui))[1]
        expect(kids(right)[0].type).toBe('Svg')
        expect(rightText(right).trim()).toBe(`${TRACK} ${want.right}`)
        const button = await closeButton(ui)
        expect([button.props.label, button.props.dimColor]).toEqual(['✕', true])
        // The terminal's track: braille cells on the ground, and the pill in
        // the phase's hue.
        const cells = trackParts(layout(await firstRow(terminal)).right).map(spanOf)
        const pills = cells.filter(s => s.backgroundColor === want.color)
        // A pill that takes more than a third of the 52 cells shows its
        // short text.
        expect(pills.map(s => s.text.trim())).toEqual([cols(` ${want.pill} `) * 3 <= 52 ? want.pill : want.short])
        for (const span of cells) if (span !== pills[0]) expect([span.text, span.backgroundColor]).toEqual([span.text, GROUND])
        await terminal.unmount()
        await ui.unmount()
      })
    }
  }

  // Rows built directly, for item counts no fixture has: the 6-pixel
  // spacing at n = 20 (6 apart) and n = 21 (under 6), and heads whose x
  // rounds near an item edge (7/9 tasks, 11/18 criteria). Each draws at the
  // full 360 pixels, at 200, and at the least 84 (12 columns of 7 pixels),
  // where the pill shows its short text.
  const BUILT: { name: string; row: BandRow; want: Expected; ticks: number }[] = [
    { name: '20 tasks, 5 checked', row: built('M900', 'Built', 'in-progress', 5, 20), want: { pill: 'Implement 5/20', short: '5/20', index: 1, fill: 5 / 20, items: 20, checked: 5, color: ORANGE, alt: [], right: '' }, ticks: 14 },
    { name: '21 tasks, 5 checked', row: built('M900', 'Built', 'in-progress', 5, 21), want: { pill: 'Implement 5/21', short: '5/21', index: 1, fill: 5 / 21, items: 21, checked: 5, color: ORANGE, alt: [], right: '' }, ticks: 0 },
    { name: '9 tasks, 7 checked', row: built('M900', 'Built', 'in-progress', 7, 9), want: { pill: 'Implement 7/9', short: '7/9', index: 1, fill: 7 / 9, items: 9, checked: 7, color: ORANGE, alt: [], right: '' }, ticks: 1 },
    { name: '18 criteria, 11 checked', row: built('M900', 'Built', 'review', 11, 18), want: { pill: 'Review 11/18', short: '11/18', index: 2, fill: 11 / 18, items: 18, checked: 11, color: GREEN, alt: [], right: '' }, ticks: 6 },
  ]
  for (const { name, row, want, ticks } of BUILT) {
    test(`a built row: ${name}`, () => {
      expect(ticksAt(want, 360).length).toBe(ticks)
      const flow = flowOf(row) as Flow
      checkSource(trackSvg(flow), want, 360, want.pill)
      checkSource(trackSvg(flow, 360), want, 360, want.pill)
      checkSource(trackSvg(flow, 200), want, 200, want.short)
      checkSource(trackSvg(flow, 84), want, 84, want.short)
    })
  }

  test('the idle track at its least width', () => {
    const want = expectedFlow('no-active', null) as Expected
    checkSource(trackSvg(idleFlow(), 84), want, 84, 'Planned')
  })
})

// The command and argument a press of the next-step Button runs, read from
// the fixture's `next`, held by test_status_fixtures.py to
// scripts/cairn_next.py's `recommend`: `cairn:` and the command without its
// slash, and the milestone id (M212 AC1).
function nextRun(name: string): { command: string; args: string } {
  const next = FIXTURES[name].next as { command: string; id: string }
  return { command: `cairn:${next.command.slice(1)}`, args: next.id }
}
const STATUS_RUN = { command: 'cairn:milestone', args: '' }

// The action Buttons' keys as drawn.
async function actionKeys(ui: Ui): Promise<string[]> {
  return (await ui.findAll({ type: 'Button' })).map(keyOf).filter((k): k is string => ACTION_KEYS.includes(k ?? ''))
}

const PRESSED = ['single-in-progress', 'states-review', 'idle-order', 'mixed']
// The next-step Button's label by the next step's action, written out by
// hand.
const LABELS: Record<string, string> = { resume: 'Resume', review: 'Review', implement: 'Start' }

describe('the next-step and status Buttons run their commands (M212 AC1)', () => {
  test('the pressed fixtures cover resume, review, and start, and a band row that is not the next step', () => {
    expect(PRESSED.map(name => FIXTURES[name].next?.action)).toEqual(['resume', 'review', 'implement', 'review'])
    // On mixed the band shows M012 and the next step names M010.
    expect([shownId('mixed'), FIXTURES.mixed.next?.id]).toEqual(['M012', 'M010'])
  })

  for (const name of PRESSED) {
    for (const surface of SURFACES) {
      test(`${name}: each press runs its command (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await actionKeys(ui)).toEqual(ACTION_KEYS)
        const [next] = await ui.findAll({ key: 'cairn-next' })
        const [status] = await ui.findAll({ key: 'cairn-status' })
        expect([next.props.label, status.props.label]).toEqual([LABELS[FIXTURES[name].next?.action as string], 'Status'])
        await ui.press({ key: 'cairn-next' })
        expect(copy.commands).toEqual([nextRun(name)])
        await ui.press({ key: 'cairn-status' })
        expect(copy.commands).toEqual([nextRun(name), STATUS_RUN])
        expect([copy.fills ?? [], copy.toasts ?? []]).toEqual([[], []])
        await ui.unmount()
      })
    }
  }
})

// What a press of `Plan` runs, written out by hand (M213 AC3).
const PLAN_RUN = { command: 'cairn:milestone-plan', args: '' }

describe('the empty row carries Plan and Status, and a press runs planning (M213 AC2, AC3)', () => {
  for (const name of EMPTY_FIXTURES) {
    for (const surface of SURFACES) {
      test(`${name}: Plan runs /cairn:milestone-plan with no arguments, and Status runs /cairn:milestone (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await actionKeys(ui)).toEqual(ACTION_KEYS)
        const [next] = await ui.findAll({ key: 'cairn-next' })
        expect([next.props.label, next.props.variant]).toEqual(['Plan', 'secondary'])
        await ui.press({ key: 'cairn-next' })
        expect(copy.commands).toEqual([PLAN_RUN])
        await ui.press({ key: 'cairn-status' })
        expect(copy.commands).toEqual([PLAN_RUN, STATUS_RUN])
        expect([copy.fills ?? [], copy.toasts ?? []]).toEqual([[], []])
        await ui.unmount()
      })
    }
  }

  for (const surface of SURFACES) {
    test(`a running cairn skill and a working turn hide Plan and Status on the empty row (${surface})`, async ($, on) => {
      seat(on, copyOf('all-waiting'))
      await $.turn.complete(turn())
      const working = { ...BAND, props: { ...BAND.props, isWorking: true } }
      const busy = (await $.ui.mount({ plugin: 'cairn', surface, ...working })) as Ui
      await isEmptyRow(busy, false)
      await busy.unmount()
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await isEmptyRow(ui, true)
      await prompt($, 'milestone')
      await isEmptyRow(ui, false)
      await $.classic.Stop(stopWith('empty'))
      await isEmptyRow(ui, true)
      await ui.unmount()
    })

    test(`a refused Plan run appends /cairn:milestone-plan to the prompt box and toasts (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      copy.runThrows = 'no such command here'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-next' })
      expect(copy.commands).toEqual([PLAN_RUN])
      expect(copy.fills).toEqual([{ text: '/cairn:milestone-plan', mode: 'append' }])
      expect(copy.toasts).toEqual([`cairn: ${NO_RUN} (/cairn:milestone-plan)`])
      await ui.unmount()
    })

    test(`a Plan press while a run is in flight reaches no second run (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      const first = ui.press({ key: 'cairn-next' })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([PLAN_RUN])
        await ui.press({ key: 'cairn-next' })
        await ui.press({ key: 'cairn-status' })
        expect(copy.commands).toEqual([PLAN_RUN])
      } finally {
        release()
        await first
      }
      copy.runHold = undefined
      await ui.press({ key: 'cairn-next' })
      expect(copy.commands).toEqual([PLAN_RUN, PLAN_RUN])
      await ui.unmount()
    })
  }
})

describe('the close button hides the empty row until a milestone is workable (M213 AC4)', () => {
  const AW = '/cairn/ROADMAP.md'
  for (const surface of SURFACES) {
    test(`a press, a refresh, a waiting row, then a workable row (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['plan-row'])
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      // A planned row waiting on the blocked M092 is not workable.
      copy.files[AW] = copy.files[AW].replace('| M001 | Shipped |', '| M094 | Also waits | planned | M092 | normal | milestones/M094-waits.md |\n| M001 | Shipped |')
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([ENGINE])
      // A planned row whose one dependency is done is workable.
      copy.files[AW] = copy.files[AW].replace('| M001 | Shipped |', '| M095 | Ready now | planned | M001 | normal | milestones/M095-ready.md |\n| M001 | Shipped |')
      await $.turn.complete(turn())
      expect(await rowKeys(ui)).toEqual(['idle-row'])
      expect((await lines(ui))[0].startsWith('M095 Ready now  ')).toBe(true)
      await ui.unmount()
    })

    // README: a hidden empty row also shows again when a milestone becomes
    // active, and a cairn skill's start and end keep it hidden (M213 review).
    test(`a skill keeps a hidden empty row hidden, and an active row shows the band (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await rowKeys(ui)).toEqual(['plan-row'])
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await prompt($, 'milestone-plan')
      expect(await lines(ui)).toEqual([ENGINE])
      await $.classic.Stop(stopWith('empty'))
      expect(await lines(ui)).toEqual([ENGINE])
      copy.files[AW] = copy.files[AW].replace('| Blocked outside | blocked |', '| Blocked outside | in-progress |')
      await $.turn.complete(turn())
      expect(await rowKeys(ui)).toEqual(['M092-row'])
      await ui.unmount()
    })
  }
})

describe('the action Buttons hide while a cairn skill runs or a turn works (M212 AC2)', () => {
  for (const surface of SURFACES) {
    test(`a running cairn skill hides them, and its end brings them back (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await prompt($, 'milestone-implement')
      expect(await actionKeys(ui)).toEqual([])
      expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual(['cairn-open', 'cairn-close'])
      await $.classic.Stop(stopWith('empty'))
      expect(await actionKeys(ui)).toEqual(ACTION_KEYS)
      await ui.unmount()
    })

    test(`a working turn hides them (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const working = { ...BAND, props: { ...BAND.props, isWorking: true } }
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...working })) as Ui
      expect(await actionKeys(ui)).toEqual([])
      expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual(['cairn-open', 'cairn-close'])
      await ui.unmount()
    })
  }
})

// The engine skips a hook that throws, so the run goes on to the bottom of
// the chain, which rejects with this message: the rejection the toast names.
const NO_RUN = 'no implementation for command.run'

describe('a refused run appends the command line to the prompt box and toasts (M212 AC3)', () => {
  for (const surface of SURFACES) {
    test(`each Button falls back when the run throws (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      copy.runThrows = 'no such command here'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-next' })
      expect(copy.fills).toEqual([{ text: '/cairn:milestone-implement M002', mode: 'append' }])
      expect(copy.toasts?.length).toBe(1)
      // The press reached the run before it fell back.
      expect(copy.commands).toEqual([nextRun('single-in-progress')])
      expect(copy.toasts?.[0]).toBe(`cairn: ${NO_RUN} (/cairn:milestone-implement M002)`)
      await ui.press({ key: 'cairn-status' })
      expect(copy.fills).toEqual([
        { text: '/cairn:milestone-implement M002', mode: 'append' },
        { text: '/cairn:milestone', mode: 'append' },
      ])
      expect(copy.toasts?.length).toBe(2)
      expect(copy.toasts?.[1]).toBe(`cairn: ${NO_RUN} (/cairn:milestone)`)
      await ui.unmount()
    })
  }
})

// A press of a drawing made before a cairn skill started cannot be staged
// here: the kit presses the current drawing, which no longer has the
// Buttons. The press's own step check is untested for that reason.
describe('a press while a run is in flight does nothing (M212 review)', () => {
  for (const surface of SURFACES) {
    test(`a second press during a held run reaches no second run (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      const first = ui.press({ key: 'cairn-next' })
      try {
        // Let the first press reach the held run, as untilHeld waits.
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([nextRun('single-in-progress')])
        await ui.press({ key: 'cairn-next' })
        await ui.press({ key: 'cairn-status' })
        expect(copy.commands).toEqual([nextRun('single-in-progress')])
      } finally {
        release()
        await first
      }
      // With the run done, a press runs again.
      copy.runHold = undefined
      await ui.press({ key: 'cairn-status' })
      expect(copy.commands).toEqual([nextRun('single-in-progress'), STATUS_RUN])
      await ui.unmount()
    })
  }
})

// A drawn element as plain data, its function props left out, so two
// drawings of one row compare whole.
function shapeOf(node: unknown): unknown {
  if (node === null || typeof node !== 'object') return node
  const el = node as Element
  const props = Object.fromEntries(Object.entries(el.props ?? {}).filter(([, v]) => typeof v !== 'function'))
  return { type: el.type, key: keyOf(el), props, children: (el.children ?? []).map(shapeOf) }
}

describe('the action Buttons give way before the title loses its room (M212 AC4)', () => {
  // The cases of the M197 sweep: every fixture's row alone, the idle rows,
  // and the empty rows (M213 AC2).
  const CASES: { name: string; key: string; copy: () => Copy }[] = [
    ...Object.keys(FIXTURES).flatMap(name => FIXTURES[name].rows.map(row => ({ name, key: `${row.id}-row`, copy: () => alone(name, row.id) }))),
    ...Object.keys(IDLE_DRAWN).map(name => ({ name, key: 'idle-row', copy: () => copyOf(name) })),
    ...EMPTY_FIXTURES.map(name => ({ name, key: 'plan-row', copy: () => copyOf(name) })),
  ]
  test('the sweep has cases, the empty rows among them, and covers 40 to 200 columns', () => {
    expect(CASES.length).toBeGreaterThan(20)
    expect(CASES.filter(c => c.key === 'plan-row').map(c => c.name)).toEqual(EMPTY_FIXTURES)
    expect([WIDTHS.length, WIDTHS[0], WIDTHS[160]]).toEqual([161, 40, 200])
  })

  for (const { name, key, copy } of CASES) {
    test(`${name}: ${key}`, async ($, on) => {
      seat(on, copy())
      await $.turn.complete(turn())
      const problems: string[] = []
      for (const surface of SURFACES) {
        const shown: number[] = []
        for (const columns of WIDTHS) {
          const view = at(columns)
          const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...view })) as Ui
          const [row] = await ui.findAll({ key })
          const acts = await actionKeys(ui)
          await ui.unmount()
          if (acts.length === 2) {
            shown.push(columns)
            const { room, need } = titleRoom(row, columns, textOf(layout(row).text))
            if (room < need) problems.push(`${surface} at ${columns}: room ${room} < ${need}`)
          } else if (acts.length === 0) {
            const working = { ...view, props: { ...view.props, isWorking: true } }
            const still = (await $.ui.mount({ plugin: 'cairn', surface, ...working })) as Ui
            const [plain] = await still.findAll({ key })
            await still.unmount()
            if (JSON.stringify(shapeOf(row)) !== JSON.stringify(shapeOf(plain))) problems.push(`${surface} at ${columns}: tree differs`)
          } else {
            problems.push(`${surface} at ${columns}: ${acts.join(', ')} alone`)
          }
        }
        const run = shown.length === 0 ? [] : WIDTHS.filter(c => c >= shown[0])
        if (JSON.stringify(shown) !== JSON.stringify(run) || !shown.includes(120)) {
          problems.push(`${surface}: Buttons at ${shown[0] ?? 'no width'} to ${shown[shown.length - 1] ?? '-'}, ${shown.length} widths`)
        }
        // The empty row's text keeps its 10 columns beside the Buttons at
        // every width from 37 (its 27 fixed columns and 10), so the Buttons
        // show at every swept width (M213 AC2).
        if (key === 'plan-row' && shown.length !== WIDTHS.length) problems.push(`${surface}: empty row Buttons at ${shown.length} of ${WIDTHS.length} widths`)
      }
      expect(firstFew(problems)).toEqual([])
    })
  }
})
