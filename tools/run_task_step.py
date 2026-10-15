#!/usr/bin/env python3
"""Exact argv/stdout/stderr/exit for the bounded B1 remediation task."""
import datetime,json,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parents[1];name,cwd,*argv=sys.argv[1:];out=root/'evidence/remediation_20261015';out.mkdir(exist_ok=True,parents=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.perf_counter()
try:
 p=subprocess.run(argv,cwd=root/cwd,capture_output=True,text=True);code=p.returncode;stdout=p.stdout;stderr=p.stderr
except OSError as e:code=127;stdout='';stderr=str(e)
j={'name':name,'argv':argv,'cwd':str(root/cwd),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'duration_seconds':time.perf_counter()-t,'exit_code':code,'stdout':stdout,'stderr':stderr};(out/(name+'.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');(out/(name+'.log')).write_text(stdout+'\nSTDERR:\n'+stderr+'\nEXIT: '+str(code)+'\n');print(json.dumps({k:v for k,v in j.items() if k not in ['stdout','stderr']},ensure_ascii=False));print(stdout);print(stderr,file=sys.stderr);sys.exit(code)
