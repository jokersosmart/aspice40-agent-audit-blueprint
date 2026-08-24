import json
import tempfile
import unittest
from pathlib import Path

from runtime.audit import run_hwe2
from runtime.cli import main


class HWE2RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.project_root = self.workspace / "project"
        self.project_root.mkdir()
        self.adapter_path = self.workspace / "sm2514_project_adapter.yaml"
        self.adapter_path.write_text(
            """source_roots:
  - source_id: HW_IP_SPEC
    path: "HW_IP_Spec"
    evidence_domains: [hardware_requirements, hardware_architecture]
    artifact_types: [requirement_specification, architecture_specification]
    confidentiality: local_only
  - source_id: HW_IP_FLOW_DIAGRAMS
    path: "HW_IP_Flow_Diagrams"
    evidence_domains: [hardware_design, traceability]
    artifact_types: [mermaid_flow, flow_description]
    confidentiality: local_only
    immutable_subpaths:
      - "1. Golden Normal Function UML Code"
excluded_sources:
  - path: "Source_file"
    reason: "local-only source material"
""",
            encoding="utf-8",
        )
        self.rulepack_path = (
            Path(__file__).parents[1]
            / "knowledge"
            / "aspice40"
            / "process_rules"
            / "HWE.2.yaml"
        )

        (self.project_root / "HW_IP_Spec" / "architecture").mkdir(parents=True)
        (self.project_root / "HW_IP_Spec" / "architecture" / "arch.md").write_text(
            "architecture evidence", encoding="utf-8"
        )
        golden_dir = (
            self.project_root
            / "HW_IP_Flow_Diagrams"
            / "1. Golden Normal Function UML Code"
        )
        golden_dir.mkdir(parents=True)
        (golden_dir / "golden.txt").write_text("golden reference", encoding="utf-8")
        forbidden = self.project_root / "Source_file"
        forbidden.mkdir()
        (forbidden / "secret.md").write_text("NDA-SECRET", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_creates_hash_only_inventory_and_human_gate_queue(self):
        output_root = self.workspace / "runs"

        result = run_hwe2(
            project_root=self.project_root,
            adapter_path=self.adapter_path,
            rulepack_path=self.rulepack_path,
            baseline="TEST-BASELINE-1",
            run_id="RUN-HWE2-001",
            output_root=output_root,
        )

        inventory = {item["item_id"]: item for item in result["evidence_inventory"]}
        self.assertEqual(result["assessment_mode"], "evidence_inventory_only")
        self.assertEqual(inventory["04-52"]["discovery_status"], "evidence_present")
        self.assertEqual(
            inventory["04-52"]["review_status"], "needs_human_review"
        )
        self.assertEqual(inventory["14-54"]["discovery_status"], "missing")

        serialized = json.dumps(result, ensure_ascii=False)
        self.assertNotIn("NDA-SECRET", serialized)
        golden_artifact = next(
            artifact
            for artifact in result["evidence_objects"]
            if artifact["uri_or_path"].endswith("golden.txt")
        )
        self.assertIn("immutable_reference", golden_artifact["tags"])
        self.assertRegex(golden_artifact["content_hash"], r"^[0-9a-f]{64}$")

        run_dir = output_root / "RUN-HWE2-001"
        self.assertTrue((run_dir / "result.json").is_file())
        self.assertTrue((run_dir / "report.md").is_file())

    def test_cli_runs_the_same_public_contract(self):
        output_root = self.workspace / "cli-runs"

        exit_code = main(
            [
                "run",
                "--process",
                "HWE.2",
                "--project-root",
                str(self.project_root),
                "--adapter",
                str(self.adapter_path),
                "--rulepack",
                str(self.rulepack_path),
                "--baseline",
                "TEST-BASELINE-2",
                "--run-id",
                "RUN-HWE2-CLI",
                "--output-root",
                str(output_root),
            ]
        )

        self.assertEqual(exit_code, 0)
        result = json.loads(
            (output_root / "RUN-HWE2-CLI" / "result.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(result["process_id"], "HWE.2")
        self.assertEqual(result["release_or_baseline"], "TEST-BASELINE-2")

    def test_config_adapter_paths_resolve_from_blueprint_root(self):
        blueprint_root = self.workspace / "blueprint"
        config_dir = blueprint_root / "config"
        config_dir.mkdir(parents=True)
        config_adapter = config_dir / "sm2514_project_adapter.yaml"
        config_adapter.write_text(
            self.adapter_path.read_text(encoding="utf-8")
            .replace('path: "HW_IP_Spec"', 'path: "../project/HW_IP_Spec"')
            .replace(
                'path: "HW_IP_Flow_Diagrams"',
                'path: "../project/HW_IP_Flow_Diagrams"',
            )
            .replace('path: "Source_file"', 'path: "../project/Source_file"'),
            encoding="utf-8",
        )

        result = run_hwe2(
            project_root=self.project_root,
            adapter_path=config_adapter,
            rulepack_path=self.rulepack_path,
            baseline="TEST-BASELINE-CONFIG",
            run_id="RUN-HWE2-CONFIG",
        )

        self.assertTrue(
            all(
                source["resolved_status"] == "available"
                for source in result["snapshot"]["source_roots"]
            )
        )


if __name__ == "__main__":
    unittest.main()
