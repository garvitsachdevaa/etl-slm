# Template 11 — User Commentary & Opinions

## Purpose
Train the model to handle subjective, speculative, or emotional
user-generated content safely.

## Input Characteristics
- Opinions
- Speculation
- Emotional language
- Assertions without evidence

## Rules
- Extract entities only if clearly named.
- Do NOT extract relations based on opinion.
- Treat confidence and certainty as irrelevant.
- Prefer abstention unless facts are explicit.

## Allowed behaviors
- Entity extraction under commentary
- Full abstention

## Disallowed behaviors
- Treating opinions as facts
- Inferring relations from belief statements
