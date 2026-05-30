# Governed Topic-Pack Membrane v0

Status: draft recovery contract  
Authority repo: `SocioProphet/slash-topics`  
Claim level: product/semantic architecture; no runtime commitment without consuming repo adoption  
Scope: topic-pack membrane semantics for governed search, knowledge, workroom, and intelligence surfaces

## Purpose

This document recovers slash-topics as the governed topic-pack membrane for the SocioProphet estate.

A slash topic is not just a label or UI route. It is a governed scope that controls which sources, evidence, policies, operators, integrations, preferences, receipts, and display behaviors are admitted for a search or knowledge surface.

The recovered role is to make topic packs navigable and enforceable without turning them into hidden memory bridges or unreviewed policy shortcuts.

## Existing repo posture

The repository already defines slash topics as governed, signed, replayable scopes for search and knowledge surfaces. It already expects:

- topic packs as signed artifacts;
- policy membranes as enforceable gates;
- deterministic receipts for audit/replay;
- TritRPC alignment for cross-language interoperability.

This document does not replace those foundations. It defines the membrane contract that downstream systems should follow when they claim slash-topic compatibility.

## Membrane definition

A governed topic-pack membrane is the boundary around a topic scope.

It answers:

- what content is in scope;
- what sources are trusted or excluded;
- what evidence is required;
- which policies apply;
- which operators are allowed;
- which integrations are sandboxed;
- what privacy posture applies;
- what execution receipt must be emitted;
- what display or ranking behavior is permitted;
- what must be quarantined, redacted, denied, or reviewed.

## Core objects

### TopicPack

A versioned artifact describing a topic scope, source set, allowed operators, evidence requirements, policy references, display behavior, and receipt expectations.

### TopicMembrane

The enforceable boundary around a topic pack. It decides what can enter, leave, be joined, be displayed, be learned, or be linked.

### SourceScope

The admitted, excluded, candidate, or quarantined sources for the topic.

### EvidenceRequirement

The minimum evidence required for claims, summaries, search answers, recommendations, actions, or teaching objects inside the topic.

### PolicyBinding

The policy bundle controlling allow, deny, quarantine, redact, require-signature, require-review, and bounded nondeterminism behavior.

### OperatorSurface

The allowed operators for the topic, including filters, date ranges, ranking operations, transformations, retrieval modes, and integration calls.

### IntegrationBoundary

The sandbox and permission scope for external calls or cross-repo integrations invoked through the topic.

### TopicReceipt

A deterministic or bounded-nondeterministic execution receipt recording query, topic pack version, policy decision refs, source/evidence refs, operators, integrations, output hashes, and replay metadata.

### DisplayContract

Rules for how results, claims, uncertainty, provenance, redaction, quarantine, and review-required states are shown to users or agents.

## Required invariants

1. A topic pack is not a memory permission.
2. A topic membership edge is not an identity link.
3. A search result is not an admitted claim.
4. A ranking result is not evidence by itself.
5. A policy membrane must not silently bypass DoNotLearn or DoNotLink.
6. An integration call must be explicit and sandboxed.
7. Every execution emits a receipt or declares bounded nondeterminism.
8. Topic packs are versioned artifacts with content hashes.
9. Signed packs and policies may be federated, but signature validity is not content validity.
10. A topic pack may require review even when retrieval succeeds.

## Downstream consumers

| Consumer | Safe use |
| --- | --- |
| `prophet-platform` | Workroom topic scopes, search views, topic-pack UX, and memory-aware display contracts. |
| `sherlock-search` | Retrieval scoping, source admission, evidence requirements, and answer receipt generation. |
| `holmes` | Reasoning/explanation traces constrained by topic evidence and claim boundaries. |
| `ontogenesis` | Semantic vocabulary, SlashTopicProfile alignment, governed-intelligence object bindings. |
| `sociosphere` | Cross-repo adoption projection and workspace/workroom route integration. |
| `TriTRPC` | Candidate transport/framing alignment for topic-pack receipts and cross-language interoperability. |
| `model-governance-ledger` | Topic execution receipts, drift, evaluation, and adoption records. |
| `systems-learning-loops` | Lessons and patterns derived from topic-pack failures, drift, and recovery. |

## Product boundary

Slash-topics is not the whole product surface. It is the governed membrane for topic scopes.

Prophet Platform may render topic experiences. Sherlock may retrieve. Holmes may reason. Ontogenesis may define semantic terms. Sociosphere may route workrooms. TriTRPC may frame transport. The topic pack membrane coordinates these roles but does not replace their authority.

## Privacy boundary

Topic packs must respect DoNotLearn and DoNotLink.

A topic pack may admit a source for ephemeral search while denying durable memory formation. It may show a redacted result while preventing cross-topic linkage. It may allow a claim inside one workroom while preventing another workroom from inheriting that claim as reusable context.

DoNotLearn primarily constrains topic-pack movement into memory, model state, durable summaries, vector indexes, profiles, and teaching objects.

DoNotLink primarily constrains cross-topic joins, identity bridges, latent-neighbor exposure, graph edges, and workroom-to-workroom references.

## Promotion discipline

A topic-pack membrane becomes implementation-ready only after:

1. topic pack schema or existing schema reference;
2. policy-binding schema or policy bundle;
3. example pack;
4. example receipt;
5. validator or review gate;
6. consuming repo integration point;
7. privacy and evidence-boundary review;
8. versioning policy.

## Non-goals

This document does not change existing schemas, does not define a new wire protocol, does not force Prophet Platform adoption, does not define a search ranking algorithm, and does not make every topic pack public or federated.

It also does not claim that topic packs solve privacy, provenance, ranking, moderation, or trust. They provide a membrane where those decisions can be declared, enforced, and receipted.

## Claim boundary

This is a recovery and placement contract. It preserves slash-topics as a governed topic-pack membrane while keeping runtime authority in consuming systems and policy authority in explicit policy bundles.
