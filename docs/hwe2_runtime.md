# HWE.2 Local Runtime

This is the first executable slice of the SM2514 Agent Blueprint. It is a
deterministic, local-only evidence inventory for HWE.2. It is not a formal
ASPICE assessment and it does not produce a rating.

## Run

Run from the `agent_audit_blueprint` directory:

```powershell
$sm2514Python = "C:\Users\joker.kang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $sm2514Python -m runtime.cli run `
  --process HWE.2 `
  --project-root .. `
  --baseline <SM2514-parent-git-commit> `
  --run-id RUN-HWE2-SM2514-<date> `
  --output-root runs
```

The baseline is required so that a run can be reproduced. The adapter reads
only the configured local source roots in
`config/sm2514_project_adapter.yaml`. Source contents are not copied into the
Blueprint or the run report; the snapshot contains relative paths, metadata
and SHA-256 hashes.

## Outputs

Each run is written to `runs/<run-id>/`:

- `result.json`: machine-readable inventory, HWE.2 checks and human gates.
- `report.md`: concise review-oriented summary.

The `runs/` directory is ignored by Git and must remain local.

The inventory uses three explicit statuses:

- `evidence_present`: matching artifact metadata was discovered.
- `missing`: no matching artifact metadata was discovered inside the configured sources.
- `needs_human_review`: a candidate exists, but content, completeness, approval and consistency are not machine-approved.

Every HWE.2 check remains `unknown` in this first slice because filename
presence cannot prove technical correctness, completeness or bidirectional
traceability.

## Completion criteria for this slice

A local HWE.2 trial is complete when:

1. The command exits successfully and writes both run files.
2. The result contains all six HWE.2 Base Practice checks and direct citations.
3. Each configured source root is reported as available or explicitly missing.
4. Forbidden sources are absent from the evidence snapshot.
5. Stage 1 Golden files are read-only references and are never modified.
6. Human review gates and owner questions are present.
7. The result is explicitly marked `evidence_inventory_only`.

The next slice can replace keyword candidate discovery with a reviewed
evidence manifest and deterministic traceability checks. It must retain the
same human Gate and no-write boundaries.
