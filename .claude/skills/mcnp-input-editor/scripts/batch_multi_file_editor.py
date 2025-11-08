#!/usr/bin/env python3
"""
Batch Multi-File Editor for MCNP Inputs

Applies consistent edits across multiple MCNP input files.
Common use cases:
- Update cycle-specific inputs when parameters change
- Library migration across model suite
- Fix validation errors in multiple files

Usage:
    python batch_multi_file_editor.py --files "bench_*.i" --find ".70c" --replace ".80c" --preview
    python batch_multi_file_editor.py --files "bench_*.i" --find ".70c" --replace ".80c"
    python batch_multi_file_editor.py --files "input1.i,input2.i" --find "X" --replace "Y" --regex

Author: MCNP Skills Project
Version: 3.0.0
"""

import sys
import os
import re
import glob
import argparse
from pathlib import Path


def find_files(pattern):
    """Expand file pattern to list of files

    Args:
        pattern: File pattern (glob) or comma/space-separated list

    Returns:
        List of file paths
    """
    if '*' in pattern or '?' in pattern:
        return sorted(glob.glob(pattern))
    else:
        # Comma-separated or space-separated list
        return [f.strip() for f in pattern.replace(',', ' ').split() if f.strip()]


def count_replacements(file_path, find_pattern, use_regex=False):
    """Count how many replacements would occur in a file

    Args:
        file_path: Path to file
        find_pattern: Pattern to find
        use_regex: Use regex matching

    Returns:
        Number of matches found
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}")
        return 0

    if use_regex:
        try:
            matches = re.findall(find_pattern, content)
            return len(matches)
        except re.error as e:
            print(f"⚠ Regex error: {e}")
            return 0
    else:
        return content.count(find_pattern)


def apply_replacement(file_path, find_pattern, replace_pattern, use_regex=False, backup=True):
    """Apply find/replace to a file

    Args:
        file_path: Path to file
        find_pattern: Pattern to find
        replace_pattern: Replacement string
        use_regex: Use regex matching
        backup: Create backup file

    Returns:
        Number of replacements made
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}")
        return 0

    if backup:
        backup_path = file_path + '.bak'
        try:
            with open(backup_path, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"⚠ Error creating backup {backup_path}: {e}")
            return 0

    if use_regex:
        try:
            new_content = re.sub(find_pattern, replace_pattern, content)
            count = len(re.findall(find_pattern, content))
        except re.error as e:
            print(f"⚠ Regex error: {e}")
            return 0
    else:
        new_content = content.replace(find_pattern, replace_pattern)
        count = content.count(find_pattern)

    try:
        with open(file_path, 'w') as f:
            f.write(new_content)
    except Exception as e:
        print(f"⚠ Error writing {file_path}: {e}")
        return 0

    return count


def batch_edit(files, find_pattern, replace_pattern, preview=False, use_regex=False, validate=False):
    """
    Apply batch edits to multiple files

    Args:
        files: List of file paths
        find_pattern: Pattern to find
        replace_pattern: Replacement string
        preview: If True, only show what would change
        use_regex: Use regex patterns
        validate: Validate structure after edits

    Returns:
        List of results (dicts with file and count)
    """
    total_count = 0
    results = []

    print(f"{'='*70}")
    print(f"Batch Multi-File Editor")
    print(f"{'='*70}")
    print(f"Files: {len(files)}")
    print(f"Find: {find_pattern}")
    print(f"Replace: {replace_pattern}")
    print(f"Mode: {'PREVIEW' if preview else 'APPLY'}")
    print(f"Regex: {use_regex}")
    print(f"{'='*70}\n")

    for file_path in files:
        if not os.path.exists(file_path):
            print(f"⚠ SKIP: {file_path} (not found)")
            continue

        count = count_replacements(file_path, find_pattern, use_regex)

        if count > 0:
            if not preview:
                actual_count = apply_replacement(file_path, find_pattern, replace_pattern, use_regex)
                results.append({'file': file_path, 'count': actual_count})
                print(f"✓ {file_path}: {actual_count} replacements")
            else:
                print(f"  {file_path}: {count} matches")

            total_count += count
        else:
            print(f"  {file_path}: 0 matches")

    print(f"\n{'='*70}")
    if preview:
        print(f"PREVIEW SUMMARY: {total_count} total replacements would be made")
        print(f"Run without --preview to apply changes")
    else:
        print(f"APPLIED: {total_count} total replacements across {len(results)} files")
        print(f"Backups saved as <file>.bak")

        if validate:
            print(f"\nValidating edited files...")
            # Basic validation: check blank line count
            for result in results:
                file_path = result['file']
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                    blank_count = sum(1 for line in lines if line.strip() == '')
                    if blank_count != 2:
                        print(f"⚠ WARNING: {file_path} has {blank_count} blank lines (should be 2)")
                    else:
                        print(f"✓ {file_path}: structure OK")
                except Exception as e:
                    print(f"⚠ Error validating {file_path}: {e}")
    print(f"{'='*70}")

    return results


def insert_card(files, card_text, block='surface', after_card=None):
    """Insert a card into multiple files

    Args:
        files: List of file paths
        card_text: Card to insert
        block: Block to insert into (cell, surface, data)
        after_card: Insert after this card number

    Returns:
        Number of files modified
    """
    # Implementation for inserting surfaces, cells, or data cards
    # This is a placeholder for more complex insertion logic
    print("Note: insert_card functionality not yet implemented")
    print(f"Would insert '{card_text}' into {block} block in {len(files)} files")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Batch edit multiple MCNP input files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Preview library update across all cycle inputs
  python batch_multi_file_editor.py --files "bench_*.i" --find ".70c" --replace ".80c" --preview

  # Apply library update
  python batch_multi_file_editor.py --files "bench_*.i" --find ".70c" --replace ".80c"

  # Update with validation
  python batch_multi_file_editor.py --files "bench_*.i" --find ".70c" --replace ".80c" --validate

  # Use regex to update specific materials
  python batch_multi_file_editor.py --files "*.i" --find "m90[0-9]{2}" --replace "m91XX" --regex

  # Comma-separated file list
  python batch_multi_file_editor.py --files "input1.i,input2.i,input3.i" --find "X" --replace "Y"

Best Practices:
  1. Always preview first (--preview)
  2. Use version control (git commit before editing)
  3. Validate after edits (--validate)
  4. Test run one file with MCNP before running all
        '''
    )

    parser.add_argument('--files', required=True,
                       help='File pattern (e.g., "bench_*.i") or comma-separated list')
    parser.add_argument('--find', required=True,
                       help='Pattern to find')
    parser.add_argument('--replace', required=True,
                       help='Replacement string')
    parser.add_argument('--preview', action='store_true',
                       help='Preview changes without applying')
    parser.add_argument('--regex', action='store_true',
                       help='Use regex patterns')
    parser.add_argument('--validate', action='store_true',
                       help='Validate files after editing')
    parser.add_argument('--insert-surface', dest='insert_surface',
                       help='Insert surface card into files')
    parser.add_argument('--insert-after', dest='insert_after',
                       help='Insert after specified card number')

    args = parser.parse_args()

    # Find files matching pattern
    files = find_files(args.files)

    if len(files) == 0:
        print(f"ERROR: No files found matching pattern: {args.files}")
        return 1

    print(f"Found {len(files)} file(s) matching pattern\n")

    # Handle insertion mode
    if args.insert_surface:
        insert_card(files, args.insert_surface, block='surface', after_card=args.insert_after)
        return 0

    # Apply batch edits
    results = batch_edit(
        files=files,
        find_pattern=args.find,
        replace_pattern=args.replace,
        preview=args.preview,
        use_regex=args.regex,
        validate=args.validate
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
