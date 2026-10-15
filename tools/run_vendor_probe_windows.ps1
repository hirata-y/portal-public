# P3-B1 independent reproducibility helper. Runs ONLY on Windows localhost.
# This script intentionally installs public npm dependencies to the local PoC folder.
# It does not push, deploy, authenticate or use personal user content.
$ErrorActionPreference = 'Stop'
$here = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$project = Join-Path $here 'astro_candidate'
$logs = Join-Path $here 'evidence\windows_vendor_probe'
New-Item -ItemType Directory -Force -Path $logs | Out-Null
Set-Location $project
@('node -v','npm -v','npm config get registry') | Set-Content -Encoding UTF8 (Join-Path $logs 'env-commands.txt')
node -v | Out-File -FilePath (Join-Path $logs 'node-version.txt')
npm -v | Out-File -FilePath (Join-Path $logs 'npm-version.txt')
Write-Host 'Will install Astro/Pagefind in the local PoC only. No GitHub/Cloudflare writes.'
npm install --save-exact --no-audit --no-fund astro 2>&1 | Tee-Object -FilePath (Join-Path $logs 'install-astro.txt')
if ($LASTEXITCODE -ne 0) { throw 'Astro npm install failed; record as NOT_EXECUTED.' }
npm install --save-dev --save-exact --no-audit --no-fund pagefind 2>&1 | Tee-Object -FilePath (Join-Path $logs 'install-pagefind.txt')
if ($LASTEXITCODE -ne 0) { throw 'Pagefind npm install failed; record as NOT_EXECUTED.' }
npm run build 2>&1 | Tee-Object -FilePath (Join-Path $logs 'astro-build.txt')
if ($LASTEXITCODE -ne 0) { throw 'Astro build failed. Do not claim framework validated.' }
npm run index:pagefind 2>&1 | Tee-Object -FilePath (Join-Path $logs 'pagefind-index.txt')
if ($LASTEXITCODE -ne 0) { throw 'Pagefind index failed. Do not claim index validated.' }
Get-FileHash (Join-Path $project 'package-lock.json') -Algorithm SHA256 | Format-List | Out-File (Join-Path $logs 'lock-sha.txt')
Write-Host 'Binaries completed. Still required: actual Japanese queries and real browser URL/Back acceptance.'
Write-Host 'Start loopback at generated site: cd astro_candidate\dist; py -m http.server 8766 --bind 127.0.0.1'
