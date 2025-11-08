#!/usr/bin/env python3
"""
MCNP Lattice Dimension Calculator

Validates FILL array dimensions for both LAT=1 (rectangular) and LAT=2 (hexagonal) lattices.
Prevents the most common MCNP fatal errors: dimension mismatches in FILL arrays.

Based on analysis from AGENT8_FILL_ARRAY_DEEP_DIVE.md

Usage:
    python lattice_dimension_calculator.py

Or import as module:
    from lattice_dimension_calculator import calculate_fill_dimensions, validate_lattice
"""

import math
from typing import Dict, List, Tuple, Optional


def calculate_fill_dimensions(imin: int, imax: int,
                              jmin: int, jmax: int,
                              kmin: int, kmax: int) -> Dict:
    """
    Calculate the number of elements needed for a FILL array.

    Critical formula: (IMAX-IMIN+1) × (JMAX-JMIN+1) × (KMAX-KMIN+1)

    Works for BOTH LAT=1 (rectangular) and LAT=2 (hexagonal) lattices.

    Args:
        imin, imax: I-index range (innermost loop)
        jmin, jmax: J-index range
        kmin, kmax: K-index range (outermost loop)

    Returns:
        Dictionary with dimension counts and fill specification

    Examples:
        >>> calculate_fill_dimensions(-7, 7, -7, 7, 0, 0)
        {'i_count': 15, 'j_count': 15, 'k_count': 1, 'total_elements': 225, ...}

        >>> calculate_fill_dimensions(0, 16, 0, 16, 0, 0)
        {'i_count': 17, 'j_count': 17, 'k_count': 1, 'total_elements': 289, ...}
    """
    i_count = imax - imin + 1
    j_count = jmax - jmin + 1
    k_count = kmax - kmin + 1
    total = i_count * j_count * k_count

    return {
        'i_count': i_count,
        'j_count': j_count,
        'k_count': k_count,
        'total_elements': total,
        'fill_spec': f"fill={imin}:{imax} {jmin}:{jmax} {kmin}:{kmax}",
        'note': f"Need {total} universe specifications in FILL array",
        'index_order': 'K (outermost), J, I (innermost)',
        'common_error': f"Don't forget to count ZERO! ({imin} to {imax} includes 0 if range crosses zero)"
    }


def calculate_hex_pitch(R: float) -> Dict:
    """
    Calculate hexagonal lattice pitch from R-vector magnitude.

    For LAT=2 (hexagonal) lattices with RHP surface.

    Critical formula: Pitch = R × √3

    Args:
        R: R-vector magnitude from RHP surface definition

    Returns:
        Dictionary with pitch and related parameters

    Example:
        >>> calculate_hex_pitch(1.6)
        {'R': 1.6, 'pitch': 2.7712..., 'sqrt3': 1.7320..., ...}
    """
    sqrt3 = math.sqrt(3)
    pitch = R * sqrt3

    return {
        'R': R,
        'pitch': pitch,
        'sqrt3': sqrt3,
        'formula': 'Pitch = R × √3',
        'note': 'This pitch value determines element spacing in hexagonal lattice'
    }


def repeat_notation_converter(universe_id: int, n_repeats: int) -> Dict:
    """
    Convert repeat notation to understand total copies.

    Critical rule: "U nR" = (n+1) total copies, NOT n copies!

    Args:
        universe_id: Universe number
        n_repeats: Number in "nR" notation

    Returns:
        Dictionary explaining the repeat notation

    Examples:
        >>> repeat_notation_converter(100, 2)
        {'notation': '100 2R', 'total_copies': 3, ...}

        >>> repeat_notation_converter(1116, 24)
        {'notation': '1116 24R', 'total_copies': 25, ...}
    """
    total_copies = n_repeats + 1

    return {
        'notation': f'{universe_id} {n_repeats}R',
        'total_copies': total_copies,
        'explanation': f'First occurrence + {n_repeats} repeats = {total_copies} total',
        'common_error': f'{universe_id} {n_repeats}R does NOT mean {n_repeats} copies!',
        'expanded_form': ' '.join([str(universe_id)] * total_copies)
    }


def validate_lattice_dimensions(lat_type: int,
                                fill_spec: Tuple[int, int, int, int, int, int],
                                surface_params: Dict,
                                element_count: int) -> Dict:
    """
    Validate that lattice dimensions match surface and element count.

    Prevents most common MCNP fatal errors.

    Args:
        lat_type: 1 for rectangular (RPP), 2 for hexagonal (RHP)
        fill_spec: (imin, imax, jmin, jmax, kmin, kmax)
        surface_params: Dictionary with surface dimensions
            For LAT=1: {'xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'}
            For LAT=2: {'R', 'height'}
        element_count: Number of elements provided in FILL array

    Returns:
        Dictionary with validation results and any warnings
    """
    imin, imax, jmin, jmax, kmin, kmax = fill_spec
    dims = calculate_fill_dimensions(imin, imax, jmin, jmax, kmin, kmax)

    warnings = []
    errors = []

    # Check element count
    if element_count != dims['total_elements']:
        errors.append(f"Element count mismatch: provided {element_count}, need {dims['total_elements']}")
        errors.append(f"  Formula: ({imax}-{imin}+1) × ({jmax}-{jmin}+1) × ({kmax}-{kmin}+1) = {dims['total_elements']}")

    if lat_type == 1:  # Rectangular - RPP validation
        if 'xmin' not in surface_params or 'xmax' not in surface_params:
            warnings.append("Cannot validate RPP surface: missing x parameters")
        else:
            x_extent = surface_params['xmax'] - surface_params['xmin']
            y_extent = surface_params['ymax'] - surface_params['ymin']
            z_extent = surface_params['zmax'] - surface_params['zmin']

            # Estimate pitch
            i_pitch = x_extent / dims['i_count'] if dims['i_count'] > 0 else 0
            j_pitch = y_extent / dims['j_count'] if dims['j_count'] > 0 else 0
            k_pitch = z_extent / dims['k_count'] if dims['k_count'] > 1 else 0

            if i_pitch == 0 or j_pitch == 0:
                warnings.append("Surface extent too small for lattice dimensions")

            warnings.append(f"Calculated pitch: I={i_pitch:.4f}, J={j_pitch:.4f}, K={k_pitch:.4f} cm")

    elif lat_type == 2:  # Hexagonal - RHP validation
        if 'R' not in surface_params:
            warnings.append("Cannot validate RHP surface: missing R parameter")
        else:
            hex_info = calculate_hex_pitch(surface_params['R'])
            warnings.append(f"Hexagonal pitch: {hex_info['pitch']:.4f} cm (R={surface_params['R']} × √3)")

            # For hexagonal, we can only warn about general fit
            if dims['i_count'] != dims['j_count']:
                warnings.append("Hexagonal lattices typically have equal I and J counts")

    else:
        errors.append(f"Invalid lattice type: {lat_type} (must be 1 or 2)")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'dimensions': dims,
        'surface_type': 'RPP' if lat_type == 1 else 'RHP' if lat_type == 2 else 'UNKNOWN'
    }


def generate_fill_array_template(imin: int, imax: int,
                                 jmin: int, jmax: int,
                                 kmin: int, kmax: int,
                                 default_universe: int = 100) -> str:
    """
    Generate a template FILL array with proper K,J,I ordering.

    Shows the structure users should fill in with actual universe numbers.

    Args:
        imin, imax, jmin, jmax, kmin, kmax: Fill range
        default_universe: Placeholder universe number

    Returns:
        Formatted FILL array string with comments showing indices
    """
    dims = calculate_fill_dimensions(imin, imax, jmin, jmax, kmin, kmax)

    lines = []
    lines.append(f"c FILL array for fill={imin}:{imax} {jmin}:{jmax} {kmin}:{kmax}")
    lines.append(f"c Total elements needed: {dims['total_elements']}")
    lines.append(f"c Index order: K (outermost), J, I (innermost)")
    lines.append("")

    element_num = 1
    for k in range(kmin, kmax + 1):
        if kmin != kmax:
            lines.append(f"c K = {k}")
        for j in range(jmin, jmax + 1):
            row = []
            for i in range(imin, imax + 1):
                row.append(str(default_universe))
                element_num += 1

            # Add comment showing J index
            if len(row) > 0:
                row_str = ' '.join(row)
                if jmin != jmax:
                    lines.append(f"     {row_str}  $ J={j}")
                else:
                    lines.append(f"     {row_str}")

        if kmin != kmax and k < kmax:
            lines.append("")  # Blank line between K levels

    return '\n'.join(lines)


def main():
    """Interactive command-line interface for lattice dimension calculator."""

    print("=" * 60)
    print("MCNP Lattice Dimension Calculator")
    print("For LAT=1 (rectangular) and LAT=2 (hexagonal) lattices")
    print("=" * 60)
    print()

    # Get lattice type
    print("Lattice type:")
    print("  1 = Rectangular (RPP surface)")
    print("  2 = Hexagonal (RHP surface)")
    lat_type = int(input("Enter lattice type (1 or 2): "))
    print()

    # Get FILL range
    print("Enter FILL array range (e.g., fill=-7:7 -7:7 0:0):")
    imin = int(input("  IMIN: "))
    imax = int(input("  IMAX: "))
    jmin = int(input("  JMIN: "))
    jmax = int(input("  JMAX: "))
    kmin = int(input("  KMIN: "))
    kmax = int(input("  KMAX: "))
    print()

    # Calculate dimensions
    dims = calculate_fill_dimensions(imin, imax, jmin, jmax, kmin, kmax)

    print("-" * 60)
    print("DIMENSION CALCULATION RESULTS:")
    print("-" * 60)
    print(f"Fill specification: {dims['fill_spec']}")
    print()
    print(f"  I elements: {imax} - {imin} + 1 = {dims['i_count']}")
    print(f"  J elements: {jmax} - {jmin} + 1 = {dims['j_count']}")
    print(f"  K elements: {kmax} - {kmin} + 1 = {dims['k_count']}")
    print()
    print(f"  TOTAL ELEMENTS NEEDED: {dims['total_elements']}")
    print()
    print(f"Index order: {dims['index_order']}")
    print()
    if any(x < 0 and y > 0 for x, y in [(imin, imax), (jmin, jmax), (kmin, kmax)]):
        print("⚠  NOTE: Your range crosses zero. Don't forget to count 0!")
        print(f"   {dims['common_error']}")
    print()

    # Lattice-specific info
    if lat_type == 2:
        print("-" * 60)
        print("HEXAGONAL LATTICE INFO:")
        print("-" * 60)
        R = float(input("Enter R-vector magnitude from RHP surface: "))
        hex_info = calculate_hex_pitch(R)
        print(f"\n  {hex_info['formula']}")
        print(f"  Pitch = {hex_info['R']} × {hex_info['sqrt3']:.6f} = {hex_info['pitch']:.4f} cm")
        print()

    # Ask about repeat notation
    print("-" * 60)
    use_repeat = input("Do you want to use repeat notation (nR)? (y/n): ").lower()
    if use_repeat == 'y':
        print()
        print("REPEAT NOTATION HELPER:")
        print("  Reminder: U nR = (n+1) total copies!")
        print()
        universe = int(input("  Universe number: "))
        n_repeats = int(input("  Number of repeats (n in nR): "))

        repeat_info = repeat_notation_converter(universe, n_repeats)
        print()
        print(f"  Notation: {repeat_info['notation']}")
        print(f"  Total copies: {repeat_info['total_copies']}")
        print(f"  Explanation: {repeat_info['explanation']}")
        print()
        print(f"  ⚠  {repeat_info['common_error']}")
        print()

    # Generate template
    print("-" * 60)
    generate = input("Generate FILL array template? (y/n): ").lower()
    if generate == 'y':
        print()
        universe = int(input("Default universe number for template: "))
        print()
        template = generate_fill_array_template(imin, imax, jmin, jmax, kmin, kmax, universe)
        print(template)
        print()

    print("=" * 60)
    print("Done! Use this information to construct your MCNP lattice.")
    print("=" * 60)


if __name__ == '__main__':
    main()
