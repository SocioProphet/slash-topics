# Index

This repository defines governed scopes (slash topics) and their executable form (capsules).

## Reading order

1. `README.md`
2. `HISTORY.md`
3. `docs/SlashTopics.md`
4. `docs/Capsules.md`
5. `docs/OperatorTaxonomy.md`
6. `docs/BlekkoMechanics.md`
7. `docs/ResolutionRules.md`

## Spec surface

- Capsule manifest schema: `spec/capsule/capsule.manifest.schema.v0.1.json`
- Operator spec schema: `spec/operators/operator.schema.v0.1.json`
- Typed query schema: `spec/query/query.request.schema.v0.1.json`
- Candidate set schema: `spec/results/search.resultset.schema.v0.1.json`
- Lattice query adapter contract: `specs/LatticeQueryAdapter_v0.1.json`
- Membrane decision schema: `specs/Membrane_Decision_v0.2.json`

## Protocols

- Lattice platform asset topic pack: `protocols/lattice/platform-asset-topic-pack.v1.json`
- Lattice slash-topic-query adapter protocol: `protocols/lattice/slash-topic-query.v0.1.json`

## Fixtures

Reference fixtures live under `fixtures/` and are intended to become golden vectors for conformance tests.

- Lattice enrichment set: `fixtures/lattice/platform-asset-enrichment-set.example.json`
- Lattice adapter dry-run: `fixtures/lattice/slash-topic-query.dry-run.example.json`
- Lattice adapter live run: `fixtures/lattice/slash-topic-query.live.example.json`

## Integrations

- Lattice Studio workspace topic handoff: `docs/integrations/lattice-studio-workspace.md`
- Lattice FederatedQueryPlane adapter: `docs/LatticeQueryAdapter.md`
