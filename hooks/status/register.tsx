import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { CairnBandHidden, CairnHotfixRead, CairnRepoRead, CairnStep } from '../../types'
import type { BandLine, Span } from './band'
import { actionsFit, cairnSkill, GAP, GRAY, knownStep, mark, PX_PER_COLUMN, same, stepLines, width } from './band'
import { countsArgv, prRead } from './counts'
import { BADGE_H, badgeSvg, badgeWidth } from './badge'
import { ICON_PX, iconSvg } from './icons'
import { archivedArgs, COMMON_DIR_ARGS, DESCRIBE_ARGS, doneSince, projectName, repoArgv, repoCounts, tagTimeArgs } from './repo'
import type { HotfixPr, PaneButton, PrRead, StartedRow } from './pane'
import {
  CHECK_LABEL,
  CLEAR_LABEL,
  CLEARS_FIRST,
  FINISH_LABEL,
  HOME_LABEL,
  hotfixPrs,
  INFO_LABEL,
  METER_EMPTY_KEY,
  nextTitle,
  startedRefs,
  startedRows,
  nextLabel as labelOf,
  NO_ROADMAP,
  paneLines,
  PLAN_CANDIDATE_LABEL,
  PLAN_LABEL,
  PR_BUTTON,
  prWord,
  READING_LABEL,
  REFRESH_LABEL,
  REVISE_LABEL,
  STATUS_LABEL,
} from './pane'
import type { BandState, FileSource, PaneState } from './reader'
import { collaborationMode, join, NO_PANE, readCairn } from './reader'
import { brailleSpans, TRACK_H, TRACK_PX, trackSvg } from './track'

// The milestone band above the prompt (M191, M193 to M201, M206): one row
// for one `in-progress` or `review` ROADMAP row, refreshed when the session
// starts, at the end of each turn, when a cairn skill's prompt is expanded,
// and when a step ends. The row is the bold id and the title, then the flow
// track and its percent (band.ts picks the row and its widths). With no
// active milestone, an idle row names the next workable planned milestone,
// and its `Implement` Button, not a command, starts it (M220). With none
// workable, a found ROADMAP draws the empty row (M213). A press of `Plan`
// or `Implement` runs `/clear`, and its command at the session end that
// the clear brings (M221).
// The track draws as an `Svg` on the desktop and as braille cells in the
// terminal (track.ts). The running cairn skill draws nothing of its own:
// /milestone-review picks the row it shows. A skill's step
// ends at the first main-loop Stop with no background work in flight and no
// one-shot wakeup pending (M210) that no hook
// beneath blocks, or at a prompt the operator types while the session is
// idle, unless a cairn skill's prompt was expanded since the last prompt,
// Stop, or turn end, as a typed cairn slash command's is. A typed prompt
// that a hook beneath drops leaves the step (M210). So the step holds while the skill waits on background work and
// through the turns that the work's notices start (M201). The row sits
// above whatever the hooks beneath draw in the same slot. It ends in a
// close button, which hides the band until the active rows' ids, statuses,
// or order, the row /milestone-review moves the band to, or the idle row's
// id change, or the session ends (M200, M206). A found ROADMAP that cannot
// be read, or is empty, keeps the rows when they came from the same repo
// root (M210), and the close state is compared against them and the
// current step.
//
// The cairn pane (M205) opens from the `/cairn-pane` command, which also
// closes it, or from the band's open button, which a row drawn from a found
// ROADMAP carries beside the close button. It shows the active milestones
// in full and the queue that scripts/cairn_next.py prints (pane.ts), from
// the same refreshes as the band. A head line whose file reads ends with
// the band's percent for its row, so the pane reads the `band` value too
// (M208). While no cairn skill's step is set, the Next line carries a
// Button with the band's next-step label after its command, and a press runs
// `pressNext`, as the band's does (M218). At the same times, the line
// carries Status after that Button, and a press runs `pressStatus` (M219).
// At the same times, the first line carries ⌂ before ↻, and a press runs
// `pressHome`: `/clear`, and an open of the pane at the clear's session end
// (M241). Until M241
// the Next line carried Clear while `ended` was true.
// Each open of the pane, by the command, the band's open button, or the
// session-start reopen, reads the blocked rows' pull request states once
// with `gh`, and so does a press of the pane's ↻ Refresh Button
// (`readPrs`, M236). The reopen skips the read when its start already read
// (M238). An open does not wait for that read, and a `/clear` or a
// `/resume` reads again while the pane is placed, shown or behind another
// tab (M230, M237). A pane listed but not placed then reads at its first
// draw, unless an open or the start's reopen read first, or the start's
// `$.ui.panes()` threw. One start reads once, though both its start hooks
// fire (M238). A blocked line then shows its state word, and a merged,
// changes-requested, or closed line carries a Button for its next step
// (M224). The same read counts each open pull request's unresolved review
// threads, which draw on a line under it (M225, M236). A github.com pull
// request's word and count come from one `gh api graphql` call (M237). The same read lists the operator's open pull requests on the
// base remote with one `gh pr list` call and keeps the ones from
// `hotfix-*` branches, which the pane draws, each with its word and counts
// (M226).

// Each shape tag names a value's layout; a reload whose value was written
// under another tag reads it as absent. Bump a tag when its type changes.
// The band's value keeps the repo root of the last read, null when no
// ROADMAP was found or the working directory could not be read; the tag
// moved to 4 with the root (M210).
type StoredBand = BandState & { root: string | null }
const BAND_REF = { plugin: 'cairn', key: 'band' } as const
const BAND_SHAPE = 'band-4'
const band = atom(BAND_REF, { rows: [], workable: [], root: null } as StoredBand, { shape: BAND_SHAPE })

// The active ids and statuses, in ROADMAP order, `milestone-review` while
// it moves the band to another row, and the idle row's id while no row is
// active, at the last press of the close button; null while the band shows.
// The tag moved to 4 when the skill's meaning changed (M206 review). The
// press writes through `$.state.set`, which takes the tag with the value and
// a reference written as literals in this file.
const DISMISSED_REF = { plugin: 'cairn', key: 'dismissed' } as const
const DISMISSED_SHAPE = 'dismissed-4'
const dismissed = atom(DISMISSED_REF, null as CairnBandHidden | null, { shape: DISMISSED_SHAPE })

// The running cairn skill, until a main-loop Stop with nothing in flight or
// an idle typed prompt ends it (the `classic.Stop` and `prompt.submit`
// hooks). A typed prompt that finds `expanded` set keeps it; null while no
// cairn skill runs. The chapter it once held went in M206.
const step = atom({ plugin: 'cairn', key: 'step' } as const, null as CairnStep | null, { shape: 'step-2' })

// True from a cairn skill's prompt until the next prompt, Stop, turn end, or
// session end.
// The engine expands a typed slash command before it raises the command's
// prompt, so that prompt finds this set and keeps the step the command just
// started (M201).
const expanded = atom({ plugin: 'cairn', key: 'expanded' } as const, false, { shape: 'expanded-1' })

// True from a main-loop Stop that ends a cairn skill's step until the next
// idle typed prompt that enters, the next cairn skill's prompt, or the
// session's end (M216). While it is true, a row that draws the action
// Buttons carries the Clear Button too, when it has room for it.
const ended = atom({ plugin: 'cairn', key: 'ended' } as const, false, { shape: 'ended-1' })

// What the cairn pane shows, written at each refresh (M205). The tag moved
// to 2 when the state gained the candidate rows (M207), to 3 when it
// gained the blocked rows (M223), to 4 when each blocked row gained its
// pull request's URL (M224), to 5 when each blocked row gained
// `archived` (M246), to 6 when the state gained the candidate rows'
// started tokens (M258), to 7 when the next step gained `title` (M272),
// and to 8 when each candidate row gained its `text` (M293).
const pane = atom({ plugin: 'cairn', key: 'pane' } as const, NO_PANE as PaneState, { shape: 'pane-8' })

// Each blocked row's pull request state word by its URL, written by the
// read at a pane open or a Refresh press (M224). A URL with no entry has
// not been read, and its line shows no word. Each entry also holds the
// open pull request's counts, or null; the tag moved to 2 with them (M225)
// and to 3 when the second count left them (M236).
const prs = atom({ plugin: 'cairn', key: 'prs' } as const, {} as Record<string, PrRead>, { shape: 'prs-3' })

// The hotfix list that the last read wrote, and the repo root it is for
// (M226, `readHotfixes` says when it is kept or empty). The pane draws
// them only while the band's root is that root, so a failed read after a
// `cd` shows no other repo's. The same value holds the candidate rows that
// the listed bodies name, so one write keeps both from one read; the tag
// moved to 2 with them (M252).
const hotfixes = atom({ plugin: 'cairn', key: 'hotfixes' } as const, { root: null, prs: [], started: [] } as CairnHotfixRead, {
  shape: 'hotfixes-2',
})

// The summary card's numbers, the project name (M291), and the repo root
// they are for (M286), written by the same read as the hotfix list
// (`readRepo` says when they are kept). The pane draws them only while the
// band's root is that root, and otherwise names the root's last segment.
const repo = atom({ plugin: 'cairn', key: 'repo' } as const, { root: null, counts: null, done: null, name: null } as CairnRepoRead, {
  // `repo-2`: `repo-1`, without the release days, never shipped (M286).
  // `repo-3` adds the project name (M291).
  shape: 'repo-3',
})

// True from the start of a read of the pull request states until the newest
// read started has settled (M236). The pane's ↻ Button reads ⋯ while it is
// true and a read that this module started is in flight (`inFlight`, M237).
// A reload keeps it, so neither the label nor a press relies on it alone
// (`pressing`).
const reading = atom({ plugin: 'cairn', key: 'reading' } as const, false, { shape: 'reading-1' })

// The pane's id, its title, and the command that opens and closes it.
const PANE = 'cairn'
const PANE_TITLE = 'cairn'
const PANE_COMMAND = 'cairn-pane'
// The key of the Next line's Button (M218).
const PANE_NEXT = 'cairn-pane-next'
// The store key that holds the project roots whose session ended with reason
// `other` while the pane was open and shown (M222). A typed `/clear` in the
// desktop app ends the process that way, and the next process starts with no
// pane at the first message after the clear, so its `session.start` opens
// the pane again. The key is `$.session.root()`, which a shell `cd` does not
// move, so it matches the folder the next session starts in (M222 review). An app quit or a signal that ends the session with reason
// `other` also brings the pane back at the next session in that folder. The
// API does not say which ends those are, and none was checked live.
const REOPEN_KEY = 'reopen'

// The close button's label. The desktop app draws a dismiss Button in the
// band as its label text, so a long label reads as text there. On the
// desktop the label is `✕`, dim at rest, which the operator picked at a
// live look as closest to the app's own close icon (M197).
const CLOSE_GLYPH = '×'
const DESKTOP_CLOSE_GLYPH = '✕'
// The columns the row's close gap and one-glyph label take on either
// surface, which the row leaves free when it picks its form.
const CLOSE_COLUMNS = GAP + width(CLOSE_GLYPH)
// The open button's one-glyph label and the space after it, which a row
// drawn from a found ROADMAP also leaves free (M205).
const OPEN_GLYPH = '≡'
const OPEN_COLUMNS = width(OPEN_GLYPH) + 1

// The action Buttons (M212): the next step's label, from pane.ts's
// `nextLabel`, which the pane's Next Button reads too (M218), and the status
// Button's command. A plugin skill runs as `cairn:<name>` (M195).
const STATUS_COMMAND = 'cairn:milestone'
// The built-in command the Clear Button runs (M216). The Status and Clear
// labels sit in pane.ts, which the pane's Next line reads too (M219).
const CLEAR_COMMAND = 'clear'
// The hover card's ground, the theme key the band's braille track sits on
// (M286).
const HOVER_GROUND = 'userMessageBackground'
// The hover group of a candidate line's info glyph and card, one per line
// key (M290).
const infoScope = (lineKey: string) => `cairn-info-${lineKey}`
// The columns a candidate line keeps for ✎ while the pointer is over it,
// and the `right` offset that parks ✎ past the row's edge at rest (M290).
// The park hides ✎ only while its Button is narrower than 8 columns, since
// the pane clips what lies past its edge; a wider label needs both changed.
const PLAN_SLOT = 4
const PLAN_PARK = -8
// The command a candidate line's ✎ holds for its `/clear` (M242).
const PLAN_COMMAND = 'cairn:milestone-plan'
// `CLEARS_FIRST`, the next steps whose Button runs `/clear` first (M221),
// sits in pane.ts beside the label map.
// The key and label of each Button after the Next line's action (M219),
// of the pane's ⌂ Home (M241) and ↻ Refresh (M236), and of a blocked
// line's Button, whose key ends in its milestone id (M224).
const PANE_BUTTONS: Record<PaneButton, { key: string; label: string }> = {
  home: { key: 'cairn-pane-home', label: HOME_LABEL },
  status: { key: 'cairn-pane-status', label: STATUS_LABEL },
  refresh: { key: 'cairn-pane-refresh', label: REFRESH_LABEL },
  finish: { key: 'cairn-pane-finish', label: FINISH_LABEL },
  revise: { key: 'cairn-pane-revise', label: REVISE_LABEL },
  check: { key: 'cairn-pane-check', label: CHECK_LABEL },
  plan: { key: 'cairn-pane-plan', label: PLAN_CANDIDATE_LABEL },
}

// The command each blocked line's Button runs, and whether the milestone's
// id is its argument (M224). None runs `/clear` first, as the Review and
// Resume Buttons keep the conversation.
const BLOCKED_COMMANDS: Partial<Record<PaneButton, { command: string; withId: boolean }>> = {
  finish: { command: 'cairn:milestone-review', withId: true },
  revise: { command: 'cairn:milestone-implement', withId: true },
  check: { command: STATUS_COMMAND, withId: false },
}

// How long one `gh api graphql` or `gh pr view` call may run, well under
// the ten minutes `$.process.run` allows. The URLs' calls run side by side,
// and a call still running then rejects and reads as `unknown` with no
// counts (M224, M237). Each URL takes one call (M237).
const GH_TIMEOUT_MS = 15_000

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await refresh($)
    // The band does not depend on the command: a refused registration
    // leaves the band as the refresh drew it.
    try {
      await $.command.register({ name: PANE_COMMAND, description: 'Open or close the cairn pane' })
    } catch {
      // No `/cairn-pane` in this session. The band's open button still opens the pane.
    }
    // After the registration, so a slow open does not hold `/cairn-pane`
    // back (M222 review).
    await reopen($)
    return result
  })

  // A `/clear` that stays in the same process raises no `session.start`, and
  // the host's state starts empty under the new session id, so the band and
  // an open pane read the files again here (M222). A `/resume` does the same
  // (M237). The hook cannot tell a resume in the process from a resumed
  // start, so a resumed start reads the files twice. A placed pane, shown or
  // behind another tab, also reads the pull request states and the hotfix
  // list again, and the hook does not wait for that read (M230, M237). A
  // pane listed but not placed owes that read, and its first draw starts it
  // (`owed`, M238), unless the hook's second listing finds it placed and
  // reads first (M256). A start whose reopen already read starts no second read
  // and owes none (`startRead`, M238).
  on('classic.SessionStart', async ($, e, next) => {
    const result = await next(e)
    if (e.source === 'clear' || e.source === 'resume') {
      // A session end during any await below makes the hook read and owe
      // nothing, as a later start may owe the read and it is that start's
      // (M260).
      const at = ends
      await refresh($)
      if (startRead) return result
      const mine = await listedPane($)
      // A reopen that read during the await is this start's read (M238
      // review).
      if (mine == null || startRead || ends !== at) return result
      if (mine.isPlaced) {
        startRead = true
        owed = false
        void readPrs($)
        return result
      }
      owed = true
      // A pane placed and drawn during the list above drew before the read
      // was owed, so the hook lists it again and reads if it is now placed,
      // unless something cleared `owed` meanwhile: a draw, an open, a
      // session end, or another start's hook (M256), or reads nothing after
      // a session end, as above (M260).
      const again = await listedPane($)
      if (again != null && again.isPlaced && owed && ends === at) {
        owed = false
        startRead = true
        void readPrs($)
      }
    }
    return result
  })

  // `/cairn-pane` closes an open pane, and otherwise reads the files and
  // opens it, or says why it did not (M205 AC1). After the open, it starts
  // the read of the pull request states (M224), and its line does not wait
  // for that read, whose calls each have a 15 s timeout (M230).
  // Only a pane the person can see is closed: one that waits undrawn, or
  // sits behind another pane's tab, is opened again instead (M205 review).
  // A hook that refuses the open or the close gives a line, not an error.
  // The first `/cairn-pane` after the session-start reopen, before any turn
  // ends, keeps the reopened pane open: a typed `/clear` took the pane off
  // the screen, and that command is the message whose start reopened it.
  on('command.run', { command: PANE_COMMAND }, async $ => {
    const afterReopen = reopened
    reopened = false
    try {
      const mine = await paneOf($)
      if (placedAndShown(mine)) {
        if (afterReopen) return { text: 'cairn pane opened' }
        await $.ui.close({ id: PANE })
        return { text: 'cairn pane closed' }
      }
      await refresh($)
      if (!(await read($, pane)).found) return { text: NO_ROADMAP }
      const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
      owed = false
      void readPrs($)
      return { text: opened.isPlaced ? 'cairn pane opened' : notPlaced(opened.reason) }
    } catch (error) {
      return { text: `cairn pane: ${error instanceof Error ? error.message : String(error)}` }
    }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    // A pane that a clear or resume start found listed but not placed reads
    // the pull request states at its first draw (M238), unless that start's
    // second listing read first (M256). The flag clears
    // before any await, so two draws at once start one read. The read is
    // the start's read, so a reopen after it reads nothing (M238 review).
    if (owed) {
      owed = false
      startRead = true
      void readPrs($)
    }
    const { Box, Button, Text } = $.ui.resolve(e)
    // The Next line's Button shows while no cairn skill's step is set
    // (M218). A pane gets no `isWorking` prop, so it also shows during a
    // turn outside a cairn skill, and a press then waits for the session to
    // be idle, as `$.command.run` queues.
    // After that Button, the Next line shows Status at the same times
    // (M219), and the first line shows ⌂ (M241).
    const acts = knownStep(await read($, step)) === null
    const shown = await read($, band)
    const held = await read($, hotfixes)
    const ours = held.root !== null && held.root === shown.root
    const counts = await read($, repo)
    const lines = paneLines(
      await read($, pane),
      shown.rows,
      acts,
      await read($, prs),
      ours ? held.prs : [],
      ours ? held.started : [],
      counts.root !== null && counts.root === shown.root ? counts : null,
      shown.root,
    )
    // ⋯ also needs a read in flight in this module, so a stored true that a
    // reload or a failed write left draws ↻ (M237).
    const busy_ = (await read($, reading)) && inFlight > 0
    // A line's lead and tail keep their width, and its text takes the room
    // left between them: cut to one line with an ellipsis, or wrapped for
    // the goal's lines. The line Box may shrink below its content's width,
    // so a long text is cut rather than pushing the tail past the edge
    // (M208, LESSONS M194). The action Button sits after them in a Box that
    // does not shrink, so the Next command is cut first (M218), and so does Status
    // after it, and the first line's ⌂ and ↻, each in its own such Box
    // (M219, M236, M241). Off the terminal, a candidate line's ✎ Box has no
    // key and sits past the row's edge until the pointer is over the line,
    // and the info glyph before it stays hidden until then (M290). A Text drops its
    // `key`, so each line's key sits on a Box.
    // The card's lines draw in one Box with a round border in `subtle`,
    // before the rest (M286). On the desktop a line with a `full` holds a
    // hidden Box with its whole text (on a candidate line, its row's text
    // after the priority token, M293), placed above the row out of the flow,
    // which the pointer over the line reveals, or on a line with `info` the
    // pointer over its info glyph, which names the card's hover group (M290);
    // an absolute Box paints over
    // the rows before it, so it opens upward (M286). A lead span that names an icon draws it as an
    // `Svg` on a surface whose table has the element, and its glyph in the
    // terminal, and a line with one centers its row (M286).
    const Svg = e.surface === 'terminal' ? undefined : $.ui.resolve(e).Svg
    // A tail span that names a badge draws as its `Svg` pill on such a
    // surface, and as its padded text on the heading's key in the terminal
    // (M289); a heading with one centers its row too.
    const drawSpan = (span: Span) =>
      span.badge !== undefined && Svg !== undefined ? (
        <Svg
          source={badgeSvg(span.badge.count, span.badge.name)}
          alt={`${span.badge.count}`}
          width={badgeWidth(span.badge.count)}
          height={BADGE_H}
        />
      ) : span.icon !== undefined && Svg !== undefined ? (
        <Svg source={iconSvg(span.icon)} alt={span.text} width={ICON_PX} height={ICON_PX} />
      ) : (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      )
    // A line that draws the info glyph, which then alone opens its card (M290).
    const infos = (line: (typeof lines)[number]) => line.info === true && line.full !== undefined && e.surface !== 'terminal'
    const centers = (line: (typeof lines)[number]) =>
      Svg !== undefined &&
      (line.lead.some(span => span.icon !== undefined) || (line.tail ?? []).some(span => span.badge !== undefined))
        ? { alignItems: 'center' as const }
        : {}
    const drawLine = (line: (typeof lines)[number]) => (
          <Box key={line.key} paddingLeft={line.indent} minWidth={0} {...centers(line)}>
            {line.lead.length === 0 ? null : (
              <Box key={`${line.key}-lead`} flexShrink={0} {...centers(line)}>
                {line.lead.map(drawSpan)}
              </Box>
            )}
            {line.text === null ? null : (
              <Box key={`${line.key}-text`} flexShrink={1} minWidth={0} {...(line.grow ? { flexGrow: 1 } : {})}>
                <Text wrap={line.wraps ? 'wrap' : 'truncate-end'} {...style(line.text)}>
                  {line.text.text}
                </Text>
              </Box>
            )}
            {line.tail === undefined ? null : (
              // A tail that grows takes the free room, so the Buttons after
              // it sit at the right end (the card's first line, M291).
              <Box key={`${line.key}-tail`} flexShrink={0} {...(line.tailGrows ? { flexGrow: 1 } : {})} {...centers(line)}>
                {line.tail.map(drawSpan)}
              </Box>
            )}
            {line.action === undefined ? null : (
              <Box key={`${line.key}-action`} flexShrink={0} marginLeft={1}>
                <Button
                  key={PANE_NEXT}
                  variant="secondary"
                  label={line.action}
                  onPress={() => pressNext($, line.action)}
                />
              </Box>
            )}
            {!infos(line) ? null : (
              // The info glyph, hidden until the pointer is over the line,
              // when ✎ also moves in. It names the hover group that alone opens the line's
              // card, so the card no longer opens with ✎ (M290). In the
              // desktop app a Text in a group heats it and a Box that only
              // names the group does not (M290 live look). Its right margin
              // keeps the room that ✎ moves into.
              <Box
                display="none"
                hover={{ display: 'flex' }}
                flexShrink={0}
                marginLeft={1}
                marginRight={(line.buttons ?? []).includes('plan') ? PLAN_SLOT : 0}
              >
                <Text color={GRAY} hover={{ scope: infoScope(line.key), bold: true }}>
                  {INFO_LABEL}
                </Text>
              </Box>
            )}
            {(line.buttons ?? []).map(kind => {
              const button = PANE_BUTTONS[kind]
              const target = line.target
              const title = line.title
              // Off the terminal a candidate line's ✎ sits in an unkeyed Box
              // placed past the row's right edge, where the pane clips it, and
              // the pointer over the line moves it into the room the info
              // glyph keeps (M290). In the desktop app a Button drawn under
              // `display: 'none'` takes no click once revealed, and one moved
              // by an offset does. A keyed Box would scope its own hover. The
              // Box spans the row's height and centers ✎ in it, as the row
              // centers ⓘ.
              const parks = kind === 'plan' && e.surface !== 'terminal'
              return (
                <Box
                  {...(parks
                    ? {
                        position: 'absolute' as const,
                        top: 0,
                        bottom: 0,
                        alignItems: 'center' as const,
                        right: PLAN_PARK,
                        hover: { right: 0 },
                      }
                    : { key: `${line.key}-${kind}` })}
                  flexShrink={0}
                  marginLeft={1}
                >
                  <Button
                    key={target === undefined ? button.key : `${button.key}-${target}`}
                    variant="secondary"
                    label={kind === 'refresh' && busy_ ? READING_LABEL : button.label}
                    onPress={() => pressPane($, kind, target, title)}
                  />
                </Box>
              )
            })}
            {line.full === undefined || e.surface === 'terminal' ? null : (
              // No key of its own: a keyed Box would scope its own hover, and a
              // hidden scope is never under the pointer. The keyed line Box
              // opens it, or on a line with the info glyph its group (M290).
              <Box
                position="absolute"
                bottom={1}
                left={0}
                right={0}
                display="none"
                hover={infos(line) ? { display: 'flex', scope: infoScope(line.key) } : { display: 'flex' }}
                borderStyle="round"
                borderColor={METER_EMPTY_KEY}
                backgroundColor={HOVER_GROUND}
                paddingX={1}
              >
                <Text wrap="wrap">{line.full}</Text>
              </Box>
            )}
          </Box>
    )
    const card = lines.filter(line => line.card)
    return (
      <Box key="cairn-pane" flexDirection="column">
        {card.length === 0 ? null : (
          <Box key="cairn-card" flexDirection="column" borderStyle="round" borderColor={METER_EMPTY_KEY} paddingX={1}>
            {card.map(drawLine)}
          </Box>
        )}
        {lines.filter(line => !line.card).map(drawLine)}
      </Box>
    )
  })

  // A turn end reads the tracking files again and ends no step (M201). A
  // skill that waits on background work ends its turn, and the work's notice
  // starts the next one, so a turn end is not the skill's end.
  on('turn.complete', async ($, e, next) => {
    reopened = false
    const result = await next(e)
    await update($, expanded, () => false)
    await refresh($)
    return result
  })

  // The main loop's Stop ends the running cairn skill's step when nothing is
  // in flight: `background_tasks` is empty or absent, and no hook beneath
  // blocked the stop (M201). A Stop with work in flight keeps the step
  // through the wait, and so does a blocked Stop, after which the turn goes
  // on. A Stop inside a subagent carries an `agent_id` and keeps the step.
  // A one-shot entry in `session_crons`, as ScheduleWakeup makes, also keeps
  // the step, so a skill that waits on a wakeup keeps it (M210). A recurring
  // cron, as `/loop` makes, does not, since it would keep the step for good.
  on('classic.Stop', async ($, e, next) => {
    const result = await next(e)
    await update($, expanded, () => false)
    if (e.agent_id !== undefined || result?.block !== undefined) return result
    const waking = (e.session_crons ?? []).some(cron => cron.recurring === false)
    if ((e.background_tasks ?? []).length === 0 && !waking) {
      if (knownStep(await read($, step)) !== null) await update($, ended, () => true)
      await update($, step, () => null)
      await refresh($)
    }
    return result
  })

  // A prompt the operator typed, at the terminal or the desktop (`composer`)
  // or through Remote Control (`bridge`), while the session was idle (no
  // `turnId`) ends a step that a Stop kept (M201). A background task's
  // notice, a peer's message, or a prompt typed over a running turn keeps
  // it. A typed cairn slash command keeps the step its own skill prompt set:
  // the engine expands the command first, so the prompt finds `expanded`
  // set. Were the skill prompt to run beneath instead, the step would end
  // before `next` and the skill prompt would set the new one. So the step
  // ends before `next`, and a prompt that a hook beneath drops puts it back,
  // unless something set a new step meanwhile (M210).
  on('prompt.submit', async ($, e, next) => {
    const typed = e.origin.kind === 'composer' || e.origin.kind === 'bridge'
    const fresh = await read($, expanded)
    await update($, expanded, () => false)
    if (!typed || e.turnId !== undefined || fresh) return next(e)
    const before = await read($, step)
    const hiddenBefore = await read($, dismissed)
    const endedBefore = await read($, ended)
    await update($, step, () => null)
    await update($, ended, () => false)
    await refresh($)
    const result = await next(e)
    // The refresh above can clear a hide made against the old step, so a
    // drop puts back the close state as well (M210 review).
    if (result?.drop !== undefined && before !== null) {
      await update($, step, current => current ?? before)
      if (hiddenBefore !== null) await update($, dismissed, current => current ?? hiddenBefore)
      await reconcile($)
    }
    // A drop also puts back the Clear Button that a skill's end left, unless
    // a skill started meanwhile (M216).
    if (result?.drop !== undefined && endedBefore && (await read($, step)) === null) {
      await update($, ended, () => true)
    }
    return result
  })

  // A cairn skill's prompt starts its step, the same skill run again
  // included. The event carries no agent id, so a subagent that loads a
  // cairn skill starts a step too. The text passes through as is.
  on('skill.prompt', async ($, e, next) => {
    const result = await next(e)
    const skill = cairnSkill(e.skill)
    if (skill !== null) {
      await update($, step, () => ({ skill }))
      await update($, ended, () => false)
      await update($, expanded, () => true)
      await refresh($)
    }
    return result
  })

  // A file the session writes under a `cairn/` directory, such as a
  // milestone file whose box was just checked, reads the files again, so the
  // track moves inside a long turn (M206 review: the chapter hook, which
  // M206 removed, had done this at each chapter). The tool's own call goes
  // through first, and a refused or failed call reads nothing.
  on('tool.call', { tool: 'Edit' }, afterWrite)
  on('tool.call', { tool: 'Write' }, afterWrite)
  on('tool.call', { tool: 'MultiEdit' }, afterWrite)

  // Every session end, a `/clear` or a resume among them, ends the step and
  // shows a band that a press hid, whatever its reason (M200).
  on('session.end', async ($, e, next) => {
    // A `Plan`, `Implement`, or ✎ press's held command is taken first, so a
    // rejecting `next(e)` below cannot leave it set (M221 review).
    const queued = heldRun
    heldRun = null
    // So is a ⌂ press's mark (M241).
    const home = homeRun
    homeRun = null
    reopened = false
    // The end ends the start, so the next start reads again (M238).
    owed = false
    startRead = false
    // A press whose checks have not settled is cut off: its checks run
    // nothing when they settle (M255).
    ends += 1
    // The run and the press mark current now are the ones this end frees.
    // A press made while `next(e)` is pending keeps its own (M260 review).
    const runAt = runs
    const checkAt = pressCheck
    const free = () => {
      if (runs === runAt) running = false
      if (pressCheck === checkAt) pressCheck = null
    }
    // An `other` end marks this folder for a reopen at the next start
    // (M222). A `clear` end needs nothing, as no pane closes when the clear
    // stays in the same process.
    if (e.reason === 'other') await markReopen($)
    let result: unknown
    let failed: { error: unknown } | null = null
    try {
      result = await next(e)
    } catch (error) {
      failed = { error }
    }
    // An end beneath that rejects resets the band as a resolved end does
    // (M278). A write that rejects stops the resets but none of what
    // follows, and its error goes on after them unless `next(e)` rejected
    // first (M278 review).
    let wrote: { error: unknown } | null = null
    try {
      await update($, step, () => null)
      await update($, expanded, () => false)
      await update($, dismissed, () => null)
      await update($, ended, () => false)
    } catch (error) {
      wrote = { error }
    }
    // A `/clear` from the Clear Button ends the session, and its run may
    // never settle, so the end frees the action Buttons (M216). So does a
    // press whose checks have not settled, once the end's own updates are
    // done, so no press reads the state of the session that ended (M255).
    // An end beneath that rejects frees them too, so a press whose `/clear`
    // run never settles leaves none dead (M260).
    free()
    // The held command runs now when this end is its `/clear` (M221). The
    // run is not awaited, so the session end does not wait on the command.
    // It takes the next run number, so the `/clear` run that settles after
    // this end does not free a press made while the command runs. Any other
    // end drops the command, and the prompt box and a toast say so, as for
    // a refused run (M221 review). An end beneath that rejects drops it
    // whatever its reason (M260).
    if (queued !== null) {
      if (failed !== null) void fallBack($, lineOf(queued.command, queued.args), 'the session end failed')
      else if (e.reason === 'clear') void run($, queued.command, queued.args)
      else void fallBack($, lineOf(queued.command, queued.args), 'the session ended before /clear')
    }
    // A ⌂ press's `/clear` opens the pane at its end, unawaited as the held
    // command's run is, and also when the end beneath rejects (M255). Any
    // other end drops the mark with no open (M241).
    if (home !== null && e.reason === 'clear') void openHome($)
    if (failed !== null) throw failed.error
    if (wrote !== null) throw wrote.error
    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const state = await read($, band)
    const { rows, workable } = state
    const current = knownStep(await read($, step))
    // A row drawn from a found ROADMAP carries the pane's open button
    // (M205), and with no active or workable row it is the empty row (M213).
    const { found: canOpen, next: nextStep } = await read($, pane)
    if (rows.length === 0 && workable.length === 0 && !canOpen) return next(e)
    const hidden = await read($, dismissed)
    if (hidden !== null && same(hidden, mark(state, current))) return next(e)
    const beneath = await next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    // The track draws as the `Svg` element on every surface whose table has
    // one, the desktop app's among them (M204), and as braille cells in the
    // terminal (M206). With the image, the row centers its parts, since the
    // track is taller than text.
    const Svg = e.surface === 'terminal' ? undefined : $.ui.resolve(e).Svg
    const center = Svg === undefined ? {} : { alignItems: 'center' as const }
    const close = CLOSE_COLUMNS + (canOpen ? OPEN_COLUMNS : 0)
    // The next-step and status Buttons (M212) show while no cairn skill's
    // step is set and no turn is working, on a row that has room for them
    // (band.ts `actionsFit`). The track gives up columns to them; without
    // them the row draws its track or label alone, and the idle row draws
    // no command in their place (M220). The next step is the
    // pane's: a milestone's step on a milestone or idle row, and planning
    // on the empty row (M213).
    const nextLabel = nextStep == null ? undefined : labelOf(nextStep.action)
    const canAct = canOpen && nextLabel !== undefined && current === null && e.props.isWorking !== true
    // Each action Button draws with its chrome, so the terminal draws it as
    // `[ label ]`: its label and 4 columns. One space follows each. Both take
    // the `secondary` look: an accent color beside the track's phase colors
    // clashed at a live look.
    // The Clear Button (M216) shows with them after a cairn skill ends, and
    // the row drops it first when the three do not fit.
    const actionColumns = nextLabel === undefined ? 0 : width(nextLabel) + 4 + 1 + width(STATUS_LABEL) + 4 + 1
    const clearColumns = width(CLEAR_LABEL) + 4 + 1
    const tries = !canAct ? [] : (await read($, ended)) ? [actionColumns + clearColumns, actionColumns] : [actionColumns]
    let acts = false
    let clears = false
    let lines: BandLine[] = []
    for (const taken of tries) {
      const reserved = close + taken
      const withActs = stepLines(rows, current, e.props.bodyColumns, reserved, workable, canOpen)
      if (withActs.length > 0 && actionsFit(withActs[0], e.props.bodyColumns, reserved)) {
        acts = true
        clears = taken > actionColumns
        lines = withActs
        break
      }
    }
    if (!acts) lines = stepLines(rows, current, e.props.bodyColumns, close, workable, canOpen)
    const spans = (list: Span[]) =>
      list.map(span => (
        <Text wrap="truncate-end" {...style(span)}>
          {span.text}
        </Text>
      ))
    const track = (line: BandLine) => {
      if (line.track === undefined) return null
      if (Svg === undefined) return spans(brailleSpans(line.track.flow, line.track.columns))
      const px = Math.min(TRACK_PX, line.track.columns * PX_PER_COLUMN)
      return <Svg source={trackSvg(line.track.flow, px)} alt={line.track.flow.alt} width={px} height={TRACK_H} />
    }

    // Two groups: the bold id and the title on the left, where the title
    // gives way first, and the track and the tail on the right, which keep
    // their width. The engine cuts the title to the room that is left.
    // A shrinking Box also takes `minWidth: 0`, and the id sits in a Box
    // that never shrinks. Without both, the desktop app drew a long text at
    // full width past the edge with no `…`, and the short parts beside it
    // shrank to nothing (M194). The empty row has no id, so no head (M213).
    const row = (line: BandLine, isFirst: boolean) => (
      <Box key={line.key} justifyContent="space-between" {...center}>
        <Box key={`${line.key}-left`} flexShrink={1} minWidth={0}>
          {line.id === '' ? null : (
            <Box key={`${line.key}-head`} flexShrink={0}>
              <Text wrap="truncate-end" color={GRAY} bold>
                {line.id}
              </Text>
              <Text wrap="truncate-end">{' '}</Text>
            </Box>
          )}
          <Box key={`${line.key}-text`} flexShrink={1} minWidth={0}>
            <Text wrap="truncate-end" color={GRAY}>
              {line.title}
            </Text>
          </Box>
        </Box>
        <Box key={`${line.key}-right`} flexShrink={0} marginLeft={GAP} {...center}>
          {track(line)}
          {spans(line.tail)}
          {isFirst ? (
            <Text wrap="truncate-end">{' '.repeat(GAP)}</Text>
          ) : null}
          {isFirst && clears ? (
            <Button key="cairn-clear" variant="secondary" label={CLEAR_LABEL} onPress={() => pressClear($)} />
          ) : null}
          {isFirst && clears ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && acts ? (
            <Button
              key="cairn-next"
              variant="secondary"
              label={nextLabel}
              onPress={() => pressNext($, nextLabel)}
            />
          ) : null}
          {isFirst && acts ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && acts ? (
            <Button key="cairn-status" variant="secondary" label={STATUS_LABEL} onPress={() => pressStatus($)} />
          ) : null}
          {isFirst && acts ? <Text wrap="truncate-end">{' '}</Text> : null}
          {isFirst && canOpen ? (
            <Button
              key="cairn-open"
              plain
              {...(e.surface === 'terminal' ? {} : { dimColor: true })}
              label={OPEN_GLYPH}
              onPress={() => openPane($)}
            />
          ) : null}
          {isFirst && canOpen ? <Text wrap="truncate-end">{' '.repeat(OPEN_COLUMNS - width(OPEN_GLYPH))}</Text> : null}
          {isFirst ? (
            <Button
              key="cairn-close"
              role="dismiss"
              plain
              {...(e.surface === 'terminal' ? {} : { dimColor: true })}
              label={e.surface === 'terminal' ? CLOSE_GLYPH : DESKTOP_CLOSE_GLYPH}
              onPress={() => dismiss($)}
            />
          ) : null}
        </Box>
      </Box>
    )

    return (
      <Box key="cairn-stack" flexDirection="column">
        <Box key="cairn-band" flexDirection="column">
          {/* A Text drops its `key`, so each row's key sits on a Box. */}
          {lines.map((line, i) => row(line, i === 0))}
        </Box>
        {beneath ?? null}
      </Box>
    )
  })
}

// After an Edit, Write, or MultiEdit call that went through, a path under a
// `cairn/` directory reads the files again.
async function afterWrite($, e, next) {
  const result = await next(e)
  if (result?.deny !== undefined || result?.isError === true) return result
  if (typeof e.file_path === 'string' && /(^|[\\/])cairn[\\/]/.test(e.file_path)) await refresh($)
  return result
}

// The press reads the rows and the step as they are now, not as they were
// drawn. It writes only while the close state stands at the version it had
// before those reads, so a session end that lands between them wins and the
// band stays shown (M210). Any other write in between drops the press too,
// and a second press hides the band.
async function dismiss($) {
  const held = await $.state.get(DISMISSED_REF)
  const state = await read($, band)
  const current = await read($, step)
  await $.state.set(DISMISSED_REF, { shape: DISMISSED_SHAPE, value: mark(state, current) }, { ifVersion: held.version })
}

// A press of the band's open button opens the pane. The press is the
// person's own act, so the surface places the pane at any width.
// A press has no output line, so an open the surface does not place, or one
// a hook refuses, says why in a toast. An open that does not throw starts
// the read of the pull request states (M224), and the press does not wait
// for it (M230).
async function openPane($) {
  try {
    const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
    if (!opened.isPlaced) $.ui.toast(notPlaced(opened.reason))
  } catch (error) {
    $.ui.toast(`cairn pane: ${error instanceof Error ? error.message : String(error)}`)
    return
  }
  owed = false
  void readPrs($)
}

// The pane as `$.ui.panes()` lists it, or undefined when it is not listed.
// It throws when that call throws. Every other place that needs the pane's
// listing reads it here (M238).
async function paneOf($) {
  return (await $.ui.panes()).find(open => open.id === PANE)
}

// The pane as `paneOf` lists it, or null when the call throws (M238).
async function listedPane($) {
  try {
    return await paneOf($)
  } catch {
    return null
  }
}

// True when `$.ui.panes()` lists the pane placed and shown, false when it
// does not or the call throws.
async function isShown($): Promise<boolean> {
  return placedAndShown(await listedPane($))
}

// True when a listing of the pane, as `paneOf` or `listedPane` gives it,
// is placed and shown. The command's close, `isShown`, and `markReopen`
// test the listing here (M256).
function placedAndShown(mine: { isPlaced: boolean; isShown: boolean } | null | undefined): boolean {
  return mine != null && mine.isPlaced && mine.isShown
}

// Each read of the pull request states takes the next number, and only the
// newest read started writes its words, so an older read that settles
// later does not put back older words (M224 review). A reload starts it
// over at 0.
let prReads = 0

// True from a clear or resume start that finds the pane listed but not
// placed until the pane's next draw starts the read it owes, the start's
// second listing finds the pane placed and reads (M256), an open reads, or
// the session ends (M238). A reload starts it over as false.
let owed = false

// True from the read that a start's reopen, its clear or resume hook, or
// the first draw that hook owed starts until the next session end, so the
// other hook of the same start starts no second read and owes none (M238).
// A reload starts it over as false.
let startRead = false

// The reads of the pull request states that this module started and that
// have not settled (M237). A reload starts it over at 0, as the reload ends
// the old module's reads.
let inFlight = 0

// Reads each blocked row's pull request with one call per URL, side by
// side, and writes each state word and its counts by its URL (M224, M225).
// A github.com URL takes one `gh api graphql` call for both (`readPr`,
// M237), and the URL names the repo, so the call needs no `--repo`. A call
// that rejects, as when `gh` cannot start or outruns its timeout, reads as
// `unknown` with no counts, as a bad result does (counts.ts `prRead`), and
// the read never throws. Threads that fail the shape check leave the word
// and draw no counts. It runs only at a pane open, a Refresh press, a
// `/clear` or `/resume` while the pane is placed (M230, M237), and the
// first draw of a pane that such a start found not placed (M238). A start
// reads once: its reopen and its clear or resume hook skip the read when
// the other, or the owed draw, already read (M238). No timer and no turn
// end starts one, since the operator does not want repeating tasks.
// A read that starts while another runs still runs, with the newest URLs.
// Words and counts are written together when every call has settled, so a
// Refresh keeps the earlier counts drawn until then.
// Beside the blocked rows' reads, `readHotfixes` lists the open hotfix pull
// requests (M226), and the blocked reads do not wait for it (M230). Once the
// list settles, the hotfix URLs that no blocked row names are read. The list
// is written with the words.
async function readPrs($) {
  prReads += 1
  const mine = prReads
  inFlight += 1
  // Each write checks again inside `update`, which retries on a version
  // conflict, that no newer read started, so a retried write never undoes a
  // newer read's write (M236 review).
  try {
    await update($, reading, current => (mine === prReads ? true : current))
  } catch {
    // The ↻ stays, and the read still runs.
  }
  try {
    const urls: string[] = []
    for (const row of (await read($, pane)).blocked) {
      if (row.url !== null && !urls.includes(row.url)) urls.push(row.url)
    }
    // One lookup of the root and its base remote's URL serves the hotfix
    // list and the card's read (M286). Neither the blocked reads nor the
    // words and list they write wait for the card's read, which is written
    // last (M286 review, as M230 keeps the blocked reads apart). A lookup
    // that rejects rejects both, so nothing is written; the card's
    // rejection is held so it is never unhandled.
    const where = baseOf($)
    const listing = readHotfixes($, where)
    const card = readRepo($, where).catch(() => null)
    const blocked = urls.map(url => readPr($, url))
    const listed = await listing
    const more: string[] = []
    for (const pr of listed.prs) {
      if (!urls.includes(pr.url) && !more.includes(pr.url)) more.push(pr.url)
    }
    urls.push(...more)
    // Each write checks inside `update`, which retries on a version
    // conflict, that no newer read started, so a retried write never
    // replaces a newer read's value (M236 review, M286 review).
    const newest = <T,>(value: T) => (current: T) => (mine === prReads ? value : current)
    if (urls.length > 0) {
      const reads = await Promise.all([...blocked, ...more.map(url => readPr($, url))])
      const out: Record<string, PrRead> = {}
      urls.forEach((url, i) => {
        out[url] = reads[i]
      })
      // A newer read that settles between the two writes keeps its list
      // (M226 review).
      if (mine === prReads) await update($, prs, newest(out))
    }
    if (mine === prReads) await update($, hotfixes, newest(listed))
    const counted = await card
    if (counted !== null && mine === prReads) await update($, repo, newest(counted))
  } catch {
    // No write: the lines keep the words they had.
  } finally {
    inFlight -= 1
    // Only the newest read puts back the ↻, so an older read that settles
    // first leaves ⋯ while the newer one runs (M236).
    if (mine === prReads) {
      try {
        await update($, reading, current => (mine === prReads ? false : current))
      } catch {
        // The stored value stays true, and once no read of this module is
        // in flight, the next draw shows ↻ (M237). A change to `inFlight`
        // draws nothing, so this asks for the pane to be drawn again (M237
        // review). No test covers that redraw.
        try {
          $.ui.invalidate('ui.render')
        } catch {
          // The ⋯ stays until something else draws the pane.
        }
      }
    }
  }
}

// One pull request's state word, and its counts when the word says it is
// open, as `readPrs` describes. It never rejects. A github.com URL takes one
// `gh api graphql` call for both (counts.ts `prRead`, M237). A URL of
// another form, as a hotfix's on another host, takes one `gh pr view` call
// for its word and gets no counts.
async function readPr($, url: string): Promise<PrRead> {
  const graph = countsArgv(url)
  if (graph !== null) {
    try {
      return prRead(await $.process.run(graph, { timeoutMs: GH_TIMEOUT_MS }))
    } catch {
      return prRead(null)
    }
  }
  try {
    const argv = ['gh', 'pr', 'view', url, '--json', 'state,reviewDecision']
    return { word: prWord(await $.process.run(argv, { timeoutMs: GH_TIMEOUT_MS })), counts: null }
  } catch {
    return { word: prWord(null), counts: null }
  }
}

// The hotfix list to write, read with one `gh pr list` call on the base
// remote of the band's repo root (M226). The base remote is the one
// `base_remote` in hooks/cairn_common.py picks: `upstream` in guest mode
// when `git remote` lists it, else `origin`. The call names the remote's
// URL, which `gh` takes as `--repo` (M226 T1), and runs in the root. With
// no root or no URL for the base remote, it runs no call, and the list is
// empty. A call that fails keeps the last good list when it was read for
// the same root, and is empty otherwise. A good read replaces it, an empty
// one included. The same result gives the candidate rows that the listed
// bodies name (`startedRows`, M252), kept and emptied with the list.
async function readHotfixes($, where: Promise<Where>): Promise<CairnHotfixRead> {
  const { root, url } = await where
  if (root === null) return { root: null, prs: [], started: [] }
  if (url === null) return { root, prs: [], started: [] }
  let got: HotfixPr[] | null
  let started: StartedRow[] | null
  try {
    const result = await $.process.run(listArgv(url), { cwd: root, timeoutMs: GH_TIMEOUT_MS })
    got = hotfixPrs(result)
    started = startedRows(result)
  } catch {
    got = null
    started = null
  }
  if (got !== null && started !== null) return { root, prs: got, started }
  const held = await read($, hotfixes)
  return held.root === root ? held : { root, prs: [], started: [] }
}

// The band's repo root, whether it is in guest mode, and its base remote's
// URL, read once per `readPrs` (M286). With no root, the URL is null and no
// call runs.
type Where = { root: string | null; guest: boolean; url: string | null }
async function baseOf($): Promise<Where> {
  const root = (await read($, band)).root
  if (root === null) return { root: null, guest: false, url: null }
  const profile = await readText($, join(root, 'cairn/PROFILE.md'))
  const guest = profile !== null && collaborationMode(profile) === 'guest'
  return { root, guest, url: await baseRemoteUrl($, root, guest) }
}

// The summary card's numbers to write (M286), read with one `gh api
// graphql` call on the base remote's repo and three git calls in the root,
// and a fourth for the name when the URL is not a github.com one.
// The GitHub numbers come from a github.com base remote only. A read that
// gives none keeps the last good numbers for the same root, and is empty
// for any other root. The release read (tag, days, done count) is this
// read's alone: null in guest mode, with no release tag, or when a git call
// fails. The project name is this read's too (`projectName` in repo.ts,
// M291): a URL that is not a github.com one, or no URL, takes one more git
// call for the common git dir. It rejects only when the root and remote
// lookup rejects.
async function readRepo($, where: Promise<Where>): Promise<CairnRepoRead> {
  // The days count to the read's start, taken before the root lookup
  // (M286 review, Copilot).
  const now = Date.now()
  const { root, guest, url } = await where
  if (root === null) return { root: null, counts: null, done: null, name: null }
  const argv = url === null ? null : repoArgv(url)
  const naming = async () => projectName(url, argv === null ? await git($, root, COMMON_DIR_ARGS) : null, root)
  const ask = async () => {
    if (argv === null) return null
    try {
      return repoCounts(await $.process.run(argv, { cwd: root, timeoutMs: GH_TIMEOUT_MS }))
    } catch {
      return null
    }
  }
  const count = async () => {
    if (guest) return null
    const tag = await git($, root, DESCRIBE_ARGS)
    const trimmed = tag?.trim() ?? ''
    if (trimmed === '') return null
    const [log, diff] = await Promise.all([git($, root, tagTimeArgs(trimmed)), git($, root, archivedArgs(trimmed))])
    return doneSince(guest, tag, log, diff, now)
  }
  const [counts, done, name] = await Promise.all([ask(), count(), naming()])
  if (counts !== null) return { root, counts, done, name }
  let held: CairnRepoRead
  try {
    held = await read($, repo)
  } catch {
    held = { root: null, counts: null, done: null, name: null }
  }
  return { root, counts: held.root === root ? held.counts : null, done, name }
}

// The `gh pr list` call for the operator's open pull requests on a remote
// (M226), with each body for its `Candidate row:` lines (M252). A list
// longer than the limit is cut at it.
const LIST_LIMIT = 100
function listArgv(url: string): string[] {
  return [
    'gh',
    'pr',
    'list',
    '--repo',
    url,
    '--state',
    'open',
    '--author',
    '@me',
    '--limit',
    `${LIST_LIMIT}`,
    '--json',
    'number,title,url,headRefName,body',
  ]
}

// The base remote's URL for a root, or null when `git remote get-url`
// fails or prints nothing (M226). An `http://` or `https://` URL loses its
// userinfo, such as `user:token@`, so no credential reaches the `gh` argv,
// and every other form is kept as it is (M230).
async function baseRemoteUrl($, root: string, guest: boolean): Promise<string | null> {
  let base = 'origin'
  if (guest) {
    const names = await git($, root, ['remote'])
    if (names !== null && names.split(/\s+/).includes('upstream')) base = 'upstream'
  }
  const url = (await git($, root, ['remote', 'get-url', base]))?.trim() ?? ''
  return url === '' ? null : withoutUserinfo(url)
}

// A URL with the userinfo of an `http://` or `https://` authority removed:
// everything after the scheme's `//` up to the last `@` before the first
// `/`, `?`, or `#`.
function withoutUserinfo(url: string): string {
  const scheme = /^https?:\/\//i.exec(url)
  if (scheme === null) return url
  const rest = url.slice(scheme[0].length)
  const end = rest.search(/[/?#]/)
  const authority = end === -1 ? rest : rest.slice(0, end)
  const at = authority.lastIndexOf('@')
  return at === -1 ? url : scheme[0] + rest.slice(at + 1)
}

// A git call's stdout in a root, or null when it rejects or exits non-zero.
async function git($, root: string, args: string[]): Promise<string | null> {
  try {
    const got = await $.process.run(['git', ...args], { cwd: root, timeoutMs: GH_TIMEOUT_MS })
    return got.exitCode === 0 ? got.stdout : null
  } catch {
    return null
  }
}

// A press of a pane Button (M219, M224). The ↻ Refresh goes to
// `pressRefresh` (M236), and a candidate line's ✎ to `pressCandidate`
// (M242).
async function pressPane($, kind: PaneButton, target: string | undefined, title?: string) {
  if (kind === 'home') return pressHome($)
  if (kind === 'plan') return target === undefined || title === undefined ? undefined : pressCandidate($, target, title)
  if (kind === 'status') return pressStatus($)
  if (kind === 'refresh') return pressRefresh($)
  if (target !== undefined) return pressBlocked($, kind, target)
}

// True from a ↻ press until the read it started settles (M236). A module
// variable, so a reload, which ends that read, starts it over as false, and
// a press after a reload reads again even while the stored `reading` is
// true.
let pressing = false

// A press of the ↻ Refresh reads the files, then the hotfix list and the
// pull request states again (M224, M226). A press while an earlier press's
// read runs does nothing (M236).
async function pressRefresh($) {
  if (pressing) return
  pressing = true
  try {
    await refresh($)
    await readPrs($)
  } finally {
    pressing = false
  }
}

// A press of a blocked line's Button runs its command as a typed command
// would, through `run` with no `/clear` first, as the Status press does
// (M224). It reads the row's state word as it is now, not as it was drawn,
// and does nothing when that word no longer carries this Button, while
// another Button's run is in flight, or while a cairn skill's step runs,
// as the Status press does (M224 review). Its checks run under the shared
// press mark (M243).
async function pressBlocked($, kind: PaneButton, id: string) {
  await pressChecked($, async () => {
    if (knownStep(await read($, step)) !== null) return undefined
    const row = (await read($, pane)).blocked.find(each => each.id === id)
    if (row === undefined || row.url === null) return undefined
    const words = await read($, prs)
    const word = Object.prototype.hasOwnProperty.call(words, row.url) ? words[row.url].word : undefined
    const route = BLOCKED_COMMANDS[kind]
    if (word === undefined || PR_BUTTON[word] !== kind || route === undefined) return undefined
    return { command: route.command, args: route.withId ? id : '' }
  })
}

// True while an action Button's run is in flight, so a second press, such
// as a double click, does not queue the command again (M212 review). A
// reload starts it over as false. Each run takes the next number in
// `runs`, and only the latest run clears `running` as it settles, so a run
// from before a session end that settles late does not free a newer run's
// press (M216 review).
let running = false
let runs = 0

// The command a `Plan`, `Implement`, or candidate ✎ press holds from the
// press until the next session end, which runs it when the end's reason is
// `clear` (M221, M242).
// While it is set, a press does nothing, as while a run is in flight. A
// refused `/clear` drops it. A reload starts it over as null.
let heldRun: { command: string; args: string } | null = null

// A ⌂ press's mark, set from the press until the next session end, which
// opens the pane when the end's reason is `clear` (M241). While it is set,
// a press does nothing, as while `heldRun` is set. A refused `/clear`
// drops it. A reload starts it over as null.
let homeRun: object | null = null

// A press of the next-step Button reads the next step and the step as they
// are now, not as they were drawn, as the close press does (M212 review). A
// cairn skill that started since the drawing, or no next step, makes the
// press do nothing. A Button drawn for a milestone (`Implement`, `Resume`,
// `Review`) also does nothing when the next step no longer names one, as
// in M212 (M213 review). `Plan` runs the next step as it is now, which is
// planning while nothing is workable (M213), with the short title of the
// first `[high]` candidate row the Candidates list draws as its argument
// (`nextTitle`, M272, M273), and with none when the list draws no such row.
// `Plan` and `Implement` run `/clear` first and hold the command for the
// session end it brings (M221). The press is the person's consent to drop
// the conversation, as a press of Clear is (M216), so it clears only when
// the drawn label is the next step's label as it is now: a `Resume` or
// `Review` drawing whose next step has since become planning or implement
// runs the command and keeps the conversation (M221 review). Its checks run
// under the shared press mark (M243).
async function pressNext($, drawn: string | undefined) {
  await pressChecked($, async () => {
    if (knownStep(await read($, step)) !== null) return undefined
    const shown = await read($, pane)
    const next = shown.next
    if (next === null) return undefined
    if (next.id === null && drawn !== PLAN_LABEL) return undefined
    const clears = CLEARS_FIRST.includes(next.action) && drawn === labelOf(next.action)
    // The title the Next line names, under the Candidates list's own hide
    // rule (M272, M273).
    const held = await read($, hotfixes)
    const ours = held.root !== null && held.root === (await read($, band)).root
    const args =
      next.id ??
      nextTitle(next, shown.candidates, shown.taken, ours ? held.prs : [], ours ? held.started : []) ??
      ''
    return { command: `cairn:${next.command.slice(1)}`, args, clears }
  })
}

// True while a run is in flight, a command or a ⌂ press waits for its
// `/clear`, or a Status, Clear, next-step, blocked-line, or ✎ press runs
// its checks (M242, M243).
function busy(): boolean {
  return running || heldRun !== null || homeRun !== null || pressCheck !== null
}

// A press of Status runs `/cairn:milestone` while no step is set. Its
// checks run under the shared press mark (M243).
async function pressStatus($) {
  await pressChecked($, async () => (knownStep(await read($, step)) !== null ? undefined : { command: STATUS_COMMAND, args: '' }))
}

// A press of Clear runs the built-in `/clear` (M216), under the same checks
// as the other action Buttons. It also reads `ended` as it is now, so a
// press of a drawing made before a typed prompt, a skill, or a session end
// cleared it does nothing (M216 review). Its checks run under the shared
// press mark (M243).
async function pressClear($) {
  await pressChecked($, async () => {
    if (knownStep(await read($, step)) !== null || !(await read($, ended))) return undefined
    return { command: CLEAR_COMMAND, args: '' }
  })
}

// The shared press mark, set from a press's entry while its checks read the
// step and the stored state, so a second press, in the same tick or later,
// finds `busy` true (M243, from the ✎ press's mark of M242). The press
// clears it when its checks end, in the same tick as `run` sets `running`
// or the press sets `heldRun`. A session end clears it too (M255). A reload
// starts it over as null.
let pressCheck: object | null = null

// The number of session ends so far, so a press can tell that an end came
// while its checks ran (M255), and so can a ⌂ press's step read and a
// start's second pane listing (M260). A reload starts it over.
let ends = 0

// What a press's checks give: a command to run, or, with `clears`, a
// command to hold for the session end of a `/clear` run first (M221).
type Checked = { command: string; args: string; clears?: boolean }

// Runs a press's checks under the shared press mark, then its command
// (M243). A press while `busy` does nothing, and a press whose checks give
// no command runs nothing and frees the mark. A held command is set only
// after the checks, so a session end during them runs none (M242 review).
// A session end frees the mark, and checks that settle after an end began
// run and hold nothing (M255).
// The hold is set before the mark's release, and no await comes between
// the release and `run`, so no other press passes `busy` in that gap. A
// refused `/clear` drops the hold.
async function pressChecked($, checks: () => Promise<Checked | undefined>) {
  if (busy()) return
  const mark = {}
  pressCheck = mark
  const at = ends
  let got: Checked | undefined
  let mine: { command: string; args: string } | null = null
  try {
    got = await checks()
    if (ends !== at) got = undefined
    else if (got?.clears) {
      mine = { command: got.command, args: got.args }
      heldRun = mine
    }
  } finally {
    if (pressCheck === mark) pressCheck = null
  }
  if (got === undefined) return
  if (mine === null) {
    await run($, got.command, got.args)
    return
  }
  if (!(await run($, CLEAR_COMMAND, '')) && heldRun === mine) heldRun = null
}

// A press of the pane's ⌂ runs the built-in `/clear` under the same checks
// as Clear, less `ended`, and marks the press for the session end the
// clear brings, which opens the pane (M241). The press is the person's
// consent to drop the conversation, as a press of Clear is. The mark is set
// before the press's first await, so a second press in the same tick finds
// `busy` true (M241 review, PR #251), and a step found set takes it back.
// A session end during the step read cancels the press, so its `/clear`
// never reaches the conversation that follows (M260). A step read that
// rejects takes the mark back too, and the rejection goes on (M278).
async function pressHome($) {
  if (busy()) return
  const mine = {}
  homeRun = mine
  const at = ends
  let stop = true
  try {
    stop = knownStep(await read($, step)) !== null || ends !== at
  } finally {
    if (stop && homeRun === mine) homeRun = null
  }
  if (stop) return
  if (!(await run($, CLEAR_COMMAND, '')) && homeRun === mine) homeRun = null
}

// A press of a candidate line's ✎ runs `/clear` and holds
// `/cairn:milestone-plan` with the row's short title for the session end
// that the clear brings, as a `Plan` press holds its command (M242). The
// press is the person's consent to drop the conversation, as a press of
// Plan is. It does nothing when a step is set, when the stored pane state
// would draw no candidate rows (no ROADMAP found, or an active milestone),
// or when the stored row at the drawn index is missing or has another
// title, or when the stored read for the band's root holds an item with
// that title (M252 review). Its checks run under the shared press mark, and `pressChecked`
// holds the command only after them, as for `Plan` (M242 review, M243).
async function pressCandidate($, index: string, title: string) {
  await pressChecked($, async () => {
    const state = await read($, pane)
    const rows = state.candidates
    const row = Object.prototype.hasOwnProperty.call(rows, index) ? rows[Number(index)] : undefined
    const drawn = state.found && state.milestones.length === 0 && row?.title === title
    if (!drawn || knownStep(await read($, step)) !== null) return undefined
    // A row that an open pull request's body names (M252), or that a
    // counted started token marks (M258), draws no line (M261), so a press
    // from a drawing made before the row was hidden plans nothing. No test
    // reaches it, since the test kit presses only the current drawing.
    const held = await read($, hotfixes)
    const ours = held.root !== null && held.root === (await read($, band)).root
    const { numbers, ids } = startedRefs(title, state.taken, ours ? held.prs : [], ours ? held.started : [])
    if (numbers.length > 0 || ids.length > 0) return undefined
    return { command: PLAN_COMMAND, args: title, clears: true }
  })
}

// The open at the session end of a ⌂ press's `/clear` (M241). A Button's
// `/clear` keeps the pane open (M222), and the open asks the surface to
// show it again. The API documents only that an open of an open id
// retitles it, so whether a pane behind another tab comes forward was not
// checked live. The open is unasked, so a pane that waits undrawn below the
// width floor stays undrawn. The clear's start reads the files and the pull
// requests (M237, M238), so this open starts no read. A refused or unplaced
// open says why in a toast, as the band's open button does.
async function openHome($) {
  try {
    const opened = await $.ui.open({ id: PANE, title: PANE_TITLE })
    if (!opened.isPlaced) $.ui.toast(notPlaced(opened.reason))
  } catch (error) {
    $.ui.toast(`cairn pane: ${error instanceof Error ? error.message : String(error)}`)
  }
}

// An action Button's command runs as if the person typed it (M212). A run
// that rejects puts the command line after the prompt box's draft, so the
// person can send it, and a toast says why and names the command line, for
// a box that could not take it. It answers false for a run that rejects.
async function run($, command: string, args: string): Promise<boolean> {
  running = true
  runs += 1
  const mine = runs
  try {
    await $.command.run({ command, args })
    return true
  } catch (error) {
    await fallBack($, lineOf(command, args), error instanceof Error ? error.message : String(error))
    return false
  } finally {
    if (runs === mine) running = false
  }
}

// A command's line as the person would type it.
function lineOf(command: string, args: string): string {
  return args === '' ? `/${command}` : `/${command} ${args}`
}

// Puts a command line that did not run after the prompt box's draft, and
// toasts why (M212). A held command that a session end dropped goes the
// same way (M221 review).
async function fallBack($, text: string, why: string) {
  try {
    await $.prompt.fill({ text, mode: 'append' })
  } catch {
    // A fill that rejects leaves the draft as it was; the toast still
    // names the refusal.
  }
  try {
    await $.ui.toast(`cairn: ${why} (${text})`)
  } catch {
    // No toast shows; the press has nothing else to say.
  }
}

// Marks the session's folder for a reopen when the pane is open and shown
// (M222). A store or pane call that fails marks nothing.
async function markReopen($) {
  try {
    const mine = await paneOf($)
    if (!placedAndShown(mine)) return
    const cwd = await $.session.root()
    const held = await reopenList($)
    if (!held.includes(cwd)) await $.store.set(REOPEN_KEY, [...held, cwd])
  } catch {
    // No mark: the next start opens no pane.
  }
}

// True from a session-start reopen that opened a pane not shown before it
// until the next `/cairn-pane`, turn end, or session end. A reload starts
// it over as false.
let reopened = false

// At the first start in a marked folder, clears the mark and, when the
// refresh found a ROADMAP, opens the pane (M222). A reopen that is not placed waits
// with no toast, and a refused one gives nothing. An open starts the read of
// the pull request states (M224), and the start does not wait for it (M230).
// A start that already read, by its resume or clear hook or by the draw
// that hook owed, starts no second read (M238).
async function reopen($) {
  try {
    const cwd = await $.session.root()
    const held = await reopenList($)
    if (!held.includes(cwd)) return
    await $.store.set(REOPEN_KEY, held.filter(each => each !== cwd))
    if (!(await read($, pane)).found) return
    const before = await isShown($)
    await $.ui.open({ id: PANE, title: PANE_TITLE })
    reopened = !before
  } catch {
    // No reopen.
    return
  }
  // The reopen is an open, so it reads the pull request states (M224),
  // unless this start already read them, by its resume or clear hook or by
  // the draw that hook owed (M238).
  owed = false
  if (startRead) return
  startRead = true
  void readPrs($)
}

async function reopenList($): Promise<string[]> {
  const held = await $.store.get(REOPEN_KEY)
  return Array.isArray(held) ? held.filter((each): each is string => typeof each === 'string') : []
}

function notPlaced(reason: string): string {
  return `cairn pane not placed: ${reason}`
}

// A change to the active ids, statuses, or order, to the running skill, or
// to the idle row's id brings the band back, and it stays until the next
// press. The end of a skill's step is a change to the running skill. The
// decision reads the close state at a version and clears it only at that
// version, so a press made while `reconcile` reads the `band` and `step`
// values is compared, not lost, and it is kept when those reads match it
// (M200, M210 review). A hook that changes the rows or the step before the
// clear can still clear a press made against the new state, because the
// comparison uses the old reads. With nothing to clear, it writes nothing
// (M210).
async function reconcile($) {
  const now = mark(await read($, band), await read($, step))
  for (let tries = 0; tries < 3; tries += 1) {
    const held = await $.state.get(DISMISSED_REF)
    const hidden = held.value !== undefined && held.value.shape === DISMISSED_SHAPE ? held.value.value : null
    if (hidden === null || same(hidden, now)) return
    const done = await $.state.set(DISMISSED_REF, { shape: DISMISSED_SHAPE, value: null }, { ifVersion: held.version })
    if (done.isSet) return
  }
}

// A span's style props, leaving out the ones it does not set.
function style(span: Span) {
  const props: { color?: string; backgroundColor?: string; bold?: boolean } = {}
  if (span.color !== undefined) props.color = span.color
  if (span.backgroundColor !== undefined) props.backgroundColor = span.backgroundColor
  if (span.bold) props.bold = true
  return props
}

// No ROADMAP found empties the band and the pane. A found ROADMAP that
// cannot be read, or whose text is empty or only whitespace, keeps the rows
// and the pane as they were (M200), and so does a throw while parsing it,
// but only when the kept rows came from the same root (M210). A failed read
// in another root, a throw from `$.session.cwd()`, and kept rows with no
// root all empty the band and the pane, so no row from another repo shows.
// The close state is then compared against the rows and the current step.
async function refresh($) {
  let got: { root: string | null; state: { band: BandState; pane: PaneState } | null } | null
  try {
    got = await readCairn(fsSource($))
  } catch {
    got = null
  }
  const root = got === null ? null : got.root
  if (got !== null && got.state !== null) {
    const next = got.state
    await update($, band, () => ({ ...next.band, root }))
    await update($, pane, () => next.pane)
  } else {
    // The keep-or-empty decision and the write stand at one version, so a
    // good read that lands in between is decided again, not overwritten
    // (M210 review). Keeping writes nothing.
    for (let tries = 0; tries < 3; tries += 1) {
      const held = await $.state.get(BAND_REF)
      const kept = held.value !== undefined && held.value.shape === BAND_SHAPE ? held.value.value.root : null
      if (kept !== null && root !== null && kept === root) break
      const empty = { rows: [], workable: [], root }
      const done = await $.state.set(BAND_REF, { shape: BAND_SHAPE, value: empty }, { ifVersion: held.version })
      if (done.isSet) {
        await update($, pane, () => NO_PANE)
        break
      }
    }
  }
  await reconcile($)
}

function fsSource($): FileSource {
  return {
    cwd: () => $.session.cwd(),
    isFile: path => isFile($, path),
    read: path => readText($, path),
    list: path => listNames($, path),
  }
}

async function listNames($, path: string): Promise<string[] | null> {
  try {
    return (await $.fs.list(path)).map(entry => entry.name)
  } catch {
    return null
  }
}

async function isFile($, path: string): Promise<boolean> {
  try {
    return (await $.fs.stat(path)).kind === 'file'
  } catch {
    return false
  }
}

async function readText($, path: string): Promise<string | null> {
  try {
    return await $.fs.read(path)
  } catch {
    return null
  }
}
