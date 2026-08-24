# ISO/SAE 21434:2021 Agent Architecture Extension

## Purpose

This document defines the ISO/SAE 21434:2021 cybersecurity extension for the SSD Controller Agent Blueprint. It operates beside, not inside, the ASPICE 4.0 Process model and the ISO 26262-5 functional-safety model. The three standards can share factual Evidence Objects when scope, baseline, ownership and version match, but one standard's evidence never automatically proves another standard's claim.

## Logical roles

The extension adds 15 Cybersecurity Agent roles: CS01 Scope and Terminology; CS02 Organizational Governance; CS03 Project Cybersecurity Management; CS04 Distributed Cybersecurity Responsibility; CS05 Continual Cybersecurity Monitoring; CS06 Vulnerability Analysis and Management; CS07 Item Definition and TARA; CS08 Cybersecurity Goals and Concept; CS09 Cybersecurity Requirements and Architecture; CS10 Cybersecurity Implementation and Integration; CS11 Cybersecurity Validation; CS12 Production Cybersecurity; CS13 Operations, Maintenance and Incident Response; CS14 End of Support and Decommissioning; and CS15 Cybersecurity Case, Audit and Evidence.

The extension adds three Manager roles. M18 coordinates organizational governance, project planning and customer／supplier responsibility. M19 coordinates item definition, TARA, cybersecurity goals, concept, requirements, architecture, implementation and validation. M20 coordinates monitoring, vulnerability management, incidents, updates, production security, support lifecycle, cybersecurity case and assessment readiness.

These 18 roles are logical accountability boundaries, not 18 independent services. They are loaded through shared R15–R18 runtimes and the same Cognitive Operating Layer used by the existing Blueprint.

## Runtime design

| Runtime | Logical roles | Primary purpose | Human Gate examples |
|---|---|---|---|
| R15 | CS01–CS04, CS15 | Scope, governance, project, supplier／customer interface, case and audit readiness | Scope, policy, tailoring, supplier agreement, assessment decision, case review |
| R16 | CS07–CS11 | Item definition, TARA, goals, concept, requirements, architecture, implementation and validation | TARA scope, risk treatment, concept, requirement baseline, architecture, validation adequacy |
| R17 | CS05, CS06, CS12, CS13 | Monitoring, vulnerability, production, updates and incident response | Vulnerability severity, remediation, patch release, incident disposition, support end |
| R18 | CS14, CS15, M18, M19, M20 | Cybersecurity coordination, case, operations and assurance | Major vulnerability, case release, update, assessment readiness, final security conclusion |

## ISO/SAE 21434 evidence chain

The minimum product evidence chain is: item definition and operational environment; assets and interfaces; damage and threat scenarios; attack paths; impact and attack-feasibility ratings; risk value and treatment; cybersecurity goals; cybersecurity concept; cybersecurity requirements; security controls; architecture and weakness analysis; secure firmware／RTL／analog boundary implementation; integration and verification; penetration／fuzz／abuse-case evidence; production provisioning; monitoring; vulnerability and incident records; update evidence; end-of-support and decommissioning records; and the cybersecurity case.

For the SSD Controller, the evidence domain must explicitly include host and NAND interfaces, PCIe／NVMe or equivalent interfaces, FTL and firmware update paths, secure boot, key management, debug and service access, DMA and memory paths, digital RTL, analog／mixed-signal boundaries, simulation／emulation, tape-out／silicon changes, manufacturing provisioning, telemetry, supplier components and support lifecycle.

## Direct citation and licensing boundary

Every normative cybersecurity finding and Cybersecurity Case claim must carry the complete approved source paragraph or complete table row, the RQ／RC／PM／WP or Clause anchor, source version, source hash, quotation hash, applicability explanation, interpretation and human verification state. A reference link or provision ID alone is invalid.

The public repository stores profiles, schemas, Prompt templates, Clause anchors, runtime citation generators, examples and metadata. It does not store the licensed ISO/SAE 21434 standard text. At execution time, the Agent loads the complete text from an approved local source and stops with `citation_missing`, `source_structure_uncertain` or `dependency_missing` when the source or required context is unavailable.

## Cross-standard rule

ASPICE 4.0 focuses on process capability assessment. ISO 26262-5 focuses on hardware-level functional-safety product development. ISO/SAE 21434 focuses on cybersecurity engineering across organization, project, concept, product development, validation, production, operations, maintenance and decommissioning. Their work products may be linked in one evidence graph, but findings remain standard-specific. A shared architecture, simulation result, silicon result, change record or verification result must be mapped separately to each applicable requirement with separate direct citations.

## Human Security Gates

The Agents may prepare and challenge evidence. Human authority remains required for item scope, asset scope, TARA method, impact and attack-feasibility ratings, risk treatment and residual risk, cybersecurity goals, concept, requirements baseline, architecture, security control acceptance, vulnerability severity, remediation, production／update release, cybersecurity case, assessment readiness and final cybersecurity conclusion.

## Dependencies

The provided source is ISO/SAE 21434:2021(E). Clause 2 identifies ISO 26262-3:2018 as a normative reference. Complete claims may also require the customer／OEM context, the complete ISO 26262 dependency set, other ISO/SAE 21434 source context and evidence from vehicle-level validation. If those are not loaded, the Agent must preserve `dependency_missing` and must not claim compliance.
