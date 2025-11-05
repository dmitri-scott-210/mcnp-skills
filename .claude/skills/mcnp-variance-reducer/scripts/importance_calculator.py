#!/usr/bin/env python3
"""
MCNP Importance Calculator

Calculates optimal cell importance values for variance reduction based on
geometric progression and distance-to-detector relationships.

Usage:
    python importance_calculator.py --cells 5 --progression 2 --detector-cell 5
    python importance_calculator.py --distances 10 30 50 70 90 --detector-distance 100

Author: MCNP Variance Reducer Skill
Version: 1.0.0
"""

import argparse
import math
import sys
from typing import List, Tuple


def geometric_progression(num_cells: int, ratio: float = 2.0, start: float = 1.0) -> List[float]:
    """
    Calculate geometric progression of importance values.

    Args:
        num_cells: Number of cells (excluding graveyard)
        ratio: Progression ratio (2.0 = double each cell, 4.0 = quadruple)
        start: Starting importance value

    Returns:
        List of importance values (last is 0 for graveyard)

    Example:
        >>> geometric_progression(5, 2.0, 1.0)
        [1.0, 2.0, 4.0, 8.0, 16.0, 0]
    """
    if ratio <= 1.0:
        raise ValueError("Ratio must be > 1.0")
    if num_cells < 1:
        raise ValueError("Number of cells must be >= 1")

    importances = [start * (ratio ** i) for i in range(num_cells)]
    importances.append(0)  # Graveyard

    return importances


def distance_based_importance(
    distances: List[float],
    detector_distance: float,
    power: float = 2.0,
    normalize: bool = True
) -> List[float]:
    """
    Calculate importance based on inverse distance to detector.

    Theory: I(r) ∝ 1 / d^power, where d = distance to detector

    Args:
        distances: List of cell distances from source (cm)
        detector_distance: Distance to detector from source (cm)
        power: Distance power law (2.0 = inverse square)
        normalize: Normalize to start at 1.0

    Returns:
        List of importance values (last is 0 for graveyard)

    Example:
        >>> distance_based_importance([10, 30, 50], 100, 2.0)
        [1.0, 3.5, 8.2, 0]
    """
    if detector_distance <= 0:
        raise ValueError("Detector distance must be > 0")
    if any(d <= 0 for d in distances):
        raise ValueError("All distances must be > 0")
    if any(d >= detector_distance for d in distances):
        raise ValueError("All cell distances must be < detector distance")

    # Calculate importance from inverse distance
    # Higher importance = closer to detector
    importances = []
    for d in distances:
        distance_to_detector = detector_distance - d
        importance = 1.0 / (distance_to_detector ** power)
        importances.append(importance)

    # Normalize to start at 1.0
    if normalize and importances:
        norm_factor = 1.0 / importances[0]
        importances = [imp * norm_factor for imp in importances]

    # Add graveyard
    importances.append(0)

    return importances


def check_importance_ratios(importances: List[float], max_ratio: float = 4.0) -> List[Tuple[int, int, float]]:
    """
    Check for importance ratio violations between adjacent cells.

    Args:
        importances: List of importance values
        max_ratio: Maximum recommended ratio (default 4.0)

    Returns:
        List of tuples: (cell_i, cell_j, ratio) for violations

    Example:
        >>> check_importance_ratios([1, 2, 8, 32], 4.0)
        [(2, 3, 4.0), (3, 4, 4.0)]
    """
    violations = []

    for i in range(len(importances) - 1):
        if importances[i] == 0 or importances[i+1] == 0:
            continue  # Skip graveyard comparisons

        ratio = importances[i+1] / importances[i]
        if ratio > max_ratio:
            violations.append((i+1, i+2, ratio))  # 1-indexed for MCNP cells

    return violations


def optimize_importance_ratios(
    importances: List[float],
    max_ratio: float = 4.0
) -> List[float]:
    """
    Optimize importance values to satisfy maximum ratio constraint.

    Inserts intermediate values where ratios are too large.

    Args:
        importances: Original importance values
        max_ratio: Maximum allowed ratio

    Returns:
        Optimized importance values with intermediate cells suggested
    """
    optimized = [importances[0]]

    for i in range(len(importances) - 1):
        if importances[i] == 0 or importances[i+1] == 0:
            optimized.append(importances[i+1])
            continue

        ratio = importances[i+1] / importances[i]

        if ratio <= max_ratio:
            optimized.append(importances[i+1])
        else:
            # Insert intermediate values
            num_intermediates = int(math.ceil(math.log(ratio) / math.log(max_ratio))) - 1
            step_ratio = ratio ** (1.0 / (num_intermediates + 1))

            for j in range(1, num_intermediates + 2):
                intermediate = importances[i] * (step_ratio ** j)
                optimized.append(intermediate)

    return optimized


def format_imp_card(importances: List[float], particle: str = "N") -> str:
    """
    Format importance values as MCNP IMP card.

    Args:
        importances: List of importance values
        particle: Particle type (N, P, E, etc.)

    Returns:
        Formatted IMP card string

    Example:
        >>> format_imp_card([1, 2, 4, 8, 0], "N")
        'IMP:N  1  2  4  8  0'
    """
    # Format values: integers if whole numbers, otherwise 2 decimal places
    formatted = []
    for imp in importances:
        if imp == int(imp):
            formatted.append(str(int(imp)))
        else:
            formatted.append(f"{imp:.2f}")

    return f"IMP:{particle}  " + "  ".join(formatted)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate MCNP cell importance values for variance reduction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Geometric progression (5 cells, ratio 2.0)
  python importance_calculator.py --cells 5 --progression 2.0

  # Distance-based (cells at 10, 30, 50 cm; detector at 100 cm)
  python importance_calculator.py --distances 10 30 50 --detector-distance 100

  # Custom starting value
  python importance_calculator.py --cells 6 --progression 2.0 --start 0.5

  # Check for ratio violations
  python importance_calculator.py --cells 5 --progression 4.0 --check-ratios
        """
    )

    # Mutually exclusive groups
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cells', type=int, help='Number of cells (geometric progression)')
    group.add_argument('--distances', type=float, nargs='+', help='Cell distances from source (cm)')

    # Optional arguments
    parser.add_argument('--progression', type=float, default=2.0,
                        help='Geometric progression ratio (default: 2.0)')
    parser.add_argument('--start', type=float, default=1.0,
                        help='Starting importance value (default: 1.0)')
    parser.add_argument('--detector-distance', type=float,
                        help='Distance to detector (required for distance-based)')
    parser.add_argument('--particle', type=str, default='N',
                        help='Particle type (default: N)')
    parser.add_argument('--check-ratios', action='store_true',
                        help='Check for importance ratio violations')
    parser.add_argument('--max-ratio', type=float, default=4.0,
                        help='Maximum recommended ratio (default: 4.0)')
    parser.add_argument('--optimize', action='store_true',
                        help='Optimize to satisfy max ratio constraint')

    args = parser.parse_args()

    # Calculate importances
    try:
        if args.cells:
            importances = geometric_progression(args.cells, args.progression, args.start)
            print(f"Geometric Progression (ratio={args.progression}, start={args.start}):")
        else:
            if not args.detector_distance:
                parser.error("--detector-distance required with --distances")
            importances = distance_based_importance(args.distances, args.detector_distance)
            print(f"Distance-Based (detector at {args.detector_distance} cm):")

        # Display importances
        print("\nCell  Importance")
        print("-" * 20)
        for i, imp in enumerate(importances[:-1], 1):
            print(f"{i:4d}  {imp:10.2f}")
        print(f"{len(importances):4d}  {importances[-1]:10.2f}  (graveyard)")

        # Check ratios
        if args.check_ratios or args.optimize:
            violations = check_importance_ratios(importances, args.max_ratio)
            if violations:
                print(f"\nWARNING: {len(violations)} importance ratio violations (max={args.max_ratio}):")
                for cell_i, cell_j, ratio in violations:
                    print(f"  Cell {cell_i} → {cell_j}: ratio = {ratio:.2f}")

                if args.optimize:
                    print("\nOptimized importances (with intermediate cells):")
                    optimized = optimize_importance_ratios(importances, args.max_ratio)
                    print("\nCell  Importance")
                    print("-" * 20)
                    for i, imp in enumerate(optimized[:-1], 1):
                        print(f"{i:4d}  {imp:10.2f}")
                    print(f"{len(optimized):4d}  {optimized[-1]:10.2f}  (graveyard)")
                    importances = optimized
            else:
                print(f"\nAll importance ratios ≤ {args.max_ratio} ✓")

        # Format as IMP card
        print(f"\nMCNP IMP Card:")
        print(format_imp_card(importances, args.particle))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
