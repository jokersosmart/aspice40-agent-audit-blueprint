import json
from pathlib import Path

path = Path('/home/ubuntu/aspice_agent_blueprint/docs/combined_blueprint_validation.json')
data = json.loads(path.read_text(encoding='utf-8'))
keys = [
    'required_files',
    'logical_agent_total',
    'manager_ids',
    'safety_agent_ids',
    'cognitive_assignments',
    'iso26262_public_source_boundary',
    'json_syntax',
]
summary = {key: data['checks'][key] for key in keys}
print(json.dumps({'ok': data['ok'], 'summary': summary}, ensure_ascii=False, indent=2))
raise SystemExit(0 if data['ok'] else 1)
