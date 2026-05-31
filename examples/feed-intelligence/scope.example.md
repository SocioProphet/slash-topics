# Feed Intelligence slash-topic scope example

Status: example-only contract

This example maps the canonical SocioProphet Feed Intelligence reader into SlashTopics without changing runtime behavior, schemas, validators, or policy bundles.

Canonical reader surface:

```text
SocioProphet/socioprophet/socioprophet-web/client-vue
```

## Purpose

Feed Intelligence lanes need governed, replayable scopes. SlashTopics owns that public query and governance boundary. The reader may render feed state, but each feed lane or saved search should resolve to a slash-topic scope before New Hope membrane evaluation, MemoryMesh recall posture, MeshRush graph preparation, or derived publication.

## Example scopes

```yaml
scopes:
  - id: feed-global-news
    topic: /news/global
    kind: feed-intelligence-source
    sourceClass: rss
    publicSurfaceRef: socioprophet-feed-intelligence-reader
    downstreamMembraneRef: new-hope-feed-item-membrane
    memoryProfileRef: memorymesh-feed-intelligence-profile
    graphViewRef: meshrush-feed-item-graph-view
    privacyPosture: public-source-private-annotation
    receipts:
      required:
        - feed.subscribed
        - item.fetched
        - item.normalized
        - membrane.evaluated

  - id: feed-browser-capture
    topic: /capture/browser
    kind: browser-capture-source
    sourceClass: bearbrowser-capture
    publicSurfaceRef: socioprophet-feed-intelligence-reader
    downstreamMembraneRef: new-hope-feed-item-membrane
    memoryProfileRef: memorymesh-local-only-capture-profile
    graphViewRef: meshrush-feed-item-graph-view
    privacyPosture: local-only-by-default
    receipts:
      required:
        - browser.page.captured
        - browser.provenance.attached
        - item.normalized
        - membrane.evaluated
```

## Boundary rules

- SlashTopics defines the governed scope; it does not fetch feeds.
- BearBrowser may discover or capture browser-originated content, but it does not define the scope policy.
- New Hope evaluates whether a normalized feed item is admitted, held, quarantined, or rejected.
- MemoryMesh may attach scoped recall and review-only writeback posture only after scope and membrane resolution.
- MeshRush may prepare graph views only as governed evidence structure.
- ActivityPub publication is never implied by scope creation.

## Acceptance posture

This example is acceptable when it remains a contract example and does not claim live feed ingestion, live publication, memory writeback, or graph traversal.
