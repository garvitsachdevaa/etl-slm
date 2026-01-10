#!/bin/bash
# Expand all template files and append variants to original files

set -e

echo "🚀 Starting programmatic expansion for all templates..."
echo ""
echo "⚠️  WARNING: This will modify template files in place!"
echo "Creating backups first..."
echo ""

# Create backup directory
BACKUP_DIR="data/train/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Number of variants per domain
VARIANTS=5

# Backup and expand each template
for template in data/train/template_*.jsonl; do
    template_name=$(basename "$template")
    
    # Create backup
    echo "📦 Backing up $template_name to $BACKUP_DIR/"
    cp "$template" "$BACKUP_DIR/"
    
    # Generate expanded examples to temporary file
    temp_file="data/train/.temp_${template_name}"
    
    echo "🔄 Expanding $template_name..."
    python3 scripts/generate_examples.py "$template" "$temp_file" "$VARIANTS"  # Changed to python3
    
    # Replace original with expanded
    mv "$temp_file" "$template"
    
    echo "✅ Updated $template with expanded examples"
    echo ""
done

echo "========================================="
echo "✅ All templates expanded and updated!"
echo ""
echo "📊 Summary:"
wc -l data/train/template_*.jsonl
echo ""
echo "💾 Backups saved in: $BACKUP_DIR/"