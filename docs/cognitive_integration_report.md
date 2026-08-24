# ASPICE 4.0 Agent Cognitive Operating Layer Integration Report

## Executive summary

The combined ASPICE 4.0 and ISO 26262-5 Agent Blueprint now contains a **Cognitive Operating Layer** that is loaded by all 72 logical Agent roles. The layer provides standard engineering behavior for problem framing, evidence analysis, system reasoning, decision support, communication, risk escalation and knowledge continuity. It is explicitly marked as `non_normative_support_layer` and cannot add, remove or reinterpret an ASPICE requirement.

The implementation uses 10 reusable modules and a role-specific assignment file. The 8 ASPICE control roles, 32 Process Auditors, 17 Managers and 15 ISO 26262 Safety roles retain their existing scope and accountability boundaries; the Cognitive Operating Layer changes how they ask questions, challenge evidence, compare options and route uncertainty.

## Layer precedence

| Priority | Source or decision authority | Agent treatment |
|---:|---|---|
| 1 | Approved ASPICE 4.0 source, customer/OEM requirement and approved company rule | Normative or authorized basis |
| 2 | Approved assessment Scope, tailoring, release/baseline and Evidence Object | Determines applicability and factual state |
| 3 | QA, Process Owner, Verification Owner, project authority and Lead Assessor | Human decision and approval authority |
| 4 | Cognitive Operating Layer | Structures analysis and collaboration; non-normative |
| 5 | Model inference and general advice | Must be labeled and cannot override higher levels |

## Ten modules

| ID | Module | Main question |
|---|---|---|
| COM-01 | Problem Framing and Scope | What exactly is being decided or verified, and what is in or out of scope? |
| COM-02 | Evidence, Source and Quantitative Integrity | What is the original source, how complete is it, and can the result be reproduced? |
| COM-03 | Hypothesis, Modeling and Controlled Verification | What competing explanations exist, and what controlled observation can distinguish them? |
| COM-04 | Decision, Prioritization and Optimization | Which option best balances constraint, risk, value, reversibility and verification burden? |
| COM-05 | Counterargument, Bias and Consistency Review | What alternative explanation, contradiction or hidden assumption could invalidate the conclusion? |
| COM-06 | Stakeholder, Interface and Communication Design | Who produces, verifies, approves or is affected, and what must each party receive? |
| COM-07 | Systems and Multi-level Causality | What dependencies, feedback, second-order effects and cross-domain impacts exist? |
| COM-08 | Learning, Reuse and Knowledge Continuity | What validated result, failure mode or decision can be reused with its context? |
| COM-09 | Responsibility, Ethics and Authority | Who is accountable, independent, authorized and responsible for the final decision? |
| COM-10 | Reversible Experiment, Stop and Escalation | What is the smallest safe test, and what conditions require rollback or human escalation? |

## Agent assignment

The file `config/agent_cognitive_assignments.json` contains exactly 72 assignments. Process Auditors are grouped by the type of work they perform: requirements/design, verification, management/support and conditional machine-learning processes. Managers receive domain emphasis for System, Firmware, Digital Hardware, Analog/Mixed-Signal, Simulation/Emulation, Tape-out/Silicon, Verification, QA, Configuration/Change, Project/Risk, Supplier/Release/Reuse, Functional Safety, Hardware Safety Assurance and Safety Verification／Confirmation. ISO 26262 Safety roles receive additional emphasis on direct safety citation, ASIL／Scope dependency, safety evidence, quantitative assumptions, alternative explanations and mandatory human safety review.

The assignments do not expose personal attribution or source metadata in user-visible Agent outputs. They use neutral engineering names and are loaded by the Runtime Registry.

## Required behavior for normative findings

A Process or Manager Agent may use the Cognitive Operating Layer to structure analysis, but each normative conclusion must still include the complete approved ASPICE source paragraph or complete table row in `spec_citations`, together with location, hash, interpretation, evidence references, status and human confirmation state. A module cannot substitute for a missing citation or make a product practice into a PAM requirement.

When evidence is incomplete, the Agent must preserve `unknown`, `partial`, `conflict`, `gap`, `not_in_scope` and `citation_missing` as distinct states. It must not fill an unknown field from model memory. When a change affects a release, tape-out, production data, customer delivery, formal rating, assessment scope or major finding closure, the Agent must route the action to a human Gate.

## Verification result

The static Blueprint validation passed after integration. The verification covers 32 ASPICE Process IDs, 17 Manager IDs, 15 ISO 26262 Safety IDs, 72 unique assignments, 10 Cognitive Modules, required Prompt／Guide／schema files, 32 ASPICE direct-citation Rule Packs, ISO 26262-5 runtime-only source boundaries, JSON syntax and source-neutrality checks. The combined validation output is stored in `docs/combined_blueprint_validation.json`.

## Files to load in production

| Order | File |
|---:|---|
| 1 | `prompts/00_global_policy.md` |
| 2 | `prompts/05_cognitive_operating_layer.md` |
| 3 | `config/agent_cognitive_assignments.json` |
| 4 | Agent profile |
| 5 | ASPICE Process Rule Pack and Direct Spec Citation Catalog |
| 6 | ISO 26262-5 Scope, dependency and runtime citation configuration |
| 7 | Agent profile and Safety profile |
| 8 | Scope and tailoring snapshot |
| 9 | Evidence Object and traceability snapshot |
| 10 | Existing findings and human decisions |

## Maintenance rule

Any change to a module, assignment, Prompt, stop condition or Runtime Registry entry is a configuration-controlled change. It requires a revision, rationale, affected-runtime analysis and a reversible pilot. Promotion requires evidence that traceability, independent verification, human visibility and finding quality have not degraded.
