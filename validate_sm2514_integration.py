from __future__ import annotations

import json
import re
from pathlib import Path


BLUEPRINT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BLUEPRINT_ROOT.parent


def check_required_files() -> list[str]:
    required = [
        "config/process_scope.yaml",
        "config/sm2514_project_adapter.yaml",
        "docs/sm2514_integration.md",
    ]
    return [path for path in required if not (BLUEPRINT_ROOT / path).is_file()]


def check_scope_profile() -> list[str]:
    path = BLUEPRINT_ROOT / "config/process_scope.yaml"
    text = path.read_text(encoding="utf-8")
    required_terms = [
        'project_id: "SM2514_ISO26262"',
        "SYS.2:",
        "SYS.3:",
        "HWE.1:",
        "HWE.4:",
        "SWE.4:",
        "SUP.8:",
        "SUP.10:",
        "Stage 1 Golden files are immutable",
    ]
    return [term for term in required_terms if term not in text]


def check_source_boundaries() -> list[str]:
    path = BLUEPRINT_ROOT / "config/sm2514_project_adapter.yaml"
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for required in [
        "../HW_IP_Spec",
        "../HW_IP_Flow_Diagrams",
        "../SM2514_Auto/AiWorkSpace/SYS2_ReqDoc",
        "../SM2514_Auto/AiWorkSpace/TestSpec",
        "../Source_file",
        "content_copy: prohibited_by_default",
        "stage_1_golden: \"read_only_reference\"",
    ]:
        if required not in text:
            errors.append(required)

    referenced_paths = re.findall(r'^\s+path: "(\.\./[^\"]+)"$', text, re.MULTILINE)
    for relative_path in referenced_paths:
        if not (BLUEPRINT_ROOT / relative_path).exists():
            errors.append(f"missing project path: {relative_path}")
    return errors


def main() -> int:
    checks = {
        "required_files": check_required_files(),
        "scope_profile": check_scope_profile(),
        "source_boundaries": check_source_boundaries(),
    }
    result = {"ok": not any(checks.values()), "checks": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
