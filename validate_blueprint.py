from pathlib import Path
import json
import re

ROOT = Path('/home/ubuntu/aspice_agent_blueprint')
expected_processes = [
    'ACQ.4','SPL.2','SYS.1','SYS.2','SYS.3','SYS.4','SYS.5',
    'SWE.1','SWE.2','SWE.3','SWE.4','SWE.5','SWE.6','VAL.1',
    'MLE.1','MLE.2','MLE.3','MLE.4','HWE.1','HWE.2','HWE.3','HWE.4',
    'SUP.1','SUP.8','SUP.9','SUP.10','SUP.11','MAN.3','MAN.5','MAN.6',
    'PIM.3','REU.2'
]
expected_managers = [f'M{i:02d}' for i in range(1, 15)]
required_files = [
    'README.md',
    'docs/agent_architecture.md',
    'docs/prompt_composition.md',
    'workflows/audit_workflow.md',
    'prompts/00_global_policy.md',
    'prompts/10_process_auditor_template.md',
    'prompts/20_manager_template.md',
    'prompts/30_control_agents_template.md',
    'profiles/process_agents.yaml',
    'profiles/manager_agents.yaml',
    'config/process_scope.yaml',
    'config/runtime_registry.yaml',
    'schemas/evidence_object.schema.json',
    'schemas/audit-finding.schema.json',
    'schemas/process-audit-result.schema.json',
    'schemas/manager-work-package.schema.json',
    'schemas/direct-spec-citation.schema.json',
    'knowledge/aspice40/process_rulepack_template.yaml',
    'knowledge/aspice40/HWE.2.yaml',
    'knowledge/aspice40/spec_citation_catalog.jsonl',
    'knowledge/aspice40/spec_citation_catalog.md',
    'examples/hwe2_audit_input.json',
    'examples/hwe2_audit_result_with_citations.json',
    'docs/direct_spec_citation_policy.md',
    'docs/cognitive_operating_layer_guide.md',
    'prompts/05_cognitive_operating_layer.md',
    'knowledge/cognitive/cognitive_modules.yaml',
    'config/agent_cognitive_assignments.json',
    'schemas/cognitive-module-assignment.schema.json',
    'schemas/cognitive-decision-record.schema.json'
]
missing = [p for p in required_files if not (ROOT / p).exists()]
process_text = (ROOT / 'profiles/process_agents.yaml').read_text(encoding='utf-8')
manager_text = (ROOT / 'profiles/manager_agents.yaml').read_text(encoding='utf-8')
process_ids = re.findall(r'^  - id: ([A-Z]{3}\.\d+)$', process_text, re.M)
manager_ids = re.findall(r'^  - id: (M\d+)$', manager_text, re.M)
all_ok = True
checks = {}
checks['required_files'] = {'expected': len(required_files), 'missing': missing, 'ok': not missing}
checks['process_ids'] = {'expected': expected_processes, 'actual': process_ids, 'count': len(process_ids), 'unique': len(set(process_ids)), 'ok': process_ids == expected_processes}
checks['manager_ids'] = {'expected': expected_managers, 'actual': manager_ids, 'count': len(manager_ids), 'unique': len(set(manager_ids)), 'ok': manager_ids == expected_managers}
checks['logical_agent_total'] = {'count': 8 + len(process_ids) + len(manager_ids), 'expected': 54, 'ok': 8 + len(process_ids) + len(manager_ids) == 54}
rulepack_dir = ROOT / 'knowledge/aspice40/process_rules'
rulepack_files = sorted(rulepack_dir.glob('*.yaml'))
rulepack_errors = []
rulepack_citation_counts = {}
for path in rulepack_files:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        citations = data.get('spec_citations', [])
        rulepack_citation_counts[path.stem] = len(citations)
        if not citations:
            rulepack_errors.append(f'{path.name}: no spec_citations')
        for idx, item in enumerate(citations):
            for field in ['verbatim_text', 'verbatim_text_sha256', 'source_anchor', 'why_this_text_applies', 'interpretation']:
                if not item.get(field):
                    rulepack_errors.append(f'{path.name}[{idx}]: missing {field}')
            if 'COPY FROM' in item.get('verbatim_text', '') or 'placeholder' in item.get('verbatim_text', '').lower():
                rulepack_errors.append(f'{path.name}[{idx}]: placeholder quote')
    except Exception as exc:
        rulepack_errors.append(f'{path.name}: invalid JSON-as-YAML: {exc}')
checks['process_rulepacks'] = {'expected': 32, 'actual': len(rulepack_files), 'citation_counts': rulepack_citation_counts, 'errors': rulepack_errors, 'ok': len(rulepack_files) == 32 and not rulepack_errors}
cognitive_errors = []
assignment_path = ROOT / 'config/agent_cognitive_assignments.json'
try:
    assignments = json.loads(assignment_path.read_text(encoding='utf-8'))
    assignment_ids = [item.get('agent_id') for item in assignments.get('assignments', [])]
    assignment_errors = []
    if assignments.get('assignment_count') != 54 or len(assignment_ids) != 54 or len(set(assignment_ids)) != 54:
        assignment_errors.append('assignment count or uniqueness mismatch')
    if assignments.get('normative_status') != 'non_normative_support_layer' or assignments.get('source_attribution_in_outputs') is not False:
        assignment_errors.append('missing non-normative or source-neutral marker')
    if any(not item.get('modules') for item in assignments.get('assignments', [])):
        assignment_errors.append('agent without modules')
    checks['cognitive_assignments'] = {'count': len(assignment_ids), 'errors': assignment_errors, 'ok': not assignment_errors}
except Exception as exc:
    checks['cognitive_assignments'] = {'errors': [str(exc)], 'ok': False}
module_text = (ROOT / 'knowledge/cognitive/cognitive_modules.yaml').read_text(encoding='utf-8')
module_ids = re.findall(r'^  - id: (COM-\d+)$', module_text, re.M)
checks['cognitive_modules'] = {'count': len(module_ids), 'ids': module_ids, 'ok': module_ids == [f'COM-{i:02d}' for i in range(1, 11)] and 'non_normative_support_layer' in module_text}
cognitive_prompt = (ROOT / 'prompts/05_cognitive_operating_layer.md').read_text(encoding='utf-8')
checks['cognitive_prompt'] = {'has_required_rules': all(term in cognitive_prompt for term in ['decision statement', '替代解釋', '人工 Gate', 'non_normative_support_layer']), 'ok': all(term in cognitive_prompt for term in ['decision statement', '替代解釋', '人工 Gate', 'non_normative_support_layer'])}
privacy_text = '\\n'.join([module_text, cognitive_prompt, (ROOT / 'docs/cognitive_operating_layer_guide.md').read_text(encoding='utf-8')])
forbidden_terms = ['你的思考', '個人習慣', '使用者思考', '個人資料庫', '思考決策資料庫']
checks['source_neutrality'] = {'forbidden_terms_found': [term for term in forbidden_terms if term in privacy_text], 'ok': not any(term in privacy_text for term in forbidden_terms)}
example_path = ROOT / 'examples/hwe2_audit_result_with_citations.json'
example = json.loads(example_path.read_text(encoding='utf-8'))
example_citations = example['checks'][0].get('spec_citations', [])
example_errors = []
for item in example_citations:
    if len(item.get('verbatim_text', '')) < 20 or '完整複製' in item.get('verbatim_text', ''):
        example_errors.append('example contains placeholder or too-short verbatim_text')
    if not item.get('verbatim_text_sha256'):
        example_errors.append('example citation missing hash')
checks['example_direct_citation'] = {'citation_count': len(example_citations), 'errors': example_errors, 'ok': bool(example_citations) and not example_errors}
json_schema_errors = []
for path in (ROOT / 'schemas').glob('*.json'):
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        json_schema_errors.append(f'{path.name}: {exc}')
checks['json_syntax'] = {'errors': json_schema_errors, 'ok': not json_schema_errors}
for value in checks.values():
    if not value['ok']:
        all_ok = False
print(json.dumps({'ok': all_ok, 'checks': checks}, ensure_ascii=False, indent=2))
raise SystemExit(0 if all_ok else 1)
