#!/usr/bin/env python3
"""
Enhanced validation with duplicate detection.
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Set  # ADD THIS LINE
from template_rules import TEMPLATE_RULES


class ExampleValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.seen_inputs: Set[str] = set()
        self.seen_outputs: Set[str] = set()
    
    def validate_file(self, filepath: str):
        """Validate entire file."""
        print(f"Validating {filepath}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                
                try:
                    example = json.loads(line)
                    self.validate_example(example, line_no)
                except json.JSONDecodeError as e:
                    self.errors.append(f"Line {line_no}: Invalid JSON - {e}")
                except Exception as e:
                    self.errors.append(f"Line {line_no}: {e}")
        
        self._report()
    
    def validate_example(self, example: Dict, line_no: int):
        """Validate single example."""
        # Check required fields
        if 'template_id' not in example:
            raise ValueError("missing template_id")
        
        template_id = example['template_id']
        
        if template_id not in TEMPLATE_RULES:
            raise ValueError(f"unknown template_id: {template_id}")
        
        if 'input' not in example:
            raise ValueError("missing input")
        
        if 'output' not in example:
            raise ValueError("missing output")
        
        # Validate output structure
        output = example['output']
        if 'entities' not in output:
            raise ValueError("missing entities in output")
        
        if 'relations' not in output:
            raise ValueError("missing relations in output")
        
        # Validate against template rules
        self._validate_template_rules(example, template_id, line_no)
        
        # Check for duplicates
        self._check_duplicates(example, line_no)
        
        # Validate entity-relation consistency
        self._validate_consistency(example, line_no)
    
    def _validate_template_rules(self, example: Dict, template_id: str, line_no: int):
        """Validate example follows template rules."""
        rules = TEMPLATE_RULES[template_id]
        relations = example['output']['relations']
        
        # Check if relations are allowed
        if not rules.get('allow_relations', False) and relations:
            raise ValueError(
                f"relations not allowed for {template_id}"
            )
        
        # Check abstention rules
        if not rules.get('allow_abstain', True) and not relations:
            self.warnings.append(
                f"Line {line_no}: No relations extracted (abstention) for {template_id}"
            )
        
        # Check confidence ranges
        if relations:
            for rel in relations:
                conf = rel.get('confidence')
                if conf is None:
                    raise ValueError("relation missing confidence score")
                
                min_conf = rules.get('min_confidence')
                max_conf = rules.get('max_confidence')
                
                if min_conf and conf < min_conf:
                    self.warnings.append(
                        f"Line {line_no}: confidence {conf} < {min_conf} for {template_id}"
                    )
                
                if max_conf and conf > max_conf:
                    self.warnings.append(
                        f"Line {line_no}: confidence {conf} > {max_conf} for {template_id}"
                    )
    
    def _check_duplicates(self, example: Dict, line_no: int):
        """Check for duplicate examples."""
        # Create fingerprint of input (normalized)
        input_text = example['input'].strip().lower()
        input_fingerprint = ''.join(input_text.split())
        
        if input_fingerprint in self.seen_inputs:
            self.warnings.append(
                f"Line {line_no}: Duplicate input detected"
            )
        else:
            self.seen_inputs.add(input_fingerprint)
        
        # Check output fingerprint
        output_str = json.dumps(example['output'], sort_keys=True)
        if output_str in self.seen_outputs:
            self.warnings.append(
                f"Line {line_no}: Duplicate output detected"
            )
        else:
            self.seen_outputs.add(output_str)
    
    def _validate_consistency(self, example: Dict, line_no: int):
        """Validate entity-relation consistency."""
        entities = example['output']['entities']
        relations = example['output']['relations']
        input_text = example['input']
        
        # Build entity ID set
        entity_ids = {e['id'] for e in entities}
        
        # Check relation references
        for rel in relations:
            if rel['source_id'] not in entity_ids:
                raise ValueError(f"invalid source_id: {rel['source_id']}")
            
            if rel['target_id'] not in entity_ids:
                raise ValueError(f"invalid target_id: {rel['target_id']}")
        
        # Check if entity texts appear in input
        for entity in entities:
            if entity['text'] not in input_text:
                self.warnings.append(
                    f"Line {line_no}: Entity '{entity['text']}' not found in input"
                )
    
    def _report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:20]:  # Show first 20
                print(f"  - {error}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:20]:
                print(f"  - {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more")
        
        if not self.errors and not self.warnings:
            print("\n✅ All validations passed!")
        elif not self.errors:
            print(f"\n✅ No errors, but {len(self.warnings)} warnings")
        else:
            print(f"\n❌ Validation failed with {len(self.errors)} errors")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_examples.py <jsonl_file>")
        sys.exit(1)
    
    validator = ExampleValidator()
    validator.validate_file(sys.argv[1])