#!/usr/bin/env python3
"""Producer Chromium HTTP evidence; never an independent F verdict."""
import os
import json,re,time,datetime,threading,http.server,functools,statistics,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]; E=Path(os.environ.get('P3_B1_EVIDENCE',str(R/'evidence/vendor_actual')))/'browser';E.mkdir(parents=True,exist_ok=True)
report={'role':'A Producer self-check','start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':[],'navigation':[],'page_errors':[]}
def ck(name,a,e):
 report['checks'].append({'id':name,'actual':a,'expected':e,'status':'PASS' if a==e else 'FAIL'})
def serve(folder,port):
 class Quiet(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*a):pass
 s=http.server.ThreadingHTTPServer(('127.0.0.1',port),functools.partial(Quiet,directory=str(folder)));threading.Thread(target=s.serve_forever,daemon=True).start();return s
servers=[serve(R/'astro_candidate/dist',8766),serve(R/'outputs/public',8767)]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('P3_B1_BROWSER','/usr/bin/chromium'),headless=os.environ.get('P3_B1_HEADFUL')!='1',args=['--no-sandbox','--window-position=0,0','--window-size=1440,1100','--no-first-run','--disable-session-crashed-bubble']);report['browser']=b.version
  c=b.new_context(viewport={'width':1440,'height':1000});page=c.new_page()
  page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
  def snap(name):
   report['navigation'].append({'step':name,'url':page.url,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});page.screenshot(path=str(E/(name+'.png')),full_page=True)
   if os.environ.get('P3_B1_HEADFUL')=='1':
    import subprocess
    subprocess.run(['ffmpeg','-y','-f','x11grab','-video_size','1440x1100','-i',os.environ.get('DISPLAY',':99'),'-frames:v','1',str(E/(name+'_native.png'))],check=True,capture_output=True)
  page.goto('http://127.0.0.1:8766/');page.wait_for_function("document.querySelector('#count').textContent==='8'");snap('01_home')
  page.locator('a.theme-tanigawa').click();ck('HOME_THEME_URL',page.url,'http://127.0.0.1:8766/themes/tanigawa-sawa-db/index.html');snap('02_theme')
  page.locator('a[href="records/SYN-TGW-001.html"]').click();ck('THEME_DETAIL_URL',page.url,'http://127.0.0.1:8766/themes/tanigawa-sawa-db/records/SYN-TGW-001.html');snap('03_detail')
  page.go_back();ck('BROWSER_BACK_THEME',page.url,'http://127.0.0.1:8766/themes/tanigawa-sawa-db/index.html');snap('04_back')
  page.go_forward();ck('BROWSER_FORWARD_DETAIL',page.url,'http://127.0.0.1:8766/themes/tanigawa-sawa-db/records/SYN-TGW-001.html');snap('05_forward')
  page.goto('http://127.0.0.1:8766/tech-evidence/pagefind_japanese_browser_probe.html');page.locator('#run').click();page.wait_for_function("!document.querySelector('#save').disabled",timeout=30000)
  actual=json.loads(page.locator('#report').inner_text());(E/'japanese_search.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2));ck('PAGEFIND_JAPANESE_FAILURES',actual.get('summary',{}).get('FAIL'),0);snap('06_pagefind')
  canary=json.loads((R/'docs/SOURCE_PIN.json').read_text())['canary']
  canary_result=page.evaluate("async q=>{const pf=await import('/pagefind/pagefind.js');const r=await pf.search(q);return {query:q,count:r.results.length}}",'\"'+canary+'\"')
  (E/'canary_search.json').write_text(json.dumps(canary_result,indent=2));ck('CANARY_QUERY_ONLY_INFORMATIONAL',canary_result['count'],0)
  with page.expect_download() as dl:page.locator('#save').click()
  dl.value.save_as(E/'P3_B1_Pagefind_Japanese_Actual_Browser_Result.json')
  # Hard-coded cases derived from the frozen eight fixtures, including null exclusion and OR/AND.
  cases=[('ALL',{},['OKU-001','OKU-002','TGW-001','TGW-002','TNZ-001','TNZ-002','TNZ-003','TNZ-004']),('JAPANESE',{'q':'谷川'},['TGW-001','TGW-002']),('AREA_OR',{'areas':['tanigawa','okutama']},['OKU-001','OKU-002','TGW-001','TGW-002']),('MONTH_OR',{'months':['5','8']},['OKU-001','OKU-002','TGW-001','TNZ-001']),('AREA_MONTH_AND',{'areas':['tanigawa'],'months':['6']},['TGW-001']),('MAX_DAYS_NULL_EXCLUDED',{'days':'1'},['OKU-001','TGW-002','TNZ-003']),('SCHEME_X',{'scheme':'syn-scale-x'},['OKU-001','OKU-002','TGW-001','TNZ-003','TNZ-004']),('GRADE_OR',{'scheme':'syn-scale-x','grades':['X2','X3']},['OKU-001','OKU-002','TGW-001']),('ALL_CONDITIONS_AND',{'areas':['okutama'],'months':['6'],'scheme':'syn-scale-x','grades':['X2'],'days':'1','q':'奥多摩'},['OKU-001']),('NO_MATCH',{'q':'穂高岳'},[]),('MONTH_NULL_EXCLUDED',{'months':['3']},[])]
  timings={};seen={}
  for label,port in [('vanilla',8767),('astro',8766)]:
   page.goto(f'http://127.0.0.1:{port}/');page.wait_for_function("document.querySelector('#count').textContent==='8'")
   for name,f,w in cases:
    page.locator('#reset').click()
    if 'q' in f:page.locator('#keyword').fill(f['q'])
    if 'scheme' in f:page.locator('#grade-scheme').select_option(f['scheme'])
    if 'days' in f:page.locator('#max-days').select_option(f['days'])
    for key,selector in [('areas','area-labels'),('months','month-labels'),('grades','grade-labels')]:
     for val in f.get(key,[]):page.locator(f'#{selector} input[value="{val}"]').check()
    ids=page.locator('#results a').evaluate_all("els=>els.map(e=>e.href.match(/SYN-[A-Z]+-\\d+/)[0]).sort()")
    ck(label+'_'+name,ids,sorted('SYN-'+x for x in w));seen[label+'_'+name]=ids
   if label=='astro':snap('07_filters')
   # Fresh browser contexts, same loopback host, no throttling: navigation through initialized UI.
   rows=[]
   for i in range(10):
    cc=b.new_context();pp=cc.new_page();st=time.perf_counter();pp.goto(f'http://127.0.0.1:{port}/');pp.wait_for_function("document.querySelector('#count').textContent==='8'");elapsed=(time.perf_counter()-st)*1000
    rows.append({'wall_to_8_results_ms':elapsed,'navigation':pp.evaluate('performance.getEntriesByType("navigation")[0].toJSON()'),'resources':pp.evaluate('performance.getEntriesByType("resource").map(x=>({name:x.name,transferSize:x.transferSize,duration:x.duration}))')});cc.close()
   timings[label]={'runs':rows,'median_wall_to_8_results_ms':statistics.median(x['wall_to_8_results_ms'] for x in rows)}
  # Actual Pagefind query latency, includes retrieving every result fragment.
  page.goto('http://127.0.0.1:8766/tech-evidence/pagefind_japanese_browser_probe.html')
  pf=page.evaluate('''async()=>{const pf=await import('/pagefind/pagefind.js');await pf.init();let out=[];for(let i=0;i<21;i++){let t=performance.now();let r=await pf.search('谷川');await Promise.all(r.results.map(x=>x.data()));out.push({iteration:i,ms:performance.now()-t,count:r.results.length});}return out;}''')
  timings['pagefind_query']=pf
  timings['vanilla_query']=page.evaluate('''async()=>{const rows=(await (await fetch('/experimental_offline_search_index.json')).json()).records;let start=performance.now(),hits;for(let i=0;i<10000;i++)hits=rows.filter(x=>x.title.includes('谷川'));return {iterations:10000,total_ms:performance.now()-start,count:hits.length,note:'title-only substring, no result rendering'};}''')
  (E/'performance.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2));ck('PARITY_ALL_CASES',all(seen['vanilla_'+n]==seen['astro_'+n] for n,_,_ in cases),True)
  # Public server cannot retrieve members artifacts.
  for path in ['canary.html','members-index.json','members/canary.html']:
   res=page.request.get('http://127.0.0.1:8766/'+path);ck('PUBLIC_HTTP_'+path,res.status,404)
  ck('BROWSER_PAGE_ERRORS',report['page_errors'],[]);page.goto('http://127.0.0.1:8766/fixtures/synthetic_format.html');snap('08_html_fixture');c.close();b.close()
except Exception as exc:
 report['exception']=str(exc);ck('PROBE_COMPLETED',False,True);raise
finally:
 for s in servers:s.shutdown();s.server_close()
 report['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();report['summary']={s:sum(x['status']==s for x in report['checks']) for s in ['PASS','FAIL']};(E/'browser_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['summary']['FAIL']==0 else 2)
