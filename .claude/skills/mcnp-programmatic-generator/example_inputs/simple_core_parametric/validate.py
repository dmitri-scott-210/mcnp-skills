"""
Validation script for Simple Core model
"""

import input_definition as indef


def extract_cell_numbers(filename):
    """Extract all cell numbers from MCNP input"""
    cell_nums = []
    in_cells = False

    try:
        with open(filename) as f:
            for line in f:
                stripped = line.strip()

                # Detect cell block
                if 'c Cells' in stripped or 'c cells' in stripped:
                    in_cells = True
                    continue

                # Detect surface block (end of cells)
                if 'c Surfaces' in stripped or 'c surfaces' in stripped:
                    in_cells = False

                if in_cells and stripped and not stripped.startswith('c'):
                    parts = stripped.split()
                    if parts:
                        try:
                            cell_nums.append(int(parts[0]))
                        except ValueError:
                            pass

        return cell_nums
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        print("Run 'python generate_model.py' first")
        return []


def check_numbering_conflicts(filename):
    """Check for duplicate cell numbers"""
    cell_nums = extract_cell_numbers(filename)

    if not cell_nums:
        return False

    duplicates = [n for n in cell_nums if cell_nums.count(n) > 1]

    if duplicates:
        print(f"❌ {filename}: CONFLICTS found: {set(duplicates)}")
        return False
    else:
        print(f"✓ {filename}: No conflicts ({len(cell_nums)} unique cells)")
        return True


def validate_enrichments():
    """Check enrichments are in valid range"""
    errors = []

    # Check specific enrichments
    for asse_num, enrich in indef.fuel_enrichments.items():
        if not 0.0 < enrich < 20.0:
            errors.append(f"Assembly {asse_num}: enrichment {enrich}% out of range")

    # Check default enrichment
    if not 0.0 < indef.default_enrichment < 20.0:
        errors.append(f"Default enrichment {indef.default_enrichment}% out of range")

    if errors:
        print("❌ Enrichment errors:")
        for e in errors:
            print(f"   {e}")
        return False
    else:
        print("✓ All enrichments valid")
        return True


def validate_control_positions():
    """Check control positions are valid"""
    errors = []
    valid_positions = ['withdrawn', 'inserted']

    for (layer, asse), position in indef.control_positions.items():
        # Check if position is valid string or valid number
        if isinstance(position, str):
            if position not in valid_positions:
                errors.append(f"Control {layer}-{asse}: invalid position '{position}'")
        else:
            try:
                pos_float = float(position)
                if not 0.0 <= pos_float <= 100.0:
                    errors.append(f"Control {layer}-{asse}: position {position} out of range (0-100)")
            except ValueError:
                errors.append(f"Control {layer}-{asse}: invalid position '{position}'")

    if errors:
        print("❌ Control position errors:")
        for e in errors:
            print(f"   {e}")
        return False
    else:
        print(f"✓ All control positions valid ({len(indef.control_positions)} controls)")
        return True


def count_assembly_types():
    """Count fuel and control assemblies"""
    fuel_count = 0
    control_count = 0

    for layer, asse_list in indef.assemblies.items():
        for asse in asse_list:
            if '_C' in asse:
                control_count += 1
            else:
                fuel_count += 1

    print(f"\nAssembly counts:")
    print(f"  Fuel: {fuel_count}")
    print(f"  Control: {control_count}")
    print(f"  Total: {fuel_count + control_count}")

    return fuel_count, control_count


def validate_assembly_consistency():
    """Verify control assemblies have positions defined"""
    errors = []

    for layer, asse_list in indef.assemblies.items():
        for asse in asse_list:
            if '_C' in asse:
                key = (str(layer), asse)
                if key not in indef.control_positions:
                    errors.append(f"Control {layer}-{asse}: no position defined (will use default 'withdrawn')")

    if errors:
        print("⚠ Control position warnings:")
        for e in errors:
            print(f"   {e}")
        return False
    else:
        print("✓ All control assemblies have positions defined")
        return True


# Run validations
def main():
    print("=" * 60)
    print("Model Validation")
    print("=" * 60)

    print("\n1. Checking numbering conflicts...")
    numbering_ok = check_numbering_conflicts('simple_core.i')

    print("\n2. Validating parameters...")
    enrichment_ok = validate_enrichments()
    control_ok = validate_control_positions()

    print("\n3. Assembly analysis...")
    count_assembly_types()
    consistency_ok = validate_assembly_consistency()

    print("\n" + "=" * 60)
    if numbering_ok and enrichment_ok and control_ok:
        print("Validation complete: ✓ PASS")
    else:
        print("Validation complete: ❌ ISSUES FOUND")
    print("=" * 60)


if __name__ == "__main__":
    main()
