# Template 06 — Table-like & CSV Inputs

## Purpose
Train the model to extract entities, roles, and attributes from
table-like, CSV-like, or column-based text inputs.

## Input Characteristics
- Headers and rows
- Delimiters like | , ;
- Inconsistent spacing
- Missing cells

## Rules
- Use headers to infer attribute meaning.
- Extract entities row by row.
- Store role/title data in entity `properties`.
- Do NOT infer relationships unless explicitly stated.
- Do not assume ownership from table structure alone.

## Allowed behaviors
- Multiple entities from one table
- Attribute extraction via headers

## Disallowed behaviors
- Inferring relations from proximity
- Treating headers as entities
