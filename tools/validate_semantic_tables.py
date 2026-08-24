#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'knowledge' / 'semantic_tables'
STANDARD_FILES = ['aspice40_tables.json', 'iso26262_part5_tables.json', 'iso21434_tables.json']
SYMBOLS = {'X', '+', '++', 'o', '—', '―', '---', 'I1', 'I2', 'I3', 'T1', 'T2'}
errors = []
summary = {}

for filename in STANDARD_FILES:
    path = ROOT / filename
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{filename}: invalid JSON: {exc}')
        continue
    tables = payload.get('tables', [])
    if not tables:
        errors.append(f'{filename}: no table objects')
    for t in tables:
        tid = t.get('table_id', '?')
        cols = t.get('columns', [])
        if len(cols) < 2:
            errors.append(f'{filename}:{tid}: table has no contextual columns')
        if not t.get('source_anchor'):
            errors.append(f'{filename}:{tid}: missing source anchor')
        for row_idx, row in enumerate(t.get('rows', [])):
            if set(row) != set(cols):
                errors.append(f'{filename}:{tid}: row {row_idx} does not match table columns')
            for col, value in row.items():
                if str(value) in SYMBOLS and len(cols) < 2:
                    errors.append(f'{filename}:{tid}: isolated symbol {value}')
        joined = json.dumps(t, ensure_ascii=False)
        if '5. Process capability levels and process attributes' in joined:
            errors.append(f'{filename}:{tid}: chapter-boundary contamination')
    summary[filename] = len(tables)

try:
    semantic_summary = json.loads((ROOT / 'table_semantic_repair_summary.json').read_text(encoding='utf-8'))
    if semantic_summary.get('standalone_symbol_count_in_rendered_rows') != 0:
        errors.append('summary: standalone symbols remain')
    if semantic_summary.get('table_count') != sum(summary.values()):
        errors.append('summary: table count mismatch')
except Exception as exc:
    errors.append(f'summary invalid: {exc}')

try:
    queue = json.loads((ROOT / 'manual_review_queue.json').read_text(encoding='utf-8'))
    if not isinstance(queue, list):
        errors.append('manual_review_queue: not a list')
    for item in queue:
        if item.get('auto_fill_prohibited') is not True or item.get('original_source_is_authoritative') is not True:
            errors.append(f'manual_review_queue:{item.get("table_id", "?")}: unsafe review flags')
except Exception as exc:
    errors.append(f'manual_review_queue invalid: {exc}')

result = {'ok': not errors, 'table_counts': summary, 'total_tables': sum(summary.values()), 'errors': errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if not errors else 1)
