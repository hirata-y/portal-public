#!/usr/bin/env python3
"""Record exact argv, cwd, timestamps, stdout/stderr and exit without a shell."""
import sys,subprocess,time,json,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
name,cwd,*argv=sys.argv[1:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
r=subprocess.run(argv,cwd=root/cwd,capture_output=True,text=True)
out=root/'evidence/vendor_actual';out.mkdir(exist_ok=True,parents=True)
p={'name':name,'argv':argv,'cwd':str(root/cwd),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'duration_seconds':time.perf_counter()-t,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
(out/(name+'.json')).write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(out/(name+'.log')).write_text(r.stdout+'\nSTDERR:\n'+r.stderr+'\nEXIT: '+str(r.returncode)+'\n')
print(json.dumps({k:v for k,v in p.items() if k not in ('stdout','stderr')},ensure_ascii=False));print(r.stdout);print(r.stderr,file=sys.stderr);sys.exit(r.returncode)
