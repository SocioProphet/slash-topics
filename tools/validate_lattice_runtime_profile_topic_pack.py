#!/usr/bin/env python3
"""Validate Lattice runtime profile Slash Topics pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs" / "lattice-data-governai" / "runtime-profile-topic-pack.v0.1.json"
NOTEBOOK = "runtime-asset:prophet-python-ml:0.1.0"
RAY = "runtime-asset:prophet-ray-ml:0.1.0"
BEAM = "runtime-asset:prophet-beam-dataops:0.1.0"
REQUIRED_RUNTIME_CLASSES = {"notebook", "ray", "beam"}
REQUIRED_SOURCE_REFS = {
    "runtimeForgePr",
    "platformRuntimeCatalogPr",
    "agentplaneRuntimeRefsPr",
    "sherlockRuntimeIndexPr",
    "topologyRuntimePr",
}


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
    require(isinstance(value, list) and bool(value), f"{key} must be a non-empty list")
    return value


def main() -> int:
    if not PACK.exists():
        return fail(f"missing {PACK}")
    try:
        data = json.loads(PACK.read_text(encoding="utf-8"))
        require(data.get("apiVersion") == "slash-topics.socioprophet.dev/v1", "apiVersion mismatch")
        require(data.get("kind") == "RuntimeProfileTopicPack", "kind mismatch")
        metadata = data.get("metadata")
        require(isinstance(metadata, dict), "metadata must be object")
        require(metadata.get("name") == "lattice-runtime-profiles", "metadata.name mismatch")
        spec = data.get("spec")
        require(isinstance(spec, dict), "spec must be object")
        require(require_str(spec, "publicSurfaceRef") == "slash-topic://lattice/data-governai/runtime-profiles", "publicSurfaceRef mismatch")
        require(require_str(spec, "parentTopicPackRef") == "slash-topics://packs/lattice-data-governai@0.1.0", "parentTopicPackRef mismatch")
        require(require_str(spec, "compatibilityRef").startswith("newhope://"), "compatibilityRef must be New Hope ref")
        require(require_str(spec, "memoryProfileRef").startswith("memory-mesh://"), "memoryProfileRef must be Memory Mesh ref")
        source_refs = spec.get("sourceRefs")
        require(isinstance(source_refs, dict), "sourceRefs must be object")
        missing_source_refs = sorted(REQUIRED_SOURCE_REFS - set(source_refs))
        require(not missing_source_refs, f"missing sourceRefs: {missing_source_refs}")

        runtime_assets = require_list(spec, "runtimeAssets")
        runtime_ids = {require_str(asset, "assetId") for asset in runtime_assets if isinstance(asset, dict)}
        require(runtime_ids == {NOTEBOOK, RAY, BEAM}, f"runtime asset ids mismatch: {sorted(runtime_ids)}")
        runtime_classes = {require_str(asset, "runtimeClass") for asset in runtime_assets if isinstance(asset, dict)}
        require(runtime_classes == REQUIRED_RUNTIME_CLASSES, f"runtime classes mismatch: {sorted(runtime_classes)}")
        for asset in runtime_assets:
            require(require_str(asset, "topic").startswith("/lattice/runtime/"), "runtime topic must be /lattice/runtime/*")
            require_list(asset, "roles")
            required_refs = require_list(asset, "requiredRefs")
            require("runtimeRef" in required_refs, "runtime asset must require runtimeRef")
            surfaces = require_list(asset, "consumerSurfaces")
            require("sherlock-search" in surfaces, "runtime asset must route to Sherlock")
            require("policy-fabric" in surfaces, "runtime asset must route to Policy Fabric")
            require("agentplane" in surfaces, "runtime asset must route to AgentPlane")

        classifications = require_list(spec, "assetClassifications")
        binding = next((item for item in classifications if isinstance(item, dict) and item.get("assetKind") == "runtime-profile-binding"), None)
        require(isinstance(binding, dict), "runtime-profile-binding classification missing")
        require(require_str(binding, "topic") == "/lattice/runtime/profile-binding", "runtime-profile-binding topic mismatch")
        require("runtimeRefs" in require_list(binding, "requiredRefs"), "runtime-profile-binding must require runtimeRefs")

        rules = spec.get("routingRules")
        require(isinstance(rules, dict), "routingRules must be object")
        require(rules.get("publicSurface") == "slash-topics", "publicSurface mismatch")
        require(rules.get("runtimeSubstrate") == "new-hope", "runtimeSubstrate mismatch")
        require(rules.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")
        require(rules.get("mustNotRedefinePlatformAssetRecord") is True, "mustNotRedefinePlatformAssetRecord must be true")
        require(rules.get("mustPreserveRuntimeAssetRefs") is True, "mustPreserveRuntimeAssetRefs must be true")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(f"PASS {PACK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
