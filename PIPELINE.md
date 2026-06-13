# FRCS (SN) Revision — Content Pipeline & Provenance

**Purpose:** Document exactly how every flashcard, SBA, and piece of content in this app was created, so any card can be traced back to its source.

---

## Pipeline overview

```
Source PDF/document
       |
       v
mine.py extract <id> <pages>   -- extracts raw text from PDF via pdfplumber
       |
       v
Claude reads extracted text     -- never generates from memory
       |
       v
Claude writes cards with        -- each card gets: exact ref (section + page),
exact page references             korky:true if from Korky folder, topic assignment
       |
       v
Cards added to content.js       -- manually inserted into the LEARN object
       |
       v
mine.py done <id> <pages> N    -- logs session in mining_manifest.json
       |
       v
mine.py validate               -- structural integrity check on content.js
```

### Key rules

1. **No cards from memory.** Every card must be created by reading the actual source text extracted by `mine.py extract`. Claude must never generate medical facts from training data alone.
2. **Exact references required.** Every card has a `ref` field with section number AND page number (e.g., `NG99 1.2.19, p12`).
3. **Korky tagging.** Cards sourced from the Korky folder (`~/Harvard University Dropbox/.../Sista & Me/FRCS Exam/`) are tagged `korky:true`.
4. **Topic assignment.** Each source has pre-assigned topics in `mine.py` SOURCES registry. Cards are placed into the matching LEARN topic block in `content.js`.
5. **Recall bank is NOT an answer source.** The recall banks (recalled exam questions) inform what questions to ask, not what answers to give. Answers must come from verified sources (guidelines, papers, textbooks). See "Recall Bank" section below.

---

## Provenance chain

For any card in the app, trace it back:

```
Card in app (Learn/Quiz tab)
  -> ref field (e.g., "NG228 1.2.4, p18")
  -> source PDF (e.g., guidelines/nice_ng228_sah.pdf, page 18, section 1.2.4)
  -> mining_manifest.json (session log: date, pages, card count)
  -> mine.py SOURCES registry (source metadata, priority, korky flag)
```

---

## What has been built (history)

### Phase 1: App scaffolding (May 2025)

- Created `index.html` — single-page app with 5 tabs (Sources, Topics, Learn, Quiz, Calendar)
- Created `content.js` — data file with SOURCES (27 entries), TOPICS (22 syllabus domains), LEARN (flashcards + SBAs)
- Created `README.md` — source library with URLs, categories, and download status
- Created `sources.json` — machine-readable source list
- Downloaded 8 guideline PDFs to `guidelines/`
- All state persisted to localStorage

### Phase 2: Guideline mining (May 2025)

Cards were created by reading extracted PDF text. Each batch below was produced by:
1. Extracting text via pdfplumber (before mine.py existed, done inline)
2. Claude reading the text and writing cards with exact section/page refs
3. Manual insertion into content.js

| Source | Topic(s) | Cards | SBAs | Method |
|--------|----------|-------|------|--------|
| NICE NG228 — SAH (2022) | vascular-aneurysm | 22 | 8 | Full PDF read, cards written with NG228 section refs |
| NICE NG232 — Head Injury (2023) | head-injury | 19 | 7 | Full PDF read, cards written with NG232 section refs |
| NICE NG99 — Brain Tumours (2021) | neuro-onco-cranial | 57 | 12 | Full PDF read (all pages), most thoroughly mined source |
| NICE NG234 — Spinal Mets/MSCC (2023) | neuro-onco-spinal | 10 | 4 | Full PDF read |
| Endocrinology Pituitary Apoplexy (2024) | pituitary | 8 | 2 | Full PDF read |

### Phase 3: Seed cards for remaining topics (May 2025)

To ensure every topic had at least some content, seed cards were created for 17 topics that had no guideline-sourced content. These were written based on standard neurosurgical knowledge (not PDF-extracted), and are clearly identifiable by their generic `ref` fields (no page numbers — e.g., `ref:"Standard neurosurgical teaching"`).

**These seed cards should be replaced with PDF-verified cards as mining progresses.**

| Topic | Seed cards | Seed SBAs | Status |
|-------|-----------|-----------|--------|
| cranial-anatomy | 8 | 2 | Needs PDF replacement |
| spinal-anatomy | 6 | 2 | Needs PDF replacement |
| neuropathology | 7 | 2 | Needs PDF replacement |
| neuroradiology | 8 | 2 | Needs PDF replacement |
| vascular-avm | 5 | 1 | Needs PDF replacement |
| vascular-ich | 6 | 3 | Needs PDF replacement |
| carotid | 5 | 2 | Needs PDF replacement |
| spinal-trauma | 8 | 2 | Needs PDF replacement |
| degenerative-spine | 6 | 2 | Needs PDF replacement |
| hydrocephalus | 8 | 2 | Needs PDF replacement |
| epilepsy-surgery | 8 | 2 | Needs PDF replacement |
| functional | 6 | 2 | Needs PDF replacement |
| peripheral-nerve | 6 | 1 | Needs PDF replacement |
| paeds | 6 | 2 | Needs PDF replacement |
| neuro-icu | 7 | 2 | Needs PDF replacement |
| neurophysiology | 6 | 1 | Needs PDF replacement |
| ethics | 8 | 3 | Needs PDF replacement |

### Phase 4: Mining infrastructure (May 2025)

- Created `mine.py` — orchestrator with commands: status, next, extract, done, validate, stats, refs
- Initially registered 46 sources in the SOURCES registry
- Created `mining_manifest.json` — session tracking
- Catalogued Korky folder structure

### Phase 5: Korky folder integration (May 2025)

- Added Korky folder toggle to Sources tab (dropdown filter)
- Added Korky toggle bar to Learn tab (gold bar, only shown when topic has Korky content)
- Added Korky toggle to Quiz tab
- Added `korky:true` flag support to card format
- **No Korky-sourced cards mined yet** — infrastructure only

### Phase 6: Recall Bank tab + comprehensive mining plan (May 2026)

**Recall Bank tab — initial build:**
- Added Recall Bank as a 6th tab in the app
- Parsed and categorized recalled exam questions from 2 recall PDFs (`recall-questions` 9pp, `recall-2021` 12pp) → 315 questions across 21 syllabus topics
- Recall bank questions clearly marked as "question prompts" — they inform what to study, not what the answers are

**Recall Bank — expanded with docx files:**
- Extracted and categorized `Bank_Imp topics and Questions.docx` → 111 additional question prompts
- Extracted and categorized `My post-exam notes.docx` → 65 additional question prompts
- **Total recall bank: 491 questions from 4 sources across all 22 syllabus topics**

**Recall Bank UI redesign:**
- Replaced long scroll list with collapsible topic accordions — click to expand/collapse
- Each topic shows coloured dot, name, and question count
- Questions inside each accordion are compact single lines with source label
- Source filter dropdown covers all 4 recall sources
- Search auto-expands matching topics

**Comprehensive source audit and registration:**
- Audited all files in the Korky folder against mine.py registry
- Found 7 missing papers in Key Papers folder (Sivakumar, Smith, Hashimoto, Kumpe, Couture, Delwel, Jahangiri) — registered all 25 papers
- Found 9 missing files in Books for FRCS Pt.1 (Bank MCQs x2, Damirez anatomy, Emergency Head Injury, Nader cases, Alleyne self-assessment, Oxford Textbook, Schmidek & Sweet, Shaya Q&A) — registered all 15 top-level files
- Found 13 missing files in Aberdeen folder (Exam tips, TJones original, Goldman/Humphrey visual fields, Viva Q Jim, 7 PowerPoint files) — registered all 29 files
- **Total registered Korky sources: 71 (was 46)**

**Mining plan created (`MINING_PLAN.md`):**
- Systematic mining order follows actual folder structure (not invented categories)
- Folder 1: Recall Bank docx (2 sources) → Folder 2: Key Papers (25 sources, 219pp) → Folder 3: Books Pt.1 (15 sources, 9,029pp) → Folder 4: Aberdeen (29 sources, 424pp + pptx)
- 20-page chunks, fully resumable via `mine.py next`
- Total scope: 71 sources, ~9,672 pages

**Mining infrastructure updates:**
- Rebuilt `mine.py` MINING_ORDER to follow folder structure
- Added PowerPoint text extraction support (python-pptx) to `mine.py`
- Added .txt file extraction support
- `mine.py next` now shows folder labels, overall progress %, and next 3 sources
- Created `PIPELINE.md` (this file) for full provenance documentation

---

## Recall Bank — special handling

Four sources of recalled exam questions (491 total):
- `recall-questions` (compiled bank PDF, 9pp) — 210 questions
- `recall-2021` (2021 sitting PDF, 12pp) — 105 questions
- `recall-imp-topics` (important topics docx) — 111 questions
- `recall-post-exam-notes` (post-exam notes docx) — 65 questions

They are:

- **Informal and messy** — shorthand, typos, incomplete options, sometimes just topic keywords
- **Question prompts, NOT answer sources** — they tell us what the exam asks about, not what the correct answer is
- **High signal** — these are the closest thing to real exam questions available

### How to use them

1. Read a recall bank question to identify the **topic and concept** being tested
2. Find the **verified source** (guideline, paper, textbook) that covers that concept
3. Create flashcards/SBAs from the **verified source**, ensuring the card covers the concept the exam tested
4. The recall bank question itself appears in the Recall Bank tab for reference, NOT as a flashcard

### What NOT to do

- Do NOT create flashcard answers based on the recalled answer hints (e.g., "we think option A")
- Do NOT use recall bank text as `ref` fields
- Do NOT treat the answer hints as verified — they are exam candidates' recollections, not confirmed answers

---

## Source registry

All sources are registered in `mine.py` SOURCES dict with:
- `label` — human-readable name
- `path` — absolute file path
- `priority` — 1 (highest) to 4 (lowest)
- `type` — recall_bank | landmark_paper | nice_guideline | course_material | textbook
- `topics` — list of syllabus topic IDs this source maps to
- `korky` — True if from the Korky folder
- `note` — context about the source

See `mine.py` for the full registry (76 sources total: 71 Korky + 5 non-Korky guidelines/resources).

---

## Current totals (as of 2026-06-10)

**Flashcards & SBAs:**
- 337 flashcards across 22 topics
- 77 SBAs across 22 topics
- 107 Korky flashcards + 11 Korky SBAs from 13 Key Papers
- ~165 PDF-verified cards (guidelines + papers with exact page refs)
- ~135 seed cards without `src_id` (need PDF replacement — see note below)

**Recall Bank:**
- 491 recalled exam questions from 4 sources
- Categorized across 22 syllabus topics
- Displayed in collapsible accordion UI

**Mining pipeline:**
- 76 sources registered in mine.py (71 Korky + 5 non-Korky)
- 71 Korky sources in mining order, ~9,672 pages
- 13/71 mined (Sivakumar, Casey [no text], NASCIS 3, ISUIA, Patchell, Stupp, SPORT, Berger, ISAT, Santarius, Smith, Hashimoto, Kulkarni)
- Next: `python3 mine.py next` → Anand 2011 (MVD in elderly)

### Note on seed cards (135 cards without `src_id`)

During Phase 3 (May 2025), before the mining discipline was established, ~135 "seed cards" were written from Claude's training data to populate every topic. These predate Rule 1 ("no cards from memory") and are identifiable by generic `ref` fields (`ref:"Standard neurosurgical knowledge"`, `ref:"ASIA classification"`, etc.) and the absence of a `src_id` field.

**These cards may be correct but are unverifiable.** They should be replaced with PDF-sourced cards as mining progresses through the Aberdeen notes, Greenberg, and TJones revision notes. As verified cards accumulate per topic, seed cards can be identified (no `src_id`) and retired.

The `src_id` system (added 2026-06-10) makes this tractable: any card in the app without `src_id` is a seed card.

---

## TODO

- **Recall-bank-driven SBAs:** Use the 491 recall bank questions as templates to write SBAs that test the mined flashcard knowledge. Back-infer the actual exam question from each recall entry, write a proper SBA with verified answers. Work through topic by topic, prioritising topics with the most recall bank entries (neuro-onco-cranial 62, degenerative-spine 52, vascular-aneurysm 26, neuro-icu 22, spinal-trauma 17). Propose this when resuming via `/frcs`.

---

## Mining log

*Append new entries here as mining sessions are completed.*

| Date | Source ID | Pages | Cards added | Notes |
|------|-----------|-------|-------------|-------|
| 2026-05-26 | paper-sivakumar-hyponatraemia | 1-9 | 8 cards | neuro-icu: SIADH vs CSW, fluid replacement vs restriction |
| 2026-05-26 | paper-casey-myelopathy | 1-4 | 0 | Scanned PDF — no extractable text |
| 2026-05-26 | paper-nascis3 | 1-8 | 7 cards + 1 SBA | spinal-trauma: MP 24h vs 48h, timing, now abandoned |
| 2026-05-26 | paper-isuia | 1-14 | 8 cards | vascular-aneurysm: rupture risk by size/location, surgical risk |
| 2026-05-27 | paper-patchell | 1-6 | 13 cards + 3 SBAs | neuro-onco-spinal: surgery+RT > RT alone for MESCC |
| 2026-05-27 | paper-stupp | 1-10 | 12 cards + 3 SBAs | neuro-onco-cranial: Stupp protocol, TMZ dosing, MGMT, toxicity |
| 2026-05-27 | paper-sport | 1-11 | 9 cards + 1 SBA | degenerative-spine: discectomy vs non-op, crossover, as-treated results |
| 2026-05-27 | paper-berger | 1-8 | 8 cards | neuro-onco-cranial: EOR in LGG, ≥90% threshold, volumetric FLAIR |
| 2026-05-27 | paper-isat | 1-15 | 6 cards | vascular-aneurysm: coiling vs clipping, 7.4% ARR, 5yr mortality, rebleed |
| 2026-05-28 | paper-santarius | 1-7 | 5 cards | head-injury/neuro-icu: CSDH drain vs no drain, 9.3% vs 24% recurrence |
| 2026-06-10 | paper-smith-abscess | 1-6 | 13 cards + 1 SBA | neuro-icu: burrhole=craniotomy, delay worsens outcome, Strep milleri, LP contraindicated |
| 2026-06-10 | paper-hashimoto-desh | 1-11 | 10 cards + 1 SBA | hydrocephalus: DESH definition, SINPHONI outcomes (69%/80%), Evans' index, DESH vs atrophy |
| 2026-06-10 | paper-kulkarni | 1-6 | 7 cards + 1 SBA | hydrocephalus: ETVSS scoring table, strata outcomes, front-load vs back-load concept |

### Infrastructure changes (2026-06-10)

**`src_id` provenance system added:**
- Added `src_id:"<source-id>"` field to card format — links each card to its toggleable source entry
- Migration script patched 279 existing mined cards retroactively using `ref:` field as a source fingerprint
- 135 seed cards intentionally left without `src_id` (no verified source to point to — see note above)
- Added 4 new source entries to content.js SOURCES array: `k-santarius-2009`, `k-smith-2009`, `k-hashimoto-2010`, `k-kulkarni-2010`
- `index.html`: `filteredCards()` and `filteredQs()` now respect source enabled/disabled state — toggling off a source in the Sources tab hides its cards in Learn and Quiz
- `mine.py`: added `CONTENT_SOURCE_MAP` dict (mine.py IDs → content.js IDs); `extract` command now prints `src_id` tag in mining instructions; unmapped sources print a warning
- Backward compatible: cards without `src_id` always show (old behaviour preserved)
