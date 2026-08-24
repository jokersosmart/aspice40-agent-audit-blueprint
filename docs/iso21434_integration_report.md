# ISO/SAE 21434:2021 Integration Report

## Executive summary

The Blueprint now contains a cybersecurity extension for ISO/SAE 21434:2021 alongside ASPICE 4.0 and ISO 26262-5. The cybersecurity layer defines 15 logical Cybersecurity Agent roles, three Cybersecurity Manager roles and four shared Runtime boundaries. The full combined design contains 90 logical roles: 8 ASPICE control roles, 32 ASPICE Process roles, 20 Manager roles, 15 ISO 26262 Safety roles and 15 ISO/SAE 21434 Cybersecurity roles.

The cybersecurity extension is designed for an automotive SSD Controller or storage component whose interfaces, firmware, hardware, production provisioning, updates or support lifecycle can affect a road-vehicle E/E system. The extension can also be tailored out when the product and customer context do not make the standard applicable, but that decision requires a recorded human Scope rationale.

## Cybersecurity roles

CS01 covers Scope, terminology and applicability. CS02 covers organizational cybersecurity governance. CS03 covers project-dependent cybersecurity planning. CS04 covers distributed cybersecurity activities and customer／supplier responsibility. CS05 covers continual cybersecurity monitoring. CS06 covers vulnerability analysis and management. CS07 covers item definition, assets, operational environment and TARA. CS08 covers cybersecurity goals and cybersecurity concept. CS09 covers cybersecurity requirements and security architecture. CS10 covers cybersecurity implementation and integration. CS11 covers cybersecurity validation. CS12 covers production cybersecurity. CS13 covers operations, maintenance and incident response. CS14 covers end of cybersecurity support and decommissioning. CS15 covers cybersecurity case, audit／assessment readiness and evidence integrity.

M18 is the Cybersecurity Governance Manager. M19 is the Product Cybersecurity Assurance Manager. M20 is the Cybersecurity Operations and Assurance Manager. They convert cybersecurity findings into controlled work packages but cannot accept residual risk, close a major vulnerability, approve a Cybersecurity Case or make a final cybersecurity claim without the designated human authority.

## Four cybersecurity Runtime boundaries

| Runtime | Roles | Focus |
|---|---|---|
| R15 | CS01–CS04, CS15 | Scope, governance, project, supplier／customer interface, case and audit readiness |
| R16 | CS07–CS11 | Item definition, TARA, goals, concept, requirements, architecture, implementation and validation |
| R17 | CS05, CS06, CS12, CS13 | Monitoring, vulnerability, production, updates and incident response |
| R18 | CS14, CS15, M18, M19, M20 | Cybersecurity Case, end of support, coordination and assurance |

## Direct Spec Citation

Each normative or recommendation-based finding must carry a complete approved ISO/SAE 21434 paragraph or complete table row, its Clause／RQ／RC／PM／WP location, source anchor, source version, quotation SHA-256, applicability explanation, interpretation and human verification state. A reference URL, Clause number or provision ID alone is invalid.

The public repository contains the citation generator and schemas but not the licensed ISO/SAE 21434 standard text. The runtime generator can build a 230-record catalog from an approved local source. If the source is unavailable, stale, structurally ambiguous or hash-inconsistent, the Agent must return `citation_missing` or `source_structure_uncertain` rather than infer a requirement from memory.

## SSD Controller cybersecurity evidence

The evidence model explicitly supports the item and operational environment; assets; host and NAND interfaces; PCIe／NVMe or equivalent interfaces; firmware／FTL; secure boot; firmware authentication; key management; debug and service access; DMA and memory paths; digital RTL; analog／mixed-signal boundaries; simulation／emulation; tape-out／silicon changes; production provisioning; security updates; telemetry; supplier components; vulnerability monitoring; incident response; and end-of-support.

A TARA evidence chain should identify assets, damage scenarios, threat scenarios, attack paths, impact, attack feasibility, risk value, risk treatment, cybersecurity goals, cybersecurity concept, cybersecurity requirements, control allocation, verification measures and residual risk. The Cybersecurity Case should link the approved claims to evidence and retain unresolved assumptions, unknowns, dependencies and human decisions.

## Relationship with ASPICE and ISO 26262-5

ASPICE 4.0 is used for process capability assessment. ISO 26262-5 is used for hardware-level functional-safety product development. ISO/SAE 21434 is used for automotive cybersecurity engineering. A common architecture baseline, simulation result, silicon result, change record, vulnerability record or verification result may be a shared factual Evidence Object, but it cannot automatically prove all three standards. Each standard claim requires a separate direct citation and interpretation.

Examples of complementary interfaces include SYS.1／SYS.2 with item definition and cybersecurity requirements; SYS.3／HWE.1／HWE.2 with security architecture and control allocation; HWE.3／HWE.4 with security control implementation and validation; SUP.8／SUP.9／SUP.10 with cybersecurity configuration, vulnerability and incident change records; and VAL.1 with target-environment cybersecurity validation. The Cross-Standard Mapping schema must classify each relationship as shared, complementary, insufficient, conflict, dependency_missing or no_direct_equivalence.

## Human Security Gates

The Human Review／Approval Gateway is mandatory for item boundary, asset scope, TARA method, impact and attack-feasibility rating, risk treatment, cybersecurity goals, concept, requirements baseline, architecture, control acceptance, vulnerability severity, remediation, production or update release, Cybersecurity Case, assessment readiness and final cybersecurity conclusion.

## Validation

The combined Blueprint validation passes for required files, 32 ASPICE Process IDs, 20 Manager IDs, 15 ISO 26262 Safety IDs, 15 ISO/SAE 21434 Cybersecurity IDs, 90 unique Cognitive assignments, 10 Cognitive Modules, JSON syntax, Runtime uniqueness, R15–R18 presence, R18 role loading and runtime-only standard source boundaries.
