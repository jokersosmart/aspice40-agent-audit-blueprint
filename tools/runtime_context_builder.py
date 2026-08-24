#!/usr/bin/env python3
"""Build and validate a minimal shared-Runtime context.

This module deliberately does not retrieve standards itself. A controlled citation
service must provide citation records that have already passed deterministic checks.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable


class ContextBuildError(ValueError):
    pass


@dataclass(frozen=True)
class Budget:
    model_context_window: int
    input_token_limit: int
    output_token_reserve: int
    validation_token_reserve: int

    @property
    def total_reserved(self) -> int:
        return self.output_token_reserve + self.validation_token_reserve


def approximate_tokens(value: Any) -> int:
    """Conservative preflight estimate; production should use the provider tokenizer."""
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
    return (len(text) + 3) // 4


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_direct_citation(
    citation: dict[str, Any],
    *,
    expected_standard_id: str,
    expected_edition: str,
    source_hash: str,
) -> None:
    """Reject a citation unless the complete approved quote is verifiable."""
    required = {
        "standard_id", "edition", "source_hash", "anchor", "verbatim_text",
        "verbatim_text_sha256", "checks",
    }
    missing = sorted(required - citation.keys())
    if missing:
        raise ContextBuildError(f"citation_missing_fields:{','.join(missing)}")
    if citation["standard_id"] != expected_standard_id or citation["edition"] != expected_edition:
        raise ContextBuildError("source_version_mismatch")
    if citation["source_hash"] != source_hash:
        raise ContextBuildError("source_hash_mismatch")
    quote = citation["verbatim_text"]
    if not isinstance(quote, str) or not quote.strip():
        raise ContextBuildError("quote_incomplete")
    if "�" in quote or "REPLACE-ME" in quote or "PLACEHOLDER" in quote.upper():
        raise ContextBuildError("placeholder_detected")
    if sha256_text(quote) != citation["verbatim_text_sha256"]:
        raise ContextBuildError("hash_mismatch")
    checks = citation["checks"]
    required_checks = {
        "source_version_match", "anchor_resolved", "complete_boundary", "hash_match",
        "no_placeholder", "no_truncation", "table_structure_verified",
    }
    if not required_checks.issubset(checks):
        raise ContextBuildError("citation_validation_incomplete")
    failed = sorted(key for key in required_checks if checks[key] is not True)
    if failed:
        raise ContextBuildError("citation_verification_failed:" + ",".join(failed))


def _citation_block(citations: Iterable[dict[str, Any]], *, standard_id: str, edition: str, source_hash: str) -> list[dict[str, Any]]:
    block: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()
    for citation in citations:
        validate_direct_citation(
            citation,
            expected_standard_id=standard_id,
            expected_edition=edition,
            source_hash=source_hash,
        )
        quote_hash = citation["verbatim_text_sha256"]
        if quote_hash in seen_hashes:
            continue
        seen_hashes.add(quote_hash)
        block.append(citation)
    if not block:
        raise ContextBuildError("citation_missing")
    return block


def build_context(
    *,
    envelope: dict[str, Any],
    global_policy: str,
    role_profile: dict[str, Any],
    scope_snapshot: dict[str, Any],
    rulepack: dict[str, Any],
    citations: list[dict[str, Any]],
    evidence_digest: dict[str, Any],
    shared_state_refs: dict[str, Any],
    output_contract: dict[str, Any],
) -> dict[str, Any]:
    """Build the only context object that should be sent to an LLM invocation."""
    scope = envelope["standard_scope"]
    budget_data = envelope["budget"]
    budget = Budget(
        model_context_window=budget_data["model_context_window"],
        input_token_limit=budget_data["input_token_limit"],
        output_token_reserve=budget_data["output_token_reserve"],
        validation_token_reserve=budget_data["validation_token_reserve"],
    )
    if budget.input_token_limit + budget.total_reserved > budget.model_context_window:
        raise ContextBuildError("invalid_budget_reserves")

    standards = scope["standards"]
    if len(standards) != 1:
        raise ContextBuildError("split_task_by_standard_before_llm")
    standard_id = standards[0]
    source_meta = rulepack.get("source", {})
    edition = source_meta.get("edition")
    source_hash = source_meta.get("source_hash")
    if not edition or not source_hash:
        raise ContextBuildError("source_version_or_hash_missing")

    citation_block = _citation_block(
        citations,
        standard_id=standard_id,
        edition=edition,
        source_hash=source_hash,
    )
    context = {
        "L0_global_policy": global_policy,
        "L1_role_profile": role_profile,
        "L2_scope_and_baseline": scope_snapshot,
        "L3_targeted_rulepack_and_citations": {
            "rulepack": rulepack,
            "spec_citations": citation_block,
        },
        "L4_evidence_digest": evidence_digest,
        "L5_shared_state_refs": shared_state_refs,
        "L6_task_output_contract": output_contract,
        "task": {
            "run_id": envelope["run_id"],
            "task_id": envelope["task_id"],
            "runtime_id": envelope["runtime_id"],
            "agent_id": envelope["agent_id"],
            "question": envelope["question"],
        },
    }
    estimated = approximate_tokens(context)
    if estimated > budget.input_token_limit:
        raise ContextBuildError(f"context_over_budget:{estimated}>{budget.input_token_limit}")
    return {
        "context": context,
        "estimated_input_tokens": estimated,
        "citation_count": len(citation_block),
        "status": "ready_for_llm",
        "llm_must_not_retrieve_or_rewrite_citations": True,
    }


if __name__ == "__main__":
    print("Import build_context() from this module; use Runtime Execution Envelope as input.")
