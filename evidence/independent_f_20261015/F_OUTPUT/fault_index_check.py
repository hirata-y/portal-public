import pathlib,shutil,subprocess,json,gzip,hashlib,datetime,threading,http.server,functools,asyncio,re,os
from playwright.async_api import async_playwright
R=pathlib.Path(__file__).resolve().parent.parent;O=R/'F_OUTPUT';D=R/'astro_candidate/dist';F=O/'fault_site';shutil.copytree(D,F,dirs_exist_ok=True);shutil.rmtree(F/'pagefind');shutil.rmtree(F/'tech-evidence');(F/'members').mkdir(exist_ok=True)
canary=json.loads((R/'docs/SOURCE_PIN.json').read_text())['canary'];(F/'members'/'f-private.html').write_text('<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>F限定混入</title></head><body><p>'+canary+'</p></body></html>')
cmd=['node',str(R/'astro_candidate/node_modules/pagefind/lib/runner/bin.cjs'),'--site',str(F),'--force-language','ja'];p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(O/'fault_index_build.log').write_bytes(p.stdout);(O/'fault_index_build.command.json').write_text(json.dumps({'command':cmd,'cwd':str(R),'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2));assert p.returncode==0
checks=[]
def c(name,exp,act):checks.append({'name':name,'expected':exp,'actual':act,'pass':exp==act})
def scan(root):
 result=[]
 for f in root.rglob('*'):
  if not f.is_file():continue
  raw=f.read_bytes();dec=gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw
  text=dec.decode('utf-8',errors='replace');clean=re.sub(r'[\s\u200b]','',text).casefold()
  reasons=[]
  if canary.encode() in raw:reasons.append('raw-canary')
  if canary.casefold() in clean:reasons.append('decoded-normalized-canary')
  if '/members/' in text:reasons.append('private-route')
  if reasons:result.append({'path':str(f.relative_to(root)),'reasons':reasons,'decoded':text[:700] if f.suffix=='.pf_fragment' else None})
 return result
clean=scan(D);fault=scan(F);c('normal_scan_clean',[],clean);c('fault_index_fragment_detected',True,any(x['path'].startswith('pagefind/fragment/') for x in fault));c('fault_index_private_route_detected',True,any('private-route' in x['reasons'] and x['path'].startswith('pagefind/') for x in fault))
# The index-derived lexicon must refuse a private input fragment.
code="import {createLexicon} from './tools/create_ja_lexicon.mjs'; createLexicon(process.argv[1]);"
cmd2=['node','--input-type=module','-e',code,str(F)];lp=subprocess.run(cmd2,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(O/'fault_lexicon.log').write_bytes(lp.stdout);c('lexicon_rejects_private_fragment',True,lp.returncode!=0)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(F)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
async def probe():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'],headless=True)
  page=await b.new_page();await page.goto(base+'/search/')
  native=[]
  for q in [canary,'"'+canary+'"','F限定混入']:
   result=await page.evaluate('''async q=>{const m=await import('/pagefind/pagefind.js');const r=await m.search(q);return {query:q,data:await Promise.all(r.results.map(x=>x.data()))}}''',q);native.append(result)
  await b.close();return native
native=asyncio.run(probe());s.shutdown();c('actual_native_index_private_route_searchable',True,any('/members/' in d['url'] for n in native for d in n['data']))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'normal_scan':clean,'fault_scan':fault,'native_results':native,'lexicon_command':cmd2,'lexicon_exit':lp.returncode};(O/'fault_index_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'pass':sum(x['pass'] for x in checks),'fail':[x for x in checks if not x['pass']]},ensure_ascii=False));assert all(x['pass'] for x in checks)
