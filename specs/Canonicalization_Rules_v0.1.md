# Canonicalization Rules v0.1 (Draft)

We need canonical forms so that:
- content hashes are stable across languages
- signatures cover the same bytes everywhere
- receipts are replayable and comparable

## v0.1 rules (repo-level)
- JSON is serialized with:
  - UTF-8
  - stable key order (lexicographic)
  - 2-space indentation for human artifacts (NOT normative bytes)
- Normative bytes are produced by a canonical encoder (to be specified):
  - Option A: Canonical JSON (RFC 8785-style)
  - Option B: CBOR canonical form
  - Option C: TritRPC canonical bytes for envelope-carried objects

## Signing coverage
- A pack signature MUST cover:
  - pack.json canonical bytes
  - manifest.json canonical bytes
  - policy attachments (if bundled) canonical bytes
