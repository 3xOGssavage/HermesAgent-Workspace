# n8n via REST (workflows, credentials, nodes)

Companion to the n8n connect bullet in SKILL.md (that covers the MCP door). This covers building inside n8n through its REST API with the Settings API key (public-api audience) — the MCP JWT (mcp-server-api audience) is rejected by REST with 401, so match the key to the door first.

## Keys and auth

- REST takes `X-N8N-API-KEY: <settings key>`. A 401 on every REST path with a working MCP token means wrong key for the door, not broken wiring — switch keys before touching config.
- Park a long pasted key in one 600-perm scratch file for the session and read it per call instead of retyping it into every command; retyping long tokens produces silent single-char breaks that 401.

## Workflows

- PUT /workflows/{id} requires `name` in the body alongside nodes/connections/settings — without it the API answers 400 naming the missing property, so include it always and read the error body before guessing at node shapes.
- Activation resolves node types strictly: `400 Unrecognized node type: X` means the community package providing X is not installed on that instance, even when a credential of the same family exists (an orphaned credential proves nothing about the node). Fix is installing the package in n8n Settings, never reshaping the workflow to dodge it.
- Never hand-write node type/version/params from memory: copy the exact node JSON (type, typeVersion, credentials block, sub-tool connection keys like ai_languageModel/ai_memory/ai_tool) from a working workflow in the same instance, then change only names, prompts, and credential picks. Node catalogs drift per instance; the instance is its own schema reference.

## Webhook intake (verified defaults that bite)

- A new webhook trigger defaults to GET: POSTing to it 404s. Set `httpMethod: POST` explicitly when the caller posts.
- Wiring a Respond-to-Webhook node with the trigger still on the default response mode fails the run with 'Unused Respond to Webhook node' — set `responseMode: responseNode` on the trigger in the same edit.
- Incoming payloads arrive wrapped: Code nodes must read `$json.body` (falling back to `$json`), not top-level fields — an empty read scores zero and fails silently downstream, so prove the parse with one live POST before building on it.

## Tavily node (verified contract)

- Regular node type `n8n-nodes-tavily.tavily`; agent-tool variant ends with `Tool` and needs node major >= 2 for tool features.
- Search call shape: resource `search`, operation `query`, params `query`, `topic` (`general`/`news`/`finance` — finance exists for market work), plus depth/range knobs. Let the model fill the query with the fromAI expression format rather than a fixed string.
- Credential block shape: `{"tavilyApi": {"id": ..., "name": ...}}` picked from the instance credential list — confirm the credential is actually attached to a used node before relying on it.
