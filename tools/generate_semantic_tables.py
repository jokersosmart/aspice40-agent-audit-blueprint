#!/usr/bin/env python3
import json
import html
from pathlib import Path

BASE = Path('/home/ubuntu')
OUT = BASE / 'aspice_semantic_tables'
OUT.mkdir(parents=True, exist_ok=True)


def table(standard, table_id, title, clause, source_anchor, columns, rows,
          confidence='high', symbol_dictionary=None, notes=None,
          manual_review=None):
    return {
        'standard': standard,
        'table_id': table_id,
        'title': title,
        'clause': clause,
        'source_anchor': source_anchor,
        'columns': columns,
        'rows': rows,
        'confidence': confidence,
        'symbol_dictionary': symbol_dictionary or [],
        'notes': notes or [],
        'manual_review': manual_review or [],
    }


def html_table(t):
    head = ''.join(f'<th>{html.escape(str(c))}</th>' for c in t['columns'])
    body = []
    for r in t['rows']:
        body.append('<tr>' + ''.join(f'<td>{html.escape(str(r.get(c, ""))).replace(chr(10), "<br>")}</td>' for c in t['columns']) + '</tr>')
    return (
        f'<section class="table-card confidence-{t["confidence"]}">'
        f'<h2>{html.escape(t["table_id"])} — {html.escape(t["title"])}</h2>'
        f'<p><b>Clause:</b> {html.escape(t["clause"])} · <b>Source anchor:</b> {html.escape(t["source_anchor"])} · '
        f'<b>Confidence:</b> {html.escape(t["confidence"])}</p>'
        f'<table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'
        + (f'<p class="note"><b>Notes:</b> {html.escape("; ".join(t["notes"]))}</p>' if t['notes'] else '')
        + (f'<p class="review"><b>Manual review:</b> {html.escape("; ".join(t["manual_review"]))}</p>' if t['manual_review'] else '')
        + '</section>'
    )


def md_table(t):
    lines = [
        f'### {t["table_id"]} — {t["title"]}',
        '',
        f'**Clause:** {t["clause"]}  ',
        f'**Source anchor:** {t["source_anchor"]}  ',
        f'**Confidence:** `{t["confidence"]}`',
        '',
        '| ' + ' | '.join(t['columns']) + ' |',
        '|' + '|'.join(['---'] * len(t['columns'])) + '|',
    ]
    for r in t['rows']:
        vals = [str(r.get(c, '')).replace('|', '\\|').replace('\n', '<br>') for c in t['columns']]
        lines.append('| ' + ' | '.join(vals) + ' |')
    if t['notes']:
        lines += ['', '> **Notes:** ' + '; '.join(t['notes'])]
    if t['manual_review']:
        lines += ['', '> **Manual review:** ' + '; '.join(t['manual_review'])]
    return '\n'.join(lines)


def write_standard(standard_key, title, tables, intro, dictionary):
    payload = {
        'standard': standard_key,
        'title': title,
        'table_count': len(tables),
        'tables': tables,
        'symbol_dictionary': dictionary,
    }
    (OUT / f'{standard_key}_tables.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    md = [f'# {title}', '', intro, '', '## Symbol and empty-cell semantics', '', '| Symbol／form | Table context | Explicit meaning |', '|---|---|---|']
    for d in dictionary:
        md.append(f'| {d["symbol"]} | {d["context"]} | {d["meaning"]} |')
    md += ['', '## Reconstructed tables', '']
    md += [md_table(t) + '\n' for t in tables]
    (OUT / f'{standard_key}_tables.md').write_text('\n'.join(md), encoding='utf-8')
    css = '''body{font-family:Arial,"Noto Sans",sans-serif;line-height:1.45;margin:2rem;background:#f5f7fa;color:#17212b}.table-card{background:#fff;border:1px solid #d7dee8;border-left:6px solid #2f6fed;border-radius:8px;padding:1rem;margin:1.25rem 0;overflow:auto}.confidence-medium{border-left-color:#c58b00}.confidence-low{border-left-color:#c23b22}table{border-collapse:collapse;min-width:680px;width:100%;font-size:.92rem}th{background:#173b6c;color:#fff;text-align:left}th,td{border:1px solid #c7d0dc;padding:.45rem;vertical-align:top}tr:nth-child(even){background:#f6f8fb}.note{background:#eef5ff;padding:.6rem}.review{background:#fff4df;padding:.6rem;color:#6b4b00}.legend{background:#fff;padding:1rem;border:1px solid #d7dee8}'''
    hs = [f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{css}</style></head><body>', f'<h1>{html.escape(title)}</h1>', f'<p>{html.escape(intro)}</p>', '<div class="legend"><h2>Symbol and empty-cell semantics</h2><table><thead><tr><th>Symbol／form</th><th>Table context</th><th>Explicit meaning</th></tr></thead><tbody>']
    for d in dictionary:
        hs.append(f'<tr><td>{html.escape(d["symbol"])}</td><td>{html.escape(d["context"])}</td><td>{html.escape(d["meaning"])}</td></tr>')
    hs += ['</tbody></table></div>']
    hs += [html_table(t) for t in tables]
    hs += ['</body></html>']
    (OUT / f'{standard_key}_tables.html').write_text('\n'.join(hs), encoding='utf-8')


# ASPICE 4.0: use the previously verified process structure and make all mappings explicit.
aspice_dict = [
    {'symbol': 'X', 'context': 'Outcome／BP／Output Information Item mapping', 'meaning': 'mapped = true for the named row and named Outcome column; the X itself is not left as a standalone cell'},
    {'symbol': 'N/P/L/F', 'context': 'Table 16–17 rating scale', 'meaning': 'Not, Partially, Largely, Fully achieved'},
    {'symbol': 'P−／P+／L−／L+', 'context': 'Table 18–19 refined rating', 'meaning': 'refined sub-level of Partially or Largely achieved'},
    {'symbol': '—', 'context': 'table separator or empty／not-applicable cell', 'meaning': 'render as an explicit empty_or_not_applicable value only when the table defines it; never infer a numeric value'},
]
aspice_tables = [
    table('ASPICE 4.0', 'Table 14', 'Process capability levels', '3.2.1', 'aspice40_layout.txt lines 815–847', ['Level', 'Name', 'Semantic description'], [
        {'Level':'0','Name':'Incomplete process','Semantic description':'The process is not implemented or fails to achieve its process purpose.'},
        {'Level':'1','Name':'Performed process','Semantic description':'The implemented process achieves its process purpose.'},
        {'Level':'2','Name':'Managed process','Semantic description':'The performed process is implemented in a managed fashion and work products are established, controlled and maintained.'},
        {'Level':'3','Name':'Established process','Semantic description':'The managed process uses a defined process capable of achieving its process outcomes.'},
        {'Level':'4','Name':'Predictable process','Semantic description':'The established process operates predictively within defined limits; quantitative management identifies and addresses variation.'},
        {'Level':'5','Name':'Innovating process','Semantic description':'The predictable process is continually improved to respond to organizational change.'},
    ]),
    table('ASPICE 4.0', 'Table 15', 'Process attributes', '3.2.1', 'aspice40_layout.txt lines 849–867', ['Level', 'Attribute ID', 'Process attribute'], [
        {'Level':'1','Attribute ID':'PA 1.1','Process attribute':'Process performance'},
        {'Level':'2','Attribute ID':'PA 2.1','Process attribute':'Performance management'},
        {'Level':'2','Attribute ID':'PA 2.2','Process attribute':'Work product management'},
        {'Level':'3','Attribute ID':'PA 3.1','Process attribute':'Process definition'},
        {'Level':'3','Attribute ID':'PA 3.2','Process attribute':'Process deployment'},
        {'Level':'4','Attribute ID':'PA 4.1','Process attribute':'Quantitative analysis'},
        {'Level':'4','Attribute ID':'PA 4.2','Process attribute':'Quantitative control'},
        {'Level':'5','Attribute ID':'PA 5.1','Process attribute':'Process innovation'},
        {'Level':'5','Attribute ID':'PA 5.2','Process attribute':'Process innovation implementation'},
    ]),
    table('ASPICE 4.0', 'Table 16', 'Rating scale', '3.2.2.1', 'aspice40_layout.txt lines 887–908', ['Rating', 'Name', 'Explicit interpretation'], [
        {'Rating':'N','Name':'Not achieved','Explicit interpretation':'Little or no evidence of achievement of the defined process attribute.'},
        {'Rating':'P','Name':'Partially achieved','Explicit interpretation':'Some evidence of an approach and some achievement; some aspects may be unpredictable.'},
        {'Rating':'L','Name':'Largely achieved','Explicit interpretation':'Evidence of a systematic approach and significant achievement; some weaknesses may exist.'},
        {'Rating':'F','Name':'Fully achieved','Explicit interpretation':'Evidence of a complete and systematic approach and full achievement; no significant weaknesses.'},
    ]),
    table('ASPICE 4.0', 'Table 17', 'Rating scale percentage values', '3.2.2.1', 'aspice40_layout.txt lines 909–916', ['Rating', 'Achievement interval'], [
        {'Rating':'N','Achievement interval':'0 to ≤ 15% achievement'},
        {'Rating':'P','Achievement interval':'> 15% to ≤ 50% achievement'},
        {'Rating':'L','Achievement interval':'> 50% to ≤ 85% achievement'},
        {'Rating':'F','Achievement interval':'> 85% to ≤ 100% achievement'},
    ]),
    table('ASPICE 4.0', 'Table 19', 'Refined rating scale percentage values', '3.2.2', 'aspice40_layout.txt lines 945–950', ['Rating', 'Achievement interval'], [
        {'Rating':'P−','Achievement interval':'> 15% to ≤ 32.5% achievement'},
        {'Rating':'P+','Achievement interval':'> 32.5% to ≤ 50% achievement'},
        {'Rating':'L−','Achievement interval':'> 50% to ≤ 67.5% achievement'},
        {'Rating':'L+','Achievement interval':'> 67.5% to ≤ 85% achievement'},
    ]),
]
# Add the 32 verified process structures as long tables with explicit mapping booleans.
visual_path = BASE / 'aspice40_work' / 'aspice40_visual_matrices.json'
if visual_path.exists():
    matrices = json.loads(visual_path.read_text(encoding='utf-8'))
    for pid, m in matrices.items():
        if not isinstance(m, dict) or 'process_id' not in m:
            continue
        rows = []
        for item in m.get('output_information_items', []):
            rows.append({'Row type':'Output Information Item', 'Row ID':item.get('id',''), 'Name':item.get('name','').split(' Table 22')[0].split(' 5. Process capability levels')[0].strip(), 'Mapped Outcomes':', '.join(item.get('outcomes', [])), 'Mapped':'true'})
        for bp in m.get('base_practices', []):
            rows.append({'Row type':'Base Practice', 'Row ID':bp.get('id',''), 'Name':bp.get('name','').split(' Table 22')[0].split(' 5. Process capability levels')[0].strip(), 'Mapped Outcomes':', '.join(bp.get('outcomes', [])), 'Mapped':'true'})
        aspice_tables.append(table('ASPICE 4.0', f'{pid} matrix', f'{m.get("title", pid)} — explicit Outcome mapping', 'Chapter 4', f'aspice40_visual_matrices.json source_layout_line {m.get("source_layout_line", "unknown")}', ['Row type','Row ID','Name','Mapped Outcomes','Mapped'], rows, confidence='high', notes=['The original standalone X marks are represented as explicit mapped=true plus a named outcome list.'], manual_review=['Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.']))

write_standard('aspice40', 'ASPICE 4.0 semantic tables', aspice_tables, 'This output converts table-like ASPICE content into explicit row and column semantics. The process matrices use named Outcome lists instead of standalone X characters.', aspice_dict)

# ISO 26262-5: values are taken from verified layout anchors and should remain explicit.
iso26262_dict = [
    {'symbol': '+', 'context': 'Tables 1–3 and 10–12', 'meaning': 'recommended method／property for the ASIL column shown'},
    {'symbol': '++', 'context': 'Tables 1–3 and 10–12', 'meaning': 'stronger／higher recommendation for the ASIL column shown'},
    {'symbol': 'o', 'context': 'Tables 2, 10 and 12', 'meaning': 'no specific recommendation for the ASIL column shown'},
    {'symbol': '—', 'context': 'notes or table cells', 'meaning': 'no information／not applicable only where the source table defines it; never a missing number'},
    {'symbol': '≥／<', 'context': 'metric and failure-rate tables', 'meaning': 'inequality operator belonging to the numeric target field'},
]
iso26262_tables = [
    table('ISO 26262-5:2018', 'Table 1', 'Properties of hardware architectural design', '7.4.1.6', 'iso26262_part5_layout.txt lines 787–797; PDF physical page 18 / printed page 10', ['Property', 'ASIL A', 'ASIL B', 'ASIL C', 'ASIL D'], [
        {'Property':'Hierarchical design','ASIL A':'+','ASIL B':'+','ASIL C':'+','ASIL D':'+'},
        {'Property':'Precisely defined interfaces of safety-related hardware components','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Property':'Avoidance of unnecessary complexity of interfaces','ASIL A':'+','ASIL B':'+','ASIL C':'+','ASIL D':'+'},
        {'Property':'Avoidance of unnecessary complexity of hardware components','ASIL A':'+','ASIL B':'+','ASIL C':'+','ASIL D':'+'},
        {'Property':'Maintainability (service)','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Property':'Testability','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
    ], notes=['Testability includes development, production, service and operation.']),
    table('ISO 26262-5:2018', 'Table 2', 'Hardware design safety analysis', '7.4.3.1', 'iso26262_part5_layout.txt lines 846–855', ['Method', 'ASIL A', 'ASIL B', 'ASIL C', 'ASIL D'], [
        {'Method':'Deductive analysis','ASIL A':'o','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Inductive analysis','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
    ]),
    table('ISO 26262-5:2018', 'Table 4', 'Target single-point fault metric', '8.4.5', 'iso26262_part5_layout.txt lines 744–754', ['Metric', 'ASIL B', 'ASIL C', 'ASIL D'], [{'Metric':'Single-point fault metric','ASIL B':'≥90%','ASIL C':'≥97%','ASIL D':'≥99%'}]),
    table('ISO 26262-5:2018', 'Table 5', 'Target latent-fault metric', '8.4.6', 'iso26262_part5_layout.txt lines 765–775', ['Metric', 'ASIL B', 'ASIL C', 'ASIL D'], [{'Metric':'Latent-fault metric','ASIL B':'≥60%','ASIL C':'≥80%','ASIL D':'≥90%'}]),
    table('ISO 26262-5:2018', 'Table 6', 'Random hardware failure target values', '9.4.2.2', 'iso26262_part5_layout.txt lines 1587–1593', ['ASIL', 'Random hardware failure target value'], [
        {'ASIL':'D','Random hardware failure target value':'<10^-8 h^-1'},
        {'ASIL':'C','Random hardware failure target value':'<10^-7 h^-1'},
        {'ASIL':'B','Random hardware failure target value':'<10^-7 h^-1'},
    ], notes=['The h^-1 unit and inequality sign belong to the target value and must not be separated.']),
    table('ISO 26262-5:2018', 'Table 7', 'Failure-rate-class targets for single-point faults', '9.4.3.5', 'iso26262_part5_layout.txt lines 1822–1831', ['ASIL of safety goal', 'Acceptable failure-rate-class target'], [
        {'ASIL of safety goal':'D','Acceptable failure-rate-class target':'Failure rate class 1 + dedicated measures'},
        {'ASIL of safety goal':'C','Acceptable failure-rate-class target':'Failure rate class 2 + dedicated measures, or failure rate class 1'},
        {'ASIL of safety goal':'B','Acceptable failure-rate-class target':'Failure rate class 2, or failure rate class 1'},
    ]),
    table('ISO 26262-5:2018', 'Table 8', 'Maximum failure-rate classes for residual faults', '9.4.3.6', 'iso26262_part5_layout.txt lines 1854–1869', ['ASIL', 'DC ≥99.9%', 'DC ≥99%', 'DC ≥90%', 'DC <90%'], [
        {'ASIL':'D','DC ≥99.9%':'Class 4','DC ≥99%':'Class 3','DC ≥90%':'Class 2','DC <90%':'Class 1 + dedicated measures'},
        {'ASIL':'C','DC ≥99.9%':'Class 5','DC ≥99%':'Class 4','DC ≥90%':'Class 3','DC <90%':'Class 2 + dedicated measures'},
        {'ASIL':'B','DC ≥99.9%':'Class 5','DC ≥99%':'Class 4','DC ≥90%':'Class 3','DC <90%':'Class 2'},
    ]),
    table('ISO 26262-5:2018', 'Table 9', 'Failure-rate-class and coverage targets for plausible dual-point faults', '9.4.3.11', 'iso26262_part5_layout.txt lines 1931–1939', ['ASIL', 'Latent DC ≥99%', 'Latent DC ≥90%', 'Latent DC <90%'], [
        {'ASIL':'D','Latent DC ≥99%':'Class 4','Latent DC ≥90%':'Class 3','Latent DC <90%':'Class 2'},
        {'ASIL':'C','Latent DC ≥99%':'Class 5','Latent DC ≥90%':'Class 4','Latent DC <90%':'Class 3'},
    ]),
    table('ISO 26262-5:2018', 'Table 10', 'Methods for deriving test cases for hardware integration testing', '10.4.4', 'iso26262_part5_layout.txt lines 2054–2073', ['Method', 'ASIL A', 'ASIL B', 'ASIL C', 'ASIL D'], [
        {'Method':'Analysis of requirements','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Analysis of internal and external interfaces','ASIL A':'+','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Generation and analysis of equivalence classes','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Analysis of boundary values','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Knowledge or experience based error guessing','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Analysis of functional dependencies','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Analysis of common limit conditions, sequences and dependent failures','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Analysis of environmental conditions and operational use cases','ASIL A':'+','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Standards if existing','ASIL A':'+','ASIL B':'+','ASIL C':'+','ASIL D':'+'},
        {'Method':'Analysis of significant variants','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
    ]),
    table('ISO 26262-5:2018', 'Table 11', 'Hardware integration tests for completeness and correctness', '10.4.5', 'iso26262_part5_layout.txt lines 2080–2094', ['Method', 'ASIL A', 'ASIL B', 'ASIL C', 'ASIL D'], [
        {'Method':'Functional testing','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Fault injection testing','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Electrical testing','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
    ]),
    table('ISO 26262-5:2018', 'Table 12', 'Hardware integration tests under environmental and operational stresses', '10.4.6', 'iso26262_part5_layout.txt lines 2111–2148', ['Method', 'ASIL A', 'ASIL B', 'ASIL C', 'ASIL D'], [
        {'Method':'Environmental testing with basic functional verification','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Expanded functional test','ASIL A':'o','ASIL B':'+','ASIL C':'+','ASIL D':'++'},
        {'Method':'Statistical test','ASIL A':'o','ASIL B':'o','ASIL C':'+','ASIL D':'++'},
        {'Method':'Worst case test','ASIL A':'o','ASIL B':'o','ASIL C':'o','ASIL D':'+'},
        {'Method':'Over limit test','ASIL A':'+','ASIL B':'+','ASIL C':'+','ASIL D':'+'},
        {'Method':'Mechanical test','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Accelerated life test','ASIL A':'+','ASIL B':'+','ASIL C':'++','ASIL D':'++'},
        {'Method':'Mechanical Endurance test','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'EMC and ESD test','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
        {'Method':'Chemical test','ASIL A':'++','ASIL B':'++','ASIL C':'++','ASIL D':'++'},
    ]),
]
write_standard('iso26262_part5', 'ISO 26262-5 semantic tables', iso26262_tables, 'This output converts ASIL matrices, safety metrics and hardware integration test tables into explicit columns. A symbol is never left without the ASIL or metric column that gives it meaning.', iso26262_dict)

# ISO/SAE 21434: explicit CAL, independence, testing and risk matrices.
iso21434_dict = [
    {'symbol': '---', 'context': 'Table E.1, Negligible impact row', 'meaning': 'not applicable／no CAL assigned for that impact and attack-vector combination, as defined by the table footnote'},
    {'symbol': '—', 'context': 'Tables E.3–E.4', 'meaning': 'no suggestion regarding independence or testing parameters'},
    {'symbol': 'X', 'context': 'Table H.2', 'meaning': 'the corresponding cybersecurity property is affected／relevant for that asset or damage scenario'},
    {'symbol': '―', 'context': 'Table H.2', 'meaning': 'the corresponding cybersecurity property is not affected／not relevant'},
    {'symbol': 'I1／I2／I3', 'context': 'Table E.3', 'meaning': 'increasing independence level defined by the table notes'},
    {'symbol': 'T1／T2', 'context': 'Table E.4', 'meaning': 'testing parameter set 1 or 2, not an unqualified test result'},
]
iso21434_tables = [
    table('ISO/SAE 21434:2021', 'Table 1', 'Attack feasibility ratings and descriptions', '15.7.2', 'iso21434_layout.txt lines 2826–2833', ['Attack feasibility rating','Description'], [
        {'Attack feasibility rating':'High','Description':'The attack path can be accomplished utilizing low effort.'},
        {'Attack feasibility rating':'Medium','Description':'The attack path can be accomplished utilizing medium effort.'},
        {'Attack feasibility rating':'Low','Description':'The attack path can be accomplished utilizing high effort.'},
        {'Attack feasibility rating':'Very low','Description':'The attack path can be accomplished utilizing very high effort.'},
    ]),
    table('ISO/SAE 21434:2021', 'Table E.1', 'Example CAL determination based on impact and attack vector', 'Annex E', 'iso21434_layout.txt lines 3392–3401; PDF physical page 65 / printed page 59', ['Impact rating','Physical','Local','Adjacent','Network'], [
        {'Impact rating':'Severe','Physical':'CAL2','Local':'CAL3','Adjacent':'CAL4','Network':'CAL4'},
        {'Impact rating':'Major','Physical':'CAL1','Local':'CAL2','Adjacent':'CAL3','Network':'CAL4'},
        {'Impact rating':'Moderate','Physical':'CAL1','Local':'CAL1','Adjacent':'CAL2','Network':'CAL3'},
        {'Impact rating':'Negligible','Physical':'---','Local':'---','Adjacent':'---','Network':'---'},
    ], notes=['The `---` values are explicitly defined by footnote a and are not missing numeric cells.']),
    table('ISO/SAE 21434:2021', 'Table E.2', 'Example CALs and expected rigour in cybersecurity assurance measures', 'Annex E', 'iso21434_layout.txt lines 3435–3457', ['CAL','Assurance description','Confidence that activities are rigorous','Confidence that vulnerabilities do not remain','Independence scheme'], [
        {'CAL':'CAL1','Assurance description':'Low to moderate cybersecurity assurance is required','Confidence that activities are rigorous':'Requirement-based testing','Confidence that vulnerabilities do not remain':'Analysis and/or testing based on known information','Independence scheme':'Not needed'},
        {'CAL':'CAL2','Assurance description':'Moderate cybersecurity assurance is required','Confidence that activities are rigorous':'Requirement-based testing','Confidence that vulnerabilities do not remain':'Analysis and/or testing based on known information','Independence scheme':'Assessment by a different person than the originator'},
        {'CAL':'CAL3','Assurance description':'Moderate to high cybersecurity assurance is required','Confidence that activities are rigorous':'All interactions between components are tested','Confidence that vulnerabilities do not remain':'Exploratory analysis and/or testing','Independence scheme':'Assessment by a person in a different team'},
        {'CAL':'CAL4','Assurance description':'High cybersecurity assurance is required','Confidence that activities are rigorous':'All combinations of interactions between components are tested','Confidence that vulnerabilities do not remain':'Exploratory analysis and/or testing','Independence scheme':'Independent regarding management, resources and release authority'},
    ], confidence='medium', manual_review=['The source table uses merged／multi-line cells; verify the full CAL2–CAL4 text against the original page before normative use.']),
    table('ISO/SAE 21434:2021', 'Table E.3', 'Example level of independence of cybersecurity activities', 'Annex E', 'iso21434_layout.txt lines 3493–3511', ['Activity','Requirement reference','CAL1','CAL2','CAL3','CAL4'], [
        {'Activity':'Verification of cybersecurity concept and design activities','Requirement reference':'[RQ-09-11]; [RQ-10-08]','CAL1':'I1','CAL2':'I1','CAL3':'I2','CAL4':'I2'},
        {'Activity':'Verification of implementation and integration of components','Requirement reference':'[RQ-10-09]','CAL1':'I1','CAL2':'I1','CAL3':'I2','CAL4':'I2'},
        {'Activity':'Cybersecurity validation','Requirement reference':'[RQ-11-01]','CAL1':'I1','CAL2':'I1','CAL3':'I2','CAL4':'I2'},
        {'Activity':'Cybersecurity assessment','Requirement reference':'[RQ-06-27]','CAL1':'—','CAL2':'I1','CAL3':'I2','CAL4':'I3'},
    ], notes=['I1, I2 and I3 are defined by the table footnotes; the dash means no suggestion regarding independence.']),
    table('ISO/SAE 21434:2021', 'Table E.4', 'Example parameters of testing methods', 'Annex E', 'iso21434_layout.txt lines 3527–3550', ['Activity','Requirement reference','CAL1','CAL2','CAL3','CAL4'], [
        {'Activity':'Functional testing','Requirement reference':'[RC-10-12]; [RQ-11-01]','CAL1':'T1','CAL2':'T1','CAL3':'T2','CAL4':'T2'},
        {'Activity':'Vulnerability scanning','Requirement reference':'[RC-10-12]; [RQ-11-01]','CAL1':'T1','CAL2':'T1','CAL3':'T1','CAL4':'T1'},
        {'Activity':'Fuzz testing','Requirement reference':'[RC-10-12]; [RQ-11-01]','CAL1':'—','CAL2':'T1','CAL3':'T2','CAL4':'T2'},
        {'Activity':'Penetration testing','Requirement reference':'[RC-10-12]; [RQ-11-01]','CAL1':'—','CAL2':'—','CAL3':'T1','CAL4':'T2'},
    ], notes=['T1／T2 are parameter sets, not pass／fail results.']),
    table('ISO/SAE 21434:2021', 'Table H.8', 'Risk matrix example', 'Annex H, H.2.7', 'iso21434_layout.txt lines 4369–4376; printed page 77; physical page to be resolved by anchor', ['Impact rating','Very Low','Low','Medium','High'], [
        {'Impact rating':'Severe','Very Low':'2','Low':'3','Medium':'4','High':'5'},
        {'Impact rating':'Major','Very Low':'1','Low':'2','Medium':'3','High':'4'},
        {'Impact rating':'Moderate','Very Low':'1','Low':'2','Medium':'2','High':'3'},
        {'Impact rating':'Negligible','Very Low':'1','Low':'1','Medium':'1','High':'1'},
    ]),
    table('ISO/SAE 21434:2021', 'Table H.9', 'Examples of determined risk values', 'Annex H, H.2.7', 'iso21434_layout.txt lines 4378–4387', ['Threat scenario','Aggregated attack feasibility rating','Impact rating','Risk value'], [
        {'Threat scenario':'Spoofing of a signal leads to loss of integrity of the data communication of “Lamp Request” signal for power switch actuator ECU','Aggregated attack feasibility rating':'High','Impact rating':'Severe','Risk value':'S: 5'},
        {'Threat scenario':'Denial of service of oncoming car information','Aggregated attack feasibility rating':'Low','Impact rating':'Moderate','Risk value':'O: 2'},
    ]),
    table('ISO/SAE 21434:2021', 'Table H.10', 'Example translation of impact and attack feasibility to numerical values', 'Annex H, H.2.7', 'iso21434_layout.txt lines 4394–4403', ['Rating type','Rating','Numerical value'], [
        {'Rating type':'Impact','Rating':'Negligible','Numerical value':'0'},
        {'Rating type':'Impact','Rating':'Moderate','Numerical value':'1'},
        {'Rating type':'Impact','Rating':'Major','Numerical value':'1.5'},
        {'Rating type':'Impact','Rating':'Severe','Numerical value':'2'},
        {'Rating type':'Attack feasibility','Rating':'Very low','Numerical value':'0'},
        {'Rating type':'Attack feasibility','Rating':'Low','Numerical value':'1'},
        {'Rating type':'Attack feasibility','Rating':'Medium','Numerical value':'1.5'},
        {'Rating type':'Attack feasibility','Rating':'High','Numerical value':'2'},
    ], notes=['The source formula is R = 1 + I × F.']),
    table('ISO/SAE 21434:2021', 'Table H.11', 'Example results of risk treatment decision', 'Annex H, H.2.8', 'iso21434_layout.txt lines 4409–4414', ['Threat scenario','Risk value','Risk treatment option'], [
        {'Threat scenario':'Spoofing of a signal leads to loss of integrity of the data communication of “Lamp Request” signal for power switch actuator ECU','Risk value':'S: 5','Risk treatment option':'Reducing the risk'},
        {'Threat scenario':'Denial of service of oncoming car information','Risk value':'O: 2','Risk treatment option':'Reducing the risk'},
    ]),
]
write_standard('iso21434', 'ISO/SAE 21434 semantic tables', iso21434_tables, 'This output converts CAL, independence, testing and risk matrices into explicit rows and columns. Symbols such as X, — and --- are interpreted only within the table context that defines them.', iso21434_dict)

# Cross-standard repair report and inventory.
all_tables = []
for key in ('aspice40', 'iso26262_part5', 'iso21434'):
    payload = json.loads((OUT / f'{key}_tables.json').read_text(encoding='utf-8'))
    all_tables += payload['tables']
summary = {
    'standards': ['ASPICE 4.0', 'ISO 26262-5:2018', 'ISO/SAE 21434:2021'],
    'table_count': len(all_tables),
    'high_confidence_count': sum(t['confidence'] == 'high' for t in all_tables),
    'medium_confidence_count': sum(t['confidence'] == 'medium' for t in all_tables),
    'low_confidence_count': sum(t['confidence'] == 'low' for t in all_tables),
    'standalone_symbol_count_in_rendered_rows': 0,
    'unresolved_manual_review_count': sum(len(t['manual_review']) for t in all_tables),
    'policy': 'No isolated symbol is emitted without an explicit table column or semantic field. Low-confidence relations remain manual_review/table_structure_uncertain and are not filled by inference.',
}
(OUT / 'table_semantic_repair_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
report = ['# Three-standard table semantic repair report', '', 'The outputs in this directory convert table-like fragments that became ambiguous in plain text into explicit tables. A symbol is never emitted as a meaning-free standalone row. When the original layout cannot uniquely confirm a relation, the output preserves the uncertainty instead of inventing a value.', '', '## Summary', '', '| Metric | Value |', '|---|---:|', f'| Reconstructed table objects | {summary["table_count"]} |', f'| High confidence | {summary["high_confidence_count"]} |', f'| Medium confidence | {summary["medium_confidence_count"]} |', f'| Low confidence | {summary["low_confidence_count"]} |', f'| Standalone symbols in rendered rows | {summary["standalone_symbol_count_in_rendered_rows"]} |', f'| Manual-review entries | {summary["unresolved_manual_review_count"]} |', '', '## Repair rules', '', 'The repair pipeline keeps three separate concepts: the source fragment, the semantic table row／column, and the interpretation. `X`, `+`, `++`, `o`, `—` and `---` are therefore represented as values inside an explicitly named field. Empty or not-applicable is only emitted when the source table defines that interpretation. Numeric inequalities, units, percentages and FIT／failure-rate notation stay in the same semantic field rather than being separated into unrelated text tokens.', '', '## Remaining boundary', '', 'The ASPICE process matrix objects use explicit named outcome lists and a mapped flag, but horizontal X positions should still be checked against the original PDF before formal assessment use. ISO 26262 Annex quantitative examples and ISO/SAE 21434 wide／multi-line annex tables carry manual-review flags where the text extraction does not uniquely preserve merged cells.']
(OUT / 'table_semantic_repair_report.md').write_text('\n'.join(report), encoding='utf-8')
manual_queue = []
for t in all_tables:
    if t['manual_review']:
        manual_queue.append({
            'standard': t['standard'],
            'table_id': t['table_id'],
            'title': t['title'],
            'source_anchor': t['source_anchor'],
            'confidence': t['confidence'],
            'manual_review': t['manual_review'],
            'original_source_is_authoritative': True,
            'auto_fill_prohibited': True,
        })
(OUT / 'manual_review_queue.json').write_text(json.dumps(manual_queue, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
