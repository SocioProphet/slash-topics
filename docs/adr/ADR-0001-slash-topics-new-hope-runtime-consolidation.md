# ADR-0001: Consolidate New Hope membrane runtime under the Slash Topics product surface

Status: Proposed
Date: 2026-04-30

## Context

Slash Topics is the visible query/search scope primitive. The repository defines slash topics as governed, signed, replayable scopes for search and knowledge surfaces, with topic packs, policy membranes, deterministic receipts, and TriTRPC alignment as first-class pieces. Its overview states that topic packs are versioned artifacts with content hashes, packs and policies can be signed/federated, membranes enforce allow/deny/quarantine/redact/require-signature, and every execution emits a deterministic receipt or declares bounded nondeterminism.

New Hope is a higher-order semantic runtime for the commons. Its specification defines the runtime objects that Slash Topics needs when query routing becomes more than static scoping: protocol, signal, carrier, receptor, membrane, receptor system, provenance, replay, and federation. Its membrane minimum requires allow/deny/quarantine, redaction, fidelity downgrade, additional signatures, rate limits, and egress controls.

Lattice query routing now treats Slash Topics and New Hope as a governance envelope before physical backend selection:

1. Slash Topic scope.
2. New Hope membrane admission.
3. Memory Mesh recall/writeback policy.
4. Lab profile selection.
5. Physical backend route.

The unresolved product question is whether `new-hope` should remain a separate product/repo name, merge into Slash Topics, or become an internal runtime layer beneath Slash Topics.

## Decision

Use **Slash Topics** as the public product and query/governance surface. Treat **New Hope** as the internal membrane/runtime substrate under Slash Topics.

Recommended public naming:

- Product surface: **Slash Topics**.
- Runtime layer: **Slash Topics Runtime**.
- Membrane layer: **Slash Topics Membrane Runtime**.
- Protocol compatibility surface: **New Hope Protocol Pack**, retained as a compatibility name during migration.

Do not delete New Hope concepts. Do not immediately merge repositories. Instead, establish a compatibility bridge:

- `SocioProphet/slash-topics` owns the public/query-facing product language, topic scopes, topic packs, policy membrane references, deterministic receipts, Lattice adapter contract, and public docs.
- `SocioProphet/new-hope` remains the repo-native source for runtime substrate concepts until the Slash Topics runtime layer has equivalent schemas and conformance fixtures.
- New Hope carrier/receptor/protocol/membrane objects remain valid compatibility objects.
- Future migration MAY move or mirror New Hope protocol-pack objects under Slash Topics once downstream references are stable.

## Vocabulary mapping

| Public Slash Topics term | New Hope runtime term | Consolidated meaning |
|---|---|---|
| Slash topic scope | `policy_context.community` / topic context | The visible scope that binds query, memory, and policy posture. |
| Topic pack | Protocol Pack / carrier input set | Versioned signed scope artifact; may select runtime protocols or carrier families. |
| Policy membrane | Membrane | Enforcement point for allow/deny/quarantine/redact/require-signature/rate-limit decisions. |
| Deterministic receipt | Trace graph / provenance output | Replayable evidence that the query route, membrane decision, and result constraints were applied. |
| Scoped search/query | Receptor graph execution | Query request admitted through a membrane and then routed to a backend or receptor. |
| Provenance event | Carrier provenance / transforms | Evidence chain for who/what emitted or transformed a scoped signal. |
| Federation | Receptor system federation | Controlled cross-system relay of signed, policy-admitted artifacts. |
| Memory setting | Memory Mesh profile | Slash-topic-scoped recall/writeback/retention/redaction posture attached to the route. |

## Lattice query-routing implication

Lattice MUST reference Slash Topics as the visible route scope and New Hope as the membrane runtime substrate.

Recommended refs:

```yaml
governanceEnvelope:
  topicScopeRef: slash-topic://lattice/federated-query
  topicPackRef: slash-topics://packs/lattice-federated-query@0.1.0
  membraneRef: newhope://membranes/query-admission@0.1.0
  memoryProfileRef: memory-mesh://profiles/slash-topic-scoped-recall@0.1.0
  memoryEventRef: memory-mesh://events/query-route-dry-run
  requiredSequence:
    - slash-topic-scope
    - newhope-membrane-admission
    - memory-mesh-recall-policy
    - lab-profile-selection
    - physical-backend-route
```

Future refs SHOULD migrate toward Slash Topics-owned runtime aliases while preserving New Hope compatibility:

```yaml
membraneRef: slash-topics://runtime/membranes/query-admission@0.1.0
compatibilityRef: newhope://membranes/query-admission@0.1.0
```

## Memory Mesh attachment

Memory Mesh settings attach to Slash Topic scopes, not directly to physical backends.

Rules:

1. Every governed query route SHOULD carry a `memoryProfileRef` selected by Slash Topic scope.
2. Dry-run routing MUST emit only memory event/evidence refs and MUST NOT read memory or write back memory.
3. Recall, writeback, retention, redaction, summarization, promotion, forgetting, and evidence refs belong to the Memory Mesh profile.
4. Physical backends such as Sherlock, Drill, SPARQL, Cypher, Lampstand, and Atomese MUST NOT bypass the Slash Topics/New Hope/Memory Mesh envelope for nontrivial governed query routes.

## Migration plan

Phase 0 — Current state

- Slash Topics owns public scoping, topic packs, membrane references, receipts, and the Lattice `slash-topic-query` adapter.
- New Hope owns carrier/receptor/membrane runtime objects and protocol-pack compatibility.
- Lattice references both directly.

Phase 1 — Alias layer

- Add Slash Topics runtime aliases for New Hope membrane refs.
- Document `newhope://` refs as compatibility refs.
- Keep New Hope protocol-pack schemas valid and tested.

Phase 2 — Mirrored contracts

- Mirror or import New Hope protocol-pack object definitions into Slash Topics runtime docs.
- Add conformance fixtures proving equivalence between Slash Topics runtime aliases and New Hope compatibility refs.

Phase 3 — Repository consolidation decision

- Decide whether to physically merge repos only after all downstream references can use Slash Topics-owned aliases.
- If merged, retain New Hope path aliases and compatibility docs for at least one major version.

## Consequences

Benefits:

- Public product language becomes clearer: users see Slash Topics, not an awkward parallel New Hope brand.
- Runtime concepts are preserved rather than flattened.
- Lattice query routing gets a precise governance sequence.
- Memory Mesh policy attaches to the human-visible topic scope.
- New Hope compatibility remains explicit for existing protocol-pack work.

Costs:

- Two repos remain active during the transition.
- Documentation must clearly distinguish product surface from runtime substrate.
- Future alias/conformance work is required before any repo merge.

## Non-goals

- No broad rename in this ADR.
- No deletion of New Hope protocol-pack objects.
- No runtime execution implementation.
- No change to physical backend adapters.
- No production migration without a separate versioned plan.

## Acceptance criteria mapping

- Evidence-based recommendation: Slash Topics is public surface; New Hope is internal runtime substrate.
- Repo references: Slash Topics docs define scoped signed query objects; New Hope docs define carriers, receptors, membranes, provenance, replay, and federation.
- Compatibility: New Hope protocol-pack objects remain valid compatibility objects.
- Lattice routing: governance envelope references Slash Topic scope, New Hope membrane, Memory Mesh profile, and backend route.
- Memory Mesh: memory settings attach to Slash Topic scopes.
