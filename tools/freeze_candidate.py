#!/usr/bin/env python3
"""One normal official Freeze. Never overwrite an archive or its manifest."""
import json,hashlib,zipfile,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=R/'artifacts/P3_B1_CANDIDATE_v0.3.0_20261015_FREEZE1.zip';manifest=R/'FREEZE1_MANIFEST.json'
assert not out.exists() and not manifest.exists(),'Freeze already exists; require an explicit finding-scoped new version, never overwrite'
for name,want in [('dist_checks.json',42),('security_formats.json',25),('browser/browser_report.json',33),('remediation_checks.json',62),('adapter_negative.json',3)]:
 j=json.loads((R/'evidence/remediation_20261015'/name).read_text());assert j['summary']['PASS']==want and j['summary']['FAIL']==0,name
assert json.loads((R/'evidence/remediation_20261015/index_fault_injection.json').read_text())['status']=='PASS'
exclude={'.git','node_modules','.astro','__pycache__','artifacts'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(part in exclude for part in p.relative_to(R).parts) and p.suffix!='.pyc')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m={'kind':'P3_B1_OFFICIAL_CANDIDATE','version':'0.3.0','normal_freeze_number':1,'task_id':'P3-B1-REMEDIATION-20261015-01','created_jst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),'official_freeze':True,'independent_F':'NOT_YET_STARTED','owner_acceptance':'PENDING','G4':'STOP','input_zip_sha256':'a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9','lock_sha256':sha(R/'astro_candidate/package-lock.json'),'historical_manifest_notice':'MANIFEST.json and management/STATUS_MANIFEST.json describe earlier immutable versions; FREEZE1_MANIFEST.json is the manifest for this candidate.','exclusions':sorted(exclude)+['.pyc','FREEZE1_MANIFEST.json self hash'],'files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[manifest]:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for row in m['files']:assert len(z.read(row['path']))==row['bytes'] and hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
 assert len(z.namelist())==len(m['files'])+1
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
digest=sha(out);out.with_suffix('.zip.sha256').write_text(digest+'  '+out.name+'\n')
receipt={'created_jst':m['created_jst'],'archive':str(out),'sha256':digest,'bytes':out.stat().st_size,'payload_files':len(files),'entries':len(files)+1,'archive_readback':'PASS','official_freeze':True,'normal_freeze_number':1}
(R/'evidence/remediation_20261015/FREEZE_RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
