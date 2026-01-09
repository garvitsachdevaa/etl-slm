# Template 01 — Explicit Entity and Explicit Relation

## Purpose
This template teaches the model to extract entities and relationships when both
are explicitly stated in the text with no ambiguity.

It establishes the baseline behavior for:
- strict schema adherence
- correct entity boundary detection
- high-confidence relation extraction

## When to Use
Use this template when:
- entities are clearly named
- the relationship is directly stated (e.g., acquired, purchased, merged)
- no inference or external context is required

Do NOT use this template if the relationship must be inferred.

## Canonical Input Constraints
- Use the canonical input format defined in `docs/canonical_input_format.md`
- Source type is typically `text`
- Content quality should be `clean`
- Input should be short and unambiguous
- No user opinions or uncertainty sections

## Expected Extraction Behavior
- Extract all explicitly mentioned entities
- Extract the explicitly stated relationship
- Assign high confidence scores (≥ 0.9)
- Do not invent additional entities or relations
- Do not infer properties not present in the text
