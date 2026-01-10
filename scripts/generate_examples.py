#!/usr/bin/env python3
"""
Programmatic expansion that actually creates DIFFERENT examples.
Substitutes entities, relations, and formats based on domain mappings.
"""

import json
import yaml
import random
import re
import sys
from pathlib import Path
from copy import deepcopy
from typing import Dict, List, Any
from template_rules import TEMPLATE_RULES


class ExampleExpander:
    """Expands seed examples into domain-specific variants."""
    
    def __init__(self, domain_mappings_path: str = "data/expansion/domain_mappings.yaml"):
        with open(domain_mappings_path, 'r') as f:
            config = yaml.safe_load(f)
            self.domains = config['domains']
        
        # Track used entity pairs to avoid duplicates
        self.used_pairs = set()
    
    def expand_example(self, seed_example: Dict, target_domain: str, variant_id: int) -> Dict:
        """
        Create a new example by substituting entities and relations.
        
        Args:
            seed_example: Original example
            target_domain: Target domain (healthcare, academic, etc.)
            variant_id: Unique ID for this variant
        
        Returns:
            New example with substituted content
        """
        if target_domain not in self.domains:
            raise ValueError(f"Unknown domain: {target_domain}")
        
        domain_config = self.domains[target_domain]
        new_example = deepcopy(seed_example)
        
        # Get template rules
        template_id = seed_example['template_id']
        template_rules = TEMPLATE_RULES[template_id]
        
        # Extract original entities
        original_entities = seed_example['output']['entities']
        original_relations = seed_example['output']['relations']
        
        # Create entity mapping (old name -> new name)
        entity_mapping = self._create_entity_mapping(
            original_entities,
            domain_config,
            variant_id
        )
        
        # Substitute in input text
        new_input = self._substitute_input_text(
            seed_example['input'],
            entity_mapping,
            domain_config,
            original_relations
        )
        
        # Substitute in output
        new_output = self._substitute_output(
            seed_example['output'],
            entity_mapping,
            domain_config,
            new_input
        )
        
        # Update example
        new_example['input'] = new_input
        new_example['output'] = new_output
        new_example['variant_id'] = f"{template_id}_dom{target_domain}_v{variant_id}"
        new_example['source_template'] = template_id
        new_example['expansion_domain'] = target_domain
        
        return new_example
    
    def _create_entity_mapping(
        self,
        original_entities: List[Dict],
        domain_config: Dict,
        variant_id: int
    ) -> Dict[str, str]:
        """Create mapping from original entity names to new domain-specific names."""
        mapping = {}
        
        # Group entities by type
        entities_by_type = {}
        for entity in original_entities:
            etype = entity['type']
            if etype not in entities_by_type:
                entities_by_type[etype] = []
            entities_by_type[etype].append(entity['text'])
        
        # Select random entities from domain's entity pool
        for etype, entity_texts in entities_by_type.items():
            if etype == "Company" or etype in domain_config['entity_types']:
                # Get available entities for this domain
                available_entities = domain_config['entity_examples']
                
                # Flatten if nested
                flat_entities = []
                for group in available_entities:
                    flat_entities.extend(group)
                
                # Ensure we have enough unique entities
                if len(entity_texts) > len(flat_entities):
                    # Cycle through if needed
                    selected = []
                    for i, old_text in enumerate(entity_texts):
                        selected.append(flat_entities[i % len(flat_entities)])
                else:
                    # Sample without replacement
                    selected = random.sample(flat_entities, len(entity_texts))
                
                # Create mapping
                for old_text, new_text in zip(entity_texts, selected):
                    mapping[old_text] = new_text
            
            elif etype == "Person":
                # Keep person names or generate generic ones
                for old_text in entity_texts:
                    # For now, keep person names unchanged or generate
                    # You can extend this to have person name pools per domain
                    mapping[old_text] = old_text
        
        return mapping
    
    def _substitute_input_text(
        self,
        original_input: str,
        entity_mapping: Dict[str, str],
        domain_config: Dict,
        original_relations: List[Dict]
    ) -> str:
        """Substitute entities and relations in input text."""
        new_input = original_input
        
        # Substitute entities (longest first to avoid partial matches)
        sorted_entities = sorted(entity_mapping.items(), key=lambda x: len(x[0]), reverse=True)
        for old_name, new_name in sorted_entities:
            new_input = re.sub(
                rf'\b{re.escape(old_name)}\b',
                new_name,
                new_input
            )
        
        # Substitute relation types if present
        if original_relations:
            for relation in original_relations:
                old_relation = relation['relation_type']
                
                # Get domain-specific relation variants
                if old_relation in domain_config['relations']:
                    new_relation = random.choice(domain_config['relations'][old_relation])
                    new_input = re.sub(
                        rf'\b{re.escape(old_relation)}\b',
                        new_relation,
                        new_input,
                        count=1  # Only replace first occurrence
                    )
        
        # Update entity type mentions (Company -> Hospital, etc.)
        for old_type, new_types in domain_config['entity_types'].items():
            if old_type in new_input:
                new_type = random.choice(new_types)
                new_input = re.sub(
                    rf'\b{old_type}\b',
                    new_type,
                    new_input
                )
        
        return new_input
    
    def _substitute_output(
        self,
        original_output: Dict,
        entity_mapping: Dict[str, str],
        domain_config: Dict,
        new_input: str
    ) -> Dict:
        """Substitute entities and relations in output JSON."""
        new_output = deepcopy(original_output)
        
        # Substitute entity texts and types
        for entity in new_output['entities']:
            old_text = entity['text']
            if old_text in entity_mapping:
                entity['text'] = entity_mapping[old_text]
            
            # Update entity type to domain-specific type
            old_type = entity['type']
            if old_type in domain_config['entity_types']:
                entity['type'] = random.choice(domain_config['entity_types'][old_type])
        
        # Substitute in relations
        for relation in new_output['relations']:
            # Update relation type
            old_relation_type = relation['relation_type']
            if old_relation_type in domain_config['relations']:
                relation['relation_type'] = random.choice(
                    domain_config['relations'][old_relation_type]
                )
            
            # Update evidence text
            old_evidence = relation['evidence']
            new_evidence = old_evidence
            
            # Substitute entity names in evidence
            for old_name, new_name in entity_mapping.items():
                new_evidence = re.sub(
                    rf'\b{re.escape(old_name)}\b',
                    new_name,
                    new_evidence
                )
            
            # Substitute relation type in evidence
            if old_relation_type in new_evidence:
                new_rel = relation['relation_type']  # Already updated above
                new_evidence = re.sub(
                    rf'\b{re.escape(old_relation_type)}\b',
                    new_rel,
                    new_evidence,
                    count=1
                )
            
            relation['evidence'] = new_evidence
        
        return new_output


def generate_variants(
    seed_example: Dict,
    expander: ExampleExpander,
    num_variants_per_domain: int = 5
) -> List[Dict]:
    """
    Generate multiple variants of a seed example across domains.
    
    Args:
        seed_example: Original example
        expander: ExampleExpander instance
        num_variants_per_domain: Number of variants per domain
    
    Returns:
        List of variant examples
    """
    variants = []
    
    # Get template ID to determine which domains are appropriate
    template_id = seed_example['template_id']
    
    # Domains to expand into (skip corporate as that's already covered)
    target_domains = ["healthcare", "academic", "government", "finance"]
    
    # Determine if this template should have domain expansion
    # Templates about abstention, conflicting info, etc. should still expand
    # but with domain-appropriate entities
    
    for domain in target_domains:
        for variant_num in range(num_variants_per_domain):
            try:
                variant = expander.expand_example(
                    seed_example,
                    domain,
                    variant_num
                )
                variants.append(variant)
            except Exception as e:
                print(f"Warning: Failed to generate variant {variant_num} for domain {domain}: {e}")
                continue
    
    return variants


def main(template_file: str, output_file: str, num_variants: int = 5):
    """
    Generate expanded dataset from template file.
    
    Args:
        template_file: Path to template JSONL file (e.g., template_01.jsonl)
        output_file: Path to output expanded JSONL file
        num_variants: Number of variants per domain
    """
    print(f"Expanding {template_file}...")
    
    # Load expander
    expander = ExampleExpander()
    
    # Load seed examples
    seed_examples = []
    with open(template_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                seed_examples.append(json.loads(line))
    
    print(f"Loaded {len(seed_examples)} seed examples")
    
    # Generate variants
    all_variants = []
    for seed_example in seed_examples:
        variants = generate_variants(seed_example, expander, num_variants)
        all_variants.extend(variants)
        print(f"  Generated {len(variants)} variants for seed example")
    
    # Save expanded dataset
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write seed examples first
        for seed in seed_examples:
            f.write(json.dumps(seed, ensure_ascii=False) + '\n')
        
        # Write variants
        for variant in all_variants:
            f.write(json.dumps(variant, ensure_ascii=False) + '\n')
    
    total = len(seed_examples) + len(all_variants)
    print(f"\n✅ Expansion complete!")
    print(f"   Seed examples: {len(seed_examples)}")
    print(f"   Generated variants: {len(all_variants)}")
    print(f"   Total examples: {total}")
    print(f"   Saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/generate_examples.py <input_template.jsonl> <output.jsonl> [num_variants]")
        print("\nExample:")
        print("  python scripts/generate_examples.py data/train/template_01.jsonl data/train/expanded/template_01_expanded.jsonl 5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    num_variants = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    main(input_file, output_file, num_variants)