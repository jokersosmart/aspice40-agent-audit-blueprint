from __future__ import annotations

import hashlib
import json
from pathlib import Path

source = Path('/home/ubuntu/aspice40_work/aspice40_clean_plain.txt')
lines = source.read_text(encoding='utf-8').splitlines()

def quote(start: int, end: int) -> str:
    return ' '.join(' '.join(x.strip() for x in lines[start-1:end] if x.strip() and not x.strip().startswith('[[SOURCE_PAGE:')).split())

verbatim = quote(4735, 4738)
citation = {
    'citation_id': 'SPEC-HWE2-BP5-001',
    'document_id': 'Automotive-SPICE-PAM-v40',
    'document_version': '4.0',
    'citation_kind': 'base_practice',
    'source_anchor': {
        'section': '4.7.2', 'process_id': 'HWE.2', 'indicator_id': 'BP5',
        'page': 73, 'source_file': 'aspice40_clean_plain.txt',
        'source_line_start': 4735, 'source_line_end': 4738
    },
    'verbatim_text': verbatim,
    'verbatim_text_sha256': hashlib.sha256(verbatim.encode('utf-8')).hexdigest(),
    'text_normalization': 'whitespace_only',
    'original_text_if_corrected': None,
    'why_this_text_applies': '本次檢查要確認 hardware elements 與 hardware requirements，以及 hardware detailed design 與 hardware architecture components 之間的雙向追溯與一致性。',
    'interpretation': 'Agent 必須同時檢查 link 是否雙向、版本與 baseline 是否相容，以及連結兩端內容是否一致；僅有 tool link 不能直接視為滿足。',
    'interpretation_type': 'traceability_mapping',
    'requirement_type': 'pam_explicit',
    'applies_to': ['HWE.2', 'C06', 'M03', 'M04', 'M05'],
    'not_implied': ['PAM 沒有指定固定 traceability 工具、固定檔名或固定資料庫。'],
    'verified_status': 'verified_against_approved_text',
    'verified_by': 'C01-source-text-review',
    'verified_at': None,
    'human_confirmation_required': True,
}

result = {
    'agent_id': 'HWE.2-auditor',
    'agent_version': '2026.08.24',
    'run_id': 'RUN-2026-0001',
    'project_id': 'SSDCTRL-A',
    'release_or_baseline': 'HW-BL-042',
    'process_id': 'HWE.2',
    'scope_status': 'in_scope',
    'checks': [{
        'check_id': 'HWE.2.BP5',
        'requirement_type': 'pam_explicit',
        'requirement_summary': 'Ensure consistency and establish bidirectional traceability.',
        'source_anchor': citation['source_anchor'],
        'spec_citations': [citation],
        'citation_missing': False,
        'evidence_refs': [
            {'artifact_id': 'HW-ARCH-001', 'uri_or_path': 'plm://ssdctrl/hw-architecture/HW-ARCH-001', 'revision': 'R12', 'baseline': 'HW-BL-042', 'owner': 'M03', 'review_status': 'approved'},
            {'artifact_id': 'RTL-BASE-017', 'uri_or_path': 'git://hardware/rtl@commit:REPLACE', 'revision': 'commit:REPLACE', 'baseline': 'HW-BL-042', 'owner': 'M04', 'review_status': 'reviewed'}
        ],
        'traceability_refs': ['HW-ARCH-001 -> RTL-BASE-017'],
        'status': 'unknown',
        'rationale': '目前看到架構與 RTL 有 candidate edge，但尚未提供完整 hardware requirement ID coverage、雙向 link 及 consistency review evidence，因此不能判定 satisfied 或 gap。',
        'missing_or_conflicting_evidence': ['hardware requirement to hardware element bidirectional traceability', 'consistency review evidence', 'technical reviewer confirmation'],
        'impact': 'high',
        'recommended_action': '補充 requirement-to-design traceability export、consistency review record 與獨立 reviewer 結果，再執行 HWE.2.BP5 re-verification。',
        'owner_manager': 'M03',
        'verification_owner': 'M10',
        'human_confirmation_required': True,
        'confidence': 'medium'
    }],
    'cross_domain_issues': [],
    'questions_for_owner': ['要求與硬體元素是否有完整雙向 ID mapping？', 'RTL baseline 是否由 approved hardware architecture R12 分解而來？', '誰是獨立 consistency reviewer？'],
    'summary': {'satisfied': 0, 'partial': 0, 'gap': 0, 'unknown': 1, 'conflict': 0, 'not_in_scope': 0}
}
Path('/home/ubuntu/aspice_agent_blueprint/examples/hwe2_audit_result_with_citations.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(Path('/home/ubuntu/aspice_agent_blueprint/examples/hwe2_audit_result_with_citations.json')), 'verbatim_sha256': citation['verbatim_text_sha256']}, ensure_ascii=False, indent=2))
