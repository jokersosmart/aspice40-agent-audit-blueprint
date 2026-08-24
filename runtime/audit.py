"""Deterministic HWE.2 evidence-inventory runtime."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re

from . import __version__
from .evidence import scan_evidence, utc_now
from .store import persist_run


PROCESS_ID = "HWE.2"
ASSESSMENT_MODE = "evidence_inventory_only"

ITEM_KEYWORDS = {
    "04-52": ("architecture", "flow", "uml", "spec"),
    "04-53": ("detailed", "design", "schematic", "hardware"),
    "15-51": ("analysis", "review", "simulation", "pvt", "fmea", "risk"),
    "13-51": ("trace", "crosswalk", "matrix", "consistency", "link"),
    "17-57": ("special", "characteristic", "safety", "critical"),
    "13-52": ("communication", "owner", "review", "signoff", "deliverable"),
    "04-54": ("schematic", "flow", "diagram"),
    "14-54": ("bom", "bill", "material"),
    "04-55": ("layout", "floorplan", "placement"),
    "03-54": ("production", "tapeout", "release", "manufactur"),
    "04-56": ("interface", "hsi", "link", "port"),
}


def _load_rulepack(rulepack_path: Path) -> dict:
    try:
        rulepack = json.loads(rulepack_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            "HWE.2 rulepack must be JSON-compatible; no YAML dependency is installed"
        ) from exc
    if rulepack.get("process_id") != PROCESS_ID:
        raise ValueError(f"expected {PROCESS_ID} rulepack: {rulepack_path}")
    return rulepack


def _citation_for(rulepack: dict, bp_id: str) -> list[dict]:
    return [
        citation
        for citation in rulepack.get("spec_citations", [])
        if citation.get("source_anchor", {}).get("indicator_id") == bp_id
    ]


def _bp_mapping(rulepack: dict) -> dict[str, set[str]]:
    return {
        mapping["id"]: set(mapping.get("outcomes", []))
        for mapping in rulepack.get("product_context", {}).get(
            "base_practice_outcome_mapping", []
        )
        if mapping.get("id")
    }


def _item_keywords(item: dict) -> tuple[str, ...]:
    explicit = ITEM_KEYWORDS.get(item.get("id"), ())
    if explicit:
        return explicit
    words = re.findall(r"[A-Za-z0-9]+", item.get("name", "").lower())
    return tuple(word for word in words if len(word) >= 4)


def _rank_candidates(artifacts: list[dict], item: dict) -> list[dict]:
    keywords = _item_keywords(item)
    ranked: list[tuple[int, str, dict]] = []
    for artifact in artifacts:
        haystack = " ".join(
            [
                artifact.get("uri_or_path", "").lower(),
                artifact.get("artifact_type", "").lower(),
                " ".join(artifact.get("tags", [])).lower(),
            ]
        )
        score = sum(1 for keyword in keywords if keyword in haystack)
        if score:
            ranked.append((score, artifact["uri_or_path"], artifact))
    ranked.sort(key=lambda entry: (-entry[0], entry[1]))
    return [entry[2] for entry in ranked[:20]]


def _evidence_ref(artifact: dict) -> dict:
    return {
        "artifact_id": artifact["artifact_id"],
        "uri_or_path": artifact["uri_or_path"],
        "revision": artifact["revision"],
        "baseline": artifact["baseline"],
        "owner": artifact["owner"],
        "review_status": artifact["review_status"],
        "content_anchor": artifact["source_anchor"]["section"],
    }


def _source_anchor(citations: list[dict]) -> dict:
    if citations:
        citation = citations[0]
        anchor = citation.get("source_anchor", {})
        return {
            "document_id": citation.get("document_id", "Automotive-SPICE-PAM-v40"),
            "version": citation.get("document_version", "4.0"),
            "page": anchor.get("page"),
            "section": anchor.get("section"),
            "chunk_id": None,
            "table_or_figure": anchor.get("table_or_figure"),
            "source_hash": citation.get("verbatim_text_sha256"),
        }
    return {
        "document_id": "Automotive-SPICE-PAM-v40",
        "version": "4.0",
        "page": None,
        "section": "4.7.2",
        "chunk_id": None,
        "table_or_figure": None,
        "source_hash": None,
    }


def _build_inventory(rulepack: dict, artifacts: list[dict]) -> list[dict]:
    inventory = []
    for item in rulepack.get("product_context", {}).get("output_information_items", []):
        candidates = _rank_candidates(artifacts, item)
        present = bool(candidates)
        inventory.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "outcomes": item.get("outcomes", []),
                "discovery_status": "evidence_present" if present else "missing",
                "review_status": "needs_human_review" if present else "missing",
                "artifact_ids": [artifact["artifact_id"] for artifact in candidates],
                "candidate_paths": [artifact["uri_or_path"] for artifact in candidates],
                "rationale": (
                    "Matching local artifact metadata was found; content, completeness, "
                    "approval and consistency still require human review."
                    if present
                    else "No matching artifact metadata was found within the configured local sources."
                ),
            }
        )
    return inventory


def _build_checks(
    rulepack: dict,
    artifacts: list[dict],
    inventory: list[dict],
    run_id: str,
    project_id: str,
    baseline: str,
) -> list[dict]:
    item_by_id = {item["item_id"]: item for item in inventory}
    artifact_by_id = {artifact["artifact_id"]: artifact for artifact in artifacts}
    mapping = _bp_mapping(rulepack)
    checks = []
    for practice in rulepack.get("pam", {}).get("base_practices", []):
        bp_id = practice["id"]
        outcomes = mapping.get(bp_id, set())
        related_items = [
            item
            for item in rulepack.get("product_context", {}).get(
                "output_information_items", []
            )
            if outcomes.intersection(item.get("outcomes", []))
        ]
        related_inventory = [item_by_id[item["id"]] for item in related_items]
        artifact_ids = sorted(
            {
                artifact_id
                for item in related_inventory
                for artifact_id in item["artifact_ids"]
            }
        )
        evidence_refs = [
            _evidence_ref(artifact_by_id[artifact_id]) for artifact_id in artifact_ids
        ]
        missing_items = [
            item["name"]
            for item in related_inventory
            if item["discovery_status"] == "missing"
        ]
        citations = _citation_for(rulepack, bp_id)
        checks.append(
            {
                "finding_id": f"AF-HWE2-{bp_id}",
                "agent_id": "HWE.2-auditor",
                "agent_version": __version__,
                "run_id": run_id,
                "project_id": project_id,
                "release_or_baseline": baseline,
                "process_id": PROCESS_ID,
                "pa_or_level": None,
                "source_anchor": _source_anchor(citations),
                "requirement_type": "pam_explicit",
                "requirement_id": f"{PROCESS_ID}.{bp_id}",
                "requirement_summary": practice.get("text", ""),
                "spec_citations": citations,
                "citation_missing": not bool(citations),
                "evidence_refs": evidence_refs,
                "traceability_refs": [item["item_id"] for item in related_inventory],
                "status": "unknown",
                "rationale": (
                    f"Inventory-only check found {len(evidence_refs)} candidate artifact(s). "
                    "The runtime does not assert technical correctness, completeness, approval "
                    "or bidirectional consistency."
                ),
                "missing_or_conflicting_evidence": missing_items,
                "impact": "high" if bp_id in {"BP4", "BP5"} else "medium",
                "recommended_action": "Send candidates and missing items to the responsible owner and independent reviewer for human confirmation.",
                "owner_manager": None,
                "verification_owner": None,
                "human_confirmation_required": True,
                "confidence": "low",
            }
        )
    return checks


def run_hwe2(
    project_root: Path,
    adapter_path: Path,
    rulepack_path: Path,
    baseline: str,
    run_id: str,
    output_root: Path | None = None,
    project_id: str = "SM2514_ISO26262",
) -> dict:
    if not baseline.strip():
        raise ValueError("baseline is required for a reproducible HWE.2 run")
    if not run_id.strip():
        raise ValueError("run_id is required for a reproducible HWE.2 run")

    rulepack = _load_rulepack(rulepack_path)
    snapshot = scan_evidence(
        project_root=project_root,
        adapter_path=adapter_path,
        baseline=baseline,
        project_id=project_id,
    )
    artifacts = snapshot["evidence_objects"]
    inventory = _build_inventory(rulepack, artifacts)
    checks = _build_checks(rulepack, artifacts, inventory, run_id, project_id, baseline)
    status_counts = Counter(check["status"] for check in checks)
    inventory_counts = Counter(item["discovery_status"] for item in inventory)
    human_review_queue = [
        {
            "gate": gate,
            "reason": "Runtime output is inventory-only and cannot replace the required human gate.",
            "required_action": "Confirm scope, technical correctness, verification adequacy, rating or finding closure as applicable.",
            "related_artifact_ids": [artifact["artifact_id"] for artifact in artifacts],
        }
        for gate in rulepack.get("human_gates", [])
    ]
    result = {
        "agent_id": "HWE.2-auditor",
        "agent_version": __version__,
        "run_id": run_id,
        "project_id": project_id,
        "release_or_baseline": baseline,
        "process_id": PROCESS_ID,
        "scope_status": "in_scope",
        "assessment_mode": ASSESSMENT_MODE,
        "captured_at": utc_now(),
        "snapshot": {key: value for key, value in snapshot.items() if key != "evidence_objects"},
        "evidence_objects": artifacts,
        "evidence_inventory": inventory,
        "checks": checks,
        "cross_domain_issues": [],
        "questions_for_owner": [
            "Which local owner confirms each discovered HWE.2 output information item?",
            "Which independent reviewer confirms technical correctness and verification adequacy?",
            "Are missing output information items intentionally outside the current baseline or located in another approved source system?",
            "Which requirement-to-design and design-to-architecture links are bidirectional and consistency-checked?",
        ],
        "human_review_queue": human_review_queue,
        "summary": {
            "satisfied": status_counts.get("satisfied", 0),
            "partial": status_counts.get("partial", 0),
            "gap": status_counts.get("gap", 0),
            "unknown": status_counts.get("unknown", 0),
            "conflict": status_counts.get("conflict", 0),
            "not_in_scope": status_counts.get("not_in_scope", 0),
        },
        "evidence_status_counts": {
            "evidence_present": inventory_counts.get("evidence_present", 0),
            "missing": inventory_counts.get("missing", 0),
            "needs_human_review": sum(
                item["review_status"] == "needs_human_review" for item in inventory
            ),
        },
    }
    if output_root is not None:
        persist_run(output_root, run_id, result)
    return result
