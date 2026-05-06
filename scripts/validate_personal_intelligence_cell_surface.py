#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs/personal-intelligence-cell-surface.schema.json"
EXAMPLE = ROOT / "examples/personal-intelligence-cell/surface.example.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> int:
    print(f"Personal Intelligence Cell slash-topic surface failed validation: {message}")
    return 1


def main() -> int:
    schema = load_json(SCHEMA)
    example = load_json(EXAMPLE)

    if schema.get("title") != "PersonalIntelligenceCellSlashTopicSurface":
        return fail("schema title mismatch")
    required = set(schema.get("required", []))
    missing = sorted(required - set(example))
    if missing:
        return fail(f"example missing required fields: {', '.join(missing)}")

    if example["surfaceKind"] != "slash-topic-cell-signal":
        return fail("surfaceKind must be slash-topic-cell-signal")
    if example["schemaVersion"] != "v0.1":
        return fail("schemaVersion must be v0.1")
    if not re.match(r"^/cell/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", example["topicRef"]):
        return fail("topicRef must match /cell/<kind>/<slug>")
    if not example.get("policyDecisionRefs"):
        return fail("policyDecisionRefs required")
    if example.get("policyDecision") not in ["allow", "deny", "quarantine", "review_required", "redact"]:
        return fail("invalid policyDecision")
    if not example.get("evidenceRefs"):
        return fail("evidenceRefs required")
    replay = example.get("replay", {})
    for key in ["sourceRef", "observedAt", "createdAt"]:
        if not replay.get(key):
            return fail(f"replay.{key} required")

    print("Personal Intelligence Cell slash-topic surface validates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
