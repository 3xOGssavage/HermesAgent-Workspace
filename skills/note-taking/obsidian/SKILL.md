---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Notes, Markdown, Vault]
    related_skills: []
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `${HERMES_HOME:-~/.hermes}/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content. Only links actually written in note bodies create graph edges and backlinks — links rendered by Dataview/Bases queries are painted on screen, never written, so a MOC built from a query leaves the graph forever incomplete; serialize query output to real Markdown when the map must show in the graph.

## View-copy discipline (live vault stays pristine)

Open a view-copy in the Obsidian app, never the live vault: the app writes `.obsidian/` state files on open, and a live-vault open pollutes history that agents verify by hash. After the owner confirms the copy opens, prove the live vault clean (git status shows nothing but expected untracked) before reporting done — because the owner cannot see contamination, only the agent's check can.

## Sparse graph reading

A graph that renders as one small hub plus a ring of unlinked dots is a correct render of a link-poor vault, not a broken view — count wikilinks plus tags before touching display settings, because no force layout fixes missing links. Fix with content (hub MOC notes, 2+ outbound links per page, tag groups for color), and prefer the local graph at depth 1-2 for real work over the global hairball.

## Copy-only densification (view-copy link pass)

Announce lane first: copy or scratch side only, live vault untouched. Never append links directly in the live vault from this house.
Add 2 to 3 genuine wikilinks per note as an idempotent Related footer: if all planned links already present, skip the file, else append one Related line once. Recount with a regex scan after the pass and prove live clean with git status before reporting, because the owner cannot see contamination, only the count can.
Wire the periphery second: diary dates link to diary index plus summary; seed notes link to index plus schema; shared specs link to their arc plus index; root log plus summary plus old schema versions link to index plus schema. Leave the live schema file alone when it already links out.
Handle attachments plus twins plus tags in the copy only: link yellow data files from a relevant note instead of hiding them; fix a dark unresolved link with a pipe alias to the real dotted filename and leave live diary text append-only; disambiguate duplicate basenames with pipe aliases; isolate an accidental channel-name tag to code-span so it stops coloring the graph. Keep a clean view with attachments plus tags hidden and an audit view with them shown.
Verify markdown-only: count [[wikilinks]] in *.md files only, because a broad file scan also counts app-state json plus csv plus txt as zero-link hits and manufactures a false orphan gap. Report both counts when another agent audits with a broad scan.

## Enrichment preservation across refreshes

The view copy holds TWO content sources: vault master plus copy-side enrichment (wired wikilinks, aliases, tag fixes). A blind full-directory mirror destroys the second — one recopy wiped 112 copy-side links down to 6. So refresh is incremental only: recopy just files whose vault hash changed since the last refresh (manifest-tracked), FLAG every refreshed file so enrichment can be re-wired, and never delete owner notes from the copy. Re-run the link wiring after every refresh, then recount from a fresh regex scan and report counts from the scan, not memory — because a wipe is silent until the count exposes it.

## Vault-ward promotion (copy enrichment into live vault)

Freeze the input first: copy link map at a date plus vault HEAD — because promotion replays exact lines, and drift between map and HEAD silently misplaces them.
Stage the exact edit table while still in the read-only seat (one row per page with its verbatim line) so the build seat executes by transcription with per-step verification — because re-deriving lines at build time reintroduces the drift the freeze just removed.
Promote notebook pages only, in small batches with hub core first and arcs after: append the copy's Related lines verbatim and touch nothing else — because byte-identical replay turns the audit into a diff check instead of a judgment call.
Keep diary copy-only forever: history is append-only, so diary links live in the view permanently and never enter the vault.
Accept every batch against a fixed bar: lines byte-identical to copy, every target resolves in-vault, orphan count drops with zero new flags, diff shows appended lines only, reviewer audits, owner commit word before the next batch — because a vault write without a bar is how enrichment becomes corruption.
