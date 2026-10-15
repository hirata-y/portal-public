#!/usr/bin/env python3
import json,threading,http.server,functools,tempfile,shutil,subprocess,datetime,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'astro_candidate/dist';E=R/'evidence/remediation_20261015';checks=[]
def ck(id,a,e):checks.append({'id':id,'actual':a,'expected':e,'status':'PASS' if a==e else 'FAIL'})
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',8773),functools.partial(Q,directory=str(D)));threading.Thread(target=s.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);g=b.new_page()
  g.route('**/search/ja-terms.json',lambda r:r.fulfill(content_type='application/json',body=json.dumps({'schema_version':1,'language':'ja','terms':['あ','ああ']})))
  g.goto('http://127.0.0.1:8773/search/');result=g.evaluate("async()=>{let a=await import('/search/pagefind-ja.js');try{await a.search('あ'.repeat(20));return 'accepted';}catch(e){return String(e)}}")
  ck('AMBIGUOUS_TOKENIZATIONS_BOUNDED','分割候補が多い' in result,True);b.close()
finally:s.shutdown();s.server_close()
# The real generator rejects a real private route fragment, independent of canary query count.
with tempfile.TemporaryDirectory() as td:
 dest=Path(td)/'dist';shutil.copytree(D,dest)
 import gzip
 f=next((dest/'pagefind/fragment').glob('*.pf_fragment'));j=json.loads(gzip.decompress(f.read_bytes())[12:]);j['url']='/members/canary.html';f.write_bytes(gzip.compress(b'pagefind_dcd'+json.dumps(j).encode()))
 code="import {createLexicon} from './tools/create_ja_lexicon.mjs';createLexicon(process.argv[1]);"
 x=subprocess.run(['node','--input-type=module','-e',code,str(dest)],cwd=R,capture_output=True,text=True)
 generation={'argv':x.args,'exit_code':x.returncode,'stdout':x.stdout,'stderr':x.stderr}
 ck('PRIVATE_FRAGMENT_GENERATOR_REJECT',x.returncode!=0 and 'Non-public index source' in x.stderr,True)
# Generated vendor JS, WASM, fragments remain byte-identical to the pre-remediation commit.
original={r['path']:r for r in json.loads((R/'MANIFEST.json').read_text())['files']}
rows=[]
for f in sorted((D/'pagefind').rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(R).as_posix();old=original.get(rel,{}).get('sha256');actual=hashlib.sha256(f.read_bytes()).hexdigest()
 rows.append({'path':rel,'sha256':actual,'old_sha256':old,'equal':old==actual})
ck('ALL_26_VENDOR_FILES_UNMODIFIED',len(rows)==26 and all(r['equal'] for r in rows),True)
report={'role':'A','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'vendor_byte_comparison':rows,'generator_rejection':generation,'ambiguous_query_error':result,'summary':{s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']}}
(E/'adapter_negative.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'checks':checks,'summary':report['summary']},ensure_ascii=False,indent=2));raise SystemExit(0 if report['summary']['FAIL']==0 else 2)
