# P3-B1 v0.2 Vendor Readiness — not a Freeze or vendor PASS

Maintains earlier interim local synthetic separation and 59/59 Producer checks. Adds actual-vendor readiness scripts and independent G4 stop handling. Does not alter fixed P2 / P3-A sources.

1. Windows 11, Node/npm, Python installed. Extract this ZIP into a non-sensitive local folder. Do not copy `node_modules` from untrusted parties.
2. Open **PowerShell** in bundle root and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\run_real_vendor_probe_windows.ps1` **only if you trust this locally generated script**. It downloads npm Astro and Pagefind packages *to this local project* and produces lockfile, dist, logs. Bypass flag affects this process only; alternatively execute commands individually after inspection.
3. On success use another terminal from `astro_candidate/dist`: `py -3 -m http.server 8766 --bind 127.0.0.1`. Open `http://127.0.0.1:8766/tech-evidence/pagefind_japanese_browser_probe.html`, click Run. Save actual JSON. Then check main site homepage/theme/detail URLs and Back/Forward.
4. Keep all logs, actual lockfile, generated `dist` (excluding dependencies) and native browser evidence. **Upload as new named evidence artifact**, do not overwrite this readiness ZIP or the P3-A frozen ZIP.
5. If npm install fails with EAI_AGAIN/blocked, record NOT_EXECUTED, do NOT mark Astro/Pagefind PASS.

This is Producer-authored source, static-reviewed locally; the package install, real vendor CLI and browser click have **not** run in this environment due registry DNS failure. To accept the technology, require actual executable results and scoped independent review.

Readiness v0.2.1 repairs test-pack consistency: all four synthetic format files are present in Astro's public/ before build; search probe uses the actual synthetic canary string instead of an unrelated probe term. Earlier v0.2.0 readiness package should not be used for final vendor evidence.
