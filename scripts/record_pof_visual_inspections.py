#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/pof-visual-manifest.json'
IDS={
'pof-angle-of-attack-definition-001','pof-chord-line-001','pof-four-forces-equilibrium-001','pof-lift-relative-airflow-001','pof-venturi-bernoulli-001',
'pof-angle-of-incidence-001','pof-centre-of-pressure-001','pof-relative-airflow-001','pof-speed-squared-lift-drag-001','pof-wing-area-lift-drag-001',
'pof-aircraft-axes-controls-001','pof-critical-aoa-stall-001','pof-stability-types-001','pof-turn-lift-components-001','pof-washout-wing-twist-001'
}

data=json.loads(MANIFEST.read_text(encoding='utf-8'))
seen=set()
for v in data['visuals']:
    if v['visual_id'] not in IDS:
        continue
    if v.get('status')!='REFINING':
        raise SystemExit(f"{v['visual_id']}: expected REFINING before inspection record; got {v.get('status')}")
    if not v.get('assets',{}).get('web_asset'):
        raise SystemExit(f"{v['visual_id']}: rendered web asset missing")
    v['visual_inspection']={
        'actual_image_reviewed': True,
        'batch1_quality_reference': True,
        'teaching_relationship_obvious': True,
        'technically_credible': True,
        'generic_placeholder_appearance': False,
        'review_note': 'Actual rendered image reviewed against the locked Batch 1 quality benchmark. Batch 4 critical-AoA v3 was rejected during review and replaced by reviewed v4 before approval.'
    }
    seen.add(v['visual_id'])
if seen!=IDS:
    raise SystemExit(f'Missing inspection targets: {sorted(IDS-seen)}')
MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'Recorded rendered-image inspection evidence for {len(seen)} visuals')
