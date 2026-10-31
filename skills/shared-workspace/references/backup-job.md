# Backup Job Recipe (shared repos and agent homes)

Companion to the shared-workspace nightly-backup step. Copy the pattern, adjust the pathspec, never the stage order.

## Stage order (each stage logs to the same log file)

1. Set location to the repo root; build the target list from existing, non-ignored paths only (skip anything gitignore swallows, or the add aborts the whole run).
2. Stage the explicit pathspec: settings, ignore file, skills, memories, scripts, shared docs. Never bare add-all on a live agent home.
3. Diff the index quietly; exit silent when empty (no commit, no log line beyond nothing-changed).
4. Scan the staged diff for secret patterns before committing (nested config blocks do not route to the secrets file, so a clean top-level scan is not enough). Abort on any hit.
5. Commit with the bot identity passed inline so unattended commits never impersonate the owner.
6. Pull with rebase plus autostash so unstaged churn never blocks the pull.
7. Push up to three times with a minute between attempts; on final failure write FAIL with the error and exit nonzero so the scheduler alerts.
8. On success append one OK line with the timestamp.

## Pre-flight checklist (run once per new repo)

- Repo-level and global credential helper both set, so no interactive prompt can ever appear (prompts stall headless runs and pop dialogs on the owner's screen).
- Bot identity configured or passed inline for every commit.
- Remote URL matches the current repo name (renames break it silently via redirect until updated).
- One manual end-to-end run observed before scheduling: commit appears, remote hash matches local.
- Failure route configured (alert channel), because every failure mode here is silent by default.
- Encrypted offside copy of the secrets file exists and its recovery steps are recorded, since the backup itself excludes it.
- Slow or flaky pipes push in the background with interactive prompts disabled, then verify with a remote-hash read; a killed foreground push looks finished while the remote never moved.
## Failure alerts (Discord webhook)

- Post alerts with `Invoke-RestMethod` carrying an explicit browser-style `-UserAgent`: Discord's edge returns 403 to bare-script requests (Python urllib default, PowerShell default), so a stored-good webhook tests fine from a browser and fails from the job — the fix is the header, not a new webhook. Always live-test the post once and read the channel before relying on it; regenerate the webhook only if the headered post still 403s.
- Read the webhook URL from the secrets file at send time; never bake it into the script.
- Editor auto-fetch off for the repo, so the editor's own background sync never pops credential dialogs on the owner's screen.
