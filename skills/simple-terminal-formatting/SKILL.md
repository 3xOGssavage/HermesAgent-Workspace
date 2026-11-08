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

Soham is a partial coder. Use simple words. Translate every technical term into plain words on first use — never assume he knows tooling, formats, or jargon. Plain terminal does NOT render markdown: asterisks, hashes, and fences print literally, so never use them for structure.

## When to Use

Every reply to Soham. Any summary, comparison, inventory, or status. Load before long answers so boxes stay lined up.

## Always-on rules

- Owner is on PC with a wide terminal: use the full width (wide tables, long lines). Never squeeze output into a narrow left column; the old 60-char wrap no longer applies.
- Auto-pick the shape without being asked: stories, explanations, and how-tos stay as short structured sections; results, lists, comparisons, inventories, and statuses get a wide table ONLY when the data truly needs comparison or alignment. Never wait to be told to use a table, and never force a table where sections scan better.
- Default to short structured sections with blank lines between parts, not one long wall of text.
- Use tables ONLY when the data truly needs a table. Otherwise use short labeled sections.
- When past format directives conflict, the newest explicit instruction wins until superseded — merge to one rule instead of stacking both.
- When a table ships misaligned, rebuild it with script-checked widths and shorter cells, ideally split into small topic boxes — never resend a hand-aligned fix. When the script builds border lines, derive the joint positions from the header row's pipe columns and re-stamp every border from those joints — a bar drawn at a fixed width drifts off the content columns.
- Never retype a script-verified table into chat; paste the checked file content verbatim — retyping reintroduces the misalignment the script just removed.
- For 100+ item listings (pending queues, full inventories), never dump every row: show a grouped count table plus conflicts, duplicates, stale items, and a suggested batch order; full rows only on request. See references/large-list-reviews.md.
- When the owner explicitly says tabular format with serial numbers, build numbered ASCII tables with an Sl No column even if wide — split into 2-4 boxes by range, keep cells to short phrases. An explicit user directive overrides table minimalism.
- When the owner says short and simple, compress to one takeaway plus labeled lines, no boxes unless asked.
- When the owner rejects a process label (says they do not want to know what X means), drop that label for good: never re-introduce it, never explain it again, translate to outcome language (what is done, what needs you) — because re-explaining a rejected label reads as ignoring a direct order.
- When the owner vetoes a whole topic (says they do not know and do not want to know about X), drop the topic entirely until they ask: never list it in next steps, never offer it as a choice, never count it in progress — because every re-mention forces a fresh rejection and stalls the goal.
- When the owner repeats "so what now" without picking a next step, answer with one next action only plus one-line safe state — never the full board, never re-offer vetoed topics — because a wall of options stalls a non-coder while one tap moves.
- Keep rows tight but use the full width; split only when a table exceeds readable width, not by default.
- Pad the left column so every pipe lines up vertically in monospace.
- ASCII only for boxes: plus, dash, pipe, equals. Never Unicode box drawing, it misaligns on some fonts.
- Semantic color is extra, structure is the base: purple for labels, green for pass and code, orange for actions and why it matters, white for story. Logs and files strip color, so the text must read fine without it.
- One idea per line. Wide lines are fine on PC; blank line before and after every box.
- Match reply length to the weight of the ask: a one-line question gets a one-line answer, finished work gets a short report of what changed, what is verified, and what is left, never a replay of the whole process. No filler openers, no restating the request, no re-summarizing what was already said.
- Write paths the way the owner reads them: native form with forward slashes (F:/CD/Projects), never spelled-out letter by letter and never backslash-escaped, because the spelled form is unreadable to a non-coder.

## Procedure

1. Results, lists, comparisons, inventories, statuses: build a wide ASCII table at full terminal width with header Item and Detail (plus Sl No column when the owner asks for numbered rows). Stories and how-tos: use labeled lines with two-space indent.
2. Shorten every cell first: cut filler, keep paths and versions exact.
3. Pad topic column to equal width, then pipes, then plus-dash borders with equals row under header.
4. Verify widths by script before sending: assert every line of the box has identical length; a box that looks aligned in your head still ships broken when one cell overflows. Never hand-align and send. State the coverage reconciliation alongside the table (N on disk, N listed, zero missing, zero phantom) so the owner can trust the list is complete without recounting.
5. Action tables always ship with a matching copy-paste command block in the same order: the table carries ID, DO, plain-words WHAT, and plain-words WHY; the block below carries the exact slash command per row, top to bottom, so the owner clicks without translating the table into commands.
6. Add a one-line takeaway above or below: Verdict, Result, Next move.
- When a decision is needed, ask it as an MCQ: each question with 2-4 labeled choices, recommended option first, never a bare open question. The owner decides fastest by picking, not by composing. Tool constraint: clarify choices are plain strings, one per choice — structured choice objects are rejected, so keep labels short and put detail in the question text. If the owner skips the card twice without picking, fall back to plain-text numbered picks in chat ("reply like 1 3, or all, or none") and continue — because a third identical card stalls a non-coder while one line of numbers moves.

## Pitfalls

- Never emit markdown bold, headings, or fences in chat; they print as literal characters and hurt scanning.
- Never build one narrow table that wastes the wide screen; use the full width the owner gave you.
- Never use Unicode borders for alignment; fallback fonts break the columns.
- Never rely on color alone; piped output loses it, so labels and ticks must carry meaning.
- Never re-present a listing from chat memory or a screenshot-transcribed ID; re-run the live query first so IDs and state are current, because one misread char breaks resume/rename and stale copies miss new rows. This covers your own environment too: run pwd before claiming which directory you are in, because the session-start snapshot goes stale and asserting the wrong folder destroys trust.
- When the owner says they did not understand, lead with the plain-words re-explanation first and ask second: never answer confusion with the same jargon restated as choices, because picking between unclear options is guessing, not deciding.
- When the owner says a summary is not enough info on what a pending item is, read the full verbatim content from disk and give it word for word before any recommendation — because a shortened WHY hides the exact words the owner must judge, and only the full text lets a non-coder decide.
- Never answer confusion with internal machinery (queue counts, batch names, click totals, color words): lead with outcome only (what is done, what is safe, what needs one tap) and keep the machinery in the table below — because a non-coder cannot verify machinery, only outcomes.
- Default table width caps near 120 chars so rows never wrap on narrower windows; when the owner explicitly demands full width, generate at that width programmatically and verify every line identical — the owner's wide screen is the target, not the cap.
