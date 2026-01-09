# Template 10 — Conflicting Information

## Purpose
Train the model to handle documents where multiple sources
or sections provide conflicting information.

## Input Characteristics
- Contradictory statements
- Rumors vs confirmations
- Updates negating earlier claims
- Mixed authoritative and non-authoritative text

## Rules
- Extract entities consistently.
- Do NOT extract relations if claims conflict.
- Prefer explicit negation or correction.
- Abstain rather than guess.
- Confidence should not override contradiction.

## Allowed behaviors
- Entity extraction under conflict
- Relation abstention

## Disallowed behaviors
- Picking a side
- Majority-vote reasoning
- Confidence-based guessing
