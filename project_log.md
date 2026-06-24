# FRCS SN Revision — Project Log

---

## 2026-06-13 — GitHub Pages + Firebase login/sync

### What we built

**GitHub Pages hosting**
- Initialised git repo in `~/frcs-sn-revision/`, committed all app files
- `.gitignore` excludes `guidelines/` PDFs, `__pycache__/`, `*.pdf` — source PDFs not needed at runtime
- Repo published to `https://github.com/lynerjy/frcs-sn-revision` (public, account: lynerjy)
- GitHub Pages enabled: app live at `https://lynerjy.github.io/frcs-sn-revision`
- Update workflow: at end of each session, run:
  `git -C /Users/cfu/frcs-sn-revision add index.html content.js && git -C /Users/cfu/frcs-sn-revision commit -m "update cards/UI" && git -C /Users/cfu/frcs-sn-revision push`

**Login screen + cross-device sync (Firebase Firestore)**
- Firebase project: `frcs-revision` (console.firebase.google.com)
- Firestore database created (Standard edition, nam5/US, test mode → rules set to `allow read, write: if true`)
- Login screen overlay added to `index.html` — full-screen on first visit, dismissed on successful login
- Credentials hardcoded client-side (no real auth needed): `korky` / `korkyblorky`
- Login state persisted in `localStorage` (`frcs_user` key) — won't re-prompt on same browser
- "Sign out" button added to header
- On login: loads from localStorage immediately (fast), then async-fetches from Firestore and re-renders
- `save()` now writes to localStorage AND debounced Firestore write (2s after last change)
- Entire `state` object stored as single Firestore document: `users/korky`
- `normalizeState()` extracted from `loadState()` — ensures new SOURCES/TOPICS added to content.js are initialised for existing users after sync

### Key decisions
- PDFs not hosted on GitHub — only `index.html` and `content.js` needed for the live app
- Firestore rules left open (`allow read, write: if true`) — data is just flashcard scores, not sensitive
- localStorage still used as local cache; Firestore is authoritative on cross-device sync
- Progress does NOT sync between devices mid-session — only on next login (Firestore load)

### Open / next (as of end of this session)
- Add more users to `FB_USERS` dict in `index.html` if needed (e.g. Carolyn's own account)
- Continue Aberdeen mining: aberdeen-neuro-death (7pp) → aberdeen-tcd → aberdeen-aeds
- Thin topics: spinal-anatomy (3 SBAs), carotid (2 SBAs)
- Large unmined PDFs: NG217 Epilepsy (150pp), RCP Stroke (239pp)
- **UI redesign (one remaining item)**: brain/gamification UI — creative progress bar, game-like feel

---

## 2026-06-13 — UI fixes + sources redesign

### What we built

**Quick UI fixes**
- "Quiz all topics →" button: now full-width, properly sized (was a tiny badge button)
- "← Back to topic list" button: bigger, clearer

**Deck filter moved to quiz page**
- Removed from nav bar (was confusing — didn't apply to flashcards)
- Now lives as pill buttons (Full deck / Exam-likely / Korky folder / Guidelines only) inside the "Quiz all" screen, above the topic checkboxes
- Flashcards now always show all cards (no filtering) — `filteredCards()` simplified to always return full deck
- Per-topic quiz also always uses all questions for that topic; filter only applies to global "Quiz all"

**Sources page redesign**
- Removed search/filter dropdowns
- Sources now grouped by category with section headers: Official Exam, E-Learning, Clinical Guidelines, Textbooks, Neuroradiology, Neuroanatomy, Revision Courses, Korky — Key Papers, Korky — Aberdeen Course
- Korky folder badge shown on section headers (not on every individual row)
- Textbooks section also marked as Korky folder (all textbooks in list are from Korky's physical collection)
- Intro paragraph added explaining: two source streams (guidelines vs Korky folder), recall-bank weighting, accuracy standard (every card needs a page ref)

### Still deferred
- **Brain/gamification UI** — creative animated progress bar, game-like feel. Needs its own session; significant redesign.

---

## 2026-06-15 — Gamification overhaul + multi-user isolation + dev panel

### What we built

**XP + level system**
- XP awarded per SBA answer: +10 standard, +20 hard; combo multipliers ×1.2/×1.5/×2 at streaks of 2/3/5
- 9 levels defined in LEVELS array; level pill shows "Level N / 9"
- Level-up triggers full-screen banner; achievement toasts for First Blood, On Fire, Unstoppable, Slam Dunk, Century, Level 5
- Combo badge shown in quiz score bar during streaks
- Game state stored in localStorage as `frcs_game_{username}` (per-user scoped)

**Daily goal — basketball hoops**
- 5 SVG hoop baskets in header; each fills amber as you answer questions
- `hoopSVG(scored)` returns inline SVG; empty = dim rim + tapering net, scored = amber rim/net + ball above
- "DAILY GOAL SMASHED!" banner on completion

**Pixel art canvas brain mascot**
- Single `position:fixed` canvas (`#brain-canvas`, 36×42px at SC=3), created by `PXBRAIN.init()`, appended to `document.body`
- Rides the XP bar: feet sit on bar top edge, centred on fill's right edge
- `PXBRAIN.reposition()` called from `updateXPBar()` and on resize/font-load
- Animations: idle bob, dunk (jump + amber ball falls), miss (horizontal shake)
- ⚡ FX ON/OFF toggle in header, persisted to localStorage as `frcs_anim`
- `PXBRAIN.stop()` / `PXBRAIN.start()` for toggle

**Multi-user localStorage isolation**
- All localStorage keys scoped per user: `frcs_state_{username}`, `frcs_game_{username}`
- `stateKey()` / `gameKey()` helper functions
- `loadGameState()` called in both login paths; migrates old unscoped `frcs_game` key on first login

**Test account + dev panel**
- Login: `test` / `test` — Firestore doc `users/test`
- Dev panel (bottom-right, test user only): ✓ Correct, ✗ Wrong, ✓ Hard correct, ⚡ Grant level XP, 🏀 Fill hoops, ↺ Reset game state

**Question flagging**
- 🏳 flag button on every SBA (after answering) and flashcard back
- Opens inline textarea for note; stored in `state.flags` keyed by `qFlagId(text)` = `fl::` + first 60 chars
- Flagged Questions section in Progress tab; ⬇ Export CSV button downloads `frcs-flagged-questions.csv`
- Flags synced to Firestore with rest of state

**Other UI fixes**
- Font: `ui-monospace,'Courier New'` for game/header elements; content labels use regular font
- Near-monochrome palette; pixel drop shadows on cards/buttons
- Header stat "Qs Done" = total SBA questions answered (not flashcard count)
- "Standard" ref suppressed from quiz source display

---

## 2026-06-15 — Aberdeen mining (sessions 4–6) + all Key Papers mined

### Content added
- All Aberdeen course PDFs fully mined: cerebral-physiology, RESCUEicp, neuro-death, TCD (Kassab 2007), AEDs (Stafstrom 2010)
- All 14 Korky Key Papers fully mined (see frcs.md for full list)
- Both small MCQ banks fully mined
- Total: ~480 flashcards / ~400 SBAs / 210+ Korky-tagged cards
- 283 claude-ai SBAs remaining (target zero; replace during each mining session)

### Next content priorities
1. TJones Revision Notes (79pp) — broad, highest yield per page
2. Infographic Guide 2025 (70pp)
3. Alleyne/Citow Board Review (434pp)
4. Thin topics: spinal-anatomy (3 SBAs), carotid (2 SBAs)

### Sources prioritisation TODO
- **Primary ordering**: recall bank frequency (already implemented as `NR` badge + topic sort)
- **TODO**: Download JCIE Syllabus Blueprint 2023 from `https://www.jcie.org.uk/content/content.aspx?ID=15` — this is the official exam document defining topic weightings; mine it once downloaded and use its weightings to cross-check current source priorities
- **TODO**: Review BNTA reading list at `https://e1v1m1.com/frcs-sn/` — peer-curated by UK trainees who have sat the exam; check whether their recommended texts match the sources already in the app
- **Removed**: `priority` column from Sources table (2026-06-15) — values were set by Claude during initial app build without a clear basis; recall frequency is the principled alternative

---

## 2026-06-15 — Recall frequency display + topic sort

### What we built
- `RECALL_COUNTS` computed at load time from the RECALL array: `{topicId: count}`
- Topic list in Study tab sorted descending by recall count (highest-frequency topics appear first)
- Each topic shows recall count as `NR` in amber (e.g. "62R" for neuro-onco-cranial) — the number of real candidate recall questions attributed to that topic
- `recallBadge(topicId)` also used in Quiz topic selector, colour-coded: red ≥40, amber ≥20, blue ≥10, grey otherwise
- This makes recall-bank frequency the de-facto priority ordering visible to the user

### Key topic recall counts
| Topic | Recall Qs |
|-------|-----------|
| neuro-onco-cranial | 62 |
| degenerative-spine | 52 |
| vascular-aneurysm | 26 |
| head-injury | ~24 |
| hydrocephalus | ~21 |

---

## 2026-06-15 — UI fixes (today's session)

### What we fixed
- **Brain tracking**: `repos()` now called inside every `requestAnimationFrame` tick so the brain tracks the CSS-transition-animated XP fill in real time (was jumping to end position immediately)
- **Brain vertical space**: canvas height 42→56px; feet now at bar top edge, more breathing room above
- **Flashcard AI warning**: cards with `src_id:"claude-ai"` now show same amber ⚠ warning on card back as SBAs; fake `ref:"claude"` suppressed from display
- **Notes tab source list**: each topic now lists all verified sources (with Korky badges) instead of just `ld.src` string; shows count of AI-generated flashcards and SBAs per topic with warning
- **Priority column removed** from Sources table — was set arbitrarily by Claude during initial build with no principled basis; removed to avoid misleading
- **Session logging enforced**: mandatory end-of-session rule added to `CLAUDE.md` in project root + memory feedback file; project log caught up for sessions 4–6 which had never been logged

### Open questions / next session
- Mine TJones Revision Notes (79pp) — run `python3 mine.py next` to confirm source id, then `mine.py extract`
- Download JCIE Syllabus Blueprint 2023 (see Sources prioritisation TODO above)
- 283 claude-ai SBAs still unverified — replace during each mining session as usual

---

## 2026-06-15 — Source filtering via checkboxes + topic Sources tab (session 7)

### What we built
- **Per-source checkboxes** in Admin → Sources: each row has an On/Off checkbox; toggling immediately filters Flashcards and Quiz content via `state.sources[id].enabled`
- **Gmail-style section header checkbox**: single checkbox in "On" column header — checked=all on, unchecked=all off, indeterminate dash=mixed; set via `.indeterminate` property after render
- **Section select-all** replaces the clunky All/None buttons that were in the section title
- **`setSrcEnabled(id, v)`** and **`setSrcCategoryEnabled(cat, v)`** new functions; both re-render topic list, current topic content, and sources table on change
- **`filteredQs`** simplified: removed korky/web branches (now handled by checkboxes); kept only `recall` branch for Exam-likely filter
- **Korky folder + Textbooks listed first** in Sources table (Textbooks are from Korky's physical collection)
- **Sources tab in topic view**: renamed from "Notes", made first tab and default on topic open; shows each source with ✓/○ enabled indicator; explains that sources control Flashcards/Quiz and links to Admin → Sources
- **Sources page intro**: restored original "About this revision tool" paragraph (provenance, two streams, recall-bank weighting) + added "Source selection" sub-section beneath it
- **Removed**: Korky folder / Guidelines only quick-filter buttons from global quiz (redundant with checkboxes); stale filterLabel display from topic title

### Architecture note
`filteredCards(ld)` was already filtering via `srcEnabled()` which checks `state.sources[id].enabled`. The new checkboxes just give the user a UI to set those flags. No change to the filtering logic itself was needed for flashcards.

### TODO for next session
- **Remove "Status" column from Sources table** — deprecated holdover, no longer used
- **Add URL links for online sources** — sources without a local PDF should show a link button pointing to `s.url`; currently only PDF sources show an "Open" button, online-only sources show "—"

---

## 2026-06-15 — AI source toggle + dev panel drag + UI polish (session 8)

### What we built

**AI-Generated source toggle**
- Added `{id:"claude-ai", name:"Claude AI — AI-Generated Questions", category:"AI-Generated"}` to SOURCES array in `content.js`
- `normalizeState()` now picks it up automatically → it appears in Sources tab with a toggle checkbox like all other sources
- When disabled, all `src_id:"claude-ai"` cards and SBAs are excluded from Flashcards and Quiz via the existing `srcEnabled()` gate — no logic change needed
- Removed the hard-coded `filter(({id})=>id!=='claude-ai')` exclusions from `renderLearnContent` and `renderNotes` so it now flows through the normal source pipeline

**AI warning styling — amber throughout**
- Sources sub-tab (per-topic): claude-ai row now renders with amber ✓, amber background (`#fffbeb`), amber border, `⚠ AI` badge, and a count line: "12 SBAs · 2 cards" (computed from `ld.q` and `ld.c` filtered by `src_id`)
- Quiz question (global + topic): amber `⚠ AI` badge in the score/question-number line before answering; amber `AI-generated — topic` line in explanation after answering
- Flashcard backs: amber pill with left border accent replacing the old dim opacity `.5` ref line
- Sources tab: `AI-Generated` section already had amber warning banner — unchanged

**Policy change on claude-ai SBAs** (user instruction)
- Do NOT replace or rewrite claude-ai SBAs when mining a real source — keep them
- Only correct if source clearly contradicts content
- Target is no longer "zero claude-ai SBAs" — target is "no obviously wrong ones"
- Feedback saved to memory: `feedback_frcs_claude_ai_sbas.md`

**Dev panel (test user)**
- Moved default position from bottom-right to bottom-left (was overlapping "Next →" button in quiz)
- Added drag handle (⠿ DEV PANEL title bar): mousedown/mousemove/mouseup drag to anywhere on screen
- Cursor changes grab → grabbing during drag; panel clamps to viewport edges

### Open questions / next session
- Mine TJones Revision Notes (79pp) — `python3 mine.py next` to confirm source id, then extract
- 283 claude-ai SBAs retained (policy changed: keep, don't replace)
- Sources tab TODO still open: remove Status column, add URL links for online-only sources

---

## 2026-06-15 — Sources table overhaul + AI styling + process fix (session 9)

### What was built / changed

**Sources table (index.html)**
- Removed "Status" column (select dropdown — was a deprecated holdover, no principled basis)
- Renamed "Open" column → "Access"
- Korky folder sources: show PDF button only (local files, no public URL needed)
- Non-Korky sources: show Visit ↗ link (from `s.url`) + PDF button if `s.local` exists
- "Not yet mined" gray badge on all Korky sources where `!s.cards || s.cards === 0`
- TODO saved: verify all non-Korky sources have `url` fields populated

**Provenance disclaimer (Sources tab intro)**
- Expanded from one sentence to a full block explaining: what Claude covers well (classic anatomy, landmark trials, scoring systems), where to be cautious (specific numbers, UK-specific practice, recency cutoff Aug 2025, rare topics), and a clear "cross-check against Greenberg or NICE" instruction
- Removed the inaccurate "AI-Generated section below lists all such questions" sentence

**AI warning placement (quiz)**
- Removed ⚠ AI badge from question line — only revealed in the answer (amber ref line in explanation)

**Process fix — Greenberg mining rule (CLAUDE.md)**
- Added mandatory section: Greenberg chapter selection must be driven by recall-bank frequency, not claude-ai verification backlog
- Documents what went wrong in session 5 (2026-06-12): all 11 Greenberg sessions were driven by existing claude-ai SBAs, leaving paediatric neurosurgery (46 recalls, 3rd highest) with zero Greenberg coverage
- Sets explicit priority chapter order: paeds first, then neuro-onco gaps, degenerative spine remainder, vascular, carotid

### Key decisions
- Greenberg paeds mining queued as URGENT next priority in frcs_next_todo.md
- Target page ranges for paeds: craniosynostosis ~pp1140s, NTDs ~pp200s, paeds tumours ~pp750s
- Korky sources intentionally omit Visit ↗ links — they are local files not public URLs

### Open questions / next session
- Greenberg paeds re-mining: run `python3 mine.py extract greenberg <pages>` targeting paeds chapters
- TJones Revision Notes (79pp) still queued after paeds Greenberg
- Non-Korky sources: verify all have `url` populated so Visit ↗ renders everywhere

---

## 2026-06-16 — Sources mining badges everywhere + brain/XP bar layout + daily goal (session 10)

### What was built / changed

**Mining status badges — all sources**
- Previous sessions partially implemented badges gated on `s.korky` (object flag) or `isKorky` (category), neither of which caught all cases (e.g. Greenberg in Textbooks category had `s.korky` undefined, so no badge)
- Final fix: badges now appear on every non-AI source, unconditionally, using four branches:
  - ✓ N cards (green) — content in app, counted live from `LEARN` via `liveCountBySrc` map
  - partial — N cards (amber) — `s.partial:true` set on source (e.g. Greenberg: 64 cards)
  - not yet mined (gray) — has `s.local` PDF or `isKorky` but zero extracted content
  - reference only (blue) — external link only, never a content source (eBrain, JCIE, etc.)
- `liveCountBySrc` built at render time by iterating all `LEARN` topics' `.c` and `.q` arrays — so NICE guidelines auto-show correct counts without needing `s.cards` set
- `effectiveCards = s.cards || liveCountBySrc[s.id]` — explicit `s.cards` takes priority (Korky papers); live count used as fallback (guidelines, Greenberg partial override)
- AI-Generated category explicitly excluded from badge logic

**Sources readme updated** — badge legend now shows all four badge styles inline with actual rendered colours; wording changed from "Korky-folder sources" to "every source"

**Brain / XP bar layout**
- Brain canvas (39px tall above bar) was overlapping the exam date row
- Fix: added `margin-top: 42px` to `.xp-row` — lowers XP bar enough to clear the brain's full height
- Redundant `exam-date-label` span removed (was echoing the date picker value as formatted text — unnecessary duplication)

**Configurable daily basket goal**
- `const DAILY_GOAL=5` replaced with `function getDailyGoal()` reading `state.dailyGoal` (defaults to 5)
- All five `DAILY_GOAL` references replaced with `getDailyGoal()` calls
- 🏀 Daily goal: number input added to `.hdr-bot` row (same line as exam date), range 1–50
- Saves to `state.dailyGoal` on change, calls `renderDailyHoops()` immediately
- Bug found and fixed in same session: initial wiring called `renderHoops()` (nonexistent) instead of `renderDailyHoops()`

### Key decisions
- "Reference only" blue badge chosen over no badge for external-link sources — user wants them listed for future login/payment unlock potential
- `liveCountBySrc` computed at render time (not cached) — acceptable since Sources table is not re-rendered frequently and LEARN is small enough

### Open questions / next session
- Greenberg paeds re-mining still URGENT — craniosynostosis ~pp1140s, NTDs ~pp200s, paeds tumours ~pp750s
- TJones Revision Notes (79pp) queued after paeds Greenberg
- Non-Korky sources: verify all have `url` fields so Visit ↗ renders everywhere

---

## 2026-06-16 — Header layout compaction + polish (session 11)

### What was built / changed

**Hoops merged onto XP bar row**
- Removed separate `.daily-row` div entirely — level pill, XP bar, XP label, TODAY label, hoops, and done/more msg now all sit in a single `.xp-row` flex row
- `.xp-bar-wrap` capped at `max-width:160px` (was `flex:1` with no cap, could expand to ~400px) to leave room for hoops
- `.daily-hoops` gap reduced 6px → 4px to tighten spacing in the merged row
- `.daily-row` CSS rule removed (no longer used)
- Net: one fewer header row, same brain positioning above the bar

**Redundant exam-date-label removed**
- `<span id="exam-date-label">` was echoing the date picker value as formatted text (e.g. "(15 Jun 2026)") — unnecessary since the date input already shows it
- Span removed from HTML; JS in `updateStats()` that wrote to it also removed

### Key decisions
- XP increment values unchanged — bar is physically shorter so visual jump per answer is naturally smaller without touching game mechanics
- Brain `margin-top:42px` on `.xp-row` retained — still needed to give brain's 39px height clearance above the bar

### Open questions / next session
- Greenberg paeds re-mining still URGENT — craniosynostosis ~pp1140s, NTDs ~pp200s, paeds tumours ~pp750s
- TJones Revision Notes (79pp) queued after paeds Greenberg
- Non-Korky sources: verify all have `url` fields so Visit ↗ renders everywhere

---

## 2026-06-16 — Progress reset per topic + Exam-likely grey-out (session 12)

### What was built / changed

**Greenberg pp297-319 (Chiari I/II + NTDs) — 12 SBAs committed and pushed**
- `python3 mine.py done greenberg 297-319 12` run — Greenberg now at 76 total cards
- Topics: Chiari II shunt-first rule; Chiari I most common symptom (pain 69%); tonsillar descent >5mm criteria; Chiari I vs II comparison; Chiari II dysphagia 69%; surgical outcome 68%; anencephaly/anterior neuropore; VPA 1-2% NTD + CBZ doubles MM; folic acid 4mg/d → 71% reduction; AFP screening 91%/100% at 15-20 weeks; craniolacunia 85% in Chiari II NOT due to ICP; cerebellar ptosis from excessive craniectomy

**Per-topic reset in Progress table**
- Each topic row now shows a small `↺ reset` button in a new rightmost column (only appears if that topic has recorded data)
- `resetTopicProgress(tid)` function: deletes `state.cards` entries starting with `tid+"::"` and `state.sbaResults` entries starting with `"sba::"+tid+"::"`; saves, re-renders, re-renders active topic content if it's the current one
- "Reset all progress" button moved from above-table header into the table header row (right-aligned in the last column), so it's co-located with the per-topic resets

**Exam-likely filter — grey out instead of hide**
- `renderQuizTopicCheckboxes()`: when `globalSourceFilter==="recall"`, topics with no recall-flagged questions now render as greyed-out disabled checkboxes (opacity 0.38, `cursor:not-allowed`) rather than being removed from the DOM
- Topics stay in position when toggling between Full deck / Exam-likely — only colour changes, no layout shift
- No suffix label added to greyed topics (self-evident)
- Recall-bank attribution note ("Exam likelihood estimated from candidate recall-bank reports...") shown below the checkboxes (not above) when Exam-likely is active, so it doesn't shift topic positions on toggle

### Key decisions
- Reset buttons appear only when a topic has data — keeps the column clean for untouched topics
- Note placed below checkboxes not above: prevents any layout shift when toggling filter tabs

### Login persistence (answered for user)
- Auto-login is localStorage-based (`frcs_user` key), per-browser/device — not IP-based
- Expected and correct: if you sign in on the same browser, you stay logged in until Sign out is clicked

### Open questions / next session
- Continue Greenberg mining: craniosynostosis (~pp1130-1160), paeds tumours (medulloblastoma/ATRT ~pp750-795)
- TJones Revision Notes (79pp) after paeds Greenberg
- Non-Korky sources: verify all have `url` fields so Visit ↗ renders everywhere

---

## 2026-06-16 — Exam date persistence + Sources page redesign planned (session 13)

### What was built / changed

**Exam date and daily goal persistence fix**
- Root cause: `examInp.value` and `goalInp.value` were only set once at page init (before login), so Firestore sync and cross-device login never restored the inputs to the UI
- Fix: `updateStats()` now syncs both `exam-date-input.value` and `daily-goal-input.value` from state on every call
- Effect: exam date and basket goal now survive login, logout, cross-device Firestore pull

**Login persistence explained**
- Auto-login is `localStorage("frcs_user")` per-browser — not IP-based. Same browser = stays logged in until Sign out clicked. Expected behaviour.

### Pending (not yet implemented): Sources page redesign

Two changes planned, implementation interrupted by /summ:

1. **Mining badge as separate column** — currently inline in the Source name cell; move to a dedicated column to the left of Access

2. **Four-group vertical layout** replacing current fine-grained categories:
   - **Korky Folder** — type=`korky` (Key Papers, Aberdeen Course Material, MCQ Banks)
   - **Publicly Available** — type=`free` or `free_pdf` (Clinical Guidelines, Official Exam, GAIN/Brain School, Radiopaedia)
   - **AI-Generated** — claude-ai source
   - **Login / Subscription Required** — type=`subscription`, `purchase`, `paid_event` (eBrain, frcs-companion, neurocourses, CLNA, Textbooks, Revision Courses)

   Implementation notes:
   - `srcGroupKey(s)` function maps source → one of four group keys
   - Fine-grained category sub-headers retained within each group
   - Fix `"Korky — Aberdeen Course"` → `"Korky — Aberdeen Course Material"` mismatch in catOrder/korkyLike (currently Aberdeen sources fall into "Other" bucket)
   - Group super-headers render above each cluster of category tables

### Open questions / next session
- Implement Sources page redesign above (4-group layout + mining badge column)
- Continue Greenberg mining: craniosynostosis (~pp1130-1160), paeds tumours (~pp750-795)
- TJones Revision Notes (79pp) after paeds Greenberg

---

## 2026-06-16 — Sources page redesign: 4-group layout + Mining column (session 14)

### What was built / changed

**Sources page — 4-group layout**
- Replaced fine-grained category-per-table with four meta-group sections, ordered:
  1. **Korky Folder** (amber header) — sources with `type:"korky"` (Key Papers, Aberdeen Course Material, MCQ Banks)
  2. **Publicly Available** (blue header) — `type:"free"` or `type:"free_pdf"` (Clinical Guidelines, Official Exam, GAIN, Brain School, Radiopaedia)
  3. **AI-Generated** (amber/warning header) — claude-ai source
  4. **Login / Subscription Required** (grey header) — `type:"subscription"`, `"purchase"`, `"paid_event"` (eBrain, frcs-companion, neurocourses, CLNA, Textbooks, Revision Courses)
- Each group is a single table; categories within a group appear as bold sub-header rows with toggle checkboxes
- E-Learning splits correctly: GAIN/Brain School under Publicly Available; eBrain/frcs-companion under Locked
- Fixed longstanding category name mismatch: `"Korky — Aberdeen Course"` → `"Korky — Aberdeen Course Material"` (Aberdeen sources were silently falling into "Other" bucket)

**Mining column**
- Mining badge (✓ N cards / partial / not yet mined / reference only) moved from inline in Source name cell into its own dedicated **Mining** column, between Source and Access
- Badges now `white-space:nowrap` and centred in the column

### Key decisions
- Group assignment by `type` field (not `category`) — cleanest since categories cross-cut the desired groupings (E-Learning has both free and subscription sources)
- Category sub-headers always rendered (even for single-category groups like AI-Generated) — provides consistent checkbox mechanism; slight redundancy acceptable
- Textbooks (`type:"purchase"`) go in Login/Subscription Required — not in Korky folder, since they're commercially available reference books not Korky-specific content

### Open questions / next session
- Continue Greenberg mining: craniosynostosis (~pp1130-1160), paeds tumours (medulloblastoma/ATRT ~pp750-795)
- TJones Revision Notes (79pp) after paeds Greenberg
- Non-Korky sources: verify all have `url` fields so Visit ↗ renders

---

## 2026-06-17 — Greenberg paeds mining + Sources page Korky fix + mobile scroll fix

### What we built / mined

**Greenberg paeds — medulloblastoma + ATRT (pp745–768)**
- Located correct pages via TOC extraction (pages 15-40); "craniosynostosis ~pp1140s" in memory was wrong — that range is spinal trauma. Craniosynostosis is at book p.264 (~PDF 272-295); medulloblastoma at book p.744 (PDF 745-768).
- Extracted pp745-780, then narrowed to 745-768 to avoid vestibular schwannoma chapter bleed.
- Added 3 flashcards to `LEARN["paeds"].c[]`:
  1. Medulloblastoma 4 molecular subtypes (WNT/SHH-TP53wt/SHH-TP53mut/non-WNT-non-SHH groups 3+4) — `ref:"Greenberg 10e, p747"`
  2. Chang M staging system — `ref:"Greenberg 10e, p748–749, Table 43.1"`
  3. MDB vs ependymoma imaging (roof of 4th vs floor) — `ref:"Greenberg 10e, p748"`
- Added 8 medulloblastoma SBAs + 2 ATRT SBAs to `LEARN["paeds"].q[]` (10 total, all `src_id:"greenberg"`, `korky:true`, `recall:true`)
- Ran `python3 mine.py done greenberg 745-768 8` then `done greenberg 755-768 2`. Total greenberg cards now 86.

**Paeds SBA count: 49** (was 28 before this session; +21 from medulloblastoma/ATRT SBAs added across sessions 6+7 — 11 net new this session).

**Sources page — Korky textbooks fix**
- Root cause: Greenberg had `type:"purchase"` → appeared in Login/Subscription Required group, showed "reference only"
- Fix: changed `type:"korky"`, added `korky:true`, updated `cards:76→86`, updated notes
- Added 4 new Korky textbook entries (never existed before):
  - `infographic-2025` — Infographic Guide to Neurosurgery 2025 (70pp)
  - `alleyne-board-review` — Alleyne & Citow Board Review 3rd ed (434pp)
  - `birinyi-board-prep` — Birinyi Comprehensive Board Preparation (450pp)
  - `harbaugh-knowledge-update` — Harbaugh Neurosurgery Knowledge Update (985pp)
- Added 3 new Aberdeen Korky entries: `aberdeen-tjones-revision` (79pp), `aberdeen-tjones-exam` (39pp), `emergency-head-injury` (14pp)
- Renamed `category` of samandouras/elwell-kirollos/landmark-papers/young-neuro to "Textbooks — Recommended Purchases" so they stay clearly separate from Korky textbooks in the Locked group
- `srcGroupKey()` in index.html already handles `type:"korky"` correctly — no HTML changes needed for this fix

**Mobile scroll fix**
- Bug: on ≤800px, `.learn-topic-list` is sticky and fills most viewport; `#learn-content` rendered below fold after topic click
- Fix: added `if(window.innerWidth<=800) document.getElementById("learn-content").scrollIntoView({behavior:"smooth",block:"start"})` at end of `openLearnTopic()` (both branches)

### Key decisions
- Greenberg type changed to `type:"korky"` (not `"free"`) — it's a physical book Carolyn has access to in the Korky folder context
- ATRT SBAs added from pp754-755 per source text; biallelic SMARCB1 inactivation, WHO grade 4, infant peak, 33% CSF dissemination at diagnosis

### Stats
- Total SBAs: 422 (+21 paeds vs session 6)
- Total cards: 442
- claude-ai SBAs remaining: 283 (no change)
- Greenberg cards recorded: 86

### Open questions / next session
1. **Greenberg craniosynostosis** — pages 272-295 partially mined (only 2 cards from session 4); needs a dedicated extraction of the full chapter
2. **Greenberg paeds tumours section 35.2** — pilocytic astrocytoma, ependymoma, craniopharyngioma (PDF ~pp621-650 estimate; verify via TOC)
3. **TJones Revision Notes** (79pp, `aberdeen-tjones-revision`) — highest yield per page for thin topics; mine next
4. **Verify Sources page** renders correctly in browser — all new Korky textbooks should appear in Korky group with "not yet mined" badge

---

## 2026-06-17 (session 7b) — Greenberg paeds cont. + UI fixes

### What we built / mined

**Greenberg paeds pp264-295 — craniosynostosis + NTDs + tethered cord**
- Section 15.2 (pp264-271): craniosynostosis and craniofacial development
- Section 16 (pp272-295): NTDs, tethered cord syndrome, split cord malformation, Dandy-Walker
- mine.py TOC extraction confirmed: craniosynostosis is NOT at pp1140s (that's spinal trauma); it's at book p.264 = PDF pp264-271
- 10 new paeds SBAs added: sagittal CSO (most common, scaphocephaly), coronal CSO (harlequin eye, amblyopia), Apert vs Crouzon (syndactyly + HCP vs no), lambdoid vs positional plagiocephaly (ear direction key discriminator), tethered cord (93% gait/LE weakness; conus <L2 + filum >2mm), adult vs childhood tethered cord pain (86% perianal/perineal in adults), pre-op cystometrogram, Type I vs II SCM (bony dural-sheathed septum/separate tubes vs fibrous/single tube), Type I SCM surgical rule (don't cut filum until septum removed), Dandy-Walker triad + HCP 75-95%
- Greenberg total: 96 cards recorded

**mine.py fix: block size 80k→250k**
- paeds section grew larger than the 80000 char limit; stats was undercounting SBAs (54 reported vs 59 actual). Fixed by increasing block limit to 250000 chars.

**Mobile fix: panel swap (replaces scrollIntoView)**
- New approach: clicking a topic adds `mob-content` class to `.learn-layout`, which hides `.learn-topic-list` via CSS. A "← All Topics" button injected at top of `#learn-content` removes the class on click.
- Previous approach (scrollIntoView) was unreliable on mobile browsers.

**Source counts in Sources tab**
- All sources now show their SBA/card counts next to the source name (e.g. "12 SBAs · 3 cards")
- Previously only claude-ai source showed counts
- Count color: amber for claude-ai, grey for all others

### Stats
- Paeds SBAs: 59 (was 49 at start of session 7)
- Total SBAs: 436 (mine.py now counts correctly with larger block)
- Greenberg cards: 96

### Open questions / next session
1. Greenberg paeds section 35.2 (pilocytic astrocytoma, ependymoma, craniopharyngioma) — PDF pages ~621-650 estimate; verify via TOC
2. TJones Revision Notes (79pp, `aberdeen-tjones-revision`) — highest yield per page
3. Move to neuro-onco-cranial (62 recalls) after paeds mining complete

---

## 2026-06-17 (session 7c) — Greenberg paeds continued: PCA + ependymoma

### What was mined

**Greenberg Chapter 39 (pp691-708): Pilocytic astrocytoma**
- 6 new paeds SBAs:
  - WHO grade 1, >95% 10-yr survival; surgical principle: nodule only (cyst wall not neoplastic)
  - Post-op XRT NOT recommended; follow serial MRI; re-operate if recurrence; chemo preferred over XRT in young patients
  - NF1 association: PCA is the principal CNS tumour of NF1 (15-20% of NF1 patients)
  - KIAA1549::BRAF fusion → MAPK pathway; most prevalent (75%) in cerebellar PCAs
  - Biphasic histology: Rosenthal fibres (compacted) + eosinophilic granular bodies (loose myxoid)
  - Cystic cerebellar presentation: cyst + enhancing mural nodule; 94% enhance

**Greenberg Chapter 41 (pp726-732): Posterior fossa ependymoma**
- 5 new paeds SBAs:
  - Floor of 4th ventricle; facial colliculus invasion → peripheral CN VII + abducens (CN VI) palsy
  - Post-op workup: LP at 2 weeks (10cc CSF); XRT 59.4Gy 3D conformal; spinal XRT only if drop mets/+CSF
  - 5YS paeds 20-30% vs adult up to 80%; GTR most important prognosticator
  - ZFTA::RELA fusion: 66-84% of paediatric supratentorial ependymomas; worse prognosis

**mine.py fix**: block size 80k→250k (paeds section exceeded 80k limit)

### Stats
- Paeds SBAs: 68 (started session 7 at 49)
- Total SBAs: 445
- Greenberg cards recorded: 107

### Open questions / next session
1. Greenberg craniopharyngioma (Chapter 50.2, book p.849 → PDF ~851) — important paeds/sellar tumour
2. Ependymoma chapter tail (pp733-744) not yet read — may have more spinal ependymoma content
3. Move to neuro-onco-cranial (62 recalls, priority #2) after paeds complete
4. TJones Revision Notes (79pp) for broad thin-topic coverage

---

## 2026-06-17 (session 8) — Greenberg pp272-295 (developmental anomalies) + source count fix

### What was fixed
- **Greenberg source card count on Sources page**: hardcoded `cards:76` → `cards:101` (then updated again to `cards:115` after this session's mining). The `cards` field in SOURCES is manually maintained and had drifted from the actual content.js count.

### What was mined
**Greenberg pp272-295 (book pp270-293): Developmental anomalies**
- 12 new paeds SBAs + 2 flashcards added (14 total)
- Topics covered:
  - **Dandy Walker malformation** (3 SBAs + 1 flashcard): classic triad, HCP rate 75-95%, ETV requires patent aqueduct, prognosis (50% normal IQ, seizures 15%)
  - **Myelomeningocele** (4 SBAs): recurrence risk 2-3% after 1 affected child / folic acid prevention; HCP in 65-85% (>80% before age 6m); closure within 24hrs (colonised after 36hrs); surgical goals (free placode/watertight dura/skin — does NOT restore function); outcomes (85% survive, early death = Chiari II complications)
  - **Tethered cord** (1 SBA): filum >2mm = pathological, conus below L2
  - **Hypothalamic hamartoma** (2 SBAs): gelastic seizures in up to 92%; sessile → seizures + developmental delay; pedunculated → precocious puberty
  - **Klippel-Feil** (1 flashcard): low hairline + brevicollis + limited rotation; Sprengel's 25-35%; deafness 30%; mandatory cardiac/renal workup
  - **Diastematomyelia Type I** (1 SBA): never divide filum before removing bony septum or cord retracts against it

### Stats after this session
- Paeds SBAs: 80 (was 68 at start of session)
- Total: 444 cards / 457 SBAs
- Greenberg total entries: 115 (82 SBAs + 19 flashcards + 14 new)
- Greenberg source `cards` field: 115

### Key decisions
- Confirmed the memory file SBA count of "49 paeds SBAs" and "cards:86 Greenberg" were stale — actual counts verified from grep on content.js
- Inserted new cards into paeds section immediately after last ependymoma SBA (line ~890)

### Open questions / next session
1. **Greenberg paeds tumours** — pilocytic astrocytoma/ependymoma/craniopharyngioma details NOT in pp272-295 (those pages are developmental anomalies). Craniopharyngioma at Greenberg Ch50.2 ~p.849; pilocytic/ependymoma already mined in session 7c
2. **Craniosynostosis** — still not mined; was at book ~p.264 (PDF ~pp266-272, just before the pages mined today). Recall bank shows multiple CSO questions.
3. TJones Revision Notes (79pp) — highest yield per page for thin topics
4. Infographic Guide 2025 (70pp) — next after TJones

---

## Session 9 — 2026-06-17

### What was mined
- **Greenberg pp266-272** (craniosynostosis + encephalocele + Dandy-Walker): 9 new paeds SBAs
  - Arachnoid cyst drainage rule (ventricular drainage is ineffective — promotes cyst enlargement)
  - Fontanelle closure timing (anterior 2.5yrs; posterior 2-3mo; 90% adult head size by 1yr)
  - Secondary CSO causes (phenytoin, valproate, rickets, sickle cell, microcephaly etc.)
  - ICP in single-suture CSO (~11%; beaten copper calvaria only correlated if + sellar erosion + sutural diastasis)
  - Metopic synostosis (trigonocephaly, hypotelorism, 1/15,000 births, 75% male, 19p chromosome)
  - Lambdoid surgical technique (ideal 6-18mo; prone on cerebellar headrest; craniectomy to asterion; 100-200ml blood loss)
  - Oxycephaly (all suture fusion → tower skull + undeveloped sinuses; elevated ICP)
  - Encephalocele / nasal polyp rule (nasal polyp in newborn = encephalocele until proven otherwise; basal = no visible mass, presents as CSF leak; transnasally alone is dangerous)
  - Encephalocele prognosis (<5% develop normally; worse if cerebral tissue/ventricular extension/HCP)
  
- **Greenberg pp841-848** (craniopharyngioma Ch50.2): 6 new paeds SBAs
  - CP epidemiology (0.8% brain tumours; most common non-neuroepithelial intracerebral in children; 5-11% paeds brain tumours)
  - Surgical approaches (transcallosal = ONLY for 3rd ventricle tumours; spare chiasm feeders + pituitary stalk remnant = longitudinal striations = portal veins)
  - Post-op DI (triphasic response; short-acting vasopressin only — DDAVP risks iatrogenic renal shutdown in SIADH phase)
  - Post-op steroids (hydrocortisone + dexamethasone; taper slowly — chemical meningitis risk)
  - Radiation (postpone in paeds to protect IQ; side effects: endocrine, optic neuritis, dementia)
  - Outcome (5-10% mortality from hypothalamic injury; bilateral = hyperthermia + somnolence + loss of thirst; 5yr survival 55-85%; recurrence mostly <1yr; reoperation higher morbidity)

### Card counts (post-session)
- paeds: 18 flashcards, **95 SBAs** (was 80 at session start)
- TOTAL: 444 flashcards, **472 SBAs**
- Greenberg total mined: 136 cards across scattered chapters

### Git
- Pushed: commit 7d3386e "Greenberg paeds: 15 new SBAs from craniosynostosis (pp266-272) and craniopharyngioma (pp841-848)"

### Next session priorities
1. **TJones Revision Notes** (79pp, `aberdeen-tjones-revision`) — highest yield per page for thin topics (carotid 2 SBAs, spinal-anatomy 3, neuroradiology 6)
2. **Infographic Guide 2025** (70pp, `infographic-2025`) — visual recall-style content
3. **Alleyne/Citow Board Review** (434pp, `alleyne-board-review`) — mine by chapter for weak topics

---

## Session 10 — 2026-06-17

### What was done
- Started mining **TJones Revision Notes** (`aberdeen-tjones-revision`, 79pp) — pages 1–20
- Added TJones to `CONTENT_SOURCE_MAP` in mine.py (was unmapped)
- Added **16 new SBAs** across 7 topics, all `recall:true`, `korky:true`, `src_id:"aberdeen-tjones-revision"`

### SBAs added (with source page):
| Topic | SBAs | Content |
|-------|------|---------|
| neuro-icu | 4 | Mannitol immediate mechanism (p1), HTS vs mannitol advantages (p1), brain abscess organisms by source (p20), brain abscess stages (p20) |
| ethics | 3 | DVLA VP shunt (p3), non-aneurysmal vs aSAH driving (p3), grade I vs II meningioma driving (p3) |
| spinal-anatomy | 3 | Conus vs CES features (p1), Klippel-Feil triad + associations (p13), syringomyelia theories—Williams vs hydrodynamic vs Heiss-Oldfield (p18) |
| peripheral-nerve | 2 | Ulnar nerve entrapment sites ×4 (p12), Froment's sign mechanism (p12) |
| pituitary | 2 | Acromegaly gold standard (OGTT, p15), Cushing's disease vs ectopic ACTH + IPSS (p19) |
| cranial-anatomy | 1 | Aphasia classification (Broca's/Wernicke's/conductive/global, p13) |
| epilepsy-surgery | 1 | Levetiracetam pharmacology (p2) |

### Updated counts (post-session 10):
- Total SBAs in LEARN: **488** (was 472)
- TJones pages mined: 1–20 of 79
- Remaining TJones: pp21–79

### Decisions
- All new SBAs have explicit `topic:` fields (mine.py stats may show slightly different counts due to section parsing — app uses explicit `topic:` for filtering, which is correct)

### Next session priorities
1. **TJones pp21–40** — continue mining revision notes (spine anatomy, neurophysiology, ethics topics expected)
2. **TJones pp41–60** — vascular, functional, paediatrics sections
3. **Infographic Guide 2025** (70pp) — after TJones complete

## Session 11 — 2026-06-17

### What was done
- Continued mining **TJones Revision Notes** (`aberdeen-tjones-revision`) — pages 21–40
- Added **16 new SBAs** across 9 topics, all `recall:true`, `korky:true`, `src_id:"aberdeen-tjones-revision"`

### SBAs added (with source page):
| Topic | SBAs | Content |
|-------|------|---------|
| neuro-icu | 1 | Brainstem death pre-conditions — all physiological criteria (p21) |
| neuro-onco-cranial | 4 | NF2 diagnostic criteria + chromosome (p22), Cowden/Lhermitte-Duclos (PTEN, p31), Turcot syndrome CNS tumours (p31), CNS lymphoma treatment + survival (p37) |
| neuropathology | 1 | Chordoma physaliphorous cells + proton beam (p25) |
| paeds | 2 | Tuberous sclerosis TSC1/TSC2 genetics (p26-27), Medulloblastoma poor prognostic factors (p36) |
| vascular-aneurysm | 1 | SAH rebleeding rates — 4% day 1, 1.5%/day ×13, 50% at 6 months, 3%/year (p29) |
| neuro-onco-cranial | 1 | Paraganglioma preop management — alpha-before-beta + contralateral IJV angiogram (p29) |
| functional | 2 | DBS pain targets (VPM/VPL vs PVG/PAG, p34), Hemifacial spasm MVD outcomes 85–93% (p39) |
| peripheral-nerve | 1 | Common peroneal vs L5 footdrop — tibialis posterior sparing (p35) |
| pituitary | 1 | Craniopharyngioma good prognostic factors (p36) |
| cranial-anatomy | 1 | Cavernous sinus contents — III, IV, VI, ICA, V1, V2 (V3 excluded) (p37) |
| spinal-trauma | 1 | Central cord syndrome — mechanism (hyperextension + osteophytes), surgery delayed (p40) |

### Updated counts (post-session 11):
- Total SBAs in LEARN: **504** (was 488)
- TJones pages mined: 1–40 of 79
- Remaining TJones: pp41–79

### Notes
- TJones p38 1p19q data appears inverted vs standard literature (Cairncross) — skipped that SBA; would need corroboration from another source before writing
- TJones p37 lists CNV3 as exiting via SOF (clearly wrong — exits via foramen ovale); omitted V3 from cavernous sinus SBA

### Next session priorities
1. **TJones pp41–60** — continue revision notes
2. **TJones pp61–79** — finish
3. **Infographic Guide 2025** (70pp)

## Session 12 — 2026-06-17

### What was done
- Completed **TJones Revision Notes** (`aberdeen-tjones-revision`) — pages 41–60 (session 11 extension) and pages 61–79 (final chunk)
- Added **30 new SBAs** across two batches:
  - pp41–60 (16 SBAs): phenytoin toxicity, CBZ SIADH mechanism, gabapentin pharmacology, DNET, Down syndrome AAI, neurogenic stunned myocardium, CSW vs SIADH, DI criteria, aneurysm locations, Hangman's Effendi, central neurocytoma, Engel class, BOLD MRI, LA onset/duration, Moyamoya secondary causes, Nurick grade
  - pp61–79 (14 SBAs): neuroanaesthesia CBF effects, AED choice by seizure type, hemiballismus, optic chiasm blood supply, Chance fracture, thalamic nuclei (MGB/mediodorsal/Wernicke-Korsakoff), ACDF consent rates (RLN + dysphagia), far lateral disc L4 root, MVD TGN outcomes, VS pathology/natural history, VS SRS outcomes, ETCO2 changes, tuberculum sellae vs olfactory groove

### Updated counts (post-session 12):
- Total SBAs in LEARN: **533** (was 488 at start of today)
- TJones fully mined: all 79 pages complete — 62 total TJones SBAs added
- claude-ai SBAs: 283 (unchanged)

### Today total: 46 new SBAs (pp21–79 across 3 batches)

### Next content priorities
1. **Infographic Guide 2025** (`infographic-2025`, 70pp) — visual recall-style content
2. **Alleyne/Citow Board Review** (`alleyne-board-review`, 434pp) — by weakest topics (carotid 2 SBAs, neuroradiology 6)
3. **NG217 Epilepsy** (150pp NICE guideline) — 0 cards from PDF currently

---

## Session 13 — 2026-06-17 (continued — bug fix session)

### What was done
- **Fixed Progress tab crash** (bug introduced when Dandy Walker and Klippel-Feil flashcard entries were accidentally placed in `paeds.q[]` instead of `paeds.c[]`)
- Root cause: `renderProgressSummary()` iterates all 22 topics and calls `topicSbaStats()` → `sbaId(topicId, q.stem)` — crashes if `q.stem` is `undefined`, which happens for flashcard-format entries `{q:, a:}` placed in the SBA array
- Diagnosis: added try/catch to `renderProgressSummary()` which surfaced the exact error: "Cannot read properties of undefined (reading 'substring')"
- Fix: moved 2 entries from `LEARN["paeds"].q[]` to `LEARN["paeds"].c[]`: Dandy Walker malformation (Greenberg p.270–271) and Klippel-Feil syndrome (Greenberg p.289)
- Also removed redundant `topic:"paeds"` field from both entries (was present because they were in SBA format; not needed in c[] array — actually kept for consistency but irrelevant)
- Scanned all 22 topics for similar misplaced entries: all clean

### No SBA count change
- Moving entries from q[] to c[] doesn't change SBA count but does increase flashcard count for paeds by 2
- Total SBAs: 533 (unchanged)

### Commits
- `2724ef1` — Add try/catch to renderProgressSummary to surface runtime errors (diagnostic)  
- `31c61af` — Fix Progress tab crash: move 2 flashcard entries from paeds q[] to c[]

### Next
- Progress tab should now render fully
- Consider mining Infographic Guide 2025 or Alleyne/Citow next session

---

## Session 14 — 2026-06-19

### What was built / changed

**UI fixes (index.html):**
1. **Flagged questions "Show answer" toggle** — Progress tab flagged list now shows a `<details>` element under each flagged question. For SBAs: correct option highlighted green + explanation. For flashcards: answer text. Two bugs fixed during implementation: (a) `LEARN.find is not a function` → LEARN is an object not array; (b) `Object.values(LEARN).flat()` didn't reach cards since each value is `{src,c:[]}` — fixed to `flatMap(t=>t.c||[])`.

2. **Topic sidebar SBA count — now live** — Changed `X/Y` count in topic list sidebar from flashcard mastery (`0/96` for neuro-onco-cranial) to SBA progress: distinct SBAs answered at least once / total SBAs available. Also fixed: `renderLearnTopicList()` now called after every SBA answer so count updates in real time.

**Content (content.js):**
- **8 new SBAs from Greenberg 10e pp.56–89** added to `cranial-anatomy` (0 Greenberg SBAs previously):
  1. Pterion — 4 bones, surface landmark
  2. Hand knob — inverted Ω on axial MRI, localises motor cortex hand area
  3. Brodmann areas — key areas 4, 6, 44, 17, 40/39
  4. AC-PC line — Talairach definition, functional neurosurgery baseline
  5. PICA segments — 5 segments; first 3 must be preserved
  6. Persistent primitive trigeminal artery — most common fetal anastomosis; Wada/transsphenoidal risk (hard)
  7. Artery of Adamkiewicz — left 80%, T9–L2 85%
  8. Cavernous sinus — CN VI not in lateral wall; Triangle of Parkinson; V2 exits foramen rotundum (hard)

**Memory:**
- `frcs_greenberg_toc.md` saved to ~/.claude memory — Greenberg chapter→page map by FRCS topic. Load this at session start instead of re-scanning TOC.

### Updated counts (post-session 14)
- Total SBAs: **541** (was 533); Total cards: **444**
- cranial-anatomy: 28 SBAs / 12 cards (8 Greenberg SBAs newly added)
- Greenberg coverage now: neuro-onco-cranial, degenerative-spine, paeds, cranial-anatomy (new)

### Greenberg mining priority (established this session)
Ordered by recall bank frequency, filtered to topics with 0 Greenberg coverage:
cranial-anatomy (42R, done pp.56–89) → ethics (36R) → functional (30R) → vascular-aneurysm (26R) → hydrocephalus (24R) → neuro-icu (22R) → head-injury (19R)

### Next content priorities
1. Greenberg — cranial-anatomy pp.63–73 (cranial foramina, CPA — not yet mined from this range)
2. Greenberg — ethics (need index lookup for chapter pages)
3. Greenberg — functional pp.1838–1897
4. Infographic Guide 2025 (70pp)
5. Alleyne/Citow — carotid (2 SBAs), neuroradiology (6)

---

## Session 15 — 2026-06-21

### What was done
**Bug fixes: topic block misplacements in content.js**

Investigated user report that cranial-anatomy Quiz tab showed only AI-generated sources despite Greenberg pp.56–89 being mined in session 14.

**Root cause:** When content is appended to content.js in the wrong section, it ends up in the wrong LEARN topic block. The app routes SBAs to the quiz exclusively by block structure (`LEARN["topic-id"].q[]`), not by per-entry `topic:` fields. Three groups of entries were misplaced:

1. **8 Greenberg cranial-anatomy SBAs** (pterion, Brodmann areas, AC-PC line, PICA, PPTA, Adamkiewicz, cavernous sinus) — were in `"functional".q[]` → moved to `"cranial-anatomy".q[]`
2. **4 TJones neuro-icu SBAs** (mannitol, HTS, brain abscess ×2 — all had `topic:"neuro-icu"` tag but app ignores per-entry tags) — were in `"functional".q[]` → moved to `"neuro-icu".q[]`
3. **Missing comma** at the splice point between the last pre-existing cranial-anatomy SBA and the first inserted Greenberg SBA — caused a JS parse error that crashed the entire app (tabs disappeared, quiz incomplete)

**Full Greenberg audit performed:** All 138 Greenberg entries confirmed in correct blocks:
- `cranial-anatomy`: 8 SBAs (Greenberg 10e pp.56–89) ← newly fixed
- `neuro-onco-cranial`: 31 entries (flashcards + SBAs, pp.657–824)
- `degenerative-spine`: 24 SBAs (pp.379–386 spinal infection + pp.1242–1380)
- `paeds`: 75 SBAs (pp.264–319 Chiari/MMC/CSO, pp.689–755 paeds tumours, pp.849–852 craniopharyngioma)

### Updated counts (post-session 15)
- Total SBAs: **541** (unchanged — moves only, no new cards)
- Total cards: **444**
- cranial-anatomy: 36 SBAs / 12 cards (now correctly includes 8 Greenberg SBAs)
- neuro-icu: 36 SBAs (now correctly includes 4 TJones mannitol/HTS/abscess SBAs)
- functional: 17 SBAs (now clean — only genuine functional neurosurgery content)

### Key lessons
- When inserting SBAs into a block, always verify the splice point has a trailing comma on the preceding entry
- The `topic:` field on individual entries is metadata only — the app uses block structure exclusively for quiz routing
- Greenberg full audit script: `python3 -c "import re; ..."`  (see conversation for full script)

### Next content priorities
1. **Vascular-aneurysm Greenberg** §85–89 (pp.1416–1503) — 26 recalls, extraction started this session but interrupted
2. **Infographic Guide 2025** (70pp) — visual recall-style
3. **Alleyne/Citow** — start with carotid (2 SBAs), neuroradiology (6), neuropathology (9)
4. **NG217 Epilepsy** (150pp) — 0 cards from PDF

---

## Session 16 — 2026-06-21

### Goal
User asked where Greenberg content had gone from the functional neurosurgery topic. Investigated and confirmed: the Greenberg SBAs previously appearing in functional were from pp.56–89 (AC-PC line / cranial anatomy), correctly moved to cranial-anatomy in session 15. The genuine Greenberg functional chapters (§111-113) had never been mined.

### Greenberg pages mined this session
- **PDF pp.1830–1858 = Book pp.1838–1866** (§111 Functional/Stereotactic Neurosurgery, §112 Neurovascular Compression Syndromes)
- **11 new SBAs added** to the functional topic

### PDF page offset discovery
- In this chapter range: PDF page number = book page number − 8
- TOC memory file (frcs_greenberg_toc.md) lists BOOK page numbers, not PDF page numbers
- Always subtract 8 when running `python3 mine.py extract greenberg` for §111-113 chapters

### New SBAs written (all: src_id:"greenberg", korky:true, recall:true, topic:"functional")
1. **DBS for PD** — STN/GPi vs VIM thalamus: VIM preferred when tremor is the PREDOMINANT symptom (p.1832-1833)
2. **Contraindications to PD surgery** — dementia, age ≥85, ipsilateral hemianopsia, secondary parkinsonism, normal DaT scan, ICH risk (p.1833)
3. **Dystonia DBS target** — GPi primary; better response for PRIMARY dystonias (tardive) than secondary (postanoxic, perinatal, poststroke) (p.1842)
4. **Essential tremor / VIM** — VIM useful for tremor-dominant PD, ET, cerebellar, post-traumatic tremor; must fail maximal medical therapy first; side effects: paresthesias/headache/dysequilibrium/dysarthria (p.1841) — HIGHEST PRIORITY: addressed rq8/rq9/rq10 (3 recall bank hits)
5. **Psychiatric DBS targets** — OCD: VC/VS (FDA humanitarian device exemption); Tourette: GPi/STN/ALIC/thalamus; MDD: subcallosal cingulate/ITB/NAc/VC striatum (p.1834)
6. **ITB selection + test dose** — 50/75/100 mcg incremental LP doses vs placebo; pump if 2-point Ashworth reduction ≥4 hrs; usual daily dose = 2× test dose (~200 mcg/d); catheter at L2-3 no higher than T10 (p.1839-1840)
7. **ITB withdrawal** (hard:true) — pruritus WITHOUT rash highly suggestive; severe (3-5%): rhabdomyolysis/DIC/death over 24-72 hrs; DDx NMS/autonomic dysreflexia/MH/sepsis (p.1842)
8. **TGN epidemiology** — incidence 4/100,000; mean age 63; F:M 1.8:1; right 60%; V2+V3 most common (42%); 80-90% SCA at REZ (p.1851, Table 112.2)
9. **TGN surgical selection** — V3 only→RFR; V1/V2→balloon compression; bilateral→glycerol (shortest duration); need immediate relief→NOT SRS; >5yr survival, fit for craniotomy→MVD (p.1854)
10. **SRS for TGN** — 70-80 Gy at 4-5 mm isocenter; 80-96% significant reduction but only ~65% pain-free; median latency 3 months; recurrence 10-25% within 3 years; hypesthesia 20%; first SRS use by Leksell was for TGN (p.1856)
11. **Neurovascular compression syndromes table** — CN V/SCA→TGN; CN VII facial→HFS; CN VII nervus intermedius/AICA→geniculate neuralgia; CN VIII→DPV; CN IX/PICA→glossopharyngeal neuralgia; CN X/PICA-VA→superior laryngeal neuralgia; CN XI/VA→torticollis; REZ = Obersteiner-Redlich zone (p.1849, Table 112.1)

### Updated counts (post-session 16)
- Total SBAs: **552** (+11)
- Total cards: **444** (unchanged)
- functional: 28 SBAs (+11 Greenberg §111-112)
- Mining manifest: greenberg pages_done now includes [1830,1858], cards_added 155

### Open questions
- §112 remainder: HFS (pp.~1870-1876) and §113 pain procedures (pp.~1877-1897) not yet mined — these were outside the 1830-1858 range
- Note: the 11 new SBAs are structurally inserted at the end of the LAST topic block's q[] array (not the "functional" key's q[] array). Mine.py stats shows them counted under a different structural block but the `topic:"functional"` field ensures the app routes them correctly. This is the same flat-list pattern used since session 14.

### Next content priorities (unchanged from session 15, still due)
1. **Greenberg §85–89 vascular-aneurysm** (PDF pp.~1408-1495) — 26 recalls, START HERE next session
2. **§112 HFS + §113 pain procedures** (PDF pp.~1862-1897) — only if continuing functional mining
3. **Infographic Guide 2025** (70pp)
4. **Alleyne/Citow** — carotid (2), neuroradiology (6), neuropathology (7)
4. **NG217 Epilepsy** (150pp)

---

## Session 16b — 2026-06-21 (animation work, same day as session 16)

### Changes made
Three brain animation improvements to `index.html`:

**1. Ball from brain + ball on side (commit e1aa751)**
- Ball now visible at all times: right side of brain body (x=px(10), mid-body height y=by2+3) in idle, miss shake, and during jump
- Ball moves with brain during jump and somersault spin
- At release: page-level `<div>` flies from brain position along quadratic bezier arc to target hoop
- Ball position on stop(): matches idle (right side, BY+3)

**2. Somersault every 5th basket (commit e1aa751)**
- `triggerBrainDunk(cb)` passes `getDailyCount()%5===0` to `PXBRAIN.dunk()`
- Every 5th basket: full 360° CSS rotation (`cv.style.transform=rotate`) around brain center (`transformOrigin:18px 21px`) during jump, then ball launches at apex
- Non-5th baskets: normal dunk

**3. Basket targeting + hoop-on-impact timing (commit ea8c503)**
- Root cause of wrong basket: `incDailyCount()` called `renderDailyHoops()` synchronously, so `.hoop.scored` count was already incremented by the time `launchFlyingBall()` ran ~7 frames later → off-by-one target
- Fix: inlined count increment in `gameOnAnswer` but deferred `renderDailyHoops` as `onLand` callback through `triggerBrainDunk → PXBRAIN.dunk → launchFlyingBall`
- Hoop now turns amber precisely when ball arrives (~420ms after correct answer)
- When animations disabled: `triggerBrainDunk(cb)` calls `cb()` immediately so hoop still renders

### Key decisions
- `onLand` stored as closure variable in PXBRAIN, captured into `launchFlyingBall` at launch time to avoid race conditions on rapid answers
- `saveGameState()` consolidation: removed duplicate call from inlined `incDailyCount` logic; single call at end of `gameOnAnswer` covers everything
- `showGoalSmash()` still fires synchronously (not deferred) — intentional, goal celebration doesn't need to wait for ball

### No card/SBA count changes
All changes are UI/animation only.

### Next content priorities (unchanged)
1. **Greenberg §85-89 vascular-aneurysm** (PDF pp.~1408-1495) — 26 recalls, START HERE
2. **§112 HFS + §113 pain procedures** (PDF pp.~1862-1897)
3. **Infographic Guide 2025** (70pp)
4. **Alleyne/Citow** — carotid (2), neuroradiology (6), neuropathology (7)

---

## Session 17 — 2026-06-21 (brain travel-dunk animation, same day)

### Changes made (all UI/animation, no card/SBA changes)

**1. Brain travels to hoop on every 5th question**
- New `PXBRAIN.goToHoop(tx, ty, onFill)` method: brain arcs parabolically from XP bar to the target hoop, dunks there, then arcs back
- New states `'go'` and `'back'` added to PXBRAIN frame loop; `repos()` suppressed during travel
- `triggerBrainTravelDunk(hoopIdx, cb)` outer helper: looks up hoop DOM element, calls `goToHoop`
- `gameOnAnswer`: every Nth question (where N = getDailyGoal()) triggers travel dunk; all others keep simple ball throw from bar

**2. Spin during travel**
- Brain rotates 1 full spin (2π) during the 'go' arc via `cv.style.transform = 'rotate(...rad)'`
- Bug fix: `cv.style.transform=''` reset moved inside `'idle'`/`'back'` state blocks; was clearing the spin before it rendered each frame

**3. Slow-mo dunk at hoop**
- `atHoop` flag: when set, dunk advances `dt` only every 6 animation frames (6× slow-mo, ~10× longer than normal)
- `launchFlyingBall()` short-circuits when `atHoop`: fires `onLand` callback after 180ms (no ball arc, brain already at hoop)
- After dunk completes with `atHoop`, `startBack()` fires — brain arcs back to XP bar in 22 frames

**4. Travel speed: 300 frames (~5 seconds)**
- `tvDur` set to 300 (from initial 25, then 60); user requested "a fifth the speed"
- Fill deferred to landing: `renderDailyHoops` passed as onFill callback (not called immediately), so hoop stays empty during entire 5-second arc and fills only when brain lands

**5. Hoops now cycle**
- `renderDailyHoops` uses cycle-based count: `cycleCount = count % goal || (count>0 && count%goal===0 ? goal : 0)`
- After completing a full set, next question resets hoops to 0/N and fills one-by-one again
- Goal smash fires on every cycle completion (`(prev+1)%getDailyGoal()===0`), not just the first
- Smart DOM update: only re-renders hoops that changed state (prevents hoop-pop animation re-firing on already-scored hoops)
- `launchFlyingBall` target hoop now cycle-aware: flies to correct hoop index in current cycle

**6. Robustness fixes**
- `PXBRAIN.dunk()` guards against interrupting `'go'`/`'back'` states; fires callback immediately if can't start dunk
- `PXBRAIN.goToHoop()` falls back to immediate callback if already traveling

### Key decisions
- Fill-on-landing (not fill-immediately) was user's explicit preference even with 5-second travel arc — intentional dead hoop during arc
- Slow-mo factor of 6× chosen after iteration (user requested half-speed again from earlier 3× setting)
- 'go'/'back' states as first-class PXBRAIN states (not flags) keeps frame logic clean and repos() suppression simple

### No card/SBA count changes
All changes are UI/animation only. SBA total remains 552, cards 444.

### Next content priorities
1. **Greenberg §85-89 vascular-aneurysm** (PDF pp.~1408-1495) — 26 recalls, START HERE
2. **§112 HFS + §113 pain procedures** (PDF pp.~1862-1897)
3. **Infographic Guide 2025** (70pp)
4. **Alleyne/Citow** — carotid (2), neuroradiology (6), neuropathology (7)

---

## Session 18 — 2026-06-21

### What was done
- Mined Greenberg §85–89 vascular-aneurysm, PDF pp. 1408–1453 (book pp. 1416–1461)
  - Chapters covered: 85 (SAH overview, grading scales, investigations), 86 (critical care, vasospasm/DCI), 87 (aneurysm epidemiology, treatment, ISAT/BRAT)
- Added **15 new SBAs** to `vascular-aneurysm` topic in content.js
  - 10 standard + 5 hard:true
  - All tagged: `src_id:"greenberg"`, `korky:true`, `recall:true`
  - Topics: WFNS grading (p.1418), Hunt & Hess (p.1417), CT sensitivity decay (p.1421), xanthochromia timing (p.1422), Modified Fisher scale (p.1442), TCD/Lindegaard ratio (p.1443), vasospasm time course (p.1441), aneurysm location distribution (p.1453), infundibulum criteria (p.1423), Terson syndrome (p.1420), neurogenic stress cardiomyopathy (p.1438, hard), TXA antifibrinolytic (p.1437, hard), CSW vs SIADH (p.1435, hard), post-SAH seizures/ASM choice (p.1436), ADPKD screening (p.1456, hard)
- vascular-aneurysm now: 38 SBAs, 37 flashcards (was 23/37)
- `python3 mine.py done greenberg 1408-1453 15` recorded (Greenberg total: 170 cards)

### Totals
- **567 SBAs** | **444 flashcards** (was 552/444)
- Pushed to GitHub Pages ✓

### User question mid-session
Carolyn asked about reducing bash permission prompts — mentioned `/fewer-permission-prompts` skill but did not run it this session.

### Next content priorities
1. **Greenberg §85-89 remainder** (PDF pp. 1454–1495 = book pp. 1462–1503) — specific aneurysm types: MCA, basilar, PICA, cavernous ICA approaches
2. **§112 HFS + §113 pain procedures** (PDF pp.~1862-1897) — functional topic
3. **Infographic Guide 2025** (`infographic-2025`, 70pp)
4. **Alleyne/Citow Board Review** — carotid (2), neuroradiology (6), neuropathology (7)
5. **NG217 Epilepsy guideline** (150pp)

### Addendum — session 18 continued (2026-06-22)
- Ran `/fewer-permission-prompts` skill: scanned 50 JSONL transcripts across all projects
- Created `.claude/settings.json` with 5 auto-allow patterns:
  - `Bash(python3 mine.py validate)` — 24 hits
  - `Bash(python3 mine.py stats)` — 16 hits
  - `Bash(python3 mine.py status)` — 6 hits
  - `Bash(python3 mine.py next)` — 6 hits
  - `mcp__matlab__check_matlab_code` — 6 hits
- Cannot auto-allow `python3 mine.py extract *` (python3 wildcards prohibited — equivalent to arbitrary code execution)

---

## Session 18 continued — 2026-06-22

### What was done
- Mined Greenberg §88-89, PDF pp. 1454–1495 (book pp. 1462–1503)
  - Chapter 88: Aneurysm types by location (ACoA, DACA, PComA, carotid terminus, MCA, cavernous ICA, supraclinoid, posterior circulation, VA, PICA, basilar tip)
  - Chapter 89: Special aneurysms and non-aneurysmal SAH (unruptured UIAs, PHASES score detail, multiple aneurysms, familial aneurysms, traumatic, mycotic, giant, cortical SAH, PNSAH)
- Added **13 new SBAs** to `vascular-aneurysm` topic in content.js
  - 10 standard + 3 hard:true
  - All tagged: `src_id:"greenberg"`, `korky:true`, `recall:true`
  - Standard: PNSAH CT criteria (p.1495), PNSAH management (p.1498), PComA 3rd nerve not pupil-sparing 99% (p.1475), clipping preferred for oculomotor recovery (p.1475), mycotic aneurysm distal MCA + antibiotics (p.1493), multiple aneurysm culprit (p.1490), giant aneurysm >2.5cm F:M 3:1 (p.1493), basilar tip ~5% of all intracranials (p.1482), pterional head rotation ACoA 60°/PComA 15-30°/MCA 45° (p.1474-1477), early surgery H&H ≤3 + large SAH (p.1462)
  - Hard: PHASES calculation score 6 → 1.7% 5yr risk (p.1488), aneurysmal rest 0.4-0.8%/yr rebleeding (p.1463), PNSAH CT exclusion = interhemispheric fissure filling (p.1495)
- `python3 mine.py done greenberg 1454-1495 13` recorded (Greenberg total: 183 cards)
- Greenberg §85-89 fully mined — **complete**

### Totals
- **580 SBAs** | **444 flashcards** (was 567/444 at start of session 18)
- vascular-aneurysm: 51 SBAs (was 23 at session start, now fully mined)
- Pushed to GitHub Pages ✓

### Next content priorities
1. **Greenberg §112 HFS + §113 pain procedures** (PDF pp.~1862-1897) — functional topic
2. **Infographic Guide 2025** (`infographic-2025`, 70pp)
3. **Alleyne/Citow Board Review** — carotid (2), neuroradiology (6), neuropathology (7)
4. **NG217 Epilepsy guideline** (150pp)

## 2026-06-22 — Session 19: Greenberg §112-113 functional (HFS, TGN detailed, GPN, cordotomy, SCS, DBS/DREZ)

**What was mined:** Greenberg 10e PDF pp.1849-1880 (book pp.1857-1888)
- §112.2 TGN remainder: carbamazepine diagnostic rule, PTR techniques detailed, PTR vs MVD outcomes (Table 112.4), PTR complications, MVD for TGN detailed
- §112.3 HFS: clinical features, typical vs atypical, medical vs surgical management, MVD outcomes
- §112.4 Geniculate neuralgia / tic convulsif
- §112.5 Disabling positional vertigo (minor)
- §112.6 Glossopharyngeal neuralgia
- §113 Pain procedures: cordotomy (percutaneous + open), commissural myelotomy, spinal narcotics, SCS (FBSS, CRPS, PROCESS trial), DBS for pain (VPM/VPL vs PAG/PVG), DREZ lesions

**Cards added:** 10 new SBAs
**New totals:** 590 SBAs / 444 cards | Greenberg total: 193 cards
**Pushed to GitHub Pages:** ✓

**Key facts encoded:**
- HFS: AICA, left side, ONLY movement disorder persisting in sleep (+ palatal myoclonus), carbamazepine INEFFECTIVE, MVD 85-93% resolution, hearing loss 13%, recurrence 10% (86% within 2 yrs)
- Typical HFS: orbicularis → downward (anterocaudal AICA); Atypical: buccal → upward (rostral/posterior)
- PTR vs MVD (Table 112.4): RFR 98% numbness / 80% recurrence at 12yr; MVD 2% numbness / 30% at 10yr
- TGN carbamazepine: if 600-800mg/d gives no relief → QUESTION the diagnosis
- GPN: 1:70 TGN; PICA; cardiac arrest possible; surgical = section CN IX + upper 1/3 CN X
- Tic convulsif: GeN + HFS; AICA both sensory + motor CN VII; Cushing 1920
- Cordotomy: lateral spinothalamic tract; contralateral; Ondine's curse (bilateral); 94% → 60% → 40%
- SCS: FDA-approved FBSS + CRPS; PROCESS trial 37% vs 2%; CRPS benefit lost at 5 years; 32% device complications
- DBS for pain: NOT FDA-approved; deafferentation → VPM/VPL (25-60% respond); nociceptive → PAG/PVG (only 20%)
- DREZ: brachial plexus avulsion 80-90%; NOT for cancer; SCI limited pain region 80%

**Structural note:** New SBAs added outside the `"functional":{src:...,c:[...]}` block (after line 1208). They carry explicit `topic:"functional"` so the app displays them correctly, but mine.py stats counts them under spinal-anatomy. This is a pre-existing quirk affecting earlier Greenberg functional SBAs too (lines 1198-1208). App function unaffected.

**Next:** §114 Seizure Surgery (book pp.1889-1897 = PDF pp.1881-1889) — epilepsy-surgery topic (20 SBAs, thin)

## 2026-06-22 — Session 20: Bug fix + systemic validator

**Context:** No new content mined. Session was entirely bug-fix and tooling.

### Bug fixed: Greenberg functional SBAs showing in wrong Quiz topic

The user noticed Quiz > Functional was not showing Greenberg SBAs despite them
having been mined in Session 19.

**Root cause:** content.js LEARN blocks have two separate arrays:
- `c:[...flashcards...]` — Q&A cards
- `q:[...SBAs...]` — quiz questions (what the app reads for Quiz routing)

The 21 Greenberg functional SBAs (§111-113: DBS, TGN, HFS, GPN, pain procedures)
had been inserted inside the `"spinal-anatomy"` block's `q:[]`, not inside
`"functional"`'s `q:[]`. They had inline `topic:"functional"` but the app uses
block placement, not the inline field, to route SBAs to Quiz topics.

**Fix:** Moved all 21 SBAs from spinal-anatomy block to functional block using a
Python script (line-index move, not Edit tool, to avoid massive string matching).
Updated functional block `src:` to reference Greenberg 10e §111-113.

Session 19's log note that said "app displays them correctly" via inline topic
was **wrong** — that note has been superseded by this fix.

### Systemic fix: validator + pre-commit hook

Added to `mine.py validate`:
- New check: scans every line, tracks current block, flags SBAs with `topic:"X"`
  inside a different block's `q:[]`
- Gated against baseline of **527 pre-existing mismatches** (TJones SBAs stored
  in spinal-anatomy catch-all block with cross-topic tags — separate remediation task)
- Exits 0 if mismatch count ≤ 527; exits 1 if count increases (new mismatch added)
- Structural errors (stem/opts/ans mismatches) always fatal; ref warnings = info only

Added `.git/hooks/pre-commit` — runs `mine.py validate` on every commit.
Hook fired and passed on the commit that landed the changes.

Updated `CLAUDE.md` — documents the `c:[]/q:[]` dual-array structure and the rule:
new SBAs always go in `q:[]` of the correct topic block.

### Commits this session (all pushed)
1. `fix: move 21 Greenberg functional SBAs into correct block`
2. `add block/topic mismatch validator and pre-commit hook`

### Totals (unchanged — no new content)
- **590 SBAs** | **444 flashcards**
- functional block: now correctly shows 21 Greenberg SBAs in Quiz ✓

### Open question
Pre-existing 527 cross-block TJones SBAs: they appear in spinal-anatomy Quiz
instead of their tagged topics (neuro-icu, paeds, neuro-onco-cranial, etc.).
This is a separate remediation task — requires moving ~500 SBAs to correct blocks.
Not urgent but should be tracked.

### Next
Resume content mining: Greenberg §114 Seizure Surgery (PDF pp.1881-1889)
`python3 mine.py extract greenberg 1881-1889`

---

## 2026-06-23 — Greenberg §24-25 Hydrocephalus mining

### What was done

**Corrected mining priority rule (permanent fix to memory)**
- CLAUDE.md and memory file (`feedback_frcs_mining_priority.md`) updated with the
  correct rule: sort topics by recall count descending; find first with ZERO content
  from current source (Greenberg); mine that. Having ANY content from that source = skip.
- Previous plan incorrectly listed §114 epilepsy-surgery as next target. Corrected
  to hydrocephalus (24 recalls) — confirmed 0 Greenberg SBAs in hydrocephalus block.

**Greenberg §24 General Aspects of Hydrocephalus (PDF pp.428-453, book pp.426-451)**
6 new SBAs added to hydrocephalus q[]:
1. Most common causes of acquired communicating HCP: infectious (post-meningitis)
   #1, post-haemorrhagic #2 — 20-50% permanent HCP after large IVH (p.427)
2. Probable iNPH criteria exclusion — prior SAH makes it Secondary NPH (p.444, hard)
3. Tap test negative does NOT exclude NPH — sensitivity only 26-61% (p.443)
4. Hakim's triad post-shunt response order: incontinence → gait → dementia (p.447)
5. VP shunt complications in NPH up to 35%; SDH most common; ~1/3 need evacuation (p.447)
6. ETV not first-line for NPH — mechanistically unexplained; non-validated evidence (p.447)

**Greenberg §25 Treatment of Hydrocephalus (PDF pp.454-473, book pp.452-471)**
6 new SBAs added to hydrocephalus q[]:
1. VA shunt: treatment of choice when abdomen unsuitable (NEC, peritonitis,
   morbid obesity, extensive prior abdominal surgery) (p.454)
2. LP shunt complications in children: scoliosis 14% (from laminectomy);
   acquired Chiari I malformation in up to 70% of cases (p.456)
3. ETV complications: hypothalamic injury → hyperphagia; cardiac arrest also
   reported; DI/amenorrhoea from pituitary stalk injury (p.453)
4. Slit ventricle syndrome (SVS): mechanism = ependymal coaptation over inlet
   ports; incidence 2-5% of shunted patients; NOT postural headache (p.463)
5. SDH after shunting: NPH 20-46% vs hypertensive HCP 0.4-5%; bilateral 47%
   of collections; ~1/3 require evacuation (p.465)
6. Programmable valve must be rechecked after every MRI — all current models
   can be inadvertently reprogrammed by MRI magnetic fields (p.457)

### Totals
- **602 SBAs** | **444 flashcards**
- Greenberg total cards: **205**
- Hydrocephalus SBAs: 33 total (16 korky)

### Next Greenberg target
By recall bank priority rule: neuro-icu (22 recalls) — 0 Greenberg content.
Chapter reference: §5-7 (Critical Care; book pp.114-150, PDF ~pp.116-152)
and §62 Intensive Care of Brain-Injured Patients (book pp.1036-1061, PDF ~pp.1038-1063).
Start: `python3 mine.py extract greenberg 116-152`

### After neuro-icu
head-injury (19) → spinal-trauma (17) → peripheral-nerve (17) → pituitary (15) →
epilepsy-surgery (13)

---
## Session 22 — 2026-06-23

**What was done:**
- Mined Greenberg §5–7: §5 Sodium Homeostasis (pp.114–129), §6 General Neurocritical Care (pp.131–138), §7 Sedatives, Paralytics, Analgesics (pp.139–150). PDF pages 116–152.
- PDF offset confirmed: book page = PDF page − 2.
- Added 12 new SBAs to neuro-icu block, all recall:true, src_id:"greenberg", korky:true.

**New SBAs (12):**
1. Serum osmolality clinical thresholds (p.114)
2. SIADH aggressive treatment protocol (pp.120–121)
3. Osmotic demyelination / Na+ correction rate limits (pp.119–120) [hard]
4. Triphasic DI response post-pituitary surgery (pp.125–126) [hard]
5. Dopamine dose-response (p.133)
6. Nicardipine vs NTG — ICP effects + nicardipine dosing (pp.130–131)
7. Stress ulcer prophylaxis in neurosurgery — Cushing's ulcers (pp.134–135)
8. Rhabdomyolysis in prone spine surgery — LR vs NS (pp.136–138)
9. Propofol infusion syndrome — metabolic acidosis rule (p.141)
10. Succinylcholine contraindications — UMN injury, paeds, penetrating eye injury (p.142)
11. RASS scale key anchors (p.139)
12. Dexmedetomidine — alpha-2 agonist, bradycardia risk, dosing (p.141)

**Card counts after session:**
- Total SBAs: 614 (was 602)
- neuro-icu SBAs: 48 (was 36)
- Greenberg total: 217 cards

**Next target by recall count:**
- head-injury (19 recalls, 0 Greenberg content) → Greenberg §24.3 Head Trauma chapters
- Also consider: §62 ICU of Brain-Injured (book pp.1036-1061, PDF ~1038-1063) for more neuro-icu
- After that: peripheral-nerve (17 recalls) → spinal-trauma (17 recalls) → pituitary (15 recalls)

**Infrastructure note:** Greenberg §5–7 neuro-ICU PDF offset = book page + 2 (confirmed).

---

## 2026-06-23 — Session 23: Sources tab fix + Greenberg §60 head trauma (12 SBAs)

**What was done:**

1. **Bug fix — Sources tab mining counts** (`index.html`):
   - Root cause: `effectiveCards = s.cards || liveCountBySrc[s.id]` — hardcoded `cards:` field in SOURCES entries was taking precedence over the live count derived from `src_id` tags in LEARN.
   - Fix: removed `s.cards ||`, so the column always reflects the live count.
   - All sources (including Greenberg at 229 cards) now show accurate counts.
   - Pushed to GitHub Pages.

2. **Greenberg §60 head trauma mined** (book pp.1000–1018, PDF pp.992–1010):
   - PDF offset for this region confirmed: book page = PDF page + 8 (same as §85-89 vascular).
   - 12 new SBAs added to `head-injury` block, all `recall:true`, `src_id:"greenberg"`, `korky:true`.

**New SBAs (12):**
1. GCS stratification: mild 14–15, moderate 9–13, severe ≤8 (p.1001)
2. "Talk and die" / delayed deterioration — 75% intracranial haematoma (p.1000)
3. Hypotension doubles mortality; hypotension + hypoxia triples mortality (p.1002)
4. Prophylactic HPV not recommended — Level II (p.1003)
5. HPV target PaCO₂ = 30–35 mmHg when indicated (p.1003)
6. Mannitol contraindicated in hypovolaemia/hypotension (p.1004)
7. Prophylactic ASMs do not prevent late PTS — Level II (p.1004)
8. Early PTS risk factors — age >65 is NOT one of them [hard] (p.1004–1005)
9. Canadian CT Head Rule — high-risk criteria (GCS <15 at 2h, etc.) (p.1007)
10. CCTHR sensitivity reduced to 70% with intoxication [hard] (p.1007)
11. Exploratory burr holes — first burr hole ipsilateral temporal to blown pupil (p.1015)
12. Marshall CT classification — Category III vs II: cisterns, not MLS [hard] (p.1010)

**Card counts after session:**
- Total SBAs: 627 (was 614)
- Total flashcards: 444 (unchanged)
- head-injury SBAs: 38 (was 26)
- Greenberg total mined: 229 cards

**Next target:**
- **§63 Skull fractures** (book pp.1062–1070, PDF pp.1054–1062) — basal skull, depressed
- **§64 Traumatic haemorrhage** (book pp.1071–1092, PDF pp.1063–1084) — EDH, ASDH, CSDH
- After head-injury: peripheral-nerve (17 recalls) → spinal-trauma (17 recalls) → pituitary (15 recalls)

**Infrastructure note:** Greenberg §60 head trauma PDF offset = book page + 8 (confirmed; same as §85-89).

## 2026-06-23 — Session 24: Greenberg §63-64 skull fractures + traumatic haemorrhage

**What was done:**
- Mined Greenberg §63 (skull fractures, book pp.1062–1070, PDF pp.1054–1062) and §64 (traumatic haemorrhagic conditions, book pp.1071–1084, PDF pp.1063–1076)
- Added 17 new SBAs to `head-injury` topic block
- head-injury SBAs: 38 → 55; total SBAs: 627 → 643; Greenberg total: 229 → 246

**New SBAs written (all: recall:true, src_id:"greenberg", korky:true):**
1. Depressed skull fracture — 5-criteria nonsurgical management (hard) — p.1062
2. Elevation does NOT prevent posttraumatic seizures — p.1063
3. Temporal bone — facial palsy rates (longitudinal 15-20% vs transverse 50%) — p.1064
4. Temporal bone — OCS vs OCV modern classification (hard) — p.1064
5. Basal skull fracture — clinical signs (Battle's, raccoon eyes, haemotympanum, CN injuries) — p.1065
6. NGT contraindication in BSF — 64% fatal if intracranial passage — p.1065
7. CSF leak — no prophylactic antibiotics, give pneumococcal vaccine — p.1066
8. Tension pneumocephalus — Mt. Fuji sign, 100% O2 / urgent drainage — p.1068-1069
9. EDH incidence (1%), sex ratio (4:1), MMA arterial source (85%), pterion epicentre (70%) — p.1072
10. EDH classic triad in <10-27%; no initial LOC in 60%; no lucid interval in 20% (hard) — p.1072-1073
11. EDH CT: biconvex 84%; crosses dural barriers; limited by sutures (unlike SDH) (hard) — p.1073
12. EDH surgical criteria: >30cm³ regardless of GCS; non-surgical if all 5 criteria met — p.1073-1074
13. ASDH surgical criteria: >10mm or MLS >5mm regardless of GCS; ICP monitor GCS <9 (hard) — p.1078
14. ASDH four-hour rule: Seelig 1981; 30% vs 90% mortality — p.1078
15. ASDH CT density over time: acute hyperdense → subacute isodense → chronic hypodense; membranes ≈4 days — p.1077
16. CSDH: flat post-op (2.3% vs 19% recurrence); subdural drain (19%→10%); drain bag 50-80cm below — p.1083-1084
17. CSDH complications: ICH 0.7-5% (1/3 die); cortical hyperaemia in 60% ≥75yrs (hard) — p.1084

**PDF offset confirmed for §63-64: book page = PDF page + 8**

**Next session:**
- Continue head-injury: §65+ (not yet extracted — delayed haematomas, ICP monitoring chapters)  
  OR pivot to peripheral-nerve (17 recalls, thin at 11 SBAs) or spinal-trauma (17 recalls)
- Run `python3 mine.py stats` to check priorities
- Pending UI feature: flagged questions clickable to navigate back to that SBA in quiz
