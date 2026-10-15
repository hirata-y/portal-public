import pathlib,json,hashlib,zipfile,datetime
R=pathlib.Path(__file__).resolve().parent;exclude={'npm-cache','rebuild'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not p.is_symlink() and not any(x in exclude for x in p.relative_to(R).parts) and p.name not in {'F_EVIDENCE_MANIFEST.json','PACKAGE_RECEIPT.json'})
m={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_sha256':'7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75','review':'one scoped independent F review','exclusions':['npm-cache/**','rebuild/**','F_EVIDENCE_MANIFEST.json self hash','PACKAGE_RECEIPT.json postpackage receipt'],'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
manifest=R/'F_EVIDENCE_MANIFEST.json';manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2));dest=R.parent/'P3_B1_FREEZE1_F_REVIEW_20261015.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[manifest]:z.write(p,'F_OUTPUT/'+str(p.relative_to(R)))
receipt={'zip':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'entries':len(files)+1,'payload_files':len(files),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for f in m['files']:
  b=z.read('F_OUTPUT/'+f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
(R/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(json.dumps(receipt))
