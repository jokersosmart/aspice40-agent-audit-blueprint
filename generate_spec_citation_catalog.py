from __future__ import annotations

import hashlib
import json
from pathlib import Path

SOURCE = Path('/home/ubuntu/aspice40_work/aspice40_clean_plain.txt')
OUT_JSONL = Path('/home/ubuntu/aspice_agent_blueprint/knowledge/aspice40/spec_citation_catalog.jsonl')
OUT_MD = Path('/home/ubuntu/aspice_agent_blueprint/knowledge/aspice40/spec_citation_catalog.md')

lines = SOURCE.read_text(encoding='utf-8').splitlines()


def exact_quote(start: int, end: int) -> str:
    # Input line numbers are 1-indexed. Page markers are metadata and are not
    # part of the normative paragraph quote.
    selected = []
    for line in lines[start - 1:end]:
        if line.strip().startswith('[[SOURCE_PAGE:'):
            continue
        selected.append(line.strip())
    return ' '.join(' '.join(selected).split())


def citation(citation_id: str, kind: str, section: str, process_id: str | None,
             indicator_id: str | None, page: int, start: int, end: int,
             why: str, interpretation: str, interpretation_type: str,
             applies_to: list[str], not_implied: list[str] | None = None,
             original_text_if_corrected: str | None = None,
             text_normalization: str = 'whitespace_only') -> dict:
    quote = exact_quote(start, end)
    return {
        'citation_id': citation_id,
        'document_id': 'Automotive-SPICE-PAM-v40',
        'document_version': '4.0',
        'citation_kind': kind,
        'source_anchor': {
            'section': section,
            'process_id': process_id,
            'indicator_id': indicator_id,
            'page': page,
            'source_file': 'aspice40_clean_plain.txt',
            'source_line_start': start,
            'source_line_end': end,
        },
        'verbatim_text': quote,
        'verbatim_text_sha256': hashlib.sha256(quote.encode('utf-8')).hexdigest(),
        'text_normalization': text_normalization,
        'original_text_if_corrected': original_text_if_corrected,
        'why_this_text_applies': why,
        'interpretation': interpretation,
        'interpretation_type': interpretation_type,
        'requirement_type': 'pam_explicit',
        'applies_to': applies_to,
        'not_implied': not_implied or [],
        'verified_status': 'verified_against_approved_text',
        'verified_by': 'C01-source-text-review',
        'verified_at': None,
        'human_confirmation_required': True,
    }


catalog = [
    citation(
        'SPEC-HWE2-PURPOSE-001', 'purpose', '4.7.2', 'HWE.2', None, 72, 4684, 4687,
        'Use when checking whether the hardware design work is expected to produce an analyzed, manufacturable design and production-relevant data.',
        'The purpose covers analyzed design, dynamic aspects, consistency with hardware requirements, manufacturing suitability and derivation of production-relevant data.',
        'literal_requirement_meaning', ['HWE.2', 'M03', 'M04', 'M05', 'M07'],
        ['This does not prescribe a specific EDA tool, document filename or silicon milestone.']),
    citation(
        'SPEC-HWE2-BP5-001', 'base_practice', '4.7.2', 'HWE.2', 'BP5', 73, 4735, 4738,
        'Use when checking requirements-to-hardware and architecture-to-detailed-design consistency and bidirectional traceability.',
        'The Agent must inspect both consistency and bidirectional traceability between hardware elements and hardware requirements, and between detailed design and architecture components.',
        'traceability_mapping', ['HWE.2', 'C06', 'M03', 'M04', 'M05'],
        ['A link existing in a tool is not by itself proof that the linked information is consistent.']),
    citation(
        'SPEC-HWE2-NOTE9-001', 'assessment_guidance', '4.7.2', 'HWE.2', 'BP5', 73, 4742, 4744,
        'Use when evaluating whether a traceability report demonstrates consistency rather than only link existence.',
        'The traceability check must test consistency and support change-impact and verification-coverage reasoning; mere link presence is insufficient.',
        'quality_explanation', ['HWE.2', 'C06', 'SUP.10'],
        ['The passage does not require a particular traceability database or visualization tool.']),
    citation(
        'SPEC-HWE2-BP6-001', 'base_practice', '4.7.2', 'HWE.2', 'BP6', 73, 4746, 4748,
        'Use when checking communication and agreement of architecture, detailed design, special characteristics and relevant production data.',
        'Affected parties must receive the agreed hardware architecture and detailed design together with special characteristics and relevant production data.',
        'evidence_mapping', ['HWE.2', 'M03', 'M07', 'M10'],
        ['The source matrix on the next page displays a BP7 label for this communication row; that conflict must remain open for human review.']),
    citation(
        'SPEC-VAL1-PURPOSE-001', 'purpose', '4.5.1', 'VAL.1', None, 58, 3851, 3853,
        'Use when checking whether product validation demonstrates intended use in the operational target environment.',
        'Validation is concerned with the end product, direct end-user interaction, intended-use expectations and the operational target environment.',
        'literal_requirement_meaning', ['VAL.1', 'M08'],
        ['System verification or laboratory testing alone is not automatically equivalent to validation in the target environment.']),
    citation(
        'SPEC-VAL1-BP4-001', 'base_practice', '4.5.1', 'VAL.1', 'BP4', 60, 3914, 3917,
        'Use when checking bidirectional traceability between validation measures, stakeholder requirements and validation results.',
        'The Agent must look for consistency and bidirectional traceability in both measure-to-requirement and result-to-measure relationships.',
        'traceability_mapping', ['VAL.1', 'C06', 'M08'],
        ['A validation result without its measure and stakeholder-requirement relationship is incomplete evidence.']),
    citation(
        'SPEC-SUP1-BP1-001', 'base_practice', '4.8.1', 'SUP.1', 'BP1', 79, 5163, 5167,
        'Use when checking QA independence and the absence of self-monitoring conflicts.',
        'Quality assurance is expected to be independent and objective; financial or organizational assignment and responsibility for the subject process can affect independence.',
        'quality_explanation', ['SUP.1', 'M11'],
        ['The passage does not mean every QA activity must be performed by a separate company or external supplier.']),
    citation(
        'SPEC-ANNEXB-VERIFICATION-MEASURE-001', 'information_item', 'Annex B', None, '08-60', 129, 8562, 8568,
        'Use when determining acceptable forms and characteristics of verification measures for hardware, firmware or system evidence.',
        'A verification/validation measure can include test, measurement, simulation or emulation; the specification should include criteria and entry/exit conditions.',
        'evidence_mapping', ['SYS.4', 'SYS.5', 'SWE.4', 'SWE.5', 'SWE.6', 'HWE.3', 'HWE.4', 'VAL.1'],
        ['This does not imply that every project must use every listed technique.']),
]

OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
with OUT_JSONL.open('w', encoding='utf-8') as f:
    for item in catalog:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

md = ['# ASPICE 4.0 Direct Spec Citation Catalog', '', 'Each entry below contains the complete verbatim paragraph or complete definition excerpt used by an Agent. Whitespace is normalized only; the source line range and hash are retained.', '']
for item in catalog:
    a = item['source_anchor']
    md += [f"## {item['citation_id']}", '', f"- **Kind:** {item['citation_kind']}", f"- **Location:** {a['section']} / {a['process_id'] or ''} / {a['indicator_id'] or ''} / page {a['page']}", f"- **Source lines:** {a['source_line_start']}–{a['source_line_end']}", f"- **Verbatim SHA-256:** `{item['verbatim_text_sha256']}`", '', '> ' + item['verbatim_text'], '', f"**Why it applies:** {item['why_this_text_applies']}", '', f"**Interpretation:** {item['interpretation']}", '', f"**Not implied:** {'; '.join(item['not_implied']) if item['not_implied'] else 'None stated.'}", '']
OUT_MD.write_text('\n'.join(md).rstrip() + '\n', encoding='utf-8')
print(json.dumps({'entries': len(catalog), 'jsonl': str(OUT_JSONL), 'markdown': str(OUT_MD)}, ensure_ascii=False, indent=2))
