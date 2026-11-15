# Batch bootstrap (mirror-freeze scaffold)

Use when opening a new sweep batch that mirrors a prior batch's roster. Produces the frozen roster, delta, and ledger plus the bootstrap commit — site work starts after.

1. Copy the mirrored batch's slugs/URLs/order verbatim into `00-roster.md`; stamp the freeze date. No fresh picks and no silent replacements — dead links get logged, never swapped, unless the governing protocol says otherwise.
2. Liveness-sweep every URL with a desktop-Chrome UA before freezing: `curl -s -o /dev/null -w '%{http_code}' -m 25 -A "<UA>" -L <url>`. `200` = alive. `000` with curl exit 35 in ~1s = TLS-blocked bot-wall (serves real browsers; browser-verify at capture), not dead. `000` after the full timeout = unreachable — log as dead in the roster.
3. Write `00-delta.md` (batch lens + what is new vs the mirrored batch) and `progress.md` (every site row queued, same columns as prior batches) in the same pass.
4. Commit the three files as `docs(research): stealbatch<N> bootstrap — mirror of batch<M>, <n> sites, liveness X/Y` and push. First site capture starts on the next step.
