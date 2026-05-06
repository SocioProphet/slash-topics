# slash-topics

Slash topics are governed, signed, replayable “scopes” for search and knowledge surfaces.

This repo turns the blekko-era idea (explicit scoping via `/topic`) into 2025-grade commons infrastructure:
- topic packs as signed artifacts
- policy membranes as enforceable gates
- deterministic receipts for audit/replay
- TritRPC alignment for cross-language interoperability

Start in:
- HISTORY.md (origins + motivation)
- docs/SlashTopics.md (the spec overview)
- specs/*.json (normative schemas)
- protocols/ (versioned packs)
- policies/ (default governance bundles)

## Personal Intelligence Cell surface

The Personal Intelligence Cell slash-topic surface is now represented as a first normative cell-specific surface:

- `specs/personal-intelligence-cell-surface.schema.json`
- `examples/personal-intelligence-cell/surface.example.json`
- `scripts/validate_personal_intelligence_cell_surface.py`

Validate locally:

```bash
python3 scripts/validate_personal_intelligence_cell_surface.py
```

This surface maps the `prophet-platform` cell-service lineage:

```text
Cell -> Watch -> Signal -> FeedItem -> SlashTopicSurface
```

into a governed `/cell/<kind>/<slug>` topic with policy decision refs, evidence refs, and replay metadata.
