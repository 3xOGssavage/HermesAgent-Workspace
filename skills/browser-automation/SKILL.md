---
name: browser-automation
description: Drive web apps via browser_exec code blocks.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [browser, automation, web, harness]
    related_skills: [dogfood, computer-use]
---

# Browser Automation (code-driven harness)

## When to Use

- Operating a real web app (clicking, typing, reading state, exporting
  files) through `browser_exec` code blocks.
- Canvas-heavy apps where DOM snapshots show almost nothing.

## Procedure

1. Open a named session and navigate; keep one session per tab.
   Never reuse a tab that went blank or stopped responding — start a
   new session name instead of reviving the dead one.
2. Map before acting, all via the accessibility tree plus CDP box
   models: list nodes with their backend IDs, resolve coordinates
   only for elements you will click. Prefer acting on the DOM
   itself over acting on coordinates (step 3).
3. Act in this preference order: real DOM `.click()` found by exact
   button text, keyboard shortcuts dispatched on `document`, form
   fills via resolved-node `Runtime.callFunctionOn` with
   input/change/Enter events plus blur. Coordinate clicks are the
   last resort — they miss when dialogs animate or recenter.
4. Read state back through `js()` after every action (input values,
   body-text markers like dialog titles or progress words). A call
   that returns nothing proved nothing — re-read until the state
   string confirms the effect.
5. Use screenshots only at checkpoints, then release them: each
   shot is verified through `vision_analyze` and never re-read.
   For downloads, hunt the workspace, the harness tmp dir, and the
   OS download folder — the save location is never announced.

## Pitfalls

- `js()` returns values only through `print` — a bare expression
  evaluates but yields empty output, which looks identical to a dead
  page. Always wrap reads in `print`.
- Keep every `js()` call under ~5s of runtime — the evaluate call
  times out fast, so poll with repeated short calls (each round trip
  adds its own delay) instead of one long wait.
- Coordinate clicks silently miss moving targets: a click that
  returns success but changes no state hit the wrong spot or a
  disabled control. Re-derive coordinates or switch to a DOM click.
- Screenshots can wedge the harness daemon on GPU-heavy canvas
  pages (calls start timing out one by one). Recover by abandoning
  the session for a fresh name; do not stack more calls onto the
  wedged one, and keep killing stray browser processes between
  attempts or they accumulate.
- Numeric field edits need the full event sequence (focus, select,
  insert, input, change, Enter, blur) — setting `.value` alone
  leaves the app model stale while the box looks edited.
- Selection state is fragile in canvas editors: panel context follows
  canvas selection, layer-row clicks do not change it, and any stray
  canvas click can drop it to a joint or the scene. Verify which
  object the panel shows before typing into its fields.
- Headless software rendering may never finish heavy effect
  pipelines (a perpetual "preparing" state with an enabled but
  inert export button). That is an environment ceiling, not a
  misclick — stop clicking and change the venue (headed browser,
  desktop build, or a human hand) instead of retrying the button.
- Coordinate space (cua-driver desktop control, Nov 2026): the click `coordinate` is consumed in screenshot pixels in practice — the driver scales to native itself. Passing native bounds double-scales and misses. Verify the effect after every input regardless.
- Element indices expire on any state-changing capture: re-capture som immediately before element clicks/sets, and never reuse ids across a vision capture.
- `set_value` drives Spinner/ValuePattern controls (percent fields, angles) reliably where background typing fails. For OS save dialogs prefer accepting the default name and moving the file afterwards over fighting the path field.
- Keyboard shortcuts dispatched on the document (e.g. Ctrl+Shift+E for Export) open dialogs when coordinate clicks miss animated targets. DOM `.click()` by exact button text beats coordinates for dialog buttons.
