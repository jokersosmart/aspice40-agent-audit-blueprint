# SM2514 Blueprint Integration

## Purpose

This checkout is the audit and evidence-governance layer for the `SM2514_ISO26262` project. It does not replace the existing IP Owner authoring workflow, the six-stage HW IP flow pipeline, or human technical sign-off.

The first adoption target is evidence readiness and audit rehearsal for the current documentation-first work products:

1. System requirement and allocation evidence.
2. HW IP requirement and architecture specifications.
3. Normal and safety dynamic-flow diagrams and descriptions.
4. Owner assignment, review and sign-off records.
5. Selected SWE.4 unit-test specifications and traceability blocks.

## Evidence mapping

| SM2514 source | Evidence role | Initial Process focus |
|---|---|---|
| `HW_IP_Spec/` | HW requirement, architecture, interface, safety and traceability evidence | HWE.1, HWE.2, HWE.4, SYS.3 |
| `HW_IP_Flow_Diagrams/` | Golden reference, normal flow, safety flow, description and Owner review evidence | HWE.2, HWE.3, HWE.4, SUP.8, SUP.10 |
| `deliverables/` and `HW_IP_Flow_Diagrams/6. Owner/` | Owner matrix, review and sign-off metadata | SUP.1, SUP.8, SUP.10 |
| `SM2514_Auto/AiWorkSpace/SYS2_ReqDoc/` | System requirements, allocation and traceability evidence | SYS.2, SYS.3 |
| `SM2514_Auto/AiWorkSpace/TestSpec/` | Selected SWE.4 test specifications and traceability | SWE.4 |
| `docs/` | Company workflow rules, templates and review gates | SUP.1, SUP.8, SUP.10 |

The exact path and handling rule for each source is recorded in `config/sm2514_project_adapter.yaml`. The adapter is a mapping contract, not permission to export the source contents.

## Stage and baseline rules

- Stage 1 Golden files are immutable reference evidence. The audit layer may record a hash and source anchor, but must not rewrite, regenerate or “fix” them.
- Stage 2–6 artifacts must retain their sequence pairing and traceability to the same flow.
- A finding about a Stage 2–6 artifact must identify its paired source/description/Owner records when applicable.
- Every run must capture the parent project commit, the Blueprint commit, scope profile version, rule-pack version, schema version and evidence snapshot time.

## Run boundary

Generated snapshots and reports belong under a local `runs/` directory outside this public Blueprint history. They must contain metadata, hashes, source anchors and authorized evidence references; they must not contain raw `Source_file/`, vendor register maps, Flash access sequences, production data or private Owner session logs.

At minimum, a run should contain:

```text
runs/<run-id>/
├── input/scope.yaml
├── input/evidence_snapshot.jsonl
├── input/traceability_snapshot.jsonl
├── outputs/findings/
├── outputs/human_review_queue/
└── manifest.yaml
```

## Human gates

The Blueprint may classify evidence as `unknown`, `partial`, `gap` or `conflict`, but it may not finalize:

- assessment scope or N/A decisions;
- technical correctness or verification adequacy;
- formal N/P/L/F ratings;
- major finding closure;
- release approval or external ASPICE claims.

The current `process_scope.yaml` is therefore a draft adoption profile. Replace the role placeholders only after the project scope owner, QA reviewer and Lead Assessor agree on the assessment context.

## Public repository boundary

The parent project contains potentially NDA-bound source material and implementation details. This public checkout must remain limited to prompts, schemas, rule packs, configuration, metadata mappings and redacted examples. The upstream citation catalog also requires an explicit copyright/distribution review before it is used for any external publication or redistribution.
