# Carrying opencode Chat Sessions Across a Project Move

Sessions live in `%USERPROFILE%\.local\share\opencode\opencode.db` (SQLite: `project`,
`project_directory`, `session` tables). Moving a folder orphans its sessions: the new path
registers as an empty project while history sits under the old path (upstream issues
anomalyco/opencode#29703, #34737).

## Project-ID resolution order (per opened directory)

1. GitHub/SSH remote URL hash (`Hash("git-remote:github.com/owner/repo")`) — file:/local-path origins skipped.
2. `.git/opencode` pin file content, if present.
3. Git root commit hash.

Pre-existing projects usually carry the remote-hash id; a fresh clone without a pin
cement the root-commit id on first open — with zero sessions.

## The pin method (preferred — no DB surgery)

Before the first opencode open in the new location, write the old project id into the
new clone's `.git/opencode`: exactly 40 ASCII bytes, no BOM, no trailing newline.
Reversible (delete the file to recompute), git-safe (untracked cache file), no push/fetch impact.
Then open in the new home and confirm the old sessions list before the owner nod.
Plain folders (no `.git`) have no pin target: their sessions stay bound to the old path
under the workspace-root project — viewable by opening the old location, never moved by editing rows.

## Proving it with the live DB (read-only copy first, never the live file)

- `SELECT project_id, directory FROM project_directory WHERE directory LIKE '%<name>%'`
- `SELECT project_id, COUNT(*) FROM session WHERE directory LIKE '%<name>%' GROUP BY project_id`
- `SELECT id, worktree FROM project WHERE ...` to see which id each path resolves to.
- Query `project`, `project_directory`, AND `session` — never trust a single table.
- Compare hashes across agents with the algorithm named (SHA-1 and SHA-256 of identical
  files print completely different strings).
