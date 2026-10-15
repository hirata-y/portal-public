import tempfile,subprocess,gzip,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
variants=['<p>奥多摩</p>','<dl><dt>山域</dt><dd> 奥多摩 </dd></dl>','<dl><dt>山域</dt><dd>奥多摩</dd></dl>','<p>山域：奥多摩</p>','<p>山域 奥多摩</p>','<p>奥多摩（okutama）</p>','<p>奥多摩。架空奥多摩A</p>','<p>奥多摩\u200b</p>']
with tempfile.TemporaryDirectory() as t:
 p=Path(t)
 for i,s in enumerate(variants):(p/(str(i)+'.html')).write_text('<html lang="ja"><title>Case '+str(i)+'</title><body>'+s+'</body></html>')
 x=subprocess.run([str(R/'astro_candidate/node_modules/.bin/pagefind'),'--site',t,'--force-language','ja'],capture_output=True,text=True);out=[]
 for f in (p/'pagefind/fragment').glob('*'):
  j=json.loads(gzip.decompress(f.read_bytes())[len(b'pagefind_dcd'):]);i=int(j['url'].strip('/').split('.')[0]);out.append({'html':variants[i],'fragment':j})
 (R/'evidence/vendor_actual/segmentation_probe.json').write_text(json.dumps({'exit':x.returncode,'stdout':x.stdout,'stderr':x.stderr,'variants':out},ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
