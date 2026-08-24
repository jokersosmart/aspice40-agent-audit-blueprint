#!/usr/bin/env python3
"""Minimal shared-Runtime query demo for semantic standard tables.

The important safety rule is that semantic tables are navigation data. A Runtime
may use them to find the smallest relevant rows, but it must not treat them as a
replacement for a verified normative quotation. A verified citation gateway must
supply the complete quotation before an LLM invocation is allowed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[1]
DEFAULT_TABLE_FILE = REPO / "knowledge/semantic_tables/aspice40_tables.json"
DEFAULT_BUDGET = 16_000


class RuntimeBlocked(RuntimeError):
    """The Runtime must not call the LLM until this condition is resolved."""


def as_text(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def token_count(value: Any, model: str = "gpt-4o-mini") -> int:
    """Use the provider tokenizer when installed; otherwise use a conservative estimate."""
    text = as_text(value)
    try:
        import tiktoken  # type: ignore

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except Exception:
        # This is only a preflight fallback. Production should pin the provider tokenizer.
        return (len(text) + 3) // 4


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class SemanticTableStore:
    """Index semantic tables once; never serialize the whole store into a prompt."""

    def __init__(self, path: Path):
        self.path = path
        self.payload = json.loads(path.read_text(encoding="utf-8"))
        self.tables = {table["table_id"]: table for table in self.payload["tables"]}

    def get(self, table_id: str) -> dict[str, Any]:
        try:
            return self.tables[table_id]
        except KeyError as exc:
            raise RuntimeBlocked(f"table_not_found:{table_id}") from exc

    def query(
        self,
        *,
        table_id: str,
        row_contains: Iterable[str] = (),
        columns: Iterable[str] | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        table = self.get(table_id)
        terms = [term.casefold() for term in row_contains]
        selected_columns = list(columns or table["columns"])
        unknown_columns = sorted(set(selected_columns) - set(table["columns"]))
        if unknown_columns:
            raise RuntimeBlocked(f"unknown_table_columns:{','.join(unknown_columns)}")

        selected_rows = []
        for row in table.get("rows", []):
            row_text = as_text(row).casefold()
            if all(term in row_text for term in terms):
                selected_rows.append({column: row.get(column, "") for column in selected_columns})
            if len(selected_rows) >= limit:
                break

        if not selected_rows:
            raise RuntimeBlocked(f"no_matching_rows:{table_id}")

        # This is the only table object that may be passed downstream.
        return {
            "standard": table["standard"],
            "table_id": table["table_id"],
            "title": table["title"],
            "clause": table["clause"],
            "source_anchor": table["source_anchor"],
            "confidence": table["confidence"],
            "columns": selected_columns,
            "rows": selected_rows,
            "manual_review": table.get("manual_review", []),
            "notes": table.get("notes", []),
        }


def verify_citation_record(
    record: dict[str, Any],
    *,
    standard_id: str,
    edition: str,
    source_hash: str,
) -> dict[str, Any]:
    """Verify a complete citation record without asking an LLM to rewrite it."""
    quote = record.get("verbatim_text", "")
    checks = record.get("checks", {})
    required_checks = {
        "source_version_match",
        "anchor_resolved",
        "complete_boundary",
        "hash_match",
        "no_placeholder",
        "no_truncation",
        "table_structure_verified",
    }
    missing = sorted(required_checks - set(checks))
    if missing:
        raise RuntimeBlocked(f"citation_validation_incomplete:{','.join(missing)}")
    if record.get("standard_id") != standard_id or record.get("edition") != edition:
        raise RuntimeBlocked("source_version_mismatch")
    if record.get("source_hash") != source_hash:
        raise RuntimeBlocked("source_hash_mismatch")
    if not quote or "�" in quote or "REPLACE-ME" in quote or "PLACEHOLDER" in quote.upper():
        raise RuntimeBlocked("placeholder_or_empty_citation")
    if any(checks[name] is not True for name in required_checks):
        raise RuntimeBlocked("citation_verification_failed")
    if sha256_text(quote) != record.get("verbatim_text_sha256"):
        raise RuntimeBlocked("citation_hash_mismatch")
    return record


def load_verified_citations(
    path: Path,
    *,
    requested_anchors: set[str],
    standard_id: str,
    edition: str,
    source_hash: str,
) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeBlocked(f"invalid_citation_jsonl:{line_number}") from exc
        anchor = record.get("anchor", "")
        if isinstance(anchor, dict):
            anchor = anchor.get("indicator_id") or anchor.get("section") or ""
        if requested_anchors and str(anchor) not in requested_anchors:
            continue
        records.append(
            verify_citation_record(
                record,
                standard_id=standard_id,
                edition=edition,
                source_hash=source_hash,
            )
        )
    if not records:
        raise RuntimeBlocked("citation_missing")
    return records


def build_minimal_context(
    *,
    role_id: str,
    runtime_id: str,
    question: str,
    scope: dict[str, Any],
    table_result: dict[str, Any],
    evidence_digest: list[dict[str, Any]],
    citations: list[dict[str, Any]],
    input_limit: int = DEFAULT_BUDGET,
    model: str = "gpt-4o-mini",
) -> dict[str, Any]:
    if not citations:
        raise RuntimeBlocked("citation_missing_before_llm")

    # Only verified citation records are inserted. The model is forbidden to
    # retrieve, paraphrase, repair or complete the quotation.
    context = {
        "policy": {
            "one_active_role": True,
            "one_task": True,
            "llm_must_not_rewrite_citations": True,
        },
        "task": {"role_id": role_id, "runtime_id": runtime_id, "question": question},
        "scope": scope,
        "targeted_semantic_table": table_result,
        "verified_spec_citations": citations,
        "evidence_digest": evidence_digest,
        "output_contract": {
            "required": ["finding_status", "spec_citations", "evidence_refs", "human_gate"],
            "unknown_is_allowed": True,
        },
    }
    estimated = token_count(context, model=model)
    if estimated > input_limit:
        raise RuntimeBlocked(f"context_over_budget:{estimated}>{input_limit}")
    return {"status": "ready_for_llm", "estimated_input_tokens": estimated, "context": context}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table-file", type=Path, default=DEFAULT_TABLE_FILE)
    parser.add_argument("--table-id", default="HWE.2 matrix")
    parser.add_argument("--row-contains", nargs="*", default=["BP5"])
    parser.add_argument("--columns", nargs="*", default=["Row ID", "Name", "Mapped Outcomes", "Mapped"])
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--role-id", default="HWE.2")
    parser.add_argument("--runtime-id", default="R06")
    parser.add_argument("--question", default="Check whether the hardware requirement-to-design mapping is bidirectional and consistent.")
    parser.add_argument("--input-limit", type=int, default=DEFAULT_BUDGET)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--citation-jsonl", type=Path, help="Optional controlled runtime JSONL of complete, verified citations.")
    parser.add_argument("--standard-id", default="ASPICE")
    parser.add_argument("--edition", default="4.0")
    parser.add_argument("--source-hash", default="", help="Must be the hash of the approved source text; never invent this value.")
    args = parser.parse_args()

    store = SemanticTableStore(args.table_file)
    table_result = store.query(
        table_id=args.table_id,
        row_contains=args.row_contains,
        columns=args.columns,
        limit=args.limit,
    )
    full_tokens = token_count(store.payload, model=args.model)
    targeted_tokens = token_count(table_result, model=args.model)

    result: dict[str, Any] = {
        "status": "table_query_ready_but_llm_blocked_without_citation",
        "query": {
            "table_file": str(args.table_file),
            "table_id": args.table_id,
            "row_contains": args.row_contains,
            "columns": args.columns,
            "limit": args.limit,
        },
        "token_measurement": {
            "tokenizer": args.model,
            "full_aspice40_tables_json_tokens": full_tokens,
            "targeted_table_query_tokens": targeted_tokens,
            "table_only_reduction_ratio": round(1 - targeted_tokens / max(full_tokens, 1), 4),
            "table_only_reduction_percent": round((1 - targeted_tokens / max(full_tokens, 1)) * 100, 2),
        },
        "targeted_table": table_result,
        "evidence_digest": [
            {
                "artifact_id": "HW-ARCH-001",
                "baseline": "HW-BL-042",
                "status": "approved",
                "full_artifact_is_pointer_only": True,
            }
        ],
    }

    if args.citation_jsonl:
        if not args.source_hash:
            raise RuntimeBlocked("source_hash_required_for_citation_loading")
        anchors = {"BP5", "HWE.2.BP5"}
        citations = load_verified_citations(
            args.citation_jsonl,
            requested_anchors=anchors,
            standard_id=args.standard_id,
            edition=args.edition,
            source_hash=args.source_hash,
        )
        ready = build_minimal_context(
            role_id=args.role_id,
            runtime_id=args.runtime_id,
            question=args.question,
            scope={"standards": [args.standard_id], "scope_state": "in_scope", "baseline_id": "HW-BL-042"},
            table_result=table_result,
            evidence_digest=result["evidence_digest"],
            citations=citations,
            input_limit=args.input_limit,
            model=args.model,
        )
        result["status"] = ready["status"]
        result["ready_context"] = ready

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.citation_jsonl:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeBlocked as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
