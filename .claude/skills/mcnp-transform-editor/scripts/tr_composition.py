#!/usr/bin/env python3
"""
TR Composition Calculator

Composes two MCNP TR transformations into a single equivalent transformation.

Given TR1 and TR2, calculates TR3 = TR2 ∘ TR1 (apply TR1 first, then TR2).

Mathematical formulation:
    R3 = R2 · R1  (matrix multiplication)
    d3 = d2 + R2 · d1

Usage:
    python tr_composition.py

    Interactive mode: Prompts for TR1 and TR2 parameters

Example:
    Compose two transformations step-by-step
"""

import numpy as np
import sys


def parse_tr_card(tr_string):
    """
    Parse TR card parameters from string.

    Args:
        tr_string: Space-separated TR parameters (3 or 12 values)
                   "dx dy dz" or "dx dy dz a11 a12 a13 a21 a22 a23 a31 a32 a33"

    Returns:
        tuple: (d, R) where d is (3,) translation vector, R is (3,3) rotation matrix
    """
    params = [float(x) for x in tr_string.strip().split()]

    if len(params) == 3:
        # Translation only
        d = np.array(params)
        R = np.eye(3)
    elif len(params) == 12:
        # Translation + rotation
        d = np.array(params[0:3])
        R = np.array([
            [params[3], params[4], params[5]],
            [params[6], params[7], params[8]],
            [params[9], params[10], params[11]]
        ])
    else:
        raise ValueError(f"Expected 3 or 12 parameters, got {len(params)}")

    return d, R


def compose_transformations(d1, R1, d2, R2, verbose=True):
    """
    Compose two transformations: TR3 = TR2 ∘ TR1

    Args:
        d1, R1: First transformation (applied first)
        d2, R2: Second transformation (applied second)
        verbose: Print detailed results

    Returns:
        tuple: (d3, R3) - composed transformation
    """
    # Calculate composition
    R3 = np.dot(R2, R1)
    d3 = d2 + np.dot(R2, d1)

    if verbose:
        print("\n" + "="*60)
        print("TR COMPOSITION: TR3 = TR2 ∘ TR1")
        print("="*60)

        print("\nTR1 (applied first):")
        print(f"  Translation: ({d1[0]:9.6f}, {d1[1]:9.6f}, {d1[2]:9.6f})")
        print("  Rotation:")
        print(f"    [{R1[0,0]:9.6f}  {R1[0,1]:9.6f}  {R1[0,2]:9.6f}]")
        print(f"    [{R1[1,0]:9.6f}  {R1[1,1]:9.6f}  {R1[1,2]:9.6f}]")
        print(f"    [{R1[2,0]:9.6f}  {R1[2,1]:9.6f}  {R1[2,2]:9.6f}]")

        print("\nTR2 (applied second):")
        print(f"  Translation: ({d2[0]:9.6f}, {d2[1]:9.6f}, {d2[2]:9.6f})")
        print("  Rotation:")
        print(f"    [{R2[0,0]:9.6f}  {R2[0,1]:9.6f}  {R2[0,2]:9.6f}]")
        print(f"    [{R2[1,0]:9.6f}  {R2[1,1]:9.6f}  {R2[1,2]:9.6f}]")
        print(f"    [{R2[2,0]:9.6f}  {R2[2,1]:9.6f}  {R2[2,2]:9.6f}]")

        print("\nTR3 (composition):")
        print(f"  Translation: ({d3[0]:9.6f}, {d3[1]:9.6f}, {d3[2]:9.6f})")
        print("  Rotation:")
        print(f"    [{R3[0,0]:9.6f}  {R3[0,1]:9.6f}  {R3[0,2]:9.6f}]")
        print(f"    [{R3[1,0]:9.6f}  {R3[1,1]:9.6f}  {R3[1,2]:9.6f}]")
        print(f"    [{R3[2,0]:9.6f}  {R3[2,1]:9.6f}  {R3[2,2]:9.6f}]")

        print("\nMCNP TR Card:")
        print(f"  *TR3  {d3[0]:.6f} {d3[1]:.6f} {d3[2]:.6f}  &")
        print(f"        {R3[0,0]:.6f} {R3[0,1]:.6f} {R3[0,2]:.6f}  &")
        print(f"        {R3[1,0]:.6f} {R3[1,1]:.6f} {R3[1,2]:.6f}  &")
        print(f"        {R3[2,0]:.6f} {R3[2,1]:.6f} {R3[2,2]:.6f}")

        # Validation
        det = np.linalg.det(R3)
        print(f"\nValidation:")
        print(f"  Determinant: {det:.10f} (should be ±1.0)")

        row_norms = [np.linalg.norm(R3[i,:]) for i in range(3)]
        print(f"  Row norms: [{row_norms[0]:.10f}, {row_norms[1]:.10f}, {row_norms[2]:.10f}]")

        print("="*60 + "\n")

    return d3, R3


def interactive_mode():
    """Interactive input for TR composition."""
    print("\n" + "="*60)
    print("TR COMPOSITION CALCULATOR")
    print("="*60)
    print("\nCompose two transformations: TR3 = TR2 ∘ TR1")
    print("(TR1 is applied first, then TR2)")
    print()

    # Get TR1
    print("Enter TR1 parameters:")
    print("  Format: dx dy dz [a11 a12 a13 a21 a22 a23 a31 a32 a33]")
    print("  (3 values for translation only, 12 for translation + rotation)")
    tr1_input = input("  TR1: ").strip()

    try:
        d1, R1 = parse_tr_card(tr1_input)
    except ValueError as e:
        print(f"Error parsing TR1: {e}")
        sys.exit(1)

    # Get TR2
    print("\nEnter TR2 parameters:")
    print("  Format: dx dy dz [a11 a12 a13 a21 a22 a23 a31 a32 a33]")
    tr2_input = input("  TR2: ").strip()

    try:
        d2, R2 = parse_tr_card(tr2_input)
    except ValueError as e:
        print(f"Error parsing TR2: {e}")
        sys.exit(1)

    # Compose
    d3, R3 = compose_transformations(d1, R1, d2, R2, verbose=True)


def example_usage():
    """Show example composition."""
    print("\n" + "="*60)
    print("EXAMPLE: Rotate 90° about z, then translate (5,0,0)")
    print("="*60)

    # TR1: Rotate 90° CCW about z-axis
    d1 = np.array([0.0, 0.0, 0.0])
    R1 = np.array([[0, -1, 0],
                   [1,  0, 0],
                   [0,  0, 1]], dtype=float)

    # TR2: Translate (5, 0, 0)
    d2 = np.array([5.0, 0.0, 0.0])
    R2 = np.eye(3)

    # Compose
    d3, R3 = compose_transformations(d1, R1, d2, R2, verbose=True)

    # Test point
    print("Test transformation on point (1, 0, 0):")
    p0 = np.array([1, 0, 0])

    # Apply TR1
    p1 = np.dot(R1, p0) + d1
    print(f"  After TR1: ({p1[0]:.3f}, {p1[1]:.3f}, {p1[2]:.3f})")

    # Apply TR2
    p2 = np.dot(R2, p1) + d2
    print(f"  After TR2: ({p2[0]:.3f}, {p2[1]:.3f}, {p2[2]:.3f})")

    # Apply TR3 (composition)
    p3 = np.dot(R3, p0) + d3
    print(f"  With TR3:  ({p3[0]:.3f}, {p3[1]:.3f}, {p3[2]:.3f})")

    if np.allclose(p2, p3):
        print("  ✓ Composition verified!")
    else:
        print("  ✗ Composition ERROR!")


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example_usage()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
