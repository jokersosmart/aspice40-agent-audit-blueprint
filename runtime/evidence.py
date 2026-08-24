"""Build a local-only evidence metadata snapshot."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path

from .adapter import (
    AdapterConfig,
    SourceRoot,
    is_within,
    load_adapter,
    normalized_artifact_type,
    resolve_config_path,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_uri(path: Path, project_root: Path) -> str:
    return path.resolve().relative_to(project_root.resolve()).as_posix()


def _is_immutable(path: Path, source_path: Path, source: SourceRoot) -> bool:
    try:
        relative = path.resolve().relative_to(source_path.resolve()).as_posix()
    except ValueError:
        return False
    return any(
        relative == immutable or relative.startswith(immutable.rstrip("/") + "/")
        for immutable in source.immutable_subpaths
    )


def _artifact_id(relative_uri: str) -> str:
    return "EV-" + hashlib.sha256(relative_uri.encode("utf-8")).hexdigest()[:16]


def _artifact_for(
    path: Path,
    project_root: Path,
    source_path: Path,
    source: SourceRoot,
    project_id: str,
    baseline: str,
    captured_at: str,
) -> dict:
    relative_uri = _relative_uri(path, project_root)
    tags = list(source.evidence_domains)
    if _is_immutable(path, source_path, source):
        tags.append("immutable_reference")
    stat = path.stat()
    return {
        "artifact_id": _artifact_id(relative_uri),
        "project_id": project_id,
        "artifact_type": normalized_artifact_type(source),
        "name": path.name,
        "uri_or_path": relative_uri,
        "source_system": "local-filesystem",
        "revision": baseline,
        "baseline": baseline,
        "owner": "UNASSIGNED",
        "review_status": "unknown",
        "content_hash": _sha256(path),
        "captured_at": captured_at,
        "created_at": None,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "confidentiality": "confidential"
        if source.confidentiality == "local_only"
        else "unknown",
        "characteristics": [],
        "source_anchor": {
            "document_id": source.source_id,
            "version": baseline,
            "section": relative_uri,
            "page": None,
            "chunk_id": None,
            "table_or_figure": None,
            "source_hash": _sha256(path),
        },
        "related_artifact_ids": [],
        "tags": tags,
        "extraction_status": "native",
        "notes": "Metadata and hash captured; source content was not exported.",
    }


def scan_evidence(
    project_root: Path,
    adapter_path: Path,
    baseline: str,
    project_id: str = "SM2514_ISO26262",
) -> dict:
    project_root = project_root.resolve()
    adapter_path = adapter_path.resolve()
    config: AdapterConfig = load_adapter(adapter_path)
    excluded = tuple(
        resolve_config_path(raw, adapter_path, project_root)
        for raw in config.excluded_paths
    )
    artifacts: list[dict] = []
    source_statuses: list[dict] = []
    captured_at = utc_now()

    for source in config.source_roots:
        source_path = resolve_config_path(source.path, adapter_path, project_root)
        if not source_path.is_dir():
            source_statuses.append(
                {
                    "source_id": source.source_id,
                    "path": source.path,
                    "resolved_status": "missing",
                    "file_count": 0,
                }
            )
            continue
        count = 0
        for path in sorted(source_path.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            if any(is_within(path.resolve(), root) for root in excluded if root.exists()):
                continue
            artifacts.append(
                _artifact_for(
                    path,
                    project_root,
                    source_path,
                    source,
                    project_id,
                    baseline,
                    captured_at,
                )
            )
            count += 1
        source_statuses.append(
            {
                "source_id": source.source_id,
                "path": source.path,
                "resolved_status": "available",
                "file_count": count,
            }
        )

    artifacts.sort(key=lambda item: item["uri_or_path"])
    return {
        "captured_at": captured_at,
        "project_root": ".",
        "adapter_path": adapter_path.name,
        "content_policy": "metadata_and_hash_only",
        "source_roots": source_statuses,
        "excluded_paths": list(config.excluded_paths),
        "evidence_objects": artifacts,
    }
