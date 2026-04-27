#!/usr/bin/env python3
"""Replay Lattice topic-pack assignments against PlatformAssetRecord enrichments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def matches(match: dict[str, Any], facets: dict[str, Any]) -> bool:
    return all(facets.get(key) == value for key, value in match.items())


def replay(topic_pack: dict[str, Any], enrichment_set: dict[str, Any]) -> dict[str, Any]:
    if topic_pack.get("kind") != "SlashTopicPack":
        raise ValueError("topic pack kind must be SlashTopicPack")
    if enrichment_set.get("kind") != "PlatformAssetRecordEnrichmentSet":
        raise ValueError("enrichment set kind must be PlatformAssetRecordEnrichmentSet")

    subjects = topic_pack.get("subjects")
    enrichments = enrichment_set.get("enrichments")
    if not isinstance(subjects, list):
        raise ValueError("topic pack subjects must be a list")
    if not isinstance(enrichments, list):
        raise ValueError("enrichments must be a list")

    assignments = []
    for enrichment in enrichments:
        if not isinstance(enrichment, dict):
            continue
        asset_id = enrichment.get("assetId")
        facets = enrichment.get("search", {}).get("facets", {})
        if not isinstance(asset_id, str) or not isinstance(facets, dict):
            continue
        topics: set[str] = set(enrichment.get("slashTopics", []))
        matched_rules = []
        for index, subject in enumerate(subjects):
            if not isinstance(subject, dict):
                continue
            if subject.get("subjectKind") != "PlatformAssetRecord":
                continue
            match = subject.get("match", {})
            if isinstance(match, dict) and matches(match, facets):
                topics.update(str(topic) for topic in subject.get("topics", []))
                matched_rules.append(index)
        assignments.append({
            "assetId": asset_id,
            "matchedRules": matched_rules,
            "topics": sorted(topic for topic in topics if isinstance(topic, str) and topic.startswith("/")),
        })

    return {
        "apiVersion": "slash-topics.socioprophet.dev/v1",
        "kind": "SlashTopicReplayReport",
        "topicPack": topic_pack.get("metadata", {}).get("name"),
        "assignments": assignments,
    }


def emit(report: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay Lattice Slash Topic assignments")
    parser.add_argument("topic_pack", type=Path)
    parser.add_argument("enrichment_set", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        emit(replay(load_json(args.topic_pack), load_json(args.enrichment_set)), args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"replay_lattice_topics: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
