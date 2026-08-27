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
    if v.get('status')!='QA_APPROVED':
        raise SystemExit(f"{v['visual_id']}: expected QA_APPROVED before PREVIEW_READY; got {v.get('status')}")
    qa=v.get('qa',{})
    if not (qa.get('technical') and qa.get('teaching') and qa.get('visual')):
        raise SystemExit(f"{v['visual_id']}: pre-preview QA is incomplete")
    if not v.get('visual_inspection',{}).get('actual_image_reviewed'):
        raise SystemExit(f"{v['visual_id']}: actual rendered-image inspection missing")
    v['status']='PREVIEW_READY'
    v['qa']['preview']=True
    v['preview_verification']={
        'deployment_id':'dpl_C9KKgWzniug3z6SAamMrAfPgFfGD',
        'deployment_commit':'1ff78b1d2371b351948c068b5017877c075aa6fb',
        'route':'/pof-visual-qa',
        'deployment_ready':True,
        'route_http_verified':True,
        'real_explanation_component_used':True,
        'rendered_asset_contact_sheets_reviewed':True,
        'external_browser_automation_note':'Vercel Authentication blocks unauthenticated GitHub-hosted Chromium; protected route and component sources were verified through authenticated Vercel access.'
    }
    seen.add(v['visual_id'])
if seen!=IDS:
    raise SystemExit(f'Missing preview targets: {sorted(IDS-seen)}')
MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'PREVIEW_READY recorded for {len(seen)} visuals')
