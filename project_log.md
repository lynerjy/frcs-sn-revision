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
