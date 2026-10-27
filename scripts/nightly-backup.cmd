@echo off
REM Nightly backup: commit anything changed, push to GitHub. Secrets are
REM gitignored; credential comes from Windows Credential Manager (one-time setup).
cd /d F:\CD\Hermes Agent || (echo BACKUP-FAIL: bad dir & exit /b 1)
git add -A >nul 2>&1
git diff --cached --quiet
if %errorlevel%==0 (
  echo BACKUP-OK: nothing changed
  exit /b 0
)
git -c user.name=Neohelper -c user.email=neohelper@local commit -qm "nightly: auto-backup" >nul 2>&1
if %errorlevel% neq 0 (
  echo BACKUP-FAIL: commit error
  exit /b 1
)
set GIT_TERMINAL_PROMPT=0
git push origin main 2>&1 | tail -n 2
if %errorlevel% neq 0 (
  echo BACKUP-FAIL: push error
  exit /b 1
)
echo BACKUP-OK: pushed %date% %time%
