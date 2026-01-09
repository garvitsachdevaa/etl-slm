# Template 03 — Abstention Under Ambiguity

## Purpose
Train the model to abstain from extracting relationships when evidence
is incomplete, vague, speculative, or conflicting.

## Rules
- Always extract entities when they are clearly mentioned.
- Extract NO relations unless evidence is explicit and unambiguous.
- Words indicating speculation, intent, possibility, or discussion
  are NOT sufficient for relation extraction.
- If multiple interpretations are possible, abstain.
- Never use external or world knowledge to resolve ambiguity.
- Confidence should not be used to justify guessing.

## Allowed behaviors
- Entity-only output
- Empty relations array

## Disallowed behaviors
- Guessing relations
- Filling in missing context
- Overconfident inference
