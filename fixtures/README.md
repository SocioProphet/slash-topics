# Fixtures

Fixtures are golden vectors used for conformance testing.

v0.1 goals:
- validate capsule manifest schema acceptance
- validate deterministic resolution decisions (short name -> full name) and the emitted receipt fields
- validate operator spec schema acceptance
- validate query/resultset schema acceptance

Each fixture should include:
- an input JSON object
- expected output JSON object(s)
- expected hashes (canonicalized)

Fixtures are intentionally minimal in v0.1; they become strict as the runtime hardens.
