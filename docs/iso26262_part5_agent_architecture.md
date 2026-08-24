# ISO 26262-5 Agent Extension for SSD Controller

## 1. Design decision

The existing ASPICE Blueprint should not create one undifferentiated “ISO Agent”. ISO 26262-5:2018 addresses different engineering decisions: safety planning, hardware safety requirements, hardware architecture, detailed design, safety analysis, architectural metrics, random hardware failure evaluation, hardware integration, qualification and lifecycle information. These decisions require different evidence, technical owners and human approval authorities.

The recommended extension adds **15 logical roles** and deploys them through four Safety runtimes. The roles are logical responsibilities, not 15 independent services.

| Layer | Logical roles | Runtime strategy |
|---|---:|---|
| Clause-focused Safety／Hardware roles | FS01–FS11 | Shared Clause Audit Runtime and Quantitative Safety Runtime |
| Evidence and cross-standard control | FS12–FS13 | Shared Evidence and Cross-Standard Runtime |
| Safety coordination and confirmation | FS14–FS15 | Shared Functional Safety Coordination Runtime |
| **Total** | **15** | **4 additional Safety runtimes** |

## 2. Clause-to-Agent map

| ISO 26262-5 scope | Agent | Primary responsibility | Main SSD Controller evidence |
|---|---|---|---|
| Clauses 1–4 | FS01 | Scope, compliance claim, tailoring, ASIL table interpretation | item definition, safety scope, tailoring rationale |
| Clause 5 | FS02 | Hardware safety activity planning and hardware/software coordination | safety plan, lifecycle plan, responsibility map |
| Clause 6 | FS03 | Hardware safety requirements, verification criteria and HSI refinement | HSR, HSI, allocated technical safety requirements |
| Clause 7.4.1 | FS04 | Hardware architecture, requirement allocation and ASIL allocation/decomposition | architecture, allocation matrix, decomposition record |
| Clause 7.4.2 | FS05 | Detailed design safety mechanisms, mission profile and operating conditions | RTL, analog, IP, safety mechanisms and design review |
| Clause 7.4.3 | FS06 | FMEA/FMEDA/FTA/DFA, failure modes and dependent failures | safety analysis, fault classification and fault injection |
| Clause 7.4.4 | FS07 | Hardware design verification, assumptions and re-verification | formal, simulation, lab, review and change verification |
| Clause 7.4.5 | FS08 | Production, operation, service and decommissioning safety information | production, service, field feedback and special characteristics |
| Clause 8 and Annex C–E | FS09 | SPFM, LFM, diagnostic coverage and metric calculations | failure-rate data, metric calculations and independent recalculation |
| Clause 9 and Annex F–H | FS10 | PMHF, EEC, safety-goal violations and latent-fault handling | PMHF/EEC model, budget and latent-fault analysis |
| Clause 10 | FS11 | Hardware integration, qualification, durability and stress testing | integration tests, AEC-Q/equivalent qualification, EMC/ESD and stress results |
| All clauses and Annexes | FS12 | Approved source, direct citation, table preservation and source hash | source manifest, citation catalog, correction record |
| ASPICE × ISO 26262 | FS13 | Cross-standard traceability, shared evidence and conflict detection | crosswalk, evidence graph, conflict register |
| All in-scope clauses | FS14 | Safety assessment orchestration and safety-case draft assembly | assessment plan, finding register and human review queue |
| Independent confirmation | FS15 | Independence, confirmation measures, review assignment and re-verification | confirmation records, reviewer assignment and release decision record |

## 3. Runtime deployment

The four additional runtime boundaries are as follows.

| Runtime | Logical roles | Function | Required human gates |
|---|---|---|---|
| R11 ISO 26262-5 Clause Audit | FS01–FS08, FS11 | Clause-by-clause requirement and evidence analysis | Scope, ASIL, HSR/HSI, architecture, analysis method, verification adequacy and qualification |
| R12 Quantitative Safety Analysis | FS09–FS10 | SPFM/LFM, diagnostic coverage, PMHF and EEC evidence | calculation method, input data, independent recalculation, metric result and residual risk |
| R13 Evidence and Cross-Standard | FS12–FS13 | Licensed-source citation, evidence normalization, ASPICE mapping and conflict detection | source version, citation correction, crosswalk approval and conflict disposition |
| R14 Safety Coordination | FS14–FS15 | Safety work packages, independence, confirmation and safety review queue | safety plan, independent confirmation, residual risk, tape-out/release and final conclusion |

R10 remains the Human Review and Approval Gateway. It is not replaced by an Agent.

## 4. Direct citation contract

Every normative ISO 26262 finding must directly carry the complete approved source paragraph or complete table row. A citation must include the standard identifier, edition, Part, clause or requirement, source anchor, page or line, verbatim text, SHA-256 hash, applicability explanation, interpretation and human verification status. A clause ID, link or paraphrase alone is insufficient.

The public repository contains only the citation contract, runtime extraction tool, profiles and metadata. It does not contain the licensed ISO 26262 PDF or a full verbatim quotation catalog. FS12 loads the approved local source at runtime. If the source is unavailable, the result is `citation_missing`; if a conclusion depends on a missing ISO 26262 Part, the result is `dependency_missing`.

## 5. ASPICE interface rule

ASPICE and ISO 26262 are complementary but not interchangeable. A shared evidence item may be linked to both models, but each model retains its own claim and citation. For example, a hardware design review may support an ASPICE HWE activity and an ISO 26262 hardware design verification claim, but the Agent must attach the relevant ASPICE original text and ISO 26262 original text separately and explain whether the relationship is shared, complementary, insufficient or conflicting.

The cross-standard relationship must never be represented as “ASPICE passed, therefore ISO 26262 passed” or “ISO 26262 analysis exists, therefore the ASPICE Process outcome is satisfied.” FS13 must preserve the distinction.

## 6. SSD Controller evidence boundaries

Digital RTL, analog/mixed-signal blocks, NAND/PHY interfaces, ECC/LDPC, clock/reset/power domains, controller firmware interaction, simulation/emulation, formal checks, lab qualification, tape-out changes and silicon characterization are evidence domains. They are not automatically safety evidence. A product artifact becomes safety evidence only when its safety relevance, scope, version, owner, review state, assumptions, verification method and relationship to the cited requirement are established.

For quantitative results, the evidence package must preserve the formula or table row, data source, failure-rate assumptions, classification rule, calculation tool and version, independent recalculation, sensitivity or boundary assumptions and human approval. A number without its method and assumptions is incomplete.

## 7. Human-only decisions

Agents may prepare evidence and propose a review queue. Human authority remains mandatory for Scope and ASIL applicability, tailoring, HSR/HSI approval, ASIL allocation or decomposition, safety mechanisms, safety-analysis method, SPFM/LFM/diagnostic coverage/PMHF/EEC results, dependent-failure disposition, residual-risk acceptance, qualification acceptance, tape-out or production release, unresolved safety anomaly closure and final safety conclusion.

## 8. Recommended implementation sequence

First, deploy FS12 and FS01–FS03 with the local approved source and citation contract. This establishes Scope, direct source quotation and hardware safety requirements before numerical analysis begins. Second, deploy FS04–FS08 and FS11 to connect architecture, detailed design, safety analysis, verification and qualification to the SSD Controller evidence graph. Third, deploy FS09–FS10 for quantitative metrics and random hardware failure analysis only after the project provides approved failure-rate, diagnostic-coverage and ASIL inputs. Fourth, deploy FS13–FS15 for cross-standard traceability, independent confirmation and safety-case rehearsal.

This ordering prevents the organization from calculating metrics before the safety requirements, architectural boundaries, failure classifications and assumptions have been approved.
