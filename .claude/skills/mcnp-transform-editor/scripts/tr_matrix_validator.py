#!/usr/bin/env python3
"""
TR Matrix Validator

Validates MCNP transformation matrices for:
- Orthonormality (rows are unit vectors)
- Orthogonality (rows are perpendicular)
- Right-handedness (determinant = ±1)

Usage:
    python tr_matrix_validator.py

    Interactive mode: Prompts for matrix elements
    OR provide matrix elements as command-line arguments

Example:
    python tr_matrix_validator.py 0 -1 0 1 0 0 0 0 1
"""

import sys
import numpy as np


def validate_tr_matrix(a11, a12, a13, a21, a22, a23, a31, a32, a33, verbose=True):
    """
    Validate a 3x3 rotation matrix for MCNP TR card use.

    Args:
        a11-a33: Matrix elements (row-major order)
        verbose: Print detailed results

    Returns:
        tuple: (is_valid, messages)
            is_valid: bool - True if matrix is valid
            messages: list of str - Validation messages
    """
    messages = []
    is_valid = True

    # Construct matrix
    R = np.array([[a11, a12, a13],
                  [a21, a22, a23],
                  [a31, a32, a33]], dtype=float)

    if verbose:
        print("\n" + "="*60)
        print("TR MATRIX VALIDATION")
        print("="*60)
        print("\nInput Matrix:")
        print(f"  [{a11:9.6f}  {a12:9.6f}  {a13:9.6f}]")
        print(f"  [{a21:9.6f}  {a22:9.6f}  {a23:9.6f}]")
        print(f"  [{a31:9.6f}  {a32:9.6f}  {a33:9.6f}]")
        print()

    # Check 1: Row norms (should be 1.0)
    tolerance = 1e-6
    row_norms = [np.linalg.norm(R[i,:]) for i in range(3)]

    if verbose:
        print("CHECK 1: Orthonormality (Row Norms)")
        print("-" * 60)

    for i, norm in enumerate(row_norms):
        status = "✓ PASS" if abs(norm - 1.0) < tolerance else "✗ FAIL"
        message = f"  Row {i+1} norm: {norm:.10f} (should be 1.0) ... {status}"

        if verbose:
            print(message)

        messages.append(message)

        if abs(norm - 1.0) >= tolerance:
            is_valid = False

    # Check 2: Orthogonality (dot products should be 0)
    if verbose:
        print("\nCHECK 2: Orthogonality (Row Dot Products)")
        print("-" * 60)

    dot_products = [
        (0, 1, np.dot(R[0,:], R[1,:])),
        (0, 2, np.dot(R[0,:], R[2,:])),
        (1, 2, np.dot(R[1,:], R[2,:]))
    ]

    for i, j, dot in dot_products:
        status = "✓ PASS" if abs(dot) < tolerance else "✗ FAIL"
        message = f"  Row {i+1} · Row {j+1}: {dot:.10f} (should be 0.0) ... {status}"

        if verbose:
            print(message)

        messages.append(message)

        if abs(dot) >= tolerance:
            is_valid = False

    # Check 3: Determinant (should be ±1)
    det = np.linalg.det(R)

    if verbose:
        print("\nCHECK 3: Right-Handedness (Determinant)")
        print("-" * 60)

    det_status = "✓ PASS" if abs(abs(det) - 1.0) < tolerance else "✗ FAIL"
    det_type = "proper rotation" if abs(det - 1.0) < tolerance else \
               "reflection/improper" if abs(det + 1.0) < tolerance else \
               "INVALID"

    message = f"  Determinant: {det:.10f} (should be ±1.0) ... {det_status}"
    if verbose:
        print(message)
        print(f"  Type: {det_type}")

    messages.append(message)
    messages.append(f"  Type: {det_type}")

    if abs(abs(det) - 1.0) >= tolerance:
        is_valid = False

    # Summary
    if verbose:
        print("\n" + "="*60)
        if is_valid:
            print("RESULT: ✓ Matrix is VALID for MCNP TR card")
        else:
            print("RESULT: ✗ Matrix is INVALID - corrections needed")
        print("="*60 + "\n")

    return is_valid, messages


def interactive_input():
    """Prompt user for matrix elements interactively."""
    print("\nEnter the 9 matrix elements (row by row):")
    print("Format: a11 a12 a13 a21 a22 a23 a31 a32 a33")
    print()

    try:
        elements = input("Matrix elements: ").strip().split()

        if len(elements) != 9:
            print(f"Error: Expected 9 elements, got {len(elements)}")
            sys.exit(1)

        return [float(x) for x in elements]

    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        sys.exit(1)


def main():
    """Main function for command-line usage."""
    if len(sys.argv) == 10:
        # Command-line arguments provided
        try:
            elements = [float(x) for x in sys.argv[1:10]]
        except ValueError as e:
            print(f"Error: Invalid matrix elements - {e}")
            sys.exit(1)
    else:
        # Interactive mode
        elements = interactive_input()

    # Validate matrix
    is_valid, messages = validate_tr_matrix(*elements, verbose=True)

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
