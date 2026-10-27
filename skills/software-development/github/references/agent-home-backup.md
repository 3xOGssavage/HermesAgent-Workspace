# Backing Up a Live Agent Home to GitHub

For pushing an agent's own home folder (Hermes home, opencode config dir) to a
private repo: the folder holds live secrets next to shareable config, so the
order matters more than the commands.

## Procedure

1. Write `.gitignore` BEFORE `git init` or the first `add`: secrets
   (`.env`, `auth.json`, token dirs, pairing, `*.pem`, `*.key`, credential
   files), runtime junk (caches, logs, sessions, state DBs, checkpoints,
   backups, tool downloads, installs), regenerable maps, and chat history
   or pasted-content dirs.
2. Migrate every plaintext secret already in tracked config to the secrets
   file plus `${VAR}` references in config, then re-verify: a secret moved
   after the first commit lives in history forever.
3. Scan staged files for secret-shaped strings (API key prefixes, JWT
   segments, bearer tokens) before the first commit; if anything leaked
   into local history, delete `.git` and re-init — safe only while nothing
   was ever pushed.
4. Verify remotes, auth, and scope BEFORE pushing: a fresh private repo
   plus a token without access to it fails the same way an expired token
   does. Read the full server error body, not the summary line.
5. Verify the remote shows the commit after pushing (`ls-remote`), never
   assume the push landed.

## Pitfalls

- Stage with `git add` only after the ignore file is final; unstage with
  `git rm -r --cached` when the ignore list changes mid-setup, and confirm
  the staged count drops before committing.
- On Windows set the repo-local credential helper to `manager` and export
  `GIT_TERMINAL_PROMPT=0` for every non-interactive push; the default
  helper selector pops a GUI dialog that hangs headless runs. Never leave
  the helper empty to dodge the popup — that also disables stored
  credentials and every push fails.
- Keep one writer convention: secrets live in the secrets file, settings
  in config; a value in both places drifts, and the wrong one wins silently.
