#!/usr/bin/env python3
"""
MCNP DXTRAN Sphere Locator

Calculates optimal DXTRAN sphere location and parameters for point detector tallies.
Verifies alignment with F5 detector coordinates.

Usage:
    python dxtran_sphere_locator.py --detector 100 0 0
    python dxtran_sphere_locator.py --detector 100 0 0 --radius 2.0 --max 1000

Author: MCNP Variance Reducer Skill
Version: 1.0.0
"""

import argparse
import math
import sys
from typing import Tuple


def calculate_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        p1: First point (x, y, z)
        p2: Second point (x, y, z)

    Returns:
        Distance in cm
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def suggest_radius(detector_distance: float) -> Tuple[float, str]:
    """
    Suggest DXTRAN sphere radius based on detector distance from source.

    Args:
        detector_distance: Distance from source to detector (cm)

    Returns:
        Tuple of (radius, reasoning)
    """
    if detector_distance < 10:
        return 0.5, "Close detector (<10 cm) - small radius sufficient"
    elif detector_distance < 50:
        return 1.0, "Medium distance (10-50 cm) - moderate radius"
    elif detector_distance < 100:
        return 2.0, "Far detector (50-100 cm) - larger radius"
    else:
        return 5.0, "Very far detector (>100 cm) - large radius for good statistics"


def suggest_max_contributions(detector_distance: float, nps: int = 1000000) -> Tuple[int, str]:
    """
    Suggest MAX parameter for DXTRAN card.

    Args:
        detector_distance: Distance from source to detector (cm)
        nps: Number of source particles

    Returns:
        Tuple of (max_value, reasoning)
    """
    # Heuristic: max ≈ nps / 1000 for close detectors, higher for far
    if detector_distance < 10:
        max_val = max(100, nps // 10000)
        reason = "Close detector - fewer contributions per particle"
    elif detector_distance < 100:
        max_val = max(500, nps // 2000)
        reason = "Medium distance - moderate contributions"
    else:
        max_val = max(1000, nps // 1000)
        reason = "Far detector - many contributions needed"

    # Cap at reasonable value
    max_val = min(max_val, 10000)

    return max_val, reason


def verify_alignment(
    detector: Tuple[float, float, float],
    dxtran_center: Tuple[float, float, float],
    dxtran_radius: float,
    tolerance: float = 0.01
) -> Tuple[bool, float, str]:
    """
    Verify DXTRAN sphere encompasses detector.

    Args:
        detector: Detector coordinates (x, y, z)
        dxtran_center: DXTRAN sphere center (x, y, z)
        dxtran_radius: DXTRAN sphere radius
        tolerance: Alignment tolerance (cm)

    Returns:
        Tuple of (aligned, distance, message)
    """
    distance = calculate_distance(detector, dxtran_center)

    if distance <= tolerance:
        aligned = True
        message = f"✓ Perfectly aligned (distance = {distance:.4f} cm)"
    elif distance <= dxtran_radius:
        aligned = True
        message = f"✓ Detector within sphere (distance = {distance:.2f} cm < radius = {dxtran_radius:.2f} cm)"
    else:
        aligned = False
        message = f"✗ MISALIGNED: Detector outside sphere (distance = {distance:.2f} cm > radius = {dxtran_radius:.2f} cm)"

    return aligned, distance, message


def format_dxtran_card(
    radius: float,
    center: Tuple[float, float, float],
    max_val: int,
    particle: str = "N"
) -> str:
    """
    Format DXTRAN card for MCNP input.

    Args:
        radius: Sphere radius (cm)
        center: Sphere center coordinates (x, y, z)
        max_val: Maximum contributions
        particle: Particle type (optional)

    Returns:
        Formatted DXTRAN card
    """
    x, y, z = center
    if particle and particle.upper() != "N":
        return f"DXTRAN  {radius:.2f}  {x:.2f} {y:.2f} {z:.2f}  {max_val}  {particle.upper()}"
    else:
        return f"DXTRAN  {radius:.2f}  {x:.2f} {y:.2f} {z:.2f}  {max_val}"


def format_f5_card(detector: Tuple[float, float, float], radius: float, particle: str = "N") -> str:
    """
    Format F5 card for MCNP input.

    Args:
        detector: Detector coordinates (x, y, z)
        radius: Detector radius (cm)
        particle: Particle type

    Returns:
        Formatted F5 card
    """
    x, y, z = detector
    return f"F5:{particle}  {x:.2f} {y:.2f} {z:.2f}  {radius:.2f}"


def main():
    parser = argparse.ArgumentParser(
        description="Calculate optimal DXTRAN sphere location and parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic DXTRAN for detector at (100, 0, 0)
  python dxtran_sphere_locator.py --detector 100 0 0

  # Custom radius and max contributions
  python dxtran_sphere_locator.py --detector 100 0 0 --radius 2.0 --max 1000

  # Verify existing DXTRAN card alignment
  python dxtran_sphere_locator.py --detector 100 0 0 --dxtran-center 100 0 0 --dxtran-radius 1.0

  # Include source location for distance calculation
  python dxtran_sphere_locator.py --detector 100 0 0 --source 0 0 0
        """
    )

    # Required arguments
    parser.add_argument('--detector', type=float, nargs=3, required=True,
                        metavar=('X', 'Y', 'Z'),
                        help='Detector coordinates (cm)')

    # Optional arguments
    parser.add_argument('--source', type=float, nargs=3, default=[0, 0, 0],
                        metavar=('X', 'Y', 'Z'),
                        help='Source coordinates (default: 0 0 0)')
    parser.add_argument('--radius', type=float,
                        help='DXTRAN sphere radius (auto-calculate if not provided)')
    parser.add_argument('--max', type=int, dest='max_contributions',
                        help='MAX contributions parameter (auto-calculate if not provided)')
    parser.add_argument('--nps', type=int, default=1000000,
                        help='Number of source particles (default: 1000000)')
    parser.add_argument('--particle', type=str, default='N',
                        help='Particle type (default: N)')
    parser.add_argument('--detector-radius', type=float, default=0.5,
                        help='F5 detector radius (default: 0.5 cm)')

    # Verification mode
    parser.add_argument('--dxtran-center', type=float, nargs=3,
                        metavar=('X', 'Y', 'Z'),
                        help='Verify existing DXTRAN center')
    parser.add_argument('--dxtran-radius', type=float,
                        help='Verify existing DXTRAN radius')

    args = parser.parse_args()

    detector = tuple(args.detector)
    source = tuple(args.source)

    # Calculate detector distance from source
    detector_distance = calculate_distance(source, detector)

    print("DXTRAN Sphere Configuration")
    print("=" * 70)
    print(f"Source location:    ({source[0]:.2f}, {source[1]:.2f}, {source[2]:.2f})")
    print(f"Detector location:  ({detector[0]:.2f}, {detector[1]:.2f}, {detector[2]:.2f})")
    print(f"Distance:           {detector_distance:.2f} cm")
    print()

    # Suggest or use provided radius
    if args.radius is None:
        radius, radius_reason = suggest_radius(detector_distance)
        print(f"Suggested radius:   {radius:.2f} cm ({radius_reason})")
    else:
        radius = args.radius
        print(f"Using radius:       {radius:.2f} cm (user-specified)")

    # Suggest or use provided max contributions
    if args.max_contributions is None:
        max_val, max_reason = suggest_max_contributions(detector_distance, args.nps)
        print(f"Suggested MAX:      {max_val} ({max_reason})")
    else:
        max_val = args.max_contributions
        print(f"Using MAX:          {max_val} (user-specified)")

    print()

    # DXTRAN center (same as detector for optimal performance)
    dxtran_center = detector

    # Verification mode
    if args.dxtran_center and args.dxtran_radius:
        print("Verification Mode:")
        print("=" * 70)
        aligned, distance, message = verify_alignment(
            detector,
            tuple(args.dxtran_center),
            args.dxtran_radius
        )
        print(message)

        if not aligned:
            print("\nRECOMMENDATION: Update DXTRAN center to match detector:")
            print(f"  Current:  DXTRAN  {args.dxtran_radius:.2f}  " +
                  f"{args.dxtran_center[0]:.2f} {args.dxtran_center[1]:.2f} {args.dxtran_center[2]:.2f}")
            print(f"  Correct:  {format_dxtran_card(args.dxtran_radius, detector, max_val, args.particle)}")
        print()

    # Output MCNP cards
    print("MCNP Data Cards:")
    print("=" * 70)
    print("c")
    print("c --- Point detector ---")
    print(format_f5_card(detector, args.detector_radius, args.particle))
    print("c")
    print("c --- DXTRAN sphere (must match detector location) ---")
    print(format_dxtran_card(radius, dxtran_center, max_val, args.particle))
    print("c")
    print("c --- DXC: Which cells contribute to DXTRAN ---")
    print("c Option 1: All cells contribute (default)")
    print("c DXC  J  J  J")
    print("c")
    print("c Option 2: Only specific cells contribute")
    print("c DXC  1  2  3  4  J  J  J        $ Cells 1-4 + rest")
    print()

    # Usage notes
    print("Usage Notes:")
    print("=" * 70)
    print("1. DXTRAN center MUST match detector location for optimal performance")
    print("2. Radius should encompass detector but not be excessive")
    print("3. MAX prevents memory overflow - increase if contributions limited")
    print("4. DXC limits which cells contribute (default: all cells)")
    print("5. Combine with weight windows for best results")
    print()

    print("Expected Benefits:")
    print("=" * 70)
    if detector_distance < 50:
        print(f"- FOM improvement: 10-50× (close detector)")
    elif detector_distance < 100:
        print(f"- FOM improvement: 50-200× (medium distance)")
    else:
        print(f"- FOM improvement: 100-500× (far detector)")
    print(f"- Reduces variance at point detector significantly")
    print(f"- Most effective when source → detector path is complex")


if __name__ == "__main__":
    main()
