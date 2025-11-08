#!/usr/bin/env python3
"""
Batch Material Editor for MCNP Inputs

Update multiple materials systematically while preserving numbering schemes.

Common use cases:
- Update density in material range (m9040-m9094)
- Add missing MT cards to materials
- Modify specific isotopes across materials
- Preserve systematic material numbering

Usage:
    python batch_material_editor.py input.i --materials "9040-9094" --set-density -1.85 --preview
    python batch_material_editor.py input.i --materials "9040-9094" --add-mt "grph.18t"
    python batch_material_editor.py input.i --materials "100,101,102" --set-density -2.0

Author: MCNP Skills Project
Version: 3.0.0
"""

import re
import sys
import argparse
from pathlib import Path


class MaterialEditor:
    """Edit MCNP material cards in batches"""

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.lines = []
        self.materials = {}

        if not self.file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()

        self._parse_materials()

    def _parse_materials(self):
        """Find all material cards"""
        in_data_block = False
        blank_count = 0
        current_mat = None
        mat_lines = []

        for i, line in enumerate(self.lines):
            # Detect blank lines to find data block
            if re.match(r'^\s*$', line):
                blank_count += 1
                if blank_count >= 2:
                    in_data_block = True
                # Save current material if at blank line
                if current_mat is not None:
                    self.materials[current_mat] = mat_lines
                    current_mat = None
                    mat_lines = []
                continue

            if not in_data_block:
                continue

            # Check for material card start (m followed by digits)
            match = re.match(r'^\s*m(\d+)\s', line, re.IGNORECASE)
            if match:
                # Save previous material if exists
                if current_mat is not None:
                    self.materials[current_mat] = mat_lines

                # Start new material
                current_mat = int(match.group(1))
                mat_lines = [(i, line)]

            # Check for continuation of current material
            elif current_mat is not None:
                # Continuation if starts with spaces or &
                if line.startswith('     ') or line.lstrip().startswith('&'):
                    mat_lines.append((i, line))
                # Check for MT card belonging to this material
                elif re.match(rf'^\s*mt{current_mat}\s', line, re.IGNORECASE):
                    mat_lines.append((i, line))
                # Check for next card
                elif re.match(r'^\s*[a-zA-Z]', line):
                    # Save completed material
                    self.materials[current_mat] = mat_lines
                    current_mat = None
                    mat_lines = []

        # Save last material
        if current_mat is not None:
            self.materials[current_mat] = mat_lines

    def _parse_material_range(self, mat_range):
        """Parse material range string

        Args:
            mat_range: String like "9040-9094" or "100,101,102"

        Returns:
            List of material numbers
        """
        if isinstance(mat_range, list):
            return mat_range

        mats = []

        # Split by comma
        for part in mat_range.split(','):
            part = part.strip()
            # Check for range (e.g., "9040-9094")
            if '-' in part:
                start, end = part.split('-')
                mats.extend(range(int(start), int(end) + 1))
            else:
                mats.append(int(part))

        return mats

    def set_density(self, mat_range, new_density, preview=False):
        """
        Set density for materials in range

        Args:
            mat_range: String like "9040-9094" or list [9040, 9041, ...]
            new_density: New density value (negative for g/cm³)
            preview: If True, only show changes

        Returns:
            Number of materials updated
        """
        mats = self._parse_material_range(mat_range)

        count = 0
        for mat_num in mats:
            if mat_num not in self.materials:
                continue

            mat_lines = self.materials[mat_num]
            first_line_num, first_line = mat_lines[0]

            # Parse: m<num> <density> <isotopes...>
            # Material card format: mN density ZAID1 frac1 ZAID2 frac2 ...
            parts = first_line.split()
            if len(parts) < 2:
                continue

            # Extract old density (second field after mN)
            old_density = parts[1]

            # Build new line preserving structure
            # Keep comment if exists
            if '$' in first_line:
                main_part, comment_part = first_line.split('$', 1)
                parts = main_part.split()
                parts[1] = str(new_density)
                new_line = '  '.join(parts[:3]) + '  ' + '  '.join(parts[3:]) + '  $' + comment_part
            else:
                parts[1] = str(new_density)
                # Preserve spacing: mN density isotopes...
                new_line = parts[0] + '  ' + parts[1] + '  ' + '  '.join(parts[2:]) + '\n'

            if preview:
                print(f"m{mat_num}: density {old_density} → {new_density}")
                count += 1
            else:
                self.lines[first_line_num] = new_line
                # Update in materials dict too
                mat_lines[0] = (first_line_num, new_line)
                count += 1

        if preview:
            print(f"\nPREVIEW: Would update density in {count} materials")
        else:
            print(f"Updated density in {count} materials")

        return count

    def add_mt_cards(self, mat_range, mt_library, preview=False):
        """
        Add MT (thermal scattering) cards to materials

        Args:
            mat_range: Materials to add MT cards to
            mt_library: Library string (e.g., 'grph.18t', 'lwtr.13t')
            preview: If True, only show what would be added

        Returns:
            Number of MT cards added
        """
        mats = self._parse_material_range(mat_range)

        count = 0
        additions = []  # Store (line_num, mt_line) for batch insertion

        for mat_num in mats:
            if mat_num not in self.materials:
                continue

            # Check if MT card already exists
            mat_lines = self.materials[mat_num]
            has_mt = any(re.match(rf'^\s*mt{mat_num}\s', line, re.IGNORECASE)
                        for _, line in mat_lines)

            if has_mt:
                continue  # Skip if MT already exists

            # Prepare MT card to insert
            last_line_num = mat_lines[-1][0]
            mt_line = f"mt{mat_num}  {mt_library}\n"

            if preview:
                print(f"Would add: mt{mat_num}  {mt_library}")
                count += 1
            else:
                # Store for later insertion (insert all at once to avoid index shifts)
                additions.append((last_line_num + 1, mt_line))
                count += 1

        # Apply all insertions (in reverse order to preserve line numbers)
        if not preview:
            for line_num, mt_line in reversed(additions):
                self.lines.insert(line_num, mt_line)

        if preview:
            print(f"\nPREVIEW: Would add MT cards to {count} materials")
        else:
            print(f"Added MT cards to {count} materials")

        return count

    def list_materials(self):
        """List all materials found in file"""
        if not self.materials:
            print("No materials found in file")
            return

        print(f"\nMaterials in {self.file_path}:")
        print(f"{'='*70}")

        for mat_num in sorted(self.materials.keys()):
            mat_lines = self.materials[mat_num]
            first_line = mat_lines[0][1]

            # Extract density
            parts = first_line.split()
            density = parts[1] if len(parts) > 1 else "?"

            # Check for MT card
            has_mt = any(re.match(rf'^\s*mt{mat_num}\s', line, re.IGNORECASE)
                        for _, line in mat_lines)

            # Count isotopes (approximate)
            all_text = ''.join([line for _, line in mat_lines])
            # Count ZAID patterns (NNNNN.XXc or NNNNN.XXt)
            zaids = re.findall(r'\d{4,6}\.\d{2,3}[cpt]', all_text, re.IGNORECASE)

            mt_str = "MT card" if has_mt else "no MT"
            print(f"m{mat_num}: density={density}, {len(zaids)} isotopes, {mt_str}")

    def validate_materials(self):
        """Basic validation of materials"""
        print(f"\nValidating materials...")
        issues = 0

        for mat_num in sorted(self.materials.keys()):
            mat_lines = self.materials[mat_num]
            all_text = ''.join([line for _, line in mat_lines])

            # Check for MT card presence
            has_mt = any(re.match(rf'^\s*mt{mat_num}\s', line, re.IGNORECASE)
                        for _, line in mat_lines)

            # Check for carbon (might need MT card)
            has_carbon = '6012' in all_text or '6000' in all_text

            if has_carbon and not has_mt:
                print(f"⚠ WARNING: m{mat_num} contains carbon but no MT card")
                issues += 1

        if issues == 0:
            print("✓ No issues found")
        else:
            print(f"\n{issues} potential issue(s) found")

    def save(self, output_path=None):
        """Save edited file"""
        if output_path is None:
            output_path = self.file_path

        # Create backup
        backup_path = str(self.file_path) + '.bak'
        with open(backup_path, 'w') as f:
            with open(self.file_path, 'r') as orig:
                f.write(orig.read())

        with open(output_path, 'w') as f:
            f.writelines(self.lines)

        print(f"Saved to: {output_path}")
        print(f"Backup: {backup_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Batch edit MCNP materials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # List all materials in file
  python batch_material_editor.py input.i --list

  # Preview density change
  python batch_material_editor.py input.i --materials "9040-9094" --set-density -1.85 --preview

  # Apply density change
  python batch_material_editor.py input.i --materials "9040-9094" --set-density -1.85

  # Add MT cards to graphite materials
  python batch_material_editor.py input.i --materials "9040-9094" --add-mt "grph.18t"

  # Multiple specific materials
  python batch_material_editor.py input.i --materials "100,101,102,110" --set-density -2.0

  # Validate materials
  python batch_material_editor.py input.i --validate

CRITICAL NOTES:
  - Material numbers are PRESERVED (m100 stays m100)
  - Density sign matters: negative = g/cm³, positive = atoms/barn-cm
  - MT card numbers must match material numbers (mt100 for m100)
  - Always preview before applying (--preview)
  - Backup created automatically as <file>.bak
        '''
    )

    parser.add_argument('input_file', help='MCNP input file')
    parser.add_argument('--materials',
                       help='Material range (e.g., "9040-9094" or "100,101,102")')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--set-density', type=float, help='Set density (negative for g/cm³)')
    group.add_argument('--add-mt', help='Add MT card with this library (e.g., grph.18t)')
    group.add_argument('--list', action='store_true', help='List all materials')
    group.add_argument('--validate', action='store_true', help='Validate materials')

    parser.add_argument('--preview', action='store_true', help='Preview changes only')
    parser.add_argument('--output', help='Output file (default: overwrite input)')

    args = parser.parse_args()

    try:
        editor = MaterialEditor(args.input_file)

        # List mode
        if args.list:
            editor.list_materials()
            return 0

        # Validate mode
        if args.validate:
            editor.validate_materials()
            return 0

        # Edit modes require --materials
        if not args.materials and (args.set_density or args.add_mt):
            print("ERROR: --materials required when using --set-density or --add-mt")
            return 1

        # Set density
        if args.set_density is not None:
            editor.set_density(args.materials, args.set_density, preview=args.preview)
            if not args.preview:
                editor.save(args.output)

        # Add MT cards
        elif args.add_mt:
            editor.add_mt_cards(args.materials, args.add_mt, preview=args.preview)
            if not args.preview:
                editor.save(args.output)

        # No operation
        else:
            print("No operation specified. Use --help for usage.")
            print("Tip: Use --list to see materials in file")
            return 1

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
