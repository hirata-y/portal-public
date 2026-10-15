#!/usr/bin/env python3
import json,hashlib,collections,datetime,platform,subprocess,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'astro_candidate';E=R/'evidence/remediation_20261015';lock=json.loads((A/'package-lock.json').read_text());rows=[]
for name,item in lock['packages'].items():
 if not name:continue
 p=A/name;files=[{'path':str(f.relative_to(A)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(p.glob('*')) if f.is_file() and f.name.lower().startswith(('license','licence','copying','notice'))]
 rows.append({'path':name,'version':item.get('version'),'resolved':item.get('resolved'),'integrity':item.get('integrity'),'license':item.get('license'),'installed':p.is_dir(),'license_files':files})
z=R/'source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip'
report={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'A','lock_sha256':hashlib.sha256((A/'package-lock.json').read_bytes()).hexdigest(),'fixed_input_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'fixed_zip_crc':zipfile.ZipFile(z).testzip(),'os':platform.platform(),'tools':{k:subprocess.run(v,capture_output=True,text=True).stdout.strip() for k,v in {'node':['node','--version'],'npm':['npm','--version'],'python':['python','--version'],'browser':['chromium','--version']}.items()},'packages':rows,'license_counts':dict(collections.Counter(str(x['license']) for x in rows)),'missing_license_metadata':[x['path'] for x in rows if not x['license']],'limits':['Lockfile metadata and installed license-file presence checked; not legal approval or complete transitive binary/dictionary rights certification.','npm audit is point-in-time registry advisory lookup, not proof of absence of vulnerabilities.','Optional platform packages in lockfile can be absent on this Linux host.']}
(E/'dependency_inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:report[k] for k in ['tools','lock_sha256','fixed_input_sha256','fixed_zip_crc','license_counts','missing_license_metadata']},indent=2))
