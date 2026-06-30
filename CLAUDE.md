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

### Q&A book mining — variation, not verbatim

When the source is a Q&A / MCQ board review book (Alleyne/Citow, Shaya, Birinyi, Harbaugh, etc.), do **not** copy questions verbatim. Instead:

1. Extract the source text (`mine.py extract <id> <pages>`) to read the questions, answer keys, and explanations.
2. Identify the underlying fact being tested.
3. Rewrite as a **new FRCS-style 5-option clinical scenario SBA** that tests the same knowledge.
   - The stem should be a clinical presentation or scenario (not a direct definition question).
   - Distractors should be plausible, not trivially wrong.
   - The explanation must be grounded in the extracted source text — quote it in your working before writing.
4. The `ref` must cite the source book and page number as extracted.

**Why variations:** (a) the source books are US board review format — different style from FRCS SN; (b) seeing the same fact in a different framing is better exam prep; (c) copyright.

The factual content (correct answer, explanation) must still be traceable to the extracted source page — no invention allowed.

---

### claude-ai SBAs — keep, don't replace

Policy changed: do NOT rewrite or replace claude-ai SBAs when mining a real source. Keep them. Only correct a claude-ai SBA if the source you just read clearly contradicts it. They are displayed with an amber ⚠ AI warning in the app and can be toggled off in Sources.

---

## Greenberg mining — recall-bank chapter priority (MANDATORY)

Greenberg must be mined by **recall-bank frequency**, not by whatever claude-ai SBAs happen to exist.

**CARDINAL RULE — TOP-N BATCH CYCLING (N=10, threshold updated 2026-06-30):**

**THRESHOLD = 10 SBAs per topic per textbook source.** A topic is "done" for a given textbook once it has ≥10 SBAs from that source. Do NOT declare done at 1 — this was the prior (wrong) rule.

Mine textbooks in this exact sequence:
1. For each textbook (Greenberg → TJones → Infographic → Alleyne/Citow → Shaya → Birinyi → Harbaugh), scan the **top 10 recall topics** in order.
2. For each topic: if it has **≥10** SBAs from this textbook → skip. If it has **<10** → mine it (target ≥10).
3. Complete the full top-10 pass for ALL textbooks before expanding to topics 11–20.
4. Exception: if a textbook genuinely has no content for a topic, record it as "exempt" (not blocking) — but verify before declaring exempt.

**Top 10 topics by recall count (RECALL array only — matches quiz site NR badges):**
1. neuro-onco-cranial (62R)
2. degenerative-spine (52R)
3. paeds (46R)
4. cranial-anatomy (42R)
5. ethics (36R)
6. functional (30R)
7. vascular-aneurysm (26R)
8. hydrocephalus (24R)
9. neuro-icu (22R)
10. head-injury (19R)

**Coverage matrix — run `python3 mine.py coverage` for the live version. Do NOT maintain a manual copy here; it will go stale.**

As of 2026-06-30 (run `mine.py coverage` to get current numbers):
- Greenberg: 9/10 done (only ethics missing)
- Infographic: 7/10 done (cranial-anatomy, ethics, head-injury gaps)
- TJones: 0/10 done at threshold — most SBAs misplaced in `spinal-anatomy` block (remediation needed)
- Alleyne: 1/10 done (only cranial-anatomy ≥8)
- Shaya/Birinyi/Harbaugh: all gaps

**What went wrong (sessions 5, 34, and the "1-per-topic" Shaya/Birinyi passes):** The prior skip rule was "skip if ≥1 entry" — far too shallow. The fix: threshold is now ≥8 per topic per source.

### MANDATORY: Before every mining session

```
python3 mine.py coverage
```

This is the **only** canonical source of truth. It counts SBAs by **physical block position** — the same way the website counts them. Never use grep or tag-based counting; those give wrong numbers because (a) many old SBAs lack a `topic:` tag, and (b) misplaced SBAs inflate the wrong topic counts.

After inserting new SBAs, re-run `python3 mine.py coverage` to confirm the counts moved correctly.

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
