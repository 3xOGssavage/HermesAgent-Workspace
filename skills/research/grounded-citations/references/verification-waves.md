# Verification Waves for Long Research Runs

When a multi-round research task files dozens of cited facts, round output is a
draft until a dedicated wave re-checks it. Run these waves after synthesis, not
during drafting.

## Owner-audit wave

Re-fetch every cited repo, account, and path against its live page in one batch.
Record one outcome per item:

- Confirmed: live page matches the filed owner, name, and signals.
- Moved: the URL redirects. A redirect is not verification — record the new path
  and re-verify the counts on the landed page.
- Wrong: the URL 404s. Search for the canonical location, record the correction.
- Imposter: same name, negligible signals (a handful of stars, empty repo).
  Link the real source instead of the lookalike.

Org renames and repo transfers are common; expect several per long run.

## Correction protocol

When a filed fact is proven wrong, patch the exact sentence in place — never
append a contradicting note underneath it. Add one timestamped CORRECTION line
to the run log naming what changed and why. If the error came from a transitive
mention (a name seen inside another source but never opened), say so in the
log — that tells the next wave where the hole was.

## Number drift

Treat scraped counts as of a timestamp. Star, fork, and price figures move
daily; note the check time next to any count that matters and recheck
load-bearing ones before final delivery. When two sources disagree, cite both
readings with their own provenance and say which you weight and why.
