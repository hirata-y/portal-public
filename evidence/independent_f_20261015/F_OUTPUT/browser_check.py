import asyncio,json,pathlib,re,datetime,threading,http.server,functools,subprocess,os
from playwright.async_api import async_playwright
R=pathlib.Path(__file__).resolve().parent.parent;O=R/'F_OUTPUT';D=R/'astro_candidate/dist';checks=[];console=[];errors=[];network=[];requests=[];screens=[]
def c(name,expected,actual):
 x={'name':name,'expected':expected,'actual':actual,'pass':expected==actual,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};checks.append(x);print(json.dumps(x,ensure_ascii=False),flush=True)
def ids(urls):return sorted(set(re.findall(r'SYN-(?:TGW|OKU|TNZ)-\d{3}',' '.join(urls))))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(D)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=False,args=['--no-sandbox','--disable-dev-shm-usage','--start-maximized'],env={**os.environ,'DISPLAY':':99'})
  ctx=await b.new_context(viewport={'width':1280,'height':850});page=await ctx.new_page()
  page.on('console',lambda m: console.append({'type':m.type,'text':m.text,'location':m.location}));page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('requestfailed',lambda q:network.append({'url':q.url,'failure':q.failure}));page.on('response',lambda r: requests.append({'url':r.url,'status':r.status}))
  async def snap(name):
   await page.screenshot(path=str(O/(name+'.png')),full_page=True);await page.wait_for_timeout(200)
   q=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','x11grab','-video_size','1440x1100','-i',':99','-frames:v','1',str(O/(name+'_native.png'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   screens.append({'name':name,'url':page.url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_command_exit':q.returncode,'native_log':q.stdout.decode()})
  await page.goto(base+'/');await page.wait_for_selector('#results li');c('home_8',8,await page.locator('#results li').count());c('theme_3',3,await page.locator('.theme-card').count());await snap('home')
  await page.locator('.theme-tanigawa').click();c('home_theme_navigation',base+'/themes/tanigawa-sawa-db/index.html',page.url)
  await page.locator('a[href*="SYN-TGW-001.html"]').click();c('theme_detail_navigation',True,page.url.endswith('/SYN-TGW-001.html'));await snap('detail')
  await page.go_back();c('back_theme',True,page.url.endswith('/tanigawa-sawa-db/index.html'))
  await page.go_forward();c('forward_detail',True,page.url.endswith('/SYN-TGW-001.html'));await page.go_back();await page.go_back();c('back_home',base+'/',page.url)
  async def visible():return ids(await page.locator('#results a').evaluate_all('(aa)=>aa.map(a=>a.href)'))
  async def filt(name,exp):c(name,sorted(exp),await visible())
  allids=['SYN-TGW-001','SYN-TGW-002','SYN-OKU-001','SYN-OKU-002']+[f'SYN-TNZ-00{i}' for i in range(1,5)]
  c('home_record_ids',sorted(allids),await visible());c('null_difficulty_default', '2',await page.locator('#ungraded-count').inner_text())
  await page.locator('input[name="area"][value="tanigawa"]').check();await page.locator('input[name="area"][value="okutama"]').check();await filt('area_OR',allids[:4])
  await page.locator('input[name="months"][value="6"]').check();await page.locator('input[name="months"][value="7"]').check();await filt('area_AND_month_OR_excludes_null',['SYN-TGW-001','SYN-OKU-001','SYN-OKU-002'])
  await page.locator('#max-days').select_option('1');await filt('area_month_AND_days',['SYN-OKU-001']);await page.locator('#reset').click();await filt('reset_8',allids)
  await page.locator('#grade-scheme').select_option('syn-scale-x');await filt('scheme_excludes_null_and_other',['SYN-TGW-001','SYN-OKU-001','SYN-OKU-002','SYN-TNZ-003','SYN-TNZ-004'])
  await page.locator('input[name="grade"][value="X2"]').check();await page.locator('input[name="grade"][value="X3"]').check();await filt('grade_OR',['SYN-TGW-001','SYN-OKU-001','SYN-OKU-002']);await page.locator('#grade-scheme').select_option('syn-scale-y');await filt('scheme_switch_clears_grades',['SYN-TNZ-001'])
  await page.locator('#reset').click();await page.locator('#max-days').select_option('1');await filt('days_null_excluded',['SYN-TGW-002','SYN-OKU-001','SYN-TNZ-003'])
  await page.locator('#reset').click();await page.locator('#keyword').fill('<img src=x onerror="window.__F_XSS=1">');await filt('home_xss_zero',[]);c('home_xss_not_executed',None,await page.evaluate('window.__F_XSS||null'))
  await page.goto(base+'/search/');await snap('search_initial')
  queries=[('谷川',['SYN-TGW-001','SYN-TGW-002']),('奥多摩',['SYN-OKU-001','SYN-OKU-002']),('丹沢',[f'SYN-TNZ-00{i}' for i in range(1,5)]),('穂高岳',[]),('F_REVIEW_NONEXISTENT_791',[]),('奥多摩不存在',[])]
  queries += [(t,[i]) for t,i in [('架空谷川A','SYN-TGW-001'),('架空谷川B','SYN-TGW-002'),('架空奥多摩A','SYN-OKU-001'),('架空奥多摩B','SYN-OKU-002')]]+[(f'架空丹沢{chr(64+i)}',[f'SYN-TNZ-00{i}']) for i in range(1,5)]
  queries += [('"奥多摩"',['SYN-OKU-001','SYN-OKU-002']),(' 奥多摩 ',['SYN-OKU-001','SYN-OKU-002'])]
  query_raw=[]
  for q,expect in queries:
   got=await page.evaluate('''async q=>{const m=await import('/search/pagefind-ja.js');const r=await m.search(q);return {normalization:r.normalization,data:await Promise.all(r.results.map(x=>x.data()))}}''',q)
   query_raw.append({'query':q,'expected':expect,'actual':got});c('adapter_query_'+q,sorted(expect),ids([x['url'] for x in got['data']]))
  (O/'search_native_objects.json').write_text(json.dumps(query_raw,ensure_ascii=False,indent=2))
  native=await page.evaluate('''async()=>{const m=await import('/pagefind/pagefind.js');const r=await m.search('奥多摩');return await Promise.all(r.results.map(x=>x.data()))}''');c('native_only_known_limitation',[],ids([x['url'] for x in native]));c('page_Intl_Segmenter_intact','function',await page.evaluate('typeof Intl.Segmenter'))
  await page.locator('#q').fill('奥多摩');await page.locator('button').click();await page.wait_for_function("document.querySelector('#status').textContent==='2件'");c('search_UI_exact_ids',['SYN-OKU-001','SYN-OKU-002'],await visible());await snap('search_okutama')
  await page.locator('a[href$="SYN-OKU-001.html"]').click();c('search_click_detail',True,page.url.endswith('/SYN-OKU-001.html'));await snap('search_click');await page.go_back();c('search_back',base+'/search/',page.url)
  for payload in ['<script>window.__F_XSS=1</script>','<img src=x onerror="window.__F_XSS=1">','javascript:alert(1)']:
   await page.locator('#q').fill(payload);await page.locator('button').click();await page.wait_for_function("!document.querySelector('#status').textContent.includes('検索中')");c('search_xss_not_executed_'+payload,None,await page.evaluate('window.__F_XSS||null'));c('search_xss_no_injected_DOM_'+payload,0,await page.locator('#results script,#results img').count())
  # Click every primary theme/detail target on genuine HTTP in this context.
  for path in ['/themes/tanigawa-sawa-db/index.html','/themes/okutama-sawa-db/index.html','/themes/tanzawa-sawa-db/index.html']+['/'+str(x.relative_to(D)) for x in sorted(D.glob('themes/*/records/*.html'))]:
   r=await page.goto(path if path.startswith(base) else base+path);c('http_page_'+path,200,r.status)
  for ext in ['html','pdf','pptx','xlsx']:
   r=await ctx.request.get(base+'/fixtures/synthetic_format.'+ext);c('format_get_'+ext,200,r.status);c('format_bytes_'+ext,(D/('fixtures/synthetic_format.'+ext)).stat().st_size,len(await r.body()))
  # Faults intercepted only in independent context; no candidate edits.
  for name,match,body in [('lexicon_bad','**/search/ja-terms.json','{}'),('worker_bad','**/search/pagefind-ja-worker.js','throw new Error("F injected worker fault");')]:
   fault=await ctx.new_page();await fault.route(match,lambda route:route.fulfill(status=200,body=body,content_type='application/javascript' if name=='worker_bad' else 'application/json'))
   await fault.goto(base+'/search/');await fault.locator('#q').fill('奥多摩');await fault.locator('button').click();await fault.wait_for_function("document.querySelector('#status').textContent.startsWith('検索を実行できません。')",timeout=35000);c(name+'_fails_closed',0,await fault.locator('#results li').count());await fault.close()
  # Normal page only: injected faults use separate page without normal listeners.
  c('normal_pageerrors',[],errors);c('normal_console_errors',[],[x for x in console if x['type']=='error']);c('normal_request_failed',[],network);c('normal_http_error_status',[],[x for x in requests if x['status']>=400]);c('normal_external_requests',[],[x for x in requests if not x['url'].startswith(base)])
  c('native_screens_capture',[],[x for x in screens if x['native_command_exit']!=0])
  await b.close()
try:asyncio.run(main())
finally:
 (O/'browser_results.json').write_text(json.dumps({'base_url':base,'checks':checks,'console':console,'pageerrors':errors,'request_failed':network,'responses':requests,'screenshots':screens},ensure_ascii=False,indent=2));s.shutdown()
print(json.dumps({'pass':sum(x['pass'] for x in checks),'fail':[x for x in checks if not x['pass']]},ensure_ascii=False));assert checks and all(x['pass'] for x in checks)
