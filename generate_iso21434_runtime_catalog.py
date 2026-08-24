from pathlib import Path
import argparse
import hashlib
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()

source_path = Path(args.source)
text = source_path.read_text(encoding='utf-8', errors='replace')
lines = text.splitlines()
records = []
current_clause = None
current_subclause = None
for idx, raw in enumerate(lines, 1):
    line = raw.strip()
    clause_match = re.match(r'^(?:Clause\s+)?(1[0-5]|[1-9])\s+(.+)$', line)
    if clause_match and not line.startswith('['):
        current_clause = clause_match.group(1)
        current_subclause = None
    sub_match = re.match(r'^((?:1[0-5]|[1-9])\.\d+(?:\.\d+)?)\s+(.+)$', line)
    if sub_match:
        current_subclause = sub_match.group(1)
    provision = re.match(r'^\[((?:RQ|RC|PM|WP)-\d{2}-\d{2})\]\s*(.*)$', line, re.I)
    if not provision:
        continue
    provision_id, first_text = provision.group(1), provision.group(2)
    provision_type = {'RQ': 'requirement', 'RC': 'recommendation', 'PM': 'permission', 'WP': 'work_product'}[provision_id[:2].upper()]
    quote_lines = [line]
    for follow in lines[idx:]:
        stripped = follow.strip()
        if not stripped:
            if len(quote_lines) > 1:
                break
            continue
        if re.match(r'^\[(?:RQ|RC|PM|WP)-\d{2}-\d{2}\]', stripped, re.I):
            break
        if re.match(r'^(?:[1-9]|1[0-5])(?:\.\d+){0,2}\s+', stripped):
            break
        if stripped.startswith('Licensed to ') or stripped.startswith('ISO Store Order:') or stripped.startswith('Single user licence'):
            break
        quote_lines.append(stripped)
    verbatim = ' '.join(quote_lines)
    records.append({
        'standard_id': 'ISO21434',
        'edition': 'ISO/SAE 21434:2021(E)',
        'clause': current_clause or 'unknown',
        'subclause': current_subclause,
        'provision_id': provision_id,
        'provision_type': provision_type,
        'verbatim_text': verbatim,
        'source_anchor': f'{source_path.name}:line-{idx}',
        'source_page_or_line': f'line-{idx}',
        'verbatim_text_sha256': hashlib.sha256(verbatim.encode('utf-8')).hexdigest(),
        'why_this_text_applies': 'Runtime record requires Agent-specific applicability to be supplied from the assigned profile and project Scope.',
        'interpretation': 'Runtime record requires Agent-specific interpretation to be supplied separately and must not be confused with the verbatim quotation.',
        'human_verification_status': 'pending',
    })
output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open('w', encoding='utf-8') as handle:
    for record in records:
        handle.write(json.dumps(record, ensure_ascii=False) + '\n')
print(json.dumps({'source': str(source_path), 'output': str(output_path), 'records': len(records)}, ensure_ascii=False))
