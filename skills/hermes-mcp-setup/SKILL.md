---
name: hermes-mcp-setup
description: Add and verify Hermes MCP servers without half-done configs.
version: 0.1.0
author: Neohelper
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, setup, verification]
    related_skills: [hermes-agent]
---

# Hermes MCP Setup (fully done, every time)

## Add

- Prefer `hermes mcp add NAME --command CMD --env K=V ... --args ...`: `--args` must be LAST, everything after it becomes args.
- Repeated flags keep only the LAST value. For 2+ env keys, set the rest after with `hermes config set mcp_servers.NAME.env.KEY VALUE` one per key.
- OAuth remote servers: `mcp add --url URL --auth oauth` saves disabled on first failed connect; then `config set mcp_servers.NAME.auth oauth`, run interactive `mcp login NAME` (needs a real browser), verify with `mcp test`, then `config set mcp_servers.NAME.enabled true`. When the entry was written by hand with `config set`, `mcp login` refuses with 'not configured for OAuth' until the auth field is set — set it before telling the user to log in. A 401 from `mcp test` before login is expected and proves the address is right, not a failure. When the client skips automatic client registration, register by hand once at the provider's registration endpoint and save the issued id/secret with `config set` (never print them); the grant screen still needs a real browser, so run `mcp login` from the user's own terminal when the session is non-interactive. A registered redirect of bare loopback without a port fails the grant against clients that bind a dynamic port — match the exact redirect the client binds or stay on the working auth shape. Flipping a working server to a new auth shape must be followed by an immediate `mcp test`; on failure revert the auth field first (restoring the proven door) and only then research the new shape — never leave the server broken while investigating. When `mcp login` fails without ever showing a URL even with secrets saved, finish by hand instead of retrying: see `references/oauth-manual-completion.md`.
- No rename command exists: copy each key to the new name with `config set`, then `mcp remove` the old name, then re-test the new one.
- In non-interactive terminals, skip `mcp add` for remote/URL servers (it can hang on OAuth or stacked prompts and time out): write the entry directly with `config set` for url, headers.Authorization, connect_timeout, then `mcp test`. The `add` prompt chain needs one piped answer per prompt — count prompts or the save step silently never runs.
- Catalog `install` may impose its own auth shape (OAuth) that mismatches the wanted setup; check what it wrote, and remove plus rebuild by hand when it does not match.
- A header referencing an env variable is only as live as the variable in the agent's own process tree: on Windows a newly set variable reaches future processes only, so reopening the UI over a stale server tree still sends an empty header and every boot 401s while hand probes with the pasted value return 200. Prove both layers read-only (registry present, live process present) and fully quit the app tree — every window — before retesting, because a UI reopen is not a process restart. The control test is a sibling variable known good in both layers.
- n8n instance MCP: take the Server URL from the Connect dialog (same for every client choice) plus the Access token from the API-key tab, and write the entry directly with `config set` (url, headers.Authorization as `Bearer <token>`, connect_timeout). The dialog's OAuth tab needs a browser grant; the API-key tab needs none — a 401 there means the token value, not the tab choice. Personal tokens authorize per user, not per key: two agents' keys open the same rooms, so per-agent separation is audit and revocation, never walls — the shared per-workflow toggles are the real gate. n8n issues audience-scoped tokens: the Settings API key (public-api audience) drives the REST API, the Connect-dialog token (mcp-server-api audience) drives the MCP endpoint — they are not interchangeable and the wrong one 401s everywhere, so match the token to the door before touching config. Building workflows through REST (PUT needs `name`, activation resolves node types strictly, copy node shapes from working in-instance workflows, Tavily tool contract): see `references/n8n-via-rest.md`. OAuth against n8n: use its real scope names (workflow:read, agent:execute, ... — never openid-style), register the client's exact redirect URI, then complete by hand per `references/oauth-manual-completion.md` when the helper stays blind.
- Local-folder MCP servers (copied tool dirs, e.g. vision-tool): copy the folder untouched, add a `.cmd` launcher that cds into it first, keep the vendor key in `.env` and reference it as `${VAR}` in the server env, and allow a long connect timeout (first starts are slow). Prove with a live tool call on the server's own fixture file, and separately prove the key itself is valid with a direct provider call — a passing fixture test through a shared fallback path does not prove your key works.
- For servers that resolve their workspace from the process working folder, add a small launcher script that cds into the indexed repo first, and point the MCP command at it — there is no per-server cwd option. On Windows the launcher must be a `.cmd` file; a `.sh` fails to spawn. Quote every path inside the launcher; a space in a folder name silently becomes two arguments and the server exits with an arg-count error.
- When mirroring one agent's server settings into another agent's config, mirror settings only and never copy credentials: each agent keeps its own keys, tokens, and logins. Handoff prompts to the other agent state end-goals plus the proof format (exact diff, per-server test table, stop conditions) and never step-by-step instructions — the other agent owns its files, schema, and restart. Filesystem roots stay separate per agent by design (each agent locked to its own home), never mirrored. After editing the other agent's config, prove direction with a masked diff of backup versus current: every changed line must be a setting upgrade, and secret counts must show nothing flowed the wrong way.
- Prefer a fixed global binary path over bare `npx -y pkg` for version-sensitive servers: npx floats to latest on a cold cache and a new release can empty the tool list.
- Probe a renamed package with a raw tools/list handshake before adopting the new name — a renamed server may serve deferred or empty tool lists the client cannot consume; keep the old package name when it lists tools eagerly.

## Verify (all must pass)

- `hermes mcp list` shows the server enabled.
- `hermes mcp test NAME` connects and lists tools.
- Count env keys in config matches intended count (grep found a 19-of-20 miss before).
- Live probe one tool call before declaring done; keyless connects prove nothing about auth. For token-based servers, also verify the token itself against the provider (identity plus scopes) — a passing connect with a wrong-scoped token still fails real work. When every endpoint and auth shape returns 401, the token value is dead: test it raw over plain HTTPS (status code only, never print it) before touching any config — rewiring around a dead token wastes the whole session.
- If tool_call validation rejects a parameter the server schema allows, retry once without that parameter and note the narrower gateway schema; never retry identical failing calls in a loop.
- A server added mid-session may be connectable via `mcp test` while its tools are still unknown to the running session (tool_call fails 'not a known tool name'). Start a new session or reload MCP tools before live-probing via tool_call; never retry the same failing call in a loop.
- An empty tools/list on a connected server means missing local state, not a broken server, when the server resolves tools from a workspace index or cache — build that index in the agent's working dir first (e.g. `graft build`), then re-test.
- When two agents share one remote instance, cross-check visible sets after every credential change: list the same collection from both sides and require an exact match (plus only announced additions). Any other delta is a red flag, never noise.
- A healthy tools/list still proves nothing about answers: run one real tool call against the server's index (e.g. a find_code query) before declaring done — a connected server with 6 tools and an empty or missing graph returns zero hits to every question. When the index is per-repo, wire one server per repo and confirm the graph file actually exists in the folder the launcher cds into — project docs may name a nested project folder while the root holds no graph. A root-folder build does not fold nested git repos into one graph on older server releases (each child keeps its own graph); do not chase a single whole-house graph by rebuilding the root — point the launcher at the project folder that holds the graph instead.
- Raw JSON-RPC probes listing tools while `mcp test` shows zero means version drift, not a broken server: npx can resolve a different (usually newer) release under the agent spawn env than in your terminal. Pin the exact working version (`pkg@x.y.z`) and re-test; newer releases may serve deferred or empty tool lists.
- A server saved disabled stays disabled after a passing test; flip it with `config set mcp_servers.NAME.enabled true` and confirm in `mcp list`.
- Masked secrets are normal: `mcp test` prints `Authorization: ***` and `mcp list` hides values. Masking proves the secret is stored, not missing — verify presence by key count, never by reading the value back.
- When the user wants precision over speed from an index server, keep the exact structural tier and skip any optional LLM-summary tier: machine-extracted facts with file and line spans are verifiable, model-written summaries can hallucinate. Always open the cited file at the cited line before acting on an index answer.

## Known environment facts

- Tavily rotator (shared launcher file) has 5 tools only: search, extract, crawl, map, usage. No research tool exists in it.
- Tavily chunks_per_source caps at 3 (API-side); asking 5 silently becomes 3.
- Rotator default depth is basic unless TAVILY_DEFAULT_DEPTH=advanced is set in server env.
- Rotator state file is shared with Neocoder; both agents rotate from it.
- Portal connector entries (_mcp names) cannot be deleted locally; Off with no account is fully removed for daily use.
- Supabase dual-door pattern: same official URL twice, once with read_only=true (daily), once full (admin). Broad setup: omit project_ref to open all projects; expand features to database,docs,debugging,development,functions,storage. Without a project lock every call needs an explicit project id — list projects first when unsure, never assume.
- Cloudflare MCP token must include User Details: Read or Account: Read, or every call fails 403 insufficient_scope even with Workers/R2/DNS rights. An R2 'denied' with code 10042 ('enable R2 through the dashboard') is account state, not token scope — the token is fine and needs no re-scope; R2 starts working the day the account enables it. Read the error body before touching token rights.
- Per-repo index servers (TrailCode maps): see `references/trailcode-index-servers.md` for build scope, version pinning, and per-project wiring.
