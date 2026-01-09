# Template 09 — Noisy OCR & Corrupted Text

## Purpose
Train the model to handle severely degraded OCR text
without hallucinating entities or relations.

## Input Characteristics
- Broken words
- Missing characters
- Line scrambling
- OCR misreads (0/O, 1/I, rn/m)

## Rules
- Extract entities ONLY if identity is still clear.
- Reduce type_confidence when text is corrupted.
- Abstain if relation meaning is ambiguous.
- Never "fix" text creatively.
- Prefer abstention over incorrect extraction.

## Allowed behaviors
- Low-confidence entity extraction
- Partial extraction with abstention

## Disallowed behaviors
- Guessing missing words
- Completing corrupted relations
