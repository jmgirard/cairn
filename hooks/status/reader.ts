// The status band's reader: which milestones are active, how many of their
// tasks and criteria are checked, and the first open one of each, and which
// planned milestones are workable. It mirrors the Python helpers the
// validator uses (`parse_roadmap_rows_full` in hooks/cairn_common.py, `_section_body` and
// `_AC_ITEM` in scripts/cairn_validate.py, `find_cairn_root` for the walk),
// and `workable` in scripts/cairn_next.py over the rows `cairn_scripts.rows`
// parses (its Depends-on cells through `parse_depends`), with what
// `workable` reaches through `done_ids` and `_workable` (`canon_id`,
// `archive_files`, and `sort_by_priority` with its `id_num`). The
// mirror reads ASCII digits only, where Python's `isdigit`, `isdecimal`,
// and `\d` also take other Unicode digits, so an id such as `M００５７`
// reads differently in the two.
// hooks/status/reader.test.ts holds this reader, and
// scripts/tests/test_status_fixtures.py the Python helpers, to the same
// fixtures.

// Where the reader gets files. The shipped mod reads through `$.fs` and
// `$.session`; the tests read an in-memory copy of a fixture.
export type FileSource = {
  cwd: () => Promise<string>
  isFile: (path: string) => Promise<boolean>
  // The file's text, or null when it cannot be read.
  read: (path: string) => Promise<string | null>
  // The names of a directory's entries, or null when it cannot be listed.
  list: (path: string) => Promise<string[] | null>
}

// A planned milestone whose dependencies are all done.
export type WorkableRow = { id: string; title: string }

// What the band reads: the active rows in ROADMAP order, and the workable
// planned rows by priority and then id, whether or not a row is active.
export type BandState = { rows: BandRow[]; workable: WorkableRow[] }

// The counts and next items are all null when the row's milestone path is
// not a readable regular file. A next item is also null when its section
// holds no open box.
export type BandRow = {
  id: string
  title: string
  status: string
  tasksChecked: number | null
  tasksTotal: number | null
  criteriaChecked: number | null
  criteriaTotal: number | null
  // The first open task or criterion line, less its `- [ ]` prefix.
  nextTask: string | null
  nextCriterion: string | null
}

export type Fixture = {
  cwd: string
  files: Record<string, string>
  rows: BandRow[]
  // The ordered ids of the workable planned rows, as cairn_next.py lists them.
  workable: string[]
  // The pane's milestones, and `recommend` with `waiting` beside it, as
  // scripts/tests/test_status_fixtures.py computes them; `next` is null
  // with no ROADMAP (M205).
  pane: PaneMilestone[]
  next: (NextStep & { waiting: WaitingRow[] }) | null
  // Paths that stat as files but whose read fails in the tests.
  unreadable: string[]
}

export const ACTIVE: readonly string[] = ['in-progress', 'review']

const AC_ITEM = /^\s*-\s*\[[ xX]\]/
const CHECKED = /^\s*-\s*\[[xX]\]/
const OPEN_BOX = /^\s*-\s*\[ \]\s*/

// The line breaks Python's str.splitlines() splits on.
const LINE_BREAK = new RegExp(
  '\\r\\n|[\\n\\r\\v\\f\\x1c\\x1d\\x1e\\x85' + String.fromCharCode(0x2028, 0x2029) + ']',
)

export function splitLines(text: string): string[] {
  return text.split(LINE_BREAK)
}

export type RoadmapRow = {
  id: string
  title: string
  status: string
  depends: string
  priority: string
  relpath: string
}

export function parseRoadmapRows(text: string): RoadmapRow[] {
  const rows: RoadmapRow[] = []
  for (const line of splitLines(text)) {
    if (!line.trimStart().startsWith('|')) continue
    const cells = line.split('|').slice(1, -1).map(c => c.trim())
    if (cells.length < 6 || !cells[0].startsWith('M')) continue
    rows.push({
      id: cells[0],
      title: cells[1],
      status: cells[2].toLowerCase(),
      depends: cells[3],
      priority: cells[4],
      relpath: cells[5],
    })
  }
  return rows
}

const DIGITS = /^\d+$/

// The milestone ids in a Depends-on cell, as `parse_depends` for ASCII
// digits: a token is an `M` and digits, and every other token, `—`
// included, is dropped.
export function parseDepends(cell: string): string[] {
  return cell
    .trim()
    .split(/[,\s]+/)
    .filter(token => token.startsWith('M') && DIGITS.test(token.slice(1)))
}

// An id at three-digit padding, as `canon_id` for ASCII digits: `M57`,
// `M057`, and `M0057` are `M057`, and a non-numeric id stays as it is.
export function canonId(id: string): string {
  const rest = id.slice(1)
  return DIGITS.test(rest) ? `M${BigInt(rest).toString().padStart(3, '0')}` : id
}

// The sort key of an id: its number, or after every numeric id.
function idNumber(id: string): number {
  const rest = id.slice(1)
  return DIGITS.test(rest) ? Number(rest) : 1e9
}

// A Map, so a priority word such as `constructor` reads as normal.
const PRIORITY_RANK = new Map([
  ['high', 0],
  ['normal', 1],
  ['low', 2],
])

function priorityRank(priority: string): number {
  return PRIORITY_RANK.get(priority.toLowerCase()) ?? 1
}

// The planned rows whose Depends-on ids are each a done row or in
// `archived`, by priority and then id; the sort keeps ROADMAP order on a
// tie. `archived` holds ids at three-digit padding.
export function workableRows(rows: RoadmapRow[], archived: string[]): WorkableRow[] {
  const done = new Set([...rows.filter(row => row.status === 'done').map(row => canonId(row.id)), ...archived])
  return rows
    .filter(row => row.status === 'planned' && parseDepends(row.depends).every(dep => done.has(canonId(dep))))
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority) || idNumber(a.id) - idNumber(b.id))
    .map(row => ({ id: row.id, title: row.title }))
}

// The glob `M*.md` and the id at the start of each name, as `archive_files`.
const ARCHIVE_NAME = /^M[\s\S]*\.md$/
const ARCHIVE_ID = /^M\d+/

// The ids, at three-digit padding, of the archive files directly under
// cairn/milestones/archive/.
async function archivedIds(source: FileSource, root: string): Promise<string[]> {
  const names = (await source.list(join(root, 'cairn/milestones/archive'))) ?? []
  const ids: string[] = []
  for (const name of names) {
    const id = ARCHIVE_NAME.test(name) ? ARCHIVE_ID.exec(name)?.[0] : undefined
    if (id !== undefined) ids.push(canonId(id))
  }
  return ids
}

// Lines under the first `## <heading>` H2, up to the next H2 or the end.
export function sectionBody(text: string, heading: string): string[] {
  const out: string[] = []
  let inSection = false
  for (const line of splitLines(text)) {
    if (line.startsWith('## ')) {
      if (inSection) break
      inSection = line.slice(3).trim().toLowerCase().startsWith(heading.toLowerCase())
      continue
    }
    if (inSection) out.push(line)
  }
  return out
}

export type SectionFields = { checked: number; total: number; next: string | null }

// The checkbox counts of one section and its first open line, less the box.
export function sectionFields(text: string, heading: string): SectionFields {
  const items = sectionBody(text, heading).filter(line => AC_ITEM.test(line))
  const open = items.find(line => OPEN_BOX.test(line))
  return {
    checked: items.filter(line => CHECKED.test(line)).length,
    total: items.length,
    next: open === undefined ? null : open.replace(OPEN_BOX, ''),
  }
}

const NO_FILE = {
  tasksChecked: null,
  tasksTotal: null,
  criteriaChecked: null,
  criteriaTotal: null,
  nextTask: null,
  nextCriterion: null,
}

function fileFields(text: string) {
  const tasks = sectionFields(text, 'Tasks')
  const criteria = sectionFields(text, 'Acceptance criteria')
  return {
    tasksChecked: tasks.checked,
    tasksTotal: tasks.total,
    criteriaChecked: criteria.checked,
    criteriaTotal: criteria.total,
    nextTask: tasks.next,
    nextCriterion: criteria.next,
  }
}

export function dirname(path: string): string {
  const trimmed = path.length > 1 ? path.replace(/[\\/]+$/, '') : path
  const cut = Math.max(trimmed.lastIndexOf('/'), trimmed.lastIndexOf('\\'))
  if (cut < 0) return trimmed
  if (cut === 0) return trimmed[0]
  const head = trimmed.slice(0, cut)
  return /^[A-Za-z]:$/.test(head) ? head + trimmed[cut] : head
}

export function join(dir: string, rel: string): string {
  return `${dir.replace(/[\\/]+$/, '')}/${rel}`
}

// The nearest directory at or above `cwd` that holds cairn/ROADMAP.md.
export async function findRoot(source: FileSource, cwd: string): Promise<string | null> {
  let path = cwd
  for (;;) {
    if (await source.isFile(join(path, 'cairn/ROADMAP.md'))) return path
    const parent = dirname(path)
    if (parent === path) return null
    path = parent
  }
}

// One row per `in-progress` or `review` milestone, in ROADMAP order, and
// the workable list. Empty when no ROADMAP is found, and null when one is
// found but cannot be read (M200). `read_roadmap` in
// scripts/cairn_scripts.py reads an unreadable ROADMAP as empty instead.
export async function loadBand(source: FileSource): Promise<BandState | null> {
  const loaded = await loadCairn(source)
  return loaded === null ? null : loaded.band
}

// The band's state and the pane's from one read of the files (M205). Null
// when a ROADMAP is found but cannot be read.
export async function loadCairn(source: FileSource): Promise<{ band: BandState; pane: PaneState } | null> {
  const root = await findRoot(source, await source.cwd())
  if (root === null) return { band: { rows: [], workable: [] }, pane: NO_PANE }
  const roadmap = await source.read(join(root, 'cairn/ROADMAP.md'))
  if (roadmap === null) return null
  const parsed = parseRoadmapRows(roadmap)
  const out: BandRow[] = []
  const milestones: PaneMilestone[] = []
  for (const row of parsed) {
    if (!ACTIVE.includes(row.status)) continue
    // A regular file only, as Python's os.path.isfile: a path to a pipe or
    // a device would otherwise stall the read at every turn end.
    const path = join(root, `cairn/${row.relpath}`)
    const text = (await source.isFile(path)) ? await source.read(path) : null
    const fields = text === null ? NO_FILE : fileFields(text)
    out.push({ id: row.id, title: row.title, status: row.status, ...fields })
    milestones.push({ id: row.id, title: row.title, status: row.status, file: text === null ? null : paneFile(text) })
  }
  const archived = await archivedIds(source, root)
  const workable = workableRows(parsed, archived)
  return {
    band: { rows: out, workable },
    pane: {
      found: true,
      milestones,
      next: recommend(parsed, workable),
      workable,
      waiting: waitingRows(parsed, archived),
    },
  }
}

// The cairn pane's state (M205): the active milestones in full, and the
// queue that scripts/cairn_next.py prints. `found` is false when no ROADMAP
// is found.
export type PaneState = {
  found: boolean
  milestones: PaneMilestone[]
  next: NextStep | null
  workable: WorkableRow[]
  waiting: WaitingRow[]
}

export type PaneItem = { text: string; checked: boolean }

// `file` is null when the milestone file is missing or its read fails.
export type PaneMilestone = {
  id: string
  title: string
  status: string
  file: { goal: string; tasks: PaneItem[]; criteria: PaneItem[]; log: string[] } | null
}

// `recommend` in scripts/cairn_next.py: `id` is null for planning.
export type NextStep = { action: string; command: string; id: string | null }

// `waiting` in scripts/cairn_next.py: `unmet` holds each undone dependency
// as written, with its row's status or `unknown`.
export type WaitingRow = { id: string; title: string; unmet: string[] }

export const NO_PANE: PaneState = { found: false, milestones: [], next: null, workable: [], waiting: [] }

// How many work-log lines the pane shows, newest last.
export const LOG_LINES = 5

const COMMENT = /<!--[\s\S]*?-->/g
const ITEM_BOX = /^\s*-\s*\[[ xX]\]\s*/
const LOG_ITEM = /^- /

// A section's lines with HTML comments removed, as the template's owner
// notes are.
function sectionText(text: string, heading: string): string[] {
  return splitLines(sectionBody(text, heading).join('\n').replace(COMMENT, ''))
}

// A section's checkbox items. A non-blank indented line that is not itself
// an item continues the item above it, so a wrapped task reads whole.
export function sectionItems(text: string, heading: string): PaneItem[] {
  const items: PaneItem[] = []
  let current: PaneItem | null = null
  for (const line of sectionText(text, heading)) {
    if (AC_ITEM.test(line)) {
      current = { text: line.replace(ITEM_BOX, ''), checked: CHECKED.test(line) }
      items.push(current)
    } else if (current !== null && /^\s/.test(line) && line.trim() !== '') {
      current.text = `${current.text} ${line.trim()}`
    } else {
      current = null
    }
  }
  return items
}

function paneFile(text: string) {
  return {
    goal: sectionText(text, 'Goal').join('\n').trim(),
    tasks: sectionItems(text, 'Tasks'),
    criteria: sectionItems(text, 'Acceptance criteria'),
    log: sectionText(text, 'Work log')
      .filter(line => LOG_ITEM.test(line))
      .slice(-LOG_LINES)
      .map(line => line.replace(LOG_ITEM, '')),
  }
}

// `recommend` in scripts/cairn_next.py, over the rows and the workable list.
export function recommend(rows: RoadmapRow[], workable: WorkableRow[]): NextStep {
  const review = rows.find(row => row.status === 'review')
  if (review !== undefined) return { action: 'review', command: '/milestone-review', id: review.id }
  const active = rows.find(row => row.status === 'in-progress')
  if (active !== undefined) return { action: 'resume', command: '/milestone-implement', id: active.id }
  if (workable.length > 0) return { action: 'implement', command: '/milestone-implement', id: workable[0].id }
  return { action: 'plan the next milestone', command: '/milestone-plan', id: null }
}

// `waiting` in scripts/cairn_next.py: the planned rows with a dependency
// not yet done, in ROADMAP order. A later row with the same id wins the
// status lookup, as the Python dict does.
export function waitingRows(rows: RoadmapRow[], archived: string[]): WaitingRow[] {
  const done = new Set([...rows.filter(row => row.status === 'done').map(row => canonId(row.id)), ...archived])
  const byId = new Map<string, RoadmapRow>()
  for (const row of rows) byId.set(canonId(row.id), row)
  const out: WaitingRow[] = []
  for (const row of rows) {
    if (row.status !== 'planned') continue
    const unmet = parseDepends(row.depends)
      .filter(dep => !done.has(canonId(dep)))
      .map(dep => `${dep} (${byId.get(canonId(dep))?.status ?? 'unknown'})`)
    if (unmet.length > 0) out.push({ id: row.id, title: row.title, unmet })
  }
  return out
}

// The names directly under `dir` in a set of absolute file paths: a file's
// name, or the first part of a deeper path. Null when nothing is under it.
export function listNames(paths: string[], dir: string): string[] | null {
  const prefix = `${dir.replace(/[\\/]+$/, '')}/`
  const names = new Set<string>()
  for (const path of paths) if (path.startsWith(prefix)) names.add(path.slice(prefix.length).split('/')[0])
  return names.size === 0 ? null : [...names]
}

// An in-memory file source over absolute paths, for the tests. A path in
// `unreadable` stats as a file, and its read fails.
export function memorySource(files: Record<string, string>, cwd: string, unreadable: string[] = []): FileSource {
  return {
    cwd: async () => cwd,
    isFile: async path => Object.prototype.hasOwnProperty.call(files, path),
    read: async path =>
      Object.prototype.hasOwnProperty.call(files, path) && !unreadable.includes(path) ? files[path] : null,
    list: async dir => listNames(Object.keys(files), dir),
  }
}
