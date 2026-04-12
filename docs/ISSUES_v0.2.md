# Canonical Issues List (v0.2)

## Slash Topics × New Hope × Topic Modeling (LSA / LSI / LDA)

### Issue 1 — Canonical Slash Topic Pack Schema (Normative)
Define the authoritative schema for slash topic packs.

Includes:
- `topics.json`, `pack.json`, `manifest.json`
- Field normalization (ordering, casing, required fields)
- Content-addressed hashing (blake3)
- Versioning and supersession rules

Why it matters:
All topic models (LSA/LSI/LDA), policy enforcement, and replay depend on this object being stable and hashable.

### Issue 2 — Provenance, Signature & Trust Envelope
Make topic packs and derived artifacts cryptographically attributable.

Includes:
- Curator identity
- Snapshot + derivation lineage
- Signature coverage
- Revocation / supersession semantics

Integration:
New Hope registry + receipt emission + model artifact lineage.

### Issue 3 — Membrane Policy Binding for Slash Topics
Bind slash topics to enforceable policy decisions.

Standard outputs (required):
- `ALLOW`
- `REDACT`
- `QUARANTINE`
- `DENY`
- `REQUIRE_SIGNATURE`

Key rule:
Policy decisions must be model-aware (LSA / LSI / LDA).

### Issue 4 — TriRPC Topic Resolution & Execution Surface
Define the RPC surface that all runtimes must honor.

Endpoints:
- `TopicPack.Resolve`
- `TopicPack.List`
- `Topic.Apply`
- `Model.Select`
- `Membrane.Evaluate`
- `Receipt.Emit`

Constraint:
Cross-language identical behavior (JS / Python / Rust).

### Issue 5 — Deterministic Receipts & Replay Semantics
Make all topic execution auditable.

Receipt must include:
- Topic pack hash
- Policy version
- Model family (LSA | LSI | LDA)
- Scope (local | global)
- Training snapshot IDs
- Filters applied + reasons

Rule:
No receipt → no commons execution.

### Issue 6 — Topic Modeling Strategy Matrix (LSA / LSI / LDA)
Formalize the three model families.

| Model | Role | Determinism | Scope |
|-----|-----|------------|------|
| LSA | Linear baseline | High | Local + Global |
| LSI | User refinement | Medium | Local-first |
| LDA | Probabilistic discovery | Lower | Global-first |

Rule:
Exploratory models never silently override deterministic ones.

### Issue 7 — Per-User Local Topic Models (Local-First)
Enable user-specific models without data exfiltration.

Requirements:
- LSA + LSI only
- Offline train + infer
- No cross-user leakage
- Explicit opt-in for signed export

### Issue 8 — Global Platform Topic Models
Provide commons-grade shared models.

Requirements:
- LSA baseline for explainability
- LDA for taxonomy evolution
- Governance over training data
- Public model cards + provenance

### Issue 9 — Topic-Conditioned Dataset Construction
Standardize corpora used for training.

Must define:
- Topic-scoped corpus extraction
- Negative sampling rules
- Deduplication & contamination control
- Corpus hashes for replay

### Issue 10 — Representation Learning & Embedding Governance
Control semantic representations.

Must specify:
- Allowed embedding families
- Dimensionality + normalization
- Drift detection
- Compatibility between LSA / LSI / LDA layers

### Issue 11 — Schema-Salad Semantic Profile (Normative)
Make semantic relationships enforceable and machine-validated.

Define node types:
- Topic
- TopicPack
- Corpus
- Model
- Policy
- Receipt

Define edges:
- `derived_from`
- `trained_on`
- `governed_by`
- `signed_by`

Hash invalidation rules:
Any schema change invalidates downstream artifacts.

### Issue 12 — Local-First Execution Guarantees
Turn local-first into testable invariants.

Must specify:
- What executes air-gapped
- What must be cacheable
- How conflicts are handled offline
- Which failures are fatal vs degradable

### Issue 13 — Failure Semantics & Hard Errors
Eliminate silent or ambiguous failure.

Must define behavior for:
- Invalid or unsigned topic packs
- Missing model artifacts
- Policy conflicts
- Unsupported topic/model combinations

Rule:
Every failure must be explicit, typed, and logged into receipts.
