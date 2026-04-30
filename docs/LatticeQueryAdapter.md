# Slash Topics Query Adapter for Lattice FederatedQueryPlane

## Overview

Slash Topics functions as a first-class backend in the Lattice `FederatedQueryPlane` under the backend identifier `slash-topic-query`. This document describes the adapter contract that governs how Lattice routes topic-scoped queries to Slash Topics, enforces policy membranes, and collects deterministic receipts.

## Normative contract

The normative JSON Schema for the adapter is at:

```
specs/LatticeQueryAdapter_v0.1.json
```

The protocol definition (step-by-step lifecycle) is at:

```
protocols/lattice/slash-topic-query.v0.1.json
```

## Lattice FederatedQueryPlane mapping

| Lattice concept | Slash Topics binding |
|---|---|
| `FederatedQueryPlane` | The Lattice routing plane this adapter registers with |
| Backend language `slash-topic-query` | Identifies Slash Topics as the backend |
| `routeRef` | Content-addressed reference to the Lattice route policy bundle |
| Topic scope | `topicScope.topicSlugs` — slash-prefixed topic slugs that filter results |
| Topic pack | `topicScope.topicPackRef` + `topicPackDigest` — signed, versioned topic pack |
| Policy membrane | `policyMembrane.membraneRef` — content-addressed policy bundle |
| Governed search | `scopedSearch.queryRef` scoped to resolved topic slugs |
| Deterministic receipt | `deterministicReceipt` block — hash-signed, replayable |

## Dry-run mode

Dry-run mode validates route and policy **without** reading topic packs or executing search.

Enable dry-run by including the `dryRun` object in an adapter request:

```json
{
  "dryRun": {
    "enabled": true,
    "validateRoute": true,
    "validatePolicy": true,
    "noPackRead": true,
    "noSearchExecute": true
  }
}
```

### Dry-run lifecycle

1. **resolve-route** — Confirm `latticeBackend.routeRef` resolves to a known, authorised route. No pack bytes fetched.
2. **validate-topic-scope** — Check that all slugs have a valid slash-prefix. If `topicPackRef` is provided, validate the reference is syntactically correct without fetching bytes.
3. **resolve-membrane** — Resolve `policyMembrane.membraneRef` and confirm `requiredDecision` is reachable for the given topic scope and policy tags.
4. **emit-dry-run-receipt** — Emit a receipt with `dryRun: true`. The receipt MUST NOT include `resultSetRef`.

### Dry-run invariants

- No topic pack bytes are read at any step.
- No search query is issued at any step.
- The emitted receipt contains `resultSetRef: null`.

## Live execution lifecycle

1. **resolve-route** — Same route resolution as dry-run.
2. **membrane-check** — Evaluate the policy membrane. `DENY` or `QUARANTINE` decisions halt the pipeline and emit a denial receipt.
3. **load-topic-pack** — Fetch pack bytes, verify digest, emit `context.pack.selected` and `context.pack.fetched` provenance events.
4. **execute-scoped-search** — Issue the search query scoped to resolved topic slugs, applying `maxHits` and `constraints`.
5. **emit-receipt** — Emit a deterministic receipt covering all required fields (see below), canonicalized and optionally signed.

## Policy membrane

The membrane is evaluated **before** any topic pack is read or any search is issued. Supported decisions follow `specs/Membrane_Decision_v0.2.json`:

| Decision | Effect |
|---|---|
| `ALLOW` | Pipeline proceeds normally |
| `REDACT` | Pipeline proceeds; specified fields are redacted in results |
| `REQUIRE_SIGNATURE` | Pack or result must carry a valid signature before release |
| `QUARANTINE` | Execution halted; quarantine receipt emitted |
| `DENY` | Execution halted; denial receipt emitted |

## Deterministic receipt

Every live execution MUST emit a receipt with these fields:

| Field | Description |
|---|---|
| `adapterKind` | `"slash-topic-query"` |
| `adapterVersion` | `"0.1"` |
| `topicSlugs` | Resolved topic slug list |
| `topicPackRef` | Pack URI (or `null`) |
| `topicPackDigest` | Pack blake3 hash (or `null`) |
| `membraneRef` | Policy bundle reference |
| `membraneDecision` | Decision obtained |
| `queryRef` | Reference to original `QueryRequest` |
| `resultSetRef` | Reference to result set (`null` in dry-run) |
| `executedAt` | ISO-8601 timestamp |
| `rng_seed_or_none` | RNG seed when bounded nondeterminism is declared; otherwise `null` |
| `canonicalization` | Canonicalization rules used to hash the receipt |

Receipts are canonicalized and hashed using blake3 (lexicographic key ordering, UTF-8, JSON format) per `specs/Canonicalization_Rules_v0.1.md`.

## Provenance and replay

Each adapter invocation SHOULD bind to a `provenanceRef` that explains:

- source corpus or topic pack lineage,
- policy membrane applied,
- any redactions or filtering,
- pack locality class (e.g. `warm-local`, `remote-cold`).

For replay, the `topicPackRef` + `topicPackDigest` pair MUST be stable: a later run can re-materialize the exact pack or declare a degradation receipt explaining why exact replay is impossible.

Working-set hit rate, remote fetch count, and total context bytes MUST be derivable from the `packLoadEvents` emitted during provenance tracking (aligned to `spec/topicpack/provenance_and_receipt_binding.md`).

## Fixtures

| Fixture | Description |
|---|---|
| `fixtures/lattice/slash-topic-query.dry-run.example.json` | Dry-run adapter request and expected validation output |
| `fixtures/lattice/slash-topic-query.live.example.json` | Live adapter request with topic pack load events and full receipt |

## Related artifacts

| Artifact | Purpose |
|---|---|
| `specs/LatticeQueryAdapter_v0.1.json` | Normative adapter contract schema |
| `protocols/lattice/slash-topic-query.v0.1.json` | Protocol lifecycle definition |
| `specs/Membrane_Decision_v0.2.json` | Policy membrane decision schema |
| `specs/SlashTopics_Schema_v0.1.json` | Slash Topics pack schema |
| `specs/Canonicalization_Rules_v0.1.md` | Canonicalization rules for hashing and signing |
| `spec/topicpack/provenance_and_receipt_binding.md` | Provenance and receipt binding spec |
| `spec/query/query.request.schema.v0.1.json` | Upstream QueryRequest schema |
| `spec/results/search.resultset.schema.v0.1.json` | Result set schema |
| `policies/commons-default@0.1.0/policy.json` | Default governance policy |
