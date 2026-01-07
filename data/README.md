# Training Data Guidelines

This directory contains training data for the adaptive entity and relation
extraction SLM.

All data in this folder MUST comply with the canonical input format defined in:

docs/canonical_input_format.md

This format represents the post-fusion, post-enrichment document that is passed
to the Extraction Layer (SLM) in production.

---

## What is allowed

- Text-only documents written in the canonical format
- Mixed-format content (JSON, CSV, HTML, OCR) rewritten into canonical text
- Visual information expressed as textual context (not raw images)
- User commentary clearly separated from factual content
- Ambiguity and uncertainty explicitly preserved

---

## What is NOT allowed

- Raw PDFs, images, or screenshots
- Raw HTML, CSV, or JSON files without canonical rewriting
- Domain labels or domain-specific hints
- Predefined entity or relation type lists
- Schema validation instructions
- Explanatory or reasoning text in outputs

---

## Extraction Philosophy

The model is trained to behave conservatively:

- Extract entities and relations only when evidence is strong
- Prefer missing extractions over hallucinated ones
- Do not infer relations without clear textual grounding
- Preserve uncertainty rather than guessing

---

## File Format

- Data files must be in JSONL format
- One training example per line
- Each example must contain:
  - `instruction`
  - canonical document text
  - structured JSON output following the frozen schema

Any data that does not meet these requirements must not be added to this folder.