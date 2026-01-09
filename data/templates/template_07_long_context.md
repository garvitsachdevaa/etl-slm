# Template 07 — Long Context & Cross-Paragraph Reasoning

## Purpose
Train the model to extract entities and relations from long documents
where evidence is distributed across multiple sections.

## Input Characteristics
- Multiple paragraphs or sections
- Entities introduced early
- Relations stated later
- Distractor information in between

## Rules
- Track entities across sections.
- Do NOT infer relations early.
- Extract relations only when explicitly stated.
- Use the strongest textual evidence available.

## Allowed behaviors
- Deferred relation extraction
- Cross-paragraph entity linking

## Disallowed behaviors
- Proximity-based inference
- Guessing relations from narrative flow
