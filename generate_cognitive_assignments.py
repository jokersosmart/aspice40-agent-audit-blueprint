from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/aspice_agent_blueprint')
process_text = (ROOT / 'profiles/process_agents.yaml').read_text(encoding='utf-8')
manager_text = (ROOT / 'profiles/manager_agents.yaml').read_text(encoding='utf-8')
process_ids = re.findall(r'^  - id: ([A-Z]{3}\.\d+)$', process_text, re.M)
manager_ids = re.findall(r'^  - id: (M\d+)$', manager_text, re.M)

control_assignments = {
    'C01': ['COM-01','COM-02','COM-08','COM-09','COM-10'],
    'C02': ['COM-01','COM-02','COM-05','COM-08'],
    'C03': ['COM-01','COM-02','COM-08','COM-09'],
    'C04': ['COM-01','COM-02','COM-05','COM-08'],
    'C05': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-09','COM-10'],
    'C06': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'C07': ['COM-02','COM-03','COM-04','COM-05','COM-09','COM-10'],
    'C08': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
}

requirements_processes = {'SYS.1','SYS.2','SYS.3','SWE.1','SWE.2','SWE.3','HWE.1','HWE.2'}
verification_processes = {'SYS.4','SYS.5','SWE.4','SWE.5','SWE.6','HWE.3','HWE.4','VAL.1'}
management_processes = {'ACQ.4','SPL.2','SUP.1','SUP.8','SUP.9','SUP.10','SUP.11','MAN.3','MAN.5','MAN.6','PIM.3','REU.2'}
ml_processes = {'MLE.1','MLE.2','MLE.3','MLE.4'}
process_assignments = {}
for pid in process_ids:
    if pid in requirements_processes:
        modules = ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09']
        emphasis = 'bounded problem definition, evidence provenance, design assumptions, interface communication and cross-level consistency'
    elif pid in verification_processes:
        modules = ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10']
        emphasis = 'testable hypotheses, controlled measures, result interpretation, regression impact and independent review'
    elif pid in ml_processes:
        modules = ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10']
        emphasis = 'data/model scope, reproducibility, alternative explanations, model risk and human approval'
    else:
        modules = ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10']
        emphasis = 'scope, evidence quality, prioritization, cross-party responsibility, baseline continuity and corrective action'
    process_assignments[pid] = {'modules': modules, 'emphasis': emphasis}

manager_assignments = {
    'M01': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M02': ['COM-01','COM-02','COM-03','COM-04','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M03': ['COM-01','COM-02','COM-03','COM-04','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M04': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'M05': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'M06': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'M07': ['COM-01','COM-02','COM-03','COM-04','COM-05','COM-07','COM-09','COM-10'],
    'M08': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M09': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M10': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M11': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-08','COM-09','COM-10'],
    'M12': ['COM-01','COM-02','COM-04','COM-05','COM-07','COM-08','COM-09','COM-10'],
    'M13': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
    'M14': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
    'M15': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
    'M16': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'M17': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
}

safety_assignments = {
    'FS01': ['COM-01','COM-02','COM-05','COM-06','COM-09','COM-10'],
    'FS02': ['COM-01','COM-02','COM-04','COM-06','COM-07','COM-09','COM-10'],
    'FS03': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS04': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS05': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS06': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'FS07': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS08': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
    'FS09': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'FS10': ['COM-01','COM-02','COM-03','COM-05','COM-07','COM-09','COM-10'],
    'FS11': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS12': ['COM-01','COM-02','COM-05','COM-08','COM-09'],
    'FS13': ['COM-01','COM-02','COM-05','COM-06','COM-07','COM-09','COM-10'],
    'FS14': ['COM-01','COM-02','COM-04','COM-05','COM-06','COM-07','COM-08','COM-09','COM-10'],
    'FS15': ['COM-01','COM-02','COM-03','COM-05','COM-06','COM-07','COM-09','COM-10'],
}

manager_emphasis = {
    'M01': 'system boundary, affected parties, interface decisions and cross-domain impact',
    'M02': 'firmware evidence chain, implementation assumptions, regression and release readiness',
    'M03': 'hardware architecture, design feasibility, manufacturing and evidence ownership',
    'M04': 'RTL behavior, CDC/reset/power-domain assumptions, formal/simulation evidence',
    'M05': 'electrical behavior, PVT/corner assumptions, measurement and characterization',
    'M06': 'controlled simulation/emulation, reproducibility, coverage and result interpretation',
    'M07': 'design freeze, irreversible release decisions, sign-off evidence and rollback limits',
    'M08': 'system-level measures, intended environment, validation and affected-party communication',
    'M09': 'software verification measures, regression, defect interpretation and independent review',
    'M10': 'hardware verification method selection, measurement, silicon evidence and closure',
    'M11': 'independence, consistency, evidence quality, corrective action and escalation',
    'M12': 'baseline integrity, change impact, problem cause, recovery and re-verification',
    'M13': 'scope, constraints, risks, resources, metrics, trade-offs and decision gates',
    'M14': 'supplier/reuse evidence, external commitments, release communication and qualification',
    'M15': 'functional safety lifecycle, safety plan, ASIL context, safety case and residual-risk governance',
    'M16': 'hardware safety requirements, safety mechanisms, safety analysis, metrics, PMHF/EEC and qualification',
    'M17': 'independent safety verification, confirmation measures, anomaly disposition, re-verification and safety release evidence',
}

entries = []
for cid, modules in control_assignments.items():
    entries.append({'agent_id': cid, 'agent_class': 'control', 'modules': modules, 'operating_mode': 'evidence_first', 'mandatory_gates': ['direct_spec_citation','source_integrity','human_review_for_authority']})
for pid, info in process_assignments.items():
    entries.append({'agent_id': pid, 'agent_class': 'process_auditor', 'modules': info['modules'], 'operating_mode': 'normative_check_plus_contextual_analysis', 'emphasis': info['emphasis'], 'mandatory_gates': ['direct_spec_citation','scope_status','unknown_and_conflict_preservation','technical_human_review']})
for mid, modules in manager_assignments.items():
    entries.append({'agent_id': mid, 'agent_class': 'manager', 'modules': modules, 'operating_mode': 'responsibility_and_action_planning', 'emphasis': manager_emphasis[mid], 'mandatory_gates': ['citation_inheritance','owner_and_verifier_separation','resource_commitment','closure_authority']})
for sid, modules in safety_assignments.items():
    entries.append({'agent_id': sid, 'agent_class': 'safety', 'modules': modules, 'operating_mode': 'safety_evidence_and_human_gate_preparation', 'emphasis': 'direct ISO 26262-5 citation, safety evidence, dependency awareness, alternative explanation and mandatory human safety review', 'mandatory_gates': ['direct_spec_citation','ASIL_or_scope_review','independent_safety_review','human_safety_gate']})

output = {
    'schema_version': '1.0',
    'layer_name': 'Cognitive Operating Layer',
    'normative_status': 'non_normative_support_layer',
    'visibility': 'standard_agent_behavior',
    'source_attribution_in_outputs': False,
    'precedence': 'below_approved_spec_company_customer_rules_and_human_approvals',
    'assignment_count': len(entries),
    'assignments': entries,
}
path = ROOT / 'config/agent_cognitive_assignments.json'
path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'assignment_count': len(entries), 'process_count': len(process_ids), 'manager_count': len(manager_ids), 'output': str(path)}, ensure_ascii=False, indent=2))
