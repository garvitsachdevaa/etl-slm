# Template 04 — Mixed & Messy Inputs

## Purpose
Train the model to extract entities and relationships correctly from
poorly formatted, noisy, or mixed-structure inputs.

## Input Characteristics
- HTML tags
- Bullet points
- Headings and fragments
- Inconsistent grammar
- Embedded metadata

## Rules
- Ignore formatting noise.
- Extract entities based on semantic content only.
- Apply the same inference and abstention rules as previous templates.
- Do not treat HTML tags or formatting as entities.
- Evidence must come from meaningful text, not markup.

## Allowed behaviors
- Robust extraction despite noise
- Abstention when content is ambiguous

## Disallowed behaviors
- Extracting tags as entities
- Inferring relations from layout alone
