Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$repo = 'F:\CD\Hermes Agent'
$log = Join-Path $repo 'cache\scratch\backup-last.log'
try {
  Set-Location $repo
  $want = @('config.yaml','.gitignore','skills','memories','scripts','shared')
  $targets = @()
  foreach ($t in $want) {
    if (-not (Test-Path (Join-Path $repo $t))) { continue }
    git check-ignore -q $t 2>$null
    if ($LASTEXITCODE -eq 0) { continue }
    $targets += $t
  }
  if ($targets.Count -eq 0) { 'BACKUP-SKIP: no targets' | Out-File $log; exit 0 }
  git add -- $targets 2>&1 | Out-File $log
  git diff --cached --quiet
  if ($LASTEXITCODE -eq 0) { 'BACKUP-SKIP: nothing changed' | Out-File $log; exit 0 }
  git -c user.name=Neohelper -c user.email=neohelper@local commit -qm 'auto: scheduled backup' 2>&1 | Out-File $log -Append
  $env:GIT_TERMINAL_PROMPT = '0'
  git pull --rebase --autostash origin main 2>&1 | Out-Null
  $attempt = 0; $pushed = $false
  while (-not $pushed -and $attempt -lt 3) {
    $attempt++
    git push origin main 2>&1 | Out-File $log
    if ($LASTEXITCODE -eq 0) { $pushed = $true } else { Start-Sleep -Seconds 60 }
  }
  if (-not $pushed) { 'BACKUP-FAIL: push failed 3x' | Out-File $log -Append; exit 1 }
  "BACKUP-OK: pushed $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Out-File $log -Append
} catch { "BACKUP-FAIL: $($_.Exception.Message)" | Out-File $log -Append; exit 1 }
