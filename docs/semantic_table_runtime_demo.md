# Semantic Table Runtime Demo

## Purpose

This document demonstrates how a shared Runtime serves 90 logical roles without loading all role profiles, all Rule Packs, or all semantic tables into one LLM context. The Runtime activates one role for one bounded task, queries only the required table rows, and blocks the LLM until the complete normative citation has passed deterministic verification.

The executable example is `tools/semantic_table_runtime_demo.py`. It uses `knowledge/semantic_tables/aspice40_tables.json` and demonstrates an HWE.2 query for BP5.

## Execution sequence

```text
agent_id + task
  -> runtime dispatch
  -> load one role profile
  -> query one semantic table and only matching rows
  -> load evidence digest and immutable references
  -> resolve complete direct citations from a controlled source
  -> validate source version, anchor, boundary, quote hash and table structure
  -> assemble minimal Runtime context
  -> call the LLM once
  -> validate the LLM output against the output schema
```

The semantic table is a navigation and structured-meaning layer. It is not a replacement for the complete normative quotation. A semantic row such as `BP5 / O3 / mapped=true` helps the Runtime find the relevant provision, but `verbatim_text` must still be supplied by the controlled citation service before the LLM is called.

## Concrete query

The following command queries only the HWE.2 matrix row whose Row ID is BP5 and emits only four columns:

```bash
python3 tools/semantic_table_runtime_demo.py \
  --table-file knowledge/semantic_tables/aspice40_tables.json \
  --table-id 'HWE.2 matrix' \
  --row-contains BP5 \
  --columns 'Row ID' Name 'Mapped Outcomes' Mapped \
  --limit 3 \
  --citation-jsonl examples/hwe2_runtime_citations_demo.jsonl \
  --source-hash 49a7716ce46be211e78139a1fbcdc4e17c011d7d8e429c94d6ddffd2221f7c5a
```

The important implementation is row-scoped retrieval:

```python
store = SemanticTableStore(table_file)
selected = store.query(
    table_id="HWE.2 matrix",
    row_contains=["BP5"],
    columns=["Row ID", "Name", "Mapped Outcomes", "Mapped"],
    limit=3,
)
```

`SemanticTableStore.query()` does not serialize `store.payload` downstream. It returns a new object containing only the selected table metadata, declared columns, matching rows, source anchor, confidence, notes, and manual-review state.

## Citation safety gate

The citation path is intentionally separate from table retrieval:

```python
citations = load_verified_citations(
    citation_jsonl,
    requested_anchors={"BP5", "HWE.2.BP5"},
    standard_id="ASPICE",
    edition="4.0",
    source_hash=approved_source_hash,
)

context = build_minimal_context(
    role_id="HWE.2",
    runtime_id="R06",
    question="Check whether the hardware requirement-to-design mapping is bidirectional and consistent.",
    scope={"standards": ["ASPICE"], "scope_state": "in_scope", "baseline_id": "HW-BL-042"},
    table_result=selected,
    evidence_digest=[{"artifact_id": "HW-ARCH-001", "baseline": "HW-BL-042", "status": "approved"}],
    citations=citations,
    input_limit=16000,
)
```

`verify_citation_record()` rejects a record when the source version, source hash, anchor, start/end boundary, complete quotation, quotation hash, placeholder status, truncation status, or table structure is not valid. When no verified citation is available, the result is `citation_missing_before_llm` and no LLM call is allowed.

## Token-saving measurement

The demo was executed with the repository's ASPICE table JSON and an approved HWE.2 citation record. The measured values were:

| Context | Measured tokens |
|---|---:|
| Full `aspice40_tables.json` | 19,700 |
| Targeted HWE.2 BP5 row with four named columns | 172 |
| Ready-for-LLM context including role, scope, evidence digest, output contract and complete citation | 609 |

The table-only reduction is 99.13 percent: `(19,700 - 172) / 19,700`. The ready-for-LLM context is still small because it contains one role, one task, one evidence digest, one targeted table row, and one complete direct citation. The percentage is a measurement for this query, not a universal promise; production must measure with the tokenizer of the selected provider and record the result in `Runtime Observation`.

The code uses `tiktoken` when installed and otherwise falls back to a conservative character estimate for preflight only. The production path should pin the provider tokenizer, model version, and encoding in the Runtime Observation record.

## Why the citation does not get compressed

The following items may be compressed or referenced by immutable ID: role profiles, repeated Evidence metadata, traceability graph nodes outside the one-hop task subgraph, previous findings, and duplicated citation records. The following item may not be compressed: the normative quotation itself. It cannot be replaced by a summary, citation ID, page number, embedding, or model-generated paraphrase. If the complete quotation does not fit the budget, the Runtime creates child tasks by standard, Clause／Process, evidence domain, or work package.

## Shared Runtime request boundary

A Runtime request should look like this conceptually:

```json
{
  "runtime_id": "R06",
  "agent_id": "HWE.2",
  "standard_scope": {
    "standards": ["ASPICE"],
    "process_or_clause_ids": ["HWE.2"],
    "scope_state": "in_scope",
    "baseline_id": "HW-BL-042"
  },
  "context_refs": {
    "role_profile_ref": "profile:HWE.2:v1",
    "rulepack_refs": ["rulepack:ASPICE:HWE.2:v4.0"],
    "evidence_snapshot_ref": "evidence-snapshot:HW-BL-042",
    "traceability_snapshot_ref": "traceability:HWE.2:HW-BL-042"
  },
  "citation_request": {
    "retrieval_mode": "provision_id",
    "anchors": ["HWE.2.BP5"],
    "require_complete_verbatim": true,
    "source_version": "ASPICE 4.0",
    "deduplicate_by_hash": true
  }
}
```

The envelope carries references and bounded queries. It does not carry the full table store. The Context Builder resolves those references into a minimal, validated Context immediately before the LLM call and discards the assembled prompt after the invocation unless the approved audit log requires it.

## Failure states

| Failure | Runtime behavior |
|---|---|
| `table_not_found` or `no_matching_rows` | Stop and route to a retrieval／scope correction task. |
| `citation_missing` | Stop before LLM; request controlled source resolution. |
| `source_version_mismatch` or `source_hash_mismatch` | Stop; do not mix editions or source baselines. |
| `anchor_unresolved` or `quote_incomplete` | Stop; send to source custodian or Human Review Gateway. |
| `hash_mismatch` or `placeholder_detected` | Stop; reject the citation record. |
| `table_structure_uncertain` | Preserve original source image／layout and require human confirmation. |
| `context_over_budget` | Split by standard, Clause／Process, evidence domain, or work package; never drop the citation block. |

## Files

- `tools/semantic_table_runtime_demo.py`: executable Table query, token measurement, citation gate and minimal Context builder.
- `examples/hwe2_runtime_citations_demo.jsonl`: controlled demo citation record with complete quotation, boundary, quote hash, source hash and checks.
- `docs/semantic_table_runtime_demo_output.json`: measured execution output with a verified citation and `ready_for_llm`.
- `docs/semantic_table_runtime_demo_blocked_output.json`: negative test showing that a table query without a verified citation exits with a blocking status and must not call the LLM.
- `schemas/runtime-execution-envelope.schema.json`: request boundary for one Runtime invocation.
- `schemas/citation-verification-result.schema.json`: deterministic citation result contract.
- `schemas/shared-state-snapshot.schema.json`: immutable cross-Runtime references.
- `config/token_budget_policy.yaml`: token budgets and forbidden compression rules.
- `config/runtime_dispatch_policy.yaml`: role-to-Runtime routing and split policy.
