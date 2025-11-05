#!/usr/bin/env python3
"""
Rotation Matrix Generator

Generates rotation matrices for MCNP TR cards from various rotation representations:
- Euler angles (x-y-z convention)
- Axis-angle (Rodrigues' formula)
- Single-axis rotations

Usage:
    python rotation_matrix_generator.py --euler <theta_x> <theta_y> <theta_z> [--degrees]
    python rotation_matrix_generator.py --axis <kx> <ky> <kz> --angle <theta> [--degrees]
    python rotation_matrix_generator.py --rotate-x <angle> [--degrees]
    python rotation_matrix_generator.py --rotate-y <angle> [--degrees]
    python rotation_matrix_generator.py --rotate-z <angle> [--degrees]

Examples:
    python rotation_matrix_generator.py --euler 30 45 60 --degrees
    python rotation_matrix_generator.py --axis 1 1 1 --angle 30 --degrees
    python rotation_matrix_generator.py --rotate-z 90 --degrees
"""

import numpy as np
import sys
import argparse


def rotation_matrix_x(theta):
    """Rotation matrix about x-axis by angle theta (radians)."""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[1,  0,  0],
                     [0,  c, -s],
                     [0,  s,  c]])


def rotation_matrix_y(theta):
    """Rotation matrix about y-axis by angle theta (radians)."""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[ c, 0, s],
                     [ 0, 1, 0],
                     [-s, 0, c]])


def rotation_matrix_z(theta):
    """Rotation matrix about z-axis by angle theta (radians)."""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s, 0],
                     [s,  c, 0],
                     [0,  0, 1]])


def rotation_matrix_euler(theta_x, theta_y, theta_z, degrees=False):
    """
    Rotation matrix from Euler angles (x-y-z convention).

    Args:
        theta_x: Rotation about x-axis
        theta_y: Rotation about y-axis
        theta_z: Rotation about z-axis
        degrees: If True, angles are in degrees; otherwise radians

    Returns:
        3x3 rotation matrix
    """
    if degrees:
        theta_x = np.radians(theta_x)
        theta_y = np.radians(theta_y)
        theta_z = np.radians(theta_z)

    Rx = rotation_matrix_x(theta_x)
    Ry = rotation_matrix_y(theta_y)
    Rz = rotation_matrix_z(theta_z)

    # MCNP convention: Rx · Ry · Rz
    R = np.dot(Rx, np.dot(Ry, Rz))

    return R


def rotation_matrix_axis_angle(axis, angle, degrees=False):
    """
    Rotation matrix from axis-angle representation using Rodrigues' formula.

    Args:
        axis: Rotation axis vector [kx, ky, kz]
        angle: Rotation angle
        degrees: If True, angle is in degrees; otherwise radians

    Returns:
        3x3 rotation matrix
    """
    if degrees:
        angle = np.radians(angle)

    # Normalize axis
    k = np.array(axis, dtype=float)
    k = k / np.linalg.norm(k)

    # Rodrigues' formula: R = I*cos(θ) + K*sin(θ) + kk^T*(1-cos(θ))
    I = np.eye(3)
    K = np.array([[0,    -k[2],  k[1]],
                  [k[2],   0,   -k[0]],
                  [-k[1], k[0],   0  ]])

    kkt = np.outer(k, k)

    R = I * np.cos(angle) + K * np.sin(angle) + kkt * (1 - np.cos(angle))

    return R


def print_matrix_info(R, name="Rotation Matrix", include_tr_card=True):
    """Print rotation matrix with validation info."""
    print("\n" + "="*60)
    print(f"{name}")
    print("="*60)

    print("\nMatrix:")
    print(f"  [{R[0,0]:9.6f}  {R[0,1]:9.6f}  {R[0,2]:9.6f}]")
    print(f"  [{R[1,0]:9.6f}  {R[1,1]:9.6f}  {R[1,2]:9.6f}]")
    print(f"  [{R[2,0]:9.6f}  {R[2,1]:9.6f}  {R[2,2]:9.6f}]")

    if include_tr_card:
        print("\nMCNP TR Card (translation at origin):")
        print(f"  *TRn  0 0 0  &")
        print(f"        {R[0,0]:.6f} {R[0,1]:.6f} {R[0,2]:.6f}  &")
        print(f"        {R[1,0]:.6f} {R[1,1]:.6f} {R[1,2]:.6f}  &")
        print(f"        {R[2,0]:.6f} {R[2,1]:.6f} {R[2,2]:.6f}")

    # Validation
    print("\nValidation:")

    row_norms = [np.linalg.norm(R[i,:]) for i in range(3)]
    print(f"  Row norms: [{row_norms[0]:.10f}, {row_norms[1]:.10f}, {row_norms[2]:.10f}]")

    dot_01 = np.dot(R[0,:], R[1,:])
    dot_02 = np.dot(R[0,:], R[2,:])
    dot_12 = np.dot(R[1,:], R[2,:])
    print(f"  Dot products: [{dot_01:.10f}, {dot_02:.10f}, {dot_12:.10f}]")

    det = np.linalg.det(R)
    print(f"  Determinant: {det:.10f}")

    # Check validity
    tolerance = 1e-6
    is_valid = (all(abs(norm - 1.0) < tolerance for norm in row_norms) and
                abs(dot_01) < tolerance and
                abs(dot_02) < tolerance and
                abs(dot_12) < tolerance and
                abs(abs(det) - 1.0) < tolerance)

    if is_valid:
        print("  Status: ✓ VALID rotation matrix")
    else:
        print("  Status: ✗ INVALID - corrections needed")

    print("="*60 + "\n")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Generate rotation matrices for MCNP TR cards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Euler angles (30° about x, 45° about y, 60° about z):
    python rotation_matrix_generator.py --euler 30 45 60 --degrees

  Axis-angle (30° about axis (1,1,1)):
    python rotation_matrix_generator.py --axis 1 1 1 --angle 30 --degrees

  Single-axis rotation (90° about z):
    python rotation_matrix_generator.py --rotate-z 90 --degrees
        """
    )

    # Rotation specification options
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--euler', nargs=3, type=float, metavar=('THETA_X', 'THETA_Y', 'THETA_Z'),
                       help='Euler angles (x-y-z convention)')

    group.add_argument('--rotate-x', type=float, metavar='ANGLE',
                       help='Rotation about x-axis')

    group.add_argument('--rotate-y', type=float, metavar='ANGLE',
                       help='Rotation about y-axis')

    group.add_argument('--rotate-z', type=float, metavar='ANGLE',
                       help='Rotation about z-axis')

    # Axis-angle requires both --axis and --angle
    parser.add_argument('--axis', nargs=3, type=float, metavar=('KX', 'KY', 'KZ'),
                        help='Rotation axis vector (for axis-angle representation)')

    parser.add_argument('--angle', type=float,
                        help='Rotation angle (for axis-angle representation)')

    # Common option
    parser.add_argument('--degrees', action='store_true',
                        help='Angles are in degrees (default: radians)')

    args = parser.parse_args()

    # Generate rotation matrix based on input
    if args.euler:
        theta_x, theta_y, theta_z = args.euler
        R = rotation_matrix_euler(theta_x, theta_y, theta_z, degrees=args.degrees)

        angle_unit = "degrees" if args.degrees else "radians"
        name = f"Euler Angles: θx={theta_x} θy={theta_y} θz={theta_z} {angle_unit}"
        print_matrix_info(R, name=name)

    elif args.rotate_x is not None:
        angle = args.rotate_x
        angle_rad = np.radians(angle) if args.degrees else angle
        R = rotation_matrix_x(angle_rad)

        angle_unit = "degrees" if args.degrees else "radians"
        name = f"Rotation about X-axis: {angle} {angle_unit}"
        print_matrix_info(R, name=name)

    elif args.rotate_y is not None:
        angle = args.rotate_y
        angle_rad = np.radians(angle) if args.degrees else angle
        R = rotation_matrix_y(angle_rad)

        angle_unit = "degrees" if args.degrees else "radians"
        name = f"Rotation about Y-axis: {angle} {angle_unit}"
        print_matrix_info(R, name=name)

    elif args.rotate_z is not None:
        angle = args.rotate_z
        angle_rad = np.radians(angle) if args.degrees else angle
        R = rotation_matrix_z(angle_rad)

        angle_unit = "degrees" if args.degrees else "radians"
        name = f"Rotation about Z-axis: {angle} {angle_unit}"
        print_matrix_info(R, name=name)

    elif args.axis and args.angle:
        axis = args.axis
        angle = args.angle
        R = rotation_matrix_axis_angle(axis, angle, degrees=args.degrees)

        angle_unit = "degrees" if args.degrees else "radians"
        name = f"Axis-Angle: k=({axis[0]}, {axis[1]}, {axis[2]}) θ={angle} {angle_unit}"
        print_matrix_info(R, name=name)

    else:
        parser.error("--axis requires --angle to be specified")


if __name__ == "__main__":
    main()
