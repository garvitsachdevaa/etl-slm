# scripts/validate_examples.py

import json
import sys
from template_rules import TEMPLATE_RULES


def validate_example(example, line_no):
    if "template_id" not in example:
        raise ValueError(f"Line {line_no}: missing template_id")

    template_id = example["template_id"]

    if template_id not in TEMPLATE_RULES:
        raise ValueError(f"Line {line_no}: unknown template_id {template_id}")

    rules = TEMPLATE_RULES[template_id]

    entities = example.get("output", {}).get("entities", [])
    relations = example.get("output", {}).get("relations", [])

    # Rule: relations allowed or not
    if not rules.get("allow_relations", False) and relations:
        raise ValueError(
            f"Line {line_no}: relations not allowed for {template_id}"
        )

    # Rule: abstention allowed or not
    if not rules.get("allow_abstain", True) and not relations:
        raise ValueError(
            f"Line {line_no}: abstention not allowed for {template_id}"
        )

    # Rule: confidence range
    if relations:
        for rel in relations:
            conf = rel.get("confidence")
            if conf is None:
                raise ValueError(f"Line {line_no}: missing confidence")

            min_c = rules.get("min_confidence")
            max_c = rules.get("max_confidence")

            if min_c is not None and conf < min_c:
                raise ValueError(
                    f"Line {line_no}: confidence {conf} < {min_c} for {template_id}"
                )
            if max_c is not None and conf > max_c:
                raise ValueError(
                    f"Line {line_no}: confidence {conf} > {max_c} for {template_id}"
                )


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if not line.strip():
                continue
            example = json.loads(line)
            validate_example(example, i)

    print(f"Validation passed: {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_examples.py <jsonl_file>")
        sys.exit(1)

    main(sys.argv[1])
