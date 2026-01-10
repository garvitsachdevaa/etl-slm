DOCUMENT METADATA
source_type: <text | mixed_format | image_ocr | pdf | html | csv | screenshot>
language: <iso_code or unknown>
content_quality: <clean | noisy | ocr_low_confidence | mixed>

CONTENT
[Section: <name>]
<section text>

[Section: <name>]
<section text>

<optional additional sections>

<optional tables rewritten as text>

VISUAL CONTEXT (if applicable)
<textual description derived from image / screenshot / VQA>

USER NOTES (if applicable)
<user commentary, opinions, uncertainty>

## Template Identity

Every example MUST include a `template_id`.

This field determines:
- which inference rules apply
- which relations are allowed
- how abstention is evaluated
- which expansion logic is valid

No example may omit this field.
