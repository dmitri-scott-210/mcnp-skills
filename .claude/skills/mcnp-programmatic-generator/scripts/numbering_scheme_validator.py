"""
Numbering Scheme Validator
Validates MCNP numbering schemes for conflicts and consistency
"""

def extract_card_numbers(filename):
    """
    Extract all cell, surface, and material numbers from MCNP input

    Returns:
        dict with 'cells', 'surfaces', 'materials' lists
    """
    cell_nums = []
    surf_nums = []
    mat_nums = []

    in_cells = False
    in_surfaces = False
    in_materials = False

    with open(filename) as f:
        for line in f:
            stripped = line.strip()

            # Detect blocks
            if 'c Cells' in stripped or 'c cells' in stripped.lower():
                in_cells = True
                in_surfaces = False
                in_materials = False
                continue

            if 'c Surfaces' in stripped or 'c surfaces' in stripped.lower():
                in_cells = False
                in_surfaces = True
                in_materials = False
                continue

            if 'c Materials' in stripped or 'c materials' in stripped.lower():
                in_cells = False
                in_surfaces = False
                in_materials = True
                continue

            if 'c Physics' in stripped or 'c physics' in stripped.lower():
                break  # End of material block

            # Extract numbers
            if stripped and not stripped.startswith('c'):
                parts = stripped.split()
                if parts:
                    try:
                        if in_cells:
                            cell_nums.append(int(parts[0]))
                        elif in_surfaces:
                            # Surface numbers can have * prefix
                            surf_num = parts[0].replace('*', '')
                            surf_nums.append(int(surf_num))
                        elif in_materials and parts[0].startswith('m'):
                            # Material cards start with 'm'
                            mat_num = parts[0][1:]  # Remove 'm'
                            mat_nums.append(int(mat_num))
                    except ValueError:
                        pass

    return {
        'cells': cell_nums,
        'surfaces': surf_nums,
        'materials': mat_nums
    }


def check_duplicates(numbers, card_type):
    """
    Check for duplicate numbers

    Args:
        numbers: List of card numbers
        card_type: 'Cell', 'Surface', or 'Material'

    Returns:
        (has_duplicates, duplicate_list)
    """
    duplicates = [n for n in set(numbers) if numbers.count(n) > 1]

    if duplicates:
        print(f"  ❌ {card_type} CONFLICTS: {sorted(duplicates)}")
        return True, duplicates
    else:
        print(f"  ✓ {card_type}s: {len(numbers)} unique")
        return False, []


def analyze_numbering_scheme(numbers, card_type):
    """
    Analyze numbering scheme statistics

    Args:
        numbers: List of card numbers
        card_type: 'Cell', 'Surface', or 'Material'
    """
    if not numbers:
        print(f"  No {card_type.lower()}s found")
        return

    min_num = min(numbers)
    max_num = max(numbers)
    total = len(numbers)
    span = max_num - min_num + 1
    density = (total / span) * 100 if span > 0 else 0

    print(f"\n  {card_type} Statistics:")
    print(f"    Range: {min_num} - {max_num}")
    print(f"    Total: {total}")
    print(f"    Span: {span}")
    print(f"    Density: {density:.1f}%")

    # Detect gaps
    all_nums = set(range(min_num, max_num + 1))
    used_nums = set(numbers)
    gaps = sorted(all_nums - used_nums)

    if gaps and len(gaps) < 20:  # Only show if reasonable number
        print(f"    Gaps: {gaps[:10]}{'...' if len(gaps) > 10 else ''}")


def decode_numbering_scheme(cell_id):
    """
    Attempt to decode cell ID structure

    Args:
        cell_id: MCNP cell number

    Returns:
        Decoded information as string
    """
    cell_str = str(cell_id)
    length = len(cell_str)

    if length == 5:
        # Could be: LNNCC (layer, number, component)
        layer = int(cell_str[0]) - 1
        number = int(cell_str[1:3])
        component = int(cell_str[3:])
        return f"Layer {layer}, Assy {number:02d}, Comp {component:02d}"

    elif length == 6:
        # Could be: LANNCC (layer, type, number, component)
        layer = int(cell_str[0]) - 1
        assy_type = int(cell_str[1])
        number = int(cell_str[2:4])
        component = int(cell_str[4:])
        return f"Layer {layer}, Type {assy_type}, Assy {number:02d}, Comp {component:02d}"

    elif length == 7:
        # Could be: LSSCCPP (layer, stack, compact, particle)
        layer = int(cell_str[0]) - 1
        stack = int(cell_str[1:3])
        compact = int(cell_str[3:5])
        particle = int(cell_str[5:])
        return f"Layer {layer}, Stack {stack:02d}, Compact {compact:02d}, Part {particle:02d}"

    else:
        return "Unknown scheme"


def validate_cross_references(filename):
    """
    Validate that cell references to surfaces and materials exist

    Args:
        filename: MCNP input file
    """
    print("\nValidating cross-references...")

    cards = extract_card_numbers(filename)
    cell_nums = set(cards['cells'])
    surf_nums = set(cards['surfaces'])
    mat_nums = set(cards['materials'])

    # Parse cell cards to find surface and material references
    referenced_surfs = set()
    referenced_mats = set()

    with open(filename) as f:
        in_cells = False
        for line in f:
            stripped = line.strip()

            if 'c Cells' in stripped:
                in_cells = True
                continue
            if 'c Surfaces' in stripped:
                in_cells = False
                break

            if in_cells and stripped and not stripped.startswith('c'):
                parts = stripped.split()
                if len(parts) >= 3:
                    # Material ID (can be 0 for void)
                    try:
                        mat_id = int(parts[1])
                        if mat_id != 0:
                            referenced_mats.add(mat_id)
                    except ValueError:
                        pass

                    # Surface IDs (in geometry specification)
                    for part in parts[3:]:
                        # Remove operators and extract surface number
                        surf_str = part.replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace(':', '')
                        try:
                            if surf_str:
                                referenced_surfs.add(int(surf_str))
                        except ValueError:
                            pass

    # Find missing references
    missing_surfs = referenced_surfs - surf_nums
    missing_mats = referenced_mats - mat_nums

    if missing_surfs:
        print(f"  ❌ Missing surfaces: {sorted(missing_surfs)}")
    else:
        print(f"  ✓ All referenced surfaces exist ({len(referenced_surfs)} refs)")

    if missing_mats:
        print(f"  ❌ Missing materials: {sorted(missing_mats)}")
    else:
        print(f"  ✓ All referenced materials exist ({len(referenced_mats)} refs)")

    # Find unused definitions
    unused_surfs = surf_nums - referenced_surfs
    unused_mats = mat_nums - referenced_mats

    if unused_surfs:
        print(f"  ⚠ Unused surfaces: {len(unused_surfs)} surfaces defined but not used")

    if unused_mats:
        print(f"  ⚠ Unused materials: {len(unused_mats)} materials defined but not used")


def generate_numbering_report(filename):
    """
    Generate comprehensive numbering report

    Args:
        filename: MCNP input file
    """
    print("=" * 70)
    print(f"Numbering Scheme Validation: {filename}")
    print("=" * 70)

    # Extract all numbers
    cards = extract_card_numbers(filename)

    # Check for duplicates
    print("\n1. Checking for numbering conflicts...")
    has_cell_dups, _ = check_duplicates(cards['cells'], 'Cell')
    has_surf_dups, _ = check_duplicates(cards['surfaces'], 'Surface')
    has_mat_dups, _ = check_duplicates(cards['materials'], 'Material')

    if has_cell_dups or has_surf_dups or has_mat_dups:
        print("\n  ❌ CONFLICTS DETECTED - Model will not run correctly!")
    else:
        print("\n  ✓ No numbering conflicts detected")

    # Analyze schemes
    print("\n2. Numbering scheme analysis...")
    analyze_numbering_scheme(cards['cells'], 'Cell')
    analyze_numbering_scheme(cards['surfaces'], 'Surface')
    analyze_numbering_scheme(cards['materials'], 'Material')

    # Sample decoding
    if cards['cells']:
        print("\n3. Decoding sample cell IDs...")
        sample_cells = sorted(cards['cells'])[:5]  # First 5 cells
        for cell_id in sample_cells:
            decoded = decode_numbering_scheme(cell_id)
            print(f"    {cell_id}: {decoded}")

    # Cross-reference validation
    print("\n4. Cross-reference validation...")
    validate_cross_references(filename)

    print("\n" + "=" * 70)
    print("Validation complete")
    print("=" * 70)


def compare_numbering_schemes(file1, file2):
    """
    Compare numbering schemes between two files

    Args:
        file1, file2: MCNP input files
    """
    print("=" * 70)
    print(f"Comparing: {file1} vs {file2}")
    print("=" * 70)

    cards1 = extract_card_numbers(file1)
    cards2 = extract_card_numbers(file2)

    # Compare cells
    cells1 = set(cards1['cells'])
    cells2 = set(cards2['cells'])

    common_cells = cells1 & cells2
    only_in_1 = cells1 - cells2
    only_in_2 = cells2 - cells1

    print(f"\nCell comparison:")
    print(f"  {file1}: {len(cells1)} cells")
    print(f"  {file2}: {len(cells2)} cells")
    print(f"  Common: {len(common_cells)}")
    print(f"  Only in {file1}: {len(only_in_1)}")
    print(f"  Only in {file2}: {len(only_in_2)}")

    if common_cells:
        print(f"\n  Sample common cells: {sorted(common_cells)[:10]}")

    if only_in_1:
        print(f"  Sample unique to {file1}: {sorted(only_in_1)[:10]}")

    if only_in_2:
        print(f"  Sample unique to {file2}: {sorted(only_in_2)[:10]}")

    print("\n" + "=" * 70)


# Command-line interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Validate single file:")
        print("    python numbering_scheme_validator.py <input_file>")
        print()
        print("  Compare two files:")
        print("    python numbering_scheme_validator.py <file1> <file2>")
        sys.exit(1)

    if len(sys.argv) == 2:
        # Validate single file
        generate_numbering_report(sys.argv[1])
    else:
        # Compare two files
        compare_numbering_schemes(sys.argv[1], sys.argv[2])
