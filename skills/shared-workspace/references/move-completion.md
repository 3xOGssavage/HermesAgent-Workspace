# Move completion (ferry checklist)

Use when one project folder exists in two copies (old path + new home) and the old copy is slated for deletion.

## Order (each verified before the next)

1. Ground check new home: date, HEAD, clean tree, remote. Record short hash + message + dirty files.
2. Re-point new origin to GitHub (never the old path). Confirm with remote -v; old-path remote must be gone.
3. Fetch + fast-forward old tip into new home only after proving safe: ancestor check passes and zero local commits. Apply clean.
4. Content proof: hash-compare key files; for text diffs that remain, re-run with CR-stripped comparison. Line-endings-only deltas are functionally zero per repo rule — note, do not fix.
5. Health in new home: lint (0 errors) + typecheck (exit 0). Quote both exit lines.
6. Desk note: correct build-lane path + equals standing in HANDOFF, commit + push. GitHub must show the new tip.
7. Signpost old copy uncommitted: MOVED note, do-not-build, HEAD frozen. Never commit the signpost.
8. Fresh-eyes audit of migrated state, all material items PASS. Old deletion stays the owner's word alone.

## Pitfalls

- Compare HEAD and status on BOTH paths before trusting either — the old copy keeps receiving commits after the move.
- Timestamps prove when a copy happened, never where-from; provenance lives in the operation record (diary), not dates.
- Moved always means copied-with-verification; originals stay until the owner explicitly orders deletion.
