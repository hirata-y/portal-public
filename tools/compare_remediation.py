#!/usr/bin/env python3
import json,datetime,statistics,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'evidence/remediation_20261015';j=json.loads((E/'remediation_checks.json').read_text());p=json.loads((E/'browser/performance.json').read_text())
m={'measured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'same_host':'Linux Chromium154, loopback, no throttling, synthetic 8 records','home_median_ms':{k:p[k]['median_wall_to_8_results_ms'] for k in ['vanilla','astro']},'home_runs_each':10,'adapter_queries':[{'query':x['query'],'ms':x['ms'],'detail_count':len(x['actual'])} for x in j['rows']],'adapter_first_ms':j['rows'][0]['ms'],'adapter_remaining_median_ms':statistics.median(x['ms'] for x in j['rows'][1:]),'output_bytes':{name:sum(f.stat().st_size for f in (R/path).rglob('*') if f.is_file()) for name,path in [('vanilla','outputs/public'),('astro_pagefind_adapter','astro_candidate/dist')]},'build_seconds':json.loads((E/'17_final_build.json').read_text())['duration_seconds'],'index_seconds':json.loads((E/'18_final_index.json').read_text())['duration_seconds'],'limits':['One host, tiny synthetic corpus, no representative production throughput/memory/concurrency measurement.','Home UI same original filters; observed ~4ms difference does not establish a significant speed advantage.','Search adapter timing includes actual native result fragment retrieval; vanilla title substring microbenchmark not equivalent full-text work.']}
(E/'comparison_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));print(json.dumps(m,ensure_ascii=False,indent=2))
for name in ['astro','pagefind']:
 src=R/'astro_candidate/node_modules'/name
 for f in src.rglob('*') if name=='pagefind' else [src/'LICENSE']:
  if f.is_file() and any(part.startswith('LICENSE') for part in f.relative_to(src).parts):
   out=R/'docs/third-party'/name/f.relative_to(src);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,out)
