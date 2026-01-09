# Template 05 — Roles, Attributes & Properties

## Purpose
Train the model to extract people and their roles or attributes
using entity properties instead of relationships.

## Rules
- Extract people as entities when clearly mentioned.
- Store roles, titles, or attributes inside the entity's `properties`.
- Do NOT convert roles into relationships unless explicitly relational.
- Continue applying abstention rules from earlier templates.
- Confidence should reflect clarity of role mention.

## Examples of properties
- role
- title
- position
- occupation
- founding_year

## Allowed behaviors
- Entity properties enrichment
- Multiple entities with different types

## Disallowed behaviors
- Creating relations for roles (e.g., CEO_of)
- Inferring roles without explicit textual support
