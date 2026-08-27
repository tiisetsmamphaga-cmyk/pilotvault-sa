#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'data/pof-visual-manifest.json').read_text(encoding='utf-8'))
owners = defaultdict(list)
for v in data.get('visuals', []):
    for qid in v.get('question_ids', []):
        owners[qid].append((v.get('visual_id'), v.get('status'), v.get('assets', {}).get('web_asset')))

dup = {qid: rows for qid, rows in owners.items() if len(rows) > 1}
print(f'visual_count={len(data.get("visuals", []))}')
print(f'unique_question_count={len(owners)}')
print(f'duplicate_question_count={len(dup)}')
for qid, rows in sorted(dup.items()):
    print(f'QUESTION {qid}')
    for visual_id, status, web_asset in rows:
        print(f'  {visual_id} | {status} | {web_asset}')
