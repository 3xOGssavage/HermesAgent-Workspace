---
name: n8n-workflows
description: "Use when building n8n workflows via the REST API."
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [n8n, workflows, automation, rest-api]
---

# n8n Workflows via REST API

## When to Use

Use for any n8n task done through the REST API: creating, editing, activating, or debugging workflows, wiring triggers, loops, switches, and AI agent nodes, and verifying runs from execution data.

Build and verify n8n workflows through `X-N8N-API-KEY` calls. Creation accepts anything — activation validates. Always activate, then fire a real trigger and read the execution.

## Procedure

1. Confirm the builder key works: `GET /workflows?limit=1` must return 200. A 401 means a stale/rotated key, never a broken workflow — refresh the key first.
2. Copy exact node shapes from a working workflow on the same instance (`GET /workflows/{id}`), never hand-write versions from memory. Type versions drift between n8n releases.
3. Create with `POST /workflows` (name, nodes with fresh uuids, connections, settings). Then `POST /workflows/{id}/activate` and assert `active: true`.
4. Fire the real trigger (webhook POST, manual execution) and read `GET /executions/{id}?includeData=true` runData per node. Fix from evidence, never from guesses.
5. Keep the builder key in session scratch (auto-pruned), never in chat logs or workflow JSON. Workflow credentials travel by id reference only.

## Pitfalls (verified the hard way)

- Code node DEFAULT mode is single-shot (`runOnceForAllItems`): with no explicit `mode`, `$json` sees only the first item and the rest silently vanish. Set `mode: runOnceForEachItem` for per-item JS, or use `$input.all().map(...)` with single-shot mode deliberately.
- SplitInBatches outputs are done-first: output 0 is done, output 1 is the loop. Wire backwards and the loop silently processes nothing while done emits raw items.
- Loops need ONE re-entry edge: fan every branch output back and the shared batch state races, emitting partial dones. Fan Calc into the loop node once, hang side branches (switches, loggers) off the loop body as terminals.
- Webhook trigger needs `httpMethod: POST` plus `responseMode: responseNode` when a Respond node answers; defaults (GET, onReceived) fail with 404/500 on real posts.
- A Respond node with no incoming data errors the run: every declared branch must either deliver or be a deliberate terminal.
- Unused nodes still validate: a disconnected tool or responder can fail activation. Remove what the run does not need.
- Community nodes must be INSTALLED on the instance, not just credentialed: a present credential with a missing package activates fine at create time then fails at activation with `Unrecognized node type`. Check before promising live search.
- Tavily tool node is `n8n-nodes-tavily.tavilyTool` v2.1, resource search, operation query, with the Tavily credential id; finance topic is a first-class value.
- Test payloads must match the node's real input shape: webhook bodies arrive under `$json.body`, not top-level `$json`.
