# scripts/generate_examples.py

import json
import sys
from copy import deepcopy
from template_rules import TEMPLATE_RULES


DOMAINS = [
    "corporate",
    "healthcare",
    "academic"
]

def generate_variants(example):
    variants = []

    for domain in DOMAINS:
        v = deepcopy(example)
        v["domain"] = domain
        v["generated_from"] = "phase_2_domain_expansion"
        variants.append(v)

    return variants


def main(input_path, output_path):
    generated = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            example = json.loads(line)
            template_id = example.get("template_id")

            if template_id not in TEMPLATE_RULES:
                raise ValueError(f"Unknown template_id: {template_id}")

            variants = generate_variants(example)
            generated.extend(variants)

    with open(output_path, "w", encoding="utf-8") as out:
        for ex in generated:
            out.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Generated {len(generated)} examples → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_examples.py <input.jsonl> <output.jsonl>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
