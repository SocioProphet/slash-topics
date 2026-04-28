# Lattice Studio Workspace Topic Handoff

Slash Topics provides the governed topic vocabulary for Lattice Studio workspace-grounding artifacts.

## Topic pack

The initial topic pack lives at:

```text
protocols/lattice-studio-workspace-topic-pack.v0.json
```

It scopes topic generation for:

```text
WorkspaceSource
WorkspaceSourceBinding
WorkspaceSynthesisArtifact
WorkspaceActionReceipt
PlatformAssetRecord
PlatformAssetRecordEnrichment
```

## Integration contract

Lattice Studio emits `PlatformAssetRecordEnrichmentSet` sidecars. Slash Topics should treat the `slashTopics` field as deterministic topic candidates that may later be signed as topic-pack outputs.

The canonical identity remains `PlatformAssetRecord`; topic enrichment must never overwrite asset identity, policy reference, evidence correlation, or producer repository fields.

## Required doctrine

Workspace source-grounded synthesis must be scoped as both:

```text
/workspace/synthesis
/source-grounded-synthesis
```

That makes generated reports discoverable as governed source-grounded artifacts rather than generic documents.
