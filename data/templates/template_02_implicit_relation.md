# Template 02 — Implicit Relation

## Purpose
Train the model to infer relationships when they are implied by context,
without explicit relational verbs.

## Rules
- Extract entities normally.
- Infer a relation only if the implication is strong and unambiguous.
- If the relation is uncertain, output NO relations.
- Do not invent entities or relations.
- Confidence must be lower than Template 01 unless evidence is explicit.
- Evidence must directly support the inferred relation.

## Allowed behaviors
- Conservative inference
- Abstention

## Disallowed behaviors
- Guessing
- Over-confident relations
- Hallucinated evidence
