# Blekko mechanics we inherit (and harden)

This document records the operational mechanics we want from the blekko lineage, while explicitly upgrading the missing organs: provenance, governance, and replay.

## 1) Slash-in / slash-out

Blekko’s core move was making scope *syntactic*:
- **slash-in** = constrain into an explicit scope (topic directory)
- **slash-out** = exclude noise and adversarial sources

In this repo:
- slash topics -> governed scopes
- capsules -> executable pipelines over those scopes

## 2) Operators vs inspection tools vs integrations

We must separate three conceptually different things that blekko visually colocated.

1) **Operators** (deterministic transforms)
- filter, sort, time-window, dedupe
- should be `pure` by default

2) **Inspection tools** (diagnostics)
- show evidence about domains/URLs (link graphs, duplicates, cache snapshots)
- can be pure if computed locally, or `connector` if it consults external systems

3) **Integrations** (calls out of the trust boundary)
- any external system interaction must be explicit and policy-gated

The operator spec must declare which class it is (and its effect surface).

## 3) Full name and resolution behavior

Blekko effectively used a stable canonical name under the hood while allowing short names in the UI.

We standardize:
- **full name**: `/namespace/slug`
- **short name**: `/slug` (resolved via follow defaults)

Resolution MUST be deterministic and explainable.

## 4) Private-by-default and promotion

Blekko’s default privacy simplified distribution.

In a governed commons:
- everything begins private unless explicitly promoted
- promotion is a signed act with policies and receipts
- revocation must be modeled (no silent deletion)

## 5) Auto-application behavior

Blekko sometimes applied scopes automatically.

In a governed system, auto-application is a *planner decision* that must emit a trace:
- which scope/capsule was applied
- why
- what fallback happened if results were sparse

## 6) Acceptance gate

We have captured blekko mechanics sufficiently when:
- slash-in/out is modeled via operator families and type signatures
- resolution rules are explicit
- promotion and revocation semantics exist
- auto-application decisions emit trace outputs
