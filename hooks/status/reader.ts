// The status band's reader: which milestones are active, how many of their
// tasks and criteria are checked, and the first open one of each. It mirrors the Python helpers the validator uses
// (`parse_roadmap_rows_full` in hooks/cairn_common.py, `_section_body` and
// `_AC_ITEM` in scripts/cairn_validate.py, `find_cairn_root` for the walk).
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
}

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

export type RoadmapRow = { id: string; title: string; status: string; relpath: string }

export function parseRoadmapRows(text: string): RoadmapRow[] {
  const rows: RoadmapRow[] = []
  for (const line of splitLines(text)) {
    if (!line.trimStart().startsWith('|')) continue
    const cells = line.split('|').slice(1, -1).map(c => c.trim())
    if (cells.length < 6 || !cells[0].startsWith('M')) continue
    rows.push({ id: cells[0], title: cells[1], status: cells[2].toLowerCase(), relpath: cells[5] })
  }
  return rows
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

// One row per `in-progress` or `review` milestone, in ROADMAP order.
export async function loadBand(source: FileSource): Promise<BandRow[]> {
  const root = await findRoot(source, await source.cwd())
  if (root === null) return []
  const roadmap = await source.read(join(root, 'cairn/ROADMAP.md'))
  if (roadmap === null) return []
  const out: BandRow[] = []
  for (const row of parseRoadmapRows(roadmap)) {
    if (!ACTIVE.includes(row.status)) continue
    // A regular file only, as Python's os.path.isfile: a path to a pipe or
    // a device would otherwise stall the read at every turn end.
    const path = join(root, `cairn/${row.relpath}`)
    const text = (await source.isFile(path)) ? await source.read(path) : null
    const fields = text === null ? NO_FILE : fileFields(text)
    out.push({ id: row.id, title: row.title, status: row.status, ...fields })
  }
  return out
}

// An in-memory file source over absolute paths, for the tests.
export function memorySource(files: Record<string, string>, cwd: string): FileSource {
  return {
    cwd: async () => cwd,
    isFile: async path => Object.prototype.hasOwnProperty.call(files, path),
    read: async path => (Object.prototype.hasOwnProperty.call(files, path) ? files[path] : null),
  }
}
