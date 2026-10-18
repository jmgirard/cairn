// The status band's reader: which milestones are active, how many of their
// tasks and criteria are checked, and the first open one of each, and which
// planned milestones are workable. It mirrors the Python helpers the
// validator uses (`parse_roadmap_rows_full` in hooks/cairn_common.py, `_section_body` and
// `_AC_ITEM` in scripts/cairn_validate.py, `find_cairn_root` for the walk),
// and `workable` in scripts/cairn_next.py over the rows `cairn_scripts.rows`
// parses (its Depends-on cells through `parse_depends`), with what
// `workable` reaches through `done_ids` and `_workable` (`canon_id`,
// `archive_files`, and `sort_by_priority` with its `id_num`). For the cairn
// pane it also mirrors `recommend` and `waiting` in scripts/cairn_next.py
// (M205), and reads the candidate rows in the sections that
// `candidate_count` in scripts/cairn_scripts.py walks (M207), and mirrors
// `blocked` and `pr_number` in scripts/cairn_next.py (M223), and `pr_url`
// (M224), and `archived_text` and `status_paragraph` (M246), and
// `stack_bases` and `_met`, with `push_remote` in hooks/cairn_common.py
// (M268), and `high_title`, which `recommend` reads for planning (M272). The mirror
// reads ASCII digits only, where Python's `isdigit`, `isdecimal`, and `\d`
// also take other Unicode digits, so an id such as `M００５７` reads
// differently in the two.
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

// A planned milestone whose dependencies are all done; in guest mode at
// most one may instead be a stack base (M268, `workableRows`).
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
  // The pane's candidate rows, as test_status_fixtures.py reads them (M207).
  candidates: CandidateRow[]
  // The pane's blocked rows, as `blocked` in scripts/cairn_next.py reads
  // them (M223).
  blocked: BlockedRow[]
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

// The planned rows whose Depends-on ids are each a done row, in
// `archived`, or in `bases`, with at most one in `bases` (M268), by
// priority and then id; the sort keeps ROADMAP order on a tie. `archived`
// and `bases` hold ids at three-digit padding. `bases` holds the stack
// bases, as `stack_bases` in scripts/cairn_next.py reads them.
export function workableRows(rows: RoadmapRow[], archived: string[], bases: string[] = []): WorkableRow[] {
  const done = doneIds(rows, archived)
  const stacked = new Set(bases)
  return rows
    .filter(row => row.status === 'planned' && unmetDeps(row, done, stacked).length === 0)
    .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority) || idNumber(a.id) - idNumber(b.id))
    .map(row => ({ id: row.id, title: row.title }))
}

function doneIds(rows: RoadmapRow[], archived: string[]): Set<string> {
  return new Set([...rows.filter(row => row.status === 'done').map(row => canonId(row.id)), ...archived])
}

// The Depends-on ids, as written, that `_met` in scripts/cairn_next.py
// leaves out: met are the done ids, and the row's stack-base dependency
// when it has exactly one (M268).
function unmetDeps(row: RoadmapRow, done: Set<string>, bases: Set<string>): string[] {
  const deps = parseDepends(row.depends)
  const onBases = new Set(deps.map(canonId).filter(id => bases.has(id) && !done.has(id)))
  const met = onBases.size <= 1 ? new Set([...done, ...onBases]) : done
  return deps.filter(dep => !met.has(canonId(dep)))
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

// `status_paragraph` in scripts/cairn_next.py (M246): the first line that
// starts with `**Status:**`, through the line before the next line of only
// spaces and tabs, or the end of the text. Null when no line starts so.
const BLANK = /^[ \t]*$/
const STATUS_DONE = /^\*\*Status:\*\*[ \t]*done/
export function statusParagraph(text: string): string | null {
  const lines = splitLines(text)
  const start = lines.findIndex(line => line.startsWith('**Status:**'))
  if (start < 0) return null
  const out = [lines[start]]
  for (const rest of lines.slice(start + 1)) {
    if (BLANK.test(rest)) break
    out.push(rest)
  }
  return out.join('\n')
}

// `archived_text` in scripts/cairn_next.py (M246): the text of the one
// archive file whose canonical id is the row's, when its read succeeds and
// its Status paragraph starts with `done`. Null otherwise.
async function archivedText(source: FileSource, root: string, id: string): Promise<string | null> {
  const dir = join(root, 'cairn/milestones/archive')
  const want = canonId(id)
  const found = ((await source.list(dir)) ?? []).filter(name => {
    const got = ARCHIVE_NAME.test(name) ? ARCHIVE_ID.exec(name)?.[0] : undefined
    return got !== undefined && canonId(got) === want
  })
  if (found.length !== 1) return null
  const path = join(dir, found[0])
  const text = (await source.isFile(path)) ? await source.read(path) : null
  const para = text === null ? null : statusParagraph(text)
  return para !== null && STATUS_DONE.test(para) ? text : null
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
  // A UNC share root (`\\host\share`) is a root, as a drive is (M210).
  if (/^[\\/]{2}[^\\/]+[\\/][^\\/]+$/.test(trimmed)) return trimmed
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
// found but cannot be read (M200) or is empty (M210). `read_roadmap` in
// scripts/cairn_scripts.py reads an unreadable ROADMAP as empty instead.
export async function loadBand(source: FileSource): Promise<BandState | null> {
  const loaded = await loadCairn(source)
  return loaded === null ? null : loaded.band
}

// The band's state and the pane's from one read of the files (M205). Null
// when a ROADMAP is found but cannot be read, or its text is empty or only
// whitespace, as a write half done can leave it (M210).
export async function loadCairn(source: FileSource): Promise<{ band: BandState; pane: PaneState } | null> {
  const root = await findRoot(source, await source.cwd())
  return root === null ? emptyCairn() : loadAt(source, root)
}

// The same read with the root it found (M210): `root` is null when no
// ROADMAP is found, and `state` is null when a found one cannot be read,
// its text is empty or only whitespace, or a throw ends the read. A throw
// from `source.cwd()` is not caught, since it leaves the root unknown.
export async function readCairn(
  source: FileSource,
): Promise<{ root: string | null; state: { band: BandState; pane: PaneState } | null }> {
  const root = await findRoot(source, await source.cwd())
  if (root === null) return { root, state: emptyCairn() }
  try {
    return { root, state: await loadAt(source, root) }
  } catch {
    return { root, state: null }
  }
}

function emptyCairn(): { band: BandState; pane: PaneState } {
  return { band: { rows: [], workable: [] }, pane: NO_PANE }
}

async function loadAt(source: FileSource, root: string): Promise<{ band: BandState; pane: PaneState } | null> {
  const roadmap = await source.read(join(root, 'cairn/ROADMAP.md'))
  if (roadmap === null || roadmap.trim() === '') return null
  const parsed = parseRoadmapRows(roadmap)
  const out: BandRow[] = []
  const milestones: PaneMilestone[] = []
  const blocked: BlockedRow[] = []
  for (const row of parsed) {
    const active = ACTIVE.includes(row.status)
    if (!active && row.status !== 'blocked') continue
    // A regular file only, as Python's os.path.isfile: a path to a pipe or
    // a device would otherwise stall the read at every turn end.
    const path = join(root, `cairn/${row.relpath}`)
    const live = await source.isFile(path)
    const text = live ? await source.read(path) : null
    if (!active) {
      const archive = live ? null : await archivedText(source, root, row.id)
      if (archive !== null) {
        const url = PR_URL.exec(statusParagraph(archive) ?? '')
        blocked.push({
          id: row.id,
          title: row.title,
          pr: url === null ? null : Number(url[1]),
          url: url === null ? null : url[0],
          archived: true,
        })
        continue
      }
      blocked.push({
        id: row.id,
        title: row.title,
        pr: text === null ? null : prNumber(text),
        url: text === null ? null : prUrl(text),
        archived: false,
      })
      continue
    }
    const fields = text === null ? NO_FILE : fileFields(text)
    out.push({ id: row.id, title: row.title, status: row.status, ...fields })
    milestones.push({ id: row.id, title: row.title, status: row.status, file: text === null ? null : paneFile(text) })
  }
  const archived = await archivedIds(source, root)
  // The stack bases, as `stack_bases` in scripts/cairn_next.py (M268).
  const profilePath = join(root, 'cairn/PROFILE.md')
  const profile = (await source.isFile(profilePath)) ? await source.read(profilePath) : null
  const stacking = profile !== null && collaborationMode(profile) === 'guest' && pushRemote(profile) === 'base'
  const bases = stacking ? blocked.filter(row => row.url !== null && !row.archived).map(row => canonId(row.id)) : []
  const workable = workableRows(parsed, archived, bases)
  return {
    band: { rows: out, workable },
    pane: {
      found: true,
      milestones,
      next: recommend(parsed, workable, roadmap),
      workable,
      waiting: waitingRows(parsed, archived, bases),
      candidates: candidateRows(roadmap),
      blocked,
      taken: takenRows(
        roadmap,
        parsed,
        blocked.filter(row => row.archived).map(row => row.id),
      ),
    },
  }
}

// A milestone header's `Branch/PR` line, and a pull request URL in it, as
// `BRANCH_PR` and `PR_URL` in scripts/cairn_next.py (M223), with spaces and
// tabs spelled out, since `\s` takes different characters in the two. A
// number has at most 15 digits, so `Number` reads it exactly.
const BRANCH_PR = /^[ \t]*-[ \t]*\*\*Branch\/PR:\*\*(.*)$/
const PR_URL = /https:\/\/github\.com\/[^/ \t]+\/[^/ \t]+\/pull\/([0-9]{1,15})(?![0-9])/

// `_pr_match` in scripts/cairn_next.py: the match of the pull request URL
// that the first `Branch/PR` header line names, the first URL before any
// `companion:` entry, or null. The header is the text before the first
// `## ` heading.
function prMatch(text: string): RegExpExecArray | null {
  for (const line of splitLines(text)) {
    if (line.startsWith('## ')) return null
    const match = BRANCH_PR.exec(line)
    if (match === null) continue
    return PR_URL.exec(match[1].split('companion:')[0])
  }
  return null
}

// The collaboration mode that a `cairn/PROFILE.md` text declares, as
// `collaboration_mode` in hooks/cairn_common.py reads it (M226): the value
// of the first `# Collaboration mode:` line before the first `## ` slot
// heading, lowercased, with the key matched in any case and a leading BOM
// skipped. A text with no such line reads as `owner`.
export function collaborationMode(text: string): string {
  return profileHeader(text, /^#\s*Collaboration mode:\s*(\S+)/i) ?? 'owner'
}

// The value of the `# Push remote:` line that a `cairn/PROFILE.md` text
// declares, as `push_remote` in hooks/cairn_common.py reads it (M268):
// read as `collaborationMode` reads its line, and null with no such line.
export function pushRemote(text: string): string | null {
  return profileHeader(text, /^#\s*Push remote:\s*(\S+)/i)
}

// The first match of `pattern` before the first `## ` slot heading,
// lowercased, with a leading BOM skipped, or null.
function profileHeader(text: string, pattern: RegExp): string | null {
  for (const each of splitLines(text.replace(/^﻿/, ''))) {
    if (each.startsWith('## ')) break
    const found = pattern.exec(each)
    if (found !== null) return found[1].toLowerCase()
  }
  return null
}

// `pr_number` in scripts/cairn_next.py: the number of that pull request, or
// null.
export function prNumber(text: string): number | null {
  const url = prMatch(text)
  return url === null ? null : Number(url[1])
}

// `pr_url` in scripts/cairn_next.py (M224): its URL up to the number, so
// with no trailing path or anchor, or null.
export function prUrl(text: string): string | null {
  const url = prMatch(text)
  return url === null ? null : url[0]
}

// The cairn pane's state (M205): the active milestones in full, the
// queue that scripts/cairn_next.py prints, the candidate rows (M207), and
// the blocked rows with their pull request numbers (M223), and the
// started tokens of the candidate rows (M258). `found` is false when no
// ROADMAP is found.
export type PaneState = {
  found: boolean
  milestones: PaneMilestone[]
  next: NextStep | null
  workable: WorkableRow[]
  waiting: WaitingRow[]
  candidates: CandidateRow[]
  blocked: BlockedRow[]
  taken: TakenRow[]
}

// One candidate row of the ROADMAP: its priority token's level, `normal`
// with no token, and its short title.
export type CandidateRow = { priority: 'high' | 'normal' | 'low'; title: string }

// One ` — started <ref>` token of a candidate row (M258), with the row's
// short title: `ref` is `M<NNN>` or `#<n>` as the token spells it.
export type TakenRow = { title: string; ref: string }

export type PaneItem = { text: string; checked: boolean }

// `file` is null when the milestone file is missing or its read fails.
export type PaneMilestone = {
  id: string
  title: string
  status: string
  file: { goal: string; tasks: PaneItem[]; criteria: PaneItem[]; log: string[] } | null
}

// `recommend` in scripts/cairn_next.py: `id` is null for planning, and
// `title` is the short title of the first unstarted `[high]` candidate row
// when planning, else null (M272).
export type NextStep = { action: string; command: string; id: string | null; title: string | null }

// `waiting` in scripts/cairn_next.py: `unmet` holds each undone dependency
// as written, with its row's status or `unknown`.
export type WaitingRow = { id: string; title: string; unmet: string[] }

// `blocked` in scripts/cairn_next.py (M223): a `blocked` row, and the
// number of the pull request its milestone file's `Branch/PR` header names,
// or null, with that pull request's URL beside it (M224). `archived` is true
// when the row's file is not a regular file and exactly one archive file
// with its id is read and its Status paragraph starts with `done` (M246). The number and URL then come from
// that file's Status paragraph, and either may be null.
export type BlockedRow = { id: string; title: string; pr: number | null; url: string | null; archived: boolean }

export const NO_PANE: PaneState = {
  found: false,
  milestones: [],
  next: null,
  workable: [],
  waiting: [],
  candidates: [],
  blocked: [],
  taken: [],
}

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

const PRIORITY_TOKENS: readonly [string, 'high' | 'low'][] = [
  ['[high] ', 'high'],
  ['[low] ', 'low'],
]

// The candidate rows (M207): each flush-left line that opens with `- `
// under a `## Candidates` heading. HTML comments are removed from each such
// section's body before it is read, so the `/cairn-init` skeleton's
// placeholder rows are not read, and a `<!--` in another section hides
// nothing here. Every `## ` line starts or ends a section, as in
// `candidate_count` in scripts/cairn_scripts.py, which also counts indented
// lines and lines inside comments. A row's priority is `high` or `low` when
// its text opens with exactly `[high] ` or `[low] `, else `normal`. Its
// short title is the text after that token up to the first `: `, else up
// to the first ` — `, else all of it (M251; tracking-rules "Candidate short
// title").
export function candidateRows(roadmap: string): CandidateRow[] {
  return candidateTexts(roadmap).map(({ priority, text }) => ({ priority, title: shortTitle(text) }))
}

// Each candidate row's priority and its text after the priority token.
function candidateTexts(roadmap: string): { priority: CandidateRow['priority']; text: string }[] {
  const bodies: string[][] = []
  let body: string[] | null = null
  for (const line of splitLines(roadmap)) {
    if (line.startsWith('## ')) {
      body = line.trim().toLowerCase().startsWith('## candidates') ? [] : null
      if (body !== null) bodies.push(body)
      continue
    }
    if (body !== null) body.push(line)
  }
  const rows: { priority: CandidateRow['priority']; text: string }[] = []
  for (const line of bodies.flatMap(lines => splitLines(lines.join('\n').replace(COMMENT, '')))) {
    if (!line.startsWith('- ')) continue
    let text = line.slice(2)
    let priority: CandidateRow['priority'] = 'normal'
    const match = PRIORITY_TOKENS.find(([token]) => text.startsWith(token))
    if (match !== undefined) {
      priority = match[1]
      text = text.slice(match[0].length)
    }
    rows.push({ priority, text })
  }
  return rows
}

function shortTitle(text: string): string {
  let cut = text.indexOf(': ')
  if (cut < 0) cut = text.indexOf(' — ')
  return (cut < 0 ? text : text.slice(0, cut)).trim()
}

// A started token (M258): ` — started ` and a milestone id or a pull
// request number, followed by the row's end or by a character that is not
// a letter or digit, so a note such as `; narrowed …` or a trailing space
// after the token leaves it read (M258 review).
const STARTED_TOKEN = / — started (M[0-9]+|#[0-9]{1,15})(?![0-9A-Za-z])/g

// The started tokens of the candidate rows (M258), in ROADMAP order, each
// with its row's short title. `/milestone-plan` writes ` — started M<NNN>`
// on a row its plan absorbs, and `/hotfix`'s guest arm ` — started #<n>`
// on a row its pull request fixes. Since each token opens with ` — `, a
// row's short title is the same with or without one. A row with an empty
// short title gives none, since no title names it.
export function startedTokens(roadmap: string): TakenRow[] {
  const out: TakenRow[] = []
  for (const { text } of candidateTexts(roadmap)) {
    const title = shortTitle(text)
    if (title === '') continue
    for (const match of text.matchAll(STARTED_TOKEN)) out.push({ title, ref: match[1] })
  }
  return out
}

// The tokens the pane counts (M258): an `M<NNN>` token while the ROADMAP
// table holds that id as `planned` or `blocked`, the two statuses under
// which that milestone is open and does not hide the candidate list (an
// `in-progress` or `review` milestone hides it), and every `#<n>` token,
// which the pane checks against its open hotfix list. A `blocked` id in
// `archived`, whose file was archived before its row changed (M246), does
// not count, since that work shipped. A counted id is given at three-digit
// padding, as the table spells it (M258 review).
export function takenRows(roadmap: string, rows: RoadmapRow[], archived: string[] = []): TakenRow[] {
  const shipped = new Set(archived.map(canonId))
  const live = new Set(
    rows
      .filter(row => row.status === 'planned' || row.status === 'blocked')
      .map(row => canonId(row.id))
      .filter(id => !shipped.has(id)),
  )
  return startedTokens(roadmap)
    .filter(item => item.ref.startsWith('#') || live.has(canonId(item.ref)))
    .map(item => (item.ref.startsWith('#') ? item : { title: item.title, ref: canonId(item.ref) }))
}

// `recommend` in scripts/cairn_next.py, over the rows, the workable list,
// and the ROADMAP text, from which planning reads `highTitle` (M272).
export function recommend(rows: RoadmapRow[], workable: WorkableRow[], roadmap = ''): NextStep {
  const review = rows.find(row => row.status === 'review')
  if (review !== undefined) return { action: 'review', command: '/milestone-review', id: review.id, title: null }
  const active = rows.find(row => row.status === 'in-progress')
  if (active !== undefined) return { action: 'resume', command: '/milestone-implement', id: active.id, title: null }
  if (workable.length > 0) return { action: 'implement', command: '/milestone-implement', id: workable[0].id, title: null }
  return { action: 'plan the next milestone', command: '/milestone-plan', id: null, title: highTitle(roadmap) }
}

// A started token as `STARTED` in scripts/cairn_next.py reads it (M272): as
// `STARTED_TOKEN`, but with no cap on a pull request number's digits.
const STARTED = / — started (M[0-9]+|#[0-9]+)(?![0-9A-Za-z])/

// `high_title` in scripts/cairn_next.py (M272): the short title of the
// first candidate row, in ROADMAP order, that opens with `[high] `, has a
// non-empty short title, and carries no started token, or null.
export function highTitle(roadmap: string): string | null {
  for (const { priority, text } of candidateTexts(roadmap)) {
    const title = shortTitle(text)
    if (priority === 'high' && title !== '' && !STARTED.test(text)) return title
  }
  return null
}

// `waiting` in scripts/cairn_next.py: the planned rows that are not
// workable, in ROADMAP order. A later row with the same id wins the status
// lookup, as the Python dict does.
export function waitingRows(rows: RoadmapRow[], archived: string[], bases: string[] = []): WaitingRow[] {
  const done = doneIds(rows, archived)
  const stacked = new Set(bases)
  const byId = new Map<string, RoadmapRow>()
  for (const row of rows) byId.set(canonId(row.id), row)
  const out: WaitingRow[] = []
  for (const row of rows) {
    if (row.status !== 'planned') continue
    const unmet = unmetDeps(row, done, stacked).map(dep => `${dep} (${byId.get(canonId(dep))?.status ?? 'unknown'})`)
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
