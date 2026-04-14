# Operator taxonomy (v0.1)

Slash topics revive blekko-style explicit scoping, but the platform must distinguish four operator families.

## 1) Filters (slash-out)

Reduce candidate sets.

Examples:
- `/out:domain=example.com`
- `/out:regex=...`
- `/out:lang=en`
- `/out:trust<0.6`

Norms:
- Filter operators SHOULD be pure/deterministic.
- Filters MUST emit an explanation record when they remove results that would otherwise rank in top-K.

## 2) Selectors (slash-in)

Whitelist or constrain to explicit sets.

Examples:
- `/in:domain=*.gov`
- `/in:source=trusted`
- `/in:collection=/commons/science`

Norms:
- Selectors SHOULD be pure/deterministic.
- Selector packs SHOULD be signable allowlists.

## 3) Aggregators (merge + dedupe + rerank)

Combine multiple corpora/engines and resolve conflicts.

Examples:
- metasearch merge
- cross-index merge (local index + web)
- entity-level dedupe

Norms:
- Aggregators MUST emit `DecisionTrace` describing:
  - sources consulted
  - dedupe decisions
  - rerank features
  - thresholds and backoff behavior

## 4) Composters (knowledge production)

Transform retrieval output into new durable artifacts.

Examples:
- dossier builder
- evidence bundle compiler
- claim extraction
- entity graph emission
- RSS/feed export

Norms:
- Composters MUST emit artifact refs and receipts.
- Composters MUST preserve parent refs (provenance).

## Effect system (required)

Each operator declares exactly one primary effect surface:
- `pure`
- `connector`
- `sensitive`
- `publish`

Any non-`pure` operator MUST run behind membrane policy gates.

## Acceptance gate (v0.1)

- Each operator family has at least one reference operator spec.
- Each operator spec declares:
  - input type
  - output type
  - effect surface
  - required receipts/trace outputs
