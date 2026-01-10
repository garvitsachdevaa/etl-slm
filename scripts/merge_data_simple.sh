#!/bin/bash
# Merge Phase 1 + Phase 2 data for training

set -e

echo "📦 Merging training data (Phase 1 + 2 only)..."

OUTPUT_DIR="data/train/final"
mkdir -p "$OUTPUT_DIR"

# Combine all template files (already contain Phase 1 + Phase 2)
cat data/train/template_*.jsonl > "$OUTPUT_DIR/all_data.jsonl"

# Shuffle
shuf "$OUTPUT_DIR/all_data.jsonl" > "$OUTPUT_DIR/shuffled.jsonl"

# 90/10 train/val split
total=$(wc -l < "$OUTPUT_DIR/shuffled.jsonl")
train_size=$((total * 9 / 10))

head -n "$train_size" "$OUTPUT_DIR/shuffled.jsonl" > "$OUTPUT_DIR/train.jsonl"
tail -n +$((train_size + 1)) "$OUTPUT_DIR/shuffled.jsonl" > "$OUTPUT_DIR/val.jsonl"

# Clean up temp files
rm "$OUTPUT_DIR/all_data.jsonl" "$OUTPUT_DIR/shuffled.jsonl"

echo "✅ Training data ready!"
echo ""
echo "📊 Statistics:"
echo "  Total: $total examples"
echo "  Train: $(wc -l < $OUTPUT_DIR/train.jsonl) examples"
echo "  Val: $(wc -l < $OUTPUT_DIR/val.jsonl) examples"
echo ""
echo "📁 Files created:"
echo "  $OUTPUT_DIR/train.jsonl"
echo "  $OUTPUT_DIR/val.jsonl"
