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
