# Large-list reviews (100+ items: memory pending queues, full inventories)

Dumping every row floods the chat and gets ignored. Group first, then report.

## Procedure

1. Count the queue: list the pending dir and count files before opening any single one.
2. Parse every file programmatically (one script pass over the JSONs: id, target, origin, timestamp, one-line summary) — never open 100 files by hand.
3. Bucket by keyword into topic groups (formatting rules, keys, MCP quirks, schedules, business lines, tool pins). One file may sit in two groups; say so, so counts visibly overlap.
4. Report shape: one grouped count table (Group | What it is about | Count), then Conflicts, then Duplicates-to-merge, then Stale items, then a suggested approve order. Full row text only on request.
5. Flag big patch/remove ops by id for careful review before approval — rewrites and removals are the only items that can destroy saved state.
6. Recommend batches: safe merges first (identity, schedule, proven fixes), tool-specific second, business lines third, big rewrites last.

## Pitfalls

- Approving a 100+ queue one by one wastes the session; always propose merged batches instead.
- A count table whose columns are swapped (counts under the wrong header) destroys trust in the whole review — verify header order before sending.
- Stale items hide inside big queues (e.g. a schedule preference superseded by a newer cron); check timestamps on anything that contradicts current state.
