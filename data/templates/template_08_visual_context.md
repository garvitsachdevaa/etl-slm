# Template 08 — Visual Context & Image-Linked Text

## Purpose
Train the model to handle documents containing images, figures,
screenshots, or scanned pages with associated text.

## Input Characteristics
- Image captions
- OCR-extracted text
- References like "see figure above"
- Mixed visual + textual context

## Rules
- Extract entities ONLY from text, OCR, or captions.
- Never infer entities from images alone.
- Use the `source` field to indicate origin (text | ocr | vqa).
- Extract relations only if explicitly stated in text.
- If image content is unclear or unlabeled, abstain.

## Allowed behaviors
- OCR-based entity extraction
- Caption-based relation extraction

## Disallowed behaviors
- Guessing image content
- Inferring relations from visuals alone
