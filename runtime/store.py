"""Persist local run outputs without copying source content."""

from __future__ import annotations

import json
from pathlib import Path


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def render_report(result: dict) -> str:
    lines = [
        "# HWE.2 Runtime Run",
        "",
        f"- Run ID: `{result['run_id']}`",
        f"- Project: `{result['project_id']}`",
        f"- Baseline: `{result['release_or_baseline']}`",
        "- Assessment mode: `evidence_inventory_only`",
        "- Source policy: metadata and hash only; source content was not exported",
        "",
        "## Evidence inventory",
        "",
        "| Item | Discovery | Human review | Artifacts |",
        "|---|---|---|---:|",
    ]
    for item in result.get("evidence_inventory", []):
        lines.append(
            "| {item_id} {name} | {discovery} | {review} | {count} |".format(
                item_id=item["item_id"],
                name=item["name"],
                discovery=item["discovery_status"],
                review=item["review_status"],
                count=len(item.get("artifact_ids", [])),
            )
        )
    lines.extend(["", "## Human review queue", ""])
    for entry in result.get("human_review_queue", []):
        lines.append(f"- **{entry['gate']}**: {entry['reason']}")
    if not result.get("human_review_queue"):
        lines.append("- None")
    lines.extend(["", "## Owner questions", ""])
    for question in result.get("questions_for_owner", []):
        lines.append(f"- {question}")
    if not result.get("questions_for_owner"):
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Safety boundary",
            "",
            "This run is a deterministic evidence inventory. It does not modify project files,",
            "does not edit Stage 1 Golden references, and does not produce a formal ASPICE rating.",
            "Human confirmation is required before any technical conclusion or finding closure.",
            "",
        ]
    )
    return "\n".join(lines)


def persist_run(output_root: Path, run_id: str, result: dict) -> Path:
    run_dir = (output_root / run_id).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write(
        run_dir / "result.json",
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
    )
    _atomic_write(run_dir / "report.md", render_report(result))
    return run_dir
