#!/usr/bin/env python3
"""Prepare immutable-source derivatives with explicit Japanese area display names."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[2];B=R/'source/p3_a_site';P=R/'astro_candidate/public'
labels={'tanigawa':'谷川連峰','okutama':'奥多摩','tanzawa':'丹沢'}
rows=json.loads((P/'experimental_offline_search_index.json').read_text())['records']
for row in rows:
 rel=row['detail_path'];s=(B/rel).read_text();old='<dt>山域</dt><dd>'+row['area_key']+'</dd>';new='<dt>山域</dt><dd>'+labels[row['area_key']]+' <span>('+row['area_key']+')</span></dd>'
 if s.count(old)!=1:raise ValueError(rel+' missing exact area field')
 (P/rel).write_text(s.replace(old,new))
print('Prepared 8 derived detail pages. Fixed source unchanged; all record values retained.')
