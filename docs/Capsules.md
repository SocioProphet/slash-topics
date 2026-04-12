# Capsules (Slash Topic Capsules)

This project treats **slash topics** as governed scopes for search and knowledge surfaces.

A **Capsule** is the *executable* form of a slash topic: a signed, versioned, replayable pipeline that transforms a query and/or a carrier set into artifacts (ranked results, dossiers, alerts, exports), emitting deterministic receipts.

Capsules are the modern continuation of the blekko pattern:
- **slash in**: explicit scoping and selectors
- **slash out**: filters that remove noise and adversarial sources
- **inspection tools**: explainable diagnostics on domains/URLs
- **composters**: operators that turn retrieval into knowledge production

## Why “Capsule”

We avoid overloaded naming that creates semantic collisions. “Capsule” is neutral and maps well to: signed bundle + deterministic execution + replay.

## Capsule object model (v0.1)

A capsule is a **pack artifact** (content-addressed) containing:

1. `capsule.manifest.json`
   - id, version, namespace, signing keys
   - input types and output types
   - operator chain (pure/connector/sensitive)
   - policy requirements and membrane expectations
   - conformance vectors

2. `operators/`
   - operator specs (schemas + effect system)

3. `fixtures/`
   - golden inputs and expected outputs (hashes)

4. `policy/`
   - default membrane pack references and gates

## Execution semantics (normative)

1. A capsule MUST declare an operator chain.
2. Each operator MUST declare its effect surface:
   - `pure` (deterministic)
   - `connector` (network egress)
   - `sensitive` (touches private corpus)
   - `publish` (user-visible / irreversible)
3. Any `connector` or `sensitive` operator MUST sit behind a membrane rule that:
   - allows/denies the call
   - budgets calls/bytes
   - emits a decision receipt
4. Capsule outputs MUST include a receipt binding:
   - inputs (carrier refs, topic pack refs)
   - policy snapshot ref
   - operator chain digest
   - output artifact refs

## Relationship to topic packs

Topic packs define *meaning and scope*. Capsules define *execution over that scope*.

A capsule may:
- load one or more topic packs (e.g., `/science`, `/gov`, `/trusted-news`)
- apply deterministic operators
- call external search/ingest edges explicitly (never silently)

## Acceptance gate (v0.1)

A capsule is v0.1-compliant when:
- it is signed
- it is content-addressed
- it can be replayed over a fixed carrier log
- it emits an execution receipt that includes topic pack refs + policy snapshot
