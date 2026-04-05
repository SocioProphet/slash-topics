# Topic Pack Provenance and Receipt Binding v0.1

## Purpose

`slash-topics` is the governed context plane in the AI+HW+State stack.

This document defines how topic packs contribute to MAIPJ receipts so that context is not treated as an anonymous blob. The point is not just retrieval. The point is:

- provenance,
- locality,
- policy scope,
- movement cost,
- replayability.

## Core rule

> If context materially influences the answer, the receipt must say which context packs were loaded, from where, under what policy, and with what movement cost.

## Topic pack identity

Every topic pack used in a governed path SHOULD expose:
- `pack_id`
- `pack_digest`
- `pack_version`
- `policy_bundle_id`
- `provenance_ref`
- `locality_class`
- `byte_size`
- `ttl` or freshness marker

### Example identity block
```json
{
  "pack_id": "topicpack://slash-topics/governance@1",
  "pack_digest": "sha256:...",
  "pack_version": "1",
  "policy_bundle_id": "hdt-policy-2026-04",
  "provenance_ref": "prov://slash-topics/governance@1",
  "locality_class": "warm-local",
  "byte_size": 32768,
  "ttl_s": 3600
}
```

## Locality classes

To support working-set and context-movement analysis, each pack SHOULD be labeled with a locality class.

Recommended classes:
- `hot-local`
- `warm-local`
- `shared-near`
- `remote-cold`
- `offline-archival`

These labels are not decorative. They should influence placement, expected fetch penalty, and movement-cost estimation.

## Receipt contribution

`slash-topics` is the authoritative source for the following receipt-aligned fields:

- `context.pack_ids`
- `context.pack_digests`
- `context.locality_class` or per-pack locality notes
- `context.total_bytes`
- `context.cache_hits`
- `context.cache_misses`
- `context.working_set_hit_rate`
- `context.remote_fetch_count`
- `context.policy_bundle_id`

## Event contract

### `context.pack.selected`
```json
{
  "event_type": "context.pack.selected",
  "payload": {
    "pack_ids": [
      "topicpack://slash-topics/community-health@1",
      "topicpack://slash-topics/governance@1"
    ],
    "pack_digests": [
      "sha256:pack01",
      "sha256:pack03"
    ],
    "policy_bundle_id": "hdt-policy-2026-04",
    "locality_class": "warm-local"
  }
}
```

### `context.pack.fetched`
```json
{
  "event_type": "context.pack.fetched",
  "payload": {
    "total_bytes": 65536,
    "cache_hits": 1,
    "cache_misses": 1,
    "working_set_hit_rate": 0.5,
    "remote_fetch_count": 1
  }
}
```

### Optional granular events
- `context.cache.hit`
- `context.cache.miss`
- `context.pack.expired`
- `context.policy.denied`

## Provenance requirements

Each pack SHOULD bind to a retrievable provenance reference that explains:
- source corpus or artifact lineage,
- build or packaging version,
- freshness or timestamp boundary,
- applied policy membrane,
- any redaction or filtering.

This does not all need to fit directly inside the receipt. The receipt may hold references. But those references must exist.

## Replay requirements

For replay support, the pack identity and digest pair must be stable enough that a later run can either:
1. re-materialize the exact pack, or
2. prove why exact re-materialization is impossible and how replay degraded.

Receipts that include pack IDs without digests are too weak for serious replay.

## Normative statements

1. Every governed path using `slash-topics` MUST emit pack IDs and digests.
2. Every pack included in a governed path SHOULD carry a provenance reference.
3. Working-set hit rate MUST be computable from emitted context events.
4. Context bytes and remote fetch count MUST be visible for MAIPJ reporting.
5. Locality class SHOULD be emitted so placement analysis can distinguish hot-local wins from remote-cold thrash.

## Why this matters for MAIPJ

Without context-side receipt binding, the benchmark can only see inference and policy behavior. That would hide the actual system bottleneck in many workflows:

- cold fetches,
- repeated misses,
- oversized packs,
- poor locality,
- governance-induced retrieval friction.

This binding makes context movement an inspectable variable instead of folklore.

## Acceptance gate for v0.1

The `slash-topics` contribution is sufficient for v0.1 when:
1. one live or captured trace emits pack IDs and digests,
2. working-set hit rate is derivable,
3. remote fetch count is visible,
4. locality class is visible,
5. the receipt builder can merge these events without case-specific glue.
