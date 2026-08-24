"""Read the small, project-specific adapter YAML without adding a dependency."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class SourceRoot:
    source_id: str
    path: str
    evidence_domains: tuple[str, ...]
    artifact_types: tuple[str, ...]
    confidentiality: str
    immutable_subpaths: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdapterConfig:
    source_roots: tuple[SourceRoot, ...]
    excluded_paths: tuple[str, ...]


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_inline_list(value: str) -> tuple[str, ...]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return ()
    inner = value[1:-1].strip()
    if not inner:
        return ()
    return tuple(_strip_quotes(item.strip()) for item in inner.split(",") if item.strip())


def _parse_key_value(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def _parse_source_roots(lines: list[str]) -> tuple[SourceRoot, ...]:
    roots: list[SourceRoot] = []
    current: dict[str, object] | None = None
    pending_list: str | None = None

    def flush() -> None:
        if current is None:
            return
        missing = [key for key in ("source_id", "path") if not current.get(key)]
        if missing:
            raise ValueError(f"source root is missing required fields: {missing}")
        roots.append(
            SourceRoot(
                source_id=str(current["source_id"]),
                path=str(current["path"]),
                evidence_domains=tuple(current.get("evidence_domains", ())),
                artifact_types=tuple(current.get("artifact_types", ())),
                confidentiality=str(current.get("confidentiality", "unknown")),
                immutable_subpaths=tuple(current.get("immutable_subpaths", ())),
            )
        )

    in_section = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line.startswith("source_roots:"):
            in_section = True
            continue
        if raw_line.startswith("excluded_sources:"):
            break
        if not in_section:
            continue
        if line.startswith("- source_id:"):
            flush()
            current = {"source_id": _strip_quotes(line.split(":", 1)[1])}
            pending_list = None
            continue
        if current is None:
            continue
        if pending_list and line.startswith("-"):
            current.setdefault(pending_list, []).append(
                _strip_quotes(line[1:].strip())
            )
            continue
        parsed = _parse_key_value(line)
        if not parsed:
            continue
        key, value = parsed
        if value == "":
            pending_list = key
            current[key] = []
        elif value.startswith("["):
            pending_list = None
            current[key] = list(_parse_inline_list(value))
        else:
            pending_list = None
            current[key] = _strip_quotes(value)
    flush()
    return tuple(roots)


def _parse_excluded_paths(lines: list[str]) -> tuple[str, ...]:
    paths: list[str] = []
    in_section = False
    current_path: str | None = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line.startswith("excluded_sources:"):
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("- path:"):
            if current_path is not None:
                paths.append(current_path)
            current_path = _strip_quotes(line.split(":", 1)[1])
    if current_path is not None:
        paths.append(current_path)
    return tuple(paths)


def load_adapter(adapter_path: Path) -> AdapterConfig:
    lines = adapter_path.read_text(encoding="utf-8").splitlines()
    source_roots = _parse_source_roots(lines)
    if not source_roots:
        raise ValueError(f"adapter contains no source_roots: {adapter_path}")
    return AdapterConfig(
        source_roots=source_roots,
        excluded_paths=_parse_excluded_paths(lines),
    )


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_config_path(raw_path: str, adapter_path: Path, project_root: Path) -> Path:
    """Resolve adapter paths while keeping them inside the declared project."""

    raw = Path(raw_path)
    blueprint_root = adapter_path.parent
    if adapter_path.parent.name == "config":
        blueprint_root = adapter_path.parent.parent
    base = (
        blueprint_root
        if raw.is_absolute() or raw.parts[:1] in ((".",), ("..",))
        else project_root
    )
    candidate = (base / raw).resolve()
    if not is_within(candidate, project_root.resolve()):
        raise ValueError(f"adapter path escapes project root: {raw_path}")
    return candidate


ARTIFACT_TYPE_MAP = {
    "requirement_specification": "requirement",
    "system_requirement": "requirement",
    "architecture_specification": "architecture",
    "mermaid_flow": "architecture",
    "golden_reference": "other",
    "flow_description": "detailed_design",
    "safety_flow": "architecture",
    "owner_matrix": "review_record",
    "owner_review": "review_record",
    "review_record": "review_record",
    "traceability_record": "review_record",
    "safety_matrix": "review_record",
    "test_specification": "verification_measure",
    "process_guidance": "other",
    "prompt": "other",
}


def normalized_artifact_type(source: SourceRoot) -> str:
    for artifact_type in source.artifact_types:
        mapped = ARTIFACT_TYPE_MAP.get(artifact_type)
        if mapped:
            return mapped
    return "other"
