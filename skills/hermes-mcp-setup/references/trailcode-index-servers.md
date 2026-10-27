# TrailCode index servers (per-repo code maps)

One server covers one repo graph. Point the launcher at the project folder that holds the graph, never at a parent root that has none.

## Build (scoped, no key, free)

- `graft build --only-dir skills --only-dir memories ...` indexes just the named subfolders and persists the scope for later rebuilds; junk folders (caches, logs, sessions, tool copies, secrets) stay out on purpose.
- Keep the exact structural tier; skip `--deep` when precision matters — machine-extracted facts with file:line spans are verifiable, model-written summaries can hallucinate.
- Freshness: `graft check` must say the wiring graph is in sync; `graft_check_freshness` says the same at runtime. Rebuild when the folder changes a lot.

## Wire

- Launcher `.cmd` cds into the graph folder, then calls a pinned global binary (`graft.cmd mcp "<dir>"`) — never a floating `npx -y pkg`, which can resolve a newer release under the spawn env than in your terminal.
- Pin the last release that lists tools eagerly (0.15.0 at time of writing): newer releases serve deferred/empty tool lists this client reads as zero tools. Prove a version with a raw tools/list handshake before adopting it.
- Older releases do not fold nested git repos into one root graph (each child keeps its own graph) — wire one server per project folder instead of chasing a single whole-house graph.
- Declare done only after a real find/query call returns hits with file paths; a connected server with a tool count and an empty or missing graph answers everything with zero hits.