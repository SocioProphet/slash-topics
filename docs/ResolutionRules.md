# Resolution rules (full name, short name, follows)

Slash topics and capsules must resolve deterministically.

## Terms

- **full name**: `/namespace/slug` (canonical)
- **short name**: `/slug` (UI convenience)
- **follow set**: an ordered list of namespaces consulted when resolving short names

## Deterministic resolution algorithm (v0.1)

Given an input token `/slug`:

1) If the token is already a full name (`/ns/slug`), it resolves to itself.

2) Otherwise, resolution consults the follow set in order:
- `/me/slug`
- `/team/slug`
- `/org/slug`
- `/commons/slug`

3) If multiple matches exist at the same precedence level, the resolver MUST:
- prefer the highest-trust signing key per current policy, or
- refuse resolution and require explicit full name

4) If no match exists:
- the resolver returns `unresolved` and SHOULD include suggestions (edit distance + category hints)

## Audit requirements

Every resolution MUST be explainable.

A resolution receipt SHOULD include:
- input token
- resolved full name (or unresolved)
- follow set snapshot hash
- policy snapshot hash
- winning pack digest and signer key ref (if resolved)

## Acceptance gate (v0.1)

We have resolution sufficiently specified when:
- the algorithm is deterministic
- ambiguity behavior is defined
- the receipt schema can encode the decision
