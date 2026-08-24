#!/usr/bin/env python3
"""Deterministic validation for approved standard citations.

The validator is intentionally independent from an LLM. It assumes a controlled
citation service has already resolved the source anchor and extracted the quote.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


TRUNCATION_MARKERS = ("[truncated]", "[...", "…", "<TRUNCATED>")
PLACEHOLDER_MARKERS = ("REPLACE-ME", "PLACEHOLDER", "TODO", "�")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _failed_checks(checks: dict[str, bool]) -> list[str]:
    return sorted(key for key, value in checks.items() if value is not True)


def verify_citation(
    record: dict[str, Any],
    *,
    expected_standard_id: str,
    expected_edition: str,
    expected_source_hash: str,
    resolved_anchor_count: int | None = None,
) -> dict[str, Any]:
    """Return an auditable verification result without changing source text."""
    quote = record.get("verbatim_text", "")
    checks = {
        "source_version_match": record.get("standard_id") == expected_standard_id and record.get("edition") == expected_edition,
        "anchor_resolved": bool(record.get("anchor")) and (resolved_anchor_count in (None, 1)),
        "complete_boundary": bool(record.get("boundary", {}).get("start")) and bool(record.get("boundary", {}).get("end")),
        "hash_match": bool(quote) and sha256_text(quote) == record.get("verbatim_text_sha256"),
        "no_placeholder": bool(quote) and not any(marker in quote for marker in PLACEHOLDER_MARKERS),
        "no_truncation": bool(quote) and not any(marker in quote for marker in TRUNCATION_MARKERS),
        "table_structure_verified": record.get("table_structure_verified", True) is True,
    }
    source_hash_match = record.get("source_hash") == expected_source_hash
    checks["source_hash_match"] = source_hash_match
    failed = _failed_checks(checks)
    if not failed:
        verdict = "verified"
    elif not checks["source_version_match"] or not source_hash_match:
        verdict = "source_version_mismatch"
    elif not checks["anchor_resolved"]:
        verdict = "anchor_unresolved"
    elif not checks["complete_boundary"] or not checks["no_truncation"]:
        verdict = "quote_incomplete"
    elif not checks["hash_match"]:
        verdict = "hash_mismatch"
    elif not checks["no_placeholder"]:
        verdict = "placeholder_detected"
    elif not checks["table_structure_verified"]:
        verdict = "table_structure_uncertain"
    else:
        verdict = "human_review_required"
    return {
        "verification_id": record.get("verification_id", f"verify:{record.get('anchor', 'unknown')}"),
        "standard_id": record.get("standard_id"),
        "edition": record.get("edition"),
        "source_hash": record.get("source_hash"),
        "anchor": record.get("anchor"),
        "verbatim_text": quote,
        "verbatim_text_sha256": record.get("verbatim_text_sha256"),
        "checks": checks,
        "failed_checks": failed,
        "verdict": verdict,
        "human_gate": {
            "required": verdict != "verified",
            "authority": ["Spec Custodian", "Lead Assessor or applicable Safety/Cybersecurity Authority"],
            "status": "pending" if verdict != "verified" else "not_applicable",
        },
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid_jsonl:{path}:{line_number}:{exc}") from exc
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-file", type=Path, required=True)
    parser.add_argument("--standard-id", required=True)
    parser.add_argument("--edition", required=True)
    parser.add_argument("--source-hash", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = load_jsonl(args.record_file)
    results = [
        verify_citation(
            record,
            expected_standard_id=args.standard_id,
            expected_edition=args.edition,
            expected_source_hash=args.source_hash,
        )
        for record in records
    ]
    args.output.write_text("\n".join(json.dumps(result, ensure_ascii=False) for result in results) + "\n", encoding="utf-8")
    summary = {
        "record_count": len(results),
        "verified_count": sum(result["verdict"] == "verified" for result in results),
        "blocked_count": sum(result["verdict"] != "verified" for result in results),
        "verdicts": sorted({result["verdict"] for result in results}),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["blocked_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
