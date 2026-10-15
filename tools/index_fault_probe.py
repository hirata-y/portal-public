#!/usr/bin/env python3
"""Build a real fault-injected Pagefind index in temp, verify native client detects it."""
import os
import json,tempfile,shutil,subprocess,threading,http.server,functools,sys,datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];E=R/'evidence/vendor_actual';canary=json.loads((R/'docs/SOURCE_PIN.json').read_text())['canary']
report={'role':'A Producer self-check','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with tempfile.TemporaryDirectory(prefix='p3b1-index-fault-') as t:
 d=Path(t)/'public';shutil.copytree(R/'astro_candidate/dist',d);shutil.rmtree(d/'pagefind');shutil.rmtree(d/'tech-evidence')
 shutil.copytree(R/'outputs/members',d/'members')
 cmd=['node',str(R/'astro_candidate/node_modules/pagefind/lib/runner/bin.cjs'),'--site',str(d),'--force-language','ja'];x=subprocess.run(cmd,text=True,capture_output=True);report['index_build']={'argv':cmd,'exit_code':x.returncode,'stdout':x.stdout,'stderr':x.stderr}
 if x.returncode:raise RuntimeError('fault index build failed')
 class Quiet(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*a):pass
 srv=http.server.ThreadingHTTPServer(('127.0.0.1',8768),functools.partial(Quiet,directory=str(d)));threading.Thread(target=srv.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path=os.environ.get('P3_B1_BROWSER','/usr/bin/chromium'),args=['--no-sandbox']);page=b.new_page();page.goto('http://127.0.0.1:8768/')
   report['actual']=page.evaluate('''async q=>{const pf=await import('/pagefind/pagefind.js');await pf.init();let out=[];for(let query of [q,'"'+q+'"']){let r=await pf.search(query);let data=await Promise.all(r.results.map(x=>x.data()));out.push({query,count:r.results.length,urls:data.map(x=>x.url)});}return out;}''',canary);b.close()
 finally:srv.shutdown();srv.server_close()
 from privacy_scan import scan
 report['scanner_findings']=scan(d,canary.encode())
report['status']='PASS' if any('/members/' in u for u in report['actual'][0]['urls']) and any('decoded_private_url' in f for f in report['scanner_findings']) else 'FAIL';(E/'index_fault_injection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(0 if report['status']=='PASS' else 2)
