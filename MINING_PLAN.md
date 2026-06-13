# FRCS (SN) — Comprehensive Mining Plan

**Scope:** Everything in the "Sista & Me / FRCS Exam / Books for FRCS" folder + Recall Bank docx files.
**Total:** 71 sources, ~9,672 pages (PDF) + docx/pptx files.
**Method:** Systematic by folder, 20 pages per chunk. All cards tagged `korky:true`.
**Ignoring:** `frcsimptopicsandquestions_docx.zip` (zip of existing docx), `.DS_Store`, `Neurological Death Testing Video Tutorial.txt` (URL only).

---

## How to resume each session

```
cd ~/frcs-sn-revision
python3 mine.py next     # shows progress + next 3 sources to mine
```

Or just tell Claude: "let's mine" — Claude reads this plan, checks mining_manifest.json, and picks up where we left off.

---

## Mining order (by folder)

### Folder 1: Recall Bank — docx files (2 sources)

The two recall bank PDFs have already been parsed into the Recall Bank tab (315 questions). These are the remaining docx files.

| # | Source ID | Format | Description |
|---|-----------|--------|-------------|
| 1 | recall-imp-topics | docx | Important Topics & Questions |
| 2 | recall-post-exam-notes | docx | Post-Exam Notes |

### Folder 2: Key Papers for FRCS (25 sources, ~219pp)

All 25 papers in the Key Papers subfolder. Each small enough to mine in one chunk.

| # | Source ID | Pages | Topic(s) |
|---|-----------|-------|----------|
| 3 | paper-sivakumar-hyponatraemia | 9pp | neuro-icu |
| 4 | paper-casey-myelopathy | 4pp | degenerative-spine |
| 5 | paper-nascis3 | 8pp | spinal-trauma |
| 6 | paper-isuia | 14pp | vascular-aneurysm |
| 7 | paper-patchell | 6pp | neuro-onco-spinal |
| 8 | paper-stupp | 10pp | neuro-onco-cranial |
| 9 | paper-sport | 11pp | degenerative-spine |
| 10 | paper-berger | 8pp | neuro-onco-cranial |
| 11 | paper-isat | 15pp | vascular-aneurysm |
| 12 | paper-santarius | 7pp | head-injury |
| 13 | paper-smith-abscess | 6pp | neuro-onco-cranial, neuro-icu |
| 14 | paper-hashimoto-desh | 11pp | hydrocephalus |
| 15 | paper-kulkarni | 6pp | hydrocephalus, paeds |
| 16 | paper-anand-mvd | 8pp | functional |
| 17 | paper-decra | 10pp | head-injury |
| 18 | paper-kumpe-iih-stents | 11pp | hydrocephalus |
| 19 | paper-chesnut | 12pp | head-injury, neuro-icu |
| 20 | paper-mautner-nf2 | 5pp | paeds, peripheral-nerve |
| 21 | paper-couture-helmet | 6pp | paeds |
| 22 | paper-delwel-nph | 6pp | hydrocephalus |
| 23 | paper-hu-epilepsy | 9pp | epilepsy-surgery |
| 24 | paper-jahangiri-redo-tss | 8pp | pituitary |
| 25 | paper-destiny2 | 10pp | vascular-ich |
| 26 | paper-liu-dbs | 10pp | functional |
| 27 | paper-aruba | 9pp | vascular-avm |

### Folder 3: Books for FRCS Pt.1 — top-level files (15 sources, ~9,029pp)

Everything at the top level of the Books for FRCS Pt.1 folder (excluding the Key Papers subfolder). Ordered smallest first.

| # | Source ID | Pages | Format |
|---|-----------|-------|--------|
| 28 | bank-neurosurgery-mcqs | 5pp | PDF |
| 29 | bank-neuro-surgery | 14pp | PDF |
| 30 | emergency-head-injury | 14pp | PDF |
| 31 | infographic-2025 | 70pp | PDF |
| 32 | nader-cases | ? | docx |
| 33 | alleyne-board-review | 434pp | PDF |
| 34 | alleyne-self-assessment | 429pp | PDF |
| 35 | birinyi-board-prep | 450pp | PDF |
| 36 | shaya-practice-questions | 256pp | PDF |
| 37 | damirez-operative-anatomy | 226pp | PDF |
| 38 | spine-surgery-2019 | 675pp | PDF |
| 39 | harbaugh-knowledge-update | 985pp | PDF |
| 40 | oxford-neurological-surgery | 1,098pp | PDF |
| 41 | schmidek-sweet | 2,391pp | PDF |
| 42 | greenberg | 1,982pp | PDF |

### Folder 4: Part 2 Prep - Aberdeen Course Material (29 sources, ~424pp + pptx)

Everything in the Aberdeen folder. PDFs and docx first, then PowerPoints.

| # | Source ID | Pages | Format |
|---|-----------|-------|--------|
| 43 | aberdeen-cerebral-physiology | 6pp | PDF |
| 44 | aberdeen-cbf-graphs | 3pp | PDF |
| 45 | aberdeen-rescueicp | 11pp | PDF |
| 46 | aberdeen-aeds | 7pp | PDF |
| 47 | aberdeen-ica-anatomy | 16pp | PDF |
| 48 | aberdeen-tcd | 7pp | PDF |
| 49 | aberdeen-neuro-death | 7pp | PDF |
| 50 | aberdeen-la-toxicity | 2pp | PDF |
| 51 | aberdeen-language | 12pp | PDF |
| 52 | aberdeen-visual-fields | 14pp | PDF |
| 53 | aberdeen-visual-fields-goldman | 10pp | PDF |
| 54 | aberdeen-visual-fields-humphrey | 7pp | PDF |
| 55 | aberdeen-who-brain-tumour | 18pp | PDF |
| 56 | aberdeen-ulnar-c8t1 | 5pp | PDF |
| 57 | aberdeen-carpal-tunnel | 27pp | PDF |
| 58 | aberdeen-ncs | 73pp | PDF |
| 59 | aberdeen-eye-exam | 31pp | PDF |
| 60 | aberdeen-exam-tips | 11pp | PDF |
| 61 | aberdeen-tjones-revision | 79pp | PDF |
| 62 | aberdeen-tjones-exam | 39pp | PDF |
| 63 | aberdeen-tjones-exam-orig | 39pp | PDF |
| 64 | aberdeen-viva-q-jim | ? | docx |
| 65 | aberdeen-brainstem | ? | pptx |
| 66 | aberdeen-frcs-sn-exam | ? | pptx |
| 67 | aberdeen-frcs-clinicals | ? | pptx |
| 68 | aberdeen-frcs-close | ? | pptx |
| 69 | aberdeen-frcs-exam | ? | pptx |
| 70 | aberdeen-mri | ? | pptx |
| 71 | aberdeen-radiology | ? | ppt |

---

## Chunk protocol

For each chunk:

1. **Extract:** `python3 mine.py extract <source-id> <start>-<end>`
2. **Read:** Claude reads the extracted text carefully
3. **Create cards:** Write flashcards + SBAs with:
   - Exact `ref` (source name + page number)
   - `korky:true` on every card
   - Assigned to the correct topic in the LEARN block
4. **Validate:** `python3 mine.py validate`
5. **Mark done:** `python3 mine.py done <source-id> <start>-<end> <N>`

### Skippable content

Mark as done with 0 cards:
- Table of contents, index, preface, acknowledgements
- Reference lists, bibliographies
- Copyright pages, blank pages
- Content that duplicates cards already created from a higher-priority source

---

## Progress tracking

Progress is tracked in:
1. **mining_manifest.json** — machine-readable, updated by `mine.py done`
2. **`python3 mine.py next`** — shows overall % and next sources
3. **`python3 mine.py status`** — full source-by-source view
