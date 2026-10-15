import pathlib,json,hashlib,zipfile,gzip,datetime,shutil
R=pathlib.Path(__file__).resolve().parent.parent;O=R/'F_OUTPUT';checks=[]
def c(name,expected,actual):
 checks.append({'name':name,'expected':expected,'actual':actual,'pass':expected==actual})
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((R/'FREEZE1_MANIFEST.json').read_text());bad=[]
for f in m['files']:
 p=R/f['path']
 if not p.is_file() or p.stat().st_size!=f['bytes'] or sha(p.read_bytes())!=f['sha256']:bad.append(f['path'])
c('freeze_manifest_payload_count',398,len(m['files']));c('freeze_manifest_mismatches',[],bad)
c('lock_pinned','dd957c01dc054952d911b48cff783e62c500d83d5d06898d730fba46faac5117',sha((R/'astro_candidate/package-lock.json').read_bytes()))
z=zipfile.ZipFile(R/'source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip');prefix=z.namelist()[0].split('/')[0]+'/'
c('vendor_input_sha','a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9',sha((R/'source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip').read_bytes()))
sources=[n for n in z.namelist() if n.startswith(prefix+'source/p3_a_site/')];c('source16_count',16,len(sources));c('source16_mismatches',[],[n for n in sources if z.read(n)!=(R/n[len(prefix):]).read_bytes()])
parity=[n for n in z.namelist() if n.startswith(prefix+'astro_candidate/public/')];c('public_input_parity',[],[n for n in parity if z.read(n)!=(R/n[len(prefix):]).read_bytes()])
c('home_is_inline_scripts',3,(R/'astro_candidate/src/pages/index.astro').read_text().count('is:inline'))
D=R/'astro_candidate/dist';canary=json.loads((R/'docs/SOURCE_PIN.json').read_text())['canary'].encode()
def scan(root):
 hits=[]
 for p in root.rglob('*'):
  if not p.is_file():continue
  b=p.read_bytes()
  if b[:2]==b'\x1f\x8b':b=gzip.decompress(b)
  if canary in b or b'/members/' in b:hits.append(str(p.relative_to(root)))
 return sorted(hits)
c('clean_public_raw_and_decoded',[],scan(D))
fault=O/'mutation_raw';shutil.rmtree(fault,ignore_errors=True);fault.mkdir(exist_ok=True);(fault/'canary.html').write_bytes(canary);c('raw_mutation_detected',['canary.html'],scan(fault))
(fault/'canary.html').unlink();(fault/'compressed.pf_fragment').write_bytes(gzip.compress(b'pagefind_dcd'+json.dumps({'url':'/members/hidden.html','content':canary.decode()}).encode()));c('compressed_mutation_detected',['compressed.pf_fragment'],scan(fault))
frags=[]
for p in sorted((D/'pagefind/fragment').glob('*')):
 b=gzip.decompress(p.read_bytes());assert b.startswith(b'pagefind_dcd');frags.append(json.loads(b[12:]))
c('native_fragment_count',13,len(frags));c('native_fragment_private_routes',[],[f['url'] for f in frags if '/members/' in f['url']]);c('detailed_record_count',8,sum('/records/' in f['url'] for f in frags))
terms=json.loads((D/'search/ja-terms.json').read_text());c('lexicon_sources_hash',[],[s['path'] for s in terms['source_fragments'] if sha((D/s['path']).read_bytes())!=s['sha256']]);c('lexicon_public_fragment_count',13,len(terms['source_fragments']))
(O/'static_results.json').write_text(json.dumps({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'fragments':frags},ensure_ascii=False,indent=2));print(json.dumps({'pass':sum(x['pass'] for x in checks),'fail':[x for x in checks if not x['pass']]},ensure_ascii=False));assert all(x['pass'] for x in checks)
