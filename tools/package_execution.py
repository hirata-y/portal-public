#!/usr/bin/env python3
"""Package only the reviewable payload; manifest hashes every included payload file."""
import hashlib,json,zipfile,datetime,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'artifacts';A.mkdir(exist_ok=True)
exclude_dirs={'.git','node_modules','.astro','__pycache__','artifacts'}
exclude_files={'MANIFEST.json','PUBLICATION_RECEIPT.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in exclude_dirs for x in p.relative_to(R).parts) and p.name not in exclude_files and p.suffix!='.pyc')
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={'kind':'P3_B1_A_EXECUTION_SNAPSHOT_NOT_OFFICIAL_FREEZE','task_id':'P3-B1-REAL-VENDOR-POC-20261016-01','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'official_freeze':False,'G4':'STOP','input_zip_sha256':'a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9','exclusions':['.git','node_modules','.astro','__pycache__','artifacts/ (archive, checksum and Git bundle sidecars)','MANIFEST.json self hash','PUBLICATION_RECEIPT.json (external readback created after packaging)'],'files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
(R/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
archive=A/'P3_B1_A_EXECUTION_SNAPSHOT_20261015.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[R/'MANIFEST.json']:z.write(p,p.relative_to(R).as_posix())
digest=sha(archive.read_bytes());(A/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n')
# Re-open and check actual archived bytes, count, safe paths, dependency exclusions.
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for row in manifest['files']:assert sha(z.read(row['path']))==row['sha256']
 assert len(z.namelist())==len(files)+1
 assert not any(any(x in name.split('/') for x in exclude_dirs) for name in z.namelist())
print(json.dumps({'archive':str(archive),'sha256':digest,'bytes':archive.stat().st_size,'payload_files':len(files),'zip_entries':len(files)+1,'readback':'PASS','official_freeze':False},indent=2))
