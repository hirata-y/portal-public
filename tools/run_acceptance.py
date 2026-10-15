#!/usr/bin/env python3
"""Run final A checks and retain FAIL; build is separate, no install or deployment here."""
import subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
steps=[('dist',['tools/verify_vendor_dist.py','--dist','astro_candidate/dist','--require-index']),('security',['tools/security_formats_probe.py']),('fault',['tools/index_fault_probe.py']),('baseline',['tools/verify_b1.py']),('browser',['tools/browser_probe.py'])]
results=[]
for name,args in steps:
 p=subprocess.run([sys.executable,'tools/run_logged.py','recheck_'+name,'.',sys.executable,*args],cwd=R)
 results.append({'step':name,'exit_code':p.returncode})
print(json.dumps(results,indent=2));sys.exit(0 if all(x['exit_code']==0 for x in results) else 2)
