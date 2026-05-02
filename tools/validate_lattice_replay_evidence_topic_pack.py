#!/usr/bin/env python3
"""Validate Lattice replay evidence Slash Topics pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packs" / "lattice-data-governai" / "replay-evidence-topic-pack.v0.1.json"
RAY = "runtime-asset:prophet-ray-ml:0.1.0"
BEAM = "runtime-asset:prophet-beam-dataops:0.1.0"
REQUIRED_ASSET_KINDS = {"replay-evidence-bundle", "lineage-receipt", "metric-expectation"}
REQUIRED_ARTIFACTS = {
    "urn:srcos:artifact:community_truth_demo_ray_metrics",
    "urn:srcos:artifact:community_truth_demo_beam_quality",
    "urn:srcos:model:community_truth_demo_candidate",
}
REQUIRED_RECEIPTS = {
    "urn:srcos:lineage-receipt:ray-community-truth-demo-0001",
    "urn:srcos:lineage-receipt:beam-community-truth-demo-0001",
}
REQUIRED_METRICS = {
    "factuality_f1",
    "grounding_precision",
    "training_records",
    "quality_completeness",
    "annotation_coverage",
    "duplicate_rate",
}
REQUIRED_COMMANDS = {
    "/lattice mlops ray run community_truth_demo --runtime prophet-ray-ml --dry-run",
    "/lattice dataops beam run community_truth_demo --runtime prophet-beam-dataops --dry-run",
}
REQUIRED_SOURCE_REFS = {
    "mlopsReplayEvidencePr",
    "sherlockReplayEvidencePr",
    "demoReadinessTopologyPr",
    "demoCommandBundlePr",
}


def fail(message: str) -> int:
    print(f"ERR: {message}", file=sys.stderr)
    return 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_str(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    require(isinstance(value, str) and bool(value), f"{key} must be non-empty string")
    return value


def require_list(mapping: dict[str, Any], key: str) -> list[Any]:
    value = mapping.get(key)
    require(isinstance(value, list) and value, f"{key} must be non-empty list")
    return value


def main() -> int:
    if not PACK.exists():
        return fail(f"missing {PACK}")
    try:
        data = json.loads(PACK.read_text(encoding="utf-8"))
        require(data.get("apiVersion") == "slash-topics.socioprophet.dev/v1", "apiVersion mismatch")
        require(data.get("kind") == "ReplayEvidenceTopicPack", "kind mismatch")
        metadata = data.get("metadata")
        require(isinstance(metadata, dict), "metadata must be object")
        require(metadata.get("name") == "lattice-replay-evidence", "metadata.name mismatch")
        spec = data.get("spec")
        require(isinstance(spec, dict), "spec must be object")
        require(require_str(spec, "publicSurfaceRef") == "slash-topic://lattice/data-governai/replay-evidence", "publicSurfaceRef mismatch")
        require(require_str(spec, "parentTopicPackRef") == "slash-topics://packs/lattice-data-governai@0.1.0", "parentTopicPackRef mismatch")
        require(require_str(spec, "compatibilityRef").startswith("newhope://"), "compatibilityRef must be New Hope ref")
        source_refs = spec.get("sourceRefs")
        require(isinstance(source_refs, dict), "sourceRefs must be object")
        missing = sorted(REQUIRED_SOURCE_REFS - set(source_refs))
        require(not missing, f"missing sourceRefs: {missing}")

        classifications = require_list(spec, "assetClassifications")
        kinds = set()
        for item in classifications:
            require(isinstance(item, dict), "classification must be object")
            kind = require_str(item, "assetKind")
            kinds.add(kind)
            require(kind in REQUIRED_ASSET_KINDS, f"unexpected assetKind {kind}")
            require(require_str(item, "topic").startswith("/lattice/mlops/"), "topic must be /lattice/mlops/*")
            require_list(item, "requiredRefs")
            surfaces = set(require_list(item, "consumerSurfaces"))
            require("sherlock-search" in surfaces, f"{kind} must route to Sherlock")
            require("policy-fabric" in surfaces, f"{kind} must route to Policy Fabric")
        require(kinds == REQUIRED_ASSET_KINDS, f"asset kind coverage mismatch: {sorted(kinds)}")

        bundle = spec.get("replayEvidenceBundle")
        require(isinstance(bundle, dict), "replayEvidenceBundle must be object")
        require(bundle.get("assetRef") == "urn:srcos:evidence-bundle:lattice-governed-execution-0001", "assetRef mismatch")
        require(set(require_list(bundle, "runtimeRefs")) == {RAY, BEAM}, "runtimeRefs mismatch")
        require(REQUIRED_ARTIFACTS <= set(require_list(bundle, "artifactRefs")), "artifactRefs incomplete")
        require(REQUIRED_RECEIPTS <= set(require_list(bundle, "lineageReceiptRefs")), "lineageReceiptRefs incomplete")
        require(REQUIRED_METRICS <= set(require_list(bundle, "metricNames")), "metricNames incomplete")
        require(REQUIRED_COMMANDS <= set(require_list(bundle, "replayCommandRefs")), "replayCommandRefs incomplete")
        safety = bundle.get("safety")
        require(isinstance(safety, dict), "safety must be object")
        require(safety.get("network") == "none", "network must be none")
        require(safety.get("secrets") == "none", "secrets must be none")
        require(safety.get("hostMutation") is False, "hostMutation must be false")

        rules = spec.get("routingRules")
        require(isinstance(rules, dict), "routingRules must be object")
        require(rules.get("publicSurface") == "slash-topics", "publicSurface mismatch")
        require(rules.get("runtimeSubstrate") == "new-hope", "runtimeSubstrate mismatch")
        require(rules.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")
        require(rules.get("mustNotRedefinePlatformAssetRecord") is True, "mustNotRedefinePlatformAssetRecord must be true")
        require(rules.get("mustPreserveReplayEvidenceRefs") is True, "mustPreserveReplayEvidenceRefs must be true")
        require(rules.get("mustPreserveRuntimeAssetRefs") is True, "mustPreserveRuntimeAssetRefs must be true")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(f"PASS {PACK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
