"""Command-line entry point for the first local HWE Runtime slice."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from .audit import run_hwe2


def _default_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"RUN-HWE2-{timestamp}"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hwe-runtime")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="run a local HWE readiness inventory")
    run.add_argument("--process", choices=["HWE.2"], default="HWE.2")
    run.add_argument("--project-root", type=Path, default=Path(".."))
    run.add_argument(
        "--adapter",
        type=Path,
        default=Path("config/sm2514_project_adapter.yaml"),
    )
    run.add_argument(
        "--rulepack",
        type=Path,
        default=Path("knowledge/aspice40/process_rules/HWE.2.yaml"),
    )
    run.add_argument("--baseline", required=True)
    run.add_argument("--run-id", default=None)
    run.add_argument("--project-id", default="SM2514_ISO26262")
    run.add_argument("--output-root", type=Path, default=Path("runs"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "run":
        return 2
    result = run_hwe2(
        project_root=args.project_root,
        adapter_path=args.adapter,
        rulepack_path=args.rulepack,
        baseline=args.baseline,
        run_id=args.run_id or _default_run_id(),
        output_root=args.output_root,
        project_id=args.project_id,
    )
    print(
        "HWE.2 run complete: "
        f"{result['run_id']} | "
        f"present={result['evidence_status_counts']['evidence_present']} "
        f"missing={result['evidence_status_counts']['missing']} "
        f"human_review={result['evidence_status_counts']['needs_human_review']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
