# Graphify structure trial (copy-first, audited)

When to use: trialing a Graphify knowledge-graph view over any markdown vault/corpus where the live source must stay untouched.

Trial a Graphify knowledge-graph view of a markdown vault without ever touching the live vault. All work happens on a scratch copy; the vault is hash-verified before and after.

## Recipe (copy-first, never live)

1. Copy the vault (or one subfolder first) to scratch. Start with ONE subfolder; expand only after the first pass verifies.
2. Add a `.graphifyignore` for junk (caches, outputs, media).
3. Run: `graphify extract <folder> --backend <name> --max-concurrency 1`.
4. Outputs (scratch only, gitignored): `graph.json` (machine), `graph.html` (clickable map), `GRAPH_REPORT.md` (inputs, counts, verdict).
5. Re-run on change or it goes stale. Record the rerun inputs so determinism is checkable (same inputs = identical counts).

## Step-0 checks (before any run — the brief goes stale)

- Package name is `graphifyy` (double-y); the command is `graphify`. Verify via `uv tool run --from graphifyy graphify --help` — never assume the binary name.
- License flag: repo+pricing says Apache 2.0 vs what-is page says MIT. Trial is evaluation only; recheck before any business use.
- Backend availability: `ollama` needs a local server at `http://localhost:11434` (connection error = no server, not a tool failure). Other backends need their keys present in env.
- Cost budget: one evening, zero spend unless a paid backend is used. Log cost in the report either way.

## Backend wiring (OpenAI-compatible doors)

- `graphify extract --backend gemini|kimi|claude|openai|deepseek|ollama` (from tool help; per-command `--help` is unsupported, read top-level help).
- `openai` backend also reaches self-hosted OpenAI-compatible servers: set `OPENAI_BASE_URL` (e.g. `http://localhost:8080/v1`) + `OPENAI_MODEL` to the serving model name.
- OpenCode inference is an OpenAI-protocol door: base `https://opencode.ai/inference/openai/v1`, model IDs like `muse-spark-1.3` (see models docs for the live list).
- Console pay-as-you-go key vs Go subscription key are different doors: a Console key with no credits fails with HTTP 402 insufficient balance (empty balance, not a broken tool); a Go subscription key bills to Go plan limits instead. Use the key that matches the door being called.
- The Go subscription door uses a separate base URL (`.../inference/go/...`) and demands an `x-opencode-session` header that Graphify cannot send (no header flag exists) — so Go is unwired for Graphify even with a valid key; use an OpenAI-compatible door without that header instead, and say so plainly after one proving attempt rather than retrying variants in a loop.
- OpenRouter free works: `OPENAI_BASE_URL=https://openrouter.ai/api/v1` with a model ID carrying the `:free` suffix; one trial evening fits inside free limits.
- NIM: read the model page first — a "playground only, no API key authorizes it" banner means that model ID is unwired regardless of key; pick a listed, API-enabled model instead of burning runs on it.
- `xhigh`/effort-style chat reasoning levels are not model knobs Graphify can pass; do not present them as backend parameters. Record the model ID actually used.

## Verdict rules (frozen per trial brief)

- Q61 (keep only if it earns its place): NOT PROVEN until a graph is produced and inspected. Say so plainly when blocked.
- Q67 (keep passing half even if the picture fails): PASS when the scan path works (AST found docs, counts match), even with zero semantic nodes.
- Blocked-on-backend is not failed-on-merit: missing server/key is an environment hold with a named next step (start server, expose key, or defer), never a tool verdict.

## Vault-untouched law

- No writes to the live vault, ever, from trial tracks. Hash-verify the source copy before and after; keep trial outputs in scratch with `no .obsidian` contamination rules.
- Secrets: paths/counts/names only in reports and logs. A `sk-` substring hit inside the word `task-log` is the classic false positive — quote surrounding context when clearing it, never silently pass.
