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

### The 284 claude-ai tagged SBAs

A prior session violated this rule and generated 284 SBAs from AI training knowledge. These are tagged `src_id:"claude-ai"` and shown with a warning on the live site. They must be verified or replaced during textbook mining. Do not add more.
