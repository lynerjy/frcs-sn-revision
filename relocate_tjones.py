#!/usr/bin/env python3
"""
Relocate 48 TJones SBAs from wrong blocks to their tagged topic blocks.
Works bottom-to-top so line numbers stay valid during removal.
Then inserts into correct blocks by finding q_end_lines fresh after removal.
"""
import re

def find_q_end(lines, topic_id):
    """Find the line index (0-based) of the ]}, that closes the q:[] of a topic block."""
    in_block = False
    in_q = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(f'"{topic_id}"') and ':{src:' in stripped:
            in_block = True
        if in_block and not in_q and '],q:[' in line:
            in_q = True
            continue
        if in_q and stripped == ']},':
            return i
    raise ValueError(f"Could not find q:[] end for topic '{topic_id}'")

with open('content.js') as f:
    lines = f.readlines()

# ── Step 1: Identify misplaced lines (bottom-to-top order for safe removal) ─
import re as _re

block_pattern = _re.compile(r'"([a-z][a-z-]+)":\{src:"[^"]+",c:\[')
text_lines = [l.rstrip('\n') for l in lines]

learn_start = next((i for i, l in enumerate(text_lines) if _re.match(r'const LEARN\s*=\s*\{', l)), None)
learn_end   = next((i for i, l in enumerate(text_lines) if i > (learn_start or 0) and _re.match(r'^\};', l)), len(text_lines))

current_block = None
misplaced = []  # (0-based line index, physical_block, tagged_topic)
for i, line in enumerate(text_lines):
    if i > learn_end:
        break
    bm = block_pattern.search(line)
    if bm:
        current_block = bm.group(1)
    if current_block:
        tm = _re.search(r'topic:"([a-z][a-z-]+)"', line)
        if tm and tm.group(1) != current_block:
            misplaced.append((i, current_block, tm.group(1)))

print(f"Misplaced SBAs to relocate: {len(misplaced)}")

# ── Step 2: Extract SBA text + remove from file (bottom-to-top) ─────────────
# Group: {tagged_topic: [sba_text, ...]}
to_insert = {}
for idx, physical, tagged in sorted(misplaced, reverse=True):
    sba_line = lines[idx]
    to_insert.setdefault(tagged, []).append(sba_line)
    del lines[idx]

print("Removed from original positions.")
for topic, sbas in to_insert.items():
    print(f"  → {topic}: {len(sbas)} SBAs to insert")

# ── Step 3: Insert into correct blocks ───────────────────────────────────────
# Process topics in sorted order so line-shift from insertions is predictable.
# Actually, we re-find q_end after each batch (expensive but safe).
for topic in sorted(to_insert.keys()):
    sbas = to_insert[topic]
    # Make sure trailing commas are correct: the existing last SBA may need a comma
    # and each inserted SBA except the last needs a comma.
    
    q_end_idx = find_q_end(lines, topic)
    # Check existing last line before q_end — if it ends with } (no comma), add one
    last_sba_idx = q_end_idx - 1
    while last_sba_idx > 0 and not lines[last_sba_idx].strip():
        last_sba_idx -= 1
    last_line = lines[last_sba_idx].rstrip('\n')
    if last_line.rstrip().endswith('}'):
        lines[last_sba_idx] = last_line + ',\n'
        print(f"  Added trailing comma at line {last_sba_idx+1} before inserting into '{topic}'")
    
    # Insert SBAs before q_end_idx (they come in reversed order due to bottom-to-top extraction)
    # Re-reverse to restore original order
    sbas_ordered = list(reversed(sbas))
    for sba in sbas_ordered:
        sba_clean = sba.rstrip('\n').rstrip(',') + ',\n'
        lines.insert(q_end_idx, sba_clean)
        q_end_idx += 1  # shift insertion point for next SBA
    
    # Last inserted SBA: remove trailing comma if q_end is ]},
    # Actually, having a trailing comma before ]}, is fine in JS (trailing comma OK in arrays)
    print(f"  Inserted {len(sbas)} SBAs into '{topic}'")

with open('content.js', 'w') as f:
    f.writelines(lines)

print("\nDone. Run: python3 mine.py validate")
