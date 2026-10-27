---
name: shared-workspace
category: autonomous-ai-agents
description: "Use when two AI agents share one working folder and memory."
version: 1.0.0
author: Neohelper
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [multi-agent, shared-workspace, memory, collaboration]
    related_skills: [hermes-mcp-setup, lstm-bridge]
---

# Shared Workspace for Cooperating Agents

One folder both agents read and write, one memory both agents learn from, rules that keep two writers from corrupting each other. Default layout for this owner: F:/CD/Projects holds all projects in one repo; each agent keeps its own private home beside it.

## When to Use

Setting up or changing a shared project folder for two agents, defining who may write what, designing the shared memory and review ritual, or moving projects into the shared home.

## Procedure

1. Agree the shape before moving anything: one repo with project folders (not one repo per project), pilot the biggest project first, rest after the pilot proves out.
2. Move, never copy: verify presence at the new address before removing the source; grep for absolute old paths and repoint every reference (workflows, configs, docs) as part of the move, not later.
3. Lock secrets out of the shared tree first: gitignore secrets, tokens, sessions, and pairings in every repo before init; owner-only file rights on every credential; leak-scan on commit. Agents reference secrets by variable name only, never by value, in anything the other agent can read.
4. Assign one writer role per concern (default: builder agent builds and edits, reviewer agent maps, reviews, verifies; owner breaks ties). Any file change gets a one-line note first.
5. Memory in two tiers only: one MEMORY file in the shared root for working truths, the shared vault for lasting ones. Both agents read the vault index every session; both propose, owner alone approves.
6. Evolve on a loop: propose (either agent, never silent) -> use twice in real work -> promote to vault -> distill to a skill only when it becomes procedure. Conflicts keep both versions visible with an expiry date; newest wins if the owner does not pick in time.
7. Back up nightly to the owner's remote (default 3 AM) plus one cold copy before adding the second project. Alert on failure in the owner's chosen channel.

## Pitfalls

- Never let a map outlive its code: whoever changes code rebuilds that project's index the same sitting, because a stale map plus fresh code produces confident wrong answers.
- Never run two writers on one file the same day without an owner assignment; last-writer-wins is silent data loss, not collaboration.
- Never let approval queues pile up: default-approve low-risk entries after 48 hours, otherwise the owner becomes the bottleneck and learning halts.
- Never build ceremony for a two-agent team that only pays off at twenty: one repo, one memory file, delete-on-touch beats tiers, boards, and quarterly reviews that die in three weeks.
- Never cross a credential between agents: each agent holds its own keys, and a shared instance means shared visibility — separation is audit and revocation, never walls.
- Disagreements resolve by joint research first, owner decision only on deadlock.
