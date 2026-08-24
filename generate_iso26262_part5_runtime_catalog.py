from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def normalize_for_hash(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text.strip())


def extract_blocks(source: str) -> list[dict]:
    lines = source.splitlines()
    pattern = re.compile(r"^(?P<id>(?:[1-9]|10)\.(?:\d+)(?:\.\d+){0,2})\s+(?P<body>.+)$")
    starts = [i for i, line in enumerate(lines) if pattern.match(line.strip())]
    records = []
    for pos, start in enumerate(starts):
        match = pattern.match(lines[start].strip())
        if not match:
            continue
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("Licensed to ") or stripped.startswith("ISO Store Order:"):
                continue
            if stripped.startswith("Single user licence only"):
                continue
            if stripped in {"© ISO 2018", "All rights reserved", "﻿"}:
                continue
            block_lines.append(stripped)
        quote = " ".join(block_lines)
        if len(quote) < 30:
            continue
        digest = hashlib.sha256(normalize_for_hash(quote).encode("utf-8")).hexdigest()
        records.append({
            "citation_id": f"ISO26262-5-{match.group('id')}",
            "standard_id": "ISO26262",
            "edition": "ISO 26262-5:2018(E)",
            "part": 5,
            "clause": match.group("id"),
            "verbatim_text": quote,
            "source_anchor": "runtime_source_line_" + str(start + 1),
            "verbatim_text_sha256": digest,
            "human_verification_status": "pending",
            "runtime_only": True,
        })
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source_path = Path(args.source)
    output_path = Path(args.output)
    text = source_path.read_text(encoding="utf-8", errors="replace")
    records = extract_blocks(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"source": str(source_path), "output": str(output_path), "records": len(records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
