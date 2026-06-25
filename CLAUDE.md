# FRCS (SN) Revision Tool — Claude Instructions

## CARDINAL RULE — NO EXCEPTIONS

**Never write a flashcard or SBA question from memory or training knowledge.**

Every single card and SBA must be written by reading the source text first via `python3 mine.py extract <id>`. If you have not read the source, you cannot write the card. Period.

This is not a style preference. This is a patient safety rule. Carolyn is preparing for a surgical exam. Wrong content could propagate into clinical practice. Lives are at stake.

### What this means in practice:

- If asked to write content for a topic and no source has been extracted: **stop and say so**. Do not write the card. Ask which source to extract first.
- `ref:"claude"` or `ref:"Standard"` or any ref that does not cite a specific document, section, and page number is a violation of this rule.
- Do not use phrases like "standard teaching", "well established", or "clinical practice" as substitutes for a real reference.
- If you are unsure whether something is in the source: **quote the source text directly** in your working before writing the card.

### The only acceptable ref formats:

```javascript
ref:"NG228 1.1.3, p4"          // guideline: section + page
ref:"Greenberg 10e, p142"      // textbook: edition + page
ref:"ISAT, Molyneux 2009, p3"  // paper: author + year + page
ref:"cerebral-physiology.pdf p6" // Aberdeen PDF: filename + page
```

No page number = not acceptable. No source = not acceptable.

### claude-ai SBAs — keep, don't replace

Policy changed: do NOT rewrite or replace claude-ai SBAs when mining a real source. Keep them. Only correct a claude-ai SBA if the source you just read clearly contradicts it. They are displayed with an amber ⚠ AI warning in the app and can be toggled off in Sources.

---

## Greenberg mining — recall-bank chapter priority (MANDATORY)

Greenberg must be mined by **recall-bank frequency**, not by whatever claude-ai SBAs happen to exist.

**CARDINAL RULE — TOP-N BATCH CYCLING (N=10, updated 2026-06-25):**

Mine textbooks in this exact sequence:
1. For each textbook (Greenberg → TJones → Infographic → Alleyne/Citow → Birinyi/Harbaugh), scan the **top 10 recall topics** in order.
2. For each topic: if it has **zero** content from this textbook → mine it. If it has **any** content → skip.
3. Complete the full top-10 pass for ALL textbooks before expanding to topics 11–20.

**Top 10 topics by recall count (RECALL array only — matches quiz site NR badges):**
1. neuro-onco-cranial (62R) — all textbooks done ✓
2. degenerative-spine (52R) — all textbooks done ✓
3. paeds (46R) — all textbooks done ✓
4. cranial-anatomy (42R) — all textbooks done ✓ (absent from Infographic; foramen magnum clockwise from Alleyne)
5. ethics (36R) — absent from ALL textbooks; needs separate source (GMC/BMA guidelines or TJones)
6. functional (30R) — all textbooks done ✓
7. vascular-aneurysm (26R) — all textbooks done ✓
8. hydrocephalus (24R) — all textbooks done ✓
9. neuro-icu (22R) — all textbooks done ✓
10. head-injury (19R) — all textbooks done ✓

**CURRENT NEXT TARGET: Birinyi / Harbaugh — apply top-10 scan. Then expand to topics 11–20.**

**Textbook top-10 pass status (updated 2026-06-25):**
- Greenberg 10e: COMPLETE (ethics absent from Greenberg)
- TJones (Aberdeen): FULLY MINED (all 79pp done)
- Infographic Guide 2025: COMPLETE (ethics + cranial-anatomy + head-injury absent)
- Alleyne & Citow 3e: COMPLETE (ethics absent; 11 SBAs added)
- Birinyi / Harbaugh: **NEXT** — 0 SBAs currently

**What went wrong (sessions 5 and 34):** Continuing to mine gaps in topics that already have textbook coverage (e.g. more neuro-onco Greenberg when neuro-onco already has 62 SBAs matching 87 recalls). The fix: always run this checklist before mining.

---

## content.js structure — where to insert new SBAs (MANDATORY)

Each topic block has TWO separate arrays:
```
"topic-id":{src:"...", c:[
  {q:"...", a:"..."},        ← flashcards go here (c:[])
  ...
],q:[
  {stem:"...", opts:[...]},  ← SBAs go here (q:[])
  ...
]},
```

**Rule: new SBAs must go inside the `q:[]` array of the CORRECT topic block.**

Common failure modes (both have occurred):
1. Inserting into the wrong block entirely (spinal-anatomy instead of functional)
2. Inserting into `c:[]` instead of `q:[]` within the right block

**Always run `python3 mine.py validate` before committing.** A pre-commit hook does this automatically, but running it manually after insertion confirms the mismatch count has not increased. The baseline is 527 (pre-existing TJones cross-block SBAs — a separate remediation task).

If the mismatch count increases, find the misplaced SBAs (look for `topic:"X"` inside the wrong block's `q:[]`), remove them, and reinsert inside the correct block's `q:[]` before the closing `]},`.

---

## MANDATORY: End-of-session log update

**Every session that touches this project must end with an entry in `project_log.md`.**

This is not optional. Before finishing any session:
1. Append a new dated entry to `~/frcs-sn-revision/project_log.md`
2. Include: what was built or mined, key decisions, card/SBA counts changed, open questions, what's next
3. If UI features were added: describe them specifically enough that a future session can recall them without reading the code (e.g. "NR badge in topic list sidebar, derived from RECALL_COUNTS, sorted descending")

The project log is the source of truth for project state between sessions. The memory files in ~/.claude supplement it but cannot replace it. A session without a log entry is incomplete.
