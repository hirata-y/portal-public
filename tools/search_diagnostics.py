import json,threading,http.server,functools
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'astro_candidate/dist'
s=http.server.ThreadingHTTPServer(('127.0.0.1',8769),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(D)));threading.Thread(target=s.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto('http://127.0.0.1:8769/');c=json.loads((R/'docs/SOURCE_PIN.json').read_text())['canary']
  out=page.evaluate('''async qs=>{let pf=await import('/pagefind/pagefind.js');let out=[];for(let q of qs){let r=await pf.search(q,{verbose:true});let data=await Promise.all(r.results.map(x=>x.data()));out.push({query:q,result:r,data});}return out;}''',['奥多摩','架空奥多摩','"奥多摩"','奥 多摩','谷川',c,'"'+c+'"']);(R/'evidence/vendor_actual/search_diagnostics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps([{ 'q':x['query'],'result':{k:v for k,v in x['result'].items() if k!='results'},'hits':[{k:v for k,v in y.items() if k in ['url','excerpt','content']} for y in x['data']]} for x in out],ensure_ascii=False,indent=2));b.close()
finally:s.shutdown();s.server_close()
