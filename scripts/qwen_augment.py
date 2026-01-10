#!/usr/bin/env python3
"""
Use Qwen 2.5 to augment training examples through linguistic variation.
Qwen rewrites INPUT text only. Output labels remain unchanged.
"""

import json
import sys
import random
from pathlib import Path
from typing import Dict, List
from copy import deepcopy

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class QwenAugmenter:
    """Uses Qwen to create linguistic variations of training examples."""
    
    def __init__(self, model_name: str = "Qwen/Qwen2.5-3B-Instruct"):
        """
        Initialize Qwen model for text augmentation.
        
        Args:
            model_name: Hugging Face model ID
        """
        print(f"Loading {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        print("✅ Model loaded")
    
    def augment_example(
        self, 
        example: Dict, 
        augmentation_type: str,
        variant_num: int
    ) -> Dict:
        """
        Create augmented variant of an example.
        
        Args:
            example: Original example
            augmentation_type: Type of augmentation (paraphrase, noise, etc.)
            variant_num: Unique variant number
        
        Returns:
            Augmented example with rewritten input, same output
        """
        # Extract content section from canonical input
        original_input = example['input']
        content_section = self._extract_content(original_input)
        
        # Generate augmentation based on type
        if augmentation_type == "paraphrase":
            augmented_content = self._paraphrase(content_section)
        elif augmentation_type == "noise":
            augmented_content = self._add_noise(content_section)
        elif augmentation_type == "formal":
            augmented_content = self._make_formal(content_section)
        elif augmentation_type == "informal":
            augmented_content = self._make_informal(content_section)
        else:
            raise ValueError(f"Unknown augmentation type: {augmentation_type}")
        
        # Reconstruct full input with metadata
        new_input = self._reconstruct_input(
            original_input,
            augmented_content
        )
        
        # Create new example
        new_example = deepcopy(example)
        new_example['input'] = new_input
        # Keep output unchanged!
        new_example['augmentation_type'] = augmentation_type
        new_example['augmentation_variant'] = variant_num
        
        return new_example
    
    def _extract_content(self, canonical_input: str) -> str:
        """Extract content section from canonical input format."""
        # Find CONTENT section
        content_match = canonical_input.split("CONTENT\n", 1)
        if len(content_match) < 2:
            return canonical_input
        
        content = content_match[1]
        
        # Remove section headers if present
        lines = content.split('\n')
        clean_lines = []
        for line in lines:
            if line.startswith('[Section:') or line.startswith('['):
                continue
            clean_lines.append(line)
        
        return '\n'.join(clean_lines).strip()
    
    def _paraphrase(self, text: str) -> str:
        """Paraphrase text while keeping meaning."""
        prompt = f"""Rewrite the following text in different words while keeping the exact same meaning and entities. Do not add or remove any information. Do not add explanations.

Original text:
{text}

Rewritten text:"""
        
        return self._generate(prompt, max_new_tokens=200)
    
    def _add_noise(self, text: str) -> str:
        """Add realistic noise (typos, informal language)."""
        prompt = f"""Rewrite the following text with minor realistic imperfections like:
- 1-2 small typos
- Slightly informal phrasing
- Minor grammatical variations

Keep all entity names and facts unchanged.

Original text:
{text}

Noisy version:"""
        
        return self._generate(prompt, max_new_tokens=200)
    
    def _make_formal(self, text: str) -> str:
        """Make text more formal."""
        prompt = f"""Rewrite the following text in a more formal, professional style. Keep all facts and entities unchanged.

Original text:
{text}

Formal version:"""
        
        return self._generate(prompt, max_new_tokens=200)
    
    def _make_informal(self, text: str) -> str:
        """Make text more informal."""
        prompt = f"""Rewrite the following text in a more casual, conversational style. Keep all facts and entities unchanged.

Original text:
{text}

Casual version:"""
        
        return self._generate(prompt, max_new_tokens=200)
    
    def _generate(self, prompt: str, max_new_tokens: int = 200) -> str:
        """Generate text using Qwen."""
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
        
        generated = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )
        
        return generated.strip()
    
    def _reconstruct_input(self, original_input: str, new_content: str) -> str:
        """Reconstruct canonical input with new content."""
        # Split into metadata and content
        parts = original_input.split("CONTENT\n", 1)
        if len(parts) < 2:
            return new_content
        
        metadata = parts[0] + "CONTENT\n"
        
        # Extract section header if present
        old_content = parts[1]
        section_header = ""
        if old_content.startswith('[Section:'):
            lines = old_content.split('\n', 1)
            section_header = lines[0] + '\n'
        
        return metadata + section_header + new_content


def augment_dataset(
    input_file: str,
    output_file: str,
    num_augmentations: int = 2,
    augmentation_types: List[str] = None
):
    """
    Augment entire dataset using Qwen.
    
    Args:
        input_file: Path to input JSONL
        output_file: Path to output augmented JSONL
        num_augmentations: Number of augmented variants per example
        augmentation_types: List of augmentation types to apply
    """
    if augmentation_types is None:
        augmentation_types = ["paraphrase", "noise"]
    
    print(f"Augmenting {input_file}...")
    print(f"  Augmentation types: {augmentation_types}")
    print(f"  Variants per example: {num_augmentations}")
    
    # Load model
    augmenter = QwenAugmenter()
    
    # Load examples
    examples = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))
    
    print(f"  Loaded {len(examples)} examples")
    
    # Sample examples for augmentation (don't augment all 2000+)
    # Augment ~20% of examples to add variety without explosion
    sample_size = max(20, len(examples) // 5)
    sampled_examples = random.sample(examples, min(sample_size, len(examples)))
    
    print(f"  Augmenting {len(sampled_examples)} examples...")
    
    # Generate augmentations
    augmented = []
    for idx, example in enumerate(sampled_examples, 1):
        print(f"  [{idx}/{len(sampled_examples)}] Augmenting...")
        
        for variant_num in range(num_augmentations):
            aug_type = random.choice(augmentation_types)
            
            try:
                augmented_example = augmenter.augment_example(
                    example,
                    aug_type,
                    variant_num
                )
                augmented.append(augmented_example)
                print(f"    ✓ Created {aug_type} variant {variant_num + 1}")
            except Exception as e:
                print(f"    ✗ Failed to create variant: {e}")
                continue
    
    # Save: original + augmented
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write original examples
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        # Write augmented examples
        for example in augmented:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    total = len(examples) + len(augmented)
    print(f"\n✅ Augmentation complete!")
    print(f"   Original: {len(examples)}")
    print(f"   Augmented: {len(augmented)}")
    print(f"   Total: {total}")
    print(f"   Saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/qwen_augment.py <input.jsonl> <output.jsonl> [num_variants]")
        print("\nExample:")
        print("  python3 scripts/qwen_augment.py data/train/template_01.jsonl data/train/augmented/template_01_aug.jsonl 2")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    num_variants = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    augment_dataset(input_file, output_file, num_variants)