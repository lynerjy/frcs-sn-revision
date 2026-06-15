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

**What went wrong in session 5 (2026-06-12):** All 11 Greenberg sessions were driven by "which page verifies this claude-ai SBA" rather than "which topic has the most recalls." Paediatric neurosurgery (46 recalls — 3rd highest) was never touched. This must not happen again.

**Rule for every Greenberg mining session:**
1. Run `python3 mine.py stats` and check which topics are thinnest relative to their recall count.
2. Look up the corresponding Greenberg 10e chapter for that topic (use the index or table of contents).
3. Mine that chapter. Do not mine a different chapter because it happens to relate to an existing claude-ai SBA.
4. Record the pages and card count with `python3 mine.py done greenberg <pages> <N>`.

**Priority order for remaining Greenberg chapters (by recall count):**
1. Paediatric neurosurgery (46 recalls) — craniosynostosis ~pp1140s, NTDs ~pp200s, paeds tumours ~pp750s
2. Neuro-oncology cranial (62 recalls) — already partially covered; check thin sub-topics
3. Degenerative spine (52 recalls) — partially covered pp659-680; check what remains
4. Vascular aneurysm (26 recalls) — check PHASES, unruptured management chapters
5. Carotid (thin topic, 2 SBAs) — carotid endarterectomy chapter

---

## MANDATORY: End-of-session log update

**Every session that touches this project must end with an entry in `project_log.md`.**

This is not optional. Before finishing any session:
1. Append a new dated entry to `~/frcs-sn-revision/project_log.md`
2. Include: what was built or mined, key decisions, card/SBA counts changed, open questions, what's next
3. If UI features were added: describe them specifically enough that a future session can recall them without reading the code (e.g. "NR badge in topic list sidebar, derived from RECALL_COUNTS, sorted descending")

The project log is the source of truth for project state between sessions. The memory files in ~/.claude supplement it but cannot replace it. A session without a log entry is incomplete.
