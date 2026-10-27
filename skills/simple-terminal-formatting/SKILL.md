---
name: simple-terminal-formatting
description: Use when formatting replies for Soham in plain terminal.
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [formatting, terminal, readability]
---

# Simple Terminal Formatting for Soham

Soham is a partial coder. Use simple words. Plain terminal does NOT render markdown: asterisks, hashes, and fences print literally, so never use them for structure.

## When to Use

Every reply to Soham. Any summary, comparison, inventory, or status. Load before long answers so boxes stay lined up.

## Always-on rules

- Owner is on PC with a wide terminal: use the full width (wide tables, long lines). Never squeeze output into a narrow left column; the old 60-char wrap no longer applies.
- Auto-pick the shape without being asked: results, lists, comparisons, inventories, and statuses go in wide tables; stories, explanations, and how-tos stay as short structured sections. Never wait to be told to use a table.
- Default to short structured sections with blank lines between parts, not one long wall of text.
- Use tables ONLY when the data truly needs a table. Otherwise use short labeled sections.
- When the owner explicitly says tabular format with serial numbers, build numbered ASCII tables with an Sl No column even if wide — split into 2-4 boxes by range, keep cells to short phrases. An explicit user directive overrides table minimalism.
- When the owner says short and simple, compress to one takeaway plus labeled lines, no boxes unless asked.
- Keep rows tight but use the full width; split only when a table exceeds readable width, not by default.
- Pad the left column so every pipe lines up vertically in monospace.
- ASCII only for boxes: plus, dash, pipe, equals. Never Unicode box drawing, it misaligns on some fonts.
- Semantic color is extra, structure is the base: purple for labels, green for pass and code, orange for actions and why it matters, white for story. Logs and files strip color, so the text must read fine without it.
- One idea per line. Wide lines are fine on PC; blank line before and after every box.

## Procedure

1. Results, lists, comparisons, inventories, statuses: build a wide ASCII table at full terminal width with header Item and Detail (plus Sl No column when the owner asks for numbered rows). Stories and how-tos: use labeled lines with two-space indent.
2. Shorten every cell first: cut filler, keep paths and versions exact.
3. Pad topic column to equal width, then pipes, then plus-dash borders with equals row under header.
4. Verify widths by script before sending: assert every line of the box has identical length; a box that looks aligned in your head still ships broken when one cell overflows. Never hand-align and send.
4. Add a one-line takeaway above or below: Verdict, Result, Next move.
5. Ask one clear next question at the end, never three.

## Pitfalls

- Never emit markdown bold, headings, or fences in chat; they print as literal characters and hurt scanning.
- Never build one narrow table that wastes the wide screen; use the full width the owner gave you.
- Never use Unicode borders for alignment; fallback fonts break the columns.
- Never rely on color alone; piped output loses it, so labels and ticks must carry meaning.
- Never re-present a listing the user already corrected from chat memory; re-run the live query first so the corrected output reflects current state, not a stale copy.
- Cap total table width near 120 chars so rows never wrap on narrower windows; wrapping breaks pipes even when lengths match.
