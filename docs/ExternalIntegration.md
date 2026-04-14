# External integration (governance note)

Some capsule pipelines will interact with systems that are not part of the local runtime.

Governance expectations:
- such interactions are declared in the capsule manifest
- policy decisions are recorded
- outputs include provenance links so that replay can explain what influenced results

This repository defines the governance and specification surface; concrete runtime integrations live elsewhere.
