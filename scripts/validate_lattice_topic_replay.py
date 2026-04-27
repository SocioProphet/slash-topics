#!/usr/bin/env python3
"""Validate Lattice Slash Topic replay reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_ASSETS = {
    "runtime-asset:prophet-python-ml:0.1.0": "/lattice/runtime",
    "boot-release-set:sourceos-recovery-demo:0.1.0": "/lattice/boot",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    require(doc.get("apiVersion") == "slash-topics.socioprophet.dev/v1", "apiVersion mismatch")
    require(doc.get("kind") == "SlashTopicReplayReport", "kind mismatch")
    assignments = doc.get("assignments")
    require(isinstance(assignments, list) and assignments, "assignments must be non-empty")
    by_asset = {item.get("assetId"): item for item in assignments if isinstance(item, dict)}
    for asset_id, expected_topic in REQUIRED_ASSETS.items():
        require(asset_id in by_asset, f"missing assignment for {asset_id}")
        topics = by_asset[asset_id].get("topics")
        require(isinstance(topics, list), f"topics for {asset_id} must be a list")
        require(expected_topic in topics, f"{asset_id} missing expected topic {expected_topic}")


def main(argv: list[str] | None = None) -> int:
    paths = [Path(arg) for arg in (argv if argv is not None else sys.argv[1:])]
    failed = False
    for path in paths:
        try:
            validate(path)
            print(f"PASS {path}")
        except Exception as exc:  # noqa: BLE001
            failed = True
            print(f"FAIL {path}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
