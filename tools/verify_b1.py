#!/usr/bin/env python3
"""Producer self-check only, not an independent F review or G4 gate."""
import json, zipfile, io, hashlib, shutil, tempfile, sys, subprocess, time, platform, os, http.server, threading, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BAS=ROOT/'source/p3_a_site';PUB=ROOT/'outputs/public';PRIV=ROOT/'outputs/members'; ASTRO=ROOT/'astro_candidate';FS=PUB/'fixtures'
checks=[]
def check(test, condition, actual=None, expected=True, note=''):
 ok=bool(condition);checks.append({'id':test,'status':'PASS' if ok else 'FAIL','expected':expected,'actual':actual if actual is not None else bool(condition),'note':note})
 if not ok:print('FAIL',test,actual,expected,file=sys.stderr)
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=json.loads((ROOT/'docs/SOURCE_PIN.json').read_text())
check('SOURCE_P3A_SHA_PIN',source['source_p3a_zip_sha256']=='bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23')
check('SOURCE_P2_SHA_PIN',source['source_p2_full_sha256']=='c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f')
original=[p for p in BAS.rglob('*') if p.is_file()]
check('SOURCE_16_MEMBER_COUNT',len(original)==16,actual=len(original),expected=16)
for p in original:
 rel=p.relative_to(BAS);check('PUBLIC_UNCHANGED_'+str(rel), (PUB/rel).exists() and SHA(p)==SHA(PUB/rel),note='byte-identical P3-A fixed source')
check('PUBLIC_8_RECORDS',len(json.loads((PUB/'experimental_offline_search_index.json').read_text())['records'])==8)
check('PUBLIC_3_THEMES',len(list((PUB/'themes').glob('*/index.html')))==3)
check('PUBLIC_8_DETAIL_PAGES',len(list((PUB/'themes').glob('*/records/*.html')))==8)
rec=json.loads((PUB/'experimental_offline_search_index.json').read_text())['records'];recids={r['record_id'] for r in rec}
check('EIGHT_UNIQUE_SOURCE_IDS',len(recids)==8)
check('SOURCE_NO_REAL_PERSONAL_DATA',all(r['record_id'].startswith('SYN-') and r['title'].startswith('架空') for r in rec))
check('DETAIL_FILE_EXISTENCE',all((PUB/r['detail_path']).is_file() for r in rec))
check('DETAIL_NO_TRAVERSAL',all('..' not in Path(r['detail_path']).parts and not Path(r['detail_path']).is_absolute() for r in rec))
# Japanese partial query baseline only; NOT Pagefind results
def search(query):return sorted(r['record_id'] for r in rec if query.casefold() in r['title'].casefold())
for name,q,expected in [('TANIGAWA','谷川',['SYN-TGW-001','SYN-TGW-002']),('OKUTAMA','奥多摩',['SYN-OKU-001','SYN-OKU-002']),('TOKYO','東京',[]),('NONMATCH','穂高岳',[])]:
 val=search(q);check('BASELINE_LOCAL_SUBSTR_'+name,val==expected,actual=val,expected=expected,note='B1 baseline local substring demonstration, not actual Pagefind')
check('BASELINE_SEARCH_EMPTY',not search('zzzz_no_match_20261015'))
# synthetic canary segregation on artifact bytes
canary=source['canary'];all_public=[p for p in PUB.rglob('*') if p.is_file()]
all_private=[p for p in PRIV.rglob('*') if p.is_file()]
check('PUBLIC_CANARY_NOT_IN_FILE_BYTES',all(canary.encode() not in p.read_bytes() for p in all_public))
check('PRIVATE_CANARY_EXISTS',any(canary.encode() in p.read_bytes() for p in all_private))
check('PUBLIC_OUTPUT_NOT_PRIVATE_INDEX',not (PUB/'members-index.json').exists())
check('PRIVATE_OUTPUT_NOT_PUBLIC_INDEX',not (PRIV/'experimental_offline_search_index.json').exists())
check('PUBLIC_NO_REFERENCES_TO_MEMBERS',not any(b'members-index.json' in p.read_bytes() or b'MEM-CANARY-001' in p.read_bytes() for p in all_public))
check('PUBLIC_MISSING_PRIVATE_HTML',not (PUB/'canary.html').exists())
# mutation tests: fixtures intentionally injected only in tempfile, not a changed public output
with tempfile.TemporaryDirectory() as td:
 newp=Path(td)/'unsafe.txt';newp.write_text('ACCIDENT: '+canary)
 detection=any(canary.encode() in p.read_bytes() for p in [newp])
 check('MUTATION_CANARY_IN_PUBLIC_DETECTED',detection)
 copy=Path(td)/'index.json';copy.write_text(json.dumps({'records':rec+[rec[0]]},ensure_ascii=False))
 crec=json.loads(copy.read_text())['records']; check('MUTATION_DUPLICATE_RECORD_ID_DETECTED',len({r['record_id'] for r in crec})!=len(crec))
 check('MUTATION_TRAVERSAL_REF_DETECTED','..' in Path('../members/canary.html').parts)
# File syntax and specimen checks
for ext in ['html','pdf','pptx','xlsx']:
 p=FS/f'synthetic_format.{ext}';check(f'SYNTHETIC_{ext.upper()}_EXISTS',p.exists() and p.stat().st_size>100)
check('PDF_PARSE_AND_TEXT',__import__('fitz').open(FS/'synthetic_format.pdf').page_count==1)
with zipfile.ZipFile(FS/'synthetic_format.pptx') as z:check('PPTX_VALID_OFFICE_ZIP',z.testzip() is None and '[Content_Types].xml' in z.namelist())
with zipfile.ZipFile(FS/'synthetic_format.xlsx') as z:check('XLSX_VALID_OFFICE_ZIP',z.testzip() is None and '[Content_Types].xml' in z.namelist())
check('ASTRO_TEMPLATE_CREATED',(ASTRO/'src/pages/index.astro').exists())
check('ASTRO_TEMPLATE_CONTROLLED_INLINE_DERIVATIVE',(ASTRO/'src/pages/index.astro').read_text()==(BAS/'index.html').read_text().replace('<script src=','<script is:inline src='))
check('ASTRO_PACKAGE_JSON_VALID',bool(json.loads((ASTRO/'package.json').read_text())['scripts']['build']))
check('READINESS_HISTORICAL_NPM_ERROR_RETAINED','EAI_AGAIN' in (ROOT/'evidence/npm_resolution.txt').read_text())
# Test actual loopback public static HTTP with controlled shutdown; user auth not tested
from functools import partial
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(PUB)))
th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
try:
 for path in ['index.html','themes/tanigawa-sawa-db/index.html','themes/tanigawa-sawa-db/records/SYN-TGW-001.html','experimental_offline_search_index.json','fixtures/synthetic_format.pdf','fixtures/synthetic_format.pptx','fixtures/synthetic_format.xlsx']:
  with urllib.request.urlopen(f'http://127.0.0.1:{srv.server_port}/{path}',timeout=4) as resp:
   a=resp.read();check('LOOPBACK_GET_'+path,resp.status==200 and a==(PUB/path).read_bytes(),actual=[resp.status,len(a)])
 try:
  urllib.request.urlopen(f'http://127.0.0.1:{srv.server_port}/canary.html',timeout=4);blocked=False
 except urllib.error.HTTPError as e:blocked=e.code==404
 check('LOOPBACK_PRIVATE_ASSET_NOT_FOUND',blocked)
finally:srv.shutdown();srv.server_close();th.join(timeout=2)
# not claiming Pagefind or Astro actual CLI executed
summary={'total':len(checks),'PASS':sum(x['status']=='PASS' for x in checks),'FAIL':sum(x['status']=='FAIL' for x in checks),'NOT_COVERED_BY_THIS_BASELINE_SUITE':['ASTRO_REAL_BUILD','PAGEFIND_EXTENDED_JAPANESE_INDEX','PAGEFIND_SEARCH_QUERY','CHROMIUM_NATIVE_HTTP_NAVIGATION','CLOUDFLARE_ACCESS_JWT','WORKERS_RANGE_304_REAL_DELIVERY','FULL_WCAG_AND_AT','PRODUCTION_DEPENDENCY_AUDIT']}
# measure baseline on tiny sample; no vendor comparison
loops=10000;st=time.perf_counter()
for i in range(loops):search('谷川')
sec=time.perf_counter()-st
summary['benchmark']={'name':'Python baseline title substring only','iterations':loops,'total_seconds':sec,'avg_milliseconds':sec/loops*1000,'NOT_A_PAGEFIND_BENCHMARK':True}
summary['bytes']={'p3a_original_site':sum(p.stat().st_size for p in BAS.rglob('*') if p.is_file()),'b1_public_including_synthetic_formats':sum(p.stat().st_size for p in all_public),'b1_members_synthetic_canary':sum(p.stat().st_size for p in all_private),'astro_candidate_source_only':sum(p.stat().st_size for p in ASTRO.rglob('*') if p.is_file() and not any(x in p.parts for x in ('node_modules','.astro','dist')))}
(ROOT/'evidence/test_expected_actual.json').write_text(json.dumps({'summary':summary,'checks':checks},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2));sys.exit(0 if summary['FAIL']==0 else 2)
