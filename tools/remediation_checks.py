#!/usr/bin/env python3
"""A remediation checks: independent fixture expectations, real HTTP/native Pagefind.
Not F evidence. Writes only the current task directory, including deliberate failures.
"""
import os,json,threading,http.server,functools,datetime,hashlib,sys,re,time,statistics
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'astro_candidate/dist';E=R/'evidence/remediation_20261015';E.mkdir(exist_ok=True)
checks=[];net=[];console=[];errors=[]
def ck(id,actual,expected):
 checks.append(dict(id=id,actual=actual,expected=expected,status='PASS' if actual==expected else 'FAIL'))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',8772),functools.partial(Quiet,directory=str(D)));threading.Thread(target=s.serve_forever,daemon=True).start();base='http://127.0.0.1:8772'
report={'role':'A Producer','start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context();pg=c.new_page()
  # Browser-generated icon 404 is recorded separately, never passed off as site-route success.
  pg.on('response',lambda r:net.append({'url':r.url,'status':r.status,'type':r.request.resource_type}))
  pg.on('requestfailed',lambda r:errors.append({'url':r.url,'failure':r.failure}))
  pg.on('console',lambda m:console.append({'type':m.type,'text':m.text}))
  pg.on('pageerror',lambda e:errors.append({'pageerror':str(e)}))
  pg.goto(base+'/');pg.wait_for_function("document.querySelector('#count').textContent==='8'")
  # Define expected record IDs from the fixed fixture contract, not computed from the lexicon.
  cases=[('谷川',['SYN-TGW-001','SYN-TGW-002']),('奥多摩',['SYN-OKU-001','SYN-OKU-002']),('丹沢',['SYN-TNZ-001','SYN-TNZ-002','SYN-TNZ-003','SYN-TNZ-004']),('穂高岳',[]),('東京',[]),('存在しない沢',[]),('奥多摩不存在',[]),('谷川丹沢',[]),('丹沢奥多摩',[]),('',[])]
  for family,letters in [('谷川','AB'),('奥多摩','AB'),('丹沢','ABCD')]:
   code={'谷川':'TGW','奥多摩':'OKU','丹沢':'TNZ'}[family]
   for i,letter in enumerate(letters,1):cases.append(('架空'+family+letter,[f'SYN-{code}-{i:03}']))
  cases.extend([('  奥多摩  ',['SYN-OKU-001','SYN-OKU-002']),('"奥多摩"',['SYN-OKU-001','SYN-OKU-002'])])
  rows=pg.evaluate('''async cases=>{const a=await import('/search/pagefind-ja.js');const n=await import('/pagefind/pagefind.js');const before=Intl.Segmenter;let out=[];for(const [q,expected] of cases){const start=performance.now();const r=await a.search(q);const data=await Promise.all(r.results.map(x=>x.data()));out.push({query:q,expected,actual:data.map(x=>x.url.match(/\\/records\\/(SYN-[A-Z]+-\\d+)\\.html/)?.[1]).filter(Boolean).sort(),urls:data.map(x=>x.url),native_ids:r.results.map(x=>x.id),normalization:r.normalization,ms:performance.now()-start});}const raw=await n.search('奥多摩');return {rows:out,raw_vendor_control:{query:'奥多摩',urls:await Promise.all(raw.results.map(async x=>(await x.data()).url))},page_Intl_unchanged:before===Intl.Segmenter};}''',cases)
  report.update(rows)
  for row in rows['rows']:
   ck('JA_'+row['query'],row['actual'],sorted(row['expected']))
   if row['query'].strip() and not row['expected']:ck('JA_NO_PAGES_'+row['query'],row['urls'],[])
  ck('PAGE_INTL_UNCHANGED',rows['page_Intl_unchanged'],True)
  ck('NATIVE_CONTROL_STILL_REPRODUCES',len([u for u in rows['raw_vendor_control']['urls'] if '/records/' in u]),0)
  # Real search UI -> detail -> Back; default home substring -> detail also separately checked.
  pg.goto(base+'/search/');pg.locator('#q').fill('奥多摩');pg.locator('button').click();pg.wait_for_function("document.querySelector('#status').textContent==='2件'");pg.screenshot(path=str(E/'search_results.png'))
  pg.locator('#results a[href$="SYN-OKU-001.html"]').click();ck('PAGEFIND_RESULT_CLICK',pg.url,base+'/themes/okutama-sawa-db/records/SYN-OKU-001.html');pg.go_back();ck('PAGEFIND_BACK',pg.url,base+'/search/')
  pg.goto(base+'/');pg.locator('#keyword').fill('谷川');pg.locator('#results a[href$="SYN-TGW-001.html"]').click();ck('HOME_SEARCH_CLICK',pg.url,base+'/themes/tanigawa-sawa-db/records/SYN-TGW-001.html')
  pg.goto(base+'/');pg.locator('#keyword').fill('穂高岳');ck('HOME_EMPTY',pg.locator('#count').inner_text(),'0');pg.locator('#reset').click();ck('EMPTY_RESET',pg.locator('#count').inner_text(),'8')
  # Every primary public HTML link and each format HTTP byte stream, not example.invalid citations.
  pages=[D/'index.html',*D.glob('themes/*/index.html'),*D.glob('themes/*/records/*.html')]
  links=set()
  for path in pages:
   pg.goto(base+'/'+path.relative_to(D).as_posix());
   for href in pg.locator('a[href]').evaluate_all('els=>els.map(x=>x.href)'):
    if href.startswith(base+'/'):links.add(href.split('#')[0])
  for href in sorted(links):ck('HTTP_LINK_'+href.removeprefix(base),pg.request.get(href).status,200)
  for ext in ['html','pdf','pptx','xlsx']:
   path='fixtures/synthetic_format.'+ext;r=pg.request.get(base+'/'+path);ck('FORMAT_HTTP_'+ext,{'status':r.status,'sha':hashlib.sha256(r.body()).hexdigest()},{'status':200,'sha':hashlib.sha256((D/path).read_bytes()).hexdigest()})
  ck('UNEXPECTED_HTTP_STATUS',[x for x in net if x['status']>=400 and not x['url'].endswith('/favicon.ico')],[])
  ck('EXTERNAL_REQUESTS',[x for x in net if not x['url'].startswith(base+'/')],[])
  ck('BROWSER_RUNTIME_ERRORS',errors,[])
  # No page console errors except browser's automatic favicon request 404 (recorded).
  report['normal_network']=net.copy();report['normal_console']=console.copy();report['favicon_404']=[x for x in net if x['url'].endswith('/favicon.ico') and x['status']==404]
  ck('CONSOLE_ERRORS',[x for x in console if x['type']=='error' and '404' not in x['text']],[])
  # Genuine accepted title payload tests textContent; separate invalid path tests fail closed.
  data=json.loads((D/'demo-data.js').read_text().split(' = ',1)[1].strip().removesuffix(';'));payload='<img src=x onerror="window.__xss=1"><script>window.__xss=2</script>'
  data['records'][0]['title']=payload
  pg.route('**/demo-data.js',lambda route:route.fulfill(content_type='text/javascript',body='window.SYNTHETIC_PUBLIC_SEARCH_INDEX='+json.dumps(data)+';'))
  pg.goto(base+'/');pg.wait_for_function("document.querySelector('#count').textContent==='8'")
  ck('XSS_PAYLOAD_ACCEPTED_AS_TEXT',pg.locator('#results a').first.inner_text(),payload);ck('XSS_NO_ELEMENT',pg.locator('#results img, #results script').count(),0);ck('XSS_NO_EXECUTION',pg.evaluate('window.__xss??null'),None);pg.screenshot(path=str(E/'xss_literal.png'))
  pg.unroute('**/demo-data.js');data['records'][0]['detail_path']='javascript:window.__xss=3'
  pg.route('**/demo-data.js',lambda route:route.fulfill(content_type='text/javascript',body='window.SYNTHETIC_PUBLIC_SEARCH_INDEX='+json.dumps(data)+';'))
  pg.goto(base+'/');pg.wait_for_function("!document.querySelector('#data-error').hidden")
  ck('INVALID_PATH_FAIL_CLOSED',pg.locator('#results a').count(),0);ck('INVALID_PATH_DISABLED',pg.evaluate("document.querySelector('#filter-controls').disabled===true"),True);ck('INVALID_PATH_NOT_ZERO',pg.locator('#count').inner_text(),'—');pg.unroute('**/demo-data.js')
  # Broken adapter asset must reject visibly, not emit a valid zero-results PASS.
  for status,body in [(503,'{}'),(200,'{"schema_version":99,"terms":[]}')]:
   cc=b.new_context();pp=cc.new_page();pp.route('**/search/ja-terms.json',lambda route,request,st=status,bo=body:route.fulfill(status=st,content_type='application/json',body=bo));pp.goto(base+'/search/');pp.locator('#q').fill('奥多摩');pp.locator('button').click();pp.wait_for_function("document.querySelector('#status').textContent.includes('実行できません')");ck('LEXICON_REJECT_'+str(status),'実行できません' in pp.locator('#status').inner_text(),True);cc.close()
  pg.goto(base+'/search/');r=pg.evaluate("async()=>{const a=await import('/search/pagefind-ja.js');try{await a.search('あ'.repeat(201));return 'accepted';}catch(e){return e.name;}}")
  ck('OVERLONG_REJECTED',r,'TypeError');b.close()
except Exception as exc:
 report['exception']=str(exc);ck('EXECUTION_COMPLETED',False,True)
finally:
 s.shutdown();s.server_close();report['checks']=checks;report['summary']={v:sum(x['status']==v for x in checks) for v in ['PASS','FAIL']};report['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(E/'remediation_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'summary':report['summary'],'exception':report.get('exception'),'failures':[x for x in checks if x['status']=='FAIL']},ensure_ascii=False,indent=2))
sys.exit(0 if report['summary']['FAIL']==0 else 2)
