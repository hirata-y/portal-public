#!/usr/bin/env python3
"""Producer executable acceptance spot for ACTUALLY BUILT Astro/Pagefind public dir.
No replacement for independent review. Standard Python library only.
Usage: python tools/verify_vendor_dist.py --dist astro_candidate/dist [--require-index]
"""
import argparse,json,hashlib,re,sys,zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--dist',default='astro_candidate/dist');ap.add_argument('--require-index',action='store_true');args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1]
DIST=(ROOT/args.dist).resolve() if not Path(args.dist).is_absolute() else Path(args.dist).resolve()
BASE=ROOT/'source/p3_a_site'; PRIVATE=ROOT/'outputs/members'; pin=json.loads((ROOT/'docs/SOURCE_PIN.json').read_text())
results=[]
def test(id,ok,expected=True,actual=None,notes=''):
 results.append({'id':id,'status':'PASS' if ok else 'FAIL','expected':expected,'actual':ok if actual is None else actual,'notes':notes});print(('PASS ' if ok else 'FAIL ')+id)
 return ok
if not DIST.is_dir():
 print(json.dumps({'status':'BLOCKED','reason':'Actual Astro dist does not exist. npm installation/build has not completed','dist':str(DIST)},ensure_ascii=False,indent=2));sys.exit(3)
files=[p for p in DIST.rglob('*') if p.is_file()]
test('ASTRO_DIST_FILES_PRESENT',len(files)>=16,actual=len(files))
for name in ['styles.css','app.js','data-validation.js','demo-data.js']:
 a=BASE/name;b=DIST/name
 test('BUNDLED_UNCHANGED_'+name,b.is_file() and a.read_bytes()==b.read_bytes(),notes='Static public assets expected copied exactly')
for r in ['index.html','themes/tanigawa-sawa-db/index.html','themes/okutama-sawa-db/index.html','themes/tanzawa-sawa-db/index.html']:
 test('HTML_ROUTE_'+r,(DIST/r).is_file())
records=list((DIST/'themes').glob('*/records/SYN-*.html'))
test('DETAIL_COUNT_EIGHT',len(records)==8,actual=len(records),expected=8)
for p in records:
 bs=p.read_text(encoding='utf-8');test('DETAIL_ID_'+p.stem,p.stem in bs and ('合成' in bs or '架空' in bs))
index=(DIST/'index.html').read_text(encoding='utf-8') if (DIST/'index.html').is_file() else ''
test('HOME_LANG_JA','lang="ja"' in index or "lang='ja'" in index)
test('HOME_A_HYBRID','調査成果' in index and '谷川連峰' in index and 'filter' in index)
canary=pin['canary'].encode('utf-8');priv=[p for p in PRIVATE.rglob('*') if p.is_file()]
test('PRIVATE_CANARY_IN_PRIVATE',any(canary in p.read_bytes() for p in priv))
test('CANARY_ABSENT_FROM_ASTRO_PUBLIC',all(canary not in p.read_bytes() for p in files))
test('PRIVATE_FILE_NAME_ABSENT',not any((DIST/n).exists() for n in ('canary.html','members-index.json')))
test('MEMBERS_NO_DIR_IN_PUBLIC',not (DIST/'members').exists())
# Revisit actual public copies, no positive private inclusion.
for p in BASE.rglob('*'):
 if not p.is_file() or p.name=='index.html':continue
 q=DIST/p.relative_to(BASE)
 test('P3A_STATIC_PARITY_'+str(p.relative_to(BASE)),q.is_file() and p.read_bytes()==q.read_bytes())
for ext in ('html','pdf','pptx','xlsx'):
 q=DIST/'fixtures'/('synthetic_format.'+ext);test('SYNTHETIC_FORMAT_'+ext,q.is_file() and q.stat().st_size>100)
pagefind_dir=DIST/'pagefind';pf_files=[p for p in pagefind_dir.rglob('*') if p.is_file()] if pagefind_dir.is_dir() else []
if args.require_index:
 test('PAGEFIND_ACTUAL_INDEX_EXISTS',(pagefind_dir/'pagefind.js').exists() and len(pf_files)>=3,actual={'files':len(pf_files),'required':True})
# Detect mutation with a real byte-oriented temp fixture, without changing dist
injected=(DIST/'index.html').read_bytes()+canary
test('MUTATION_CANARY_BYTE_SCAN_DETECTS_INJECTION',canary in injected)
summary={'status':'COMPLETE' if all(x['status']=='PASS' for x in results) else 'FAIL','total':len(results),'PASS':sum(x['status']=='PASS' for x in results),'FAIL':sum(x['status']=='FAIL' for x in results),'required_pagefind':args.require_index,'pagefind_actual_status':'TO_BE_CHECKED_AFTER_VENDOR_BUILD' if not args.require_index else ('INDEX_FOUND' if (pagefind_dir/'pagefind.js').exists() else 'MISSING'),'dist':str(DIST),'dist_total_bytes':sum(p.stat().st_size for p in files),'pagefind_file_count':len(pf_files),'source_p3_a_sha256':pin.get('source_p3a_zip_sha256'),'notes':['This is a Producer check, not independent F verification.','Japanese query accuracy and native browser URL/Back require browser probe evidence.']}
output=ROOT/'evidence/vendor_real_dist_checks.json';output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps({'summary':summary,'checks':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2));sys.exit(0 if summary['FAIL']==0 else 2)
