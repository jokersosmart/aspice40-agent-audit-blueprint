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
expected_managers = [f'M{i:02d}' for i in range(1, 21)]
expected_cybersecurity_agents = [f'CS{i:02d}' for i in range(1, 16)]
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
    'docs/iso26262_part5_agent_architecture.md',
    'docs/iso21434_agent_architecture.md',
    'docs/iso21434_integration_report.md',
    'docs/runtime_token_citation_architecture.md',
    'workflows/runtime_token_citation_sop.md',
    'workflows/example_three_standard_runtime_dag.yaml',
    'tools/runtime_context_builder.py',
    'tools/citation_validator.py',
    'tools/validate_semantic_tables.py',
    'tools/generate_semantic_tables.py',
    'tools/semantic_table_runtime_demo.py',
    'examples/hwe2_runtime_citations_demo.jsonl',
    'docs/semantic_table_runtime_demo.md',
    'docs/semantic_table_runtime_demo_output.json',
    'docs/semantic_table_runtime_demo_blocked_output.json',
    'docs/semantic_table_repair_validation.json',
    'docs/external_references.md',
    'config/standards_registry.yaml',
    'config/iso26262_part5_scope.yaml',
    'profiles/iso26262_safety_agents.yaml',
    'prompts/40_iso26262_safety_auditor_template.md',
    'prompts/41_iso26262_safety_manager_template.md',
    'knowledge/iso26262/README.md',
    'knowledge/iso26262/part5_rulepack_template.yaml',
    'generate_iso26262_part5_runtime_catalog.py',
    'schemas/safety-finding.schema.json',
    'schemas/cross-standard-mapping.schema.json',
    'schemas/triple-standard-mapping.schema.json',
    'schemas/runtime-execution-envelope.schema.json',
    'schemas/citation-verification-result.schema.json',
    'schemas/shared-state-snapshot.schema.json',
    'schemas/runtime-observation.schema.json',
    'examples/iso26262_part5_audit_input.json',
    'examples/aspice_iso26262_crosswalk_example.json',
    'prompts/05_cognitive_operating_layer.md',
    'knowledge/cognitive/cognitive_modules.yaml',
    'config/agent_cognitive_assignments.json',
    'schemas/cognitive-module-assignment.schema.json',
    'schemas/cognitive-decision-record.schema.json',
    'config/iso21434_scope.yaml',
    'config/token_budget_policy.yaml',
    'config/runtime_dispatch_policy.yaml',
    'profiles/iso21434_cybersecurity_agents.yaml',
    'prompts/42_iso21434_cybersecurity_auditor_template.md',
    'prompts/43_iso21434_cybersecurity_manager_template.md',
    'schemas/cybersecurity-finding.schema.json',
    'schemas/cybersecurity-case.schema.json',
    'knowledge/iso21434/README.md',
    'knowledge/iso21434/part_rulepack_template.yaml',
    'generate_iso21434_runtime_catalog.py',
    'examples/iso21434_audit_input.json',
    'examples/aspice_iso26262_iso21434_crosswalk_example.json',
    'knowledge/semantic_tables/README.md',
    'knowledge/semantic_tables/aspice40_tables.md',
    'knowledge/semantic_tables/aspice40_tables.html',
    'knowledge/semantic_tables/aspice40_tables.json',
    'knowledge/semantic_tables/iso26262_part5_tables.md',
    'knowledge/semantic_tables/iso26262_part5_tables.html',
    'knowledge/semantic_tables/iso26262_part5_tables.json',
    'knowledge/semantic_tables/iso21434_tables.md',
    'knowledge/semantic_tables/iso21434_tables.html',
    'knowledge/semantic_tables/iso21434_tables.json',
    'knowledge/semantic_tables/manual_review_queue.json',
    'knowledge/semantic_tables/table_semantic_repair_report.md',
    'knowledge/semantic_tables/table_semantic_repair_summary.json'
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
safety_text = (ROOT / 'profiles/iso26262_safety_agents.yaml').read_text(encoding='utf-8')
cyber_text = (ROOT / 'profiles/iso21434_cybersecurity_agents.yaml').read_text(encoding='utf-8')
cyber_ids = re.findall(r'^  - id: (CS\d+)$', cyber_text, re.M)
checks['cybersecurity_agent_ids'] = {'expected': expected_cybersecurity_agents, 'actual': cyber_ids, 'count': len(cyber_ids), 'unique': len(set(cyber_ids)), 'ok': cyber_ids == expected_cybersecurity_agents}
safety_ids = re.findall(r'^  - id: (FS\d+)$', safety_text, re.M)
checks['safety_agent_ids'] = {'expected_count': 15, 'actual': safety_ids, 'count': len(safety_ids), 'unique': len(set(safety_ids)), 'ok': safety_ids == [f'FS{i:02d}' for i in range(1, 16)]}
checks['logical_agent_total'] = {'count': 8 + len(process_ids) + len(manager_ids) + len(safety_ids) + len(cyber_ids), 'expected': 90, 'ok': 8 + len(process_ids) + len(manager_ids) + len(safety_ids) + len(cyber_ids) == 90}
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
    if assignments.get('assignment_count') != 90 or len(assignment_ids) != 90 or len(set(assignment_ids)) != 90:
        assignment_errors.append('assignment count or uniqueness mismatch')
    if assignments.get('normative_status') != 'non_normative_support_layer' or assignments.get('source_attribution_in_outputs') is not False:
        assignment_errors.append('missing non-normative or source-neutral marker')
    if any(not item.get('modules') for item in assignments.get('assignments', [])):
        assignment_errors.append('agent without modules')
    checks['cognitive_assignments'] = {'count': len(assignment_ids), 'errors': assignment_errors, 'ok': not assignment_errors and set(assignment_ids) == set(['C01','C02','C03','C04','C05','C06','C07','C08'] + process_ids + manager_ids + safety_ids + cyber_ids)}
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
standards_text = (ROOT / 'config/standards_registry.yaml').read_text(encoding='utf-8')
scope_text = (ROOT / 'config/iso26262_part5_scope.yaml').read_text(encoding='utf-8')
semantic_table_errors = []
semantic_dir = ROOT / 'knowledge/semantic_tables'
try:
    semantic_summary = json.loads((semantic_dir / 'table_semantic_repair_summary.json').read_text(encoding='utf-8'))
    semantic_queue = json.loads((semantic_dir / 'manual_review_queue.json').read_text(encoding='utf-8'))
    expected_standard_table_files = [
        semantic_dir / 'aspice40_tables.json', semantic_dir / 'iso26262_part5_tables.json', semantic_dir / 'iso21434_tables.json'
    ]
    if semantic_summary.get('standalone_symbol_count_in_rendered_rows') != 0:
        semantic_table_errors.append('standalone symbol remains in rendered rows')
    if semantic_summary.get('table_count', 0) < 1:
        semantic_table_errors.append('no semantic tables generated')
    if not isinstance(semantic_queue, list):
        semantic_table_errors.append('manual review queue is not a list')
    for path in expected_standard_table_files:
        payload = json.loads(path.read_text(encoding='utf-8'))
        if not payload.get('tables'):
            semantic_table_errors.append(f'{path.name}: no tables')
except Exception as exc:
    semantic_table_errors.append(str(exc))
checks['semantic_tables'] = {'errors': semantic_table_errors, 'manual_review_count': len(semantic_queue) if 'semantic_queue' in locals() and isinstance(semantic_queue, list) else None, 'ok': not semantic_table_errors}
runtime_text = (ROOT / 'config/runtime_registry.yaml').read_text(encoding='utf-8')
checks['iso26262_public_source_boundary'] = {'runtime_only_in_registry': 'public_repository_must_not_store_full_licensed_standard_text: true' in standards_text and 'source_mode: runtime_only' in (ROOT / 'knowledge/iso26262/part5_rulepack_template.yaml').read_text(encoding='utf-8'), 'no_clause_11_in_scope': 'clause_11:' in scope_text and 'not_present_in_provided_part' in scope_text, 'safety_runtimes_present': all(f'runtime_id: R{i:02d}' in runtime_text for i in range(11, 15)), 'cybersecurity_runtimes_present': all(f'runtime_id: R{i:02d}' in runtime_text for i in range(15, 19))}
checks['iso26262_public_source_boundary']['ok'] = all(checks['iso26262_public_source_boundary'].values())
iso21434_scope_text = (ROOT / 'config/iso21434_scope.yaml').read_text(encoding='utf-8')
iso21434_template_text = (ROOT / 'knowledge/iso21434/part_rulepack_template.yaml').read_text(encoding='utf-8')
checks['iso21434_public_source_boundary'] = {
    'runtime_only_in_scope': 'source_mode: runtime_only' in iso21434_scope_text,
    'public_repository_boundary': 'public_repository_must_not_store_full_licensed_standard_text: true' in iso21434_scope_text and 'public_repository_must_not_store_full_licensed_standard_text: true' in iso21434_template_text,
    'cybersecurity_runtime_generator_present': (ROOT / 'generate_iso21434_runtime_catalog.py').exists(),
    'cybersecurity_prompts_present': (ROOT / 'prompts/42_iso21434_cybersecurity_auditor_template.md').exists() and (ROOT / 'prompts/43_iso21434_cybersecurity_manager_template.md').exists(),
    'ok': 'source_mode: runtime_only' in iso21434_scope_text and 'public_repository_must_not_store_full_licensed_standard_text: true' in iso21434_scope_text and (ROOT / 'generate_iso21434_runtime_catalog.py').exists()
}
runtime_ids = re.findall(r'^  - runtime_id: (R\d+)$', runtime_text, re.M)
r14_ok = 'logical_agents: [FS14, FS15, M15, M16, M17]' in runtime_text
r18_ok = 'logical_agents: [CS14, CS15, M18, M19, M20]' in runtime_text
checks['runtime_registry'] = {'ids': runtime_ids, 'count': len(runtime_ids), 'unique': len(set(runtime_ids)), 'no_duplicates': len(runtime_ids) == len(set(runtime_ids)), 'r14_safety_coordination_loaded': r14_ok, 'r18_cybersecurity_coordination_loaded': r18_ok, 'ok': len(runtime_ids) == len(set(runtime_ids)) and r14_ok and r18_ok}
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
