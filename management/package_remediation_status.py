#!/usr/bin/env python3
"""Management snapshot after F, distinct from the official Candidate Freeze."""
from pathlib import Path
import json,hashlib,zipfile,datetime
R=Path(__file__).resolve().parents[1];F='evidence/independent_f_20261015/F_OUTPUT/'
names=['PROJECT_STATUS.md','ROADMAP_STATUS.md','TASK_REGISTER.md','FINDINGS_REGISTER.md','DECISION_LOG.md','EVIDENCE_INDEX.md','management/P3_B1_REMEDIATION_PROGRESS_REPORT_20261015.md','management/P3_B1_FINAL_EXECUTION_HANDOFF.md','management/NEXT_OWNER_DECISIONS.md','management/F_REVIEW_TASK_ORDER.md','management/package_remediation_status.py','management/evidence/current_markdown_readbacks.json','management/evidence/remediation_acceptance_current.json','management/evidence/post_freeze_scope.json','management/evidence/progress_entry_remediation.json','evidence/remediation_20261015/FREEZE_RECEIPT.json','FREEZE1_MANIFEST.json',F+'REVIEW.md',F+'SUMMARY.json','artifacts/P3_B1_CANDIDATE_v0.3.0_20261015_FREEZE1.zip.sha256','artifacts/P3_B1_FREEZE1_F_REVIEW_20261015.zip.sha256']
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={'kind':'POST_F_MANAGEMENT_SNAPSHOT_NOT_ANOTHER_CANDIDATE_FREEZE','version':'1.1.0','created_jst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),'normal_candidate_freeze_count':1,'normal_independent_F_count':1,'F_verdict':'PASS_WITH_MINOR','owner_acceptance':'PENDING','github_new_payload':'BLOCKED_AUTO_REVIEW','G4':'STOP','exclusions':['REMEDIATION_PUBLICATION_RECEIPT.json: created/updated after packaging for raw readback and public approval','this manifest self hash','node_modules/npm caches','Candidate and F binary ZIPs delivered separately and identified by SHA sidecars'],'files':[{'path':n,'bytes':(R/n).stat().st_size,'sha256':sha((R/n).read_bytes())} for n in names]}
mp=R/'management/REMEDIATION_STATUS_MANIFEST.json';out=R/'artifacts/P3_B1_REMEDIATION_STATUS_20261015_v1.1.0.zip';assert not out.exists() and not mp.exists(),'Do not overwrite previous snapshot';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names+['management/REMEDIATION_STATUS_MANIFEST.json']:z.write(R/n,n)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for row in manifest['files']:assert sha(z.read(row['path']))==row['sha256'] and len(z.read(row['path']))==row['bytes']
digest=sha(out.read_bytes());out.with_suffix('.zip.sha256').write_text(digest+'  '+out.name+'\n');j={'archive':str(out),'sha256':digest,'bytes':out.stat().st_size,'entries':len(names)+1,'payload_files':len(names),'archive_readback':'PASS'};print(json.dumps(j,indent=2));p=R/'management/REMEDIATION_PUBLICATION_RECEIPT.json';r=json.loads(p.read_text());r['management_snapshot']=j;p.write_text(json.dumps(r,ensure_ascii=False,indent=2))
