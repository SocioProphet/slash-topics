#!/usr/bin/env python3
"""Validate Lattice platform asset slash topic packs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    require(doc.get("apiVersion") == "slash-topics.socioprophet.dev/v1", "apiVersion mismatch")
    require(doc.get("kind") == "SlashTopicPack", "kind mismatch")
    require(isinstance(doc.get("subjects"), list) and doc["subjects"], "subjects must be a non-empty list")
    for subject in doc["subjects"]:
        require(subject.get("subjectKind") == "PlatformAssetRecord", "subjectKind must be PlatformAssetRecord")
        require(isinstance(subject.get("match"), dict), "match must be an object")
        topics = subject.get("topics")
        require(isinstance(topics, list) and topics, "topics must be a non-empty list")
        for topic in topics:
            require(isinstance(topic, str) and topic.startswith("/"), f"invalid slash topic: {topic!r}")
    governance = doc.get("governance")
    require(isinstance(governance, dict), "governance must be an object")
    require(governance.get("canonicalRecordKind") == "PlatformAssetRecord", "canonicalRecordKind mismatch")


def main(argv: list[str] | None = None) -> int:
    paths = [Path(arg) for arg in (argv if argv is not None else sys.argv[1:])]
    if not paths:
        paths = sorted(Path("protocols/lattice").glob("*.json"))
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
