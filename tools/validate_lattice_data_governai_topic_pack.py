#!/usr/bin/env python3
"""Validate the Lattice Data/GovernAI Slash Topics topic pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs" / "lattice-data-governai" / "topic-pack.v0.1.json"

REQUIRED_ASSET_KINDS = {
    "data-product",
    "runtime-asset",
    "query-run",
    "evaluation-bundle",
    "factsheet",
    "publication-artifact",
    "ray-job-dry-run",
    "beam-pipeline-dry-run",
}
REQUIRED_SEQUENCE = [
    "slash-topic-scope",
    "slash-topics-runtime-alias",
    "newhope-compatibility-membrane",
    "memory-mesh-profile",
    "policy-fabric-decision",
    "consumer-surface-route",
]


def fail(message: str) -> int:
    print(f"ERR: {message}", file=sys.stderr)
    return 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_str(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    require(isinstance(value, str) and bool(value), f"{key} must be a non-empty string")
    return value


def require_list(mapping: dict[str, Any], key: str) -> list[Any]:
    value = mapping.get(key)
    require(isinstance(value, list) and value, f"{key} must be a non-empty list")
    return value


def main() -> int:
    if not PACK.exists():
        return fail(f"missing {PACK}")
    try:
        data = json.loads(PACK.read_text(encoding="utf-8"))
        require(isinstance(data, dict), "topic pack root must be object")
        require(data.get("apiVersion") == "slash-topics.socioprophet.dev/v1", "apiVersion mismatch")
        require(data.get("kind") == "TopicPack", "kind must be TopicPack")
        metadata = data.get("metadata")
        require(isinstance(metadata, dict), "metadata must be object")
        require(metadata.get("name") == "lattice-data-governai", "metadata.name mismatch")
        require(metadata.get("version") == "0.1.0", "metadata.version mismatch")

        spec = data.get("spec")
        require(isinstance(spec, dict), "spec must be object")
        require(require_str(spec, "publicSurfaceRef").startswith("slash-topic://"), "publicSurfaceRef must be slash-topic://")
        require(require_str(spec, "topicPackRef").startswith("slash-topics://packs/"), "topicPackRef must be slash-topics pack ref")
        require(require_str(spec, "runtimeAliasRef").startswith("slash-topics://runtime/"), "runtimeAliasRef must be Slash Topics runtime alias")
        require(require_str(spec, "compatibilityRef").startswith("newhope://"), "compatibilityRef must preserve New Hope compatibility")
        require(require_str(spec, "memoryProfileRef").startswith("memory-mesh://"), "memoryProfileRef must attach Memory Mesh profile")

        source_refs = spec.get("sourceRefs")
        require(isinstance(source_refs, dict), "sourceRefs must be object")
        for key in ["umbrellaIssue", "sherlockPr", "topologyPr", "policyPr"]:
            require_str(source_refs, key)

        classifications = require_list(spec, "assetClassifications")
        asset_kinds = set()
        for item in classifications:
            require(isinstance(item, dict), "assetClassifications entries must be objects")
            asset_kind = require_str(item, "assetKind")
            asset_kinds.add(asset_kind)
            require(asset_kind in REQUIRED_ASSET_KINDS, f"unexpected assetKind {asset_kind}")
            require(require_str(item, "topic").startswith("/lattice/"), f"{asset_kind} topic must be /lattice/*")
            require_str(item, "scope")
            require_str(item, "governancePosture")
            required_refs = require_list(item, "requiredRefs")
            require("evidenceCorrelationId" in required_refs, f"{asset_kind} must require evidenceCorrelationId")
            surfaces = require_list(item, "consumerSurfaces")
            require("sherlock-search" in surfaces or asset_kind == "runtime-asset", f"{asset_kind} should route to Sherlock or be runtime-discoverable")
        missing = sorted(REQUIRED_ASSET_KINDS - asset_kinds)
        require(not missing, f"missing assetKind classifications: {missing}")

        rules = spec.get("routingRules")
        require(isinstance(rules, dict), "routingRules must be object")
        require(rules.get("requiredSequence") == REQUIRED_SEQUENCE, "routingRules.requiredSequence mismatch")
        require(rules.get("publicSurface") == "slash-topics", "Slash Topics must remain public surface")
        require(rules.get("runtimeSubstrate") == "new-hope", "New Hope must remain runtime substrate")
        require(rules.get("dryRunOnly") is True, "dryRunOnly must be true")
        require(rules.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")
        require(rules.get("mustNotRedefinePlatformAssetRecord") is True, "mustNotRedefinePlatformAssetRecord must be true")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(f"PASS {PACK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
