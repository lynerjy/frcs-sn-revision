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

### The 284 claude-ai tagged SBAs — mandatory verification during mining

A prior session violated this rule and generated 284 SBAs from AI training knowledge. These are tagged `src_id:"claude-ai"` and shown with a warning on the live site.

**Every mining session must include a verification step:**

After mining a source, before marking it done:
1. Run: `grep 'src_id:"claude-ai"' content.js | grep -i "<topic keyword>"` to find claude-ai SBAs in that topic area
2. For each one found: check whether the source just mined covers that content
3. If yes: rewrite the SBA from the source text, replace `src_id:"claude-ai"` with the real `src_id`, and update `ref:` to include a real page number
4. If the source doesn't cover it: leave it tagged claude-ai for now — do not verify from memory

The goal is zero claude-ai SBAs by the time all textbooks are mined. Track progress by running:
```bash
grep -c 'src_id:"claude-ai"' content.js
```

---

## MANDATORY: End-of-session log update

**Every session that touches this project must end with an entry in `project_log.md`.**

This is not optional. Before finishing any session:
1. Append a new dated entry to `~/frcs-sn-revision/project_log.md`
2. Include: what was built or mined, key decisions, card/SBA counts changed, open questions, what's next
3. If UI features were added: describe them specifically enough that a future session can recall them without reading the code (e.g. "NR badge in topic list sidebar, derived from RECALL_COUNTS, sorted descending")

The project log is the source of truth for project state between sessions. The memory files in ~/.claude supplement it but cannot replace it. A session without a log entry is incomplete.
