# P3-B1 producer-controlled Windows runner. No external cloud deployment, git push, or real data.
# Called by Owner / authorized A session in local Windows PowerShell, inside unmodified copy of this bundle.
# Install is local npm only (network required), not an evaluation of external services.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$project = Join-Path $root 'astro_candidate'
$log = Join-Path $root 'evidence\vendor_actual'
New-Item -ItemType Directory -Path $log -Force | Out-Null
function Invoke-Step($name,$cmd) {
  $at=Get-Date -Format o
  Write-Host "[RUN] $name @ $at"
  $output=& cmd.exe /d /s /c $cmd 2>&1 | Out-String
  $exit=$LASTEXITCODE
  $output | Out-File -LiteralPath (Join-Path $log "$name.log") -Encoding utf8
  Write-Host $output
  if($exit -ne 0){throw "$name EXIT $exit. This is FAIL/BLOCKED; no claim of PASS. See $log"}
}
Set-Location $project
node --version | Out-File (Join-Path $log 'node-version.txt') -Encoding utf8
npm --version | Out-File (Join-Path $log 'npm-version.txt') -Encoding utf8
npm config get registry | Out-File (Join-Path $log 'npm-registry.txt') -Encoding utf8
# Reproduce the selected exact dependencies from the submitted lockfile.
Invoke-Step '01_npm_ci' 'npm ci --no-audit --no-fund'
Invoke-Step '03_astro_build' 'npm run build'
# Pagefind extended (npm wrapper) should index Japanese via exact -ja language.
Invoke-Step '04_pagefind_index' 'npm run index:pagefind'
New-Item -ItemType Directory -Force (Join-Path $project 'dist\tech-evidence') | Out-Null
Copy-Item -LiteralPath (Join-Path $root 'tools\pagefind_japanese_browser_probe.html') -Destination (Join-Path $project 'dist\tech-evidence\pagefind_japanese_browser_probe.html') -Force
Get-FileHash (Join-Path $project 'package-lock.json') -Algorithm SHA256 | Format-List | Out-File (Join-Path $log 'package-lock-sha256.txt')
(Get-Content (Join-Path $project 'package.json') -Raw) | Out-File (Join-Path $log 'pinned-package.json') -Encoding utf8
$cli='py -3'
try { & py -3 --version | Out-Null; if($LASTEXITCODE -ne 0){throw 'no py'} } catch {$cli='python'}
$verifyCmd="$cli `"$root\tools\verify_vendor_dist.py`" --dist `"$project\dist`" --require-index"
Invoke-Step '05_dist_privacy_acceptance' $verifyCmd
Write-Host 'AUTO PHASE COMPLETE. The Pagefind CLIENT SEARCH and native Back/Forward require actual browser.'
Write-Host 'Start a separate loopback server: cd astro_candidate\dist ; py -3 -m http.server 8766 --bind 127.0.0.1'
Write-Host 'Then open http://127.0.0.1:8766/tech-evidence/pagefind_japanese_browser_probe.html and click the button.'
Write-Host 'Export JSON and attach ZIP with evidence/vendor_actual plus dist hashes; do not upload npm node_modules.'
