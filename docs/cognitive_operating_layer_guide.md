# Cognitive Operating Layer Adoption Guide

## Purpose

The Cognitive Operating Layer is a standard, non-normative support layer for the ASPICE 4.0 Agent system. It improves problem framing, evidence review, system analysis, option comparison, communication, risk routing and knowledge continuity. It does not add ASPICE requirements and must never override approved PAM text, customer or OEM requirements, company process rules, approved assessment scope, Evidence Objects or human approvals.

## Loading order

Every runtime loads the following artifacts in order:

1. `prompts/00_global_policy.md`
2. `prompts/05_cognitive_operating_layer.md`
3. `config/agent_cognitive_assignments.json`
4. the role profile
5. the ASPICE Process Rule Pack and Direct Spec Citation Catalog
6. the approved assessment scope and tailoring snapshot
7. Evidence Object and traceability snapshots
8. existing findings and human decisions

The Cognitive Operating Layer can change the order and depth of analysis, but it cannot change the normative source or the evidence status.

## Ten operating modules

| ID | Module | Main use | Typical output |
|---|---|---|---|
| COM-01 | Problem Framing and Scope | Define the decision, boundaries, dependencies and success/failure conditions | decision statement, scope boundary, constraint list |
| COM-02 | Evidence, Source and Quantitative Integrity | Check provenance, uncertainty, reproducibility and missing/conflicting data | claim register, source chain, uncertainty label |
| COM-03 | Hypothesis, Modeling and Controlled Verification | Convert assumptions into testable hypotheses and controlled checks | hypothesis table, experiment plan, result record |
| COM-04 | Decision, Prioritization and Optimization | Compare options under constraints and prioritize reversible, high-value work | option matrix, priority order, decision rationale |
| COM-05 | Counterargument, Bias and Consistency Review | Challenge conclusions and expose unsupported assumptions or inconsistent sources | challenge log, assumption register, conflict record |
| COM-06 | Stakeholder, Interface and Communication Design | Translate technical work into ownership, interfaces and usable actions | stakeholder map, interface map, communication record |
| COM-07 | Systems and Multi-level Causality | Trace dependencies, feedback, second-order impacts and cross-domain effects | system map, change-impact graph, cross-domain risks |
| COM-08 | Learning, Reuse and Knowledge Continuity | Preserve validated decisions, failure modes and reusable assets with context | decision record, lesson record, retrieval test |
| COM-09 | Responsibility, Ethics and Authority | Keep accountability, independence, approval authority and sensitive-data controls explicit | accountability map, independence check, human gate |
| COM-10 | Reversible Experiment, Stop and Escalation | Define pilots, rollback, expansion gates and escalation conditions | pilot plan, rollback plan, escalation record |

## Assignment rules

C01–C08 use the assignments in `config/agent_cognitive_assignments.json`. The 32 Process Auditors use a Process-family emphasis while sharing the same core behavior contract. Requirement and design Processes emphasize COM-01, COM-02, COM-03, COM-05, COM-06, COM-07 and COM-09. Verification Processes add COM-10 and strengthen controlled measurement, reproducibility and independent review. Management and support Processes add COM-04, COM-06, COM-08 and COM-10. MLE Processes are conditional on Scope and emphasize data/model integrity, reproducibility and model risk.

The 14 Managers use the same modules but with domain-specific emphasis. System, Firmware and Hardware Managers coordinate responsibilities and interfaces. Digital Hardware, Analog/Mixed-Signal, Simulation/Emulation and Tape-out/Silicon Managers specialize the evidence and change-impact questions without creating new ASPICE Processes. System Verification, Firmware Verification and Hardware Verification Managers must preserve independent verification and technical review boundaries. QA, configuration/change, project/risk and supplier/release/reuse Managers focus on evidence continuity, change impact, risk and closure authority.

## Required behavior for every normative conclusion

Before stating that an ASPICE indicator is satisfied, partially satisfied or a gap, the Agent must:

1. define the claim and the applicable Scope;
2. attach the complete approved ASPICE source paragraph or complete table row in `spec_citations`;
3. attach Evidence Object identifiers, revision, baseline, owner and review state;
4. separate PAM text, company rule, customer requirement, product context and inference;
5. inspect at least one alternative explanation or counterexample for material findings;
6. preserve `unknown`, `conflict`, `partial`, `gap`, `not_in_scope` and `citation_missing` as distinct statuses;
7. specify the owner, independent verifier, reviewer, action, success criterion and re-verification method;
8. route scope decisions, technical correctness, verification adequacy, formal ratings, major finding closure, release approval and source conflicts to human Gate.

The output must not cite the Cognitive Operating Layer as the reason that an ASPICE requirement exists. It may state that the layer was used to structure the analysis, but the normative basis must remain the direct ASPICE citation and the approved evidence.

## Maintenance and change control

Changes to a module, module assignment, prompt or stop condition are configuration-controlled changes. A change record must identify the old version, new version, rationale, affected runtimes and expected impact. A small reversible pilot should be used before changing all Process Auditors. The pilot must compare false positives, false negatives, unresolved conflicts, review effort, evidence completeness and re-verification quality. A change must not be promoted when it improves an internal score while reducing traceability, independent review or human visibility.

## Privacy and source neutrality

User-visible files and Agent outputs use neutral engineering terminology and do not contain personal attribution or personal-source metadata. Internal provenance of the configuration may be maintained in access-controlled change records, but it is not part of the normative audit result. This separation does not hide evidence: every ASPICE claim remains directly auditable through its complete source quotation, location, hash and verification state.
