import json,subprocess,tempfile,shutil,threading,http.server,functools,gzip,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 d=Path(t)/'dist';shutil.copytree(R/'astro_candidate/dist',d);shutil.rmtree(d/'pagefind');shutil.rmtree(d/'tech-evidence');cmd=['/tmp/p3-b1-pagefind14/node_modules/.bin/pagefind','--site',str(d),'--force-language','ja'];x=subprocess.run(cmd,capture_output=True,text=True)
 s=http.server.ThreadingHTTPServer(('127.0.0.1',8770),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(d)));threading.Thread(target=s.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto('http://127.0.0.1:8770/')
   actual=page.evaluate('''async()=>{let p=await import('/pagefind/pagefind.js'),out=[];for(let q of ['谷川','奥多摩','穂高岳']){let r=await p.search(q);let data=await Promise.all(r.results.map(x=>x.data()));out.push({query:q,urls:data.map(x=>x.url)});}return out;}''');b.close()
 finally:s.shutdown();s.server_close()
 out={'version':'1.4.0','argv':cmd,'exit_code':x.returncode,'stdout':x.stdout,'stderr':x.stderr,'actual':actual};(R/'evidence/vendor_actual/previous_minor.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
