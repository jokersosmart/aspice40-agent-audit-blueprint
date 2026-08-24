from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

SOURCE = Path('/home/ubuntu/aspice40_work/aspice40_clean_plain.txt')
MATRIX_SOURCE = Path('/home/ubuntu/aspice40_work/aspice40_visual_matrices.json')
ROOT = Path('/home/ubuntu/aspice_agent_blueprint')
OUT = ROOT / 'knowledge/aspice40/process_rules'
OUT.mkdir(parents=True, exist_ok=True)

lines = SOURCE.read_text(encoding='utf-8').splitlines()
matrices = json.loads(MATRIX_SOURCE.read_text(encoding='utf-8')) if MATRIX_SOURCE.exists() else {}
process_re = re.compile(r'^(\d+\.\d+\.\d+)\.\s+([A-Z]{3}\.\d+)\s+(.+)$')
page_re = re.compile(r'^\[\[SOURCE_PAGE:(\d{3})\]\]$')


def clean_quote(parts: list[str]) -> str:
    # Keep the wording verbatim while normalizing only physical line breaks and spaces.
    parts = [p.strip() for p in parts if p.strip() and not page_re.fullmatch(p.strip())]
    return ' '.join(' '.join(parts).split())


def make_citation(cid: str, kind: str, process_id: str, indicator_id: str | None,
                  section: str, page: int | None, start: int, end: int,
                  quote: str, why: str, interpretation: str,
                  interpretation_type: str = 'literal_requirement_meaning') -> dict:
    return {
        'citation_id': cid,
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
        'text_normalization': 'whitespace_only',
        'original_text_if_corrected': None,
        'why_this_text_applies': why,
        'interpretation': interpretation,
        'interpretation_type': interpretation_type,
        'requirement_type': 'pam_explicit',
        'applies_to': [process_id],
        'not_implied': [
            'This citation does not prescribe a fixed company filename, tool or organizational structure unless a separate company_rule or customer_specific citation says so.'
        ],
        'verified_status': 'verified_against_approved_text',
        'verified_by': 'C01-source-text-review',
        'verified_at': None,
        'human_confirmation_required': True,
    }


# Find the 32 process blocks only in Chapter 4正文, excluding TOC entries.
chapter4_start = next(i for i, line in enumerate(lines) if line.strip() == '4. Process reference model and performance indicators (Level 1)')
chapter5_start = next(i for i, line in enumerate(lines) if line.strip() == '5. Process capability levels and process attributes')
blocks = []
for idx in range(chapter4_start, chapter5_start):
    line = lines[idx]
    m = process_re.match(line.strip())
    if m:
        blocks.append((idx, m.group(1), m.group(2), m.group(3)))

all_ids = []
for block_i, (start_idx, section, pid, pname) in enumerate(blocks):
    end_idx = blocks[block_i + 1][0] if block_i + 1 < len(blocks) else chapter5_start
    segment = lines[start_idx:end_idx]
    all_ids.append(pid)
    page = None
    for x in segment:
        pm = page_re.match(x.strip())
        if pm:
            page = int(pm.group(1))
            break

    # Purpose: after Process purpose until Process outcomes.
    purpose_idx = next((i for i, x in enumerate(segment) if x.strip() == 'Process purpose'), None)
    outcomes_idx = next((i for i, x in enumerate(segment) if x.strip() == 'Process outcomes'), None)
    base_idx = next((i for i, x in enumerate(segment) if x.strip() == 'Base Practices'), None)
    purpose = clean_quote(segment[purpose_idx + 1:outcomes_idx]) if purpose_idx is not None and outcomes_idx is not None else ''

    outcomes = []
    citations = []
    if purpose:
        pstart = start_idx + purpose_idx + 2
        pend = start_idx + outcomes_idx
        citations.append(make_citation(
            f'SPEC-{pid.replace(".", "")}-PURPOSE-001', 'purpose', pid, None, section, page,
            pstart, pend, purpose,
            f'Use this exact purpose when deciding the boundary of {pid}.',
            f'This is the PAM purpose statement for {pid}; it defines the intended result of the Process but does not define the company lifecycle or fixed document names.'
        ))

    if outcomes_idx is not None:
        outcome_start_positions = []
        for i in range(outcomes_idx + 1, base_idx if base_idx is not None else len(segment)):
            if re.match(r'^\s*\d+\)\s*', segment[i]):
                outcome_start_positions.append(i)
        for oi, local_start in enumerate(outcome_start_positions):
            local_end = outcome_start_positions[oi + 1] if oi + 1 < len(outcome_start_positions) else (base_idx if base_idx is not None else len(segment))
            quote = clean_quote(segment[local_start:local_end])
            number = re.match(r'^\s*(\d+)\)', segment[local_start]).group(1)
            outcome_id = f'OUTCOME.{number}'
            outcomes.append({'id': outcome_id, 'text': quote})
            citations.append(make_citation(
                f'SPEC-{pid.replace(".", "")}-OUTCOME-{int(number):02d}', 'outcome', pid, outcome_id, section, page,
                start_idx + local_start + 1, start_idx + local_end,
                quote,
                f'Use the complete {pid} outcome {number} as the normative result to inspect.',
                f'This text states the expected positive result for {pid} outcome {number}; evidence must be evaluated against its full meaning, not against a filename or checkbox.'
            ))

    # Base Practices: each BP begins with ID, and includes wrapped lines and Notes until next BP.
    bps = []
    if base_idx is not None:
        bp_starts = []
        bp_re = re.compile(r'^\s*' + re.escape(pid) + r'\.BP(\d+):')
        for i in range(base_idx + 1, len(segment)):
            if bp_re.match(segment[i]):
                bp_starts.append(i)
        for bi, local_start in enumerate(bp_starts):
            local_end = bp_starts[bi + 1] if bi + 1 < len(bp_starts) else len(segment)
            # Stop before matrix table headings or the next numbered section when needed.
            raw = segment[local_start:local_end]
            quote = clean_quote(raw)
            bm = bp_re.match(segment[local_start])
            number = bm.group(1)
            bp_id = f'BP{number}'
            title_line = quote.split(':', 1)[1].strip() if ':' in quote else quote
            bps.append({'id': bp_id, 'text': quote, 'title': title_line})
            bp_page = page
            for x in raw:
                pm = page_re.match(x.strip())
                if pm:
                    bp_page = int(pm.group(1))
                    break
            citations.append(make_citation(
                f'SPEC-{pid.replace(".", "")}-BP-{int(number):02d}', 'base_practice', pid, bp_id, section, bp_page,
                start_idx + local_start + 1, start_idx + local_end,
                quote,
                f'Use the complete {pid}.{bp_id} paragraph when checking the corresponding practice.',
                f'This is the complete Base Practice paragraph extracted from the approved PAM text. The Agent must compare evidence to the entire paragraph and its notes, not only the BP title.'
            ))

    matrix = matrices.get(pid)
    product_context = {
        'evidence_domains': [],
        'manager_routing': [],
        'matrix_reconstruction_status': 'not_available'
    }
    if matrix:
        product_context['matrix_reconstruction_status'] = 'available_from_layout_extraction'
        product_context['matrix_source_layout_line'] = matrix.get('source_layout_line')
        product_context['output_information_items'] = matrix.get('output_information_items', [])
        product_context['base_practice_outcome_mapping'] = matrix.get('base_practices', [])

    pack = {
        'schema_version': '1.0',
        'aspice_version': '4.0',
        'profile_version': '2026.08.24',
        'process_id': pid,
        'process_name': pname,
        'process_group': pid.split('.')[0],
        'source': {
            'document_id': 'Automotive-SPICE-PAM-v40',
            'version': '4.0',
            'source_file': 'aspice40_clean_plain.txt',
            'source_section': section,
            'source_page_hint': page,
            'citation_policy': 'Every normative finding must carry one or more direct spec citation objects with verbatim_text.'
        },
        'pam': {
            'purpose': purpose,
            'outcomes': outcomes,
            'base_practices': bps,
        },
        'spec_citations': citations,
        'product_context': product_context,
        'human_gates': ['scope_and_na', 'technical_correctness', 'verification_adequacy', 'formal_rating', 'major_finding_closure'],
    }
    out_path = OUT / f'{pid}.yaml'
    # JSON is valid YAML 1.2 and avoids losing quotation marks in verbatim text.
    out_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

summary = {'process_count': len(all_ids), 'process_ids': all_ids, 'output_dir': str(OUT)}
(Path('/home/ubuntu/aspice_agent_blueprint/knowledge/aspice40/process_rulepack_generation.json')).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
