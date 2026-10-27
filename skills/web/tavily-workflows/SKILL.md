---
name: tavily-workflows
description: Maxed Tavily web research via rotator MCP tools.
version: 0.3.0
author: Soham (3xOGsavage), Neohelper
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tavily, web-search, research, extract, crawl]
    related_skills: [blocked-page-recovery, grounded-citations]
---

# Tavily Workflows (maxed, rotator MCP)

Fixed maxed Tavily usage through the local rotator MCP (20 keys, advanced default). Use for every web search, docs lookup, deep research, fact-check, crawl, extract, or lookup task.

## When to Use

- Any web search, fresh facts, news, docs lookup, or unknown info.
- Deep research, comparison, market analysis, literature review.
- Big result sets that would flood context (use disk-filter workflow below).
- Blocked pages: try Tavily extract before blocked-page-recovery ladder.
- Don't use for: local files, repo code, or anything already in context.

## Prerequisites

- Hermes `tavily` MCP server enabled and tested (node + shared launcher).
- 20 TAVILY_API_KEY_N keys in server env; advanced is the global default.
- Scratch dir for disk filtering: the session TMPDIR (Hermes scratch, pruned daily).
- Rotator has 5 tools only: search, extract, crawl, map, usage. No research tool.

## Setup (rotator MCP, verified path)

- Add with env flags BEFORE --args: `hermes mcp add tavily --command node --env KEY=VAL ... --args <launcher>` — everything after --args is treated as args, so --env placed after it is silently swallowed and the server starts keyless or with one key.
- Repeated --env keeps only the last key; set the rest one per call with `hermes config set mcp_servers.tavily.env.TAVILY_API_KEY_N value`, then verify the count.
- Answer the interactive enable prompt non-interactively by piping Y.
- Global default depth lives in server env as TAVILY_DEFAULT_DEPTH (advanced), so per-call depth can be omitted.
- Launcher dedupes repeat keys and shares rotation state with Neocoder via the same state file; distinct-key count is what matters, not raw count.

## Fixed Defaults (apply on every call)

- Search: advanced depth, max_results 20, chunks 3, raw content on.
- News topics: add time_range day or week (topic general only in this session).
- Extract: advanced depth, markdown format, query rerank set, chunks 3.
- Crawl/map: max_depth 5, max_breadth 80, limit 100; raise limit only if task needs.
- Caps (API-side, do not exceed): chunks max 3, max_results max 20.
- Costs: search basic 1, advanced 2 credits; extract 1-2 per 5 pages; map 1-2 per 10.

## Procedure

1. Search first, broad, no raw content. Done when titles, URLs, scores visible.
2. Extract only the best 3-5 sources, with query rerank set. Done when page bodies verified.
3. Big payloads: save raw JSON to scratch dir, filter locally, print only evidence plus source URLs. Done when no raw dump enters context.
4. Research combo (no research tool exists): max search for sources, extract top pages, synthesize cited answer in reply. Done when every claim has a source URL.
5. Batch work: cap parallel calls, tag each result ok or error, retry only failures with backoff on 429. Done when all queries resolved or explicitly failed.
6. Dedupe repeat URLs (strip query strings) and merge unique chunks before answering.

## Pitfalls

- 429 means slow down, not dead keys; back off, never hammer. A fast burst of balance probes also 429s on healthy keys — retest slow with gaps before declaring a key dead.
- Rotator exposes search, extract, crawl, map, usage only; there is no research tool, so research is always the hand combo in step 4.
- Chunks above 3 are silently clamped to 3; asking 5 wastes nothing but gains nothing.
- This session validates topic general only; use time_range for freshness instead.
- usage tool is free and never spends credits; check it before big batches.
- Shared state file with Neocoder; rotation is global, not per-agent.

## Key Health Audit

- Probe GET https://api.tavily.com/usage once per key with 12-20s gaps; bursting trips shared rate limits and 429s healthy keys, which looks like mass key death but is not.
- Read usage at data.key.usage and limit at data.key.limit, falling back to data.account.plan_usage and data.account.plan_limit; plan name at data.account.current_plan. There are no top-level usage/limit fields — reading them reports 0 and lies about the balance.
- 401/403 means the key is dead and can be dropped; 429 means back off and retest slow, never delete on a first 429.
- Sum remaining limit minus usage across keys for the pool total (free plan is 1000 credits/key/month). Done when every key has a verified status and the total is reported.

## Verification

- [ ] Search returned scored results with source URLs.
- [ ] Extracted facts trace to page bodies, not snippets alone.
- [ ] No raw JSON dump left in context; evidence plus URLs only.
- [ ] Every final claim has a cited source or is labeled unverified.
